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
    __primarykey__ = ""
    '''
    Properties belong to the excel file - emboj
    '''
    ucscgene = Property()
    Name = Property()
    accession = Property()
    Alus = Property()
    MinINV = Property()
    Edited = Property()

    five_utr = RelatedTo("region")
    exon1 = RelatedTo("region")
    intron1 = RelatedTo("region")

    '''
    Properties belong to the excel file - emboj
    '''
    chromosome = Property()
    strand = Property()
    txStart = Property()
    txEnd = Property()
    CdsStart = Property()
    CdsEnd = Property()
    exonCount = Property()
    exonStarts = Property()
    exonEnds = Property()

    '''
    def __init__(self, excelattribs, ucscinfo):
        self.excelattribsdict = {'ucscgene': '', 'Name': '', 'accession': '', 'Alus': '', 'MinINV': '', 'Edited': ''}
        self.ucscinfodict = {}

    def setExcel(self, excelClass):
        self.excelattribsdict['ucscgene'] = excelClass.ucscgene
        self.excelattribsdict['Name'] = excelClass.Name
        self.excelattribsdict['accession'] = excelClass.accession
        self.excelattribsdict['Alus'] = excelClass.Alus
        self.excelattribsdict['MinINV'] = excelClass.MinINV
        self.excelattribsdict['Edited'] = excelClass.Edited

    def setUCSC(self):
        pass'''

class unknownGene(GraphObject):
    __primarykey__ = ""
    '''
        Properties belong to the excel file - emboj
    '''
    ucscgene = Property()
    Name = Property()
    accession = Property()
    Alus = Property()
    MinINV = Property()
    Edited = Property()

    '''
        Properties belong to the excel file - emboj
    '''
    chromosome = Property()
    strand = Property()
    txStart = Property()
    txEnd = Property()
    CdsStart = Property()
    CdsEnd = Property()
    exonCount = Property()
    exonStarts = Property()
    exonEnds = Property()

    five_utr = RelatedTo("region")
    exon1 = RelatedTo("region")
    intron1 = RelatedTo("region")


class region(GraphObject):
    __primarykey__ = ""
    indicator = Property()
    sequence  = Property()

    U = RelatedFrom("Gene", "U")
    E = RelatedFrom("Gene", "E")
    I = RelatedFrom("Gene", "I")

    UEFrom = RelatedFrom("region", "UE")
    UETo = RelatedTo("region")

    EEFrom = RelatedFrom("region", "EE")
    EETo = RelatedTo("region")

    IEFrom = RelatedFrom("region", "IE")
    IETo = RelatedTo("region")

    EIFrom = RelatedFrom("region", "EI")
    EITo = RelatedTo("region")

    IIFrom = RelatedFrom("region", "II")
    IITo = RelatedTo("region")

    EUFrom = RelatedFrom("region", "EU")
    EUTo = RelatedTo("region")


'''
class utr5(GraphObject):
    def __init__(self):
        self.utrNum = 5
    gene = RelatedFrom("Gene", "U")

class utr3(GraphObject):
    def __init__(self):
        self.utrNum = 3
    last_exon = RelatedFrom("exon", "EU")
    last_intron = RelatedFrom("")

class exon(GraphObject):
    gene = RelatedFrom("Gene", "E")
    def __init__(self):
        self.exonNum = None

class intron(GraphObject):
    intronNum = Property()
    gene = RelatedFrom("Gene", "I")
'''
