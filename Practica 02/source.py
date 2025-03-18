import pygame
import pandas as pd
import math
from collections import Counter

def calcular_entropia(columna):
    """ Calcula la entropía de un conjunto de datos."""
    conteo = Counter(columna)
    total = len(columna)
    entropia = -sum((freq/total) * math.log2(freq/total) for freq in conteo.values())
    return entropia

def ganancia_de_informacion(df, atributo, objetivo):
    """ Calcula la ganancia de información de un atributo respecto al objetivo."""
    entropia_total = calcular_entropia(df[objetivo])
    valores_atributo = df[atributo].unique()
    entropia_condicional = sum(
        (len(df[df[atributo] == valor]) / len(df)) * calcular_entropia(df[df[atributo] == valor][objetivo])
        for valor in valores_atributo
    )
    return entropia_total - entropia_condicional

def id3(df, atributos, objetivo, profundidad=2):
    """ Implementa el algoritmo ID3 con un límite de profundidad."""
    if len(df[objetivo].unique()) == 1:
        return df[objetivo].iloc[0]  # Si todos los valores son iguales, devolver ese valor
    
    if not atributos or profundidad == 0:
        return df[objetivo].mode()[0]  # Devolver la clase más frecuente
    
    mejor_atributo = max(atributos, key=lambda attr: ganancia_de_informacion(df, attr, objetivo))
    arbol = {mejor_atributo: {}}
    
    for valor in df[mejor_atributo].unique():
        subconjunto = df[df[mejor_atributo] == valor]
        nuevos_atributos = [attr for attr in atributos if attr != mejor_atributo]
        arbol[mejor_atributo][valor] = id3(subconjunto, nuevos_atributos, objetivo, profundidad-1)
    
    return arbol

def draw_tree(screen, tree, x, y, level=0, parent_x=None, parent_y=None, width=800):
    """ Dibuja el árbol en la pantalla con etiquetas en los bordes y nodos correctamente centrados."""
    font = pygame.font.Font(None, 36)
    spacing_y = 100
    node_radius = 20
    if isinstance(tree, str):  # Nodo hoja
        pygame.draw.circle(screen, (0, 0, 0), (x, y), node_radius, 2)
        text_surface = font.render(tree, True, (0, 0, 0))
        screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))
        if parent_x is not None:
            pygame.draw.line(screen, (0, 0, 0), (parent_x, parent_y + node_radius), (x, y - node_radius), 2)
    elif isinstance(tree, dict):
        key = list(tree.keys())[0]
        pygame.draw.circle(screen, (0, 0, 0), (x, y), node_radius, 2)
        text_surface = font.render(key, True, (0, 0, 0))
        screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))
        if parent_x is not None:
            pygame.draw.line(screen, (0, 0, 0), (parent_x, parent_y + node_radius), (x, y - node_radius), 2)
        
        subtree = tree[key]
        num_children = len(subtree)
        spacing_x = width // (num_children + 1)
        
        for i, (subkey, subsubtree) in enumerate(subtree.items()):
            child_x = x - (num_children // 2 - i) * spacing_x
            child_y = y + spacing_y
            draw_tree(screen, subsubtree, child_x, child_y, level+1, x, y + node_radius, width // 2)
            # Draw edge label
            edge_label_surface = font.render(subkey, True, (0, 0, 0))
            edge_label_x = (x + child_x) // 2
            edge_label_y = (y + child_y) // 2 - 10
            screen.blit(edge_label_surface, (edge_label_x - edge_label_surface.get_width() // 2, edge_label_y))

def print_tree(tree, indent=''):
    """ Imprime el árbol de decisión en la terminal."""
    if isinstance(tree, dict):
        for key, subtree in tree.items():
            print(f"{indent}{key}")
            if isinstance(subtree, dict):
                for subkey, subsubtree in subtree.items():
                    print(f"{indent}  {subkey}:")
                    print_tree(subsubtree, indent + '    ')
            else:
                print(f"{indent}  -> {subtree}")
    else:
        print(f"{indent}{tree}")

# Datos de la práctica
atributos = ["TiempoExterior", "Temperatura", "Humedad", "Viento", "Jugar"]
datos = [
    ["soleado", "caluroso", "alta", "falso", "no"],
    ["soleado", "caluroso", "alta", "verdad", "no"],
    ["nublado", "caluroso", "alta", "falso", "si"],
    ["lluvioso", "templado", "alta", "falso", "si"],
    ["lluvioso", "frio", "normal", "falso", "si"],
    ["lluvioso", "frio", "normal", "verdad", "no"],
    ["nublado", "frio", "normal", "verdad", "si"],
    ["soleado", "templado", "alta", "falso", "no"],
    ["soleado", "frio", "normal", "falso", "si"],
    ["lluvioso", "templado", "normal", "falso", "si"],
    ["soleado", "templado", "normal", "verdad", "si"],
    ["nublado", "templado", "alta", "verdad", "si"],
    ["nublado", "caluroso", "normal", "falso", "si"],
    ["lluvioso", "templado", "alta", "verdad", "no"]
]

df = pd.DataFrame(datos, columns=atributos)

# Generar el árbol de decisión con una profundidad máxima de 2
arbol_decision = id3(df, atributos[:-1], "Jugar", profundidad=2)

# Imprimir el árbol de decisión en la terminal
print("Árbol de Decisión:")
print_tree(arbol_decision)

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Árbol de Decisión ID3")
screen.fill((255, 255, 255))

draw_tree(screen, arbol_decision, 500, 50)  # Centrar en la pantalla
pygame.display.flip()

# Bucle principal de pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()