import language_tool_python


def spellcheck(content, languagecode):
    spellchecker = language_tool_python.LanguageToolPublicAPI(languagecode if languagecode else 'en')
    spellchecker_matches = spellchecker.check(content)
    is_bad_rule = lambda rule: rule.message == 'Possible spelling mistake found.' and len(rule.replacements) and rule.replacements[0][0].isupper()
    spellchecker_matches = [rule for rule in spellchecker_matches if not is_bad_rule(rule)]
    phrase_transform = language_tool_python.utils.correct(content, spellchecker_matches)