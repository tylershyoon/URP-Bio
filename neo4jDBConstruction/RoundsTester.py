import file_retrieval
import ucsc_mysql

lst = file_retrieval.excel_retrieve('emboj200894s3.xls')

#print("lst:", lst)
ucscs = []
names = []
for i in range(1, len(lst)):
    ucscs.append(lst[i][1])
    #names.append(lst[i][2])
print "ucscs:", ucscs
print(len(ucscs))
#ucsc_set = list(set(ucscs))
#names_set = list(set(names))
'''print("UCSCS:", len(ucscs)); print("names: ", len(names));
print(len(names_set))
print(len(ucsc_set))

print ucsc_mysql.exec_lst
print ucsc_mysql.exception_lst
'''

#qlst = ucsc_mysql.create_select_query_lst_Round1(ucscs)

#print qlst
#exec_lst = ucsc_mysql.create_execution_result(qlst)
#print(exec_lst)
#print(len(exec_lst))


# ROUND 2
#roun2lst = ucsc_mysql.Round2(ucscs)


'''f = open("Round2.txt",'r')
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
'''unknown_after_r2 = file_retrieval.unknownGenes_afterR2_retrieve()
new_ucsc_lst = ucsc_mysql.Round3(unknown_after_r2)
'''

#preprocessing for ROUND 4 -> saved in file_retrieval R3 result
'''f = open("Round3.txt","r")
lst = []
f = f.readlines()
for line in f:
    linelst = line.split(",")
    lst.append(linelst[2][2:-1])
print len(lst)
print len(list(set(lst)))
print(lst)'''

#ROUND 4_2
unknown_after_r3 = file_retrieval.unknown_afterR3_retrieve()
new_ucsc_lst = ucsc_mysql.Round4_2(unknown_after_r3)
