Programa: Inventario de edificaciones para Colombia
================================================
Este programa se desarrolló con el  propósito  del  artículo (Inventario  de  edificaciones  residenciales  de  Colombia  para  fines de  análisis  de  riesgos).  El  programa  se  subdividió  en  tres  módulos  (procesamientodatos, prostaxonomy, utilities) para facilidad de ejecución y modificación por parte del usuario. Está  desarrollado  en  python  3.6. 

- Descarga de datos del CNPV 2018: http://microdatos.dane.gov.co/index.php/catalog/643/get_microdata

Ejecución
--------

En la carpeta **folder** se encuentra el archivo `inventario.py`. En este archivo de python se ejemplifica el uso de los módulos para obtener un inventario detallado de las edificaciones de uno o múltiples municipios. El archivo `modelo_exposicion.py` por otro lado, hace uso de los módulos para obtener la matriz de tipologías por municipio. Se puede profundizar más en el funcionamiento de los diferentes módulos, modo y opciones de ejecución en la documentación que se puede encontrar en (xxxx).


Features
--------

* Basado en lenguaje de programación de uso libre.
* Fácil uso y adaptable a necesidades particulares.
* Permite realizar inventario detallado de edificaciones con sus características a nivel municipal o departamental.
* Realizado con motivos académicos y de investigación sobre gestión del riesgo.
* Ideado a partir del curso Ingeniería Sísmica de la Universidad EAFIT.

Modelo de exposición para Colombia
--------
Los resultados obtenidos para Colombia se pueden encontrar en **results** que consiste en cinco archivos:

* Número de edificaciones y personas por municipio.
* Número de edificaciones y personas por combinación de materiales de pared, piso y tipo de vivienda por municipio.
* Matriz de taxonomía por municipio.
* Matriz de taxonomía por combinación de materiales de pared, piso y tipo de vivienda por municipio.
* Matriz de taxonomía por combinación de materiales de pared, piso y tipo de vivienda por municipio agregada por número de pisos.
