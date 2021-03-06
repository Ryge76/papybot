import fr_core_news_sm
import logging
import json
from pathlib import Path

# create parser logger as pl for short
pl = logging.getLogger("components.parser")
nlp = fr_core_news_sm.load()
pl.info("spacy initialized")

# add custom stopwords to built-in stopwords list
parser_path = Path(__file__)  # absolute path of this script

stopwords_file = parser_path.parent / "custom_stopwords.json"

with open(stopwords_file, "rb") as f:
    custom_stopwords = json.load(f)
    nlp.Defaults.stop_words |= set(custom_stopwords)


class Analyze:
    """Analyze sentence given in parameter during instantiation. """

    @staticmethod
    def is_greeting(token):
        """Check if a word (token) is a greeting word (given our list)."""

        greeting_words = (
            "bonjour",
            "bonsoir",
            "au revoir",
            "adieu",
            "salut",
            "coucou",
            "hey",
            "'lut",
            "hello",
            "merci",
            "bonne " "nuit",
        )

        return bool(token.lower_ in greeting_words)

    @staticmethod
    def is_entity_location(ent):
        """Check if en entity found in the document has a type in the defined
        target. Require a spacy ents type. Returns a boolean."""

        target_ent_type = ("LOC", "GPE", "ORG")

        return bool(ent.label_ in target_ent_type)

    @staticmethod
    def is_travel_verb(verb_token):
        """Check if a verb token found in the document is in the defined
        target. Require a spacy ents type. Returns a boolean."""

        target_verbs = (
            "aller",
            "bouger",
            "bourlinguer",
            "circuler",
            "courir",
            "déplacer",
            "excursionner",
            "filer",
            "louvoyer",
            "marcher",
            "naviguer",
            "nomadiser",
            "pérégriner",
            "partir",
            "se balader",
            "se trouver",
            "trouver",
            "se déplacer",
            "se promener",
            "se transporter",
            "sillonner",
            "transhumer",
            "vagabonder",
            "visiter",
            "voyager",
            "se promoner",
            "se rendre",
            "voir",
        )

        return bool(verb_token.lemma_ in target_verbs)

    def __init__(self, sentence, auto=True):
        self.locations = []  # list of location entities in sentence
        self.found_locations = False
        self.travel_verbs = []  # list of travel verbs in sentence
        self.found_travel_verbs = False
        self.valuable_info = []  # out of stopword and punctuation tokens
        self.greetings = []  # list of greetings words
        self.found_greetings = False

        self.doc = nlp(sentence)
        self.entities = self.doc.ents

        if auto:
            self.get_valuable_info()
            self.check_greetings()
            self.check_location_in_entities()
            self.check_travel_verb()

    def get_entities(self):
        """Show identified entities in document"""
        print("\n Nombre d'entités trouvées: {}.".format(len(self.entities)))
        for ent in self.entities:
            print("\n Entité: {a} > Etiquette: {b}".format(a=ent.text,
                                                           b=ent.label_))

    def get_valuable_info(self):
        """"Get only tokens that are not punctuation marks or part of the
        stopwords list."""

        self.valuable_info = [token for token in self.doc
                              if not (token.is_stop or token.is_punct)]
        print(
            "\n Phrase initiale: {a}. \n Mots retenus: {b}".format(
                a=self.doc.text, b=self.valuable_info
            )
        )

    def check_greetings(self):
        """Check if there are greetings word in sentence."""
        for token in self.valuable_info:
            greeting = self.is_greeting(token)
            if greeting:
                pl.info("{} est un mot de salutation.".format(token.lemma_))
                self.greetings.append(token)
                self.found_greetings = True
                print("Salutation trouvée: {} ".format(self.greetings))
                return
        print("Pas de mots de saluation dans la phrase.")

    def is_valuable_location(self, ent):
        """Check if all token in an entity is a valid one"""

        for token in ent:
            if token in self.valuable_info:
                continue

            return False

        return True

    def check_location_in_entities(self):
        """Check if there are entities in given sentence that are considered
        location entities."""

        if self.valuable_info:

            # keep entities that are considered locations
            locations = [ent for ent in self.entities
                         if self.is_entity_location(ent)]

            # keep locations containing only valuable words
            # made to filter out wrong identifications from spacy
            valid_location = [
                ent for ent in locations if self.is_valuable_location(ent)
            ]

            if valid_location:
                self.locations = valid_location
                self.found_locations = True

            print("\n Lieu(x) trouvé(s): {}".format(self.locations))

    def check_travel_verb(self):
        """Check if there are verbs in the semantic field of travel"""
        verbs_only = [token for token in self.valuable_info
                      if token.pos_ == "VERB"]

        if verbs_only:
            for token in verbs_only:
                verb = self.is_travel_verb(token)
                if verb:
                    pl.info(
                        "{} fait partie des verbes nécessitant une recherche "
                        "sur carte.".format(token.lemma_)
                    )
                    self.travel_verbs.append(token)
                    self.found_travel_verbs = True

            print("Verbe(s) trouvé(s): {} ".format(self.travel_verbs))


def main():
    """Simple example"""

    Analyze("Salut GrandPy ! Est ce que tu connais l'adresse "
            "d'OpenClassrooms ?")


if __name__ == "__main__":
    main()
