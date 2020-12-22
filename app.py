import json
import numpy as np
import requests

from flask import jsonify
from flask import Flask, request
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.embeddings import WordEmbeddings, DocumentPoolEmbeddings
from flair.data import Label

app = Flask(__name__)

tagger = SequenceTagger.load('best-model.pt')
glove_embedding = WordEmbeddings('glove')
document_embeddings = DocumentPoolEmbeddings([glove_embedding])

@app.route('/')
def test_server():
    return "Server is running"

@app.route('/indexdoc', methods=['POST'])
def index_doc():
    docs = request.get_json()
    print(docs)
    source = [docs['_source']]
    #source = [doc['_source'] for doc in docs]
    # this needs to be modified
    tags_arr = source[0]['tags']
    tags = ""
    for tag in tags_arr:
        tags+=tag
        tags+=", "
    tags_vector = embed_text(tags)
    return jsonify({"result": tags_vector.tolist()})

@app.route('/search',methods=['GET'])
def search():
    query = request.args.get("q")
    location = " "
    location = nertagger(query)
    print(location)
    query_vector = embed_text(query)
    #return '{} {}'.format(json.dumps(query_vector.tolist()), location)
    return jsonify({"result": query_vector.tolist(), "location": location})

# Helper functions #
def embed_text(doc):
    sentence = Sentence(doc)
    document_embeddings.embed(sentence)
    embeddings = sentence.embedding.numpy()
    return embeddings

def nertagger(query):
    sentence = Sentence(query)
    tagger.predict(sentence)
    location = "EMPTY"
    response = sentence.to_dict(tag_type='ner')
    for entity in response['entities']:
        if entity['labels'][0].to_dict()['value']=="LOC":
            location =entity['text']
    return location
    
def find_lat_long(location):
    # change to pelias endpoint
    URL = "http://localhost:4000/v1/search"
    PARAMS = {"text":location}
    r = requests.get(url = URL, params = PARAMS) 
    data = r.json()
    print(data["bbox"])
    return data["bbox"]

if __name__ == '__main__':
    app.run()