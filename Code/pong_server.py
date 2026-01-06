import argparse
import socket

# Liest aus einer TCP Verbindung bis ein Zeilenende erreicht ist
# TCP ist ein Bytestream, daher wird das Zeilenende als Nachrichtenbegrenzer genutzt
def recv_line(conn: socket.socket) -> str:
    buf = b""
    while b"\n" not in buf:
        chunk = conn.recv(1024)
        if not chunk:
            # Client hat die Verbindung geschlossen
            break
        buf += chunk

    # Erste Zeile extrahieren und in Text umwandeln
    return buf.split(b"\n", 1)[0].decode("utf-8", errors="replace").strip()


def main() -> None:
    # Definition der Kommandozeilenargumente
    parser = argparse.ArgumentParser(
        description="Basic Pong Server (TCP): antwortet mit n+1"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Adresse, auf der der Server lauscht",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9000,
        help="Port, auf dem der Server lauscht",
    )

    # Argumente einlesen und validieren
    args = parser.parse_args()

    # TCP Server Socket erstellen
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Erlaubt sofortiges Wiederverwenden des Ports nach Neustart
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Socket an Host und Port binden
        server.bind((args.host, args.port))

        # Server in den Listen-Modus versetzen
        server.listen(5)

        # Timeout verhindert dauerhaft blockierendes accept()
        server.settimeout(1.0)

        print(f"Pong Server läuft auf {args.host}:{args.port}")

        try:
            # Endlosschleife zur Annahme neuer Clients
            while True:
                try:
                    # Wartet auf eine eingehende TCP Verbindung
                    conn, addr = server.accept()
                except socket.timeout:
                    # Kein Client, Schleife erneut durchlaufen
                    continue

                # Bearbeitung genau eines Clients
                with conn:
                    # Eine Zeile vom Client lesen
                    line = recv_line(conn)

                    # Prüfen, ob eine Ganzzahl empfangen wurde
                    try:
                        n = int(line)
                    except ValueError:
                        # Ungültige Eingabe wird ignoriert
                        continue

                    # Antwort senden: n + 1
                    conn.sendall(f"{n + 1}\n".encode("utf-8"))

        except KeyboardInterrupt:
            # Beenden des Servers mit Ctrl+C
            print("\nServer sauber beendet")


if __name__ == "__main__":
    # Startpunkt des Programms
    main()
