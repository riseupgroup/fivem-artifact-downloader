import requests
from bs4 import BeautifulSoup

linux_url = "https://runtime.fivem.net/artifacts/fivem/build_proot_linux/master/"

html = requests.get(linux_url, allow_redirects=True)
soup = BeautifulSoup(html.text, 'html.parser')
all_elements = soup.findAll('a', {'class':'panel-block'}, href=True)

linux_versions = []

for version in all_elements:
    if not version['href'] == "..":
        tag = version['href'].replace('./', '').split("-", 1)[0]
        url = linux_url + version['href'].replace('./', '')
        latest_recommended = False
        latest_optional = False
        linux_versions.append({"tag": tag, "url": url, "latest": False, "latest_recommended": False, "latest_optional": False })
    
linux_versions[0]["latest"] = True

version_buttons = soup.findAll('a', {'class':'is-link'}, href=True)

for version in version_buttons:
    tag = version['href'].replace('./', '').split("-", 1)[0]
    if "RECOMMENDED" in str(version):
        if tag in str(version):
            for index, linux_version in enumerate(linux_versions):
                if linux_version["tag"] == tag:
                    linux_versions[index]["latest_recommended"] = True
    
    if "OPTIONAL" in str(version):
        if tag in str(version):
            for index, linux_version in enumerate(linux_versions):
                if linux_version["tag"] == tag:
                    linux_versions[index]["latest_optional"] = True

for index, version in enumerate(linux_versions):
    if version["latest"]:
        open("latest.tar.gz", "wb").write(requests.get(version["url"], allow_redirects=True).content)
    if version["latest_optional"]:
        open("latest_optional.tar.gz", "wb").write(requests.get(version["url"], allow_redirects=True).content)
    if version["latest_recommended"]:
        open("latest_recommendedt.tar.gz", "wb").write(requests.get(version["url"], allow_redirects=True).content)

print("run 'tar xf fx.tar.gz' to unpack the artifact")