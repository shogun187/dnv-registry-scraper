import requests
from bs4 import BeautifulSoup
import re

page = requests.get("https://vesselregister.dnv.com/vesselregister/details/G12916")
soup = BeautifulSoup(page.text, 'html.parser')
#extract the part you want here
script = soup.find("body").find("script")


print(script)

# #here I'm using regex to just pre process the string
# for items in re.findall(r"(\[.*\])", script.string):
#     print(items)