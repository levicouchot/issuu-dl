#!/usr/bin/env python3
#
# issuu-dl.py v0.1
#
# download pdf from issuu.com
#
# tested (and working) on 02 Aug 2019
#

import requests
import sys
import json
import img2pdf
import os
from termcolor import colored
from tqdm import tqdm

def usage():
    print("USAGE: %s [full issuu url of target document]" % sys.argv[0])
    exit()

try:
    url = sys.argv[1]
except:
    usage()

doc = url.split('/')
doc = doc[3] + '/' + doc[5]
print(doc)
print("[*] doc is '%s'" % colored(doc, 'yellow'))
outfile = doc.replace('/', '_') + ".pdf"

print("[*] opening page...")
s = requests.Session()
r = s.get(url)
assert r.status_code == 200
print(colored("[+] url confirmed", "green"))
assert 'issuu-reader3-embed-files' in r.content.decode()
print(colored("[+] reader3 support confirmed", "green"))

print("[*] downloading reader3_4.json...")

r = s.get("https://reader3.isu.pub/%s/reader3_4.json" % doc)
j = json.loads(r.content.decode())

pubId = j["document"]["publicationId"]
revId = j["document"]["revisionId"]
pages = j["document"]["pages"]

print(colored("[+] fetched document data: ", "green") + colored("publicationId is %s, revisionId is %s" % (pubId, revId), "yellow"))
print(colored("[+] found %d pages" % len(pages), "green"))

print("[*] downloading pages...")

filenames = []
for page in tqdm(pages):
    i = page["imageUri"].split('/')
    f = i[1]+"-"+i[3]
    r = s.get("https://"+page["imageUri"])
    open(f, "wb").write(r.content)
    filenames.append(f)

print(colored("[+] downloaded %s jpg files" % len(pages), "green"))

print("[*] converting to single pdf...")

with open(outfile, "wb") as out:
    out.write(img2pdf.convert(filenames))

print(colored("[+] output pdf '%s' is ready" % colored(outfile, "yellow"), "green"))

print("[*] cleaning up jpg files...")
for f in filenames:
    os.remove(f)

print(colored("[+] done.", "green"))

