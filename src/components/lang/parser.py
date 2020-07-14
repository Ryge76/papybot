import fr_core_news_sm
import logging

# create parser logger as pl for short
pl = logging.getLogger('components.parser')
nlp = fr_core_news_sm.load()
pl.info("spacy initialized")


class Analyze:
    """Analyze sentence given in parameter during instantiation. """

    @staticmethod
    def is_greeting(token):
        greeting_words = ("bonjour", "bonsoir", "au revoir", "adieu", "salut",
                          "coucou", "hey", "'lut", "hello", "merci", "bonne "
                                                                     "nuit")

        if token.lower_ in greeting_words:
            return True
        else:
            return False

    @staticmethod
    def is_location(entity):
        """Check if en entity found in the document has a type in the defined
        target. Require a spacy ents type. Returns a boolean."""

        target_ent_type = ("LOC", "GPE", "ORG")

        if entity.label_ in target_ent_type:
            return True

        else:
            return False

    @staticmethod
    def is_travel_verb(verb_token):
        """Check if a verb token found in the document is in the defined
        target. Require a spacy ents type. Returns a boolean."""

        target_verbs = ("aller", "bouger", "bourlinguer", "circuler", "courir",
                        "déplacer", "excursionner", "filer", "louvoyer",
                        "marcher",
                        "naviguer", "nomadiser", "pérégriner", "partir",
                        "se balader", "se trouver", "trouver",
                        "se déplacer", "se promener", "se transporter",
                        "sillonner",
                        "transhumer", "vagabonder", "visiter", "voyager",
                        "se promoner", "se rendre", "voir")

        if verb_token.lemma_ in target_verbs:
            return True
        else:
            return False

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
            self.check_location()
            self.check_travel_verb()

    def get_entities(self):
        print("\n Nombre d'entités trouvées: {}.".format(len(self.entities)))
        for ent in self.entities:
            print("\n Entité: {a} > Etiquette: {b}".format(a=ent.text, b=ent.label_))

    def get_valuable_info(self):
        """"Get only tokens that are not punctuation marks or part of the
        stopwords list."""

        self.valuable_info = [token for token in self.doc if not (
                token.is_stop or token.is_punct)]
        print("\n Phrase initiale: {a}. \n Mots retenus: {b}".format(
            a=self.doc.text, b=self.valuable_info))

    def check_greetings(self):
        """Check if there are greetings word in sentence."""
        for token in self.valuable_info:
            greeting = self.is_greeting(token)
            if greeting:
                pl.info("{} est un mot de salutation.".format(
                    token.lemma_))
                self.greetings.append(token)
                self.found_greetings = True
                print("Salutation trouvée: {} ".format(self.greetings))
                return
        print("Pas de mots de saluation dans la phrase.")

    def check_location(self):
        """Check if there are entities in given sentence that are considered
        location entities."""
        for ent in self.doc.ents:
            pl.info("Recherche des entitées dans le document...")
            if ent is None:
                pl.info("Pas d'entités retrouvées.")
                return
            else:
                location = self.is_location(ent)
                if location:
                    pl.info("Entitée de lieu trouvée: {a} > label: {b}".format(
                        a=ent.text, b=ent.label_))
                    self.locations.append(ent)
                    self.found_locations = True

        print("\n Lieu(x) trouvé(s): {}".format(
            self.locations))

    def check_travel_verb(self):
        """Check if there are verbs in the semantic field of travel"""
        verbs_only = [token for token in self.valuable_info
                      if token.pos_ == "VERB"]

        if verbs_only:
            for token in verbs_only:
                verb = self.is_travel_verb(token)
                if verb:
                    pl.info("{} fait partie des verbes nécessitant une recherche "
                            "sur carte.".format(token.lemma_))
                    self.travel_verbs.append(token)
                    self.found_travel_verbs = True

            print("Verbe(s) trouvé(s): {} ".format(self.travel_verbs))

    def parse_noun_chunks(self):
        """Parse sentence to get noun chunks and their roots."""

        for chunk in self.doc.noun_chunks:
            print("Groupe nominal: ", chunk.text, " >> racine du groupe: ",
                  chunk.root.text, " > role: ", chunk.root.dep_,
                  " > racine dans la phrase: ", chunk.root.head.text)


def main():

    Analyze("Salut GrandPy ! Est ce que tu connais l'adresse "
                   "d'OpenClassrooms ?")


if __name__ == '__main__':
    main()
