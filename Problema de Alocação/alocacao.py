import numpy as np
import pyomo.environ as pyEnv


path = "/home/tito/cplex/bin/x86-64_linux/cplex"


#Alocar m  tarefas para n unidades

#            Unidade 1 Unidade 2 Unidade 3 Unidade 4 
#Tarefa 1      c11      c12         c13      c14
#Tarefa 2      c21      c22         c23      c24
#Tarefa 3      c31      c32         c33      c34
#Tarefa 4      c41      c42         c43      c44


##-------------------------LEITURA DA INSTANCIA------------------------------------##
file = open('assign300.txt')
linhas = file.readlines()
file.close()

cij = []
aux = []
aux2=[]

m=int(linhas[0].split('\n')[0])
linhas = linhas[1:]

for i in range(len(linhas)):
    vet=linhas[i][:-1]
    splitada = vet.split()
    #aux.append(splitada)
    splitada = [int(i) for i in splitada if i!= '']
    aux.append(splitada)

for sublist in aux:
    for item in sublist:
        aux2.append(item)
        
tam = len(aux2)      
for i in range(m,tam+1,m):
    cij.append(aux2[i-m:i])

n = len(cij[0])

##-------------------------DECLARACAO DO MODELO E SEUS PARAMETROS--------------------##

#Modelo
modelo = pyEnv.ConcreteModel()
#Indices para tarefas a serem alocadas
modelo.I = pyEnv.RangeSet(n)
#Indices para unidades              
modelo.J = pyEnv.RangeSet(m)

#Custo de alocacao da tarefa i pra unidade j
modelo.c = pyEnv.Param(modelo.I, modelo.J,initialize=lambda modelo, i, j: cij[i-1][j-1])

#Varivaeis de decisao xij
modelo.x=pyEnv.Var(modelo.I,modelo.J, within=pyEnv.NonNegativeReals)


##-------------------------DECLARACAO DA FUNCAO OBJETIVO E RESTRICOES--------------------##

def func_objetivo(modelo):
    return sum(modelo.x[i,j] * modelo.c[i,j] for i in modelo.I for j in modelo.J)

modelo.objetivo = pyEnv.Objective(rule=func_objetivo,sense=pyEnv.minimize)

##------------------------------------------------------##
#Cada tarefa alocada para exatamente 1 unidade

def rule_rest1(modelo,i):
    return sum(modelo.x[i,j] for j in modelo.J) == 1

modelo.rest1 = pyEnv.Constraint(modelo.I,rule=rule_rest1)

##------------------------------------------------------##
#Cada unidade corresponde para exatamente 1 tarefa

def rule_rest2(modelo,j):
    return sum(modelo.x[i,j] for i in modelo.I) == 1

modelo.rest2 = pyEnv.Constraint(modelo.J,rule=rule_rest2)


##-------------------------------RESOLUCAO DO MODELO-----------------------------------##
solver = pyEnv.SolverFactory('cplex',executable=path)
resultado = solver.solve(modelo,tee = True)
print('\n-------------------------\n')
#modelo.pprint()
modelo.objetivo()
print(resultado)


##-------------------------PRINT DAS VARIAVEIS DE DECISAO ESCOLHIDAS--------------------##
##(tarefa,unidade)
#lista = list(modelo.x.keys())
#for i in lista:
#    if modelo.x[i]() != 0:
#        print(i,'--', modelo.x[i]())
