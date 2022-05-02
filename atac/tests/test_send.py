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
        'contacto@psp.pt',
        'geral@prociv.pt',
        'gnr@gnr.pt',
        'mail@ansr.pt',
        'sef@sef.pt',
        'geral@igai.pt',
        'sec.geral.mai@sg.mai.gov.pt',
        'geral@igai.pt',
        'info@gulbenkian.pt',
        'agenda.informacao@rtp.pt',
        'raymond.marshall@guinnessworldrecords.com',
        'press@guinnessworldrecords.com'
    ]

    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    mailing_list = random.sample(recipients, 1).pop()
    #
    subject = "NeuroRights and Blue-whale suicide games abusing biophotonics to exact Cybertorture in order to force the SUT to complete tasks to bargain for relief"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/cybertorture.md")), "message")
    print(os.path.abspath(os.getcwd()))
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, False)
    assert(status == 0) is True
    #
    
    recipients = [
        'indiaoffice@macfound.org',
        'info-ng@macfound.org',
        '4answers@macfound.org'
    ]
    #
    subject = "neuro-ights and blue-hwale suicide games: Jasper Kums and colégio militar alumni gamble with life and direct violence inducing synthetic psychosis in the middle of the night abusing biophotonics to direct violence against parents, women and children"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/devil.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, False)
    assert(status == 0) is True

    subject = "neuro-rights and blue-whale suicide games - colégio militar alumni and criminal associates participate in interactive human degradation spectacles to turn people homeless and force them into poverty, gambling lifes in blue whale suicide games where they take turns abusing biophotonics to exact vibrotactile cybertorture, force psychosis and simulate Van Gogh syndrome in a style reminiscent of Matthew Puncher's murder"
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/neurorights.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, False)
    assert(status == 0) is True

#@pytest.mark.skip(reason="we fight spam :)")
def test_send_emails():
    """
    """

    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    email_files_path = os.path.join(os.getcwd(), "atac/tests/test_emails.csv")
    message_file_path = os.path.join(os.getcwd(), "data/messages/email/devil.md")
    #
    subject = "Neuro Rights and Blue Whale Suicide Games: Jasper Kums and Colegio Militar alumni gamble with life and direct violence inducing synthetic psychosis in the middle of the night abusing biophotonics to direct violence against parents, women and children"
    status = katie.send_emails(email_files_path, message_file_path, subject, False)
    assert(status == 0) is True
