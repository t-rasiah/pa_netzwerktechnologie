import argparse
import socket


def recv_line(conn: socket.socket) -> str:
    """lesen bis //n oder connection close."""
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

        print(f"Pong server listening on {args.host}:{args.port}")

        while True:
            conn, addr = server.accept()
            with conn:
                line = recv_line(conn)

                try:
                    n = int(line)
                except ValueError:
                    # ignore invalid input (KISS)
                    continue

                conn.sendall(f"{n + 1}\n".encode("utf-8"))


if __name__ == "__main__":
    main()
