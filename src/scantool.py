import nmap
import requests
from copy import copy
import re
from chardet.universaldetector import UniversalDetector
from tqdm.auto import tqdm
from parallel_requests.session import extended_session

def check_encoding(file_path):
    detector = UniversalDetector()
    with open(file_path, mode='rb') as f:
        for binary in f:
            detector.feed(binary)
            if detector.done:
                break
    detector.close()
    return detector.result['encoding']

def dirb(domain, wordlist="/usr/share/dirb/wordlists/big.txt"):
    encoding = check_encoding(wordlist)
    with open(wordlist, "r", encoding=encoding) as fp:
        words = [word.strip() for word in fp]
    if re.match("https?://",domain):
        uris = [domain]
    else:
        urls = ["http://"+domain, "https://"+domain]
    retval = copy(urls)
    while len(urls)>0:
        candidate = urls.pop(0)
        method_args = [{"url":candidate+"/"+word, "method":"get"} for word in words]
        with extended_session() as session:
            responses = session.parallel_request(
                method_args=method_args,
                max_workers=5
            )
        for response, method in zip(responses, method_args):
            if response.status_code!=404:
                print(method["url"], response.status_code)
                retval.append(method["url"])
                urls.append(method["url"])

    return retval


def scan(addr, output="result"):
    pass
