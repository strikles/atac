from atac.util.Util import str2bool, get_file_content

import argparse
import os
import sys
from threading import Thread
import atac


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
    encrypted_config = False
    key_file_path = None
    config_file_path = "auth.json"
    #
    if arguments.encrypted_config is not None:
        encrypted_config = str2bool(getattr(arguments, "encrypted_config"))
        print("{} {}", encrypted_config, type(encrypted_config))
    #
    if arguments.config_file is not None:
        config_file_path = getattr(arguments, "config_file")
        print("{} {}", config_file_path, type(config_file_path))
    #
    if arguments.key_file is not None:
        key_file_path = getattr(arguments, "key_file")
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
    if arguments.generate_key_file is not None:
        generate_key_file_path = getattr(arguments, "generate_key_file")
        if generate_key_file_path:
            config.generate_key()
            config.save_key(generate_key_file_path)
    #
    if arguments.new_config_file is not None:
        new_config_file_path = getattr(arguments, "new_config_file")
        if new_config_file_path:
            config.new_config(new_config_file_path)
    #
    if arguments.decrypted_config_file is not None:
        decrypted_config_file_path = getattr(arguments, "decrypted_config_file")
        if decrypted_config_file_path:
            config.load_config()
            config.save_config(decrypted_config_file_path, False)


# sub-command functions
def chat(arguments):
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
    chat = atac.SendChat(encrypted_config, config_file_path, key_file_path)


# sub-command functions
def irc(arguments):
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
    chat = atac.SendIRC(encrypted_config, config_file_path, key_file_path)
    #
    if arguments.list_users is not None:
        list_users = getattr(arguments, "list_users")
    if arguments.message_users is not None:
        message_users = getattr(arguments, "message_users")
    if arguments.message_channels is not None:
        message_channels = getattr(arguments, "message_channels")
    #
    chat.list_channels()


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
    emailer = atac.SendEmail(encrypted_config, config_file_path, key_file_path)
    subject = None
    email_files_path = os.path.dirname(os.path.abspath(__file__)) + "/data/contacts/emails/"
    #
    if arguments.subject is not None:
        subject = getattr(arguments, "subject")
    if arguments.message_file is not None:
        message_file_path = getattr(arguments, "message_file")
    if arguments.emails_file is not None:
        email_files_path = getattr(arguments, "emails_file")
    if arguments.target is not None:
        target = getattr(arguments, "target")
    #
    _, content = emailer.get_config()
    #
    if not subject:
        sys.exit(1)
    #
    if not message_file_path:
        sys.exit(1)
    #
    emailer.send_batch(
        email_files_path,
        message_file_path,
        subject,
        False,
        False,
        correct_spelling=False,
        src=False,
        dest=False,
    )


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
    chatter = atac.SendChat(encrypted_config, config_file_path, key_file_path)
    #
    target = "whatsapp"
    phone_files_path = os.path.dirname(os.path.abspath(__file__)) + "/data/contacts/phones/"
    #
    if arguments.message_file is not None:
        message_file_path = getattr(arguments, "message_file")
    if arguments.phones_file is not None:
        phone_files_path = getattr(arguments, "phones_file")
    if arguments.target is not None:
        target = getattr(arguments, "target")
    #
    if "whatsapp" in target and os.environ.get("DISPLAY"):
        chatter.send_pywhatkit(phone_files_path, message_file_path)


