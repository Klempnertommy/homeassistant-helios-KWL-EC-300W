# homeassistant-helios-KWL-EC-300W

Eine maßgeschneiderte Smart-Home-Erweiterung für die Lüftungsanlage **Helios KWL EC 300W (Firmware V2.x)** zur nahtlosen Integration in **Home Assistant**.

Dieses Projekt entstand in stundenlanger, intensiver Entwicklungs- und Testarbeit durch mich, einem erfahrenen Heizungs- und Lüftungsbaumeister und hilfreicher KI Unterstützung.
Es hebelt die träge, fehlerhafte Werkslogik des Herstellers aus und ermöglicht die uneingeschränkte, automatisierte Kontrolle über den Sommer-/Winter-Bypass sowie externe Erweiterungsmodule (z. B. EM-Modul mit T6-Heizregisterfühler).

---

## ⚠️ HAFTUNGSAUSSCHLUSS (Disclaimer)
**Nutzung auf eigene Gefahr!** Dies ist ein privates Open-Source-Projekt. Der Entwickler übernimmt keinerlei Haftung für Schäden an der Lüftungsanlage, der Elektronik, dem Gebäude oder für Folgeschäden (z. B. durch falsche Kondensatbildung oder fehlerhafte Registerwerte). Das Projekt wird "wie besehen" bereitgestellt. Jede Modifikation an einer 4.000€-Anlage geschieht in vollkommener Eigenverantwortung des Nutzers.

---

## 🚀 Features
* **Bypass-Direktsteuerung:** Zuverlässiges Öffnen und Schließen der Klappe über das Register `v01035` – komplett ohne die berüchtigten Firmware-Hysteresen und RAM-Sperren.
* **Intelligente Sommer-Kühlung:** Home Assistant steuert die Anlage dynamisch. Es holt nachts automatisch kühle Luft ins Haus und schaltet tagsüber auf Hitzeschutz (Kälterückgewinnung).
* **Automatischer Lüfter-Boost:** Kopplung von Klappe und Ventilatoren (z. B. automatisches Hochregeln auf Stufe 3 bei aktiver Nachtkühlung, bis die Wunschtemperatur erreicht ist).
* **EM-Modul Integration:** Vollständiges Auslesen des T6-Temperaturfühlers nach dem Heizregister.
* **Der "Soft-Reset-Trick":** Dokumentierter Weg, um festgefahrene Helios-Firmware ohne den Gang zum Sicherungskasten per Software direkt im Webinterface freizumachen.

---

## 🛠️ Installationsanleitung

### 1. Das Python-Skript hinterlegen (Auf dem Pi / Home Assistant)
Da die Helios-Firmware V2 über das Netzwerk Text-Strings (z. B. `"v01035=18\0"`) anstelle von reinen Zahlenwerten erwartet, kann die Standard-Modbus-Integration von Home Assistant nicht direkt genutzt werden. Die Datei `helios_modbus.py` arbeitet als unverzichtbarer Dolmetscher.

1. Lade die Datei `helios_modbus.py` aus diesem Repository herunter.
2. Kopiere die Datei in das `/config/`-Verzeichnis deiner Home Assistant Installation (z. B. via Samba Share oder File Editor).
3. *Hinweis:* Das Skript benötigt das Python-Paket `pymodbus`. In modernen Home Assistant Core/OS-Umgebungen ist dieses für die Befehlszeile meist bereits vorhanden.

### 2. Die Home Assistant Helfer (Input-Elemente) anlegen
Bevor du die YAML-Dateien einspielst, müssen in Home Assistant über die Benutzeroberfläche (**Einstellungen -> Geräte & Dienste -> Helfer -> + Helfer erstellen**) folgende Elemente angelegt werden:

1. **Dropdown (Input Select):**
   * **Name:** `KWL Bypass Modus`
   * **Entitäts-ID:** `input_select.kwl_bypass_modus`
   * **Optionen (Exakte Schreibweise!):**
     * `Werkseinstellung (Helios-Auto)`
     * `Winterbetrieb (HA-Heizen)`
     * `Zwangsschaltung (Bypass AUF)`
     * `Zwangsschaltung (Bypass ZU)`
     * `Sommerbetrieb (HA-Kühlen)`

2. **Nummer (Input Number):** *(Für die spätere Erweiterung der Wunschtemperatur)*
   * **Name:** `KWL Vorgabetemperatur`
   * **Entitäts-ID:** `input_number.kwl_vorgabetemperatur`
   * **Bereich:** `10` bis `40` (Schrittgröße: `1`)

### 3. Integration in die `configuration.yaml`
Kopiere die Sensor-Abfragen und die `shell_command`-Befehle aus der Beispiel-Datei `configuration.yaml` dieses Repositories in deine eigene Konfiguration. Passe dort ggf. die IP-Adresse (`192.168.1.199`) an deine KWL an.

### 4. Integration in die `automations.yaml`
Kopiere die Steuerungs-Automation aus der `automations.yaml` dieses Repositories in dein Home Assistant. Diese Automation triggert bei jedem Umschalten des Dashboard-Helfers sowie im automatischen 5-Minuten-Takt, um die Temperaturen abzugleichen.

---

## 💡 Der Klempnertommy "Soft-Reset-Trick"
Falls sich die Firmware der Helios bei der wilden Testerei oder durch widersprüchliche Befehle im RAM "verknotet" hat und weder auf HA noch auf Klicks im eigenen Webinterface reagiert (Werte frieren starr ein):
* Navigiere im Helios-Webinterface zur **Passiven Außenluftkühlung**.
* Deaktiviere die Funktion kurzzeitig komplett und aktiviere sie danach wieder.
* **Effekt:** Das Bypass-Subsystem wird auf der Platine augenblicklich stromlos geschaltet und der blockierte RAM-Speicher gelöscht. Die sture Anti-Pendel-Sperre ist sofort aufgehoben, ohne dass man die Sicherung im Haus herausdrehen muss!

---

## 📄 Lizenz
Dieses Projekt ist unter der **MIT-Lizenz** lizenziert – siehe die `LICENSE`-Datei für Details. Der Code darf frei verwendet und modifiziert werden, solange der Urheber-Credit erhalten bleibt.
