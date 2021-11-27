import argparse
import os
from threading import Thread
import atac


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_config_arguments(arguments):
    """
    Generate New Config

    Parameters
    ----------
    name : str
        The name of the animal
    sound : str
        The sound the animal makes
    num_legs : int, optional
        The number of legs the animal (default is 4)
    """
    encrypted_config = True
    key_file_path = None
    config_file_path = 'auth.json'
    #
    if hasattr(arguments, "encrypted_config"):
        encrypted_config = hasattr(arguments, "encrypted_config")
        print("{} {}", encrypted_config, type(encrypted_config))
    if hasattr(arguments, "config_file"):
        config_file_path = hasattr(arguments, "config_file")
    if hasattr(arguments, "key_file"):
        key_file_path = hasattr(arguments, "key_file")
    #
    return encrypted_config, config_file_path, key_file_path


# sub-command functions
def configuration(arguments):
    """
    Generate New Config

    Parameters
    ----------
    name : str
        The name of the animal
    sound : str
        The sound the animal makes
    num_legs : int, optional
        The number of legs the animal (default is 4)
    """
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    config = atac.Config(encrypted_config, config_file_path, key_file_path)
    #
    if hasattr(arguments, "generate_key_file"):
        generate_key_file_path = hasattr(arguments, "generate_key_file")
        if generate_key_file_path:
            config.generate_key()
            config.save_key(generate_key_file_path)
    if hasattr(arguments, "new_config_file"):
        new_config_file_path = hasattr(arguments, "new_config_file")
        if new_config_file_path:
            config.new_config(new_config_file_path, encrypted_config)
    if hasattr(arguments, "decrypted_config_file"):
        decrypted_config_file_path = hasattr(arguments, "decrypted_config_file")
        if decrypted_config_file_path:
            config.load_config()
            config.save_config(decrypted_config_file_path, False)


# sub-command functions
def email(arguments):
    """
    Generate New Config

    Parameters
    ----------
    name : str
        The name of the animal
    sound : str
        The sound the animal makes
    num_legs : int, optional
        The number of legs the animal (default is 4)
    """
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file_path, key_file_path)
    #
    target = "smtp"
    email_files_path = os.path.dirname(os.path.abspath(__file__)) + "/data/contacts/emails/"
    subject = None
    #
    if hasattr(arguments, "subject"):
        subject = hasattr(arguments, "subject")
    if hasattr(arguments, "message_file"):
        message_file_path = hasattr(arguments, "message_file")
    if hasattr(arguments, "emails_file"):
        email_files_path = hasattr(arguments, "emails_file")
    if hasattr(arguments, "target"):
        target = hasattr(arguments, "target")
    #
    _, content = katie.get_email_config()
    #
    if not subject:
        subject = content['subject']
    #
    if not message_file_path:
        md = 'data/messages/email/' + content['markdown']
        message_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', md))
    #
    if "smtp" in target:
        katie.send_emails(email_files_path, message_file_path, subject)
        print(subject)


# sub-command functions
def phone(arguments):
    """
    Generate New Config

    Parameters
    ----------
    name : str
        The name of the animal
    sound : str
        The sound the animal makes
    num_legs : int, optional
        The number of legs the animal (default is 4)
    """
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file_path, key_file_path)
    #
    target = "whatsapp"
    phone_files_path = os.path.dirname(os.path.abspath(__file__)) + "/data/contacts/phones/"
    #
    if hasattr(arguments, "message_file"):
        message_file_path = hasattr(arguments, "message_file")
    if hasattr(arguments, "phones_file"):
        phone_files_path = hasattr(arguments, "phones_file")
    if hasattr(arguments, "target"):
        target = hasattr(arguments, "target")
    #
    if "whatsapp" in target and os.environ.get('DISPLAY'):
        katie.send_pywhatkit(phone_files_path, message_file_path)
    if "sms" in target:
        katie.send_twilio(phone_files_path, message_file_path, 'sms')


# sub-command functions
def social(arguments):
    """
    Generate New Config

    Parameters
    ----------
    name : str
        The name of the animal
    sound : str
        The sound the animal makes
    num_legs : int, optional
        The number of legs the animal (default is 4)
    """
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file_path, key_file_path)
    #
    target = "twitter"
    #
    if hasattr(arguments, "message_file"):
        message_file_path = hasattr(arguments, "message_file")
    if hasattr(arguments, "target"):
        target = hasattr(arguments, "target")
    #
    if "facebook" in target:
        katie.send_facebook(message_file_path)
    if "twitter" in target:
        katie.send_twitter(message_file_path)


