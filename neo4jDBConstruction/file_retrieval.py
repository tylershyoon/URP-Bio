# -*- coding: cp949 -*-

import xlrd
import tools

def excel_retrieve(filename):
    wb = xlrd.open_workbook(filename)
    #print wb.sheet_names()

    # Selecting sheet, the first one
    ws = wb.sheet_by_index(0)
    nrows = ws.nrows

    row_val = []
    for row_num in range(nrows):
        #print ws.row_values((row_num))
        row_val.append(ws.row_values(row_num))
    return_lst = tools.encode_lst(row_val)
    # PRINT LST
    #tools.print_lst(return_lst)
    ALU_in_3UTR_names = [elem for elem in return_lst]
    #print ALU_in_3UTR_names
    return return_lst

''' Hard coded data - remain unknown genes after round 2 ! => For Round 3 '''
unknownGenes = [
    'uc002yxe', 'uc003pbg', 'uc003tra', 'uc003ywp', 'uc001fxe', 'uc002mzu', 'uc001gxz', 'uc002qac', 'uc003zmv', 'uc002qag', 'uc002qak', 'uc002rvv', 'uc003wqp', 'uc002dio', 'uc001hpb', 'uc003kgx', 'uc001xbw', 'uc001yqc', 'uc002hgn', 'uc002gbe', 'uc002yrt', 'uc002npc', 'uc003lad', 'uc002pev', 'uc003liw', 'uc001oyy', 'uc002qpx', 'uc003xcd', 'uc002lwl', 'uc003wwj', 'uc001czd', 'uc004avj', 'uc002mgc', 'uc002upe', 'uc001zri', 'uc004afm', 'uc002ojr', 'uc001meo', 'uc003ceu', 'uc003sna', 'uc003mjq', 'uc002pkd', 'uc003dik', 'uc003hgn', 'uc003urg', 'uc002fyz', 'uc004ecs', 'uc001juc', 'uc002cxo', 'uc002pzt', 'uc004acx', 'uc001zoi', 'uc001vmi', 'uc002djd', 'uc002nro', 'uc001tfy', 'uc002qmx', 'uc003ubq', 'uc003wur', 'uc003zew', 'uc001hmw', 'uc002qbe', 'uc002pre', 'uc002ogf', 'uc003vox', 'uc003kxm', 'uc002hfl', 'uc002qjr', 'uc003uas', 'uc002ilc', 'uc001nrz', 'uc003jiw', 'uc002odx', 'uc001dhb', 'uc002xqr', 'uc002yvu', 'uc002xhf', 'uc002qtp', 'uc003eef', 'uc003hnw', 'uc001ofo', 'uc002ago', 'uc003euy', 'uc003sjh', 'uc003uzi', 'uc003vad', 'uc001flv'
]
''' excel attributes: ucsc / name / accession / ...'''
def unknownGenes_afterR2_retrieve():
    lst = excel_retrieve('emboj200894s3.xls')
    target = []
    for row in lst:
        if row[1][:-2] in unknownGenes:
            target.append(row[1:])
    print "unknown after R2 finished"
    for elem in target:
        print elem
    return target

R3_result = [
    'NM_013229', 'NM_001012659', 'NM_001032363', 'NM_198320', 'NM_000554', 'NM_004079', 'NM_176815', 'NM_138368', 'NM_181706', 'NM_032160', 'NM_032160', 'NM_013302', 'NM_005665', 'NM_182705', 'NM_198549', 'NM_052941', 'NM_032554', 'NM_004285', 'NM_176877', 'NM_005472', 'NM_020844', 'NM_020954', 'NM_017644', 'NM_203422', 'NM_181705', 'NM_012214', 'NM_144618', 'NM_018000', 'NM_004549', 'NM_032316', 'NM_198887', 'NM_014028', 'NM_182612', 'NM_006606', 'NM_006918', 'NM_000367', 'NM_019069', 'NM_005431', 'NM_014898', 'NM_003417', 'NM_207333', 'NM_024620', 'NM_024762', 'NM_001039891', 'NM_152458', 'NM_024646'
]
def unknown_afterR3_retrieve():
    afterR2 = unknownGenes_afterR2_retrieve()
    target = []
    for row in afterR2:
        if row[2] not in R3_result:
            target.append(row)
    print "unknown after R3 finished"
    for elem in target:
        print elem
    print(len(target))
    return target

unknown_afterR3_retrieve()
#excel_retrieve('emboj200894s3.xls')
