import argparse
import os
import sys
import json
from threading import Thread
import atac


# sub-command functions
def send(arguments):
    #
    katie = atac.FromRuXiaWithLove()
    target = "email"
    path_emails = os.path.dirname(os.path.abspath(__file__)) + "/contacts/emails/"
    path_phones = os.path.dirname(os.path.abspath(__file__)) + "/contacts/phones/"
    subject = None
    #
    if getattr(arguments, "subject"):
        subject = getattr(arguments, "subject")
    if getattr(arguments, "message"):
        path_message = getattr(arguments, "message")
    if getattr(arguments, "target"):
        target = getattr(arguments, "target")
    if getattr(arguments, "path_emails"):
        path_emails = getattr(arguments, "path_emails")
    if getattr(arguments, "path_phones"):
        path_phones = getattr(arguments, "path_phones")
    #
    if "email" in target:
        katie.send_emails(path_emails, path_message, subject)
    if "whatsapp" in target and os.environ.get('DISPLAY'):
        katie.send_pywhatkit(path_phones, path_message)
    if "sms" in target:
        katie.send_twilio(path_phones, path_message, 'sms')
    if "facebook" in target:
        katie.send_facebook()
    if "twitter" in target:
        katie.send_twitter()


def scrape(arguments):
    #
    url = ""
    target = ""
    config = ""

    with open('auth.json') as json_file:
        config = json.load(json_file)
    if getattr(arguments, "url"):
        mango = atac.UnderTheMangoTree()
        url = getattr(arguments, "url")
        mango.process_page("url", url)
    elif getattr(arguments, "target"):
        mango = atac.UnderTheMangoTree()
        target = getattr(arguments, "target")
        mango.process_page(target, config['scrape']['targets'][target])
    else:
        # create threads
        mangos = dict()
        for data_key, starting_url in config['scrape']['targets'].items():
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
        

# create the top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# create the parser for the "send" command
parser_send = subparsers.add_parser('send')
parser_send.add_argument('-m', dest='message', type=str, help='path to message file')
parser_send.add_argument('-e', dest='path_emails', type=str, help='path to csv dir')
parser_send.add_argument('-p', dest='path_phones', type=str, help='path to csv dir')
parser_send.add_argument('-s', dest='subject', type=str, help='email subject')
parser_send.add_argument('-t', dest='target', choices=['email', 'facebook', 'twitter', 'whatsapp', 'sms', 'all'])
parser_send.set_defaults(func=send)

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