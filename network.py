from flask import Flask, render_template, jsonify
from urllib.parse import quote_plus

import json
import sys
import urllib.request

app = Flask(__name__)

url = 'http://suggestqueries.google.com/complete/search?client=firefox&q={}'

@app.route('/')
def index():
    return render_template('index.html')

def get_related(entity):
    search_term = quote_plus('{} vs '.format(entity))
    request = urllib.request.Request(url.format(search_term))
    result = urllib.request.urlopen(request)
    suggestions = json.loads(result.read())
    return [x.replace(suggestions[0],'') for x in suggestions[1] if 'vs' not in x.replace(suggestions[0],'')]


@app.route('/get_all_related/<entities>')
def get_all_related(entities):
    entities = entities.split(',')
    nodes = dict((c,1) for c in entities)
    edges = set()

    for gen in range(1,3):
        for entity in nodes.copy():
            if nodes[entity] == gen:
                for related in get_related(entity):
                    if related not in nodes:
                        nodes[related] = gen + 1
                    edges.add((entity, related))
    return jsonify({'nodes': [{'id': k, 'group': v} for k, v in nodes.items()],
        'links': [{'source': e[0], 'target': e[1], 'value': 1} for e in edges]})
