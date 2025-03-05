import heapq
import math
import matplotlib.pyplot as plt
import numpy as np

def leer_matriz_fichero(nombre_fichero):
    matriz = []
    puntos = {}

    conversion = {
        'O': 0,  # Camino libre
        'X': -1,  # Obstáculo
        'P': 0.5,  # Celda peligrosa
        '1': 1,  # Punto 1
        '2': 2,  # Punto 2
        '3': 3,  # Punto 3
        '4': 4,  # Punto 4
        '5': 5,  # Punto 5
        '6': 6,  # Punto 6
    }

    with open(nombre_fichero, 'r') as fichero:
        for i, linea in enumerate(fichero):
            fila = []
            for j, caracter in enumerate(linea.strip().split()):
                if caracter in conversion:
                    valor = conversion[caracter]
                    fila.append(valor)
                    if valor > 0:
                        puntos[valor] = (i, j)
                else:
                    raise ValueError(f"Caracter no reconocido: {caracter}")
            matriz.append(fila)

    return matriz, puntos

def distancia_euclidiana(nodo1, nodo2):
    return math.sqrt((nodo1[0] - nodo2[0])**2 + (nodo1[1] - nodo2[1])**2)

def astar(matriz, inicio, final):
    filas, columnas = len(matriz), len(matriz[0])
    lista_abierta = []
    lista_cerrada = set()

    # Colocar los obstáculos directamente en la lista cerrada
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == -1:
                lista_cerrada.add((i, j))

    # Inicializar el nodo de inicio
    g_coste = {inicio: 0}
    f_coste = {inicio: distancia_euclidiana(inicio, final)}
    padres = {inicio: None}

    # Agregar el nodo inicial a la lista abierta
    heapq.heappush(lista_abierta, (f_coste[inicio], inicio))

    # Direcciones de movimiento: vertical, horizontal y diagonal
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while lista_abierta:
        _, nodo_actual = heapq.heappop(lista_abierta)

        # Si hemos llegado al objetivo, reconstruir el camino
        if nodo_actual == final:
            return reconstruir_camino(padres, nodo_actual)

        lista_cerrada.add(nodo_actual)

        # Explorar vecinos
        for direccion in direcciones:
            vecino = (nodo_actual[0] + direccion[0], nodo_actual[1] + direccion[1])

            # Verificar que el vecino esté dentro de los límites y no sea un obstáculo o ya esté cerrado
            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas and vecino not in lista_cerrada:
                riesgo = 1 if matriz[vecino[0]][vecino[1]] == 0 else matriz[vecino[0]][vecino[1]]
                g_nuevo = g_coste[nodo_actual] + distancia_euclidiana(nodo_actual, vecino) * riesgo

                # Si no está en lista_abierta o encontramos un camino más corto, actualizamos
                if vecino not in g_coste or g_nuevo < g_coste[vecino]:
                    g_coste[vecino] = g_nuevo
                    f_coste[vecino] = g_nuevo + distancia_euclidiana(vecino, final)
                    padres[vecino] = nodo_actual
                    heapq.heappush(lista_abierta, (f_coste[vecino], vecino))

    # No se encontró un camino
    return None

def reconstruir_camino(padres, nodo):
    camino = []
    while nodo is not None:
        camino.append(nodo)
        nodo = padres[nodo]
    camino.reverse()
    return camino

def mostrar_matriz(matriz, camino=None):
    filas, columnas = len(matriz), len(matriz[0])
    imagen = np.zeros((filas, columnas, 3))  # Imagen en RGB

    colores = {
        0: (1, 1, 1),  # Blanco para caminos libres
        -1: (0, 0, 0), # Negro para obstáculos
        0.5: (1, 1, 0), # Amarillo para celdas peligrosas
        1: (0, 1, 0),  # Verde para puntos
        2: (0, 1, 0),  # Verde para puntos
        3: (0, 1, 0),  # Verde para puntos
        4: (0, 1, 0),  # Verde para puntos
        5: (0, 1, 0),  # Verde para puntos
        6: (1, 0, 0),  # Rojo para el final
    }

    # Pintar la matriz
    for i in range(filas):
        for j in range(columnas):
            imagen[i, j] = colores.get(matriz[i][j], (1, 1, 1))

    # Si hay un camino, dibujarlo en azul
    if camino:
        for nodo in camino:
            if nodo not in puntos.values():  # No sobrescribir puntos
                imagen[nodo[0], nodo[1]] = (0, 0, 1)  # Azul para el camino

    # Mostrar la imagen con Matplotlib
    plt.figure(figsize=(5, 5))
    plt.imshow(imagen)
    plt.grid(visible=True, color="gray", linewidth=0.5)
    plt.xticks([])
    plt.yticks([])
    plt.title("Mapa con el camino encontrado")
    plt.show()

# Prueba del algoritmo
nombre_fichero = "matriz3.txt" 
matriz, puntos = leer_matriz_fichero(nombre_fichero)

print("Matriz cargada:")
for fila in matriz:
    print(fila)

print(f"Puntos: {puntos}")

# Ordenar los puntos por su valor
puntos_ordenados = sorted(puntos.items())

camino_total = []
for i in range(len(puntos_ordenados) - 1):
    inicio = puntos_ordenados[i][1]
    final = puntos_ordenados[i + 1][1]
    camino = astar(matriz, inicio, final)
    if camino:
        camino_total.extend(camino[:-1])  # Evitar duplicar el nodo final
    else:
        print(f"No se encontró un camino de {inicio} a {final}")
        break

# Agregar el último nodo final
camino_total.append(puntos_ordenados[-1][1])

if camino_total:
    print("Camino encontrado:")
    for paso in camino_total:
        print(paso)
else:
    print("No se encontró un camino.")

# Mostrar la matriz con el camino encontrado
mostrar_matriz(matriz, camino_total)
