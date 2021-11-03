import argparse
import os
import sys
import json
from threading import Thread
import atac


# sub-command functions
def email(arguments):
    #
    katie = atac.FromRuXiaWithLove()
    target = "smtp"
    path_emails = os.path.dirname(os.path.abspath(__file__)) + "/contacts/emails/"
    subject = None
    #
    if getattr(arguments, "subject"):
        subject = getattr(arguments, "subject")
    if getattr(arguments, "message_file"):
        path_message = getattr(arguments, "message_file")
    if getattr(arguments, "emails_file"):
        path_emails = getattr(arguments, "emails_file")
    if getattr(arguments, "target"):
        target = getattr(arguments, "target")
    #
    if "smtp" in target:
        katie.send_emails(path_emails, auth_ndx, content_ndx, path_message, subject)


# sub-command functions
def phone(arguments):
    #
    katie = atac.FromRuXiaWithLove()
    target = "whatsapp"
    path_phones = os.path.dirname(os.path.abspath(__file__)) + "/contacts/phones/"
    subject = None
    #
    if getattr(arguments, "message_file"):
        path_message = getattr(arguments, "message_file")
    if getattr(arguments, "phones_file"):
        path_phones = getattr(arguments, "phones_file")
    if getattr(arguments, "target"):
        type = getattr(arguments, "target")
    #
    if "whatsapp" in target and os.environ.get('DISPLAY'):
        katie.send_pywhatkit(path_phones, path_message)
    if "sms" in target:
        katie.send_twilio(path_phones, path_message, 'sms')


# sub-command functions
def social(arguments):
    #
    katie = atac.FromRuXiaWithLove()
    target = "twitter"
    #
    if getattr(arguments, "message_file"):
        path_message = getattr(arguments, "message_file")
    if getattr(arguments, "target"):
        target = getattr(arguments, "target")
    #
    if "facebook" in target:
        katie.send_facebook()
    if "twitter" in target:
        katie.send_twitter()


# sub-command functions
def config(arguments):
    #
    config = atac.Config()
    config.load_config()
    encrypt = False
    #
    if getattr(arguments, "encrypt"):
        encrypt = getattr(arguments, "encrypt")
        if encrypt:
            config.load_decrypted()
            config.save_config()
    if getattr(arguments, "key"):
        key = getattr(arguments, "key")
        if key:
            config.gen_key()
    if getattr(arguments, "load"):
        load = getattr(arguments, "load")
        if load:
            config.load_config()
    if getattr(arguments, "new"):
        new = getattr(arguments, "new")
        if new:
            config.new_config()


def scrape(arguments):
    #
    url = ""
    target = ""
    #
    if getattr(arguments, "url"):
        mango = atac.UnderTheMangoTree()
        url = getattr(arguments, "url")
        mango.process_page("url", url)
    elif getattr(arguments, "target"):
        mango = atac.UnderTheMangoTree()
        target = getattr(arguments, "target")
        mango.process_page(target, mango.config.data['scrape']['targets'][target])
    else:
        # create threads
        mangos = dict()
        for data_key, starting_url in mango.config.data['scrape']['targets'].items():
            print("{0} - {1}".format(data_key, starting_url))
            mangos[data_key] = atac.UnderTheMangoTree()
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
    path_emails = os.path.dirname(os.path.abspath(__file__)) + "/contacts/emails/"
    path_phones = os.path.dirname(os.path.abspath(__file__)) + "/contacts/phones/"
    leon = atac.Leon()
    
    if getattr(arguments, "target"):
        target = getattr(arguments, "target")
        
    if "email" in target:
        leon.clean_emails(path_emails)
    if "phone" in target:
        leon.clean_phones(path_phones)
    else:
        leon.clean_emails(path_emails)
        leon.clean_phones(path_phones)
        
config = atac.Config()
config.gen_key()
config.load_decrypted()
config.save_config()
config.load_config()
            
# create the top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# create the parser for the "email command
parser_email = subparsers.add_parser('email')
parser_email.add_argument('-m', dest='message_file', type=str, help='path to message file')
parser_email.add_argument('-e', dest='emails_file', type=str, help='path to csv dir')
parser_email.add_argument('-s', dest='subject', type=str, help='email subject')
parser_email.add_argument('-t', dest='target', choices=['smtp', 'aws'])
parser_email.set_defaults(func=email)

# create the parser for the "phone" command
parser_phone = subparsers.add_parser('phone')
parser_phone.add_argument('-m', dest='message_file', type=str, help='path to message file')
parser_phone.add_argument('-p', dest='phones_file', type=str, help='path to csv dir')
parser_phone.add_argument('-t', dest='target', choices=['whatsapp', 'sms'])
parser_phone.add_argument('-w', dest='whatsapp', choices=['pywhatkit', 'twilio', 'yowsup'])
parser_phone.add_argument('-s', dest='sms', choices=['aws', 'twilio'])
parser_phone.set_defaults(func=phone)

# create the parser for the "social" command
parser_social = subparsers.add_parser('social')
parser_social.add_argument('-m', dest='message', type=str, help='path to message file')
parser_social.add_argument('-t', dest='target', choices=['facebook', 'twitter'])
parser_social.set_defaults(func=social)

# create the parser for the "config" command
parser_config = subparsers.add_parser('config')
parser_config.add_argument('-e', dest='encrypt', choices=['true', 'false'])
parser_config.add_argument('-k', dest='key', choices=['true', 'false'])
parser_config.add_argument('-l', dest='load', choices=['true', 'false'])
parser_config.add_argument('-n', dest='new', choices=['true', 'false'])
parser_config.set_defaults(func=config)

# create the parser for the "scrape" command
parser_scrape = subparsers.add_parser('scrape')
parser_scrape.add_argument('-t', dest='target', choices=['museums', 'embassies', 'activism', 'education', 'religion', 'rescue', 'addiction', 'music', 'journalists', 'defense', 'ukraine', 'islam', 'all'])
parser_scrape.add_argument('-u', dest='url', help="The URL to scrape.")
parser_scrape.set_defaults(func=scrape)

# create the parser for the "compose" command
parser_compose = subparsers.add_parser('compose')
parser_compose.add_argument('-c', dest='corpus', type=str, help='path to corpus')
parser_compose.set_defaults(func=compose)

# create the parser for the "compose" command
parser_clean = subparsers.add_parser('clean')
parser_clean.add_argument('-t', dest='target', choices=['email', 'phone', 'all'])
parser_clean.set_defaults(func=clean)

# parse the args and call whatever function was selected
args = parser.parse_args()
args.func(args)