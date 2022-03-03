# PROGRAMA 2. VALIDA QUE NO SE REPITAN LAS ESTACIONES
import csv
from tokenize import PlainToken

# CARGA ESTACIONES
estacion = []  # INICIALIZA LA LISTA
estacion.append("vacio")  # COLOCA EL ELEMENTO EN EL INDICE CERO
with open("estaciones.csv", encoding = "utf8" ,newline='') as File:  # ABRE EL ARCHIVO
    archivo = csv.reader(File)  # INTERPRETA EL ARCHIVO COMO CSV
    for registro in archivo:  # TOMA UN REGISTRO DEL ARCHIVO CSV

        # CONVIERTE A TIPO int CADA UNO DE LOS VECINOS
        listaVecinos = []
        vecinos = registro[5].split(",")
        for unVecino in vecinos:
              listaVecinos.append(int(unVecino))

        # GENERA UNA TUPLA PARA GUARDARLA EN LA LISTA DE estacion      
        tupla = (int(registro[0]),registro[1],registro[2],float(registro[3]),float(registro[4]),listaVecinos)
       
        # AÑADE LA TUPLA EN LA LISTA estacion
        estacion.append(tupla)
        #print(str(tupla))     # DESPLIEGA LA TUPLA

# PIDE LA ESTACION INICIAL Y LA FINAL
estacionIni = int(input('Escribe la estación inicial: '))
estacionFin = int(input('Escribe la estación final: '))

# INICIA EL ALGORITMO DE BÚSQUEDA CIEGA (BUSQUEDA EN AMPLITUD)
cola = []  # CREA LA COLA VACÍA
utilizados = []  # LISTA DE NODOS UTILIZADOS
cola.append(estacionIni)
haySolucion = False
anterior = 0   # INICIALIZA EL NODO ANTERIOR CON CERO QUE NO EXISTE
visitados = []  # PAREJAS DE NODOS VISITADOS

while len(cola) > 0: # MIENTRAS LA COLA TENGA ELEMENTOS
    nodo = cola.pop(0)    # RETIRA EL ELEMENTO DEL INICIO DE LA COLA
   
    print("Utilizo: "+str(estacion[nodo][1])) # DESPLIEGA NOMBRE DE ESTACIÓN

    utilizados.append(int(nodo))  # AÑADE EL NODO A LOS UTILIZADOS PARA EVITAR LOOPS INFINITO

    visitados.append((anterior,nodo)) # GUARDA PARES (NODO anterior, nodo ACTUAL)
    anterior = nodo   # ACTUALIZA EL NODO anterior COMO EL nodo ACTUAL
   
    if nodo == estacionFin:
         haySolucion = True
         break

    vecinos = estacion[nodo][5]
    for vecino in vecinos:
         if not (vecino in utilizados):
             cola.append(vecino) # ADICIONA CADA VECINO EN LA COLA

# TERMINÓ LA BÚSQUEDA, AHORA OBTIENE LA RUTA (plan)            
if haySolucion == True:
    print("HAY SOLUCION")
    print(visitados) #POR EL MOMENTO IMPRIME LOS DATOS ERRONEOS YA QUE PASA POR PANTITLAN VARIAS VECES AL SER VECINOS
else:
    print("no hay solución")
#AHORA IMPRIMIMOS EL PLAN
print("Estacion de inicio: "+str(estacion[estacionIni][1]))
print("Estacion a la que se quiere llegar: "+str(estacion[estacionFin][1]))
#print(type (utilizados))
# EL plan SE EMPIEZA A IMPRIMIR
print("Estación || Línea")
for incremental in utilizados:
    plan=(estacion[incremental][1],estacion[incremental][2])
    print("De la estacion "+str(plan),end= " ")

#print(type (plan)) #IMPRIMIE EL tipo de dado DE PLAN (ES UNA TUPLA)
