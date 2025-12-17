import argparse, socket, time

def recv_line(s):
    buf = b""
    while b"\n" not in buf:
        c = s.recv(1024)
        if not c: break
        buf += c
    return buf.split(b"\n", 1)[0] + b"\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lhost", default="127.0.0.1")
    ap.add_argument("--lport", type=int, default=8000)
    ap.add_argument("--phost", default="127.0.0.1")
    ap.add_argument("--pport", type=int, default=9000)
    ap.add_argument("--delay-ms", type=int, default=0)
    a = ap.parse_args()

    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((a.lhost, a.lport))
    srv.listen(5)
    print(f"proxy {a.lhost}:{a.lport} -> {a.phost}:{a.pport}")

    while True:
        c, _ = srv.accept()
        with c:
            line = recv_line(c)
            if a.delay_ms: time.sleep(a.delay_ms/1000)
            with socket.create_connection((a.phost, a.pport), timeout=5) as u:
                u.sendall(line)          # Spin bleibt: unverändert
                c.sendall(recv_line(u))  # Antwort zurück

if __name__ == "__main__":
    main()
