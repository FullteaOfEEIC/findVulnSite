import nmap
import requests
from copy import copy, deepcopy
import re
import subprocess
import uuid
from tqdm.auto import tqdm
from parallel_requests.session import extended_session
from multiprocessing import cpu_count
import os

def dirb(domain, wordlist="/usr/share/dirb/wordlists/big.txt"):
    if re.match("https?://",domain):
        domains = [domain]
    else:
        domains = ["http://"+domain,"https://"+domain]
    retval = []
    dirb_retval = re.compile("^\+ (https?:\/\/.+) \(CODE:\d+\|SIZE:\d+\)$")
    for domain in domains:
        random_name = str(uuid.uuid4())
        subprocess.run(["dirb", domain, "-o", random_name,"-w"])
        with open(random_name,"r") as fp:
            for line in fp:
                match = dirb_retval.match(line.strip())
                if match:
                    retval.append(match.group(1))
        os.remove(random_name)


    return retval


def scan(addr, output="result"):
    pass
