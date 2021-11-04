def log(instance, z, x):
    log_phrase = "z= "+str(z)+", x= "+str(x)
    print(log_phrase)
    with open("./log/"+str(instance)+".log", 'w') as f:
        print(log_phrase, file=f)
