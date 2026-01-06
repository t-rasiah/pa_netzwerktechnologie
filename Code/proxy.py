import argparse
import socket
import time


# Liest aus einer TCP Verbindung bis ein Zeilenende erreicht ist
# TCP ist ein Bytestream, daher wird das Zeilenende als Nachrichtenbegrenzer genutzt
def recv_line(conn: socket.socket) -> str:
    buf = b""
    while b"\n" not in buf:
        chunk = conn.recv(1024)
        if not chunk:
            break
        buf += chunk
    return buf.split(b"\n", 1)[0].decode("utf-8", errors="replace").strip()


# Sendet eine Zeile inklusive Zeilenende
def send_line(conn: socket.socket, text: str) -> None:
    conn.sendall(f"{text}\n".encode("utf-8"))


def main() -> None:
    # Proxy Konfiguration
    # listen_host und listen_port sind die Adresse und der Port, auf dem der Proxy auf Clients wartet
    # target_host und target_port sind die Adresse und der Port des echten Pong Servers
    parser = argparse.ArgumentParser(
        description="TCP Proxy für Ping Pong. Leitet Ping an Pong Server weiter und gibt Pong zurück."
    )
    parser.add_argument("--listen-host", default="127.0.0.1", help="Adresse, auf der der Proxy lauscht")
    parser.add_argument("--listen-port", type=int, default=9005, help="Port, auf dem der Proxy lauscht")
    parser.add_argument("--target-host", default="127.0.0.1", help="Adresse des echten Pong Servers")
    parser.add_argument("--target-port", type=int, default=9000, help="Port des echten Pong Servers")
    parser.add_argument("--delay", type=float, default=0.0, help="Optionale Verzoegerung in Sekunden")
    args = parser.parse_args()

    # TCP Server Socket für den Proxy erstellen
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((args.listen_host, args.listen_port))
        server.listen(5)

        # Timeout verhindert dauerhaft blockierendes accept und macht Ctrl+C zuverlässiger
        server.settimeout(1.0)

        print(
            f"TCP Proxy läuft auf {args.listen_host}:{args.listen_port} "
            f"und leitet weiter an {args.target_host}:{args.target_port}"
        )

        try:
            # Endlosschleife für eingehende Client Verbindungen
            while True:
                try:
                    client_conn, client_addr = server.accept()
                except socket.timeout:
                    continue

                # Pro Verbindung wird genau ein Ping verarbeitet und eine Antwort zurückgegeben
                with client_conn:
                    # Eine Zeile vom Client lesen, erwartet wird eine Zahl als Text
                    ping_line = recv_line(client_conn)
                    if ping_line == "":
                        continue

                    # Optionale Verzoegerung, um die Flugbahn zu verlaengern
                    if args.delay > 0:
                        time.sleep(args.delay)

                    # Verbindung zum echten Pong Server herstellen
                    try:
                        with socket.create_connection(
                            (args.target_host, args.target_port), timeout=5
                        ) as upstream:
                            # Ping unverändert weiterleiten
                            send_line(upstream, ping_line)

                            # Antwort vom Pong Server lesen
                            pong_line = recv_line(upstream)

                    except OSError:
                        # Falls der Pong Server nicht erreichbar ist, wird eine einfache Fehlermeldung zurückgegeben
                        send_line(client_conn, "ERR upstream_unreachable")
                        continue

                    # Optional erneut verzoegern, um Rueckweg zu simulieren
                    if args.delay > 0:
                        time.sleep(args.delay)

                    # Antwort an den Client zurückgeben
                    if pong_line == "":
                        send_line(client_conn, "ERR empty_reply")
                    else:
                        send_line(client_conn, pong_line)

        except KeyboardInterrupt:
            print("\nProxy sauber beendet")


if __name__ == "__main__":
    main()
