# homeassistant-helios-KWL-EC-300W

Eine Smart-Home-Erweiterung für die Lüftungsanlage **Helios KWL EC 300W (Firmware V2.x)** zur Integration in **Home Assistant**.

Dieses projekt ist noch in der Weiterentwicklung.

Dieses Projekt entsteht durch stundenlange, intensive Entwicklungs- und Testarbeit durch mich, einem erfahrenen Heizungs- und Lüftungsbaumeister und KI Unterstützung.
Es umgeht die Werkslogik des Herstellers (Helios) und ermöglicht direkten Zugriff auf alle grundlegende Funktionen die über Parameter erreichbar sind.
Zum Beispiel die Kontrolle über den Sommer-/Winter-Bypass oder auch externe Erweiterungsmodule wie das EM-Modul mit T6-Heizregisterfühler.

---

## ⚠️ HAFTUNGSAUSSCHLUSS (Disclaimer)
**Nutzung auf eigene Gefahr!** Dies ist ein privates Open-Source-Projekt. Der Entwickler übernimmt keinerlei Haftung für Schäden an der Lüftungsanlage, der Elektronik, dem Gebäude oder für Folgeschäden (z. B. durch falsche Kondensatbildung oder fehlerhafte Registerwerte). Das Projekt wird "wie besehen" bereitgestellt. Alle Handlungen liegen in vollkommener Eigenverantwortung des Nutzers.

---

## 🚀 Features aktuell
* **Bypass-Direktsteuerung:** Zuverlässiges Öffnen und Schließen der Klappe über das Register `v01035`.
* **EM-Modul Integration:** Vollständiges Auslesen des T6-Temperaturfühlers nach dem Heizregister.

---

## 🛠️ Installationsanleitung

### 1. Das Python-Skript hinterlegen (Auf dem Pi / Home Assistant)
Da die Helios-Firmware V2 über das Netzwerk Text-Strings (z. B. `"v01035=18\0"`) anstelle von reinen Zahlenwerten erwartet, kann die Standard-Modbus-Integration von Home Assistant nicht direkt genutzt werden. Die Datei `helios_modbus.py` arbeitet als unverzichtbarer Dolmetscher.

1. Lade die Datei `helios_modbus.py` aus diesem Repository herunter.
2. Kopiere die Datei in das `/config/`-Verzeichnis deiner Home Assistant Installation (z. B. via Samba Share oder File Editor).
3. *Hinweis:* Das Skript benötigt das Python-Paket `pymodbus`. In modernen Home Assistant Core/OS-Umgebungen ist dieses für die Befehlszeile meist bereits vorhanden.

### 2. Die Home Assistant Helfer (Input-Elemente) anlegen
Bevor du die YAML-Dateien einspielst, müssen in Home Assistant über die Benutzeroberfläche (**Einstellungen -> Geräte & Dienste -> Helfer -> + Helfer erstellen**) folgende Elemente angelegt werden:
### 2. Die Home Assistant Helfer (Input-Elemente) anlegen
Bevor du die YAML-Dateien einspielst, müssen in Home Assistant über die Benutzeroberfläche (**Einstellungen -> Geräte & Dienste -> Helfer -> + Helfer erstellen**) folgende Elemente angelegt werden:

1. **Dropdown (Input Select) für den globalen Modus:**
   * **Name:** `KWL Globale Kontrolle`
   * **Entitäts-ID:** `input_select.kwl_globaler_modus`
   * **Optionen (Exakte Schreibweise!):**
     * `Gerät entscheidet alles (Auto)`
     * `HA übernimmt die Macht (Hand)`

2. **Dropdown (Input Select) für die Lüfterstufen:**
   * **Name:** `Manuelle Lüfterstufe`
   * **Entitäts-ID:** `input_select.kwl_luefterstufe_auswahl`
   * **Optionen (Exakte Schreibweise!):**
     * `Stufe 1 (Minimal)`
     * `Stufe 2 (Normal)`
     * `Stufe 3 (Erhöht)`
     * `Stufe 4 (Stoßlüftung)`

3. **Dropdown (Input Select) - [AKTUELL NUR VORBEREITUNG FÜR UPGRADES]:**
   * **Name:** `KWL Bypass Modus`
   * **Entitäts-ID:** `input_select.kwl_bypass_modus`
   * **Optionen (Exakte Schreibweise!):**
     * `Werkseinstellung (Helios-Auto)`
     * `Winterbetrieb (HA-Heizen)`
     * `Zwangsschaltung (Bypass AUF)`
     * `Zwangsschaltung (Bypass ZU)`
     * `Sommerbetrieb (HA-Kühlen)`
   * *Hinweis:* Dieser Helfer ist für zukünftige Automations-Updates vorbereitet und im aktuellen Basis-Release noch ohne Funktion.

4. **Nummer (Input Number) - [AKTUELL NUR VORBEREITUNG FÜR UPGRADES]:**
   * **Name:** `KWL Vorgabetemperatur`
   * **Entitäts-ID:** `input_number.kwl_vorgabetemperatur`
   * **Bereich:** `10` bis `40` (Schrittgröße: `1`)
   * *Hinweis:* Für spätere Erweiterungen der Wunschtemperatur-Fälschung reserviert.


### 3. Integration in die `configuration.yaml`
Kopiere die Sensor-Abfragen und die `shell_command`-Befehle aus der Beispiel-Datei `configuration.yaml` dieses Repositories in deine eigene Konfiguration. Passe dort ggf. die IP-Adresse (`192.168.1.199`) an deine KWL an.

### 4. Integration in die `automations.yaml`
Kopiere die Steuerungs-Automation aus der `automations.yaml` dieses Repositories in dein Home Assistant. Diese Automation triggert bei jedem Umschalten des Dashboard-Helfers sowie im automatischen 5-Minuten-Takt, um die Temperaturen abzugleichen.

---

## 📄 Lizenz
Dieses Projekt ist unter der **MIT-Lizenz** lizenziert – siehe die `LICENSE`-Datei für Details. Der Code darf frei verwendet und modifiziert werden, solange der Urheber-Credit erhalten bleibt.
