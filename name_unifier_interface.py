import streamlit as st

from NameUnifier import NameUnifier
from calculador_similitud import calculador
import pandas as pd


# Función principal para Streamlit
def main():
    st.title("Unificador de Nombres")

    # Instancia de NameUnifier
    unificador = NameUnifier()

    # Cargar el archivo CSV
    uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

    # Barra lateral para configuración de metodos disponibles
    st.sidebar.title("Configuración")
    umbral_similitud = st.sidebar.slider("Umbral de Similitud", 0, 100, 80, 1)
    metodos = st.sidebar.multiselect("Elige el método para calcular el porcentaje de similitud:",
                                     list(calculador.keys()))
    if uploaded_file:
        # Vista previa del CSV
        st.write("Vista previa del CSV:")
        st.dataframe(unificador.cargar_csv(uploaded_file))

        # Establecer umbral de similitud en el unificador
        unificador.set_umbral_similitud(umbral_similitud)

        if metodos:
            unificador.set_metodos(metodos)
            # Calcular porcentaje de similitud de a cuerdo a un nombre estandar
            df_porcentaje_similitud = unificador.procesar_nombres()
            # Mostrar el DataFrame
            st.write("Porcentajes de similitud")
            st.dataframe(pd.DataFrame(df_porcentaje_similitud))

            # Mostrar el DataFrame después de unificación
            st.write("Nombres Unificados")
            st.dataframe(unificador.unificar_nombres())


# Ejecutar la aplicación Streamlit
if __name__ == "__main__":
    main()
