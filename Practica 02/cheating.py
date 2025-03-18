import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from dtreeviz.trees import dtreeviz

# Leer los archivos
def leer_archivos(atributos_file, ejemplos_file):
    with open(atributos_file, 'r') as f:
        atributos = f.read().splitlines()

    ejemplos = pd.read_csv(ejemplos_file, header=None, names=atributos + ['Jugar'])
    return atributos, ejemplos

# Leer los datos
atributos, ejemplos = leer_archivos('AtributosJuego.txt', 'Juego.txt')

# Preparar los datos
X = ejemplos[atributos]
y = ejemplos['Jugar']

# Codificar las variables categóricas
X_encoded = pd.get_dummies(X)
y_encoded = y.map({'si': 1, 'no': 0})

# Entrenar el modelo
clf = DecisionTreeClassifier(max_depth=2)
clf.fit(X_encoded, y_encoded)

# Visualizar el árbol
viz = dtreeviz(clf, X_encoded, y_encoded,
               target_name="Jugar",
               feature_names=X_encoded.columns,
               class_names=["no", "si"])

# Mostrar el árbol
viz.view()