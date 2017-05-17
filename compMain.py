import pysam
from py2neo import Node, Relationship
from py2neo import Graph, Path
from pandas import DataFrame

class knownGene():
    def __init__(self, ucscGene, geneSymbol, strand, exonNum):
        self.ucscGene = ucscGene
        self.geneSymbol = geneSymbol
        self.strand = strand
        self.exonNum = exonNum


    def exon_read_counts(self, bamfile):
        exonCounts = {}
        for i in range(1,self.exonNum+1):
            indicator = "exon" + str(i)
            exonCounts[indicator] = {}
            exonCounts[indicator]['count'] = 0
            exonCounts[indicator]['length'] = 0
        print exonCounts

        samfile = AlignmentFile("/mnt/d/Bio/sequence/" + bamfile, "rb")

        graph = Graph("http://neo4j:neo4jpwd@localhost:7474")

        ''' For exon 1'''
        e1cypher = "MATCH (n:knownGene{geneSymbol:'" + self.geneSymbol + \
            "'})-[:E1]-(exon1) RETURN exon1.indicator, exon1.chrom, exon1.start, exon1.end, exon1.length"
        e1 = graph.data(e1cypher)
        for r in e1:
            exonCounts['exon1']['count'] = samfile.count(r[exon1.chrom], r[exon1.start], r[exon1.end])
            exonCounts['exon1']['length'] = r[exon1.length]

        ''' For rest of the exons '''
        cypher = "MATCH (n:knownGene{geneSymbol:'" + self.geneSymbol + \
                 "'})-[:E1]-(exon1)-[:EE*]-(exon) RETURN exon.indicator, exon.chrom, exon.start, exon.end, exon.length"
        results = graph.data(cypher)
        for r in results:
            exonCounts[r[exon.indicator]]['count'] = samfile.count(r[exon.chrom], r[exon.start], r[exon.end])
            exonCounts[r[exon.indicator]]['length'] = r[exon.length]
        return exonCounts

    def utr_read_counts(self, bamfile):
        utrCount = {}
        samfile = AlignmentFile("/mnt/d/Bio/sequence/" + bamfile, "rb")

        graph = Graph("http://neo4j:neo4jpwd@localhost:7474")
        cypher = "MATCH (n:knownGene{geneSymbol:'" + self.geneSymbol + \
            "'})-[:E1]-(exon1)-[:EE*]-(last)-[:EU]-(utr)"
        if self.strand == '+':
            cypher += " RETURN utr.cdsEnd, utr.txEnd"
            results = graph.data(cypher)
            for r in results:
                utrCount['count'] = samfile.count(self.chrom, utr.cdsEnd, utr.txEnd)
                utrCount['length'] = utr.txEnd - utr.cdsEnd
        else:
            cypher += " RETURN utr.txStart, utr.cdsStart"
            results = graph.data(cypher)
            for r in results:
                utrCount['count'] = samfile.count(self.chrom, utr.txStart, utr.cdsStart)
                utrCount['length'] = utr.cdsStart - utr.txStart
        return utrCount




#K.exon_read_counts("J2M.bam")
def compMain(isknown):
    if isknown is true:
        graph = Graph("http://neo4j:neo4jpwd@localhost:7474")
        cypher = "MATCH (n:knownGene) RETURN n.ucscGene, n.geneSymbol, n.strand, n.exonNum"
        results = graph.data(cypher)

    else:
        pass


