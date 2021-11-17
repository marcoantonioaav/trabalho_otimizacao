# https://realpython.com/linear-programming-python/

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
import pulp # pip install pulp

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

def solve(instance, instance_name, solver_time_limit):
    # Create the model
    model = LpProblem(name=instance_name, sense=LpMaximize)

    # Initialize the decision variables
    M = instance.n+instance.k+1

    estaNoAviao = [None]*instance.n
    for i in range(instance.n):
        line = [None]*instance.k
        for j in range(instance.k):
            line[j] = LpVariable(name="estaNoAviao"+str(i)+"_"+str(j), lowBound=0, cat="Binary")
        estaNoAviao[i] = line

    #noMesmoAviao = [None]*instance.n
    #for i in range(instance.n):
    #    line = [None]*instance.n
    #    for j in range(instance.n):
    #        line[j] = LpVariable(name="noMesmoAviao"+str(i)+str(j), lowBound=0, cat="Binary")
    #    noMesmoAviao[i] = line
    noMesmoAviao = [None]*instance.n
    for i in range(instance.n):
        line = [None]*(i+1)
        for j in range(i+1):
            if i != j:
                line[j] = LpVariable(name="noMesmoAviao"+str(i)+"_"+str(j), lowBound=0, cat="Binary")
            else:
                line[j] = 0
        noMesmoAviao[i] = line

    a = [None]*instance.n
    for i in range(instance.n):
        a[i] = LpVariable(name="A"+str(i), lowBound=1, cat="Integer")

    s = [None]*instance.n
    for i in range(instance.n):
        s[i] = LpVariable(name="S"+str(i), lowBound=1, cat="Binary")

    # Add the constraints to the model
    model += (a[0] <= instance.k, "0-p0")
    model += (sum(estaNoAviao[0][aviao] for aviao in range(instance.k)) == s[0], "1-p0")
    for pessoa in range(1, instance.n):
        model += (a[pessoa] <= instance.k, "0-p"+str(pessoa))
        model += (sum(estaNoAviao[pessoa][aviao] for aviao in range(instance.k)) == s[pessoa], "1-p"+str(pessoa))
        for pessoa2 in range(pessoa):
            model += (a[pessoa] <= a[pessoa2] + M*(1- noMesmoAviao[pessoa][pessoa2]), "2-p"+str(pessoa)+"p"+str(pessoa2))
            model += (M*(1- noMesmoAviao[pessoa][pessoa2]) + a[pessoa] >= a[pessoa2], "3-p"+str(pessoa)+"p"+str(pessoa2))
            model += (noMesmoAviao[pessoa][pessoa2] <= s[pessoa], "4-p"+str(pessoa)+"p"+str(pessoa2))
            model += (noMesmoAviao[pessoa][pessoa2] <= s[pessoa2], "5-p"+str(pessoa)+"p"+str(pessoa2))
    for aviao in range(instance.k):
        for pessoa in range(instance.n):
            model += (a[pessoa] <= aviao + M*(1-estaNoAviao[pessoa][aviao]), "6-p"+str(pessoa)+"a"+str(aviao))
            model += (M*(1-estaNoAviao[pessoa][aviao]) + a[pessoa] >= aviao, "7-p"+str(pessoa)+"a"+str(aviao))
        model += (sum(instance.p[pessoa]*estaNoAviao[pessoa][aviao] for pessoa in range(instance.n)) <= instance.P[aviao], "8-a"+str(aviao))
    
    # Add the objective function to the model
    obj_ci = list(instance.cI[pessoa]*s[pessoa] for pessoa in range(instance.n))
    obj_cp = []
    for p1 in range(1, instance.n):
        for p2 in range(p1):
            obj_cp.append(instance.cP[p1][p2]*noMesmoAviao[p1][p2])
    model += lpSum(obj_ci + obj_cp)

    #print(pulp.LpSolverDefault)
    # Solve the problem
    solver = pulp.PULP_CBC_CMD(timeLimit=solver_time_limit)
    status = model.solve(solver)
    #status = solver.findSolutionValues(model)

    return model.objective.value(), convert_sa_to_g(s, a)