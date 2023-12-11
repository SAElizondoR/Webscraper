import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from datetime import datetime
import dateparser
import time
from urllib import parse as urlparse
import sqlite3
import configparser

consulta = ''' INSERT INTO PUBLIS(story_id, organizacion, fecha, texto, enlace)
VALUES (?,?,?,?, ?)
'''

browser = webdriver.Firefox()
browser.get(target_url)

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

cookies = pickle.load(open(os.getcwd() + "/cookies.pkl", "rb"))
target_url = "https://mbasic.facebook.com/"

for cookie in cookies:
   browser.add_cookie(cookie)
username = browser.find_element(By.NAME, "email")
password = browser.find_element(By.NAME, "pass")
submit = browser.find_element(By.NAME, "login")
username.send_keys(config['CS']['uno'])
password.send_keys(config['CS']['dos'])
submit.click()
time.sleep(2)
pickle.dump(browser.get_cookies(), open(os.getcwd() + "/cookies.pkl", "wb"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "fb.db")
archivo = open(os.path.join(BASE_DIR, "organizaciones.txt"), 'r')
organizaciones = archivo.read().splitlines()

with sqlite3.connect(db_path) as con:
    ids = con.execute("SELECT story_id FROM PUBLIS").fetchall()
    ids = [id[0] for id in ids]
    print(ids)

    for org in organizaciones:
        print(org)
        target_url = "https://mbasic.facebook.com/" + org + "?v=timeline"
        browser.get(target_url)
        resp = browser.page_source
        # print(resp)
        soup = BeautifulSoup(resp, 'html.parser')
        # items = soup.find_all('article', {'class', '_55wo _56bf _5rgl'})
        # print(items)

        links = soup.find_all('a', href=True, string='Historia completa')
        for link in links:
            url =  "https://mbasic.facebook.com" + link['href']
            spt = urlparse.urlsplit(url)
            try:
                id = urlparse.parse_qs(spt.query)['story_fbid'][0]
            except KeyError:
                try:
                    id = urlparse.parse_qs(spt.query)['id'][0]
                except KeyError:
                    id = spt.path.split("/")[1]
            print(id)

            if (str(id) in ids):
                print("Continuando")
            else:
                browser.get(url)
                time.sleep(1)
                resp = browser.page_source
                soup = BeautifulSoup(resp, 'html.parser')
                titulo = soup.find_all('h3')[0].text
                print(titulo)
                try:
                    html = soup.find_all('div', {'class', 'bj'})[0]
                except IndexError:
                    html = soup.find_all('div', {'class', '_2vj8'})[0]
                texto = html.text
                fecha = soup.find_all('abbr')[0]
                print(fecha.text)
                fechanv = dateparser.parse(fecha.text)
                con.execute(consulta, (id, titulo, fechanv, texto, url))

con.commit()
browser.close()
