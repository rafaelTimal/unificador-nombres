from calculador_similitud import *
import pandas as pd


# Clase para el unificador de nombres
def normalizar(nombre):
    return " ".join([word for word in nombre.strip().split()])

    # Verificar que los métodos seleccionados estén disponibles


def cacular_porcentajes_similitud(metodos, estandar, variante):
    max_nombre = None
    max_valor = float("-inf")

    for funcion in metodos:
        valor = calculador[funcion](estandar, variante)
        if valor > max_valor:
            max_nombre = funcion
            max_valor = valor

    return max_nombre, max_valor


class NameUnifier:
    def __init__(self):
        self.dataframe = None
        self.umbral_similitud = 90
        self.metodos = None

    # Cargar el archivo CSV
    def cargar_csv(self, uploaded_file):
        self.dataframe = pd.read_csv(uploaded_file)
        return self.dataframe  # Vista previa de las primeras filas

    # Establecer el umbral de similitud
    def set_umbral_similitud(self, umbral):
        self.umbral_similitud = umbral

    # Establecer el umbral de similitud
    def set_metodos(self, metodos):
        self.metodos = metodos

    # Unificar los nombres con el nombre estándar y el umbral de similitud
    def procesar_nombres(self):
        if self.dataframe is None:
            return None

        df_unificado = self.dataframe.copy()
        df_unificado['Mejor Nombre'] = None

        variantes = self.dataframe.columns[1:]

        # Recorrer Todas las filas
        for index, row in self.dataframe.iterrows():
            max_valor = float("-inf")
            # Recorrer todas las columnas
            for col_name in variantes:
                current_name = row[col_name]
                metodo, similitud = cacular_porcentajes_similitud(self.metodos, self.dataframe.at[index, 'Nombre'],
                                                                  normalizar(current_name))
                if similitud > max_valor:
                    max_valor = similitud
                    df_unificado.at[index, 'Mejor Nombre'] = f"{current_name} ({similitud :.2f}%)"
                new_column = col_name + ' %'
                if new_column not in df_unificado.columns:
                    df_unificado.insert(df_unificado.columns.get_loc(col_name) + 1,
                                        new_column,
                                        f"{metodo} ({similitud :.2f}%)")
                else:
                    df_unificado.at[index, new_column] = f"{metodo} ({similitud :.2f}%)"

        return df_unificado

    # Unificar los nombres con el umbral de similitud
    def unificar_nombres(self):
        nombres_unificados = {}

        for index, row in self.dataframe.iterrows():
            nombre_base = normalizar(row['Nombre'])
            variantes = {columna: row[columna] for columna in self.dataframe.columns[1:]}

            if nombre_base not in nombres_unificados:
                nombres_unificados[nombre_base] = []

            # Buscar si alguna variante coincide con el nombre base
            encontrado = False
            for columna, variante in variantes.items():
                variante_normalizada = normalizar(variante)
                metodo, similitud = cacular_porcentajes_similitud(self.metodos, nombre_base,
                                                                  variante_normalizada)

                if similitud >= self.umbral_similitud:
                    nombres_unificados[nombre_base].append(variante)

            # Si no se encontró ninguna variante que supere el umbral, se agrega el nombre base
            if not nombres_unificados[nombre_base]:
                nombres_unificados[nombre_base].append(row['Nombre'])

        # Convertir el diccionario en un DataFrame
        df_resultados = pd.DataFrame.from_dict(nombres_unificados, orient='index').reset_index()
        df_resultados.columns = ['Nombre base'] + [f'Variante {i + 1}' for i in range(len(df_resultados.columns) - 1)]
        return df_resultados
