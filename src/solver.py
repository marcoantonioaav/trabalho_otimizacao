# https://realpython.com/linear-programming-python/

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable # pip install pulp

def convert_sa_to_g(s, a):
    s_values = []
    for var in s:
        s_values.append(var.value())
    a_values = []
    for var in a:
        a_values.append(var.value())
    g = []
    for i in range(len(s_values)):
        if s_values[i] == 1:
            g.append(int(a_values[i]))
        else:
            g.append(0)
    return g

def solve(instance, instance_name):
    # Create the model
    model = LpProblem(name=instance_name, sense=LpMaximize)

    # Initialize the decision variables
    M = instance.n+instance.k+1

    estaNoAviao = [None]*instance.n
    for i in range(instance.n):
        line = [None]*instance.k
        for j in range(instance.k):
            line[j] = LpVariable(name="estaNoAviao"+str(i)+str(j), lowBound=0, cat="Binary")
        estaNoAviao[i] = line

    noMesmoAviao = [None]*instance.n
    for i in range(instance.n):
        line = [None]*instance.n
        for j in range(instance.n):
            line[j] = LpVariable(name="noMesmoAviao"+str(i)+str(j), lowBound=0, cat="Binary")
        noMesmoAviao[i] = line

    a = [None]*instance.n
    for i in range(instance.n):
        a[i] = LpVariable(name="A"+str(i), lowBound=1, cat="Integer")

    s = [None]*instance.n
    for i in range(instance.n):
        s[i] = LpVariable(name="S"+str(i), lowBound=1, cat="Binary")

    # Add the constraints to the model
    pessoas_visitadas = []
    for pessoa in range(instance.n):
        model += (a[pessoa] <= instance.k, "0-p"+str(pessoa))
        model += (sum(estaNoAviao[pessoa][aviao] for aviao in range(instance.k)) == s[pessoa], "1-p"+str(pessoa))
        for pessoa2 in range(instance.n):
            if pessoas_visitadas.count((pessoa, pessoa2)) == 0 and  pessoas_visitadas.count((pessoa2, pessoa)) == 0:
                model += (a[pessoa] <= a[pessoa2] + M*(1- noMesmoAviao[pessoa][pessoa2]), "2-p"+str(pessoa)+"p"+str(pessoa2))
                model += (M*(1- noMesmoAviao[pessoa][pessoa2]) + a[pessoa] >= a[pessoa2], "3-p"+str(pessoa)+"p"+str(pessoa2))
                model += (noMesmoAviao[pessoa][pessoa2] <= s[pessoa], "4-p"+str(pessoa)+"p"+str(pessoa2))
                model += (noMesmoAviao[pessoa][pessoa2] <= s[pessoa2], "5-p"+str(pessoa)+"p"+str(pessoa2))
                pessoas_visitadas.append((pessoa, pessoa2))
    for aviao in range(instance.k):
        for pessoa in range(instance.n):
            model += (a[pessoa] <= aviao + M*(1-estaNoAviao[pessoa][aviao]), "6-p"+str(pessoa)+"a"+str(aviao))
            model += (M*(1-estaNoAviao[pessoa][aviao]) + a[pessoa] >= aviao, "7-p"+str(pessoa)+"a"+str(aviao))
        model += (sum(instance.p[pessoa]*estaNoAviao[pessoa][aviao] for pessoa in range(instance.n)) <= instance.P[aviao], "8-a"+str(aviao))
    
    # Add the objective function to the model
    obj_ci = list(instance.cI[pessoa]*s[pessoa] for pessoa in range(instance.n))
    obj_cp = []
    pessoas_visitadas = []
    for p1 in range(instance.n):
        for p2 in range(instance.n):
            if pessoas_visitadas.count((p1, p2)) == 0 and pessoas_visitadas.count((p2, p1)) == 0:
                obj_cp.append(instance.cP[p1][p2]*noMesmoAviao[p1][p2])
                pessoas_visitadas.append((p1, p2))
    model += lpSum(obj_ci + obj_cp)

    # Solve the problem
    status = model.solve()

    return model.objective.value(), convert_sa_to_g(s, a)