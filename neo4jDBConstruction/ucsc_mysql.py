import file_retrieval
import pymysql
import tools
import ast


# DB -> 'hg38' / Patch number annotated til Patch9 => 'hg38Patch9'
def connect(DB):
    conn = pymysql.connect(host='genome-mysql.cse.ucsc.edu', user='genome', db=DB)
    if conn:
        print 'Connection with ucsc-genome-mysql ' + DB + " Done"
    return conn

def execute(conn, query, dictionary=False):
    if dictionary:
        curs = conn.cursor(pymysql.cursors.DictCursor)
    else:
        curs = conn.cursor()
    curs.execute(query)
    return curs

''' For S-F-W structure '''
def lst_to_str(sel_lst, from_lst, where_lst):
    sel_str = ', '.join(sel_lst); from_str = ', '.join(from_lst); where_str = ' '.join(where_lst)
    return sel_str, from_str, where_str

def select(conn, sel_lst, from_lst, where_lst):
    sel_str, from_str, where_str = lst_to_str(sel_lst, from_lst, where_lst)
    query = 'select distinct ' + sel_str + ' from ' + from_str + ' where ' + where_str
    #print 'Query: ', query
    execute(conn, query)

# DB close
def close(conn):
    conn.close()
    print 'DB connection closed'

''' For reference '''
def sfw_example():
    a = connect('hg38')
    s = ['X.geneSymbol','X.refseq', 'K.txStart','K.cdsStart', 'K.txEnd', 'K.cdsEnd']
    f = ['kgXref as X', 'knownGene as K']
    w = ['X.geneSymbol!="" AND', 'K.name=X.kgId AND', 'K.strand="+" AND', 'X.geneSymbol like "RPL__" AND', 'X.refseq!=""']
    select(a, s, f, w)
    close(a)

''' Query Execution for R1 to R3 '''
def query_execution_round1(conn, f, query, lst):
    curs = execute(conn, query)
    for row in curs:
        print(row)
        newrow = []
        for i in range(8):
            newrow.append(row[i])
        newrow.append(' '.join(row[8].split(',')))
        newrow.append(' '.join(row[9].split(',')))
        lst.append(row[0])
        f.write(str(newrow))
        f.write("\n")

def query_execution(conn, f, query, lst):
    #conn = connect('hg38')
    curs = execute(conn, query)
    for row in curs:
        newrow = []
        for i in range(10):
            newrow.append(row[i])
        newrow.append(' '.join(row[10].split(',')))
        newrow.append(' '.join(row[11].split(',')))
        lst.append(row[0])
        f.write(str(newrow))
        f.write("\n")

def query_execution_round3(conn, f, query, lst):
    #conn = connect('hg38')
    R2 = open("Round2","r")
    R2 = R2.readlines()
    R2 = [ast.literal_eval(e) for e in R2]
    curs = execute(conn, query)
    for row in curs:
        newrow = []
        for i in range(10):
            newrow.append(row[i])
        newrow.append(' '.join(row[10].split(',')))
        newrow.append(' '.join(row[11].split(',')))
        if newrow in R2:
            lst.append(row[0])
            f.write(str(newrow))
            f.write("\n")
        else:
            print "BATS!!!!"

''' Round 1 - hg38 schema -> knownGene Table using ucsc gene ID '''
def Round1(ucsc_lst):
    conn = connect('hg38')
    R1 = open("Round1", "w")
    s=['K.name', 'K.chrom', 'K.strand', 'K.txStart', 'K.cdsStart', 'K.cdsEnd', 'K.txEnd', 'K.exonCount', 'K.exonStarts', 'K.exonEnds']
    f=['knownGene as K']
    w=['K.name!="" AND']
    lst = []
    for ucsc in ucsc_lst:
        ucsc_match = 'K.name like "' + ucsc[:-2] + '%"'
        w.append(ucsc_match)
        ss, fs, ws = lst_to_str(s, f, w)
        Q = 'SELECT ' + ss + ' FROM ' + fs + ' WHERE ' + ws
        print Q
        query_execution_round1(conn, R1, Q, lst)
        w = w[:-1]
    R1.close()
    return lst

''' Round 2 - hg38 schema -> knownGene join kgXref'''
def Round2(ucsc_lst):
    conn = connect('hg38')
    R2 = open("Round2", "w")
    s = ['K.name', 'X.geneSymbol', 'X.refseq', 'K.chrom', 'K.strand', 'K.txStart', 'K.cdsStart', 'K.cdsEnd', 'K.txEnd', 'K.exonCount',
         'K.exonStarts', 'K.exonEnds']
    f = ['kgXref as X', 'knownGene as K']
    w = ['K.name=X.kgID AND','K.name!="" AND']
    lst = []
    for ucsc in ucsc_lst:
        ucsc_match = 'K.name like "' + ucsc[:-1] + '%"'
        w.append(ucsc_match)
        ss, fs, ws = lst_to_str(s, f, w)
        Q = 'SELECT ' + ss + ' FROM ' + fs + ' WHERE ' + ws
        print Q
        query_execution(conn, R2, Q, lst)
        w = w[:-1]
    R2.close()
    return lst

