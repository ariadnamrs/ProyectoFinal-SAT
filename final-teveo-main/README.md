# Final-TeVeO

# ENTREGA CONVOCATORIA MAYO

# ENTREGA DE PRÁCTICA

## Datos

* Nombre: Ariadna Marcos Sanz
* Titulación: Grado de Ingeniería de Tecnologías de la Telecomunicación
* Cuenta en laboratorios: ariadnam
* Cuenta URJC: a.marcoss.2021@alumnos.urjc.es
* Video básico (url): https://youtu.be/HubEOD_GahU
* Video parte opcional (url): https://youtu.be/b84BXxFHOw4
* Despliegue (url): ariadnamarcos.pythonanywhare.com
* Contraseñas: 
* Cuenta Admin Site: usuario/contraseña: admin/admin

## Resumen parte obligatoria


### En cuanto a la parte obligatoria de la práctica:

- **Página principal:** Listado de comentarios de las cámaras, ordenados de más nuevos a más viejos, junto con la ID e imagen de cada cámara.
- **Página de cámaras:** Permite la descarga de datos de Listados 1 y Listados 2. Según la descarga, se muestra la información de cada cámara y sus respectivos enlaces (incluye opción dinámica y para añadir un comentario).
- **Página de cada cámara:** Muestra toda la información de la cámara seleccionada y sus enlaces respectivos (incluye opción dinámica y para añadir un comentario).
- **Página para poner un comentario:** Página destinada a escribir un comentario sobre una cámara específica. Muestra toda la información de la cámara y ofrece la funcionalidad para escribir comentarios.
- **Página dinámica:** Muestra de forma dinámica el contenido de la "Página de cámara", actualizándose cada 30 segundos. (Comentario: A veces se bloquea al intentar navegar a otra página con el menú de navegación, pero funciona al hacer clic varias veces).
- **Página de configuración:** Permite al usuario identificarse con un nombre. Por defecto, el usuario tiene el nombre 'Anónimo' hasta que rellena el formulario. También permite cambiar la configuración de TeVeO. (IMPORTANTE: Para poner tamaño de letra, debe de ir acompañado de 'px')
- **Página de ayuda:** Proporciona información sobre la página web.

### Elementos generales de todas las páginas HTML:

- **Cabecera:** Como especifica el enunciado, la cabecera está compuesta por el nombre de la aplicación web (TeVeO), que es un enlace a la página principal, una imagen de fondo y el nombre del comentador actual.
- **Menú:** Barra de navegación situada debajo de la cabecera, que permite acceder, mediante enlaces, al menos a las siguientes páginas: Principal, Cámaras, Configuración, Ayuda y Admin.
- **Pie:** Pie de página compuesto por el número de cámaras y comentarios en cada momento.
- **Marcado:** Se han implementado IDs para referir fácilmente en documentos CSS, como title, header, comentador, main-content, footer y nav.
- **CSS:** Elementos que deban tener el mismo aspecto están en una misma clase CSS para gestionarlo de forma común. Se han creado dos CSS: uno estático (por defecto en TeVeO) y otro dinámico (se sirve cuando el usuario ha cambiado la configuración de la aplicación web).
- **Bootstrap:** Añadido en cada página HTML.
- **Cámara en formato JSON:** Cada cámara tiene un enlace para ver su contenido en formato JSON.
- **Autenticación:** Utiliza las herramientas que proporciona Django para sesiones, administrando todo con sesiones. IMPORTANTE: Para "pasar" la configuración a otro navegador, se debe pasar al recurso una query string con la clave id y el valor dado en el panel de configuración.
- **Tests:** Se han realizado tests de extremo a extremo.

## Lista partes opcionales

- **Favicon.ico:** Inclusión del favicon.ico, usando una imagen de una cámara como favicon del sitio.
- **Terminar sesión:** Opción para terminar la sesión, disponible en el menú de configuración. Este enlace borra la sesión, haciendo que el usuario "parezca" que entra al sitio por primera vez (se borra su configuración, si la ha editado).
- **Me gusta:** Se ha añadido la funcionalidad para dar "me gusta" a las cámaras del sitio.
- **Codigo QR:** Por añadir un objeto nuevo al proyecto que esta actualmente de moda, he añadido un codigo qr para ver la fotografia de la camara con más likes de 2023 (juntando asi dos ideas de funcionalidades optativas.) IMPORTANTE: installar la biblioteca de codigo qr (se indica en requirements.txt)
- **Mejora de tests:** Se han mejorado los tests existentes.

