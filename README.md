# IUDX NLP Server  

The NLP Server is a Flask application for enabling natural language queries on elasticsearch. It uses [Flair](https://github.com/flairNLP/flair) along with a custom NER location tagger.   

For NER model, we use [DVC](https://dvc.org/doc) for versioning the model. To install DVC:  
```
pip install dvc
pip install 'dvc[gdrive]'
```  

To fetch the NER model:
```
dvc fetch -r myremote
dvc pull -r myremote
```  
This will download the tagger to the project's base directory.

### Installation  
Create a virtual environment, install the dependencies and start the server.  
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 app.py
```

### Docker  
To bring up the service using docker:  
```
docker-compose up
```


