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
procesos = 5
capacidadram = 100
cantidadcpu = 1

#Se crea la función proceso para la simulación de procesos dentro de un sistema operativo
#Esta función utiliza en nombre del proceso, la cantidad de memoria a usar, la cantidad de instrucciones del proceso
#la ram disponible y el CPU el cual puede atender un proceso a la vez
def proceso(env, nombre, memoria, instrucciones, ram, cpu):
    #Se inicia el proceso en new, solicitando ram
    print(f"{env.now}: Proceso {nombre} en NEW, solicita {memoria} de RAM")
    #Espera para tener la memoria ram necesaria para funcionar
    yield ram.get(memoria)
    #Obtiene la memoria ram necesaria y pasa a READY
    print(f"{env.now}: Proceso {nombre} obtuvo memoria y pasa a READY")
    #Mientras hayan instrucciones
    while instrucciones > 0:
        #Se solicita utilizar el CPU
        with cpu.request() as req:  
            yield req
            #Media vez el CPU pueda hacer el proceso, este pasa al estado Running
            print(f"{env.now}: {nombre} ha pasado a RUNNING")
            #Se pueden ejecutar 3 instrucciones a la vez
            ejecucion = min(3, instrucciones)
            #El numero de instrucciones va disminuyendo conforme el CPU las trata
            instrucciones -= ejecucion
            #Realizar las instrucciones toma 1 unidad de tiempo
            yield env.timeout(1)
            #Se indica cuantas instrucciones se ejecutaron y las faltantes
            print(f"{env.now}: Proceso {nombre} ejecutó {ejecucion}. Faltan {instrucciones}")
    #Se libera la ram que estaba siendo utilizada

                # Verificar si el proceso ha terminado
            if instrucciones == 0:
                print(f"{env.now}: Proceso {nombre} ha terminado y pasa a TERMINATED")
                yield ram.put(memoria)  # Libera la RAM usada
                return

            # Verificar si el proceso entra en WAITING (I/O)
            probabilidad = random.randint(1, 21)
            if probabilidad == 1:
                print(f"{env.now}: Proceso {nombre} entra en WAITING (I/O)")
                yield env.timeout(random.randint(1, 3))  # Simula el tiempo de espera en I/O
                print(f"{env.now}: Proceso {nombre} ha terminado I/O y vuelve a READY")

    yield ram.put(memoria)
    #El proceso a sido terminado
    print(f"{env.now}: Proceso {nombre} ha terminado")

#Función para generar los procesos a simular
def generar_procesos(env, cantidad, ram, cpu):
    #En el rango de los procesos a generar
    for i in range(cantidad):
        #Se define el tiempo variable de llegada
        tiempo_llegada = random.expovariate(1.0 / 10)
        #Se esperan tales unidades de tiempo
        yield env.timeout(tiempo_llegada)
        #Se define cuanta memoria utilizará el proceso, entre 1 a 10 unidades de tiempo
        memoria_requerida = random.randint(1, 10)  
        #Se define la cantidad de instrucciones de cada proceso
        instrucciones = random.randint(1, 10)  
        #Se lleva a cabo el proceso definido en la funcoin anterior
        env.process(proceso(env, f"P{i}", memoria_requerida, instrucciones, ram, cpu))
#Utilización de la semilla para generar siempre la misma secuencia
random.seed(20)
#Creación del environtment y de los containers y resources a simular, el cpu y la ram
env = simpy.Environment()
ram = simpy.Container(env, init=capacidadram, capacity=capacidadram)
cpu = simpy.Resource(env, capacity=cantidadcpu)
#Se simulan los procesos
env.process(generar_procesos(env, procesos, ram, cpu))
env.run()