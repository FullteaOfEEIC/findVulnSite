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
    domains.append(_domain)
    if _domain.split(".")[0]=='*':
        domains += sublist3r.main(_domain,threads,None,None,None,None,False,None) #そこそこの確率で活きていないサブドメインが含まれている。


addrs = []
for _domain in domains:
    try:
        addrs += socket.gethostbyname_ex(_domain)[2]
    except:
        pass


for domain in domains:
    scan(domain)
#os.mkdir("result")