import nmap
import re
import subprocess
import uuid
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import docx
from docx.shared import Inches

def dirb(domain, wordlist="/usr/share/dirb/wordlists/common.txt"):
    if re.match("^https?:\/\/",domain):
        domains = [domain]
    else:
        domains = ["https://"+domain, "http://"+domain]
    retval = []
    dirb_retval = re.compile("^\+ (https?:\/\/.+) \(CODE:(\d+)\|SIZE:\d+\)$")
    for domain in domains:
        random_name = str(uuid.uuid4())
        subprocess.run(["dirb", domain, "-o", random_name,"-w","-r"])
        with open(random_name,"r") as fp:
            for line in fp:
                match = dirb_retval.match(line.strip())
                if match and int(match.group(2))!=301:
                    retval.append(match.group(1))
        os.remove(random_name)


    return set(retval)

def nikto(url):
    random_name = str(uuid.uuid4())+".txt"
    subprocess.run(["nikto", "-h", url, "-o", random_name])
    return "\n".join(open(random_name,"r").readlines())


def scan(addr, output="result"):
    urls = dirb(addr)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    imagenames = []
    for url in urls:
        driver.get(url)
        driver.set_window_size(1920,1080)
        filename = re.sub("^https?:\/\/","",url)
        filename = filename.replace("/","-")+".png"
        driver.save_screenshot(filename)
        imagenames.append(filename)
    driver.close()
    nikto_results = [nikto(url) for url in urls]
    doc = docx.Document()
    for url, imagename, nikto_result in zip(urls, imagenames, nikto_results):
        doc.add_heading(url,0)
        doc.add_picture(imagename, width=Inches(8.27*0.7))
        doc.add_heading("nikto",1)
        doc.add_paragraph(nikto_result)
        doc.add_page_break()
    doc.save("/mnt/{0}.docx".format(addr))

