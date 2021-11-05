def log(instance, z, x, method):
    log_phrase = "z= "+str(z)+", x= "+str(x)
    print(log_phrase)
    with open("./log/"+str(instance)+"_"+method+".log", 'a') as f:
        print(log_phrase, file=f)
