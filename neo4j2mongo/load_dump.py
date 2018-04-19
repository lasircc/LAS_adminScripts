"""This module does blah blah."""

from pymongo import MongoClient
import json

# connetct to MongoDB
client = MongoClient()
client.drop_database('dump')
db = client.dump


BATCH_SIZE = 1000000
nodesCount = 0  # number of queries


# loading nodes
print('loading nodes...')
with open('data/nodes.dump') as data_file:
    nodes = json.load(data_file)
print('Done!')

mongo_list = list()

for n in nodes['results'][0]['data']:
    mongo_dict = dict()
    mongo_dict['labels'] = n['row'][0]
    mongo_dict['properties'] = dict(zip(n['row'][1], n['row'][2]))
    mongo_dict['_id'] = n['row'][3]
    mongo_list.append(mongo_dict)
    nodesCount += 1
    if nodesCount % BATCH_SIZE == 0:
        print('inserting into mongo nodes from {} to {}'.format(nodesCount - BATCH_SIZE + 1, nodesCount))
        db.nodes.insert_many(mongo_list)
        print('inserted!')
        mongo_list = list()

# clear batch if not empty
if mongo_list:
    print('inserting into mongo last {} nodes'.format(nodesCount % BATCH_SIZE))
    db.nodes.insert_many(mongo_list)
    print('inserted!')


# loading rels
print('\nloading rels...')
with open('data/rels.dump') as data_file:
    rels = json.load(data_file)
print('Done!')


relsCount = 0  # number of queries

mongo_list = list()

for n in rels['results'][0]['data']:
    mongo_dict = dict()
    mongo_dict['type'] = n['row'][0]
    if n['row'][1]:
        mongo_dict['properties'] = dict(zip(n['row'][1], n['row'][2]))
    mongo_dict['_id'] = n['row'][3]
    mongo_dict['from'] = n['row'][4]
    mongo_dict['to'] = n['row'][5]
    mongo_list.append(mongo_dict)
    relsCount += 1
    if relsCount % BATCH_SIZE == 0:
        print('inserting into mongo rels from {} to {}'.format(relsCount - BATCH_SIZE + 1, relsCount))
        db.rels.insert_many(mongo_list)
        print('inserted!')
        mongo_list = list()

# clear batch if not empty
if mongo_list:
    print('inserting into mongo last {} rels'.format(relsCount % BATCH_SIZE))
    db.rels.insert_many(mongo_list)
    print('inserted!')

print('\n\n~-~-~-~-~-~-~-~-~-~-~-~-')
print('Final report:')
print('Nodes:\t{:,}'.format(nodesCount))
print('Rels:\t{:,}'.format(relsCount))
print('\n\n')