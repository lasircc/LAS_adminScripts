# Dumping Neo4j and loading data into MongoDB

`dump.sh` makes a dump of a Neo4j (sub)graph and serializes data in JSON into file (*.dump). Finally, it runs `load_dump.py` for loading extracted data into the database `dump` of your local MongoDB instance.

## MongoDB, final data schema

```JavaScript
> db.nodes.findOne()
{
	"_id" : 2,
	"labels" : [
		"Bioentity",
		"Biomouse"
	],
	"properties" : {
		"identifier" : "HNC0032PRX0B02004SCR000000"
	}
}
```

```JavaScript
> db.rels.findOne()
{
	"_id" : 292,
	"from" : 2,
	"type" : "generates",
	"properties" : {
		"app" : "explant"
	},
	"to" : 164
}
```

## Querying MongoDB (example)

Get the 1-hop neighborhood of a node harnessing Mongo's aggregation framework:

```JavaScript
> db.nodes.aggregate( [
    {
        "$match":{"_id":92157} // node id
    },
    {
        $graphLookup: {
            from: "rels",
            startWith: "$_id",
            connectFromField: "to",
            connectToField: "from",
            maxDepth: 2,
            as: "connectedTo",
            depthField: "numConnections",
        }
    },
    {
        $unwind: "$connectedTo"
    },
    {
        $lookup : {
            from: "nodes",
            localField: "connectedTo.to",
            foreignField: "_id",
            as: "node"
        }
    },
    {
        "$match":{"connectedTo.numConnections":0}
    }
] ).pretty()
```



## Notes

* For a customized slicing, you may want to define your own subgraph by modifying labels stored in `nodes` in `dump.sh`
* Neo4j queries are executed leveraging Transactional Cypher HTTP endpoint (URLs are sadly hard-coded in `dump.sh`, therefore you need to make them point to the graph instance you are going to dump)
* Take a look at `requirements.txt` for `pip` requirements.