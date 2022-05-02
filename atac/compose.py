from .art import *
from .epicycle_drawing import *
from .config import Config

from datetime import datetime
from email import charset
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
import mistune
import os
import sys

from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

from googletrans import Translator

import attr
import nltk
import spacy
from collections import OrderedDict
from functools import partial
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from pywsd import disambiguate
from spellchecker import SpellChecker


# Penn TreeBank POS tags:
# http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
supported_pos_tags = [
    # 'CC',   # coordinating conjunction
    # 'CD',   # Cardinal number
    # 'DT',   # Determiner
    # 'EX',   # Existential there
    # 'FW',   # Foreign word
    # 'IN',   # Preposition or subordinating conjunction
    'JJ',   # Adjective
    # 'JJR',  # Adjective, comparative
    # 'JJS',  # Adjective, superlative
    # 'LS',   # List item marker
    # 'MD',   # Modal
    'NN',   # Noun, singular or mass
    'NNS',  # Noun, plural
    'NNP',  # Proper noun, singular
    'NNPS', # Proper noun, plural
    # 'PDT',  # Predeterminer
    # 'POS',  # Possessive ending
    # 'PRP',  # Personal pronoun
    # 'PRP$', # Possessive pronoun
    'RB',   # Adverb
    # 'RBR',  # Adverb, comparative
    # 'RBS',  # Adverb, superlative
    # 'RP',   # Particle
    # 'SYM',  # Symbol
    # 'TO',   # to
    # 'UH',   # Interjection
    'VB',   # Verb, base form
    'VBD',  # Verb, past tense
    'VBG',  # Verb, gerund or present participle
    'VBN',  # Verb, past participle
    'VBP',  # Verb, non-3rd person singular present
    'VBZ',  # Verb, 3rd person singular present
    # 'WDT',  # Wh-determiner
    # 'WP',   # Wh-pronoun
    # 'WP$',  # Possessive wh-pronoun
    # 'WRB',  # Wh-adverb
]


@attr.s
class SubstitutionCandidate:
    token_position = attr.ib()
    similarity_rank = attr.ib()
    original_token = attr.ib()
    candidate_word = attr.ib()


def vsm_similarity(doc, original, synonym):
    window_size = 3
    start = max(0, original.i - window_size)
    return doc[start: original.i + window_size].similarity(synonym)


def _get_wordnet_pos(spacy_token):
    '''Wordnet POS tag'''
    pos = spacy_token.tag_[0].lower()
    if pos in ['a', 'n', 'v']:
        return pos


def _synonym_prefilter_fn(token, synonym):
    '''
    Similarity heuristics go here
    '''
    if  (len(synonym.text.split()) > 2) or \
        (synonym.lemma == token.lemma) or \
        (synonym.tag != token.tag) or \
        (token.text.lower() == 'be'):
        return False
    else:
        return True


def _generate_synonym_candidates(doc, disambiguate=False, rank_fn=None, nlp=None):
    '''
    Generate synonym candidates.
    For each token in the doc, the list of WordNet synonyms is expanded.
    the synonyms are then ranked by their GloVe similarity to the original
    token and a context window around the token.
    :param disambiguate: Whether to use lesk sense disambiguation before
            expanding the synonyms.
    :param rank_fn: Functions that takes (doc, original_token, synonym) and
            returns a similarity score
    '''
    if rank_fn is None:
        rank_fn=vsm_similarity

    candidates = []
    for position, token in enumerate(doc):
        if token.tag_ in supported_pos_tags:
            wordnet_pos = _get_wordnet_pos(token)
            wordnet_synonyms = []
            if disambiguate:
                try:
                    synset = disambiguate(
                           doc.text, token.text, pos=wordnet_pos)
                    wordnet_synonyms = synset.lemmas()
                except:
                    continue
            else:
                synsets = wn.synsets(token.text, pos=wordnet_pos)
                for synset in synsets:
                    wordnet_synonyms.extend(synset.lemmas())

            synonyms = []
            for wordnet_synonym in wordnet_synonyms:
                spacy_synonym = nlp(wordnet_synonym.name().replace('_', ' '))[0]
                synonyms.append(spacy_synonym)

            synonyms = filter(partial(_synonym_prefilter_fn, token),
                              synonyms)
            synonyms = reversed(sorted(synonyms,
                                key=partial(rank_fn, doc, token)))

            for rank, synonym in enumerate(synonyms):
                candidate_word = synonym.text
                candidate = SubstitutionCandidate(
                        token_position=position,
                        similarity_rank=rank,
                        original_token=token,
                        candidate_word=candidate_word)
                candidates.append(candidate)

        return candidates


