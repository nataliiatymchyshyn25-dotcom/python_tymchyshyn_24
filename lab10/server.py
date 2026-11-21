import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients = {}
clients_lock = threading.Lock()
send_lock = threading.Lock()

def send_message(conn, message):
    try:
        with send_lock:
            conn.sendall((message + "\n").encode("utf-8"))
    except OSError:
        pass


def broadcast(message, sender=None):
    with clients_lock:
        recipients = list(clients)

    for conn in recipients:
        if conn is not sender:
            send_message(conn, message)

def handle_client(conn, address):
    name = None
    try:
        with conn:
            with conn.makefile("r", encoding="utf-8") as reader:
                name = reader.readline().strip()
                if not name:
                    return

                with clients_lock:
                    clients[conn] = name

                print(f"Підключився {name}: {address}")
                send_message(conn, "Ви в чаті! Для виходу введіть /exit")
                broadcast(f"* {name} приєднався до чату", sender=conn)

                for line in reader:
                    message = line.strip()
                    if message == "/exit":
                        break
                    if message:
                        text = f"{name}: {message}"
                        print(text)
                        broadcast(text, sender=conn)
    except (OSError, UnicodeError):
        pass
    finally:
        with clients_lock:
            was_connected = clients.pop(conn, None) is not None
        if was_connected:
            print(f"Відключився {name}")
            broadcast(f"* {name} вийшов із чату")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Сервер запущено на {HOST}:{PORT}")

        try:
            while True:
                conn, address = server.accept()
                thread = threading.Thread(
                    target=handle_client, args=(conn, address), daemon=True
                )
                thread.start()
        except KeyboardInterrupt:
            print("\nСервер зупинено")

if __name__ == "__main__":
    main()
