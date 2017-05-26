import csv
import pysam
from knownGene import knownGene
from unknownGene import unknownGene
from py2neo import Node, Relationship
from py2neo import Graph, Path
from pandas import DataFrame

#K.exon_read_counts("J2M.bam")
def compMain(isknown, bamfile, csvfilename):
    f = open(csvfilename, "wb")
    writer = csv.writer(f, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
    if isknown: knownBool = "knownGene"
    else: knownBool = "unknownGene"
    csv_title = ["bamfile", bamfile, "isknown", knownBool]
    writer.writerow(csv_title)
    csv_attributes = ["ucsc","geneSymbol","utr:Cnt","utr:Len","utr:Cnt/Len"]
    for i in range(1, 64):
        ex = "exon" + str(i)
        csv_attributes +=[ex+":Cnt", ex+":len", ex+":Cnt/len"]
    writer.writerow(csv_attributes)

    if isknown is True:
        graph = Graph("http://neo4j:neo4jpwd@localhost:7474")
        cypher = "MATCH (n:knownGene) RETURN n.ucscGene, n.geneSymbol, n.strand, n.exonNum, n.chrom"
        results = graph.data(cypher)
        print results
        for each in results:
            K = knownGene(each['n.ucscGene'], each['n.geneSymbol'], each['n.strand'], each['n.exonNum'], each['n.chrom'])
            E_counts = K.exon_read_counts(bamfile)
            U_counts = K.utr_read_counts(bamfile)
            csv_row = [each['n.ucscGene'], each['n.geneSymbol']]
            if U_counts['length'] != 0:
                U_div = U_counts['count']/float(U_counts['length'])
            else:
                U_div = 'NaN'
            csv_row += [U_counts['count'], U_counts['length'], U_div]
            #print "typechecker:", type(each['n.exonNum'])
            for i in range(1, each['n.exonNum']+1):
                csv_row.append(E_counts['exon'+str(i)]['count'])
                csv_row.append(E_counts['exon'+str(i)]['length'])
                if E_counts['exon'+str(i)]['length'] != 0:
                    E_div = E_counts['exon'+str(i)]['count']/float(E_counts['exon'+str(i)]['length'])
                else:
                    E_div = 'NaN'
                csv_row.append(E_div)
            writer.writerow(csv_row)
        f.close()
    else:
        graph = Graph("http://neo4j:neo4jpwd@localhost:7474")
        cypher = "MATCH (u:unknownGene) RETURN u.geneSymbol, u.strand, u.exonNum, u.chrom"
        results = graph.data(cypher)
        print "results:", results
        for each in results:
            print "each:",each
            U = unknownGene(each['u.geneSymbol'], each['u.strand'], each['u.exonNum'], each['u.chrom'])
            E_counts = U.exon_read_counts(bamfile)
            U_counts = U.utr_read_counts(bamfile)
            csv_row = [U.ucscGene, each['u.geneSymbol']]
            print "U.ucsc:", U.ucscGene
            print "Ucounts:", U_counts
            if U_counts['length'] != 0:
                U_div = U_counts['count'] / float(U_counts['length'])
            else:
                U_div = 'NaN'
            csv_row += [U_counts['count'], U_counts['length'], U_div]
            for i in range(1, each['u.exonNum']+1):
                csv_row.append(E_counts['exon'+str(i)]['count'])
                csv_row.append(E_counts['exon'+str(i)]['length'])
                if E_counts['exon'+str(i)]['length'] != 0:
                    E_div = E_counts['exon'+str(i)]['count']/float(E_counts['exon'+str(i)]['length'])
                else:
                    E_div = 'NaN'
                csv_row.append(E_div)
            writer.writerow(csv_row)
        f.close()

'''print "CompMain -> j2M/S bam known"
compMain(True, "J2M.bam","j2m_known.csv")
compMain(True, "J2S.bam","j2s_known.csv")
'''
print "CompMain -> j2M/S bam unknown"
compMain(False, "J2M.bam", "j2m_unknown.csv")
compMain(False, "J2S.bam", "j2s_unknown.csv")

