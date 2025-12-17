import argparse
import socket


def recv_line(conn: socket.socket) -> str:
    """Lesen bis \\n oder connection close."""
    buf = b""
    while b"\n" not in buf:
        chunk = conn.recv(1024)
        if not chunk:
            break
        buf += chunk
    return buf.split(b"\n", 1)[0].decode("utf-8", errors="replace").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Basic Pong server (TCP): replies with n+1.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9000, help="Port to listen on (default: 9000)")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((args.host, args.port))
        server.listen(5)
        server.settimeout(1.0)  # accept() blockiert nicht unendlich

        print(f"Pong server listening on {args.host}:{args.port}")

        try:
            while True:
                try:
                    conn, addr = server.accept()
                except socket.timeout:
                    continue  # loop zurück, Ctrl+C

                with conn:
                    line = recv_line(conn)

                    try:
                        n = int(line)
                    except ValueError:
                        continue

                    conn.sendall(f"{n + 1}\n".encode("utf-8"))

        except KeyboardInterrupt:
            print("\nServer stopped cleanly")


if __name__ == "__main__":
    main()

# "getestet und funktioniert"
# "Starten des Pong Servers durch diesen Befehl: "py Code\pong_server.py --host 127.0.0.1 --port 9000"