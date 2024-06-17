from rapidfuzz import fuzz
import sys
import math


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
    result = intersection / union if union != 0 else 0
    return result * 100


# Distancia de Jaro-Winkler: Mide la similitud entre dos cadenas teniendo en cuenta
#    la frecuencia de caracteres coincidentes y la proximidad de las coincidencias.
#    Es útil para comparar cadenas de texto cortas, como nombres.

def jaro_winkler_similarity(str1, str2):
    # Longitud de las cadenas
    len1 = len(str1)
    len2 = len(str2)

    # Longitud máxima para la ventana de coincidencia
    max_len = max(len1, len2)
    match_range = (max_len // 2) - 1

    # Contadores para las coincidencias y transposiciones
    matches = 0
    transpositions = 0

    # Conjunto para almacenar caracteres ya emparejados
    matched_indices_str1 = set()
    matched_indices_str2 = set()

    # Encontrar coincidencias
    for i in range(len1):
        start = max(0, i - match_range)
        end = min(i + match_range + 1, len2)
        for j in range(start, end):
            if str1[i] == str2[j] and j not in matched_indices_str2:
                matches += 1
                matched_indices_str1.add(i)
                matched_indices_str2.add(j)
                break

    # Encontrar transposiciones
    for i, j in zip(matched_indices_str1, matched_indices_str2):
        if str1[i] != str2[j]:
            transpositions += 1

    # Calcular similitud de Jaro
    jaro_similarity = 0.0
    if matches > 0:
        jaro_similarity = ((matches / len1) + (matches / len2) + ((matches - transpositions) / matches)) / 3

    # Factor de ajuste de Winkler
    prefix_len = 0
    for i in range(min(4, min(len1, len2))):
        if str1[i] == str2[i]:
            prefix_len += 1
        else:
            break
    result = jaro_similarity + (prefix_len * 0.1 * (1 - jaro_similarity))

    return result * 100  # Convertir a porcentaje


def vectorize_string(text):
    # Crear un vector de frecuencia de caracteres Unicode
    vector = [0] * 65536  # Asignar 65536 elementos para todos los caracteres Unicode

    # Contar la frecuencia de cada caracter en el texto
    for char in text:
        vector[ord(char)] += 1

    return vector


# Índice de Similaridad de Coseno
# Es una medida de similitud entre dos vectores en un espacio vectorial.
# Cada vector representa la frecuencia de aparición de palabras en una cadena de texto.
def cosine_similarity(str1, str2):
    # Vectorizar las cadenas de texto
    vec1 = vectorize_string(str1)
    vec2 = vectorize_string(str2)

    # Calcular el producto punto de los vectores
    dot_product = sum(vec1[i] * vec2[i] for i in range(len(vec1)))

    # Calcular las magnitudes de los vectores
    magnitude1 = math.sqrt(sum(vec1[i] ** 2 for i in range(len(vec1))))
    magnitude2 = math.sqrt(sum(vec2[i] ** 2 for i in range(len(vec2))))

    # Evitar división por cero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    # Calcular la similitud de coseno
    cosine_sim = dot_product / (magnitude1 * magnitude2)

    return cosine_sim * 100


# Algoritmo de Smith-Waterman: Este es un algoritmo de programación dinámica
# que encuentra la mejor alineación local entre dos cadenas,
# lo que permite identificar regiones similares incluso si no coinciden exactamente.

def smith_waterman(s1, s2):
    # Definir la matriz de puntuación y la matriz de dirección
    m = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    directions = [[None] * (len(s2) + 1) for _ in range(len(s1) + 1)]

    # Calcular las puntuaciones de coincidencia
    match = 2
    mismatch = -1
    gap_penalty = -1

    max_score = 0
    max_i = 0
    max_j = 0

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                score = match
            else:
                score = mismatch

            diagonal = m[i - 1][j - 1] + score
            up = m[i - 1][j] + gap_penalty
            left = m[i][j - 1] + gap_penalty

            m[i][j] = max(0, diagonal, up, left)

            if m[i][j] > max_score:
                max_score = m[i][j]
                max_i = i
                max_j = j

            if m[i][j] == diagonal:
                directions[i][j] = 'diagonal'
            elif m[i][j] == up:
                directions[i][j] = 'up'
            elif m[i][j] == left:
                directions[i][j] = 'left'

    # Retroceder desde la celda con la puntuación máxima para reconstruir la subcadena óptima
    alignment = []
    i, j = max_i, max_j
    while i > 0 and j > 0 and m[i][j] > 0:
        if directions[i][j] == 'diagonal':
            alignment.append(s1[i - 1])
            i -= 1
            j -= 1
        elif directions[i][j] == 'up':
            alignment.append(s1[i - 1])
            i -= 1
        elif directions[i][j] == 'left':
            alignment.append(s2[j - 1])
            j -= 1

    # Calcular el porcentaje de similitud
    max_possible_score = min(len(s1), len(s2)) * match
    similarity = (max_score / max_possible_score) * 100 if max_possible_score > 0 else 0

    # Devolver la alineación y el porcentaje de similitud
    return similarity


calculador = {
    "Token Sort Ratio": token_sort_ratio,
    "Levenshtein": levenshtein,
    "Jaccard": jaccard,
    "Ratcliff/Obershelp": ratio,
    "Jaro-Winkler": jaro_winkler_similarity,
    "Cosine": cosine_similarity,
    "Smith Waterman": smith_waterman
}
