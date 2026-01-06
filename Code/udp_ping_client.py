import argparse
import socket

# UDP Ping Client
# Sendett einen Wert n an den Server und gibt die Antwort aus


def main() -> None:
    # Definition der Kommandozeilenargumente
    parser = argparse.ArgumentParser(
        description="UDP Ping Client: sendet n und erwartet n+1"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Adresse des UDP Pong Servers",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9001,
        help="Port des UDP Pong Servers",
    )
    parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Zu sendender Ping Wert",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=2.0,
        help="Maximale Wartezeit auf eine Antwort in Sekunden",
    )

    # Argumente einlesen und validieren
    args = parser.parse_args()

    # UDP Socket erstellen
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Timeout verhindert endloses Warten auf eine Antwort
        s.settimeout(args.timeout)



        # Ping als einzelnes UDP Datagramm senden
        s.sendto(f"{args.n}\n".encode("utf-8"), (args.host, args.port))

        # Antwort vom Server empfangen
        data, _ = s.recvfrom(4096)

        # Antwort dekodieren und ausgeben
        print(data.decode("utf-8", errors="replace").strip())


if __name__ == "__main__":
    # Startpunkt des Programms
    main()
