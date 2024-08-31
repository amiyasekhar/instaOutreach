from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re

from bios import Bios
from user import User

# Set up the Safari driver
driver = webdriver.Safari()

seed_users = [
    "https://www.instagram.com/jordanplatten/",
    "https://www.instagram.com/jordanwelch/",
    "https://www.instagram.com/aribk7/",
    "https://www.instagram.com/mahenceo",
    "https://www.instagram.com/mussy.02/",
    "https://www.instagram.com/oliverb/",
    "https://www.instagram.com/toni_onis_/",
    "https://www.instagram.com/kenan.svv/",
    "https://www.instagram.com/sam.vilanovay/",
    "https://www.instagram.com/matt_mortimer/",
    "https://www.instagram.com/drizz6y/",
    "https://www.instagram.com/luechter/",
    "https://www.instagram.com/jasoncooperson/"
]

seed_user_objects = []
bio_objects = []

cookie = 'csrftoken=AkqCAvbLrpkRIWQhgGc62TlxaCunXJh1; ds_user_id=61529964100; rur="CCO\05461529964100\0541755875666:01f787ba441aae794429057047b92ed1cb0a7f9f1ef033531fb6b78910221e7e1cb91a1f"; sessionid=61529964100%3Azf15Ww6Eegk59J%3A7%3AAYfcZmi3wTFHyitiFtY7j1r16WNHt5JJZgZ5cdDdjg; wd=1728x477; ig_nrcb=1; shbid="19169\05461529964100\0541755861921:01f7aedcd50c8a8902e1480e625d9ac492a4bb48c75a0d258d4fbdbd219ee86b7da34734"; shbts="1724325921\05461529964100\0541755861921:01f731bd70c2b17b375754e3ffbd02a5d8ec1c2383ec0edab8cc0ac22d91b994ef8edd39"; ig_did=3AE20921-BE2D-41FC-9818-5D26EE3AA763; ps_l=1; ps_n=1; datr=aE24Zgrx15S4DEGh41LgxqHK; mid=ZrhNaAAEAAEGWXD8XwILj3jkcROV'
ig_app_id = '936619743392459'
# convert profiles into User objects
for seed_user_url in seed_users:
    user = User(seed_user_url, driver, cookie, ig_app_id)
    seed_user_objects.append(user)
    print(user)
    print()

for user in seed_user_objects:
    bio = Bios(user.get_bio())
    bio_objects.append(bio)

# Creating embeddings for all bios
Bios.create_embeddings()

# Find similar bios
query_bio = "Blockchain expert | Crypto tips inside 🚀"
most_similar_bios = Bios.find_similar_bios(query_bio, k=2)


with open("test.txt", "w") as file:
    file.write("Bios:\n")

    for bio in bio_objects:
        file.write(f"{bio}\n")
    file.write("\n")

    file.write(f"Query Bio: {query_bio}")
    file.write("\n")

    for bio, score in most_similar_bios:
        file.write(f"Bio: {bio}, Score: {score}\n")



driver.quit()

