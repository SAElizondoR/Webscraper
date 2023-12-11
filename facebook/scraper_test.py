from facebook_scraper import get_posts
import sqlite3
import datetime
import os

archivo = open(os.getcwd() + '/organizaciones.txt', 'r')
organizaciones = archivo.readlines()
# print(organizaciones)

con = sqlite3.connect(os.getcwd() + '/prueba.db')
# con.execute('''CREATE TABLE PUBLICACIONES
#    (ID INT PRIMARY KEY,
#    TEXTO TEXT,
#    FECHA INT NOT NULL,
#    ENLACE TEXT NOT NULL,
#    ORG TEXT NOT NULL)
#    ''')

consulta = ''' INSERT INTO PUBLICACIONES(ID, TEXTO, FECHA, ENLACE, ORGANIZACION)
VALUES (?,?,?,?,?)
'''
opciones = {"posts_per_page": 5}

for org in organizaciones:
    print(org)
    for pub in get_posts("nintendo", credentials=(config['CS']['uno'], config['CS']['dos'])):
        ide: int = pub['post_id']
        texto: str = pub['text']
        fecha: datetime.datetime = pub['time']
        enlace: str = pub['post_url']
        usr: str = pub['username']
        con.execute(consulta, (ide, texto, fecha, enlace, usr))
        print(pub)

con.commit()
cursor = con.execute("SELECT TEXTO, FECHA, ENLACE, ORGANIZACION FROM PUBLICACIONES")
print(cursor)

con.close()
