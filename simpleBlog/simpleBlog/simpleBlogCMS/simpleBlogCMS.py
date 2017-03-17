#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3
import article as article
from flask import abort
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.exceptions import HTTPException, ServiceUnavailable

ADRESSE_BASE_DONNEE = 'simpleBlogCMS/databases/simpleBlog.db'


"""
retourne une connexion sur la db et son curseur,
créer le fichier db s'il n'existe pas.
"""


def connexion():
    if not os.path.isfile(ADRESSE_BASE_DONNEE):
        conn = sqlite3.connect(ADRESSE_BASE_DONNEE)
        print "la base de donnée simpleBlog.db a été créée."
    else:
        conn = sqlite3.connect(ADRESSE_BASE_DONNEE)
    curs = conn.cursor()
    return conn, curs

"""
Vérifie que la table existe, créer la table sinon.
"""


def init_db():

    conn, curs = connexion()
    curs.execute("""
        CREATE TABLE IF NOT EXISTS article (
            id integer primary key,
            titre varchar(100),
            identifiant varchar(50),
            auteur varchar(100),
            date_publication text,
            paragraphe varchar(500)
        )
    """)
    conn.commit()
    curs.close()
    conn.close()


def aucun_articles_affichable():
    conn, curs = connexion()
    curs.execute("""
        SELECT COUNT(*) from article
        WHERE date_publication < DATETIME('now')
    """)
    return not curs.fetchall()
"""
Permet d'obtenir une liste d'articles selon
la commande sqlite3 passée en paramètre
"""


def requete(sqlite_string, args=''):
    if aucun_articles_affichable():
        abort(500)
    conn, curs = connexion()
    if args != '':
        curs.execute(sqlite_string, args)
    else:
        curs.execute(sqlite_string)

    articles = []
    for row in curs.fetchall():
        articles.append(article.article(row).for_display())
    if not articles:
        abort(404)
    conn.commit()
    curs.close()
    conn.close()
    return articles
"""
Permet de savoir si un article existe selon
une spécification de requete sqlite
"""


def est_disponible(identifiant):
    conn, curs = connexion()
    curs.execute("""
        SELECT * FROM article WHERE identifiant = ?
        COLLATE NOCASE
    """, [identifiant])
    return not curs.fetchall()

'''
Retourne tous les articles de la base de donnée
'''


def obtenir_tous():
    return requete("""
        SELECT * from article
        ORDER BY date_publication DESC
    """)

'''
Retourne les articles dont le titre
ou le paragraphe contiennent la phrase/mot clef recherché
'''


def obtenir_par_recherche(mot_clef):
    mot_clef = '%' + mot_clef + '%'
    return requete("""
        SELECT * from article
        where date_publication < DATETIME('now') AND
        ( titre like ? OR
        paragraphe like ? )
        COLLATE NOCASE
        ORDER BY date_publication DESC
    """, [mot_clef, mot_clef])

'''
retourne les n articles les plus récents
'''


def obtenir_plus_recent(n=1):
    return requete("""
        SELECT * from article
        WHERE date_publication < DATETIME('now')
        ORDER BY date_publication DESC
        LIMIT ?
    """, [n])
'''
retourne un article selon l'id unique
'''


def obtenir_par_id(id):
    return requete("""
        SELECT * from article
        WHERE id = ?
    """, [id])[0]

'''
retourne un article selon l'identifiant
'''


def obtenir_par_identifiant(identifiant):
    return requete("""
        SELECT * from article
        WHERE identifiant = ?
    """, [identifiant])

'''
Permet d'enregistrer un article dans la base de donnée
'''


def ajouter(article):
    conn, curs = connexion()
    curs.execute("""
        INSERT INTO article (titre,identifiant,auteur,
        date_publication,paragraphe)
        values(?,?,?,?,?)""",
                 [article.titre, article.identifiant, article.auteur,
                  article.date_publication, article.paragraphe]
                 )
    conn.commit()
    curs.close()
    conn.close()

'''
Permet de modifier un article
'''


def modifier(id_num, titre, paragraphe):
    conn, curs = connexion()
    curs.execute("""
        UPDATE article
        SET titre = ?,
        paragraphe = ?
        WHERE id = ?
        """,
                 [titre, paragraphe, id_num]
                 )
    conn.commit()
    curs.close()
    conn.close()
