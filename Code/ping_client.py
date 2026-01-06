import argparse
import socket

# Liest Daten aus einem TCP Socket bis ein Zeilenende erreicht ist
# TCP ist ein Bytestream, deshalb muss die Nachricht selbst abgegrenzt werden
def recv_line(sock: socket.socket) -> str:
    buf = b""
    while b"\n" not in buf:
        chunk = sock.recv(1024)
        if not chunk:
            # Verbindung wurde vom Server geschlossen
            break
        buf += chunk

    # Extrahiert die erste Zeile und wandelt Bytes in Text um
    return buf.split(b"\n", 1)[0].decode("utf-8", errors="replace").strip()


def main() -> None:
    # Definition der Kommandozeilenargumente
    parser = argparse.ArgumentParser(
        description="Basic Ping Client (TCP): sendet n und erwartet n+1"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Adresse des Pong Servers",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9000,
        help="Port des Pong Servers",
    )
    parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Zu sendender Ping Wert",
    )

    # Einlesen und Validieren der Argumente
    args = parser.parse_args()

    # Aufbau einer TCP Verbindung zum Server
    # Timeout verhindert endloses Blockieren, falls der Server nicht erreichbar ist
    with socket.create_connection((args.host, args.port), timeout=5) as s:
        # Senden des Ping Wertes als Zeile
        s.sendall(f"{args.n}\n".encode("utf-8"))

        # Lesen der Antwortzeile vom Server
        reply = recv_line(s)

    # Ausgabe der Antwort (sollte n+1 sein)
    print(reply)


if __name__ == "__main__":
    # Startpunkt des Programms
    main()
