import argparse
import socket


def main() -> None:
    parser = argparse.ArgumentParser(description="UDP Pong server: replies with n+1.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9001)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((args.host, args.port))
        s.settimeout(1.0)  # delay check for beenden
        print(f"UDP Pong server listening on {args.host}:{args.port}")

        try:
            while True:
                try:
                    data, addr = s.recvfrom(4096)
                except socket.timeout:
                    continue  # check again for Ctrl+C

                text = data.decode("utf-8", errors="replace").strip()
                try:
                    n = int(text)
                except ValueError:
                    continue

                s.sendto(f"{n + 1}\n".encode("utf-8"), addr)

        except KeyboardInterrupt:
            print("\nServer stopped cleanly")


if __name__ == "__main__":
    main()