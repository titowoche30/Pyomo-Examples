import numpy as np
import pyomo.environ as pyEnv

path = "/home/tito/cplex/bin/x86-64_linux/cplex"
#            Cliente 1 Cliente 2 
#Fabrica 1    c11        c12      
#Fabrica 2    c21        c22      
#Fabrica 3    c31        c32

#Custo de transporte da fabrica i pro cliente j
cij = [[162,247], 
       [117,193],
       [131,185]]

capacidades = [1000,1500,1200]
demandas = [2300,1400]

m = len(capacidades)
n = len(demandas)

##-------------------------DECLARACAO DO MODELO E SEUS PARAMETROS--------------------##
#Modelo
modelo = pyEnv.ConcreteModel()
#Indice para as fabricas
modelo.I = pyEnv.RangeSet(m)
#Indice para os clientes                
modelo.J = pyEnv.RangeSet(n)

#Variaveis de decisao xij
modelo.x=pyEnv.Var(modelo.I,modelo.J, within=pyEnv.NonNegativeReals)

#Custo de transporte da fabrica i pro cliente j
modelo.c = pyEnv.Param(modelo.I, modelo.J,initialize=lambda modelo, i, j: cij[i-1][j-1])
#Capacidade de cada fabrica
modelo.b = pyEnv.Param(modelo.I, initialize = lambda modelo,i: capacidades[i-1])
#Demanda de cada cliente
modelo.d = pyEnv.Param(modelo.J, initialize = lambda modelo,j: demandas[j-1])


##-------------------------DECLARACAO DA FUNCAO OBJETIVO E RESTRICOES--------------------##

def func_objetivo(modelo):
    return sum(modelo.x[i,j] * modelo.c[i,j] for i in modelo.I for j in modelo.J)

modelo.objetivo = pyEnv.Objective(rule=func_objetivo,sense=pyEnv.minimize)


##------------------------------------------------------##
#Cada fabrica nao exceder sua capacidade

def rule_rest1(modelo,i):
    return sum(modelo.x[i,j] for j in modelo.J) <= modelo.b[i]

modelo.rest1 = pyEnv.Constraint(modelo.I,rule=rule_rest1)


##------------------------------------------------------##
#Cada cliente ter sua demanda atendida

def rule_rest2(modelo,j):
    return sum(modelo.x[i,j] for i in modelo.I) >= modelo.d[j]

modelo.rest2 = pyEnv.Constraint(modelo.J,rule=rule_rest2)

##-------------------------------RESOLUCAO DO MODELO-----------------------------------##
solver = pyEnv.SolverFactory('cplex',executable=path)
resultado = solver.solve(modelo,tee = True)
print('\n-------------------------\n')
#modelo.pprint()
modelo.objetivo()
print(resultado)

##-------------------------PRINT DAS VARIAVEIS DE DECISAO ESCOLHIDAS--------------------##
##(cliente,facilidade)
lista = list(modelo.x.keys())
for i in lista:
    print(i,'--', modelo.x[i]())
