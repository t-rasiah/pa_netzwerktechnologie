import argparse
import socket
import time

# Prüft Transportfehler, Datentypfehler und logische Fehler

def parse_reply(text: str):
    # Zerlegt und kontrolliert die Serverantwort
    parts = text.strip().split()

    # Antwort muss genau zwei Felder enthalten
    if len(parts) != 2:
        return None

    resp_id, value_str = parts

    # Wert muss eine Ganzzahl sein
    try:
        value = int(value_str)
    except ValueError:
        return None

    return resp_id, value


def main() -> None:
    # Kommandozeilenargumente definieren
    parser = argparse.ArgumentParser(
        description="UDP Ping Client mit Timeout, Retry und Validierung"
    )
    parser.add_argument("--host", default="127.0.0.1")  # Serveradresse
    parser.add_argument("--port", type=int, default=9004)  # Serverport
    parser.add_argument("--n", type=int, required=True)  # Ping-Wert
    parser.add_argument("--id", type=int, default=1)  # Request-ID
    parser.add_argument("--timeout", type=float, default=0.5)  # Timeout pro Versuch
    parser.add_argument("--retries", type=int, default=3)  # Anzahl Wiederholungen

    # Argumente auswerten
    args = parser.parse_args()

    # Erwartete korrekte Antwort
    expected_value = args.n + 1

    # Request-ID als String
    req_id = str(args.id)

    # UDP Payload erzeugen
    payload = f"{req_id} {args.n}\n".encode("utf-8")

    # UDP Socket erstellen
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Timeout für recvfrom setzen
        s.settimeout(args.timeout)

        # Retry-Schleife
        for attempt in range(1, args.retries + 1):
            # Ping senden
            s.sendto(payload, (args.host, args.port))

            try:
                # Innerhalb eines Versuchs auf passende Antworten warten
                while True:
                    data, _ = s.recvfrom(4096)
                    text = data.decode("utf-8", errors="replace")

                    # Antwort
                    parsed = parse_reply(text)
                    if not parsed:
                        # wenn ungültiges Format oder falscher Datentyp
                        break

                    resp_id, value = parsed

                    # Antwort gehört nicht zu diesem Request
                    if resp_id != req_id:
                        continue

                    # Logischer Fehler: falsche Zählung
                    if value != expected_value:
                        raise SystemExit(
                            f"Falsche Antwort: erwartet {expected_value}, erhalten {value}"
                        )

                    # Korrekte Antwort erhalten
                    print(value)
                    return

            except socket.timeout:
                # Timeout u nächster Versuch
                pass

            # Kurze Pause zwischen Versuchen
            time.sleep(0.05)

    # Alle Versuche fehlgeschlagen
    raise SystemExit(
        f"Timeout: keine gültige Antwort nach {args.retries} Versuchen"
    )


if __name__ == "__main__":
    main()
