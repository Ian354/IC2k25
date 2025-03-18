import math
import pandas as pd

# Leer los archivos
def leer_archivos(atributos_file, ejemplos_file):
    with open(atributos_file, 'r') as f:
        atributos = f.read().splitlines()
    
    ejemplos = pd.read_csv(ejemplos_file, header=None, names=atributos + ['Jugar'])
    return atributos, ejemplos

# Calcular la entropía
def calcular_entropia(ejemplos):
    total = len(ejemplos)
    positivos = len(ejemplos[ejemplos['Jugar'] == 'si'])
    negativos = len(ejemplos[ejemplos['Jugar'] == 'no'])
    
    if positivos == 0 or negativos == 0:
        return 0
    
    p_pos = positivos / total
    p_neg = negativos / total
    
    return -p_pos * math.log2(p_pos) - p_neg * math.log2(p_neg)

# Calcular la ganancia de información
def ganancia_informacion(ejemplos, atributo):
    total_entropia = calcular_entropia(ejemplos)
    valores = ejemplos[atributo].unique()
    
    suma_entropias = 0
    for valor in valores:
        subset = ejemplos[ejemplos[atributo] == valor]
        entropia_subset = calcular_entropia(subset)
        suma_entropias += (len(subset) / len(ejemplos)) * entropia_subset
    
    return total_entropia - suma_entropias

# Seleccionar el mejor atributo
def seleccionar_mejor_atributo(ejemplos, atributos):
    mejor_atributo = None
    mejor_ganancia = -1
    
    for atributo in atributos:
        ganancia = ganancia_informacion(ejemplos, atributo)
        if ganancia > mejor_ganancia:
            mejor_ganancia = ganancia
            mejor_atributo = atributo
    
    return mejor_atributo

# Implementar el algoritmo ID3
def id3(ejemplos, atributos, nivel=1, max_nivel=2):
    if len(atributos) == 0 or nivel > max_nivel:
        return None
    
    mejor_atributo = seleccionar_mejor_atributo(ejemplos, atributos)
    if mejor_atributo is None:
        return None
    
    arbol = {mejor_atributo: {}}
    
    for valor in ejemplos[mejor_atributo].unique():
        subset = ejemplos[ejemplos[mejor_atributo] == valor]
        if len(subset['Jugar'].unique()) == 1:
            arbol[mejor_atributo][valor] = subset['Jugar'].iloc[0]
        else:
            nuevos_atributos = [a for a in atributos if a != mejor_atributo]
            arbol[mejor_atributo][valor] = id3(subset, nuevos_atributos, nivel + 1, max_nivel)
    
    return arbol

# Leer los datos
atributos, ejemplos = leer_archivos('AtributosJuego.txt', 'Juego.txt')

# Generar el árbol de decisión
arbol_decision = id3(ejemplos, atributos)
print(arbol_decision)