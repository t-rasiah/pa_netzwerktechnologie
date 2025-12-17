# Projekt Ping Pong (Level 1)

---
Dieses Projekt implementiert ein einfaches, aber erweiterbares **Ping-Pong-Protokoll** in Python auf Basis von **UDP und/oder TCP**.  
Ein *Ping*-Client sendet eine Zahl (den sogenannten *Spin*) an einen *Pong*-Server, welcher darauf mit einer modifizierten Antwort reagiert.  
Das Projekt ist modular aufgebaut, sodass jede Erweiterung separat (z. B. in einer eigenen Datei) umgesetzt werden kann.



---

## Funktionen
Das Projekt umfasst folgende Funktionen und Erweiterungen:

### Basic Ping-Pong
- Ein Ping sendet eine Zahl `n` (Spin)
- Der Pong antwortet mit `n + 1`

Die Ping Pong Anwendung besteht aus einem Server und einem "Client"
- `ping_client.py` - Ping Client (TCP)
- `pong_server.py` - Pong Server (TCP)


### Ping-Pong mit UDP
- XX
- `udp_ping_client.py` - Ping Client (UDP)
- `udp_pong_server.py` - Pong Server (UDP)



### Ping-Pong mit Proxy
- Ein Proxy leitet Ping- und Pong-Nachrichten weiter
- Der Spin bleibt unverändert
- Simuliert eine verlängerte Übertragungsstrecke

### Kette von Ping-Pongs
- Mehrere Ping-Pong-Service-Provider (PPSP) sind hintereinandergeschaltet
- Jede Instanz verarbeitet und leitet die Nachricht weiter

### Stern-Topologie
- Statische Stern-Topologie
- Ein zentraler Hub übernimmt das Routing
- Clients kommunizieren ausschließlich über den Hub

### Vermaschte Topologie
- Mesh-Topologie ähnlich dem Internet
- Mehrere gleichberechtigte Ping-Pong-Knoten
- Nachrichten können über verschiedene Pfade weitergeleitet werden

---

## Voraussetzungen
Für die Ausführung des Projekts werden folgende Voraussetzungen benötigt:

- Python **3.11 oder höher**
- Betriebssystem mit Netzwerkunterstützung (Linux, macOS oder Windows)
- Grundlegende Kenntnisse in:
  - Python
  - Netzwerkprogrammierung (UDP/TCP)
  - Kommandozeile

Optionale Tools:
- `git` für Versionsverwaltung und Branches
- Virtuelle Python-Umgebung (venv)

---


## Client starten
> **Hinweis:** Dieser Abschnitt dient als Vorlage und wird später ergänzt.

Beispielhafter Start eines Ping-Client:

>`ping_server.py`



---

## Server starten
> **Hinweis:** Dieser Abschnitt dient als Vorlage und wird später ergänzt.

Beispielhafter Start eines Pong-Servers:

>`pong_server.py`