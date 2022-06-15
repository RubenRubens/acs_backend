# Paranoid Social Network

## Como obtener el código fuente

La forma mas sencilla de obtener el código fuente es a traves de GIT.

```
git clone https://github.com/RubenRubens/paranoid_backend.git
cd paranoid_backend
```

## Como ejecutar este proyecto

Este proyecto utiliza Python, PostgreSQL y Redis. No es necesario
descargar ninguna de esas
El único requisito es tener Docker (y docker-compose) instalado. Para
poner en funcionamiento el proyecto:

```
docker-compose up
```

Ahora deberías de obtener un respuesta en `http://localhost:8000`.

Para ver los contenedores que hay en ejecución:

```
docker-compose ps
```

Para entrar en el contenedor de Python:

```
docker exec -it paranoid_backend_web_1 bash
```

Una vez dentro del contenedor puedes ejecutar los test del proyecto
con el comando:

```
./manage.py test
```

## Opciones para consumir la API

Es posible utilizar la API directamente con un navegador web. En algunos
endpoints se incluye un formulario y en otros no se hace. Por ejemplo, es posible
hacer login abriendo un navegador web y dirigirse a `localhost:8000/account/login/`.
Es por ello que se recomienda utilizar algún otro tipo de cliente HTTP para consumir
la API, como por ejemplo cURL, Postman o HTTPie. La lista completa de con todos los
endpoints puede encontrarse en `localhost:8000/docs/`.

## Uso con HTTPie en UNIX

Para consumir y testar la API es interesante se ha utilizado [HTTPie](https://httpie.io/docs/cli/installation).
Todo lo que se necesita es tener HTTPie instalado. Algunos comandos son específicos de
sistemas UNIX, pero con cambios mínimos se pueden reproducir los resultados en PowerShell.

### Endpoints mas interesante

+ Crear un nuevo usuario.

```
http localhost:8000/account/registration/ username=mario password=secret first_name=Mario last_name=M
```

+ Hacer login (es decir, obtener el Token).

```
http localhost:8000/account/login/ username=francisco password=secret
```

Ahora copiamos el Token (llamado key) y creamos  una variable de entorno para utilizarla como
_header_ en todas las siguientes llamadas HTTP.

```
HEADER="Authorization: Token c60e234c03d5170d7db707fdf12063ddff020695"
```

+ Obtener la información del usuario con el que hemos hecho el login.

```
http localhost:8000/account/user/ $HEADER
```

+ Obtener la información de un usuario en concreto (el usuario con id=1).

```
http localhost:8000/account/user/1/ $HEADER
```

+ Obtener la información de un perfil de usuario en concreto.

```
http localhost:8000/account/account/1/ $HEADER
```

+ Cambiar la biografía del perfil.

```
http PATCH localhost:8000/account/account/1/ $HEADER bio="Its me, Mario"
```

+ Actualizar la foto de perfil.

```
http -f PUT localhost:8000/account/account/1/ $HEADER profile_picture@my_photo.png
```

+ Descargar una fotografía de perfil.

```
http localhost:8000/account/profile_picture/1/ $HEADER > perfil.png
```

+ Enviar una solicitud de amistad a otro usuario.

```
http localhost:8000/account/petition/send/ $HEADER user=5
```

+ Obtener una lista con las peticiones de amistad recibidas.

```
http localhost:8000/account/petition/ $HEADER
```

+ Aceptar una solicitud de amistad recibida.

```
http localhost:8000/account/petition/accept/ $HEADER possible_follower=3
```

+ Listar los usuario que siguen a un usuario.

```
http localhost:8000/account/following/1/ $HEADER
```

+ Listar los seguidores de un usuario.

```
http localhost:8000/account/followers/1/ $HEADER
```

+ Buscar usuarios por nombre, apellido y username.

```
http localhost:8000/account/search/ $HEADER name=cesar
```

+ Obtener el feed.

```
http localhost:8000/photos/feed/ $HEADER
```

+ Crear una publicación

```
http -f localhost:8000/photos/post/ $HEADER image_file@my_image.png
```

+ Descargar una imagen

```
http localhost:8000/photos/image/1/ $HEADER > image.png
```

+ Obtener las publicaciones de una persona

```
http localhost:8000/photos/post_list/1/ $HEADER
```

+ Dar "me gusta" a una publicación.

```
http POST localhost:8000/photos/post_like/1/ $HEADER
```

+ Obtener los usuarios que le han dado a "me gusta" a una publicación.

```
http localhost:8000/photos/post_like/1/ $HEADER
```

+ Quitar "me gusta" a una publicación.

```
http DELETE localhost:8000/photos/post_like/1/ $HEADER
```

+ Comentar una publicación.

```
http localhost:8000/photos/comment/ $HEADER post=1 text="This is a comment"
```

+ Lista de comentarios de una publicación.

```
http localhost:8000/photos/comment_list/1/ $HEADER
```

+ Elimina un comentario.

```
http DELETE localhost:8000/photos/comment_destroy/1/ $HEADER
```
