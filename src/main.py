from read_file import ReadInstance
from logger import log
from solver import solve
from ga import run_ga

for i in range(1, 4):
    if i < 10:
        instance_name = "VA0"+str(i)
    else:
        instance_name = "VA"+str(i)
    instance = ReadInstance(instance_name+".dat")
    print("Resolving instance", i)
    z, x = run_ga(20, 0.9, True, 0.015, 0.2, 10, 100, 10, instance)
    log(i, z, x, "ga")
    #z, x = solve(instance, instance_name)
    #log(i, z, x, "solver")