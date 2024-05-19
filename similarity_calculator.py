import argparse
from NameUnifier import NameUnifier
from calculador_similitud import verificar_metodos


def main():
    # Configurar argparse para manejar los argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description='Calcular el porcentaje de similitud entre nombres.')
    parser.add_argument('csv_path', type=str, help='Ruta del archivo CSV')
    parser.add_argument('metodos', nargs='+',
                        help='Lista de métodos a probar. Ejemplo: ["Token Sort Ratio", "Levenshtein", "Jaccard"]')
    parser.add_argument('--umbral', type=float, default=0,
                        help='Umbral de porcentaje de similitud para filtrar los resultados (0-100)')

    args = parser.parse_args()

    unificador = NameUnifier()
    # Cargar el archivo CSV
    unificador.cargar_csv(args.csv_path)

    # Establecer umbral de similitud en el unificador
    unificador.set_umbral_similitud(args.umbral)
    metodos = args.metodos

    if metodos:
        verificar_metodos(metodos)
        unificador.set_metodos(metodos)
        # Calcular porcentaje de similitud de a cuerdo a un nombre estandar
        df_porcentaje_similitud = unificador.procesar_nombres()
        df_porcentaje_similitud.to_csv('resultado.csv', index=False)
        print(f"Resultados guardados en 'resultado.csv' exitosamente.")


if __name__ == '__main__':
    main()
