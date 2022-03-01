import csv

# PRIMER PROGRAMA CARGA LA TABLA DE LAS ESTACIONES
# CARGA ESTACIONES
estacion = []
estacion.append("vacio") #COLOCA EL ELEMENTO "vacio" EN EL ÍNDICE CERO
with open("estaciones.csv",encoding="utf8", newline='') as File:  #ABRE EL ARCHIVO
  archivo = csv.reader(File) #ESTO HACE QUE INTERPRETE EL ARCHIVO COMO CSV
  for registro in archivo: #TOMA UN registro DEL CSV CADA VEZ QUE ITERA
      # CONSEJO COMENTARIOS EN MAYÚSCULAS, DATO Y TIPO DE DATO EN minúsculas

      #CONVIERTE LA LISTA DE TIPO string EN int
      listaVecinos = []
      vecinos = registro[5].split(",")
      for unVecino in vecinos:
            listaVecinos.append(int(unVecino))
      print("LISTA "+str(listaVecinos))

      #SE GENERA UNA tupla PARA ALMACENAR LOS DATOS Y DESPUES PASARLOS A ESTACION
      tupla = (int(registro[0]),registro[1],registro[2],float(registro[3]),float(registro[4]),listaVecinos)
      estacion.append(tupla)

        #IMPRIME LOS DATOS
      print("Reg: "+str(registro[0]))
      print("Estación: "+registro[1])
      print("Línea: "+registro[2])
      print("Lat: "+str(registro[3]))
      print("Lon: "+str(registro[4]))
      print("Vecinos: "+registro[5])
      print()
#PIDE LOS DATOS PARA ESTACION FINAL E INICIAL
estacionIni = int(input('Escribe la estación inicial: '))
estacionFin = int(input('Escribe la estación final: '))

cola = []  # CREA LA COLA VACÍA
cola.append(estacionIni)
haySolucion = False
while len(cola) > 0: # MIENTRAS LA COLA TENGA ELEMENTOS
    nodo = cola.pop(0)    # RETIRA EL ELEMENTO DEL INICIO DE LA COLA
    if nodo == estacionFin:
         haySolucion = True
         break
    vecinos = estacion[nodo][5] #VA A LA LISTA DE LOS VECINOS AL REGISTRO 5 QUE ES LA LISTA DE VECINOS
    print(vecinos)
    #COMO NO CHECA SI YA UTILIZAMOS LA ESTACION PASADA PUEDE QUE SE HAGA UN LOOP INFINITO
    for vecino in vecinos:
         cola.append( int(vecino) ) # ADICIONA CADA VECINO EN LA COLA
if haySolucion == True:
    print("HAY SOLUCION")
else:
    print("no hay solución")
