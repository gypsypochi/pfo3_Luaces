import socket
import threading
import queue
import json
import os


HOST = "127.0.0.1"
PORT = 5000
WORKERS = 3
DATA_FILE = "notas.json"

task_queue = queue.Queue()
notes_lock = threading.Lock()


def load_notes():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_notes(notes):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=4, ensure_ascii=False)


def process_task(task):
    parts = task.strip().split(" ", 1)
    command = parts[0].upper()

    with notes_lock:
        notes = load_notes()

        if command == "AGREGAR":
            if len(parts) < 2 or not parts[1].strip():
                return "Error: tenés que escribir una nota. Ejemplo: AGREGAR Estudiar sockets"

            new_id = notes[-1]["id"] + 1 if notes else 1
            note = {
                "id": new_id,
                "texto": parts[1].strip()
            }

            notes.append(note)
            save_notes(notes)

            return f"Nota agregada correctamente con ID {new_id}"

        elif command == "LISTAR":
            if not notes:
                return "No hay notas guardadas."

            result = "Notas guardadas:\n"
            for note in notes:
                result += f'{note["id"]} - {note["texto"]}\n'

            return result.strip()

        elif command == "ELIMINAR":
            if len(parts) < 2 or not parts[1].strip().isdigit():
                return "Error: tenés que indicar el ID. Ejemplo: ELIMINAR 1"

            note_id = int(parts[1])
            filtered_notes = [note for note in notes if note["id"] != note_id]

            if len(filtered_notes) == len(notes):
                return f"No existe una nota con ID {note_id}"

            save_notes(filtered_notes)
            return f"Nota con ID {note_id} eliminada correctamente"

        elif command == "AYUDA":
            return (
                "Comandos disponibles:\n"
                "AGREGAR texto de la nota\n"
                "LISTAR\n"
                "ELIMINAR id\n"
                "SALIR"
            )

        else:
            return (
                "Comando no reconocido.\n"
                "Usá AYUDA para ver los comandos disponibles."
            )


def worker(worker_id):
    while True:
        client_socket, client_address, task = task_queue.get()

        try:
            print(f"[Worker {worker_id}] Procesando tarea de {client_address}: {task}")
            response = process_task(task)
            client_socket.sendall(response.encode("utf-8"))

        except Exception as error:
            error_message = f"Error interno del servidor: {error}"
            client_socket.sendall(error_message.encode("utf-8"))

        finally:
            client_socket.close()
            task_queue.task_done()


def handle_client(client_socket, client_address):
    try:
        data = client_socket.recv(1024).decode("utf-8")

        if not data:
            client_socket.close()
            return

        print(f"[Servidor] Tarea recibida de {client_address}: {data}")
        task_queue.put((client_socket, client_address, data))

    except Exception as error:
        print(f"[Servidor] Error con el cliente {client_address}: {error}")
        client_socket.close()


def start_server():
    for i in range(WORKERS):
        thread = threading.Thread(target=worker, args=(i + 1,), daemon=True)
        thread.start()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[Servidor] Escuchando en {HOST}:{PORT}")
    print(f"[Servidor] Pool de workers iniciado con {WORKERS} hilos")
    print("[Servidor] Esperando conexiones...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[Servidor] Cliente conectado: {client_address}")

            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[Servidor] Servidor detenido manualmente.")

    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()