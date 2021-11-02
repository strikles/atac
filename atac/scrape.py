import regex as re
import os
import csv
import json
import requests
from requests import HTTPError
from threading import currentThread
from fake_useragent import UserAgent
from validator_collection import checkers
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
from functools import reduce
from email_validator import validate_email, EmailNotValidError
from .config import Config


class UnderTheMangoTree:


    def __init__(self):
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
        self.config = Config()
        self.scrape = self.config.data['scrape']


    def invalid_url(self, url):
        # reject invalid domains
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
            if url.lower().endswith(k):
                print(">>> invalid file..\n")
                return True
        return False


    @staticmethod
    def set_useragent():
        ua = UserAgent()
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Language": "en-US,en;q=0.5", "Referer": "https://www.google.com/", "DNT": "1",
                   "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1", 'User-Agent': ua.random}
        return headers


    @staticmethod
    def make_dirs():
        # make dirs 
        if not os.path.isdir(os.getcwd() + "/contacts"):
            os.makedirs(os.getcwd() + "/contacts")
        if not os.path.isdir(os.getcwd() + "/contacts/emails"):
            os.makedirs(os.getcwd() + "/contacts/emails")
        if not os.path.isdir(os.getcwd() + "/contacts/phones"):
            os.makedirs(os.getcwd() + "/contacts/phones")


    @staticmethod
    def truncate_files(data_key):
        # save to file
        csv_path = os.getcwd() + "/contacts/emails/" + data_key + "_emails.csv"
        with open(csv_path, mode='a') as emails_file:
            emails_file.truncate(0)
            emails_writer = csv.writer(emails_file,
                                       delimiter=',',
                                       quotechar='"',
                                       quoting=csv.QUOTE_MINIMAL)

            emails_writer.writerow(['', 'email'])

        csv_path = os.getcwd() + "/contacts/phones/" + data_key + "_phones.csv"
        with open(csv_path, mode='a') as phones_file:
            phones_file.truncate(0)
            phones_writer = csv.writer(phones_file,
                                       delimiter=',',
                                       quotechar='"',
                                       quoting=csv.QUOTE_MINIMAL)

            phones_writer.writerow(['', 'phone'])


    @staticmethod
    def extract_emails(content):
        #
        rx_emails = re.compile(r"[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+"
                               r"(?!jpg|jpeg|png|svg|gif|webp|yji|pdf|htm|title|content|formats)[a-zA-Z]{2,7}")
        return set(filter(lambda x: (checkers.is_email(x)), rx_emails.findall(content)))


    @staticmethod
    def extract_phones(content):
        #
        rx_phones = re.compile(r'\+(?:[0-9] ?){6,14}[0-9]')
        return set(rx_phones.findall(content))


    def save_contacts(self, new_contacts, data_key, type):
        # save to file
        if type == "email":
            csv_path = os.getcwd() + "/contacts/emails/" + data_key + "_emails.csv"
        elif type == "phone":
            csv_path = os.getcwd() + "/contacts/phones/" + data_key + "_phones.csv"
        else:
            raise Exception('unknown type: {}'.format(type))
            
        with open(csv_path, mode='a') as f:
            writer = csv.writer(f,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
                                
            if type == "email":
                unique_contacts = list(filter(lambda e: e not in self.emails, new_contacts))
            elif type == "phone":
                unique_contacts = list(filter(lambda e: e not in self.phones, new_contacts))
                
            for c in unique_contacts:
                if type == "email":
                    try:
                        if validate_email(c):
                            print("\x1b[6;37;41m new {0}:{1} \x1b[0m".format(type, c))
                            self.num_emails +=1
                            writer.writerow([self.num_emails, c])
                    except EmailNotValidError as e:
                        # email is not valid, exception message is human-readable
                        print(str(e))
                elif type == "phone":
                    print("\x1b[6;37;41m new {0}:{1} \x1b[0m".format(type, c))
                    self.num_phones +=1
                    writer.writerow([self.num_phones, c])


    def process_page(self, data_key, starting_url):

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
            print("\x1b[6;37;42m {0} urls:{1} {2} | emails:{3} phones:{4} - {5} \x1b[0m".format(
                currentThread().getName(),
                len(self.primary_unprocessed_urls),
                len(self.secondary_unprocessed_urls),
                len(self.emails),
                len(self.phones),
                url)
            )
            #
            self.processed_urls.add(url)

            # skip if invalid 
            if self.invalid_url(url):
                continue
            # get page with timeout of 10s
            try:
                proxies = dict()
                if self.scrape["active_proxies"]:
                    proxies = self.scrape["proxies"]

                response = requests.get(url, headers=self.set_useragent(), proxies=proxies, timeout=10, stream=False)
                response.encoding = "utf-8"
                # If the response was successful, no Exception will be raised
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                continue
            except Exception as err:
                print(f'Other error occurred: {err}')
                continue
            else:
                pass

            # extract email addresses into the resulting set
            new_emails = self.extract_emails(response.text)
            if new_emails:
                self.save_contacts(new_emails, data_key, "email")
                self.emails.update(new_emails)

            # extract phone numbers into resulting set
            new_phones = self.extract_phones(response.text)
            if new_phones:
                self.save_contacts(new_phones, data_key, "phone")
                self.phones.update(new_phones)

            # create a beautiful soup for the html document
            try:
                soup = BeautifulSoup(response.text, 'lxml')
            except Exception as bs_err:
                print(f'html bs parsing error occurred: {bs_err}')
                continue
            else:
                pass
                
            # extract base url to resolve relative links
            parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/') + 1] if '/' in parts.path else url
            
            # find all the anchors
            anchors = soup.find_all("a")
            num_anchors = len(anchors)
            print("> {0} new anchors {1}".format(currentThread().getName(), num_anchors))
            
            # process all the anchors
            count = 0
            for anchor in anchors:
                # extract link url from the anchor
                link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                # resolve relative links (starting with /)
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                # add the new url to queue if not in unprocessed list nor in processed list
                if checkers.is_url(link) and link not in self.processed_urls:
                    count += 1
                    if count > 20 and url not in self.secondary_unprocessed_urls:
                        self.secondary_unprocessed_urls.append(url)
                        if url in self.processed_urls:
                            self.processed_urls.remove(url)
                        break
                    elif link not in self.primary_unprocessed_urls:
                        self.primary_unprocessed_urls.append(link)

            if not self.primary_unprocessed_urls:
                print(">>> primary queue empty...\n")
                self.primary_unprocessed_urls.extend(self.secondary_unprocessed_urls)
                self.secondary_unprocessed_urls.clear()

        return status
        