from rapidfuzz import fuzz
import sys


def verificar_metodos(metodos):
    for metodo in metodos:
        if metodo not in calculador:
            print(f"El método {metodo} no está disponible.")
            sys.exit(1)


# Calcula la similitud después de ordenar los tokens de las cadenas.
def token_sort_ratio(estandar, variante):
    # Usar FuzzyWuzzy para obtener el porcentaje de similitud
    return fuzz.token_sort_ratio(estandar, variante)


# compara las dos cadenas de texto carácter por carácter
# y determina cuántos caracteres coinciden entre ellas.
def ratio(estandar, variante):
    # Usar FuzzyWuzzy para obtener el porcentaje de similitud
    return fuzz.ratio(estandar, variante)


def levenshtein(estandar, variante):
    # Función para calcular la distancia de Levenshtein entre dos cadenas
    if len(estandar) > len(variante):
        estandar, variante = variante, estandar

    distances = range(len(estandar) + 1)
    for index2, char2 in enumerate(variante):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(estandar):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances
    return (distances[-1] / max(len(estandar), len(variante))) * 100


def jaccard(estandar, variante):
    # Función para calcular el índice de Jaccard entre dos cadenas
    set1 = set(estandar)
    set2 = set(variante)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


calculador = {
    "Token Sort Ratio": token_sort_ratio,
    "Levenshtein": levenshtein,
    "Jaccard": jaccard,
    "Ratcliff/Obershelp": ratio
}
