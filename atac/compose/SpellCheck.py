import language_tool_python
from autocorrect import Speller

"""
def contextual_spellcheck(content, lang='en'):
    #
    nlp = spacy.load("en_core_web_sm")
    # nlp.pipe_names ['tok2vec', 'tagger', 'parser', 'ner', 'attribute_ruler', 'lemmatizer']
    # You can pass the optional parameters to the contextualSpellCheck
    # eg. pass max edit distance use config={"max_edit_dist": 3}
    nlp.add_pipe("contextual spellchecker")
    #nlp.pipe_names ['tok2vec', 'tagger', 'parser', 'ner', 'attribute_ruler', 'lemmatizer', 'contextual spellchecker']
    doc = nlp(content)
    if doc._.performed_spellCheck:
        translation = doc._.outcome_spellCheck
    #
    return translation
"""


def spelling_corrector(content, lang="en"):
    #
    spell = Speller(lang)
    return spell(content)


def correct_spelling_languagetool(content, lang="en"):
    spellchecker = language_tool_python.LanguageToolPublicAPI(lang if lang else "en")
    spellchecker_matches = spellchecker.check(content)
    is_bad_rule = (
        lambda rule: rule.message == "Possible spelling mistake found."
        and len(rule.replacements)
        and rule.replacements[0][0].isupper()
    )
    spellchecker_matches = [
        rule for rule in spellchecker_matches if not is_bad_rule(rule)
    ]
    return language_tool_python.utils.correct(content, spellchecker_matches)