def scrape(arguments):
    """
    Generate New Config

    Parameters
    ----------
    name : str
        The name of the animal
    sound : str
        The sound the animal makes
    num_legs : int, optional
        The number of legs the animal (default is 4)
    """
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    #
    url = ""
    target = ""
    #
    if hasattr(arguments, "url"):
        url = hasattr(arguments, "url")
        mango = atac.UnderTheMangoTree(encrypted_config, config_file_path, key_file_path)
        mango.process_page("url", url)
    elif hasattr(arguments, "target"):
        target = hasattr(arguments, "target")
        mango = atac.UnderTheMangoTree(encrypted_config, config_file_path, key_file_path)
        mango.process_page(target, mango.scrape['targets'][target])
    else:
        # create threads
        mangos = {}
        config = atac.Config(encrypted_config, config_file_path, key_file_path)
        for data_key, starting_url in config.data['scrape']['targets'].items():
            print("{0} - {1}".format(data_key, starting_url))
            mangos[data_key] = atac.UnderTheMangoTree(encrypted_config, config_file_path, key_file_path)
            catcher_thread = Thread(
                target=mangos[data_key].process_page, args=(data_key, starting_url)
            )
            catcher_thread.start()


def compose(arguments):
    """
    Generate New Config

    Parameters
    ----------
    name : str
        The name of the animal
    sound : str
        The sound the animal makes
    num_legs : int, optional
        The number of legs the animal (default is 4)
    """
    corpus_file_path = os.path.dirname(os.path.abspath(__file__)) + '/data/pg1009.txt'
    #
    if hasattr(arguments, "corpus"):
        corpus_file_path = hasattr(arguments, "corpus")
    #
    two_bach = atac.AllTimeHigh()
    two_bach.gen_content(corpus_file_path)


def clean(arguments):
    """
    Generate New Config

    Parameters
    ----------
    name : str
        The name of the animal
    sound : str
        The sound the animal makes
    num_legs : int, optional
        The number of legs the animal (default is 4)
    """
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    leon = atac.Leon(encrypted_config, config_file_path, key_file_path)
    #
    email_files_path = os.path.dirname(os.path.abspath(__file__)) + "/data/contacts/emails/"
    phone_files_path = os.path.dirname(os.path.abspath(__file__)) + "/data/contacts/phones/"
    #
    if hasattr(arguments, "target"):
        target = hasattr(arguments, "target")
    #
    if "email" in target:
        leon.clean_emails(email_files_path)
    if "phone" in target:
        leon.clean_phones(phone_files_path)
    else:
        leon.clean_emails(email_files_path)
        leon.clean_phones(phone_files_path)


if __name__ == "__main__":
    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the "config" command
    parser_config = subparsers.add_parser('config')
    parser_config.add_argument('-c', dest='config_file', type=str, help='config file')
    parser_config.add_argument('-e', dest='encrypted_config', action='store_false')
    parser_config.add_argument('-k', dest='key_file', type=str, help='key file path')
    parser_config.add_argument('-g', dest='generate_key_file', type=str, help='generate key file')
    parser_config.add_argument('-d', dest='decrypted_config_file', type=str, help='decrypted config file')
    parser_config.add_argument('-n', dest='new_config_file', type=str, help='new config file')
    parser_config.set_defaults(func=configuration)

    # create the parser for the "email command
    parser_email = subparsers.add_parser('email')
    parser_email.add_argument('-c', dest='config_file', type=str, help='config file')
    parser_email.add_argument('-e', dest='encrypted_config', action='store_false')
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
    parser_phone.add_argument('-e', dest='encrypted_config', action='store_false')
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
    parser_social.add_argument('-e', dest='encrypted_config', action='store_false')
    parser_social.add_argument('-k', dest='key_file', type=str, help='key file path')
    parser_social.add_argument('-m', dest='message', type=str, help='path to message file')
    parser_social.add_argument('-t', dest='target', choices=['facebook', 'twitter'])
    parser_social.add_argument('-v', dest='verbose')
    parser_social.set_defaults(func=social)

    # create the parser for the "scrape" command
    parser_scrape = subparsers.add_parser('scrape')
    parser_scrape.add_argument('-c', dest='config_file', type=str, help='config file')
    parser_scrape.add_argument('-e', dest='encrypted_config', action='store_false')
    parser_scrape.add_argument('-k', dest='key_file', type=str, help='key file path')
    parser_scrape.add_argument('-t', dest='target', choices=[
                                                                'museums',
                                                                'embassies',
                                                                'activism',
                                                                'education',
                                                                'religion',
                                                                'rescue',
                                                                'addiction',
                                                                'music',
                                                                'journalists',
                                                                'defense',
                                                                'ukraine',
                                                                'islam',
                                                                'all'
                                                            ])
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
    parser_clean.add_argument('-e', dest='encrypted_config', action='store_false')
    parser_clean.add_argument('-k', dest='key_file', type=str, help='key file path')
    parser_clean.add_argument('-t', dest='target', choices=['email', 'phone', 'all'])
    parser_clean.add_argument('-v', dest='verbose')
    parser_clean.set_defaults(func=clean)

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    args.func(args)
