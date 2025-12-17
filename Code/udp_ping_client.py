import argparse
import socket


def main() -> None:
    parser = argparse.ArgumentParser(description="UDP Ping client: sends n, prints n+1.")
    parser.add_argument("--host", default="127.0.0.1", help="Server address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9001, help="Server port (default: 9001)")
    parser.add_argument("--n", type=int, required=True, help="Spin value to send")
    parser.add_argument("--timeout", type=float, default=2.0, help="Receive timeout in seconds (default: 2.0)")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(args.timeout)
        s.sendto(f"{args.n}\n".encode("utf-8"), (args.host, args.port))

        data, _ = s.recvfrom(4096)
        print(data.decode("utf-8", errors="replace").strip())


if __name__ == "__main__":
    main()
