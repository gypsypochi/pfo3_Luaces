import socket


HOST = "127.0.0.1"
PORT = 5000


def send_task(task):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(task.encode("utf-8"))

        response = client_socket.recv(4096).decode("utf-8")
        print("\nRespuesta del servidor:")
        print(response)

    except ConnectionRefusedError:
        print("Error: no se pudo conectar con el servidor. Verificá que server.py esté ejecutándose.")

    except Exception as error:
        print(f"Error en el cliente: {error}")

    finally:
        client_socket.close()


def main():
    print("Cliente de gestión de notas por sockets")
    print("Comandos disponibles:")
    print("AGREGAR texto de la nota")
    print("LISTAR")
    print("ELIMINAR id")
    print("AYUDA")
    print("SALIR")

    while True:
        task = input("\nIngresá una tarea: ").strip()

        if task.upper() == "SALIR":
            print("Cliente finalizado.")
            break

        if not task:
            print("No ingresaste ninguna tarea.")
            continue

        send_task(task)


if __name__ == "__main__":
    main()