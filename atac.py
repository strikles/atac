import argparse
import os
import sys
import json
from threading import Thread
import atac


def get_config_arguments(arguments):
    #
    encrypted_config = True
    key_file_path = None
    config_file_path = 'auth.json'
    #
    if getattr(arguments, "encrypted_config"):
        encrypted_config = getattr(arguments, "encrypted_config")
    if getattr(arguments, "config_file"):
        config_file_path = getattr(arguments, "config_file")
    if getattr(arguments, "key_file"):
        key_file_path = getattr(arguments, "key_file")
    #
    return encrypted_config, config_file_path, key_file_path

# sub-command functions
def config(arguments):
    #
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    config = atac.Config(encrypted_config, config_file_path, key_file_path)
    #
    if getattr(arguments, "generate_key_file"):
        generate_key_file_path = getattr(arguments, "generate_key_file")
        if generate_key_file_path:
            config.generate_key()
            config.save_key(generate_key_file_path)
    if getattr(arguments, "new_config_file"):
        new_config_file_path = getattr(arguments, "new_config_file")
        if new_config_file_path:
            config.new_config(new_config_file_path, encrypted_config)
    if getattr(arguments, "decrypted_config_file"):
        decrypted_config_file_path = getattr(arguments, "decrypted_config_file")
        if decrypted_config_file_path:
            config.save_config(decrypted_config_file_path, False)

# sub-command functions
def email(arguments):
    #
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file_path, key_file_path)
    #
    target = "smtp"
    email_files_path = os.path.dirname(os.path.abspath(__file__)) + "/contacts/emails/"
    subject = None
    #
    if getattr(arguments, "subject"):
        subject = getattr(arguments, "subject")
    if getattr(arguments, "message_file"):
        message_file_path = getattr(arguments, "message_file")
    if getattr(arguments, "emails_file"):
        email_files_path = getattr(arguments, "emails_file")
    if getattr(arguments, "target"):
        target = getattr(arguments, "target")
    #
    if "smtp" in target:
        katie.send_emails(email_files_path, message_file_path, subject)

# sub-command functions
def phone(arguments):
    #
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file_path, key_file_path)
    #
    target = "whatsapp"
    phone_files_path = os.path.dirname(os.path.abspath(__file__)) + "/contacts/phones/"
    subject = None
    #
    if getattr(arguments, "message_file"):
        message_file_path = getattr(arguments, "message_file")
    if getattr(arguments, "phones_file"):
        phone_files_path = getattr(arguments, "phones_file")
    if getattr(arguments, "target"):
        target = getattr(arguments, "target")
    #
    if "whatsapp" in target and os.environ.get('DISPLAY'):
        katie.send_pywhatkit(phone_files_path, message_file_path)
    if "sms" in target:
        katie.send_twilio(phone_files_path, message_file_path, 'sms')

# sub-command functions
def social(arguments):
    #
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file_path, key_file_path)
    #
    target = "twitter"
    #
    if getattr(arguments, "message_file"):
        message_file_path = getattr(arguments, "message_file")
    if getattr(arguments, "target"):
        target = getattr(arguments, "target")
    #
    if "facebook" in target:
        katie.send_facebook()
    if "twitter" in target:
        katie.send_twitter()

def scrape(arguments):
    #
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    #
    url = ""
    target = ""
    #
    if getattr(arguments, "url"):
        url = getattr(arguments, "url")
        mango = atac.UnderTheMangoTree(encrypted_config, config_file_path, key_file_path)
        mango.process_page("url", url)
    elif getattr(arguments, "target"):
        target = getattr(arguments, "target")
        mango = atac.UnderTheMangoTree(encrypted_config, config_file_path, key_file_path)
        mango.process_page(target, mango.scrape['targets'][target])
    else:
        # create threads
        mangos = dict()
        config = atac.Config(encrypted_config, config_file_path, key_file_path)
        for data_key, starting_url in config.data['scrape']['targets'].items():
            print("{0} - {1}".format(data_key, starting_url))
            mangos[data_key] = atac.UnderTheMangoTree(encrypted_config, config_file_path, key_file_path)
            catcher_thread = Thread(
                target=mangos[data_key].process_page, args=(data_key, starting_url)
            )
            catcher_thread.start()

def compose(arguments):
    #
    corpus = os.path.dirname(os.path.abspath(__file__)) + '/assets/pg1009.txt'
    #
    if getattr(arguments, "corpus"):
        target = getattr(arguments, "corpus")
    #
    two_bach = atac.AllTimeHigh()
    two_bach.gen_content(corpus)
    
def clean(arguments):
    #
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    leon = atac.Leon(encrypted_config, config_file_path, key_file_path)
    #
    email_files_path = os.path.dirname(os.path.abspath(__file__)) + "/contacts/emails/"
    phone_files_path = os.path.dirname(os.path.abspath(__file__)) + "/contacts/phones/"
    #
    if getattr(arguments, "target"):
        target = getattr(arguments, "target")
    #
    if "email" in target:
        leon.clean_emails(email_files_path)
    if "phone" in target:
        leon.clean_phones(phone_files_path)
    else:
        leon.clean_emails(email_files_path)
        leon.clean_phones(phone_files_path)

