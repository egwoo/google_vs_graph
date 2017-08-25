import json
import sys
from urllib.parse import quote_plus
import urllib.request

url='http://suggestqueries.google.com/complete/search?client=firefox&q={}'

def get_competitors(company):
    search_term = quote_plus('{} vs '.format(company))

    req = urllib.request.Request(url.format(search_term))
    res = urllib.request.urlopen(req)
    suggestions = json.loads(res.read())
    return [x.replace(suggestions[0],'') for x in suggestions[1] if 'vs' not in x.replace(suggestions[0],'')]


if __name__ == "__main__":
    companies = u' '.join(sys.argv[1:]).split(',')
    nodes = dict((c,1) for c in companies)
    edges = set()
    for company in companies:
        for c1 in get_competitors(company):
            if c1 not in nodes:
                nodes[c1] = 2
            edges.add((company, c1))
    for k in nodes.copy():
        if nodes[k] == 2:
            for c2 in get_competitors(k):
                if c2 not in nodes:
                    nodes[c2] = 3
                edges.add((k, c2))
    with open('graph.json', 'w+') as f:
      f.write(json.dumps({'nodes': [{'id': k, 'group': v} for k, v in nodes.items()], 'links': [{'source': e[0], 'target': e[1], 'value': 1} for e in edges]}))
