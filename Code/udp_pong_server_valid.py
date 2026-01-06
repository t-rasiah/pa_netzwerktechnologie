import argparse
import socket

# Unterstützt absichtlich falsche Antworten zur Demonstration der Client-Validierung

def main() -> None:
    # Kommandozeilenargumente definieren
    parser = argparse.ArgumentParser(
        description="UDP Pong Server mit Request-ID und Testmodi"
    )
    parser.add_argument("--host", default="127.0.0.1")  # Adresse zum Binden
    parser.add_argument("--port", type=int, default=9004)  # Port zum Lauschen

    # Testflags für gezielte Fehlersimulation
    parser.add_argument(
        "--send-text",
        action="store_true",
        help="Antwortet mit Text statt Zahl (falscher Datentyp)",
    )
    parser.add_argument(
        "--wrong-reply",
        action="store_true",
        help="Antwortet mit n+2 statt n+1 (falsche Zählung)",
    )

    # Argumente auswerten
    args = parser.parse_args()

    # UDP Socket erstellen
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Socket an Host und Port binden
        s.bind((args.host, args.port))

        # Timeout verhindert endloses Blockieren und erlaubt sauberes Beenden
        s.settimeout(1.0)

        print(f"UDP Pong Server läuft auf {args.host}:{args.port}")

        try:
            # Endlosschleife für eingehende UDP Pakete
            while True:
                try:
                    # Empfängt genau ein UDP Datagramm
                    data, addr = s.recvfrom(4096)
                except socket.timeout:
                    # Kein Paket erhalten, Schleife fortsetzen
                    continue

                # Bytes in Text umwandeln
                text = data.decode("utf-8", errors="replace").strip()
                parts = text.split()

                # Erwartetes Format: "<id> <n>"
                if len(parts) != 2:
                    continue

                req_id, n_str = parts

                # Prüfen, ob n eine Ganzzahl ist
                try:
                    n = int(n_str)
                except ValueError:
                    continue

                # Testfall: falscher Datentyp
                if args.send_text:
                    reply = f"{req_id} abc\n"

                # Testfall: falsche Zählung
                elif args.wrong_reply:
                    reply = f"{req_id} {n + 2}\n"

                # Normaler korrekter Fall
                else:
                    reply = f"{req_id} {n + 1}\n"

                # Antwort an den Absender senden
                s.sendto(reply.encode("utf-8"), addr)

        except KeyboardInterrupt:
            # Beenden mit Ctrl+C
            print("\nServer sauber beendet")


if __name__ == "__main__":
    main()
