import sys
sys.path.append("/Sublist3r")

import sublist3r
import socket
import os
from scantool import scan, dirb

domain = sys.argv[1]
threads = 30

domains = [domain]

domains += sublist3r.main(domain,threads,None,None,None,None,False,None) #そこそこの確率で活きていないサブドメインが含まれている。


addrs = []
for _domain in domains:
    try:
        addrs += socket.gethostbyname_ex(_domain)[2]
    except:
        pass


for domain in domains:
    scan(domain)
#os.mkdir("result")