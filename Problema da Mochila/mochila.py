#Problema da Mochila - Knapsack Problem
import pyomo.environ as pyEnv

path = "/home/tito/cplex/bin/x86-64_linux/cplex"

##-------------------------LEITURA DA INSTANCIA------------------------------------##

filePesoMaximo = open('p08_c.txt')
pesoMaximo  = filePesoMaximo.readline().split('\n')[0]
pesoMaximo = int(pesoMaximo)

filePesos = open('p08_w.txt')
pesos  = filePesos.readlines()
pesos = pesos[0].split()
pesos = [int(i) for i in pesos]


fileLucros = open('p08_p.txt')
lucros  = fileLucros.readlines()
lucros = lucros[0].split()
lucros = [int(i) for i in lucros]

m = len(pesos)

#-------------------------DECLARACAO DO MODELO E SEUS PARAMETROS--------------------##
#Modelo
modelo = pyEnv.ConcreteModel()                     
#Indice para os pesos e precos
modelo.I = pyEnv.RangeSet(m)

#Variaveis de decisao xi
modelo.x = pyEnv.Var(modelo.I,within=pyEnv.Binary)     

#Preco de cada produto
modelo.c = pyEnv.Param(modelo.I, initialize = lambda modelo,i: lucros[i-1])
#Peso de cada produto
modelo.p = pyEnv.Param(modelo.I, initialize = lambda modelo,i: pesos[i-1])

##-------------------------DECLARACAO DA FUNCAO OBJETIVO E RESTRICAO--------------------##
#Funcao objetivo do problema
modelo.objetivo = pyEnv.Objective(expr = sum(modelo.c[i]*modelo.x[i] for i in modelo.I), sense=pyEnv.maximize)

#Restricao do problema
modelo.restricao = pyEnv.Constraint(expr = sum(modelo.p[i] * modelo.x[i] for i in modelo.I) <= pesoMaximo)


##-------------------------------RESOLUCAO DO MODELO-----------------------------------##
solver = pyEnv.SolverFactory('cplex',executable=path)
resultado = solver.solve(modelo, tee= True)
print('\n-------------------------\n')
modelo.pprint()
modelo.objetivo()
print(resultado)

##-------------------------PRINT DAS VARIAVEIS DE DECISAO--------------------##
lista = list(modelo.x.keys())
for i in lista:
    print(i,'--', modelo.x[i]())