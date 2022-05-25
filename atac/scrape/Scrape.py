from ..config.Config import Config
from ..util.Util import str2bool

import csv
from bs4 import BeautifulSoup
from collections import deque
from fake_useragent import UserAgent
import regex as re
import os
import requests
from requests import HTTPError
import tldextract
from torrequest import TorRequest
from urllib.parse import urlsplit
import validators
import threading


class Scrape(Config):
    """A class used to represent a scraper object

    Attributes
    ----------
    key : str
        a encryption key
    data : dict
        configuration data
    encrypted_config : bool
        use an encrypted configuration file
    config_file_path : str
        path to the configuration file
    key_file_path : str
        path to encryption key file
    gpg : gnupg.GPG
        python-gnupg gnupg.GPG

    Methods
    -------
    generate_key()
        Generates a new encryption key from a password + salt
    """

    def __init__(
        self, encrypted_config=True, config_file_path="auth.json", key_file_path=None
    ):
        """Class init

        Parameters
        ----------
        encrypted_config : bool
            use an encrypted configuration file
        config_file_path : str
            path to the configuration file
        key_file_path : str
            path to encryption key file
        """
        super().__init__(encrypted_config, config_file_path, key_file_path)
        self.scrape = self.data["scrape"]
        # primary queue (urls to be crawled)
        self.primary_unprocessed_urls = deque()
        self.secondary_unprocessed_urls = deque()
        # visited set (already crawled urls for email)
        self.processed_urls = set()
        # a set of fetched emails
        self.emails = set()
        self.phones = set()
        self.num_phones = 0
        self.num_emails = 0

    def invalid_url(self, url):
        """Check url against blacklist

        Parameters
        ----------
        url : str
            The url to validate against

        """
        for i in self.scrape["invalid_domains"]:
            if i in url.lower():
                print(">>> invalid domain...\n")
                return True
        for j in self.scrape["invalid_paths"]:
            if j in url.lower():
                print(">>> invalid path...\n")
                return True
        # reject invalid file types
        for k in self.scrape["invalid_files"]:
            if k in url.lower():
                print(">>> invalid file..\n")
                return True
        #
        return False

    @staticmethod
    def set_useragent():
        """Set user agent to random and return headers dictionary"""
        ua = UserAgent()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": ua.random,
        }
        #
        return headers

    @staticmethod
    def make_dirs():
        """Make contacts directories if they don’t exist"""
        if not os.path.isdir(os.getcwd() + "/data/contacts"):
            os.makedirs(os.getcwd() + "/data/contacts")
        if not os.path.isdir(os.getcwd() + "/data/contacts/emails"):
            os.makedirs(os.getcwd() + "/data/contacts/emails")
        if not os.path.isdir(os.getcwd() + "/data/contacts/phones"):
            os.makedirs(os.getcwd() + "/data/contacts/phones")

    @staticmethod
    def truncate_files(data_key):
        """Save contacts to file

        Parameters
        ----------
        data_key : str
            the scraped prefix
        """
        csv_path = os.getcwd() + "/data/contacts/emails/" + data_key + "_emails.csv"
        try:
            with open(csv_path, mode="a", newline="") as emails_file:
                emails_file.truncate(0)
                emails_writer = csv.writer(
                    emails_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                emails_writer.writerow(["", "email"])
        except OSError as e:
            print("{} file error {}".format(csv_path, e.errno))
        finally:
            emails_file.close()
        #
        csv_path = os.getcwd() + "/data/contacts/phones/" + data_key + "_phones.csv"
        try:
            with open(csv_path, mode="a", newline="") as phones_file:
                phones_file.truncate(0)
                phones_writer = csv.writer(
                    phones_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                phones_writer.writerow(["", "phone"])
        except OSError as e:
            print("{} file error {}".format(csv_path, e.errno))
        finally:
            phones_file.close()

    @staticmethod
    def extract_emails(content):
        """Use regex to extract emails from content

        Parameters
        ----------
        content : str
            the content scraped
        """
        rx_emails = re.compile(
            r"[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+"
            r"(?!jpg|jpeg|png|svg|gif|webp|yji|pdf|htm|title|content|formats)[a-zA-Z]{2,7}"
        )
        #
        return set(filter(lambda x: (validators.email(x)), rx_emails.findall(content)))

    @staticmethod
    def extract_phones(content):
        """Use regex to extract phones from content

        Parameters
        ----------
        content : str
            the content scraped
        """
        rx_phones = re.compile(r"\+(?:[0-9] ?){6,14}[0-9]")
        #
        return set(rx_phones.findall(content))

    def save_email_contacts(self, new_contacts, data_key):
        """Save to file

        Parameters
        ----------
        content : str
            the content scraped
        """
        csv_path = os.getcwd() + "/data/contacts/emails/" + data_key + "_emails.csv"
        try:
            with open(csv_path, mode="a", newline="") as contact_file:
                writer = csv.writer(
                    contact_file,
                    delimiter=",",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                )
                unique_contacts = list(
                    filter(lambda email: email not in self.emails, new_contacts)
                )
                for contact in unique_contacts:
                    print("\x1b[6;37;41m new email:{0} \x1b[0m".format(contact))
                    self.num_emails += 1
                    writer.writerow([self.num_emails, contact.strip()])
        except OSError as e:
            print("{} file error {}".format(csv_path, e.errno))

    def save_phone_contacts(self, new_contacts, data_key):
        """Save contacts to file

        Parameters
        ----------
        new_contacts : list
            Phone contacts
        """
        csv_path = os.getcwd() + "/data/contacts/phones/" + data_key + "_phones.csv"
        try:
            with open(csv_path, mode="a", newline="") as contact_file:
                writer = csv.writer(
                    contact_file,
                    delimiter=",",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                )
                unique_contacts = list(
                    filter(lambda phone: phone not in self.phones, new_contacts)
                )
                for contact in unique_contacts:
                    print("\x1b[6;37;41m new phone:{0}\x1b[0m".format(contact))
                    self.num_phones += 1
                    writer.writerow([self.num_phones, contact.strip()])
        except OSError as e:
            print("{} file error {}".format(csv_path, e.errno))

    def process_page(self, data_key, starting_url):
        """Scrape page

        Parameters
        ----------
        data_key : str
            the scrape data key
        starting_url : str
            The scrape starting url
        """
        from http import cookiejar

        status = 0
        # primary queue (urls to be crawled)
        self.primary_unprocessed_urls.append(starting_url)
        # secondary queue
        self.secondary_unprocessed_urls.clear()
        # visited set (already crawled urls for email)
        self.processed_urls.clear()
        # a set of fetched emails
        self.emails.clear()
        self.phones.clear()
        # make dirs
        self.make_dirs()
        self.truncate_files(data_key)
        # process urls 1 by 1 from queue until empty
        while self.primary_unprocessed_urls:
            # move next url from queue to set of processed urls
            url = self.primary_unprocessed_urls.popleft()
            print(
                "\x1b[6;37;42m {0} urls:{1} {2} | emails:{3} phones:{4} - {5} \x1b[0m".format(
                    threading.get_native_id(),
                    len(self.primary_unprocessed_urls),
                    len(self.secondary_unprocessed_urls),
                    len(self.emails),
                    len(self.phones),
                    url,
                )
            )
            #
            self.processed_urls.add(url)
            # skip if invalid
            if self.invalid_url(url):
                continue
            # get page with timeout of 10s
            response = None
            try:
                if "use_tor" in self.scrape.keys() and str2bool(self.scrape["use_tor"]):
                    # Choose a proxy port, a control port, and a password.
                    # Defaults are 9050, 9051, and None respectively.
                    # If there is already a Tor process listening the specified
                    # ports, TorRequest will use that one.
                    # Otherwise, it will create a new Tor process,
                    # and terminate it at the end.
                    tor_password = None
                    tor_proxy_port = 9050
                    tor_ctrl_port = 9051
                    with TorRequest(
                        proxy_port=tor_proxy_port,
                        ctrl_port=tor_ctrl_port,
                        password=tor_password,
                    ) as tr:
                        # Change your Tor circuit,
                        # and likely your observed IP address.
                        tr.reset_identity()
                        # TorRequest object also exposes the underlying Stem controller
                        # and Requests session objects for more flexibility.
                        print(type(tr.ctrl))  # a stem.control.Controller object
                        tr.ctrl.signal(
                            "CLEARDNSCACHE"
                        )  # see Stem docs for the full API
                        print(type(tr.session))  # a requests.Session object
                        c = cookiejar.CookieJar()
                        tr.session.cookies.update(
                            c
                        )  # see Requests docs for the full API
                        # Specify HTTP verb and url.
                        response = tr.get(url)
                        print(response.text)
                        # Send data. Use basic authentication.
                        # resp = tr.post('https://api.example.com',
                        # data={'foo': 'bar'}, auth=('user', 'pass'))'
                        # print(resp.json)
                else:
                    proxies_dict = {}
                    if "use_proxies" in self.scrape.keys() and str2bool(
                        self.scrape["use_proxies"]
                    ):
                        proxies_dict = self.scrape["proxies"]
                    #
                    response = requests.get(
                        url,
                        headers=self.set_useragent(),
                        proxies=proxies_dict,
                        timeout=10,
                        stream=False,
                    )
                    response.encoding = "utf-8"
                    # If the response was successful, no Exception will be raised
                    response.raise_for_status()
            #
            except HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                continue
            except Exception as err:
                print(f"Other error occurred: {err}")
                continue
            else:
                pass
            # extract email addresses into the resulting set
            new_emails = self.extract_emails(response.text)
            if new_emails:
                self.save_email_contacts(new_emails, data_key)
                self.emails.update(new_emails)
            # extract phone numbers into resulting set
            new_phones = self.extract_phones(response.text)
            if new_phones:
                self.save_phone_contacts(new_phones, data_key)
                self.phones.update(new_phones)
            # create a beautiful soup for the html document to get anchors
            try:
                soup = BeautifulSoup(response.text, "lxml")
            except Exception as bs_err:
                print(f"html bs parsing error occurred: {bs_err}")
                continue
            else:
                pass
            # extract base url to resolve relative links
            parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            base_ext = tldextract.extract(url)
            path = url[: url.rfind("/") + 1] if "/" in parts.path else url
            # find all the anchors
            anchors = soup.find_all("a")
            num_anchors = len(anchors)
            print(
                "> {0} new anchors {1}".format(threading.get_native_id(), num_anchors)
            )
            # process all the anchors
            count = 0
            for anchor in anchors:
                # extract link url from the anchor
                link = anchor.attrs["href"] if "href" in anchor.attrs else ""
                # resolve relative links (starting with /)
                if link.startswith("/"):
                    link = base_url + link
                elif not link.startswith("http"):
                    link = path + link
                # don't scrape if not in same domain
                link_ext = tldextract.extract(link)
                print("{0}.domain - {1}.domain".format(base_ext, link_ext))
                if base_ext.domain not in link:
                    print(
                        "Invalid link - link domain is outside domain of url being scraped..."
                    )
                    continue
                # add the new url to queue if not in unprocessed list nor in processed list
                if validators.url(link) and link not in self.processed_urls:
                    count += 1
                    if count > 20 and url not in self.secondary_unprocessed_urls:
                        self.secondary_unprocessed_urls.append(url)
                        if url in self.processed_urls:
                            self.processed_urls.remove(url)
                            break
                    elif link not in self.primary_unprocessed_urls:
                        self.primary_unprocessed_urls.append(link)
            #
            if not self.primary_unprocessed_urls:
                print(">>> primary queue empty...\n")
                self.primary_unprocessed_urls.extend(self.secondary_unprocessed_urls)
                self.secondary_unprocessed_urls.clear()
        #
        return status
