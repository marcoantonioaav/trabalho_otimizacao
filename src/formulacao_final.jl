using JuMP
using GLPK

m = Model();
set_optimizer(m, GLPK.Optimizer);

#dados de entrada
n = 2                #numero de pessoas
k =  2               #numero de avioes
p = [60, 50]            #pesos das pessoas 
cIndividual = [200, 300] #valor que cada pessoa quer pagar
cDupla = [0 10; 10 0] #valor que cada pessoa pagaria a mais se a outra pessoa estivesse no mesmo avião
@variable(m, P[1:k] >= 0, Int);             #peso máximo de cada avião

@variable(m, estaNoAviao[1:n, 1:k] >= 0, Bin);  #estaNoAviao[i, j] = a pessoa i está no avião j? 
@variable(m, noMesmoAviao[1:n, 1:n] >= 0, Bin);  #noMesmoAviao[i, j] = a pessoa i está no avião mesmo aviao de j? 
M = n+k+1 #big M

#saida
@variable(m, A[1:n] >= 1, Int);  #aloca as pessoas nos avioes (qual aviao A[i] esta a pessoa i)
@variable(m, S[1:n] >= 0, Bin);  #seleção de pessoas (a pessoa i esta em um aviao?)

@objective(m, Max, sum(cIndividual[pessoa]*S[pessoa] for pessoa=1:n) + sum(cDupla[p1, p2]*noMesmoAviao[p1, p2] for p1=1:n for p2=1:n)/2);

for pessoa=1:n
    @constraint(m, A[pessoa] <= k); #Limita valores de aviões
    @constraint(m, sum(estaNoAviao[pessoa, aviao] for aviao=1:k) == S[pessoa]); #Se uma pessoa está em qualquer avião, esta pessoa foi selecionada
    for pessoa2=1:n
        @constraint(m, A[pessoa] <= A[pessoa2] + M*(1- noMesmoAviao[pessoa, pessoa2])); #Se o avião de duas pessoas são iguais então estão no mesmo avião
        @constraint(m, M*(1- noMesmoAviao[pessoa, pessoa2]) + A[pessoa] >= A[pessoa2]); #Se o avião de duas pessoas são iguais então estão no mesmo avião
        @constraint(m, noMesmoAviao[pessoa, pessoa2] <= S[pessoa]); #Duas pessoas só podem estar no mesmo avião se estão em algum avião
        @constraint(m, noMesmoAviao[pessoa, pessoa2] <= S[pessoa2]); #Duas pessoas só podem estar no mesmo avião se estão em algum avião
    end
end
for aviao=1:k
    for pessoa=1:n
        @constraint(m, A[pessoa] <= aviao + M*(1-estaNoAviao[pessoa, aviao])); #mapeia A[pessoa] em aviões
        @constraint(m, M*(1-estaNoAviao[pessoa, aviao]) + A[pessoa] >= aviao); #mapeia A[pessoa] em aviões
    end
    #@constraint(m, P[aviao] == 0.8*sum(p)*(1/k)); #Nas instâncias a capacidade de cada avião é 80 % de um k-ésimo do peso total das pessoas.
    @constraint(m, P[aviao] == 60); #Restrição para testes
    @constraint(m, sum(p[pessoa]*estaNoAviao[pessoa, aviao] for pessoa=1:n) <= P[aviao]); #limita a ocupação dos aviões pelo seu peso maximo
    
end

optimize!(m);

for pessoa=1:n
    println("A[$(pessoa)] = $(value(A[pessoa])), S[$(pessoa)] = $(value(S[pessoa]))");
end
println("z = $(objective_value(m))");