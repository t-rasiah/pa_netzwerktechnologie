# pa_netzwerktechnologie
# Projektarbeit für Netzwerktechnologie TEKO

Wir haben in dem Modul Netzwerktechnologie den Auftrag erhalten einen Ping-Pong Protokoll in Phyton zu programmieren.
Folgendes wurde uns als Auftrag erteilt. 

## 1 Projekt Ping Pong (Level 1)

**Projektbeschrieb:** Implementiere ein UDP/TCP basierendes Ping-Pong Protokoll
in Python. Ein Ping wird gesendet und mit einem Pong beantwortet.
Jede Erweiterung des Service (siehe unten für die Erweiterung
gen) gibt zusätzliche Punkte (siehe Notenschlüssel). Jeder Erweiterung
in einer separaten Datei oder git branch.

**Note/Punkte:** Siehe oben für grundlegende Notengebung
- Implementation des Basic-Ping-Pong Service : 4-5
- Jedes weitere Feature: +0.3

**Features:** Siehe untenstehende Liste von Ping-pong Services/Architektur

### 1.1.1 Basic Ping-Pong
Ping sendet eine Zahl n (=spin), und Pong antwortet mit n +1

### 1.1.2 Ping-Pong mit UDP Fehlerbehandlung
Manchmal können Daten-Fehler entstehen. Ping-Pong mit Fehlerbehand
lung kann damit umgehen.

### 1.1.3 Ping-Pong mit einem Ping-Pong Proxy
Der proxy nimmt den ping-pong-pall und verlängert die Flugbahn ohne den
Spin zu ändern.

### 1.1.4 Kette von Ping-Pongs
Generalisierung des Ping-Pong-Service: Mehrere PP service provider (PPSP)
bilden eine Kette.

### 1.1.5 Ping-Pong in einer Stern Topologie
Implementiert ein eigene statische Stern Topologie, der Hub mach das Stern
Routing.

### 1.1.6 Ping-Pong in einer vermaschten Topologie
Due to technical diffculties no image is provided.
Consider a Mesh-Topology (like the internet) and implement a meshed
network of ping-pong services on top of it.

Wir werden versuchen dies nach den Vorgaben aufzubauen und möglichst viele Erweiterungen zu implementieren. 

