import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(conn):
    try:
        with conn.makefile("r", encoding="utf-8") as reader:
            for line in reader:
                print("\n" + line.rstrip("\r\n"))
    except (OSError, UnicodeError):
        pass


def main():
    name = input("Ваше ім'я: ").strip()
    if not name:
        print("Ім'я не може бути порожнім")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((HOST, PORT))
            client.sendall((name + "\n").encode("utf-8"))
        except OSError:
            print("Не вдалося підключитися до сервера")
            return

        threading.Thread(
            target=receive_messages, args=(client,), daemon=True
        ).start()

        try:
            while True:
                message = input()
                if not message:
                    continue
                client.sendall((message + "\n").encode("utf-8"))
                if message == "/exit":
                    break
        except (KeyboardInterrupt, EOFError, OSError):
            pass
        finally:
            try:
                client.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

    print("Ви вийшли з чату")


if __name__ == "__main__":
    main()
