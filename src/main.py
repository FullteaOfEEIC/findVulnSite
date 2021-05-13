import sys
sys.path.append("/Sublist3r")

import sublist3r
import socket
import os
from scantool import scan, dirb
from multiprocessing import Pool
from tqdm.auto import tqdm

_domains = sys.argv[1:]
threads = 30

domains = []
for _domain in _domains:
    if _domain.split(".")[0]=='*':
        domains += sublist3r.main(_domain[2:],threads,None,None,None,None,False,None) #そこそこの確率で活きていないサブドメインが含まれている。
    else:
        domains.append(_domain)

def domain_exists(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except:
        return False

domains = [domain for domain in domains if domain_exists(domain)]


if __name__=="__main__":
    with Pool() as p:
        imap = p.imap(scan, domains)
        list(tqdm(imap, total = len(domains)))
