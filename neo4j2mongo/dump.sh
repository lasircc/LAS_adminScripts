#!/bin/bash

# This script:
#     1. creates a Dump of neo4j (sub)graph extracting a subset of nodes and relative relationships
#     2. loads data into mongoDB
#     N.B. make sure your mongod is up&running

# usage:
#     bash dump.sh
#     run with -d for a fresh dump from neo4j (otherwise old *.dump files will be used)

# Insert node lables here, remember to escape \"
nodes=( \"Bioentity\") # \"annotation\" \"kb_node\" )

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -d|--dump)
    DUMP=1
    shift   # past value
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done

# create dump if required
if [ "$DUMP" == 1 ]; then

    labels=[
    for i in "${nodes[@]}"
    do
        if [ $i == ${nodes[0]} ]; then
            labels=$labels$i
        else
            labels=$labels,$i
        fi
    done
    labels=${labels}]
    echo
    echo 'Extrating (sub)graph with labels '$labels

    echo
    echo 'Getting nodes'
    # get nodes
    curl -H accept:application/json -H content-type:application/json \
    -o data/nodes.dump -d '{"statements":[{"statement":"MATCH (n) WHERE ANY(l1 IN LABELS(n) WHERE l1 IN {labels}) RETURN labels(n), keys(n), [x in keys(n) | n[x]], ID(n)","parameters":{"labels":'$labels'}}]}' \
    http://192.168.122.9:7474/db/data/transaction/commit

    echo
    echo 'Getting rels'
    # get rels
    curl -H accept:application/json -H content-type:application/json \
    -o data/rels.dump -d '{"statements":[{"statement":"MATCH (n)-[r]->(m) WHERE ANY(l1 IN LABELS(n) WHERE l1 IN {labels}) AND ANY(l2 IN LABELS(m) WHERE l2 IN {labels}) RETURN type(r), keys(r), [x in keys(r) | r[x]], ID(r), ID(n), ID(m)","parameters":{"labels":'$labels'}}]}' \
    http://192.168.122.9:7474/db/data/transaction/commit
fi

echo
echo 'Loading data into MongoDB'
python load_dump.py