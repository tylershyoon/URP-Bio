import file_retrieval
import ucsc_mysql
import ast

def RoundsBegin():
    lst = file_retrieval.excel_retrieve('emboj200894s3.xls')
    print("lst:", lst)
    ucscs = []
    names = []
    for i in range(1, len(lst)):
        ucscs.append(lst[i][1])
        #names.append(lst[i][2])
    print "ucscs:", ucscs
    print(len(ucscs))
    return ucscs

def Round1():
    ucscs = RoundsBegin()
    #R1LIST = ucsc_mysql.Round1(ucscs)
    R1 = open("Round1","r")
    R1 = R1.readlines()
    print(R1)
    R1 = [ast.literal_eval(e)[0][:-2] for e in R1]
    ucscs = [e[:-2] for e in ucscs]
    print("ucscs:",len(ucscs), ucscs)
    print("R1:",len(R1), R1)
    diff = set(ucscs) - set(R1)
    #diff = list(diff)
    print("diff:", len(list(diff)), list(diff))
    unknownGenes = [
        'uc002yxe', 'uc003pbg', 'uc003tra', 'uc003ywp', 'uc001fxe', 'uc002mzu', 'uc001gxz', 'uc002qac', 'uc003zmv',
        'uc002qag', 'uc002qak', 'uc002rvv', 'uc003wqp', 'uc002dio', 'uc001hpb', 'uc003kgx', 'uc001xbw', 'uc001yqc',
        'uc002hgn', 'uc002gbe', 'uc002yrt', 'uc002npc', 'uc003lad', 'uc002pev', 'uc003liw', 'uc001oyy', 'uc002qpx',
        'uc003xcd', 'uc002lwl', 'uc003wwj', 'uc001czd', 'uc004avj', 'uc002mgc', 'uc002upe', 'uc001zri', 'uc004afm',
        'uc002ojr', 'uc001meo', 'uc003ceu', 'uc003sna', 'uc003mjq', 'uc002pkd', 'uc003dik', 'uc003hgn', 'uc003urg',
        'uc002fyz', 'uc004ecs', 'uc001juc', 'uc002cxo', 'uc002pzt', 'uc004acx', 'uc001zoi', 'uc001vmi', 'uc002djd',
        'uc002nro', 'uc001tfy', 'uc002qmx', 'uc003ubq', 'uc003wur', 'uc003zew', 'uc001hmw', 'uc002qbe', 'uc002pre',
        'uc002ogf', 'uc003vox', 'uc003kxm', 'uc002hfl', 'uc002qjr', 'uc003uas', 'uc002ilc', 'uc001nrz', 'uc003jiw',
        'uc002odx', 'uc001dhb', 'uc002xqr', 'uc002yvu', 'uc002xhf', 'uc002qtp', 'uc003eef', 'uc003hnw', 'uc001ofo',
        'uc002ago', 'uc003euy', 'uc003sjh', 'uc003uzi', 'uc003vad', 'uc001flv'
    ]
#Round1()
#qlst = ucsc_mysql.create_select_query_lst_Round1(ucscs)

#print qlst
#exec_lst = ucsc_mysql.create_execution_result(qlst)
#print(exec_lst)
#print(len(exec_lst))


# ROUND 2
#roun2lst = ucsc_mysql.Round2(ucscs)


'''f = open("Round2",'r')
r2ucsclst = []

for line in f:
    r2ucsclst.append(line[2:12]) # ucsc id
print(r2ucsclst)
r2ucscset = list(set(r2ucsclst))
print(len(r2ucscset))

diff = set(ucscs) - set(r2ucsclst)
print(set(ucscs) - diff)

print(diff)
print(len(diff))
print()
ucscs_no_version = [ e[:-2] for e in ucscs]
r2ucsclst_no_version = [e[:-2] for e in r2ucsclst]

diff2 = set(ucscs_no_version) - set(r2ucsclst_no_version)
print("diff2 ", diff2)
print(len(diff2))'''

#ROUND 3
#print len(file_retrieval.unknownGenes)
unknown_after_r2 = file_retrieval.unknownGenes_afterR2_retrieve()
print len(unknown_after_r2)
new_ucsc_lst = ucsc_mysql.Round3(unknown_after_r2)

def Round3checker():
    R3 = open("Round3", "r")
    R3 = R3.readlines()
    R3 = [ast.literal_eval(e) for e in R3]
    unknown_after_r3 = unknown_after_r2[:]
    for tuple in unknown_after_r3:
        for elem in R3:
            #print("elem: ", elem)
            #print("tuple: ", tuple)
            if elem[2] == tuple[2]:
                print "HURRAY"
                unknown_after_r3.remove(tuple)
    print(unknown_after_r3)
    print(len(unknown_after_r3))
#Round3checker()



#preprocessing for ROUND 4 -> saved in file_retrieval R3 result
'''f = open("Round3","r")
lst = []
f = f.readlines()
for line in f:
    linelst = line.split(",")
    lst.append(linelst[2][2:-1])
print len(lst)
print len(list(set(lst)))
print(lst)'''

#ROUND 4_2
'''unknown_after_r3 = file_retrieval.unknown_afterR3_retrieve()
new_ucsc_lst = ucsc_mysql.Round4_2(unknown_after_r3)
'''

