import json
import string
import random
import requests
from .message import Listen


def username_gen(length=24, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))


def password_gen(length=8, chars=string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(length))


class Email(Listen):
    token = ""
    domain = ""
    address = ""
    session = requests.Session()

    def __init__(self, proxies):
        if not self.domains(proxies):
            print("Failed to get domains")

    def domains(self, proxies):
        url = "https://api.mail.tm/domains"
        response = self.session.get(url, proxies=proxies)
        response.raise_for_status()

        try:
            data = response.json()
            for domain in data['hydra:member']:
                if domain['isActive']:
                    self.domain = domain['domain']
                    return True

            raise Exception("No Domain")
        except:
            return False

    def register(self, proxies):
        self.domain = self.domain
        username = username_gen()
        password = password_gen()

        url = "https://api.mail.tm/accounts"
        payload = {
            "address": f"{username}@{self.domain}",
            "password": password
        }
        headers = {'Content-Type': 'application/json'}
        response = self.session.post(url, headers=headers, json=payload, proxies=proxies)
        response.raise_for_status()

        data = response.json()
        try:
            self.address = data['address']
        except:
            self.address = f"{username}@{self.domain}"

        self.get_token(password, proxies)

        if not self.address:
            raise Exception("Failed to make an address")

    def get_token(self, password, proxies):
        url = "https://api.mail.tm/token"
        payload = {
            "address": self.address,
            "password": password
        }
        headers = {'Content-Type': 'application/json'}
        response = self.session.post(url, headers=headers, json=payload, proxies=proxies)
        response.raise_for_status()
        try:
            self.token = response.json()['token']
        except:
            raise Exception("Failed to get token")


if __name__ == "__main__":
    Dict = {
        "https": "123.635.345"
    }


    def listener(message):
        print("\nSubject: " + message['subject'])
        print("Content: " + message['text'] if message['text'] else message['html'])


    # Get Domains
    test = Email(Dict)
    print("\nDomain: " + test.domain)

    # Make new email address
    test.register(Dict)
    print("\nEmail Adress: " + str(test.address))

    # Start listening
    test.start(listener, proxies)
    print("\nWaiting for new emails...")

    # Stop listening
    # test.stop()
