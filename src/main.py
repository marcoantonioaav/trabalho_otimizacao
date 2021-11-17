from read_file import ReadInstance
from logger import incialize_log_csv, log_csv_multiple_seeds, log_result
from solver import solve
from ga import run_ga
import numpy as np
import timeit

def ga_test():
    for i in range(1, 2):
        if i < 10:
            instance_name = "VA0"+str(i)
        else:
            instance_name = "VA"+str(i)
        instance = ReadInstance(instance_name+".dat")
        print("Resolving instance", i)
       # z, x = run_ga(70, 0.9, True, 0.02, 0.1, 70, 11, instance)
        #log_result(i, z, x, "ga")
        z, x = solve(instance, instance_name)
        log_result(i, z, x, "solver")

def percentage(part, whole):
    return 100 * float(part)/float(whole)

def complete_test():
    best_value = {
        "VA01": 29234,
        "VA02": 22509,
        "VA03": 16118,
        "VA04": 101100,
        "VA05": 102049,
        "VA06": 51413,
        "VA07": 69977,
        "VA08": 49363,
        "VA09": 29931,
        "VA10": 270718,
        "VA11": 184909,
        "VA12": 112354
    }
    parameters = [
        {"name":"population_size", "test_range": range(7, 77, 7), "default": 35}, 
        {"name":"crossover_rate", "test_range": np.arange(0, 1.1, 0.1), "default": 0.9}, 
        {"name":"elitism", "test_range": [False, True], "default": True}, 
        {"name":"mutation_rate", "test_range": np.arange(0, 0.11, 0.01), "default": 0.02}, 
        {"name":"displacement_rate", "test_range": np.arange(0, 1.1, 0.1), "default": 0.2},
        {"name":"max_generations_without_improve", "test_range": range(7, 77, 7), "default": 35} 
    ]
    seeds = [16, 17]
    
    for p in range(len(parameters)):
        incialize_log_csv(parameters[p]["name"], seeds)
        test_parameters = []
        for attribute in parameters:
            test_parameters.append(attribute["default"])
        for test_value in parameters[p]["test_range"]:
            optimality_list =[]
            time_list = []
            for seed in seeds:
                test_parameters[p] = test_value
                optimality_avg = 0
                time_avg = 0
                for i in range(1, 13):
                    if i < 10:
                        instance_name = "VA0"+str(i)
                    else:
                        instance_name = "VA"+str(i)
                    instance = ReadInstance(instance_name+".dat")
                    print("Resolving parameter "+parameters[p]["name"]+"="+str(test_value)+", seed="+str(seed)+", instance "+instance_name)
                    start = timeit.default_timer()
                    z, x = run_ga(test_parameters[0], test_parameters[1], test_parameters[2], test_parameters[3], test_parameters[4], test_parameters[5], seed, instance)
                    stop = timeit.default_timer()
                    optimality = percentage(z, best_value[instance_name])
                    optimality_avg += optimality
                    time = stop - start
                    time_avg += time
                optimality_avg = optimality_avg/12
                time_avg = time_avg/12
                optimality_list.append(optimality_avg)
                time_list.append(time_avg)
            log_csv_multiple_seeds(parameters[p]["name"], test_value, optimality_list, time_list)
if __name__ == "__main__":
    complete_test()