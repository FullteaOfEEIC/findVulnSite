import nmap
import requests
from copy import copy, deepcopy
import re
from chardet.universaldetector import UniversalDetector
from tqdm.auto import tqdm
from parallel_requests.session import extended_session
from multiprocessing import cpu_count
import time

def check_encoding(file_path):
    detector = UniversalDetector()
    with open(file_path, mode='rb') as f:
        for binary in f:
            detector.feed(binary)
            if detector.done:
                break
    detector.close()
    return detector.result['encoding']

def dirb(domain, wordlist="/usr/share/dirb/wordlists/common.txt"):
    encoding = check_encoding(wordlist)
    with open(wordlist, "r", encoding=encoding) as fp:
        words = [word.strip() for word in fp]
    if re.match("https?://",domain):
        urls = [domain]
    else:
        urls = ["http://"+domain, "https://"+domain]
    retval = copy(urls)
    batch_size = 8
    while len(urls)>0:
        candidate = urls.pop(0)
        responses = []
        method_args = [{"url":candidate+"/"+word, "method":"get"} for word in words]
        for batch in tqdm(range(0, len(method_args), batch_size)):
            with extended_session() as session:
                _responses = session.parallel_request(
                    method_args=method_args[batch:batch+batch_size],
                    max_workers=cpu_count()*5
                )
            responses += _responses
        for response, method in zip(responses, method_args):
            if response.status_code!=404:
                print(method["url"], response.status_code)
                retval.append(method["url"])
                urls.append(method["url"])
        time.sleep(3)

    return retval


def scan(addr, output="result"):
    pass
