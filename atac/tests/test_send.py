import os
import random
import sys
import pytest
import atac

encrypted_config = False
config_file = 'auth.json'
key_file = None


#@pytest.mark.skip(reason="we fight spam :)")
def test_send_email():
    """
    """
    recipients = [
        'raymond.marshall@guinnessworldrecords.com',
        'press@guinnessworldrecords.com',
        'indiaoffice@macfound.org',
        'info-ng@macfound.org',
        '4answers@macfound.org'
        'contacto@psp.pt',
        'geral@prociv.pt',
        'gnr@gnr.pt',
        'mail@ansr.pt',
        'sef@sef.pt',
        'geral@igai.pt',
        'sec.geral.mai@sg.mai.gov.pt',
        'geral@igai.pt',
        'info@gulbenkian.pt',
        'agenda.informacao@rtp.pt'
    ]
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    #
    subject = "neurorights and blue_whale suicide games: jasper_kums and colégio_militar alumni gamble with life and direct violence inducing synthetic psychosis in the middle of the night, abusing biophotonics to direct violence against parents, women and children"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/devil.md")), "message")
    print(os.path.abspath(os.getcwd()))
    mailing_list = "; ".join(recipients)
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=False, translate_to_languagecode=None)
    assert(status == 0) is True
    #
    subject = "neurorights and blue_whale suicide games: abusing biophotonics for cyber torture in order to force the subject under torture to complete tasks to bargain for relief"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/cybertorture.md")), "message")
    print(os.path.abspath(os.getcwd()))
    mailing_list = "; ".join(recipients)
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=False, translate_to_languagecode=None)
    assert(status == 0) is True
    #
    subject = "neurorights and blue_whale suicide games: colégio_militar alumni and criminal associates participate in interactive human degradation spectacles to turn people homeless, force them into poverty, gambling life in blue_whale suicide games where they take turns abusing bio photonics to exact vibrotactile cyber torture, force psychosis and simulate Van_Gogh syndrome in a style reminiscent of the murder of Matthew Puncher"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/neurorights.md")), "message")
    print(os.path.abspath(os.getcwd()))
    mailing_list = "; ".join(recipients)
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=False, translate_to_languagecode=None)
    assert(status == 0) is True


#@pytest.mark.skip(reason="we fight spam :)")
def test_send_email_with_translation():
    """
    """
    recipients = [
        'raymond.marshall@guinnessworldrecords.com',
        'press@guinnessworldrecords.com',
        'indiaoffice@macfound.org',
        'info-ng@macfound.org',
        '4answers@macfound.org'
        'contacto@psp.pt',
        'geral@prociv.pt',
        'gnr@gnr.pt',
        'mail@ansr.pt',
        'sef@sef.pt',
        'geral@igai.pt',
        'sec.geral.mai@sg.mai.gov.pt',
        'geral@igai.pt',
        'info@gulbenkian.pt',
        'agenda.informacao@rtp.pt'
    ]
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    #
    subject = "neurorights and blue_whale suicide games: Jasper Kums and colégio_militar alumni gamble with life and direct violence inducing synthetic psychosis in the middle of the night abusing biophotonics to direct violence against parents, women and children"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/devil.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=False, translate_to_languagecode="pt")
    assert(status == 0) is True
    #
    subject = "neurorights and blue_whale suicide games: abusing biophotonics for cyber torture in order to force the subject under torture to complete tasks to bargain for relief"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/cybertorture.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=False, translate_to_languagecode="pt")
    assert(status == 0) is True
    #
    subject = "neurorights and blue_whale suicide games: colégio_militar alumni and criminal associates participate in interactive human degradation spectacles to turn people homeless, force them into poverty, gambling life in blue_whale suicide games where they take turns abusing bio photonics to exact vibrotactile cyber torture, force psychosis and simulate Van_Gogh syndrome in a style reminiscent of the murder of Matthew Puncher"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/neurorights.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=False, translate_to_languagecode="pt")
    assert(status == 0) is True


#@pytest.mark.skip(reason="we fight spam :)")
def test_send_email_with_paraphrase():
    """
    """
    recipients = [
        'raymond.marshall@guinnessworldrecords.com',
        'press@guinnessworldrecords.com',
        'indiaoffice@macfound.org',
        'info-ng@macfound.org',
        '4answers@macfound.org'
        'contacto@psp.pt',
        'geral@prociv.pt',
        'gnr@gnr.pt',
        'mail@ansr.pt',
        'sef@sef.pt',
        'geral@igai.pt',
        'sec.geral.mai@sg.mai.gov.pt',
        'geral@igai.pt',
        'info@gulbenkian.pt',
        'agenda.informacao@rtp.pt'
    ]
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    #
    subject = "neurorights and blue_whale suicide games: Jasper Kums and colégio_militar alumni gamble with life and direct violence inducing synthetic psychosis in the middle of the night abusing biophotonics to direct violence against parents, women and children"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/devil.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=True, translate_to_languagecode=None)
    assert(status == 0) is True
    #
    subject = "neurorights and blue_whale suicide games: abusing biophotonics for cyber torture in order to force the subject under torture to complete tasks to bargain for relief"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/cybertorture.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=True, translate_to_languagecode=None)
    assert(status == 0) is True
    #
    subject = "neurorights and blue_whale suicide games: colégio_militar alumni and criminal associates participate in interactive human degradation spectacles to turn people homeless, force them into poverty, gambling life in blue_whale suicide games where they take turns abusing bio photonics to exact vibrotactile cyber torture, force psychosis and simulate Van_Gogh syndrome in a style reminiscent of the murder of Matthew Puncher"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/neurorights.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=True, translate_to_languagecode=None)
    assert(status == 0) is True


#@pytest.mark.skip(reason="we fight spam :)")
def test_send_emails_with_paraphrasing_and_translation():
    """
    """
    #
    target_languages = ['el', 'fr', 'it', 'ja', 'pt', 'uk', 'nl', 'la']
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    email_files_path = os.path.join(os.getcwd(), "atac/tests/contacts/test_emails.csv")
    #
    for lang_code in target_languages:
        #
        message_file_path = os.path.join(os.getcwd(), "data/messages/email/devil.md")
        subject = "neurorights and blue_whale suicide games: Jasper Kums and colégio_militar alumni gamble with life and direct violence inducing synthetic psychosis in the middle of the night abusing biophotonics to direct violence against parents, women and children"
        status = katie.send_emails(email_files_path, message_file_path, subject, True, lang_code)
        assert(status == 0) is True
        #
        message_file_path = os.path.join(os.getcwd(), "data/messages/email/cyber torture.md")
        subject = "neurorights and blue_whale suicide games: abusing biophotonics for cyber torture in order to force the subject under torture to complete tasks to bargain for relief"
        status = katie.send_emails(email_files_path, message_file_path, subject, True, lang_code)
        assert(status == 0) is True
        #
        message_file_path = os.path.join(os.getcwd(), "data/messages/email/neurorights.md")
        subject = "neurorights and blue_whale suicide games: colégio_militar alumni and criminal associates participate in interactive human degradation spectacles to turn people homeless, force them into poverty, gambling life in blue_whale suicide games where they take turns abusing bio photonics to exact vibrotactile cyber torture, force psychosis and simulate Van_Gogh syndrome in a style reminiscent of the murder of Matthew Puncher"
        status = katie.send_emails(email_files_path, message_file_path, subject, True, lang_code)
        assert(status == 0) is True
