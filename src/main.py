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
    addrs += socket.gethostbyname_ex(_domain)[2]


for domain in domains:
    urls = dirb(domain)
    print(urls)
#os.mkdir("result")