''' Round 3 -> searched by Accession in excel -> unknown lists extracted from Round 2,
excel info of the unknown lists are obtained by the function in file_retrieval.
Try to do in R3: keep same format of information that are retrieved from accession.
excel.Accession = kgXref.refseq
kgXref natural join with knownGene
'''
def Round3(unknown_after_r2):
    conn = connect('hg38')
    R3 = open("R3_in_R2", "w")
    s = ['K.name', 'X.geneSymbol', 'X.refseq', 'K.chrom', 'K.strand', 'K.txStart', 'K.cdsStart', 'K.cdsEnd', 'K.txEnd',
         'K.exonCount',
         'K.exonStarts', 'K.exonEnds']
    f = ['kgXref as X', 'knownGene as K']
    w = ['K.name=X.kgID AND', 'X.refseq!="" AND']

    lst = []
    for tuple in unknown_after_r2:
        refseq_match = 'X.refseq like "' + tuple[2] + '"'
        w.append(refseq_match)
        ss, fs, ws = lst_to_str(s, f, w)
        Q = 'SELECT ' + ss + ' FROM ' + fs + ' WHERE ' + ws
        print Q
        query_execution_round3(conn, R3, Q, lst)
        w = w[:-1]
    R3.close()
    return lst

''' Query execution & Round4_2 code for R4-2
Data retrieved solely from all_mrna table, retrieved data format is different from the prev.
Initially data of unknown after-r3 pushed as an input.
'''
def query_execution_R4_2(conn, f, query, lst):
    curs = execute(conn, query)
    for row in curs:
        newrow = []
        for i in range(6):
            newrow.append(row[i])
        newrow.append(' '.join(row[6].split(',')))
        newrow.append(' '.join(row[7].split(',')))
        newrow.append(' '.join(row[8].split(',')))
        lst.append(row[0])
        f.write(str(newrow))
        f.write("\n")

def Round4_2(unknown_after_r3):
    conn = connect('hg38')
    R4 = open("Round4_2", "w")
    s = ['A.qName', 'A.tName', 'A.strand', 'A.tStart', 'A.tEnd', 'A.blockCount', 'A.BlockSizes', 'A.tStarts', 'A.qStarts']
    f = ['all_mrna as A']
    w = []
    lst = []
    for tuple in unknown_after_r3:
        qname_match = 'A.qName like "' + tuple[2] +'"'
        w.append(qname_match)
        ss, fs, ws = lst_to_str(s, f, w)
        Q = 'SELECT ' + ss + ' FROM ' + fs + ' WHERE ' + ws
        print Q
        query_execution_R4_2(conn, R4, Q, lst)
        w = w[:-1]
    R4.close()
    return lst

def create_select_query_lst_new(name_lst):
    query_lst=[]
    s = ['K.chrom', 'K.strand', 'K.txStart', 'K.cdsStart', 'K.cdsEnd', 'K.txEnd', 'K.exonCount', 'K.exonStarts', 'K.exonEnds']
    f = ['knownGene as K']
    w = ['K.name=X.kgId AND', 'X.refseq!="" AND']
    for name in name_lst:
        pass

# input parameter, name_lst has come from emboj~.xls excel file.
def create_select_query_lst(name_lst):
    query_lst = []

    s = ['X.geneSymbol', 'X.refseq', 'K.chrom', 'K.strand', 'K.txStart', 'K.cdsStart', 'K.cdsEnd', 'K.txEnd', 'K.exonCount', 'K.exonStarts', 'K.exonEnds']
    f = ['kgXref as X', 'knownGene as K']
    w = ['K.name=X.kgId AND', 'X.refseq!="" AND']
    for name in name_lst:
        gene_match = 'X.geneSymbol="' + name + '"'
        w.append(gene_match)
        sel_str, from_str, where_str = lst_to_str(s, f, w)
        tmp_query = 'SELECT distinct ' + sel_str + ' FROM ' + from_str + ' WHERE ' + where_str
        query_lst.append(tmp_query)
        w = w[:-1]
    tools.print_lst(query_lst)
    print(len(query_lst))
    return query_lst

def create_execution_result(query_lst):
    exec_lst = []

    # DB Connection
    conn = connect('hg38')

    for query in query_lst:
        curs = execute(conn, query)
        for row in curs:
            exec_lst.append(row)
    close(conn)
    # DB Closure
    tools.print_lst(exec_lst)
    return exec_lst


def create_ALU_in_3UTR_lst(ALU_in_3UTR_names):
    select_query_lst = create_select_query_lst(ALU_in_3UTR_names)
    exec_lst = create_execution_result(select_query_lst)
    tools.make_lst_into_file('alu_in_3UTR_info.txt', exec_lst)


# Define "exception" including genes(or mRNA) that does not has conventional gene names.
def create_exception_lst():
    exec_lst_names = [ x[0] for x in exec_lst ]
    exception_lst = list( set(ALU_in_3UTR_names) - set(exec_lst_names) )
    exception_lst.sort()
    return exception_lst


# common declaration - either direct interpret or import
ALU_in_3UTR_lst = file_retrieval.excel_retrieve('emboj200894s3.xls')
ALU_in_3UTR_names = [elem[2] for elem in ALU_in_3UTR_lst][1:]

if __name__ == "__main__":
    create_ALU_in_3UTR_lst(ALU_in_3UTR_names)
else:
    pass
    # The function, make_file_into_lst() is specifically used - Cannot be used for general-formatted files.
    #exec_lst = tools.make_file_into_lst('alu_in_3UTR_info.txt')
    #exception_lst = create_exception_lst()
