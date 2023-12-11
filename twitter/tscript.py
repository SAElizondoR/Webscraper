from tweety import *
import sqlite3
import datetime
import os
import os.path

consulta = ''' INSERT INTO TWEETS(id, fecha, texto, autor, es_repost, cita, es_respuesta, enlace)
VALUES (?,?,?,?,?,?,?,?)
'''

app = Twitter("session")
app.sign_in(config['CS']['tres'], config['CS']['dos'])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "twitter.db")
archivo = open(os.path.join(BASE_DIR, "organizaciones.txt"), 'r')
organizaciones = archivo.read().splitlines()

with sqlite3.connect(db_path) as con:
    ids = con.execute("SELECT id FROM TWEETS").fetchall()
    print([id[0] for id in ids])
    for org in organizaciones:
        print(org)
        all_tweets = app.get_tweets(org)
        for tweet in all_tweets:
            try:
                print(tweet.id)
                print(int(tweet.id) in [int(id[0]) for id in ids])
                if (int(tweet.id) in [int(id[0]) for id in ids]):
                    print("Continuando")
                else:
                    id = tweet.id
                    fecha = tweet.date
                    texto = tweet.text
                    autor = tweet.author.name
                    es_repost = tweet.is_retweet
                    cita = tweet.quoted_tweet.text if tweet.is_quoted else ''
                    es_respuesta = tweet.is_reply
                    enlace = tweet.url
                    con.execute(consulta, (id, fecha, texto, autor, es_repost, cita, es_respuesta, enlace))
            except AttributeError:
                print("Error de atributo.")

    con.commit()
