#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sqlite3
import simpleBlogCMS.simpleBlogCMS as cms
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
import re

app = Flask(__name__)

NB_ARTICLES_INDEX = 5

'''
S'il n'y a aucun article dans la DB
'''


@app.errorhandler(500)
def not_articles(e):
    return render_template('not_articles.html'), 500

'''
Si aucun article n'est retourné lors d'une recherche
'''


@app.errorhandler(404)
def page_not_found(e):
    cms.init_db()
    articles = cms.obtenir_plus_recent(NB_ARTICLES_INDEX)
    return render_template('404.html', articles=articles), 404

'''
"Index"
Montre les 5 articles déjà parus les plus récents
'''


@app.route('/')
def index():
    cms.init_db()
    articles = cms.obtenir_plus_recent(NB_ARTICLES_INDEX)
    return render_template('index.html', articles=articles)

'''
"Search"
Retourne le résultat de la recherche effectuée à l'index
'''


@app.route('/', methods=['POST', 'GET'])
def search():
    cms.init_db()
    articles = cms.obtenir_par_recherche(request.form['search'])
    return render_template('search.html', articles=articles)

"""
"Article"
présente un article selon l'identifiant dans l'url
"""


@app.route('/article/<identifiant>')
def article(identifiant):
    cms.init_db()
    article = cms.obtenir_par_identifiant(identifiant)
    return render_template('index.html', articles=article)

"""
"Edit"
présente un formulaire pour modifier un article
"""


@app.route('/edit/<id>')
def edit(id):
    cms.init_db()
    article = cms.obtenir_par_id(id)
    return render_template('edit.html', article=article)

"""
Modifie un article suite au formulaire, selon son id unique
"""


@app.route('/edit', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        cms.modifier(
            request.form['id'],
            request.form['titre'],
            request.form['paragraphe']
        )
    return redirect('/')

"""
Présente tous les articles de la db avec un lien pour les modifier
"""


@app.route('/admin')
def admin():
    cms.init_db()
    articles = cms.obtenir_tous()
    return render_template('admin.html', articles=articles)

"""
Présente une forme permettant de créer un nouvel article
"""


@app.route('/admin-nouveau')
def adminNouveau():
    return render_template('admin-nouveau.html')

"""
Appelle la fonction de création d'article du cms avec le contenu de la requete
"""


@app.route('/admin-nouveau', methods=['GET', 'POST'])
@app.route('/admin-nouveau-invalide', methods=['GET', 'POST'])
def nouveau():
    if request.method == 'POST':
        temp_row = [0,
                    request.form['titre'],
                    request.form['identifiant'],
                    request.form['auteur'],
                    request.form['date_publication'],
                    request.form['paragraphe']
                    ]

        invalidites = valider_row(temp_row)
        article_nouveau = cms.article.article(temp_row)

        if not invalidites:
            cms.ajouter(article_nouveau.for_db())
            return redirect(url_for('article', identifiant=temp_row[2]))
        else:
            return render_template(
                'admin-nouveau-invalide.html',
                article=article_nouveau.for_display(),
                invalidites=invalidites
            )


def valider_row(row):
    invalidites = []
    if not row[1]:
        invalidites.append(unicode("Veuillez entrer un titre.", 'utf-8'))
    if not row[2]:
        invalidites.append(unicode("Veuillez entrer un identifiant.", 'utf-8'))
    if row[2] and not caracteres_url_valide(row[2]):
        invalidites.append(
            unicode("L'identifiant doit respecter (a->z,0->9)", 'utf-8'))
    if row[2] and not cms.est_disponible(row[2]):
        invalidites.append(unicode("L'identifiant est déjà utilisé.", 'utf-8'))
    if not row[3]:
        invalidites.append(
            unicode("Veuillez entrer un nom d'auteur.", 'utf-8'))
    if not row[5]:
        invalidites.append(unicode("Veuillez écrire un paragraphe.", 'utf-8'))
    if re.search("\n", row[5]):
        print "saut de ligne dans le paragraphe"
        invalidites.append(
            unicode("Limitez vous à un seul paragraphe.", "utf-8"))
    if not row[4]:
        invalidites.append(
            unicode("Choisissez une date de publication.", 'utf-8'))

    return invalidites

"""
la section de l'url en paramètre respecte RFC 1738 et LOWERCASE
"""


def caracteres_url_valide(text):
    return re.match(r"[a-z0-9()\-$_.+!*']", text)


if __name__ == "__main__":
    app.run()
