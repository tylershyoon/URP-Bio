import file_retrieval
import pymysql
import tools


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
    print 'Query: ', query
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

def create_select_query_lst(name_lst):
    query_lst=[]
    s = ['K.chrom', 'K.strand', 'K.txStart', 'K.cdsStart', 'K.cdsEnd', 'K.txEnd', 'K.exonCount', 'K.exonStarts', 'K.exonEnds']
    f = ['knownGene as K']
    w = ['K.name=X.kgId AND', 'X.refseq!="" AND']


# input parameter, name_lst has come from emboj~.xls excel file.
def create_select_query_lst_PAST(name_lst):
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
    # The function, make_file_into_lst() is specifically used - Cannot be used for general-formatted files.
    exec_lst = tools.make_file_into_lst('alu_in_3UTR_info.txt')
    exception_lst = create_exception_lst()
