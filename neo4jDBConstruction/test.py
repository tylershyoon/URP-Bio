
r2ucsc = []
r3ucsc = []

f = open("Round2", "r")
r2 = f.readlines()
for t in r2:
    r2ucsc.append(t.split(".")[0][2:])

g = open("Round3", "r")
r3 = g.readlines()
for t in r3:
    r3ucsc.append(t.split(".")[0][2:])

r2ucsc.sort()
r3ucsc.sort()
print r2ucsc
print r3ucsc

count = []
for x in r2ucsc:
    for y in r3ucsc:
        if x == y:
            count.append(x)

count = list(set(count))
print len(count)
