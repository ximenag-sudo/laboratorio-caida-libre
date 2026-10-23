
from pathlib import Path
import csv
import math

# --------------------------------------------------
# 1. CONSTANTES FISICAS
# --------------------------------------------------

H0 = 10.00                  # Altura inicial en metros
G_REFERENCIA = 9.81         # Gravedad de referencia en m/s^2


# --------------------------------------------------
# 2. LECTURA DEL ARCHIVO CSV
# --------------------------------------------------

def leer_datos(ruta):
    """Lee los datos del archivo CSV."""

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo: {ruta}"
        )

    with ruta.open("r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)

        if lector.fieldnames is None:
            raise ValueError("El archivo CSV esta vacio.")

        columnas_requeridas = {
            "tiempo_s",
            "altura_m",
            "incertidumbre_m"
        }

        if not columnas_requeridas.issubset(lector.fieldnames):
            raise ValueError(
                "El CSV debe contener las columnas: "
                "tiempo_s, altura_m, incertidumbre_m."
            )

        filas = list(lector)

    if not filas:
        raise ValueError("El archivo CSV no contiene datos.")

    return filas


# --------------------------------------------------
# 3. VALIDACION DE LOS DATOS
# --------------------------------------------------

def validar_datos(filas):
    """Comprueba que los datos sean fisicamente validos."""

    datos = []
    tiempo_anterior = None

    for numero_fila, fila in enumerate(filas, start=2):

        try:
            tiempo = float(fila["tiempo_s"])
            altura = float(fila["altura_m"])
            incertidumbre = float(fila["incertidumbre_m"])

        except (ValueError, TypeError, KeyError) as error:
            raise ValueError(
                f"Hay datos invalidos en la fila {numero_fila}."
            ) from error

        valores = (tiempo, altura, incertidumbre)

        if not all(math.isfinite(valor) for valor in valores):
            raise ValueError(
                f"La fila {numero_fila} contiene valores no finitos."
            )

        if tiempo < 0:
            raise ValueError(
                f"El tiempo no puede ser negativo en la fila {numero_fila}."
            )

        if tiempo_anterior is not None and tiempo <= tiempo_anterior:
            raise ValueError(
                f"Los tiempos deben aumentar estrictamente. "
                f"Revisa la fila {numero_fila}."
            )

        if not 0 <= altura <= H0:
            raise ValueError(
                f"La altura debe estar entre 0 y {H0} m. "
                f"Revisa la fila {numero_fila}."
            )

        if incertidumbre <= 0:
            raise ValueError(
                f"La incertidumbre debe ser positiva. "
                f"Revisa la fila {numero_fila}."
            )

        datos.append({
            "tiempo_s": tiempo,
            "altura_m": altura,
            "incertidumbre_m": incertidumbre
        })

        tiempo_anterior = tiempo

    if datos[0]["tiempo_s"] != 0:
        raise ValueError(
            "La primera medicion debe corresponder a t = 0 s."
        )

    return datos


# --------------------------------------------------
# 4. CALCULO DE LAS ESTIMACIONES DE LA GRAVEDAD
# --------------------------------------------------

def calcular_gravedades(datos):
    """Calcula g_i para tiempos mayores que cero."""

    resultados = []

    for dato in datos:
        tiempo = dato["tiempo_s"]
        altura = dato["altura_m"]

        # En t = 0 no se calcula g_i porque habria
        # una division entre cero.
        if tiempo == 0:
            continue

        # Ecuacion: g_i = 2(H0 - h_i) / t_i^2
        gravedad = 2 * (H0 - altura) / (tiempo ** 2)

        resultados.append(gravedad)

    return resultados


# --------------------------------------------------
# 5. CALCULO DE ESTADISTICAS
# --------------------------------------------------

def calcular_estadisticas(valores):
    """Calcula estadisticas poblacionales y errores."""

    n = len(valores)

    if n == 0:
        raise ValueError("No hay estimaciones para analizar.")

    # Media aritmetica
    media = sum(valores) / n

    # Desviacion estandar poblacional
    varianza = sum(
        (valor - media) ** 2 for valor in valores
    ) / n

    desviacion = math.sqrt(varianza)

    # Valores extremos y rango
    minimo = min(valores)
    maximo = max(valores)
    rango = maximo - minimo

    # Diferencia frente al valor de referencia
    error_absoluto = abs(media - G_REFERENCIA)

    # Error relativo y porcentual
    error_relativo = error_absoluto / G_REFERENCIA
    error_porcentual = error_relativo * 100

    return (
        media,
        desviacion,
        minimo,
        maximo,
        rango,
        error_absoluto,
        error_relativo,
        error_porcentual
    )


# --------------------------------------------------
# 6. PRESENTACION DE RESULTADOS
# --------------------------------------------------

def mostrar_resultados(datos, gravedades, estadisticas):
    """Muestra la tabla y el resumen de resultados."""

    print("\n" + "=" * 75)
    print("ANALISIS DE CAIDA LIBRE")
    print("=" * 75)

    print(f"Altura inicial: {H0:.2f} m")
    print(f"Gravedad de referencia: {G_REFERENCIA:.2f} m/s^2")
    print(f"Numero de filas validas: {len(datos)}")
    print(f"Numero de estimaciones de gravedad: {len(gravedades)}")

    print("\nTABLA DE DATOS Y ESTIMACIONES")
    print("-" * 75)

    print(
        f"{'t (s)':>8} "
        f"{'h (m)':>10} "
        f"{'Incert. (m)':>13} "
        f"{'g_i (m/s^2)':>16}"
    )

    print("-" * 75)

    indice_gravedad = 0

    for dato in datos:
        tiempo = dato["tiempo_s"]
        altura = dato["altura_m"]
        incertidumbre = dato["incertidumbre_m"]

        if tiempo == 0:
            gravedad_texto = "No aplica"
        else:
            gravedad = gravedades[indice_gravedad]
            gravedad_texto = f"{gravedad:.4f}"
            indice_gravedad += 1

        print(
            f"{tiempo:8.2f} "
            f"{altura:10.2f} "
            f"{incertidumbre:13.3f} "
            f"{gravedad_texto:>16}"
        )

    (
        media,
        desviacion,
        minimo,
        maximo,
        rango,
        error_absoluto,
        error_relativo,
        error_porcentual
    ) = estadisticas

    print("\nESTADISTICAS")
    print("-" * 45)
    print(f"Media de g: {media:.4f} m/s^2")
    print(f"Desviacion estandar poblacional: {desviacion:.4f} m/s^2")
    print(f"Minimo de g: {minimo:.4f} m/s^2")
    print(f"Maximo de g: {maximo:.4f} m/s^2")
    print(f"Rango: {rango:.4f} m/s^2")
    print(f"Diferencia absoluta: {error_absoluto:.4f} m/s^2")
    print(f"Error relativo: {error_relativo:.4f}")
    print(f"Error porcentual: {error_porcentual:.2f} %")

    print("\nVALIDACION")
    print("-" * 45)
    print("Los datos superaron las validaciones.")
    print("La medicion t = 0 s se conserva, pero no se usa para calcular g_i.")
    print("La incertidumbre de altura se muestra en la tabla.")
    print("No se realizo propagacion formal de incertidumbres.")

    print("=" * 75)


# --------------------------------------------------
# 7. PROGRAMA PRINCIPAL
# --------------------------------------------------

def main():
    # Permite encontrar el CSV aunque se ejecute el
    # programa desde otra carpeta.
    carpeta_programa = Path(__file__).resolve().parent
    ruta_csv = carpeta_programa / "caida_libre_sintetica.csv"

    try:
        filas = leer_datos(ruta_csv)
        datos = validar_datos(filas)
        gravedades = calcular_gravedades(datos)
        estadisticas = calcular_estadisticas(gravedades)

        mostrar_resultados(datos, gravedades, estadisticas)

    except (FileNotFoundError, ValueError) as error:
        print(f"\nERROR: {error}")


if __name__ == "__main__":
    main()