def _generate_typo_candidates(doc, min_token_length=4, rank=1000):
    candidates = []
    spell = SpellChecker()

    for position, token in enumerate(doc):
        if (len(token)) < min_token_length:
            continue

        for typo in spell.unknown(token.text.split(" ")):
            candidate = SubstitutionCandidate(
                    token_position=position,
                    similarity_rank=rank,
                    original_token=token,
                    candidate_word=typo)
            candidates.append(candidate)

    return candidates


def _compile_perturbed_tokens(doc, accepted_candidates):
    '''
    Traverse the list of accepted candidates and do the token substitutions.
    '''
    candidate_by_position = {}
    for candidate in accepted_candidates:
        candidate_by_position[candidate.token_position] = candidate

    final_tokens = []
    for position, token in enumerate(doc):
        word = token.text
        if position in candidate_by_position:
            candidate = candidate_by_position[position]
            word = candidate.candidate_word.replace('_', ' ')
        final_tokens.append(word)

    return final_tokens


def perturb_text(
        doc,
        use_typos=True,
        rank_fn=None,
        heuristic_fn=None,
        halt_condition_fn=None,
        nlp=None,
        verbose=False):
    '''
    Perturb the text by replacing some words with their WordNet synonyms,
    sorting by GloVe similarity between the synonym and the original context
    window, and optional heuristic.
    :param doc: Document to perturb.
    :type doc: spacy.tokens.doc.Doc
    :param rank_fn: See `_generate_synonym_candidates``.
    :param heuristic_fn: Ranks the best synonyms using the heuristic.
            If the value of the heuristic is negative, the candidate
            substitution is rejected.
    :param halt_condition_fn: Returns true when the perturbation is
            satisfactory enough.
    :param verbose:
    '''

    heuristic_fn = heuristic_fn or (lambda _, candidate: candidate.similarity_rank)
    halt_condition_fn = halt_condition_fn or (lambda perturbed_text: False)
    candidates = _generate_synonym_candidates(doc, rank_fn=rank_fn, nlp=nlp)
    if use_typos:
        candidates.extend(_generate_typo_candidates(doc))

    perturbed_positions = set()
    accepted_candidates = []
    perturbed_text = doc.text
    if verbose:
        print('Got {} candidates'.format(len(candidates)))

    sorted_candidates = zip(
            map(partial(heuristic_fn, perturbed_text), candidates),
            candidates)
    sorted_candidates = list(sorted(sorted_candidates,
            key=lambda t: t[0]))

    while len(sorted_candidates) > 0 and not halt_condition_fn(perturbed_text):
        score, candidate = sorted_candidates.pop()
        if score < 0:
            continue
        if candidate.token_position not in perturbed_positions:
            perturbed_positions.add(candidate.token_position)
            accepted_candidates.append(candidate)
            if verbose:
                print('Candidate:', candidate)
                print('Candidate score:', heuristic_fn(perturbed_text, candidate))
                print('Candidate accepted.')
            perturbed_text = ' '.join(
                    _compile_perturbed_tokens(doc, accepted_candidates))

            if len(sorted_candidates) > 0:
                _, candidates = zip(*sorted_candidates)
                sorted_candidates = zip(
                        map(partial(heuristic_fn, perturbed_text),
                            candidates),
                        candidates)
                sorted_candidates = list(sorted(sorted_candidates,
                        key=lambda t: t[0]))
    return perturbed_text


def get_paraphrase(text, nlp):
    print('Original text:', text)
    doc = nlp(text)
    perturbed_text = perturb_text(doc, verbose=True, nlp=nlp)
    print('Perturbed text:', perturbed_text)
    return perturbed_text


