from pymongo import MongoClient
import pprint as pp
client = MongoClient('localhost:27017')
db = client.examples
node={'created': {'changeset': '37534937',
             'timestamp': '2016-03-01T03:56:46Z',
             'uid': '2657768',
             'user': 'smlevine',
             'version': '1'},
 'id': '4034056640',
 'position': [40.7582088, -74.0470171],
 'type': 'node'}

db.map.insert(node)
for row in db.map.find():
    pp.pprint(row)