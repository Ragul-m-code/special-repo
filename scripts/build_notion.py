import os
import zipfile
import shutil

def build_notion_package():
    print("--- Building Notion Deliverables ---")
    notion_dir = os.path.join("downloads", "Secret_to_Dream_Notion_Workspace_Files")
    os.makedirs(notion_dir, exist_ok=True)

    # 1. 00_Master_Sanctum_Dashboard.md
    dashboard_md = """# 🏛️ SECRET TO DREAM — SOVEREIGN SANCTUM WORKSPACE
*Confidential Psychological Architecture & Audio Vault // Edition 1130*

> 🗝️ **Sanctum Classification:** Restricted Private Collector Access.
> All frameworks, audio debriefs, and behavioral protocols contained herein are proprietary to the *Secret to Dream* methodology.

---

## ⚡ Quick Navigation
- [Part I: Silent Seduction Playbook](./01_Part_I_Silent_Seduction_Playbook.md)
- [Part II: Voice Vérité Audio Transcripts & Deconstruction](./02_Part_II_Voice_Verite_Psychology.md)
- [Part III: The Modern Siren's Blueprint](./03_Part_III_Modern_Siren_Blueprint.md)
- [Part IV: Obsidian Boundaries & Frame Retention](./04_Part_IV_Obsidian_Protocols.md)
- [Master Audio Vault Database (CSV)](./Audio_Transcripts_and_Vault_Index.csv)
- [Daily Calibration & Habit Tracker (CSV)](./Daily_Protocols_and_Habit_Tracker.csv)

---

## 🧭 The Core Doctrine
1. **The Sovereign Anchor:** Calmness in the face of provocation is the ultimate demonstration of masculine sovereignty.
2. **Vocal Gravity:** The rate at which you speak dictates who controls the emotional state of the room.
3. **The Accessibility Ratio:** 100% presence when physically together; absolute focus on your purpose when apart.
4. **The Obsidian Boundary:** Boundaries stated without anger command immediate subconscious compliance.

---

## 🎯 Daily Operational Checklist
- [ ] Morning Vocal Calibration (Sub-diaphragmatic breathing, 5-minute resonance drill)
- [ ] Posture & Stillness Check (Zero fidgeting, steady unhurried eye contact)
- [ ] Evening Review: Audit conversational dynamic tension and emotional polarity
- [ ] Listen to 1 Voice Vérité Session & complete psychological breakdown
"""

    with open(os.path.join(notion_dir, "00_Master_Sanctum_Dashboard.md"), "w", encoding="utf-8") as f:
        f.write(dashboard_md)

    # 2. 01_Part_I_Silent_Seduction_Playbook.md
    part1_md = """# 📖 Part I: The Silent Seduction Playbook
*Subconscious Dynamics, Vocal Gravity & Stillness*

> "True gravity is not proclaimed; it is felt the instant you enter the room and refuse to seek validation."

### Section 1: The Sovereign Anchor Principle
When a high-caliber woman tests a man, she is not seeking compliance—she is probing for emotional structural integrity. Most men immediately rationalize, apologize, or react emotionally, betraying their internal fragility.
- **Rule 1.1:** Never defend yourself against an emotional projection.
- **Rule 1.2:** Acknowledge the emotion without absorbing the frame: *"I hear what you are saying, and I respect your perspective."*
- **Rule 1.3:** Maintain three seconds of stillness before speaking. This breaks the subconscious cycle of urgency.

### Section 2: Vocal Cadence Calibration
- **Pitch:** Lower 1.5 tones into the chest resonator.
- **Cadence:** 110-120 words per minute during crucial interactions.
- **Downward Inflection:** End statements with a descending tone rather than an inquisitive ascending tone.
- **The Deliberate Pause:** Silence after an important statement forces the other person to fill the psychological vacuum.

### Section 3: Physical Stillness & Eye Calibration
- Fidgeting, excessive nodding, and nervous laughter immediately degrade perceived value.
- Hold eye contact for 1.5 seconds longer than customary before looking away horizontally (never downwards).
- Still hands on table surfaces create an aura of unshakeable calm.
"""

    with open(os.path.join(notion_dir, "01_Part_I_Silent_Seduction_Playbook.md"), "w", encoding="utf-8") as f:
        f.write(part1_md)

    # 3. 02_Part_II_Voice_Verite_Psychology.md
    part2_md = """# 🎙️ Part II: Voice Vérité — 9 Sessions Psychological Deconstruction
*Unedited Late-Night Transcripts & Behavioral Analysis*

> "Behind closed doors, the polite masks come off. These recordings capture raw, unvarnished feminine psychology."

---

### Session 01: The Unspoken Shift
- **Duration:** 02:45
- **Primary Psychological Vector:** Frame test deconstruction & emotional anchoring.
- **Transcript Summary:** "The moment he stopped rushing to answer my texts within seconds, something shifted. It wasn't games—it was the realization that he actually had an entire empire he was building that mattered more than my validation."
- **Core Actionable Principle:** Scarcity must be genuine, rooted in high-value purpose, not manufactured neglect.

---

### Session 02: The Currency of Attention
- **Duration:** 03:12
- **Primary Psychological Vector:** Attention economy & perceived value.
- **Transcript Summary:** "When a man gives away his undivided attention too easily to every compliment, it loses all value. The man whose praise feels earned becomes the only opinion that matters."
- **Core Actionable Principle:** Bestow verbal affirmation as a rare reward, not a baseline greeting.

---

### Session 03: The Stillness Paradox
- **Duration:** 02:58
- **Primary Psychological Vector:** Physical composure during conflict.
- **Transcript Summary:** "We were having an intense disagreement at dinner. He took a sip of his drink, looked me directly in the eyes with a warm, steady smile, and didn't raise his voice by half a decibel. I immediately felt my defensiveness dissolve."
- **Core Actionable Principle:** Physical stillness in argument induces involuntary de-escalation in the counterpart.

---

### Session 04: The Velvet Rope Effect
- **Duration:** 03:20
- **Primary Psychological Vector:** Exclusivity & boundary defense.
- **Transcript Summary:** "The hardest thing to walk away from is a man who lets you know his life is magnificent with or without you. He opened the door to his world, but made it clear that disrespect would close it forever without a scene."
- **Core Actionable Principle:** Clear boundaries enforced without emotional volatility create irresistible psychological respect.

---

### Sessions 05-09: Complete Transcripts Summary
- **Session 05: The Midnight Frequency** — Nocturnal cadence & romantic intimacy pacing.
- **Session 06: The Polarity Engine** — Masculine direction relieves female cognitive load.
- **Session 07: Unspoken Vows** — Private integrity creates outward unshakeable charisma.
- **Session 08: The Seduction of Competence** — Deep immersion in craft without seeking applause.
- **Session 09: The Sovereign Farewell** — The ultimate power: stepping away without resentment.
"""

    with open(os.path.join(notion_dir, "02_Part_II_Voice_Verite_Psychology.md"), "w", encoding="utf-8") as f:
        f.write(part2_md)

    # 4. 03_Part_III_Modern_Siren_Blueprint.md
    part3_md = """# 🍸 Part III: The Modern Siren's Blueprint
*Dynamic Polarity, Seduction Vectors & Tension Calibration*

> "Attraction is an oscillating pendulum between certainty and intrigue. Kill the pendulum, and desire flatlines."

### The Golden Ratio of Accessibility
- **In-Person Dynamic:** 100% focused, tactile, attentive, and grounded. Zero checking phones, zero distracted glances.
- **Apart Dynamic:** Low digital chatter, high mission focus. Communications serve strictly to confirm logistics and build brief, playful anticipation.

### The 3 Archetypes of Seduction
1. **The Sovereign King:** Calm, immovable, high structural security, unwavering principles.
2. **The Enigmatic Poet:** Subtle wit, intellectual depth, nuanced conversational pacing.
3. **The Unapologetic Challenger:** Teasing, unswayed by beauty, capable of playful reframing.

### Conversational Push-Pull Formulas
- *"You have an incredible sense of style... although I'm not convinced you could survive without your phone for forty-eight hours."*
- *"I love that ambition in you; it's rare. Most people settle for comfort far too early."*
"""

    with open(os.path.join(notion_dir, "03_Part_III_Modern_Siren_Blueprint.md"), "w", encoding="utf-8") as f:
        f.write(part3_md)

    # 5. 04_Part_IV_Obsidian_Protocols.md
    part4_md = """# 🛡️ Part IV: The Obsidian Protocols
*High-Leverage Psychological Boundaries & Unwavering Sovereignty*

> "A boundary is not a wall to punish another; it is the perimeter that protects your highest self."

### Protocol 01: The Zero-Bargaining Standard
When basic respect or agreements are violated, address it once, calmly:
- State what occurred objectively without adjectives.
- State the boundary without an ultimatum: *"In my life, I only engage in dynamics where mutual respect is baseline. If that's difficult right now, we can step back."*
- Disengage gracefully. No posturing.

### Protocol 02: The Sovereign Reset
When emotional chaos threatens your equanimity:
1. Five box-breaths (4s inhale, 4s hold, 4s exhale, 4s hold).
2. Reset posture to neutral vertical alignment.
3. Return to your primary creative or commercial purpose before responding.
"""

    with open(os.path.join(notion_dir, "04_Part_IV_Obsidian_Protocols.md"), "w", encoding="utf-8") as f:
        f.write(part4_md)

    # 6. Audio Transcripts Database CSV
    csv_audio = """Session,Title,Duration,Psychology Vector,Key Timestamp,Core Principle,Transcript Excerpt
01,The Unspoken Shift,02:45,Frame Test Neutralization,01:14,Never rationalize emotional tests,"The moment he stopped rushing to answer my texts something shifted..."
02,The Currency of Attention,03:12,Scarcity & Value Perception,00:45,Affirmation must be earned,"When a man gives away his undivided attention too easily it loses all value..."
03,The Stillness Paradox,02:58,Physical Composure Under Fire,01:50,Stillness commands the room,"He looked me directly in the eyes with a warm steady smile and didn't raise his voice..."
04,The Velvet Rope Effect,03:20,Exclusivity & Soft Boundaries,02:10,High standards without hostility,"The hardest thing to walk away from is a man who lets you know his life is magnificent with or without you..."
05,The Midnight Frequency,02:34,Nocturnal Vocal Resonance,00:55,Slow resonant vocal cadence,"The vocal tone alone created an atmosphere where time seemed to slow down..."
06,The Polarity Engine,03:40,Dynamic Masculine Direction,01:30,Decisiveness relieves female cognitive load,"Knowing that he had completely planned the evening allowed me to finally relax..."
07,Unspoken Vows,02:50,Standards & Integrity,01:15,Integrity in private breeds outward charisma,"A man who keeps promises to himself possesses a natural magnetism..."
08,The Seduction of Competence,03:05,Mastery & Focus,00:40,Total immersion in craft is magnetic,"Watching him work with laser focus without seeking applause was intoxicating..."
09,The Sovereign Farewell,02:40,Graceful Detachment,01:45,Willingness to walk away preserves frame,"The moment he calmly walked away when respect slipped proved he wasn't posturing..."
"""

    with open(os.path.join(notion_dir, "Audio_Transcripts_and_Vault_Index.csv"), "w", encoding="utf-8") as f:
        f.write(csv_audio)

    # 7. Daily Protocols Database CSV
    csv_habits = """Protocol ID,Routine Name,Time of Day,Target Anchor State,Frequency,Key Metric
PROT-01,Vocal Resonance Calibration,07:30 AM,Deep diaphragmatic resonance,Daily,5 minutes breathwork
PROT-02,Physical Stillness Drill,12:00 PM,Zero involuntary fidgeting,Daily,Audit posture in meetings
PROT-03,Digital Accessibility Audit,03:00 PM,Sovereign work focus,Daily,Max 3 message check windows
PROT-04,Frame Integrity Review,09:30 PM,Emotional non-reactivity,Daily,Log conversational tension
PROT-05,Voice Vérité Audio Study,10:00 PM,Psychological deconstruction,3x / Week,1 session + notes
"""

    with open(os.path.join(notion_dir, "Daily_Protocols_and_Habit_Tracker.csv"), "w", encoding="utf-8") as f:
        f.write(csv_habits)

    # 8. README
    readme = """# 🏛️ Secret to Dream — Notion Workspace Export
*Native Import Archive for Notion*

### To import this workspace into Notion:
1. Open Notion (web app or desktop app).
2. Click **Import** at the bottom of your left sidebar.
3. Choose **Markdown & CSV** (or drag this ZIP file).
4. Select this package folder or ZIP.
5. Notion instantly populates your workspace with all dashboards, chapters, and relational databases.
"""
    with open(os.path.join(notion_dir, "README_NOTION_IMPORT.md"), "w", encoding="utf-8") as f:
        f.write(readme)

    # Create the zip archive
    zip_dest = os.path.join("downloads", "Secret_to_Dream_Notion_Workspace.zip")
    with zipfile.ZipFile(zip_dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(notion_dir):
            for file in files:
                full_p = os.path.join(root, file)
                arc_p = os.path.join("Secret to Dream Notion Workspace", file)
                zf.write(full_p, arc_p)

    print(f"Created Notion Workspace ZIP: {zip_dest} ({os.path.getsize(zip_dest)} bytes)")

    # Also generate standalone markdown file
    standalone_md_path = os.path.join("downloads", "Secret_to_Dream_Sovereign_Sanctum.md")
    with open(standalone_md_path, "w", encoding="utf-8") as f:
        f.write(dashboard_md + "\n\n---\n\n" + part1_md + "\n\n---\n\n" + part2_md + "\n\n---\n\n" + part3_md + "\n\n---\n\n" + part4_md)
    print(f"Created Standalone Notion Markdown file: {standalone_md_path} ({os.path.getsize(standalone_md_path)} bytes)")


if __name__ == "__main__":
    build_notion_package()
