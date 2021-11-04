def remove_lines(lines, number_of_lines):
    return lines[number_of_lines:]

def read_n(lines):
    return int(lines[0][0])

def read_k(filename):
    n_name = int(list(filename)[2] + list(filename)[3])
    if (n_name-1)%3 == 0:
        return 3
    if (n_name-1)%3 == 1:
        return 5
    return 10

def read_ci(lines, n):
    new_lines = remove_lines(lines, 1)
    cI = [None]*n
    for i in range(n):
        cI[i] = int(new_lines[0][i])
    return cI

def read_cp(lines, n):
    new_lines = remove_lines(lines, 2)
    new_lines = new_lines[:n-1]
    cP = [None]*n
    for i in range(n):
        cP_line = [None]*n
        for j in range(n):
            if i == j:
                cP_line[j] = 0
            else:
                new_j = j-(i+1)
                if new_j >= 0:
                    cP_line[j] = int(new_lines[i][new_j])
                else:
                    cP_line[j] = cP[j][i]
        cP[i] = cP_line
    return cP

def read_p(lines, n):
    new_lines = remove_lines(lines, n+4)
    p = [None]*n
    for i in range(n):
        p[i] = int(new_lines[0][i])
    return p 

class ReadInstance:
    n = 0
    k = 1
    p = []
    P =  []
    cI = []
    cP = []

    def __init__(self, filename):
        lines = [i.strip().split() for i in open("./data/"+filename).readlines()]
        self.n = read_n(lines)
        self.k = read_k(filename)
        self.cI = read_ci(lines, self.n)
        self.cP = read_cp(lines, self.n)
        self.p = read_p(lines, self.n)
        self.P =  [0.8*sum(self.p)*(1/self.k)]*self.k
