import pyomo.environ as pyEnv
import numpy as np

#Single sourced facility location problem
#n=clientes
#n=clients
#m=facilidades
#m=facilities

path = "/home/tito/cplex/bin/x86-64_linux/cplex"

capacidades = []
demandas = []
custoAbertura = []
cij = []

##-------------------------LEITURA DA INSTANCIA DO PROBLEMA--------------------##
##-------------------------READING THE PROBLEM INSTANCE--------------------##

file = open('cap101')
linhas = file.readlines()
nFacilidades = int(linhas[0].split()[0])       
nClientes = int(linhas[0].split()[1])       
        
flag = 0
for i in linhas:
    L = i.split()
    if(0 < flag <= nFacilidades):
        capacidades.append(float(L[0]))
        custoAbertura.append(float(L[1]))
                
    if(flag == nFacilidades +1 ):
        demandas = [float (j) for j in L]

    if(flag >= nFacilidades +2):
        aux = []
        for j in range(len(L)):
            aux.append(float(L[j]))
        cij.append(aux)    

    flag += 1
        
cij = np.transpose(cij)
file.close()
    

##-------------------------DECLARACAO DO MODELO E SEUS PARAMETROS--------------------##
##-------------------------MODEL DEFINITION AND IT'S PARAMETERS--------------------##

#Modelo
#Model
modelo = pyEnv.ConcreteModel()

#Indices para as facilidades
#Facilities indexes
modelo.M = pyEnv.RangeSet(nFacilidades)
#Indices para os clientes
#Clients indexes
modelo.N = pyEnv.RangeSet(nClientes)

#Variavel de decisao xij
#Decision variable xij
modelo.x = pyEnv.Var(modelo.N,modelo.M,within=pyEnv.Binary)
#Variavel de decisao yi
#Decision variable yj
modelo.y = pyEnv.Var(modelo.M,within=pyEnv.Binary)

#Matriz de custos de envio cij
#Cost matrix cij
modelo.c = pyEnv.Param(modelo.N, modelo.M,initialize=lambda modelo, i, j: cij[i-1][j-1])
#Demanda de cada cliente
#Client's request
modelo.d = pyEnv.Param(modelo.N, initialize = lambda modelo, i: demandas[i-1])
#Custo de abertura de cada facilidades
#Facilities opening cost
modelo.f = pyEnv.Param(modelo.M, initialize = lambda modelo, j: custoAbertura[j-1])
#Capacidade cada facilidade
#Facilities capacities
modelo.b = pyEnv.Param(modelo.M, initialize = lambda modelo, j: capacidades[j-1])

##-------------------------DECLARACAO DA FUNCAO OBJETIVO E RESTRICOES--------------------##
##-------------------------OBJECTIVE FUNCTION DEFIINTION AND CONSTRAINTS DEFINITION--------------------##

def func_objetivo(modelo):
    return sum (modelo.f[f] * modelo.y[f] for f in modelo.M) + sum (modelo.c[c,f] * modelo.x[c,f] for c in modelo.N for f in modelo.M)

modelo.objetivo = pyEnv.Objective(rule = func_objetivo, sense = pyEnv.minimize) 

##------------------------------------------------------##
#Facilidade não exceder sua capacidade
#Facility doesn't exced it's capacity
def rule_rest1(modelo,j):
    return sum (modelo.d[c] * modelo.x[c,j] for c in modelo.N) <= modelo.b[j]

modelo.rest1 = pyEnv.Constraint(modelo.M,rule=rule_rest1)


##------------------------------------------------------##
#Cada cliente recebe de exatamente 1 facilidade
#Each client gets from exactly 1 facility
def rule_rest2(modelo,i):
    return sum (modelo.x[i,f] for f in modelo.M) == 1

modelo.rest2 = pyEnv.Constraint(modelo.N, rule=rule_rest2)


##------------------------------------------------------##
#As alocacoes sao feitas somente para facilidades abertas
#Allocates just the opened facilities
def rule_rest3(modelo,i,j):
    return  modelo.x[i,j] <= modelo.y[j]

modelo.rest3 = pyEnv.Constraint(modelo.N,modelo.M,rule=rule_rest3)


##-------------------------RESOLUCAO DO MODELO--------------------##
##-------------------------MODEL SOLVING--------------------##


solver = pyEnv.SolverFactory('cplex',executable=path)
resultado = solver.solve(modelo,tee = True)
print('\n-------------------------\n')
#modelo.pprint()
modelo.objetivo()
print(resultado)

##-------------------------PRINT DAS VARIAVEIS DE DECISAO ESCOLHIDAS--------------------##
##-------------------------DECISION VARIABLES PRINT--------------------##
##(cliente,facilidade)

lista = list(modelo.x.keys())
for i in lista:
    if modelo.x[i]() != 0:
        print(i,'--', modelo.x[i]())
