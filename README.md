# Laboratorio de caída libre

## Descripción

Este proyecto analiza datos sintéticos de un objeto en caída libre utilizando Python. El objetivo es estimar la aceleración de la gravedad y comparar los resultados con el valor de referencia de 9.81 m/s².

## Modelo físico

La altura del objeto se describe mediante:

h(t) = h0 - (g*t²)/2

Donde h0 es la altura inicial, t es el tiempo y g es la aceleración de la gravedad.

La altura inicial utilizada es de 10.00 m.

## Archivos del proyecto

- `main.py`: programa principal.
- `pruebas.py`: pruebas del programa.
- `caida_libre_sintetica.csv`: datos sintéticos utilizados en el análisis.
- [Informe del laboratorio en PDF](Informe_Laboratorio_Caida_Libre.pdf)
## Requisitos


## Requisitos y dependencias

- **Lenguaje:** Python 3.
- **Dependencias externas:** ninguna.
- **Bibliotecas utilizadas:** módulos de la biblioteca estándar de Python, como `pathlib`, `csv` y `math`, según las importaciones del código.
- **Versión exacta de Python:** pendiente de verificar en el entorno de ejecución.

## Cómo ejecutar

Para ejecutar el programa:

```bash
python main.py
```

Para ejecutar las pruebas:

```bash
python pruebas.py
```

Si el comando `python` no funciona en tu equipo, puede ser necesario utilizar `python3`.

## Datos y resultados

El programa valida los datos del archivo CSV, calcula estimaciones de la gravedad para tiempos mayores que cero y obtiene estadísticas para comparar los resultados con el valor de referencia.

Los resultados detallados se presentan en el informe PDF.

## Autoría

- Estudiante: [Ximena Criollo Grisales]
- Asignatura: Programación
- Docente: [Santiago Echeverry]
