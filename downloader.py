#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import os
import sys
import signal


def ctrl_c_handler(sig, frame):
    sys.exit("\nYou pressed Ctrl+C!")

signal.signal(signal.SIGINT, ctrl_c_handler)

args = {
    "b" : None,
    "a" : False,
    "f" : False,
    "l" : False,
}

def printHelp():
    sys.exit("""
    Usage:
        python3 downloader.py [options]

    Options:
        -b <int>    download fivem artifact by build version
        -a          download all fivem artifacts
        -h          show this message
        -f          overide artifact, even if its present
        -l          download the latest version
    """)
if len(sys.argv) > 1:
    for key, value in enumerate(sys.argv):
        value = value.replace("-", "")
        if value in args.keys():
            if value == "b":
                if len(sys.argv) > key + 1:
                    if sys.argv[key+1] and not str(sys.argv[key+1]).startswith("-"):
                        args[value] = str(sys.argv[key+1])
                    else:
                        sys.exit("invalid argument after argument [" + str(key) + ",-" + str(value) +"]")
                else:
                    sys.exit("missing argument after argument [" + str(key) + ",-" + str(value) +"]")
            else:
                args[value] = True
else:
    printHelp()

path = "artifacts"
if not os.path.exists(path):
   os.makedirs(path)
   print("Artifact Directory created")

linux_url = "https://runtime.fivem.net/artifacts/fivem/build_proot_linux/master/"

html = requests.get(linux_url, allow_redirects=True)
soup = BeautifulSoup(html.text, 'html.parser')

panel_blocks = soup.findAll('a', {'class':'panel-block'}, href=True)
for block in panel_blocks:
    href = block["href"].replace("./", "")
    if "tar.xz" in href:
        artifact_name = href.split("-")[0]
        if args["b"] == artifact_name or args["a"] or args["l"]:
            artifact_path = path + "/" + artifact_name + ".tar.xz"
            if not os.path.exists(artifact_path) or args["f"]:
                url = linux_url + href
                open(artifact_path, "wb").write(requests.get(url, allow_redirects=True).content)
                print("FiveM Artifact Successfully [" + artifact_name +"] downloaded!")
            else:
                print("FiveM Artifact [" + artifact_name +"] already downloaded!")
            if args["l"]:
                sys.exit()

