# Fuzzy-Logic Game AI Controller

Ein interaktives Streamlit-Projekt zur Visualisierung und Steuerung von KI-Entscheidungen mittels Fuzzy-Logic.

---

## Projektstruktur

```txt
src/
├── main.py
├── config.py
├── modules/
│   ├── membership_function.py             # (Konkrete MF-Funktionen wie trap_mf, tri_mf, bell_mf)
│   └── fuzzy_logic/
│       ├── membership_function.py         # Wrapper: MembershipFunction
│       ├── fuzzy_variable.py
│       ├── fuzzy_rule.py
│       ├── fuzzy_controller.py
│       └── defuzzifier.py
├── utils/
│   └── ui_helper.py
```

---

## Schnellstart

1. **Repository klonen**

   ```bash
   git clone https://github.com/DominikHommer/FuzzyLogic
   cd FuzzyLogic
   ```


2. **Virtuelle Umgebung erstellen (empfohlen)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate     # Für Linux/Mac
   # .venv\Scripts\activate      # Für Windows (cmd)
   # .venv\Scripts\Activate.ps1  # Für Windows (PowerShell)
   ```

3. **Abhängigkeiten installieren**

   ```bash
   pip install -r requirements.txt
   ```

4. **App starten**

   ```bash
   streamlit run src/main.py
   ```

5. Der Browser öffnet automatisch `http://localhost:8501`.


---

## Modulüberblick

**modules/fuzzy\_logic/**

* **membership\_function.py:**
  Enthält die Klasse `MembershipFunction` (Wrapper für Funktionen, die x → μ(x) ∈ \[0,1] abbilden).

* **fuzzy\_variable.py:**
  Definiert `FuzzyVariable` für linguistische Variablen.

  * `name`: z. B. "Health"
  * `terms`: Dict Label → MembershipFunction
  * `domain`: Wertebereich (z. B. (0,100))

* **fuzzy\_rule.py:**
  Definiert `FuzzyRule` für IF-THEN-Regeln

  * `antecedents`: Liste von (var\_name, term\_label)
  * `consequent`: (var\_name, term\_label)

* **fuzzy\_controller.py:**
  Steuert das gesamte Fuzzy-Inferenzsystem:

  * Fuzzification
  * Rule Evaluation (Min-AND)
  * Aggregation (Max-OR)
  * Defuzzification (z. B. centroid, min\_of\_max, etc.)

* **defuzzifier.py:**
  Statische Methoden für verschiedene Defuzzifizierungsstrategien.

**modules/membership\_function.py:**
Implementiert konkrete MF-Generatoren (`trap_mf`, `tri_mf`, `bell_mf`), die den Wrapper aus `fuzzy_logic/membership_function.py` verwenden.

**utils/ui\_helper.py:**
Hilfsfunktionen für UI (z. B. dynamische Erstellung von Membership Functions über die Oberfläche).

**config.py:**
Zentrale Konfiguration von MF-Typen, Labels, Domains, Default-Parametern und Hilfetexten für die UI.

---

## Funktionsweise der App

1. **Eingabe & Konfiguration**

   * Slider für **Health**, **Enemy Count** und **Distance**
   * Auswahl der Defuzzification-Methode
   * **Dynamische Auswahl und Parametrisierung** aller Membership Functions (inkl. Hilfetext)
   * **Regel-Editor**: Regeln mit beliebigen Kombinationen von Bedingungen anlegen, Duplikate werden verhindert, Set jederzeit editierbar

2. **Visualisierung**

   * Plots der Input-Membership Functions (mit aktuellem Wert)
   * Für jede ausgelöste Regel: Clipped Output-Plot (Regelstärke)
   * Darstellung der Output-MFs
   * Aggregiertes Output-Set & Defuzzifizierte Linie

3. **Ergebnisdarstellung**

   * Tabelle der aggregierten Zugehörigkeiten
   * **Crisp Command** (Textausgabe: "ANGRIFF", "VERTEIDIGUNG", "RÜCKZUG")

     ```python
     cmd = (
         'ANGRIFF'      if def_val >= 66 else
         'VERTEIDIGUNG' if def_val >= 34 else
         'RÜCKZUG'
     )
     ```

