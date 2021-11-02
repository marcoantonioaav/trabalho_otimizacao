linhas = [i.strip().split() for i in open("VA01.dat").readlines()]


n = int(linhas[0][0])
linhas = linhas[1:]

ci = []
ci = linhas[0]
linhas = linhas[1:]

cij = []
cij = linhas[:n-1]
linhas = linhas[n:]

linhas = linhas[1:]
linhas = linhas[1:]

p = linhas[0]


print(n)
