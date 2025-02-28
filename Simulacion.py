#Universidad del Valle de Guatemala
#Algoritmos y Estructuras de Datos
#Ing. Douglas Barrios
#@author: Julián Divas, Arodi Chávez, Ronald Catún
#Creación: 25/02/2025
#última modificación: 28/02/2025
#File Name: Simulacion.py
#Descripción: Simulacion DES de un sistema operativo utilizando la clase Resources y Container de SimPy

import simpy
import random

#El proceso correspondiente solicita memoria para poderse llevar a cabo, espera la memoria según sea necesario
def solicitar_memoria(env, nombre, memoria, ram):
    print(f"{nombre} está en NEW, solicitando {memoria} de RAM")
    yield ram.get(memoria)
    print(f"{nombre} obtuvo memoria y está en READY")

#El proceso correspondiente solicita utilizar el resource CPU para poder ejecutar las instrucciones que este contiene
# Existen dos posibilidades, terminar el proceso por completo o entrar en el estado de Waiting para realizar operaciones I/O
def ejecutar_instrucciones(env, nombre, instrucciones, cpu):
    while instrucciones > 0:
        with cpu.request() as req:
            yield req
            print(f"{nombre} está en RUNNING")
            ejecutar = min(3, instrucciones)
            instrucciones -= ejecutar
            yield env.timeout(1)
            print(f"{nombre} ejecutó {ejecutar} instrucciones. Restantes: {instrucciones}")
            
            if instrucciones == 0:
                print(f"{nombre} ha finalizado y pasa a TERMINATED")
                return True
            
            if random.choice([True, False]):
                print(f"{nombre} entra en WAITING (I/O)")
                yield env.timeout(random.randint(1, 3))
                print(f"{nombre} terminó I/O y vuelve a READY")
    return False

#Una vez se termina el proceso, se libera la cantidad de memoria que estaba siendo solicitada
def liberar_memoria(env, nombre, memoria, ram):
    print(f"{nombre} libera {memoria} de RAM")
    yield ram.put(memoria)

#Para llevar a cabo el proceso, se solicita memoria, posteriormente se ejecutan las instrucciones del proceso y al terminar se libera la memoria
def proceso(env, nombre, memoria, instrucciones, ram, cpu):
    yield from solicitar_memoria(env, nombre, memoria, ram)
    finalizado = yield from ejecutar_instrucciones(env, nombre, instrucciones, cpu)
    if finalizado:
        yield from liberar_memoria(env, nombre, memoria, ram)

#Función que indica el tiempo de simulación utiilzado para realizar n procesos en total.
def tiempo_requerido(env, total_procesos):
    print(f"Se necesitaron {env.now} unidades de tiempo para completar {total_procesos} procesos")

#Se crean los procesos mediante un for y se llevan a cabo. Se toma en cuento el timepo de llegada con random.expovariate y 
#se generan la cantidad de instrucciones y memoria que usa cada proceso mediante randint.
def crear_procesos(env, total_procesos, ram, cpu):
    for i in range(total_procesos):
        yield env.timeout(random.expovariate(1.0 / 10))
        mem_necesaria = random.randint(1, 10)
        instrucciones = random.randint(1, 10)
        env.process(proceso(env, f"Proceso {i + 1}", mem_necesaria, instrucciones, ram, cpu))


# Configuración inicial
random.seed(0)
capacidad_ram = 100
cantidad_cpu = 1
procesos_totales = 10

# Creación del entorno de simulación
env = simpy.Environment()
ram = simpy.Container(env, init=capacidad_ram, capacity=capacidad_ram)
cpu = simpy.Resource(env, capacity=cantidad_cpu)

# Se realiza la simulación
env.process(crear_procesos(env, procesos_totales, ram, cpu))
env.run()
tiempo_requerido(env, procesos_totales)