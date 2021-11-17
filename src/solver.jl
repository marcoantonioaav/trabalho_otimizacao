using JuMP
using GLPK

function read_n(lines)
    parse(Int, lines[1][1])
end

function read_k(filename)
    n_name = parse(Int, filename[3] * filename[4])
    if (n_name-1)%3 == 0
        3
    elseif (n_name-1)%3 == 1
        5
    else
        10
    end
end

function read_ci(lines, n)
    cI =  Array{Int}(undef, n);
    for i=1:n
        cI[i] = parse(Int, lines[2][i])
    end
    cI
end

function read_cp(lines, n)
    cP = Array{Array{Int}}(undef, n);
    for i=1:n
        cP_line = Array{Int}(undef, n);
        for j=1:n
            if i == j
                cP_line[j] = 0
            else
                new_j = j-(i+1)
                new_j += 1
                if new_j >= 1
                    lines_i = i+2 
                    cP_line[j] = parse(Int, lines[lines_i][new_j])
                else
                    cP_line[j] = cP[j][i]
                end
            end
        end
        cP[i] = cP_line
    end
    cP
end

function read_p(lines, n)
    p = Array{Int}(undef, n);
    for i in 1:n
        p[i] = parse(Int, lines[n+5][i])
    end
    p 
end

function log_result(instance_name, A, S, z, n)
    println(instance_name)
    for i=1:n
        print(string(value(A[i]))*" ")
    end
    print("\n")
    for i=1:n
        print(string(value(S[i]))*" ")
    end
    print("\n")
    println(z)
    open("./log/results.log", "a") do io
        println(io, instance_name)
        for i=1:n
            print(io, string(value(A[i]))*" ")
        end
        print(io, "\n")
        for i=1:n
            print(io, string(value(S[i]))*" ")
        end
        print(io, "\n")
        println(io, z)
    end;
end

function solve(instance_name, n, k, cI, cP, p, P)
    m = Model();
    set_optimizer(m, GLPK.Optimizer; bridge_constraints=false)

    @variable(m, estaNoAviao[1:n, 1:k] >= 0, Bin);  #estaNoAviao[i, j] = a pessoa i está no avião j? 
    @variable(m, noMesmoAviao[1:n, 1:n] >= 0, Bin);  #noMesmoAviao[i, j] = a pessoa i está no avião mesmo aviao de j? 
    M = n+k+1 #big M

    #saida
    @variable(m, A[1:n] >= 1, Int);  #aloca as pessoas nos avioes (qual aviao A[i] esta a pessoa i)
    @variable(m, S[1:n] >= 0, Bin);  #seleção de pessoas (a pessoa i esta em um aviao?)

    @objective(m, Max, sum(cI[pessoa]*S[pessoa] for pessoa=1:n) + sum(cP[p1][p2]*noMesmoAviao[p1, p2] for p1=1:n for p2=1:p1));

    for pessoa=1:n
        @constraint(m, A[pessoa] <= k); #Limita valores de aviões
        @constraint(m, sum(estaNoAviao[pessoa, aviao] for aviao=1:k) == S[pessoa]); #Se uma pessoa está em qualquer avião, esta pessoa foi selecionada
        for pessoa2=1:pessoa
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
        @constraint(m, sum(p[pessoa]*estaNoAviao[pessoa, aviao] for pessoa=1:n) <= P[aviao]); #limita a ocupação dos aviões pelo seu peso maximo
        
    end

    set_time_limit_sec(m, 5400)
    println("Solving instance "*instance_name)
    optimize!(m);
    log_result(instance_name, A, S, objective_value(m), n);
end

function solve_instance(i)
    instance_name = "VA"*string(i, base=10, pad = 2)
    filename = instance_name*".dat"
    lines = []
    for line in(readlines("./data/"*filename))
        append!(lines, [split(strip(line))]);
    end
    n = read_n(lines)
    k = read_k(filename)
    cI = read_ci(lines, n)
    cP = read_cp(lines, n)
    p = read_p(lines, n)
    P =  Array{Float64}(undef, k);
    for i=1:k
        P[i] = 0.8*sum(p)*(1/k)
    end
    solve(instance_name, n, k, cI, cP, p, P)
end

for i=7:12
    solve_instance(i)
end

#solve("exemplo", 3, 2, [1 0 2], [0 1 2; 1 0 1; 2 1 0], [50 40 50], [100 100])
#log_result("instância_fake", [1 2 3], [0 1 0], 6)