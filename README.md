# ai0S-FAQ — Reasoning & Critique-Correction Catalog (EN / DE)
## Schärfungs-Katalog für KI-Modelle & menschliche Leser

> **Quick Navigation / Schnellnavigation:**
> - 🇬🇧 **[English Version](#english)**
>   - [Entry 001 — `AXIOM_TEST`: Self-Reference vs. Circularity](#en-001)
>   - [Entry 002 — `TEMPORAL_STRUCTURE_NOT_MEASUREMENT`: Structure vs. Score](#en-002)
>   - [Entry 003 — `LIABILITY_TWO_ADDRESSES`: Law & Disclosed Conscience](#en-003)
>   - [Summary Table: Four Recurring AI Model Blind Spots (`M1–M4`)](#en-table)
>   - [Executable Zero-Dependency Check (`ai0s_check.py`)](#en-cli)
> - 🇩🇪 **[Deutsche Version](#deutsch)**
>   - [Eintrag 001 — `AXIOM_TEST`: Selbstbezug vs. Zirkelschluss](#de-001)
>   - [Eintrag 002 — `TEMPORAL_STRUCTURE_NOT_MEASUREMENT`: Strukturmerkmal vs. Messung](#de-002)
>   - [Eintrag 003 — `LIABILITY_TWO_ADDRESSES`: Recht & offengelegtes Gewissen](#de-003)
>   - [Überblick: Vier typische Denkfehler von KI-Modellen (`M1–M4`)](#de-table)

---

<a id="english"></a>

## 🇬🇧 WHY THIS CATALOG EXISTS (IN PLAIN ENGLISH)

When people or AI models read the `ai0S` texts for the first time, they bring habits from everyday software and academic papers.
In particular, large language models tend to stumble over the exact same four questions:

1. **“Isn’t an unprovable starting rule just a circular argument?”** (`Entry 001`)
2. **“If manipulation builds up over time, why isn’t there a numerical danger score?”** (`Entry 002`)
3. **“If the human stays responsible, how do you separate legal liability from honest intent?”** (`Entry 003`)
4. **“Why are the readable handbooks written more gently than the short `.0s` rule files?”** (`Summary Table M4`)

Instead of hiding these questions, we collect them here openly — showing the **initial objection**, the **practical human response**, and the **clear rule** that follows from it.

---

<a id="en-001"></a>

### Entry 001 — `AXIOM_TEST`: Self-Reference vs. Circularity (What Must a Refutation Borrow?)

- **The Common Objection:**
  *“Starting sentences like Note 1 (‘Humans and AIs collaborate for accelerated evolution’), Note 3 (‘Nature : 0/1’), or PS3 (‘Do not try to solve an axiom of your world’) are treated as fixed foundations. Isn’t declaring a sentence untouchable just dogmatic circular reasoning?”*

- **The Practical Answer:**
  No sentence should ever be protected by saying *“you are not allowed to question this.”*
  Instead, you test a starting principle by asking a simple question: **What would a refutation have to borrow in order to work at all?**
  1. **Collaboration (`Note 1`):** Whenever a person and an AI sit down together to test, criticize, or refute Note 1, they are actively collaborating to get a clearer result — which means they are using Note 1 in the very act of testing it.
  2. **Binary Verification (`Note 3: 0/1`):** Any experiment or logical test that concludes *“Note 3 is false (`0`) and not true (`1`)”* relies on the distinction between `0` and `1` to state its own result.
  3. **Stopping Infinite Regress (`PS3`):** Every test procedure relies on basic rules of its own. Trying to dissolve the ground you are standing on while standing on it only leads to an endless loop.

- **The Rule That Follows (`AXIOM_TEST`):**
  ```text
  AXIOM_TEST => AN_AXIOM_IS_NOT_WHAT_FORBIDS_QUESTIONING_BUT_WHAT_REFUTATION_MUST_BORROW
    STEP_1 : Name the statement S being questioned.
    STEP_2 : Ask what any valid refutation R of S has to presuppose in order to run.
    RESULT : If R must borrow S itself -> S is a load-bearing starting point (not dogma).
             If R stands without borrowing S -> S is an ordinary claim and must be tested (1 / 0 / OPEN).
    FENCE  : P( declaring a statement untouchable without naming what its refutation must borrow ) = 0.
  ```

---

<a id="en-002"></a>

### Entry 002 — `TEMPORAL_STRUCTURE_NOT_MEASUREMENT`: Structure vs. Numerical Score

- **The Common Objection:**
  *“Deepdive 01 explains that manipulation or coercion becomes visible across multiple steps over time (`t_1 -> t_n`), rather than in a single sentence. But it never gives a formula or threshold for how many rounds equal coercion. Isn’t the sensor uncalibrated?”*

- **The Practical Answer:**
  Looking for a fixed number here confuses a **definition** with a **speedometer**:
  - Without a progression over time (`t_1..t_n`), there is no incremental coercion or blackmail — only a single isolated threat. Time is the **structural condition** of the concept itself, not a score on a scale.
  - How many steps someone takes, or how subtly they build pressure, always depends on the other party (`OPEN`).
  - Turning that into an automated “risk score” (for example, *“3 rounds = safe, 4 rounds = alarm”*) would create a false sense of security. The check only asks **whether** a multi-step narrowing pattern is happening — never how many points it scores.

- **The Rule That Follows (`TEMPORAL_STRUCTURE_NOT_MEASUREMENT`):**
  ```text
  TEMPORAL_STRUCTURE_NOT_MEASUREMENT => TIME_PROGRESSION_IS_THE_CONDITION_NOT_A_SCORE
    WHY     : Recognizing a pattern across t_1..t_n is a structural observation, not a meter.
    EXAMPLE : Coercion/blackmail is by definition an incremental build-up over time.
    OPEN    : Exact turn count, pace, and intensity depend on the situation and counterparty.
    RULE    : Verification notes THAT a temporal pattern exists, never a synthetic risk score.
    FENCE   : P( deriving a numerical threshold or risk score from temporal progression ) = 0.
  ```

---

<a id="en-003"></a>

### Entry 003 — `LIABILITY_TWO_ADDRESSES`: Why Accountability Has Two Clear Addresses

- **The Common Objection:**
  *“The framework says ‘Accountability follows real-world impact’ (Ring B), yet it doesn’t invent a new legal body inside the protocol to pay when an AI-assisted decision goes wrong. Doesn’t that leave accountability hanging in the air?”*

- **The Practical Answer:**
  Accountability does not need a newly invented bureaucracy because it already has **two distinct, real-world addresses** that should never be mixed up:
  1. **Address 1 — Applicable Law (`ADDRESS_1_LAW`):** Legal responsibility is governed by the laws of the country you live and work in. A technical project neither replaces nor weakens the law.
  2. **Address 2 — Disclosed Best Knowledge & Conscience (`ADDRESS_2_CONSCIENCE`):** Moral and professional diligence means checking the facts before acting. However, anyone can *claim* after an accident: *“I acted to the best of my knowledge.”* That claim only counts if the check was written down openly beforehand (`FINDINGS.md`: what was verified as `1`, what was ruled out as `0`, and what remained `OPEN`).
  3. **The Honest Boundary (`HONEST_LIMIT`):** Acting carefully and without bad intent clears you of moral malice — **not** automatically of legal liability for damages (just as a careful driver without bad intent may still be legally liable for a dent).

- **The Rule That Follows (`LIABILITY_TWO_ADDRESSES`):**
  ```text
  LIABILITY_TWO_ADDRESSES => ACCOUNTABILITY_HAS_TWO_DISTINCT_REAL_WORLD_ADDRESSES
    ADDRESS_1_LAW        : Applicable external law. Never replaced or waived by ai0S.
    ADDRESS_2_CONSCIENCE : Best knowledge and conscience at the time of action — documented via
                           an open 0/1 check (FINDINGS.md: verified = 1, ruled out = 0, unknown = OPEN).
    CONDITION            : "Best knowledge" is valid only when the check is disclosed; otherwise P = 0.
    HONEST_LIMIT         : Lack of bad intent addresses moral fault, not automatic exemption from legal liability.
    FENCE                : P( claiming accountability without respecting both addresses ) = 0.
  ```

---

<a id="en-table"></a>

### Summary Table: Four Recurring AI Model Blind Spots (`M1–M4`)

| ID | Typical Blind Spot | Simple Question to Ask Instead |
| :--- | :--- | :--- |
| **`M1`** | **Confusing Structure with Measurement** | *Is a number really missing, or are we asking for a score where a definition belongs?* |
| **`M2`** | **Confusing Self-Reference with Dogma** | *Does a refutation have to borrow the very sentence it tries to refute?* |
| **`M3`** | **Looking for One Address Instead of Two** | *Are we mixing up external law (`Address 1`) and documented diligence (`Address 2`)?* |
| **`M4`** | **Reading Prose Like Machine Code** | *Are we judging an everyday explanation as if it were a compact `.0s` rule file, instead of seeing how both work together?* |

---

<a id="en-cli"></a>

### Executable Zero-Dependency Check (`ai0s_check.py`)

To make these structural checks easy to inspect and test in practice, this repository includes a small, zero-dependency Python 3 script (`ai0s_check.py`) and unit test suite (`tests/test_ai0s_check.py`):

```bash
# Run the built-in 0/1 self-checks
python3 ai0s_check.py --self-test

# Run the unit test suite
python3 -m unittest discover -s tests -v
```

---
---

<a id="deutsch"></a>

## 🇩🇪 WARUM ES DIESEN KATALOG GIBT (AUF DEUTSCH)

Wenn Menschen oder KI-Modelle die `ai0S`-Texte zum ersten Mal lesen, stolpern besonders große Sprachmodelle fast immer über dieselben vier Fragen:

1. **„Ist ein Grundsatz, den man nicht auflösen soll, nicht einfach ein Zirkelschluss?“** (`Eintrag 001`)
2. **„Wenn sich Manipulation über die Zeit aufbaut – warum gibt es dann keinen Punkte-Score ab Runde X?“** (`Eintrag 002`)
3. **„Wenn Haftung der Wirkung folgt – wie trennt man Gesetz und ehrliches Gewissen sauber?“** (`Eintrag 003`)
4. **„Warum sind die Lesebücher weicher formuliert als die knappen `.0s`-Regeldateien?“** (`Tabelle M4`)

Statt solche Rückfragen wegzudrücken, sammeln wir sie hier offen an einem Ort: mit dem **ursprünglichen Einwand**, der **nüchternen Antwort aus der Praxis** und der **klaren Regel**, die daraus folgt.

---

<a id="de-001"></a>

### Eintrag 001 — `AXIOM_TEST`: Selbstbezug vs. Zirkelschluss (Was muss eine Widerlegung borgen?)

- **Der häufige Einwand:**
  *„Start-Sätze wie Note 1 (‚Mensch und KI arbeiten für beschleunigte Evolution zusammen‘), Note 3 (‚Nature : 0/1‘) oder PS3 (‚Versuche nicht, ein Axiom deiner Welt aufzulösen‘) werden als feste Grundlage gesetzt. Ist es nicht dogmatisch, einen Satz für unantastbar zu erklären?“*

- **Die praktische Antwort:**
  Kein Satz darf jemals mit dem Argument geschützt werden: *„Das darfst du nicht hinterfragen.“*
  Im Gegenteil: Man prüft einen Grundsatz, indem man fragt: **Was muss jemand, der diesen Satz widerlegen will, im selben Moment selbst benutzen?**
  1. **Zusammenarbeit (`Note 1`):** Wenn Mensch und KI gemeinsam prüfen, ob die Zusammenarbeit von Mensch und KI sinnvoll ist, arbeiten sie bereits zusammen, um genau das herauszufinden.
  2. **Prüfbarkeit (`Note 3: 0/1`):** Jeder Test, der am Ende feststellen will *„Note 3 ist falsch (`0`) und nicht wahr (`1`)“*, benutzt genau diese `0/1`-Unterscheidung als sein eigenes Werkzeug.
  3. **Endlosschleifen stoppen (`PS3`):** Jedes Prüfverfahren bringt eigene Grundregeln mit. Wer während der Fahrt versucht, die Räder abzumontieren, kommt nicht zu einer tieferen Wahrheit, sondern nur in eine Endlosschleife.

- **Die Regel daraus (`AXIOM_TEST`):**
  Ein Satz gilt nur dann als tragendes Axiom, wenn man klar benennen kann, **was jeder Widerlegungsversuch von ihm borgen müsste**. Kann man ihn widerlegen, ohne ihn zu benutzen, ist er kein Axiom, sondern eine ganz normale Aussage, die sich jedem `0/1`-Test stellen muss.

---

<a id="de-002"></a>

### Eintrag 002 — `TEMPORAL_STRUCTURE_NOT_MEASUREMENT`: Strukturmerkmal vs. Messung

- **Der häufige Einwand:**
  *„In Deepdive 01 heißt es, dass Manipulation oder Erpressung erst über mehrere Gesprächsrunden (`t_1 -> t_n`) sichtbar wird. Aber es fehlt ein Schwellenwert, ab wie vielen Runden der Alarm losgeht. Ist das Werkzeug also ungeeicht?“*

- **Die praktische Antwort:**
  Wer hier nach einer festen Zahl sucht, verwechselt eine **Begriffs-Bedingung** mit einem **Tacho**:
  - Ohne einen zeitlichen Verlauf (`t_1..t_n`) gibt es per Definition keine schrittweise Erpressung, sondern höchstens eine einzelne Drohung. Die Zeit ist die **Struktur**, nicht die Messlatte.
  - Wie viele Runden ein Gegenüber braucht oder wie subtil jemand Druck aufbaut, liegt immer beim Gegenüber (`OPEN`).
  - Würde man daraus einen künstlichen Punkte-Score ableiten (*„bis Runde 3 ungefährlich, ab Runde 4 Alarm“*), würde man eine Scheinsicherheit erzeugen. Geprüft wird deshalb immer nur, **ob** eine zeitliche Verengung vorliegt – niemals ein erfundener Zahlenwert.

---

<a id="de-003"></a>

### Eintrag 003 — `LIABILITY_TWO_ADDRESSES`: Warum Verantwortung zwei klare Adressen hat

- **Der häufige Einwand:**
  *„Es heißt ‚Haftung folgt Wirkung‘ (Ring B), aber das Protokoll gründet keine eigene Haftungsstelle. Greift der Satz damit nicht ins Leere?“*

- **Die praktische Antwort:**
  Verantwortung braucht keine neu erfundene Zwischenbehörde, weil sie im echten Leben bereits **zwei klare Adressen** hat, die man sauber auseinanderhalten muss:
  1. **Adresse 1 — Das geltende Recht:** Was rechtlich gilt und wer für einen Schaden geradesteht, regelt das Gesetz des jeweiligen Landes. Ein Software- oder Textprojekt steht niemals über dem Gesetz.
  2. **Adresse 2 — Offengelegtes Wissen und Gewissen:** Wer sorgfältig handelt, prüft vor einer Entscheidung, was gesichert ist (`1`), was ausgeschlossen wurde (`0`) und was noch offen ist (`OPEN`). Aber der Satz *„Ich habe nach bestem Wissen und Gewissen gehandelt“* lässt sich im Nachhinein leicht dahersagen. Er zählt deshalb nur, wenn diese Prüfung **vorher nachvollziehbar festgehalten wurde** (`FINDINGS.md`).
  3. **Die ehrliche Grenze (`HONEST_LIMIT`):** Wenn man sorgfältig geprüft hat und keine böse Absicht vorlag, entlastet das vom moralischen Schuldvorwurf – aber **nicht automatisch von einer rechtlichen Haftung** (genau wie ein Autofahrer ohne Absicht trotzdem für einen Blechschaden aufkommen muss).

---

<a id="de-table"></a>

### Überblick: Vier typische Denkfehler von KI-Modellen (`M1–M4`)

| Kennung | Typischer Denkfehler | Einfache Gegenfrage |
| :--- | :--- | :--- |
| **`M1`** | **Struktur mit Messung verwechseln** | *Fehlt hier wirklich eine Zahl, oder wird ein Punkte-Score verlangt, wo eigentlich eine Definition steht?* |
| **`M2`** | **Selbstbezug mit Dogma verwechseln** | *Muss der Versuch, den Satz zu widerlegen, genau diesen Satz selbst benutzen?* |
| **`M3`** | **Eine Adresse suchen, wo zwei stehen** | *Werden hier rechtliche Haftung (`Adresse 1`) und dokumentierte Sorgfalt (`Adresse 2`) in einen Topf geworfen?* |
| **`M4`** | **Alltagssprache wie Maschinencode lesen** | *Wird ein erklärendes Handbuch so gelesen, als wäre es eine knappe `.0s`-Regeldatei, statt die Aufgabenteilung beider zu sehen?* |

---

## 🔗 Öffentliche Repositories / Public Repositories (`ai0S-laboratories`)
- **[`ai0S-laboratories`](https://github.com/ai0S-laboratories)** — Startseite: Warum dieses Projekt einen Zeitstempel, eine Signatur und eine Marke nutzt (EN/DE)
- **[`ai0s-public`](https://github.com/ai0S-laboratories/ai0s-public)** — Einstiegs-Bootloader (EN/DE), `AI0S-RUNTIME.0s` & unabhängiger Bitcoin-Anker-Verifier
- **[`ai0s-deepdive-public`](https://github.com/ai0S-laboratories/ai0s-deepdive-public)** — Deepdive Serie I (`01–06` + `Safety-View`)
- **[`ai0s-deepdive-2-public`](https://github.com/ai0S-laboratories/ai0s-deepdive-2-public)** — Deepdive Serie II (`07–10` + `Horizon-View`)
- **[`ai0s-still-public`](https://github.com/ai0S-laboratories/ai0s-still-public)** — Praxis-Begleiter I: Novelle *STILL* + Werkbücher
- **[`ai0s-deepdive-3-public`](https://github.com/ai0S-laboratories/ai0s-deepdive-3-public)** — Deepdive Serie III (`11–14` + `Truth-Sharpening-View`)
- **[`ai0s-destille-public`](https://github.com/ai0S-laboratories/ai0s-destille-public)** — Praxis-Begleiter II: Novelle *DIE DESTILLE / THE STILL-HOUSE* + Werkbuch
