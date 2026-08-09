import datetime
import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

clients = []  # each entry: {"conn": socket, "addr": address, "username": str}
clients_lock = threading.Lock()


def timestamp() -> str:
    return datetime.datetime.now().strftime("%H:%M")


def broadcast(message: str, exclude_conn=None) -> None:
    with clients_lock:
        for client in clients:
            if client["conn"] is exclude_conn:
                continue
            try:
                client["conn"].sendall(message.encode("utf-8"))
            except OSError:
                pass


def remove_client(conn) -> str:
    username = "Someone"
    with clients_lock:
        for client in clients:
            if client["conn"] is conn:
                username = client["username"]
                clients.remove(client)
                break
    return username


def handle_client(conn: socket.socket, addr) -> None:
    try:
        username = conn.recv(1024).decode("utf-8").strip()
        if not username:
            username = f"Guest-{addr[1]}"

        with clients_lock:
            clients.append({"conn": conn, "addr": addr, "username": username})

        print(f"[SERVER] {username} connected from {addr}.")
        broadcast(f"[{timestamp()}] *** {username} has joined the chat ***\n", exclude_conn=conn)
        conn.sendall(f"[{timestamp()}] *** Connected as {username} ***\n".encode("utf-8"))

        while True:
            data = conn.recv(1024)
            if not data:
                break

            text = data.decode("utf-8").strip()
            if not text:
                continue

            formatted = f"[{timestamp()}] {username}: {text}\n"
            print(formatted.strip())
            broadcast(formatted, exclude_conn=conn)

    except (ConnectionResetError, ConnectionAbortedError):
        pass
    except Exception as e:
        print(f"[SERVER] Unexpected error for {addr}: {e}")
    finally:
        username = remove_client(conn)
        print(f"[SERVER] {username} disconnected.")
        broadcast(f"[{timestamp()}] *** {username} has left the chat ***\n", exclude_conn=conn)
        conn.close()


def main() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[SERVER] Listening on {HOST}:{PORT}. Waiting for clients...")

    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
