# PFO 3 - Rediseño como Sistema Distribuido Cliente-Servidor

## Repositorio de GitHub

https://github.com/gypsypochi/pfo3_Luaces

## Descripción del proyecto

Este proyecto corresponde a la PFO 3 de Programación sobre Redes. El objetivo es rediseñar un sistema como una arquitectura distribuida utilizando sockets.

La solución implementada es un sistema de gestión de notas. Un cliente envía tareas al servidor mediante sockets TCP, el servidor recibe esas tareas, las coloca en una cola interna y las distribuye a workers implementados con hilos.

El proyecto incluye:

- Diagrama de arquitectura distribuida.
- Servidor en Python con sockets TCP.
- Cliente en Python que envía tareas y recibe resultados.
- Pool de workers para procesar tareas.
- Cola interna con `queue.Queue` para simular la distribución de tareas.

## Consigna cubierta

La consigna solicita:

1. Diseñar un diagrama que incluya:
   - Clientes móviles y web.
   - Balanceador de carga Nginx o HAProxy.
   - Servidores workers con pool de hilos.
   - Cola de mensajes RabbitMQ.
   - Almacenamiento distribuido PostgreSQL y S3.

2. Implementar en Python:
   - Un servidor que reciba tareas por socket y las distribuya a workers.
   - Un cliente que envíe tareas y reciba resultados.

En este proyecto, el diagrama representa la arquitectura distribuida completa solicitada. La implementación en Python corresponde a un prototipo local funcional con sockets TCP, workers y una cola interna.

RabbitMQ, PostgreSQL y S3 se incluyen en el diseño arquitectónico. En el prototipo local, RabbitMQ se representa mediante `queue.Queue`, y el almacenamiento se realiza con un archivo JSON generado durante la ejecución.

## Estructura del proyecto

pfo3_Luaces/
│
├── cliente/
│   └── client.py
│
├── servidor/
│   └── server.py
│
├── diagramas/
│   └── arquitectura.md
│
├── README.md
├── .gitignore
└── LICENSE


## Diagrama del sistema

El diagrama se encuentra en:

diagramas/arquitectura.md

Incluye los componentes principales de una arquitectura distribuida:

- Clientes web y móviles.
- Balanceador de carga Nginx / HAProxy.
- Servidores workers con pool de hilos.
- RabbitMQ como cola de mensajes.
- PostgreSQL como almacenamiento de datos estructurados.
- S3 como almacenamiento de archivos u objetos.

## Funcionamiento general

El sistema funciona bajo el modelo cliente-servidor.

El cliente permite ingresar tareas desde la terminal. Cada tarea se envía al servidor mediante un socket TCP.

El servidor escucha conexiones en `127.0.0.1:5000`. Cuando recibe una tarea, la agrega a una cola interna. Luego, uno de los workers disponibles toma la tarea, la procesa y devuelve una respuesta al cliente.

## Comandos disponibles

El cliente permite usar los siguientes comandos:

AGREGAR texto de la nota
LISTAR
ELIMINAR id
AYUDA
SALIR

Ejemplos:

AGREGAR Estudiar arquitectura cliente-servidor
AGREGAR Probar comunicación con sockets TCP
LISTAR
ELIMINAR 1
LISTAR

## Cómo ejecutar el proyecto

Primero, clonar o descargar el repositorio.

Luego, desde la carpeta raíz del proyecto, abrir una terminal y ejecutar el servidor:

```bash
python servidor/server.py
```

El servidor mostrará un mensaje similar a:

[Servidor] Escuchando en 127.0.0.1:5000
[Servidor] Pool de workers iniciado con 3 hilos
[Servidor] Esperando conexiones...

Después, abrir una segunda terminal en la misma carpeta del proyecto y ejecutar el cliente:

```bash
python cliente/client.py
```

Desde el cliente se pueden ingresar los comandos disponibles.

## Ejemplo de prueba

Entrada desde el cliente:

AGREGAR Estudiar arquitectura cliente-servidor
AGREGAR Probar comunicación con sockets TCP
LISTAR
ELIMINAR 1
LISTAR

Salida esperada:

Nota agregada correctamente con ID 1
Nota agregada correctamente con ID 2
Notas guardadas:
1 - Estudiar arquitectura cliente-servidor
2 - Probar comunicación con sockets TCP
Nota con ID 1 eliminada correctamente
Notas guardadas:
2 - Probar comunicación con sockets TCP

## Relación con sockets

El sistema utiliza sockets TCP para permitir la comunicación entre cliente y servidor. El servidor crea un socket, lo vincula a una dirección IP y puerto, escucha conexiones, recibe datos y responde al cliente.

El cliente crea su propio socket, se conecta al servidor, envía una tarea y espera la respuesta.

## Relación con workers y cola de tareas

El servidor no procesa directamente cada tarea recibida. Primero la coloca en una cola interna implementada con `queue.Queue`.

Luego, los workers toman tareas de esa cola y las procesan. Esto permite representar una distribución de trabajo similar a la de un sistema distribuido.

## Aclaración sobre RabbitMQ, PostgreSQL y S3

RabbitMQ, PostgreSQL y S3 forman parte del diseño distribuido representado en el diagrama.

Para esta implementación local:

- RabbitMQ se simula con `queue.Queue`.
- PostgreSQL se representa de forma simplificada con persistencia en archivo JSON.
- S3 se muestra en el diagrama como almacenamiento de objetos dentro de la arquitectura propuesta.

Esta decisión permite entregar un prototipo funcional y ejecutable en Python, cumpliendo la implementación solicitada de sockets, servidor, cliente y workers.

## Tecnologías utilizadas

- Python 3
- Sockets TCP
- Threading
- Queue
- JSON
- Git y GitHub
- Mermaid para el diagrama

## Archivos principales

servidor/server.py

Contiene el servidor TCP, la cola interna y el pool de workers.

cliente/client.py

Contiene el cliente que envía tareas al servidor y recibe resultados.

diagramas/arquitectura.md

Contiene el diagrama de arquitectura distribuida.
