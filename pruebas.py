
from pathlib import Path
from tempfile import TemporaryDirectory

from main import (
    leer_datos,
    validar_datos,
    calcular_gravedades
)


def comprobar_error(nombre, funcion):
    """Comprueba que un caso invalido produzca un error esperado."""

    try:
        funcion()
    except (ValueError, FileNotFoundError) as error:
        print(f"[APROBADA] {nombre}")
        print(f"  Se detecto correctamente: {error}")
    else:
        raise AssertionError(
            f"FALLO: la prueba '{nombre}' debio generar un error."
        )


def prueba_calculo_manual():
    """Comprueba un caso cuyo resultado se conoce de antemano."""

    filas = [
        {
            "tiempo_s": "0",
            "altura_m": "10",
            "incertidumbre_m": "0.03"
        },
        {
            "tiempo_s": "1",
            "altura_m": "5.095",
            "incertidumbre_m": "0.03"
        }
    ]

    datos = validar_datos(filas)
    gravedades = calcular_gravedades(datos)

    assert len(gravedades) == 1
    assert abs(gravedades[0] - 9.81) < 1e-9

    print("[APROBADA] Calculo manual")
    print(f"  Gravedad calculada: {gravedades[0]:.2f} m/s^2")
    print("  Gravedad esperada: 9.81 m/s^2")


def prueba_archivo_vacio():
    """Comprueba que se rechace un archivo CSV vacio."""

    with TemporaryDirectory() as carpeta:
        ruta = Path(carpeta) / "vacio.csv"
        ruta.write_text("", encoding="utf-8")

        comprobar_error(
            "Archivo vacio",
            lambda: leer_datos(ruta)
        )


def prueba_fila_invalida():
    """Comprueba que se rechacen datos que no son numericos."""

    filas = [
        {
            "tiempo_s": "0",
            "altura_m": "10",
            "incertidumbre_m": "0.03"
        },
        {
            "tiempo_s": "abc",
            "altura_m": "9.5",
            "incertidumbre_m": "0.03"
        }
    ]

    comprobar_error(
        "Fila con dato invalido",
        lambda: validar_datos(filas)
    )


def prueba_tiempos_no_crecientes():
    """Comprueba que los tiempos deban aumentar estrictamente."""

    filas = [
        {
            "tiempo_s": "0",
            "altura_m": "10",
            "incertidumbre_m": "0.03"
        },
        {
            "tiempo_s": "1",
            "altura_m": "5",
            "incertidumbre_m": "0.03"
        },
        {
            "tiempo_s": "1",
            "altura_m": "4",
            "incertidumbre_m": "0.03"
        }
    ]

    comprobar_error(
        "Tiempos repetidos o no crecientes",
        lambda: validar_datos(filas)
    )


def prueba_frontera_tiempo_cero():
    """Comprueba que t = 0 se conserve sin calcular g en esa fila."""

    filas = [
        {
            "tiempo_s": "0",
            "altura_m": "10",
            "incertidumbre_m": "0.03"
        },
        {
            "tiempo_s": "1",
            "altura_m": "5.095",
            "incertidumbre_m": "0.03"
        }
    ]

    datos = validar_datos(filas)
    gravedades = calcular_gravedades(datos)

    assert datos[0]["tiempo_s"] == 0
    assert len(datos) == 2
    assert len(gravedades) == 1

    print("[APROBADA] Frontera t = 0")
    print("  La fila inicial se conserva.")
    print("  No se calcula g_i para t = 0.")
    print(f"  Estimaciones calculadas: {len(gravedades)}")


def main():
    print("=" * 55)
    print("PRUEBAS DEL PROGRAMA DE CAIDA LIBRE")
    print("=" * 55)

    prueba_calculo_manual()
    print()

    prueba_archivo_vacio()
    print()

    prueba_fila_invalida()
    print()

    prueba_tiempos_no_crecientes()
    print()

    prueba_frontera_tiempo_cero()
    print()

    print("=" * 55)
    print("RESULTADO: LAS CINCO PRUEBAS FUERON APROBADAS.")
    print("=" * 55)


if __name__ == "__main__":
    main()
