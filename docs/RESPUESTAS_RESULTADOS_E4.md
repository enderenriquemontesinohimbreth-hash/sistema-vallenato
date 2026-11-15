# Respuestas para usar después de verificar el módulo de resultados

No presentar la función como verificada antes de instalarla y completar las pruebas. Respuestas breves para el banco de la Entrega 4:

## Pregunta 16 De dónde obtiene la aplicación los datos para mostrar los resultados

Los resultados se obtienen de los votos guardados en MySQL. Django los agrupa y cuenta por opción mediante el ORM y Count. La página permite elegir edición y categoría, incluye opciones con cero votos y actualiza los conteos al recargar, sin mostrar nombres de votantes.

## Pregunta 2 Función de modelos vistas y plantillas

Los modelos representan los datos y sus relaciones. Las vistas procesan solicitudes y consultan MySQL; la vista de resultados cuenta los votos por opción. Las plantillas presentan los formularios y las tablas que ve el usuario, siguiendo el patrón MVT.

## Pregunta 4 Relación entre URL y vista

Django conecta cada dirección con una vista mediante path en urls.py. En nuestro proyecto, /resultados/ llama a la vista resultados de festival/resultados.py. Esa vista valida los filtros, consulta los votos y entrega los datos a resultados.html.

## Pregunta 17 Pruebas realizadas

La versión anterior aprobó 39 pruebas locales. Agregamos siete pruebas de resultados para conteos, ceros, filtros, privacidad, categorías cerradas y actualización. Para la sustentación indicaremos el número y resultado real de la nueva ejecución; no consideramos aprobadas las pruebas que no se hayan ejecutado.

## Pregunta 20 Configuración para 2028

El administrador crea la edición 2028, sus categorías, subeventos y opciones, y habilita la participación correspondiente. No necesita modificar el código. La página de resultados permite seleccionar esa edición y consultar los conteos, incluyendo opciones que todavía tienen cero votos.

## Aclaración si preguntan cuándo se publican resultados

Para la demostración académica mostramos los acumulados de categorías abiertas como provisionales y conservamos los de categorías cerradas. No declaramos ganadores. La política definitiva de visibilidad para un Festival real requiere validación de sus organizadores.
