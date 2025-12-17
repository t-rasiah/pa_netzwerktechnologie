import argparse
import socket


def recv_line(sock: socket.socket) -> str:
    """lesen bis //n oder connection close."""
    buf = b""
    while b"\n" not in buf:
        chunk = sock.recv(1024)
        if not chunk:
            break
        buf += chunk
    return buf.split(b"\n", 1)[0].decode("utf-8", errors="replace").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Basic Ping client (TCP): sends n, prints n+1.")
    parser.add_argument("--host", default="127.0.0.1", help="Server address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9000, help="Server port (default: 9000)")
    parser.add_argument("--n", type=int, required=True, help="Spin value to send")
    args = parser.parse_args()

    with socket.create_connection((args.host, args.port), timeout=5) as s:
        s.sendall(f"{args.n}\n".encode("utf-8"))
        reply = recv_line(s)

    print(reply)


if __name__ == "__main__":
    main()
