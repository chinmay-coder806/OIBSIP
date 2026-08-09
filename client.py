import socket
import sys
import threading

HOST = "127.0.0.1"
PORT = 5555


def receive_messages(sock: socket.socket) -> None:
    while True:
        try:
            data = sock.recv(1024)
        except OSError:
            break

        if not data:
            print("\n[Connection closed by server.]")
            break

        print(f"\r{data.decode('utf-8')}You: ", end="", flush=True)


def main() -> None:
    username = input("Enter your username: ").strip() or "Guest"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"Could not connect to server at {HOST}:{PORT}. "
              f"Make sure server.py is running first.")
        sys.exit(1)

    client_socket.sendall(username.encode("utf-8"))

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    print("Connected! Type a message and press Enter to send. Type 'exit' to quit.\n")

    try:
        while True:
            message = input("You: ")
            if message.strip().lower() == "exit":
                break
            if message.strip():
                try:
                    client_socket.sendall(message.encode("utf-8"))
                except OSError:
                    print("[Lost connection to server.]")
                    break
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        client_socket.close()
        print("Disconnected.")


if __name__ == "__main__":
    main()