# sub-command functions
def art(arguments):
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
    artist = atac.Art(encrypted_config, config_file_path, key_file_path)
    font_size = 22
    message_text = None
    images_path = None
    gif_path = None
    #
    if arguments.font_size is not None:
        font_size = int(getattr(arguments, "font_size"))
    if arguments.message_text is not None:
        message_text = getattr(arguments, "message_text")
    if arguments.images_path is not None:
        images_path = getattr(arguments, "images_path")
    if arguments.gif_path is not None:
        gif_path = getattr(arguments, "gif_path")
    #
    if images_path:
        artist.generate_gifs_from_all_dirs(images_path, "*.png")
    #
    if gif_path and message_text:
        artist.add_centered_text_to_gif(gif_path, message_text, font_size)


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
    socialite = atac.SendSocial(encrypted_config, config_file_path, key_file_path)
    #
    target = "twitter"
    #
    if arguments.message_file is not None:
        message_file_path = getattr(arguments, "message_file")
    if arguments.target is not None:
        target = getattr(arguments, "target")
    #
    if "facebook" in target:
        socialite.send_facebook(message_file_path)
    if "twitter" in target:
        socialite.send_twitter(message_file_path)


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
    if arguments.url is not None:
        url = getattr(arguments, "url")
        scraper = atac.Scrape(encrypted_config, config_file_path, key_file_path)
        scraper.process_page("url", url)
    elif arguments.target is not None:
        target = getattr(arguments, "target")
        scraper = atac.Scrape(encrypted_config, config_file_path, key_file_path)
        scraper.process_page(target, scraper.scrape["targets"][target])
    else:
        # create threads
        scrapers = {}
        config = atac.Config(encrypted_config, config_file_path, key_file_path)
        for data_key, starting_url in config.data["scrape"]["targets"].items():
            print("{0} - {1}".format(data_key, starting_url))
            scrapers[data_key] = atac.Scrape(encrypted_config, config_file_path, key_file_path)
            catcher_thread = Thread(target=scrapers[data_key].process_page, args=(data_key, starting_url))
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
    corpus_file_path = os.path.dirname(os.path.abspath(__file__)) + "/data/pg1009.txt"
    #
    input_file_path = None
    output_file_path = None
    translate_from_languagecode = None
    translate_to_languagecode = None
    paraphrase_language = None
    spellcheck_language = None
    images_dir = None
    #
    if arguments.images_dir is not None:
        images_dir = getattr(arguments, "images_dir")
    if arguments.input_file_path is not None:
        input_file_path = getattr(arguments, "input_file_path")
    if arguments.output_file_path is not None:
        output_file_path = getattr(arguments, "output_file_path")
    if arguments.translate_from_languagecode is not None:
        translate_from_languagecode = getattr(arguments, "translate_from_languagecode")
    if arguments.translate_to_languagecode is not None:
        translate_to_languagecode = getattr(arguments, "translate_to_languagecode")
    if arguments.paraphrase_language is not None:
        paraphrase_language = getattr(arguments, "paraphrase_language")
    if arguments.spellcheck_language is not None:
        spellcheck_language = getattr(arguments, "spellcheck_language")
    #
    paraphrase = paraphrase_language if paraphrase_language else False
    from_lang = translate_from_languagecode if translate_from_languagecode else "en"
    to_lang = translate_to_languagecode if translate_to_languagecode else "en"
    translate = True if from_lang != to_lang else False
    spellcheck = spellcheck_language if spellcheck_language else False
    #
    encrypted_config, config_file_path, key_file_path = get_config_arguments(arguments)
    composer = atac.Compose(encrypted_config, config_file_path, key_file_path)
    #
    corpus = None
    if input_file_path is not None:
        corpus = get_file_content(input_file_path)
    if corpus is not None:
        transform = composer.transform(corpus, paraphrase, translate, spellcheck, src=from_lang, dest=to_lang)
        try:
            if not os.path.isdir(os.path.dirname(output_file_path)):
                os.makedirs(os.path.dirname(output_file_path))
            with open(output_file_path, mode="w") as output_file:
                output_file.write("\n".join(transform))
        except Exception as err:
            print(err)


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
    cleaner = atac.Clean(encrypted_config, config_file_path, key_file_path)
    #
    email_files_path = os.path.dirname(os.path.abspath(__file__)) + "/data/contacts/emails/"
    phone_files_path = os.path.dirname(os.path.abspath(__file__)) + "/data/contacts/phones/"
    #
    if arguments.target is not None:
        target = getattr(arguments, "target")
    #
    if "email" in target:
        cleaner.clean_emails(email_files_path)
    if "phone" in target:
        cleaner.clean_phones(phone_files_path)
    else:
        cleaner.clean_emails(email_files_path)
        cleaner.clean_phones(phone_files_path)


