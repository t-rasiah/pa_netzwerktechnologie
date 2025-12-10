#!/usr/bin/env python3
import socket
import threading

HOST = "0.0.0.0"   # auf allen Interfaces lauschen
PORT = 5000        # Port frei wählbar

# Menge aller verbundenen Clients (Sockets)
clients = set()
clients_lock = threading.Lock()


def broadcast(message: str, sender_socket: socket.socket | None = None):
    """Sende message an alle Clients (außer optional dem Sender)."""
    with clients_lock:
        dead_clients = []
        for client in clients:
            if client is sender_socket:
                continue
            try:
                client.sendall(message.encode("utf-8") + b"\n")
            except OSError:
                # Client ist vermutlich weg
                dead_clients.append(client)

        # Tote Clients aufräumen
        for dc in dead_clients:
            clients.remove(dc)


def handle_client(sock: socket.socket, addr):
    """Behandelt einen einzelnen Client in einem eigenen Thread."""
    print(f"[INFO] Neuer Client verbunden: {addr}")

    with clients_lock:
        clients.add(sock)

    try:
        sock.sendall(b"[SERVER] Willkommen im Chat!\n")

        # Haupt-Loop für eingehende Nachrichten
        while True:
            data = sock.recv(1024)
            if not data:
                # Verbindung wurde geschlossen
                break

            text = data.decode("utf-8").strip()
            if not text:
                continue

            # Nachricht an alle anderen broadcasten
            msg = f"[{addr[0]}:{addr[1]}] {text}"
            print(msg)  # auf Server-Konsole
            broadcast(msg, sender_socket=sock)

    except ConnectionError:
        pass
    finally:
        # Client entfernen und alle informieren
        with clients_lock:
            if sock in clients:
                clients.remove(sock)
        sock.close()
        info = f"[SERVER] {addr} hat den Chat verlassen."
        print(info)
        broadcast(info)


def main():
    """Startet den Server und akzeptiert neue Clients."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()

        print(f"[INFO] Chat-Server läuft auf {HOST}:{PORT}")

        while True:
            client_sock, addr = server_sock.accept()
            # Für jeden Client einen Thread starten
            t = threading.Thread(
                target=handle_client, args=(client_sock, addr), daemon=True
            )
            t.start()


if __name__ == "__main__":
    main()