# create the top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# create the parser for the "config" command
parser_config = subparsers.add_parser('config')
parser_config.add_argument('-c', dest='config_file', type=str, help='config file')
parser_config.add_argument('-e', dest='encrypted_config', choices=[True, False], nargs='?', const=True, default=True)
parser_config.add_argument('-k', dest='key_file', type=str, help='key file path')
parser_config.add_argument('-g', dest='generate_key_file', type=str, help='generate key file')
parser_config.add_argument('-d', dest='decrypted_config_file', type=str, help='decrypted config file')
parser_config.add_argument('-n', dest='new_config_file', type=str, help='new config file')
parser_config.set_defaults(func=config)

# create the parser for the "email command
parser_email = subparsers.add_parser('email')
parser_email.add_argument('-c', dest='config_file', type=str, help='config file')
parser_email.add_argument('-e', dest='encrypted_config', choices=[True, False], nargs='?', const=True, default=True)
parser_email.add_argument('-k', dest='key_file', type=str, help='key file path')
parser_email.add_argument('-m', dest='message_file', type=str, help='path to message file')
parser_email.add_argument('-p', dest='emails_file', type=str, help='path to csv dir')
parser_email.add_argument('-s', dest='subject', type=str, help='email subject')
parser_email.add_argument('-t', dest='target', choices=['smtp', 'aws'])
parser_email.add_argument('-v', dest='verbose')
parser_email.set_defaults(func=email)

# create the parser for the "phone" command
parser_phone = subparsers.add_parser('phone')
parser_phone.add_argument('-c', dest='config_file', type=str, help='config file')
parser_phone.add_argument('-e', dest='encrypted_config', choices=[True, False], nargs='?', const=True, default=True)
parser_phone.add_argument('-k', dest='key_file', type=str, help='key file path')
parser_phone.add_argument('-m', dest='message_file', type=str, help='path to message file')
parser_phone.add_argument('-p', dest='phones_file', type=str, help='path to csv dir')
parser_phone.add_argument('-t', dest='target', choices=['whatsapp', 'sms'])
parser_phone.add_argument('-w', dest='whatsapp', choices=['pywhatkit', 'twilio', 'yowsup'])
parser_phone.add_argument('-s', dest='sms', choices=['aws', 'twilio'])
parser_phone.add_argument('-v', dest='verbose')
parser_phone.set_defaults(func=phone)

# create the parser for the "social" command
parser_social = subparsers.add_parser('social')
parser_social.add_argument('-c', dest='config_file', type=str, help='config file')
parser_social.add_argument('-e', dest='encrypted_config', choices=[True, False], nargs='?', const=True, default=True)
parser_social.add_argument('-k', dest='key_file', type=str, help='key file path')
parser_social.add_argument('-m', dest='message', type=str, help='path to message file')
parser_social.add_argument('-t', dest='target', choices=['facebook', 'twitter'])
parser_social.add_argument('-v', dest='verbose')
parser_social.set_defaults(func=social)

# create the parser for the "scrape" command
parser_scrape = subparsers.add_parser('scrape')
parser_scrape.add_argument('-c', dest='config_file', type=str, help='config file')
parser_scrape.add_argument('-e', dest='encrypted_config', choices=[True, False], nargs='?', const=True, default=True)
parser_scrape.add_argument('-k', dest='key_file', type=str, help='key file path')
parser_scrape.add_argument('-t', dest='target', choices=['museums', 'embassies', 'activism', 'education', 'religion', 'rescue', 'addiction', 'music', 'journalists', 'defense', 'ukraine', 'islam', 'all'])
parser_scrape.add_argument('-u', dest='url', help="The URL to scrape.")
parser_scrape.add_argument('-v', dest='verbose')
parser_scrape.set_defaults(func=scrape)

# create the parser for the "compose" command
parser_compose = subparsers.add_parser('compose')
parser_compose.add_argument('-c', dest='corpus', type=str, help='path to corpus')
parser_compose.add_argument('-v', dest='verbose')
parser_compose.set_defaults(func=compose)

# create the parser for the "compose" command
parser_clean = subparsers.add_parser('clean')
parser_clean.add_argument('-c', dest='config_file', type=str, help='config file')
parser_clean.add_argument('-e', dest='encrypted_config', choices=[True, False], nargs='?', const=True, default=True)
parser_clean.add_argument('-k', dest='key_file', type=str, help='key file path')
parser_clean.add_argument('-t', dest='target', choices=['email', 'phone', 'all'])
parser_clean.add_argument('-v', dest='verbose')
parser_clean.set_defaults(func=clean)

# parse the args and call whatever function was selected
args = parser.parse_args()
args.func(args)