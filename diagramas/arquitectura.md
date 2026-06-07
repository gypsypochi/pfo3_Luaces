# Diagrama de arquitectura distribuida

Este diagrama representa el rediseño del sistema como una arquitectura distribuida cliente-servidor. Incluye clientes web y móviles, un balanceador de carga, servidores workers con pool de hilos, una cola de mensajes y almacenamiento distribuido.

```mermaid
flowchart TD

    subgraph Clientes
        C1[Cliente Web]
        C2[Cliente Móvil]
    end

    LB[Balanceador de carga<br/>Nginx / HAProxy]

    subgraph Servidores["Servidores de aplicación"]
        S1[Servidor Worker 1<br/>Pool de hilos]
        S2[Servidor Worker 2<br/>Pool de hilos]
        S3[Servidor Worker 3<br/>Pool de hilos]
    end

    MQ[Cola de mensajes<br/>RabbitMQ]

    subgraph Almacenamiento["Almacenamiento distribuido"]
        DB[(PostgreSQL<br/>Datos estructurados)]
        S3Storage[(S3<br/>Archivos / objetos)]
    end

    C1 -->|Solicitudes / tareas| LB
    C2 -->|Solicitudes / tareas| LB

    LB -->|Distribuye carga| S1
    LB -->|Distribuye carga| S2
    LB -->|Distribuye carga| S3

    S1 -->|Publica / consume mensajes| MQ
    S2 -->|Publica / consume mensajes| MQ
    S3 -->|Publica / consume mensajes| MQ

    S1 -->|Lee / escribe datos| DB
    S2 -->|Lee / escribe datos| DB
    S3 -->|Lee / escribe datos| DB

    S1 -->|Guarda / consulta archivos| S3Storage
    S2 -->|Guarda / consulta archivos| S3Storage
    S3 -->|Guarda / consulta archivos| S3Storage

    MQ -->|Coordina tareas entre servidores| S1
    MQ -->|Coordina tareas entre servidores| S2
    MQ -->|Coordina tareas entre servidores| S3
```

## Explicación breve

Los clientes web y móviles envían tareas al sistema. El balanceador de carga, que puede implementarse con Nginx o HAProxy, distribuye las solicitudes entre varios servidores workers.

Cada servidor worker posee un pool de hilos, lo que permite procesar varias tareas de manera concurrente. Para la comunicación entre servidores se utiliza una cola de mensajes RabbitMQ, que ayuda a organizar las tareas y desacoplar los componentes.

El almacenamiento se divide en PostgreSQL para datos estructurados y S3 para archivos u objetos. Esta separación permite mejorar la escalabilidad, la organización y la disponibilidad del sistema.