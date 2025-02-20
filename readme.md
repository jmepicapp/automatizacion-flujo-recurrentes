# Automatización de Flujos Recurrentes con Python

## Descripción

Este repositorio contiene la guía completa para la formación **"Automatización Inteligente: Diseña y Optimiza Flujos Recurrentes con Python"**. La formación abarca desde el análisis de procesos repetitivos hasta la implementación de una solución automatizada que integra APIs con Flask, gestión de tareas mediante un demonio, y generación de reportes dinámicos con Jinja.

## Objetivos

- Comprender qué son los flujos recurrentes y su impacto en la eficiencia operativa.
- Analizar y mapear procesos repetitivos para identificar oportunidades de automatización.
- Diseñar una solución automatizada usando:
  - **Flask** para la creación de APIs.
  - **SQLAlchemy** para la gestión de la base de datos.
  - **Jinja** para la generación de plantillas dinámicas.
  - **Flask-RESTX** para exponer y documentar la API con Swagger.
- Evaluar el impacto de la automatización a través de métricas y KPIs.

## Estructura del Proyecto

La estructura del repositorio es la siguiente:

```
automatizacion-flujos/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── demonio.py
│   ├── dependencies.py
│   ├── flujos/
│   │   ├── reportes/
│   │   │   ├── recipe.yml
│   │   │   ├── Reporte.py
│   │   │   ├── templates/
│   │   │   │   ├── validacion_datos.j2
│   │   │   │   ├── procesamiento_datos.j2
│   │   │   │   ├── generacion_informe.j2
│   │   ├── facturacion/
│   │   │   ├── recipe.yml
│   │   │   ├── Factura.py
│   │   │   ├── templates/
│   │   │   │   ├── verificacion_pagos.j2
│   │   │   │   ├── generacion_factura.j2
│   │   │   │   ├── envio_notificacion.j2
├── tests/
│   └── test_api.py
├── requirements.txt
└── README.md
```
- **app/api.py**: Define los endpoints de la API para iniciar y consultar flujos.
- **app/demonio.py**: Simula la ejecución de los pasos del flujo, actualizando el estado en la base de datos.
- **app/flujos/**: Contiene las definiciones de los modelos utilizando SQLAlchemy las recipes que orquestan el flujo y las plantillas.
- **diagrams/flujo_automatizado.pdf**: Diagrama visual que ilustra el proceso de automatización.
- **tests/test_api.py**: Pruebas unitarias para asegurar el correcto funcionamiento de la API.

## Instalación y Ejecución

### Requisitos

- Python 3.x
- pip

### Pasos para instalar y ejecutar el proyecto

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/automatizacion-flujos.git
   cd automatizacion-flujos
   ```

2. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```
   
3. **Ejecutar la API (con Swagger):**

   ```bash
   python app/api.py
   ```
    *Por defecto, se levanta en http://127.0.0.1:5000 y la documentación Swagger se encuentra en /api*


4. **Ejecutar el demonio de orquestación:**

    ```bash
    python app/demonio.py
    ```
   *Simulará la ejecución de los pasos de forma indefinida.*

## Personalizar los Flujos
- Puedes editar los archivos recipe.yml para definir nuevos pasos o dependencias.
- Cada paso puede tener una plantilla .j2 asociada para generar contenido dinámico (JSON, reportes, etc.).
- Para un control de estados más completo, amplía la lógica en demonio.py y dependencies.py.

## Tests
Para ejecutar las pruebas:

   ```bash
   python -m unittest discover tests
   ```