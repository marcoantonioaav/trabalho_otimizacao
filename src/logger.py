def log_result(instance, z, x, method, time):
    log_phrase = "z= "+str(z)+", x= "+str(x)+", time= "+str(time)
    print(log_phrase)
    with open("./log/"+str(instance)+"_"+method+".log", 'a') as f:
        print(log_phrase, file=f)

def log_csv(ga_parameter, ga_parameter_value, optimality, time):
    log_phrase = str(ga_parameter_value)+","+str(optimality)+","+str(time)
    with open("./log/"+ga_parameter+".csv", 'a') as f:
        print(log_phrase, file=f)

def log_csv_multiple_seeds(ga_parameter, ga_parameter_value, optimality_list, time_list):
    log_phrase = str(ga_parameter_value)
    for i in range(len(optimality_list)):
        log_phrase +=","+str(optimality_list[i])
    for i in range(len(time_list)):
        log_phrase +=","+str(time_list[i])
    with open("./log/"+ga_parameter+".csv", 'a') as f:
        print(log_phrase, file=f)

def incialize_log_csv(ga_parameter, seeds):
    optimality_list_names = []
    time_list_names = []
    for seed in seeds:
        optimality_list_names.append("otimalidade_"+str(seed))
        time_list_names.append("tempo_"+str(seed))
    log_csv_multiple_seeds(ga_parameter, "parametro", optimality_list_names, time_list_names)
