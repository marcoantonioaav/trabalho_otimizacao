import random

from numpy.core.numeric import Infinity
import numpy as np

n = 0
k = 1
p = []
P =  [0.8*sum(p)*(1/k)]*k
cI = []
cD = []

def evaluate(g):
    individual_profit = 0
    for i in range(n):
        if g[i] != 0:
            individual_profit += cI[i]
    pair_profit = 0
    for i in range(n):
        for j in range(n):
            if g[i] == g[j]:
                pair_profit += cD[i][j]
    return individual_profit + (pair_profit/2)

def is_valid_solution(g):
    total_weight = np.zeros(k) #inicializa os pesos com zero
    for i in range(n): 
        total_weight[g[i]] += p[i] #soma o peso atual em cada avião
    for i in range(k):
    #se algum dos pesos ultrapassa a capacidade máxima, a solução não é válida
        if total_weight[i]>P[i]:
            return False
    return True

def validate_solution(g):
    occupied = list(range(n)) #marca os elementos não nulos de g 
    while(not is_valid_solution(g)): #enquanto g não é válido
        choice = random.choice(occupied) 
        #sorteia um dos elementos não nulos
        g[choice] = 0 #torna o elemento nulo
        occupied.remove(choice)	#remove ele da lista de ocupados
    return g

def initial_solution():
    g = [None]*n #gera novo vetor de inteiros
    for i in range(n):
        g[i] = random.randint(1, k) #inicializa com valores de 1 até k
    return validate_solution(g)

def tournament(participants):
    best_individual = participants[0]
    best_profit = Infinity

    for individual in participants:
        profit = evaluate(individual)
        if profit > best_profit:
            best_individual = individual
            best_profit = profit

    return best_individual

def crossover(f, s, crossover_rate):
    if random.random() < crossover_rate:
        p = random.randint(0, n-1)	#randomiza ponto de cruzamento
        f_tail = f[p:] #separa ambos no ponto de cruzamento
        s_tail = s[p:]
        f_head = f[:p]
        s_head = s[:p]
        f = f_head + s_tail #concatena as partes gerando dois indivíduos
        s = s_head + f_tail
    return validate_solution(f), validate_solution(s)

def mutate(g, mutation_rate, displacement_rate):
    if random.random() < mutation_rate: #se o número randômico gerado é menor do que taxa de mutação
        p = random.randint(0, n-1) #escolhe um gene aleatório para mutar
        if random.random() < displacement_rate: #se número randômico gerado é menor do que taxa de desalocação
            g[p] = 0 #desaloca o passageiro
        else: #se não, muda o voo
            g[p] = random.randint(1, k)
    return validate_solution(g)

def initial_population(population_size):
    individuals = [None]*population_size
    for i in range(population_size):
        individuals[i] = initial_solution()
    return individuals

def selection(individuos, k):
    random.shuffle(individuos)
    k_individuos = individuos[:k]
    melhor_individuo = tournament(k_individuos)
    k_individuos.remove(melhor_individuo)
    segundo_melhor = tournament(k_individuos)
    k_individuos.append(melhor_individuo)

    return melhor_individuo, segundo_melhor

def run_ga(population_size, crossover_rate, elitism, mutation_rate, displacement_rate, max_generations_without_improve, max_generations, seed):
    random.seed(seed)
    individuals = initial_population(population_size)
    generations_without_improve= 0
    for generation in range(max_generations):
        new_individuals = []
        if elitism:         
            best_individual = tournament(individuals)
            new_individuals.append(best_individual)
        while len(new_individuals) < population_size:
            best_individual, second_best = selection(individuals, population_size)
            best_individual, second_best = crossover(best_individual, second_best, crossover_rate)
            best_individual = mutate(best_individual, mutation_rate, displacement_rate)
            second_best = mutate(second_best, mutation_rate, displacement_rate)
            new_individuals.append(best_individual)
            new_individuals.append(second_best)
        if evaluate(tournament(individuals)) == evaluate(tournament(new_individuals)):
            generations_without_improve += 1
        else:
            generations_without_improve = 0
        individuals = new_individuals
        if generations_without_improve > max_generations_without_improve:
            break
    return tournament(individuals)

if __name__ == "__main__":
    melhor_individuo = run_ga(30, 0.9, True, 0.75, 0.2, 20, 200, 10)
    print(melhor_individuo)
    print(evaluate(melhor_individuo))