class AllTimeHigh(Config):
    """ A class used to represent a Configuration object

    Attributes
    ----------
    key : str
        a encryption key
    data : dict
        configuration data
    encrypted_config : bool
        use an encrypted configuration file
    config_file_path : str
        path to the configuration file
    key_file_path : str
        path to encryption key file
    gpg : gnupg.GPG
        python-gnupg gnupg.GPG
    """

    """
    Methods
    -------
    generate_key()
        Generates a new encryption key from a password + salt
    """

    @staticmethod
    def fix_mixed_encoding(s):
        """ Fixed mixed encoding

        Parameters
        ----------
        s : str
            The mixed encoding string to fix
        """
        output = ''
        ii = 0
        for _ in s:
            if ii <= len(s)-1:
                if s[ii] == '\\' and s[ii+1] == 'x':
                    b = s[ii:ii+4].encode('ascii').decode('utf-8')
                    output = output+b
                    ii += 3
                else:
                    output = output+s[ii]
            ii += 1
        #
        return output


    @staticmethod
    def get_datetime():
        """ Return datetime string

        """
        # datetime object containing current date and time
        now = datetime.now()
        # print("now =", now)
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)
        #
        return dt_string


    @staticmethod
    def compose_email(sender_email, mailing_list, message_content, subject, do_paraphrase, translate_to_languagecode=None):

        """ Compose MIMEMultipart email message

        Parameters
        ----------
        sender_email : str
            The name of the animal
        mailing_list : list
            The sound the animal makes
        message_content : str
            The message content to send
        subject : str
            The email subject
        """
        message = MIMEMultipart("mixed")
        cs = charset.Charset('utf-8')
        cs.header_encoding = charset.QP
        cs.body_encoding = charset.QP
        message.set_charset(cs)
        message.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        nlp = None
        translator = None
        #
        message["Subject"] = subject
        if do_paraphrase:
            nlp = spacy.load('en_core_web_sm')
            subject_transform = get_paraphrase(subject_transform, nlp)
        if translate_to_languagecode:
            translator = Translator()
            subject_transform = translator.translate(subject_transform, translate_to_languagecode)
            message["Subject"] = subject_transform    
        #
        message["From"] = sender_email
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        body = MIMEMultipart("alternative")
        body.set_charset(cs)
        body.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        lines = None
        if not do_paraphrase:
            lines = message_content
        else:
            lines = []
            print("compose: "+json.dumps(message_content, indent=4))
            for phrase in message_content:
                phrase_transform = phrase
                if bool(BeautifulSoup(phrase_transform, "html.parser").find()):
                    lines.append(phrase_transform)
                elif not phrase_transform:
                    lines.append('\n')
                else:
                    if do_paraphrase:
                        phrase_transform = get_paraphrase(phrase, nlp)
                    if translate_to_languagecode:
                        translator = Translator()
                        phrase_transform = translator.translate(phrase_transform, translate_to_languagecode)
                lines.append(phrase_transform)
        #
        print("text: "+json.dumps(lines, indent=4))
        message_str = "\n".join(lines)
        soup = BeautifulSoup(message_str)
        text = soup.get_text()
        html = "<p align='center' width='100%'><img height='300' src='cid:header'></p>" + mistune.html(message_str) + "<p align='center' width='100%'><img height='300' src='cid:signature'></p>"
        # Turn these into plain/html MIMEText objects
        part1 = MIMENonMultipart('text', 'plain', charset='utf-8')
        part2 = MIMENonMultipart('text', 'html', charset='utf-8')
        part1.set_payload(text, charset=cs)
        part2.set_payload(html, charset=cs)
        # Add HTML/plain-text parts to MIMEMultipart message
        body.attach(part1)
        body.attach(part2)
        # The email client will try to render the last part first
        message.attach(body)
        print(message.as_string())
        #
        hfp = open('data/assets/img/jesus/jesus_king.png', 'rb')
        msg_image_header = MIMEImage(hfp.read())
        hfp.close()
        # Define the image's ID as referenced above
        msg_image_header.add_header('Content-ID', '<header>')
        message.attach(msg_image_header)
        #
        sfp = open('data/assets/img/jesus/mary.png', 'rb')
        msg_image_signature = MIMEImage(sfp.read())
        sfp.close()
        # Define the image's ID as referenced above
        msg_image_signature.add_header('Content-ID', '<signature>')
        message.attach(msg_image_signature)
        #
        return message
