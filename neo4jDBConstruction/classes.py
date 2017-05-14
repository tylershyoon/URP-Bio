from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject, Property, PropertyDict, RelatedTo, RelatedFrom

class excelattribs():
    def __init__(self):
        self.ucscgene = None
        self.Name = None
        self.accession = None
        self.Alus = None
        self.MinINV = None
        self.Edited = None

    def setAttribs(self, lst):
        self.ucscgene = lst[0]
        self.Name = lst[1]
        self.accession = lst[2]
        self.Alus = lst[3]
        self.MinINV = lst[4]
        self.Edited = lst[5]

excel_label = "EXCELFILE"

exceltuple = {
    'label': excel_label,
    'properties': {
        'ucscgene': '',
        'Name': '',
        'accession': '',
        'Alus': '',
        'MinINV': '',
        'Edited': ''
    }
}

class knownGene(GraphObject):
    __primarykey__ = "ucscGene"

    ucscGene = Property(); geneSymbol = Property(); accession = Property(); chrom = Property();
    strand = Property(); txStart = Property(); txEnd = Property(); cdsStart = Property()
    cdsEnd = Property(); exonNum = Property(); exonStarts = Property(); exonEnds = Property()
    '''
    Properties belong to the excel file - emboj
    '''
    Alus = Property()
    MinINV = Property()
    Edited = Property()

    exon1 = RelatedTo("region")
    intron1 = RelatedTo("region")

class region(GraphObject):
    def __copy__(self):
        return self
    def __deepcopy__(self, memo):
        return self
    __primarykey__ = "ucscGene"
    ucscGene = Property()
    indicator = Property()
    #sequence  = Property()
    chrom = Property()
    start = Property()
    end = Property()
    length = Property()

    E = RelatedFrom("knownGene", "EXON1") # gene -> exon

    EEFrom = RelatedFrom("region", "EE")
    EE = RelatedTo("region")
