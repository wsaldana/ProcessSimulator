'''
UNIVERSIDAD DEL VALLE DE GUATEMALA
Algoritmos y Estructuras de Datos
Seccion 20
05 de marzo del 2020

Walter Saldaña #19897

Simulacion discreta basada en eventos de la ejecucion de un proceso en un sistema operativo de tiempo compartido
'''
#Importacion de librerias
import simpy as sp
import random as r
import matplotlib.pyplot as plt

#Declaracion de valores constantes
INTERVALO = 3
CAPACIDAD_RAM = 100 #MB
VELOCIDAD_CPU = 1 #Instrucciones por segundo
NUMERO_PROCESADORES = 1
NUMERO_PROCESOS = 25

tiempo = 0
muestra = []
row = []

#Simulacion de un proceso
def proceso(env, numero, ram, cpu, tiempoCreacion, nInstrucciones, cantidadRam):
    inicio = env.now
    #New
    print('New ', numero, ' - ', env.now)
    yield env.timeout(tiempoCreacion)
    ram.get(cantidadRam)
    
    #ready
    instruccion = 0
    print('Ready ', numero, ' instr# ',instruccion,' - ',env.now)
    while instruccion < nInstrucciones:
        with cpu.request() as rq:
            yield rq
            
            #running
            print('Running ', numero, ' instr# ',instruccion,' - ',env.now)
            yield env.timeout(nInstrucciones/VELOCIDAD_CPU)
        
        siguiente = r.randint(1,2)
        if(siguiente == 1):
            print('Running ', numero, ' Waiting instr# ',instruccion,' - ',env.now)
            yield env.timeout(r.randint(1,3))
        instruccion += 1
        
    final = env.now
    dt = final - inicio
    print('Running ', numero, ' Terminated - en ',dt)
    global tiempo
    tiempo += dt
    global muestra
    muestra.append(dt)
    global row
    row.append(nInstrucciones)
    ram.put(cantidadRam) #Se devuelve la ram cuando se deja de utilizar
        

#Creacion de ambiente
env = sp.Environment()
cpu = sp.Resource(env, NUMERO_PROCESADORES)
ram = sp.Container(env, init=CAPACIDAD_RAM, capacity=CAPACIDAD_RAM)

#Generar procesos
for i in range(NUMERO_PROCESOS):
    tiempoCreacion = r.expovariate(1.0/INTERVALO)
    nInstrucciones = r.randint(1,10)
    cantidadRam = r.randint(1,10)
    env.process(proceso(env, i, ram, cpu, tiempoCreacion, nInstrucciones, cantidadRam))

env.run()

#Calculos estadisticos
x = tiempo/NUMERO_PROCESOS
print('Timepo total: ',tiempo)
print('Media: ',x)
suma = 0
for i in muestra:
    suma += (i - x)*(i - x)
desv = (suma/NUMERO_PROCESOS)**0.5
print('Desviacion estandar: ', desv)

#Graficar
plt.plot(row, muestra) # crear la grafica
plt.title("Tiempo medio por unidad de procesos") #Titulo de la grafica
plt.xlabel("Numero de procesos") #nombre del eje X
plt.ylabel("Tiempo") #Nombre del eje Y
plt.show() #Mostrar gráfica




