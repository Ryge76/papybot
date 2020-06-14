import spacy
import fr_core_news_sm
import logging

# create parser logger as pl for short
pl = logging.getLogger('components.parser')
pl.info("spacy initialized")

# nlp = spacy.load("fr_core_news_sm")
nlp = fr_core_news_sm.load()

# demo sentence
doc = nlp("Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?")

"""
Etapes: 
    - chercher les verbes
    - chercher les entités
    - voir si lien entre les verbes et les entités
    - voir si entités correspond à un lieu géographique
    - sinon recherche sur les mots
"""

# get valuable tokens from sentence by getting rid of punctuation and words in stop-word list
for token in doc:
    if not (token.is_stop or token.is_punct):
        print(token.text)

valuable_info = [token for token in doc if not (token.is_stop or token.is_punct)]
print(valuable_info)

# get lemma for every valuable token

# get entities from sentence
for ent in doc.ents:
    print(ent.label_, ent.text)





