#Universidad del Valle de Guatemala
#Algoritmos y Estructuras de Datos
#Ing. Douglas Barrios
#@author: Julián Divas, Arodi Chávez, Ronald Catún
#Creación: 19/02/2025
#última modificación: 19/02/2025
#File Name: Simulacion.py
#Descripción: Simulacion DES de un sistema operativo utilizando la clase Resources y Container de SimPy
import simpy
import random

#Se definen la cantidad de procesos a trabajar e inicializan variables a utilizar
procesos = 25
capacidadram = 100
cantidadcpu = 1

#Se crea la función proceso para la simulación de procesos dentro de un sistema operativo
#Esta función utiliza el nombre del proceso, la cantidad de memoria a usar, la cantidad de instrucciones del proceso
#la ram disponible y el CPU el cual puede atender un proceso a la vez
def proceso(env, nombre, memoria, instrucciones, ram, cpu):
    print(f"{env.now}: Proceso {nombre} se encuentra en NEW, pide {memoria} de RAM")
    yield ram.get(memoria)
    print(f"{env.now}: Proceso {nombre} consiguio memoria y pasa a READY")
    while instrucciones > 0:
        with cpu.request() as req:  
            yield req
            print(f"{env.now}: {nombre} ha pasado a RUNNING")
            ejecucion = min(3, instrucciones)
            instrucciones -= ejecucion
            yield env.timeout(1)
            print(f"{env.now}: Proceso {nombre} ejecutó {ejecucion} instrucciones. Faltan {instrucciones}")

            if instrucciones == 0:
                print(f"{env.now}: Proceso {nombre} ha terminado y pasa a TERMINATED")
                yield ram.put(memoria)
                return

            probabilidad = random.randint(1, 2)
            if probabilidad == 1:
                print(f"{env.now}: Proceso {nombre} entra en WAITING (I/O)")
                yield env.timeout(random.randint(1, 3))
                print(f"{env.now}: Proceso {nombre} ha terminado I/O y vuelve a READY")

    yield ram.put(memoria)
    print(f"{env.now}: Proceso {nombre} ha terminado")

#Se crea la función generar procesos para definir la cantidad de procesos a procesar y  la cantidad de memoria e instrucciones que requieren
def generar_procesos(env, cantidad, ram, cpu):
    for i in range(cantidad):
        tiempo_llegada = random.expovariate(1.0 / 10)
        yield env.timeout(tiempo_llegada)
        memoria_requerida = random.randint(1, 10)  
        instrucciones = random.randint(1, 10)  
        env.process(proceso(env, f"P{i}", memoria_requerida, instrucciones, ram, cpu))
        
#Utilización de la semilla para generar siempre la misma secuencia
random.seed(0)
#Creación del environtment y de los containers y resources a simular, el cpu y la ram
env = simpy.Environment()
ram = simpy.Container(env, init=capacidadram, capacity=capacidadram)
cpu = simpy.Resource(env, capacity=cantidadcpu)
#Se simulan los procesos
env.process(generar_procesos(env, procesos, ram, cpu))
env.run()