import configparser
import tweety
import sqlite3
import datetime
import os
import os.path

consulta = ''' INSERT INTO TWEETS(id, fecha, texto, autor, es_repost, cita, es_respuesta, enlace)
VALUES (?,?,?,?,?,?,?,?)
'''

DIR_BASE: str = os.path.dirname(os.path.abspath(__file__))
ruta_organizaciones: str \
    = open(os.path.join(DIR_BASE, "organizaciones.txt"), 'r')
ruta_datos: str = os.path.join(DIR_BASE, "twitter.db")
organizaciones: [str] = ruta_organizaciones.read().splitlines()

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

with sqlite3.connect(ruta_datos) as con:
    ids = con.execute("SELECT id FROM TWEETS").fetchall()
    print([id[0] for id in ids])
    ids = [str(id[0]) for id in ids]

    ap = tweety.Twitter("session")
    ap.sign_in(config['D']['u'], config['D']['cn'])

    for org in organizaciones:
        print(org)
        publis = ap.get_tweets(org)

        for publi in publis:
            try:
                if (publi.id in ids):
                    print("Continuando.")
                else:
                    id = publi.id
                    print(id)

                    fecha = publi.date
                    texto = publi.text
                    autor = publi.author.name
                    es_repost = publi.is_retweet
                    cita = publi.quoted_tweet.text if publi.is_quoted else ''
                    es_respuesta = publi.is_reply
                    enlace = publi.url
                    con.execute(consulta,
                        (id, fecha, texto, autor, es_repost, cita,
                        es_respuesta, enlace))
            except AttributeError:
                print("Error de atributo.")

    con.commit()
