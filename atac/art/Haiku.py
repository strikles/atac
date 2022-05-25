import random
import spacy
from spacy.matcher import Matcher
import syllapy


def generate_haiku():
    """ """
    nlp = spacy.load("en_core_web_sm")
    matcher2 = Matcher(nlp.vocab)
    matcher3 = Matcher(nlp.vocab)
    matcher4 = Matcher(nlp.vocab)
    #
    pattern = [
        {"POS": {"IN": ["NOUN", "ADP", "ADJ", "ADV"]}},
        {"POS": {"IN": ["NOUN", "VERB"]}},
    ]
    matcher2.add("TwoWords", [pattern])
    pattern = [
        {"POS": {"IN": ["NOUN", "ADP", "ADJ", "ADV"]}},
        {"IS_ASCII": True, "IS_PUNCT": False, "IS_SPACE": False},
        {"POS": {"IN": ["NOUN", "VERB", "ADJ", "ADV"]}},
    ]
    matcher3.add("ThreeWords", [pattern])
    pattern = [
        {"POS": {"IN": ["NOUN", "ADP", "ADJ", "ADV"]}},
        {"IS_ASCII": True, "IS_PUNCT": False, "IS_SPACE": False},
        {"IS_ASCII": True, "IS_PUNCT": False, "IS_SPACE": False},
        {"POS": {"IN": ["NOUN", "VERB", "ADJ", "ADV"]}},
    ]
    matcher4.add("FourWords", [pattern])
    #
    doc = nlp(open("data/orwell_1984.txt").read())
    #
    matches2 = matcher2(doc)
    matches3 = matcher3(doc)
    matches4 = matcher4(doc)
    #
    g_5 = []
    g_7 = []
    #
    for match_id, start, end in matches2 + matches3 + matches4:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        #
        syl_count = 0
        for token in span:
            syl_count += syllapy.count(token.text)
        if syl_count == 5:
            if span.text not in g_5:
                g_5.append(span.text)
        if syl_count == 7:
            if span.text not in g_7:
                g_7.append(span.text)
        #
        return "{}\n{}\n{}".format(
            random.choice(g_5), random.choice(g_7), random.choice(g_5)
        )