if __name__ == "__main__":
    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the "config" command
    parser_config = subparsers.add_parser("config")
    parser_config.add_argument("-c", dest="config_file", type=str, help="use config file path")
    parser_config.add_argument("-e", dest="encrypted_config", action="store_true")
    parser_config.add_argument("-k", dest="key_file", type=str, help="use key file path")
    parser_config.add_argument("-g", dest="generate_key_file", type=str, help="generate new key file path")
    parser_config.add_argument(
        "-d",
        dest="decrypted_config_file",
        type=str,
        help="output decrypted config file path",
    )
    parser_config.add_argument("-n", dest="new_config_file", type=str, help="generate new config file path")
    parser_config.set_defaults(func=configuration)

    # create the parser for the "email command
    parser_email = subparsers.add_parser("email")
    parser_email.add_argument("-c", dest="config_file", type=str, help="use config file path")
    parser_email.add_argument("-e", dest="encrypted_config", action="store_true")
    parser_email.add_argument("-k", dest="key_file", type=str, help="use key file path")
    parser_email.add_argument("-m", dest="message_file", type=str, help="path to message file")
    parser_email.add_argument("-p", dest="emails_file", type=str, help="path to csv dir or file")
    parser_email.add_argument("-s", dest="subject", type=str, help="email subject")
    parser_email.add_argument("-t", dest="target", choices=["smtp", "aws"], default="smtp")
    parser_email.add_argument("-v", dest="verbose")
    parser_email.set_defaults(func=email)

    # create the parser for the irc command
    parser_irc = subparsers.add_parser("irc")
    parser_irc.add_argument("-c", dest="config_file", type=str, help="use config file path")
    parser_irc.add_argument("-e", dest="encrypted_config", action="store_true")
    parser_irc.add_argument("-k", dest="key_file", type=str, help="use key file path")
    parser_irc.add_argument("-u", dest="message_users", action="store_true")
    parser_irc.add_argument("-z", dest="message_channels", action="store_true")
    parser_irc.add_argument("-l", dest="list_users", action="store_true")
    parser_irc.add_argument("-v", dest="verbose")
    parser_irc.set_defaults(func=irc)

    # create the parser for the chat command
    parser_email = subparsers.add_parser("chat")
    parser_email.add_argument("-c", dest="config_file", type=str, help="use config file path")
    parser_email.add_argument("-e", dest="encrypted_config", action="store_true")
    parser_email.add_argument("-k", dest="key_file", type=str, help="use key file path")
    parser_email.add_argument("-u", dest="message_users", action="store_true")
    parser_email.add_argument("-l", dest="list_users", action="store_true")
    parser_email.add_argument("-v", dest="verbose")
    parser_email.set_defaults(func=chat)

    # create the parser for the "phone" command
    parser_phone = subparsers.add_parser("phone")
    parser_phone.add_argument("-c", dest="config_file", type=str, help="use config file path")
    parser_phone.add_argument("-e", dest="encrypted_config", action="store_true")
    parser_phone.add_argument("-k", dest="key_file", type=str, help="use key file path")
    parser_phone.add_argument("-m", dest="message_file", type=str, help="path to message file")
    parser_phone.add_argument("-p", dest="phones_file", type=str, help="path to csv dir or file")
    parser_phone.add_argument("-t", dest="target", choices=["whatsapp", "sms"])
    parser_phone.add_argument("-w", dest="whatsapp", choices=["pywhatkit", "twilio", "yowsup"])
    parser_phone.add_argument("-s", dest="sms", choices=["aws", "twilio"], default="aws")
    parser_phone.add_argument("-v", dest="verbose")
    parser_phone.set_defaults(func=phone)

    # create the parser for the "social" command
    parser_social = subparsers.add_parser("social")
    parser_social.add_argument("-c", dest="config_file", type=str, help="use config file path")
    parser_social.add_argument("-e", dest="encrypted_config", action="store_true")
    parser_social.add_argument("-k", dest="key_file", type=str, help="use key file path")
    parser_social.add_argument("-m", dest="message", type=str, help="path to message file")
    parser_social.add_argument("-t", dest="target", choices=["facebook", "twitter"], default="twitter")
    parser_social.add_argument("-v", dest="verbose")
    parser_social.set_defaults(func=social)

    # create the parser for the "art" command
    parser_art = subparsers.add_parser("art")
    parser_art.add_argument("-c", dest="config_file", type=str, help="use config file path")
    parser_art.add_argument("-e", dest="encrypted_config", action="store_true")
    parser_art.add_argument("-k", dest="key_file", type=str, help="use key file path")
    parser_art.add_argument("-f", dest="font_size", type=int, help="font_size")
    parser_art.add_argument("-m", dest="message_text", type=str, help="text message")
    parser_art.add_argument("-g", dest="gif_path", type=str, help="path to gif file")
    parser_art.add_argument("-p", dest="images_path", type=str, help="path to images directory")
    parser_art.add_argument("-t", dest="art_type", choices=["sudoku", "invaders"])
    parser_art.add_argument("-v", dest="verbose")
    parser_art.set_defaults(func=art)

    # create the parser for the "scrape" command
    parser_scrape = subparsers.add_parser("scrape")
    parser_scrape.add_argument("-c", dest="config_file", type=str, help="use config file path")
    parser_scrape.add_argument("-e", dest="encrypted_config", action="store_true")
    parser_scrape.add_argument("-k", dest="key_file", type=str, help="use key file path")
    parser_scrape.add_argument(
        "-t",
        dest="target",
        choices=[
            "museums",
            "embassies",
            "activism",
            "education",
            "religion",
            "rescue",
            "addiction",
            "music",
            "journalists",
            "defense",
            "ukraine",
            "islam",
            "all",
        ],
        default="all",
    )
    parser_scrape.add_argument("-u", dest="url", help="The URL to scrape.")
    parser_scrape.add_argument("-v", dest="verbose")
    parser_scrape.set_defaults(func=scrape)

    # create the parser for the "compose" command
    parser_compose = subparsers.add_parser("compose")
    parser_compose.add_argument("-c", dest="config_file", type=str, help="use config file path")
    parser_compose.add_argument("-e", dest="encrypted_config", action="store_true")
    parser_compose.add_argument("-g", dest="images_dir", type=str, help="images directory to create gif from")
    parser_compose.add_argument("-k", dest="key_file", type=str, help="use key file path")
    parser_compose.add_argument("-i", dest="input_file_path", type=str, required=False, help="input_file_path")
    parser_compose.add_argument("-o", dest="output_file_path", type=str, required=False, help="output_file_path")
    parser_compose.add_argument("-p", dest="paraphrase_language", type=str, help="paraphrase source language")
    parser_compose.add_argument("-s", dest="spellcheck_language", type=str, help="spellcheck source language")
    parser_compose.add_argument(
        "-f",
        dest="translate_from_languagecode",
        type=str,
        help="translate from source language code",
    )
    parser_compose.add_argument(
        "-t",
        dest="translate_to_languagecode",
        type=str,
        help="translate to target language code",
    )
    parser_compose.add_argument("-v", dest="verbose")
    parser_compose.set_defaults(func=compose)

    # create the parser for the "compose" command
    parser_clean = subparsers.add_parser("clean")
    parser_clean.add_argument("-c", dest="config_file", type=str, help="config file")
    parser_clean.add_argument("-e", dest="encrypted_config", action="store_true")
    parser_clean.add_argument("-k", dest="key_file", type=str, help="key file path")
    parser_clean.add_argument("-t", dest="target", choices=["email", "phone", "all"])
    parser_clean.add_argument("-v", dest="verbose")
    parser_clean.set_defaults(func=clean)

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    # validate conditions
    cond_translation_from = "translate_from_languagecode" in vars(args) and "translate_to_languagecode" not in vars(
        args
    )
    cond_translation_to = "translate_to_languagecode" in vars(args) and "translate_from_languagecode" not in vars(args)
    if cond_translation_from or cond_translation_to:
        parser.error("The -LoadFiles argument requires the -SourceFolder or -SourceFile")
    #
    args.func(args)
