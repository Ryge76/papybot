init: python -m spacy download fr_core_news_sm
web: gunicorn -w 3 'src:create_app()' --preload
init: flask run