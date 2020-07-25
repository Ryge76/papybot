# Papybot

Meet Papybot !
A Flask project to discover a python micro-framework, while talking about nearly any place in the world ! Well... 
assumed you ask him in French (for now !).

Papybot (like our grandparents) has always a word about any specific place you ask for. 
Try it live at [heroku]


# Requirements

- Python 3.7.7 64 bits
- Spacy 2.3.2 (Natural Language Processor)
- Flask (of course)
- Requests
- Google Maps credentials (API key)

See `Pipfile` or `requirements.txt` for complete list of packages and dependencies.

# Installation

1. First, you should **install python** [python.org]

2. **Clone or download this repository.**

3. Once done, **install a virtual environment manager** (here we'll use pipenv [pipenv]). 

4. With Pipenv, create a virtual environment inside the folder you've clone this repository (or inside the folder you've unpacked 
the zip file):

    `pipenv install` or `pipenv install -r folder_of_your_copy/requirements.txt`

5. Register your Google API Key in environnement variables

6. Finally, type ``pipenv run flask run `` The application should be accessible on http://127.0.0.1:5000


# What's next ?

- English support
- More communication capabilities (Text-to-speech, Speech-To-Text, General or Specific Conversation capabilities)
- UI/UX
