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
    subject = "Cibertortura, Cibersodomia e angariação de ódios entre a população - Exoneração imediata de ex-alunos do colégio militar associados a Pedro Miguel De Brito Esteves Grilo"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_pt.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    #
    '''
    subject = "Cibertortura, Cibersodomia e angariação de ódios entre a população - Exoneração imediata de ex-alunos do colégio militar associados a Pedro Miguel De Brito Esteves Grilo"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/ferronha_colete.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    '''
    #
    '''
    subject = "Cibertortura, Cibersodomia e angariação de ódios entre a população - Exoneração imediata de ex-alunos do colégio militar associados a Luís Nazareth Carvalho Figueira"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_duarte.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    '''
    #
    '''
    subject = "Cibertortura, Cibersodomia e angariação de ódios entre a população - Exoneração imediata de ex-alunos do colégio militar"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_brito.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    '''
    #
    '''
    subject = "espectáculos extrajudiciais de cibertortura e automutilação genital na polícia portuguesa e governo português versus prevenção de pedofilia no caso de Madelin McCann - Exoneração imediata de ex-alunos do colégio militar associados a Pedro Miguel De Brito Esteves Grilo"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/ferronha_colete.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    '''
    #
    '''
    subject = "Elect the former colegio militar student (from largo da Luz, Portugal) Pedro Miguel de Brito Esteves Grilo @PSP Portugal the dumbest policeman in the world"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_grilo.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    '''
    #
    '''
    subject = "Elect the former colegio militar student (from largo da Luz, Portugal) Nuno Poiares @PSP Portugal the dumbest policeman from sci division in the world"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_poiares.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    '''
    
    recipients = [
        'indiaoffice@macfound.org',
        'info-ng@macfound.org',
        '4answers@macfound.org'
        ]
    #
    subject = "Elect the former colegio militar student (from largo da Luz, Portugal) Nuno Poiares @PSP Portugal the dumbest policeman from sci division in the world"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_poiares.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    #
    subject = "This is a request for emergency humanitarian help to address the threat the hate mongering Portuguese police represents to the families of their cybertorture victims"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_figueira.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    #
    subject = "Espectáculos extrajudiciais de cibertortura e automutilação genital na polícia portuguesa e governo português versus prevenção de pedofilia no caso de Madelin McCann - Exoneração imediata de ex-alunos do colégio militar associados a Pedro Miguel De Brito Esteves Grilo"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/ferronha_colete.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    #
    subject = "Sentenças extrajudiciais de cibertortura, cybersodomy e angariação de ódios entre a população - Exoneração imediata de ex-alunos do colégio militar associados a Pedro Miguel De Brito Esteves Grilo e internamento compulsivo de Carla Maria Marinho Rodrigues”
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_duarte.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    #
    subject = "Sentenças extrajudiciais de cibertortura, cybersodomy e angariação de ódios entre a população - Exoneração imediata de ex-alunos do colégio militar associados a Pedro Miguel De Brito Esteves Grilo e internamento compulsivo de Carla Maria Marinho Rodrigues”
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_brito.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    #
    subject = "Elect the former colegio militar student (from largo da Luz, Portugal) Pedro Miguel de Brito Esteves Grilo @PSP Portugal the dumbest policeman in the world"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_grilo.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    #
    subject = "Elect Carla Maria Marinho Rodrigues the dumbest women in the world for participating in cybertorture and cybersodomy sex parties to force extrajudicial sentences of genital self-harm and compulsory psychiatric care in criminal association with Portuguese law enforcement after turning my father into a cripple"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_maria.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True


#@pytest.mark.skip(reason="we fight spam :)")
def test_send_emails():
    """
    """
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    email_files_path = os.getcwd() + "/atac/tests/test_emails.csv"
    message_file_path = os.getcwd() + "/atac/tests/test_message.md"
    #
    subject = "Madeline McCann, Cybertorture extrajudicial trial and sentences and the hate mongering Portuguese Police"
    status = katie.send_emails(email_files_path, message_file_path, subject)
    assert(status == 0) is True
    #
    email_files_path = os.getcwd() + "/atac/tests/test_emails.csv"
    message_file_path = os.getcwd() + "/atac/tests/test_message_figueira.md"
    subject = "This is a request for emergency humanitarian help to address the threat the Portuguese police represents to the families of their cybertorture victims"
    status = katie.send_emails(email_files_path, message_file_path, subject)
    assert(status == 0) is True
