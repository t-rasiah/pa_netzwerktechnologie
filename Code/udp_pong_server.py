import argparse
import socket

# Empfängt einen Wert n und antwortet mit n+1 BAsic


def main() -> None:
    # Definition der Kommandozeilenargumente
    parser = argparse.ArgumentParser(
        description="UDP Pong Server: antwortet mit n+1"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Adresse, auf der der Server lauscht",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9001,
        help="Port, auf dem der Server lauscht",
    )

    # Argumente einlesen und validieren
    args = parser.parse_args()

    # UDP Socket erstellen
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Socket an Host und Port binden
        s.bind((args.host, args.port))

        # Timeout verhindert endloses Blockieren bei recvfrom
        # und ermöglicht sauberes Beenden mit Ctrl+C
        s.settimeout(1.0)

        print(f"UDP Pong Server läuft auf {args.host}:{args.port}")

        try:
            # Endlosschleife für eingehende UDP Pakete
            while True:
                try:
                    # Empfängt genau ein UDP Datagramm
                    data, addr = s.recvfrom(4096)
                except socket.timeout:
                    # Kein Paket empfangen, Schleife erneut durchlaufen
                    continue

                # Empfangene Bytes in Text umwandeln
                text = data.decode("utf-8", errors="replace").strip()

                # Prüfen, ob eine Ganzzahl empfangen wurde
                try:
                    n = int(text)
                except ValueError:
                    # Ungültige Eingabe wird ignoriert
                    continue

                # Antwort senden: n + 1
                s.sendto(f"{n + 1}\n".encode("utf-8"), addr)

        except KeyboardInterrupt:
            # Sauberes Beenden des Servers mit Ctrl+C
            print("\nServer sauber beendet")


if __name__ == "__main__":
    # Startpunkt des Programms
    main()
