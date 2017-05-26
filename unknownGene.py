from neo4jDBConstruction import file_retrieval
import csv
import pysam
from py2neo import Node, Relationship
from py2neo import Graph, Path
from pandas import DataFrame

class unknownGene():
    def __init__(self, geneSymbol, strand, exonNum, chrom):
        self.geneSymbol = geneSymbol
        self.ucscGene = self.retrieve_ucscGene(geneSymbol)
        self.strand = strand
        self.exonNum = exonNum
        self.chrom = chrom

    def retrieve_ucscGene(self, geneSymbol):
        emboj = file_retrieval.excel_retrieve("./neo4jDBConstruction/emboj200894s3.xls")
        for each in emboj:
            if each[3] == geneSymbol:
                return each[1]
        print "UNKNOWN"
        return "UNKNOWN"

    def exon_read_counts(self, bamfile):
        exonCounts = {}
        for i in range(1, self.exonNum+1):
            indicator = "exon" + str(i)
            exonCounts[indicator] = {}
            exonCounts[indicator]['count'] = 0
            exonCounts[indicator]['length'] = 0
        samfile = pysam.AlignmentFile("/mnt/d/Bio/sequence/" + bamfile, "rb")
        graph = Graph("http://neo4j:neo4jpwd@localhost:7474")

        ''' For exon 1 '''
        e1cypher = "MATCH (u:unknownGene{geneSymbol:'" + self.geneSymbol + \
                   "'})-[:E1]-(exon1) RETURN exon1.indicator, exon1.chrom, exon1.start, exon1.end, exon1.length"
        e1 = graph.data(e1cypher)

        for r in e1:
            exonCounts['exon1']['count'] = samfile.count(r['exon1.chrom'], r['exon1.start'], r['exon1.end'])
            exonCounts['exon1']['length'] = r['exon1.length']

        ''' For rest of the exons '''
        cypher = "MATCH (u:unknownGene{geneSymbol:'" + self.geneSymbol + \
                 "'})-[:E1]-(exon1)-[:EE*]-(exon) RETURN exon.indicator, exon.chrom, exon.start, exon.end, exon.length"
        results = graph.data(cypher)
        for r in results:
            exonCounts[r['exon.indicator']]['count'] = samfile.count(r['exon.chrom'], r['exon.start'], r['exon.end'])
            exonCounts[r['exon.indicator']]['length'] = r['exon.length']
        return exonCounts

    def utr_read_counts(self, bamfile):
        utrCount = {}
        samfile = pysam.AlignmentFile("/mnt/d/Bio/sequence/" + bamfile, "rb")
        graph = Graph("http://neo4j:neo4jpwd@localhost:7474")
        if self.exonNum == 1:
            print "unknown utr - exonNum: 1 "
            cypher = "MATCH (u:unknownGene{geneSymbol:'" + self.geneSymbol + \
                     "'})-[:E1]-(exon1) RETURN exon1.start, exon1.end"
            results = graph.data(cypher)
            for r in results:
                utrCount['count'] = samfile.count(self.chrom, r['exon1.start'], r['exon1.end'])
                utrCount['length'] = r['exon1.end'] - r['exon1.start']
        elif self.exonNum == 2:
            cypher = "MATCH (u:unknownGene{geneSymbol:'" + self.geneSymbol + \
                     "'})-[:E1]-(exon1)-[:EL]-(last) RETURN last.start, last.end"
            results = graph.data(cypher)
            print "CKPT", results
            for r in results:
                utrCount['count'] = samfile.count(self.chrom, r['last.start'], r['last.end'])
                utrCount['length'] = r['last.end'] - r['last.start']
        else:
            print "unknown utr - exonNum > 1"
            cypher = "MATCH (u:unknownGene{geneSymbol:'" + self.geneSymbol + \
                "'})-[:E1]-(exon1)-[:EE*]-(exons)-[:EL]-(last) RETURN last.start, last.end"
            results = graph.data(cypher)
            print "CKPT", results
            for r in results:
                utrCount['count'] = samfile.count(self.chrom, r['last.start'], r['last.end'])
                utrCount['length'] = r['last.end'] - r['last.start']
        return utrCount


#U = unknownGene("AB209023","+",13,"chr1")

