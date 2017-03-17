#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dateutil.parser
import copy
from datetime import datetime

# format iso8601
FORMAT_DATE_DB = "%Y-%m-%d %H:%M:%S"
# format iso8601 sans heure pour la sortie
FORMAT_DATE_APP = "%Y-%m-%d"


class article:
    'représente un article du simpleBlog'

    def __init__(self, row):
        self.row = row
        self.id = row[0]
        self.titre = verifier_encodage(row[1])
        self.identifiant = verifier_encodage(row[2])
        self.auteur = verifier_encodage(row[3])
        self.paragraphe = verifier_encodage(row[5])
        if row[4]:
            self.date_publication = dateutil.parser.parse(row[4])

    '''
    retourne un object article avec les données
    en unicode pour html/flask/jinja
    '''
    def for_display(self):
        unicode_article = copy.copy(self)

        unicode_article.id
        unicode_article.titre = unicode(unicode_article.titre, 'utf-8')
        unicode_article.identifiant = unicode(
            unicode_article.identifiant, 'utf-8')
        unicode_article.auteur = unicode(unicode_article.auteur, 'utf-8')
        if hasattr(unicode_article, 'date_publication'):
            unicode_article.date_publication = unicode(
                unicode_article.date_publication.strftime(
                    FORMAT_DATE_APP), 'utf-8')
        else:
            unicode_article.date_publication = "0000-00-00"
        unicode_article.paragraphe = unicode(
            unicode_article.paragraphe, 'utf-8')

        return unicode_article

    '''
    retourne un object article avec les données
    en unicode pour html/flask/jinja
    '''
    def for_db(self):
        unicode_article = copy.copy(self)

        unicode_article.id
        unicode_article.titre = unicode(unicode_article.titre, 'utf-8')
        unicode_article.identifiant = unicode(
            unicode_article.identifiant, 'utf-8')
        unicode_article.auteur = unicode(unicode_article.auteur, 'utf-8')
        unicode_article.date_publication = unicode(
            unicode_article.date_publication.strftime(FORMAT_DATE_DB), 'utf-8')
        unicode_article.paragraphe = unicode(
            unicode_article.paragraphe, 'utf-8')

        return unicode_article

'''
Detecte si un champ text est en unicode et l'encode en utf-8
avec as_unicode() constitue une implémentation du "unicode sandwich"
'''


def verifier_encodage(txt):
    if isinstance(txt, unicode):
        txt = txt.encode('UTF-8')
    return txt

'''
retourne une liste d'articles dont les données sont en unicode
'''
global as_unicode_for_list


def as_unicode_for_list(articles):

    for article in articles:
        article = article.as_unicode()

    return articles
