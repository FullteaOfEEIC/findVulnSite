import sys
sys.path.append("/Sublist3r")

import sublist3r
import socket
import os
from scantool import scan, dirb

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


for domain in domains:
    scan(domain)
