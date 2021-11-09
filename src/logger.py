def log(instance, z, x, method):
    log_phrase = "z= "+str(z)+", x= "+str(x)
    print(log_phrase)
    with open("./log/"+str(instance)+"_"+method+".log", 'a') as f:
        print(log_phrase, file=f)

def log_csv(ga_parameter, ga_parameter_value, optimality, time):
    log_phrase = str(ga_parameter_value)+";"+str(optimality)+";"+str(time)
    with open("./log/"+ga_parameter+".csv", 'a') as f:
        print(log_phrase, file=f)
