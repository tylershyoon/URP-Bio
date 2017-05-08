

def print_lst(lst):
    for elem in lst:
        print elem


# encode 2X2 matrix formatted lst u'str' => 'str'
def encode_lst(lst):
    return_lst = []
    for inst in lst:
        return_inst = []
        for elem in inst:
            if type(elem) != float:
                return_inst.append(elem.encode())
            else:
                return_inst.append(elem)
        return_lst.append(return_inst)
    #print return_lst
    return return_lst


def make_lst_into_file(filename, lst):
    f = open(filename, 'w')
    for elem in lst:
        f.write(str(elem)+'\n')
    f.close()


## Specific function - should not be used for general purpose.
def make_file_into_lst(filename):
    f = open(filename, 'r')
    f = f.readlines()
    lst = [ x[:-1] for x in f ]
    new_lst = []
    for elem in lst:
        tmp = elem[1:-1].split(',')
        tmp2 = []
        for i in range(len(tmp)):
            if i < 2 :
                tmp2.append(tmp[i][i+1:-1])
            elif i < 4:
                tmp2.append(tmp[i][2:-1])
            else:
                tmp2.append(int(tmp[i]))
        new_lst.append(tmp2)
    new_lst.sort()
    return new_lst

