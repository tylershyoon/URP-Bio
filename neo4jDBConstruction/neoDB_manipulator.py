import construction_main
from py2neo import Node, Relationship
from py2neo import Graph, Path
from pandas import DataFrame

def known_retrieval():
    graph = Graph("http://neo4j:neo4jpwd@localhost:7474")
    utrCypher = "MATCH (n:knownGene)-[:E1]-(e1)-[:EE*]-(last)-[:EU]-(utr) RETURN n.geneSymbol, utr.txEnd, utr.cdsEnd"
    testCypher = "MATCH (n:knownGene) RETURN n.geneSymbol"

    #results = graph.cypher.execute(utrCypher)
    print(DataFrame(graph.data(utrCypher)))

def unknown_retrieval():
    pass

known_retrieval()
