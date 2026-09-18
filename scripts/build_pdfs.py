import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Custom Canvas for dynamic 'Page X of Y' and luxury headers/footers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        if self._pageNumber == 1:
            # Skip running headers/footers on the cover page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#7E7688"))

        # Running Header
        self.drawString(54, 11 * 72 - 36, "SECRET TO DREAM // 1130 EDITION")
        self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "CONFIDENTIAL PSYCHOLOGICAL FOLIO")

        # Header rule
        self.setStrokeColor(colors.HexColor("#C5A059"))
        self.setLineWidth(0.5)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Running Footer
        self.line(54, 46, 8.5 * 72 - 54, 46)
        self.drawString(54, 34, "RESTRICTED PRIVATE SANCTUM · UNAUTHORIZED DUPLICATION PROHIBITED")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 34, page_str)
        self.restoreState()


def create_complete_folio(output_path):
    print(f"Generating Complete Folio PDF: {output_path}")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    GOLD = colors.HexColor("#C5A059")
    GOLD_LIGHT = colors.HexColor("#E6C364")
    DARK_BG = colors.HexColor("#14121A")
    TEXT_MAIN = colors.HexColor("#1A1824")
    TEXT_MUTED = colors.HexColor("#555060")
    BORDER_GOLD = colors.HexColor("#C5A059")

    # Typography Styles
    title_cover = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=32,
        leading=38,
        textColor=colors.HexColor("#14121A"),
        alignment=1, # Center
        spaceAfter=15
    )

    subtitle_cover = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=GOLD,
        alignment=1,
        spaceAfter=30,
        textTransform='uppercase'
    )

    h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=20,
        leading=26,
        textColor=colors.HexColor("#14121A"),
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )

    h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=GOLD,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h3 = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#242230"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=TEXT_MAIN,
        spaceAfter=8
    )

    quote = ParagraphStyle(
        'Quote_Custom',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor("#2C2836"),
        leftIndent=20,
        rightIndent=20,
        spaceBefore=8,
        spaceAfter=12
    )

    callout_text = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#1A1824")
    )

    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MUTED,
        alignment=1
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 80))
    story.append(Paragraph("S E C R E T &nbsp; T O &nbsp; D R E A M", title_cover))
    story.append(Paragraph("THE COMPLETE UNREDACTED FOLIO // ARCHIVE 1130", subtitle_cover))
    story.append(HRFlowable(width="60%", thickness=1.5, color=BORDER_GOLD, spaceAfter=25, spaceBefore=10))

    cover_desc = """
    A master psychological treatise on frame resilience, vocal resonance, subconscious feminine attraction dynamics, 
    and the uncompromising maintenance of sovereign purpose in high-stakes personal relationships.
    """
    story.append(Paragraph(cover_desc.strip(), ParagraphStyle('CoverDesc', parent=styles['Normal'], fontName='Times-Roman', fontSize=12, leading=18, alignment=1, textColor=TEXT_MAIN, spaceAfter=40)))

    cover_meta = [
        [Paragraph("<b>CLASSIFICATION:</b> Restricted / Sovereign Sanctum", meta_style)],
        [Paragraph("<b>DELIVERY FORMAT:</b> Encrypted Digital Folio & Audio Master Archive", meta_style)],
        [Paragraph("<b>PRODUCT CODE:</b> STD-1130-VLT · MASTER EDITION", meta_style)],
        [Paragraph("<b>VALIDATION STATUS:</b> Verified Cryptographic Clearance", meta_style)]
    ]
    meta_table = Table(cover_meta, colWidths=[350])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9F7F3")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GOLD),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 120))
    story.append(Paragraph("© 2026 SECRET TO DREAM SANCTUM. ALL RIGHTS RESERVED.", meta_style))
    story.append(PageBreak())

    # ==================== TABLE OF CONTENTS & PREFACE ====================
    story.append(Paragraph("TABLE OF CONTENTS & STRUCTURE", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_GOLD, spaceAfter=15, spaceBefore=4))

    toc_data = [
        [Paragraph("<b>PART I</b>", h3), Paragraph("<b>THE SILENT SEDUCTION PLAYBOOK</b>", h3), Paragraph("Page 3", h3)],
        [Paragraph("", body), Paragraph("The Sovereign Anchor Principle · Vocal Cadence · Physical Stillness", body), Paragraph("", body)],
        [Paragraph("<b>PART II</b>", h3), Paragraph("<b>VOICE VÉRITÉ: 9 LATE NIGHT SESSIONS</b>", h3), Paragraph("Page 4", h3)],
        [Paragraph("", body), Paragraph("Unedited Transcripts · Subconscious Tests · Decoded Psychology", body), Paragraph("", body)],
        [Paragraph("<b>PART III</b>", h3), Paragraph("<b>THE MODERN SIREN'S BLUEPRINT</b>", h3), Paragraph("Page 6", h3)],
        [Paragraph("", body), Paragraph("Accessibility Ratios · Dynamic Tension & Polarity · Seduction Vectors", body), Paragraph("", body)],
        [Paragraph("<b>PART IV</b>", h3), Paragraph("<b>THE OBSIDIAN PROTOCOLS</b>", h3), Paragraph("Page 7", h3)],
        [Paragraph("", body), Paragraph("Uncompromising Boundaries · The Zero-Bargaining Standard · Sovereign Reset", body), Paragraph("", body)],
    ]
    t_toc = Table(toc_data, colWidths=[60, 380, 60])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5DFC5")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_toc)

    story.append(Spacer(1, 15))
    story.append(Paragraph("EXECUTIVE PREFACE", h2))
    story.append(Paragraph(
        "\"The greatest illusion in modern romance is that overt pursuit generates attraction. In reality, attraction operates like physical gravity: it is generated exclusively by density, mass, and unwavering stillness. When a man establishes unshakeable sovereign composure, the entire emotional universe naturally calibrates around him.\"",
        quote
    ))
    story.append(Paragraph(
        "This folio is designed to be studied alongside the nine <i>Voice Vérité</i> master audio sessions. Each concept documented in these pages is not hypothetical theory; it is reverse-engineered from real-world psychological dynamics observed across high-caliber social interactions.",
        body
    ))
    story.append(PageBreak())

    # ==================== PART I ====================
    story.append(Paragraph("PART I: THE SILENT SEDUCTION PLAYBOOK", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_GOLD, spaceAfter=12, spaceBefore=4))

    story.append(Paragraph("1.1 The Sovereign Anchor Principle", h2))
    story.append(Paragraph(
        "Whenever a high-caliber woman enters a relationship dynamic, she will instinctively test the masculine frame. These tests are almost never conscious; they are autonomic bio-evolutionary probes designed to discover whether you are an immovable mountain or an emotional feather swayed by every breeze.",
        body
    ))
    story.append(Paragraph(
        "<b>The Mistake:</b> 95% of men react defensively. They explain themselves, argue the technical merits, apologize when they have done nothing wrong, or resort to petulant passive-aggression. Each of these responses signals internal panic.",
        body
    ))
    story.append(Paragraph(
        "<b>The Sovereign Anchor:</b> When provoked, pause. Breathe down into the solar plexus. Deliver a gentle, knowing half-smile. Acknowledge her emotion without adopting her premise: <i>'I see you feel passionately about this. Let's speak when we are both ready for solutions.'</i>",
        body
    ))

    story.append(Paragraph("1.2 Vocal Cadence Calibration", h2))
    story.append(Paragraph(
        "Your voice is the primary biological broadcast of your nervous system. An elevated pitch and rapid tempo signal adrenaline, eagerness to please, and submission to the room's prevailing tension.",
        body
    ))

    vocal_points = [
        [Paragraph("<b>Parameter</b>", h3), Paragraph("<b>Submissive Default</b>", h3), Paragraph("<b>Sovereign Calibration</b>", h3)],
        [Paragraph("Pacing", body), Paragraph("150-180 words/min (rushed)", body), Paragraph("105-120 words/min (unhurried)", body)],
        [Paragraph("Inflection", body), Paragraph("Rising upward at sentence end (question tone)", body), Paragraph("Downward settling inflection (authoritative)", body)],
        [Paragraph("Pause Duration", body), Paragraph("0.2 seconds (afraid of interruption)", body), Paragraph("1.5 - 2.0 seconds (comfortable with silence)", body)],
        [Paragraph("Resonator", body), Paragraph("Nasal and upper throat", body), Paragraph("Chest and sub-diaphragm cavity", body)]
    ]
    t_vocal = Table(vocal_points, colWidths=[100, 190, 210])
    t_vocal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F0EAE1")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GOLD),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_vocal)

    story.append(Spacer(1, 10))
    story.append(Paragraph("1.3 Physical Stillness: Eradication of Leakage", h2))
    story.append(Paragraph(
        "Physical fidgeting—tapping feet, readjusting your drink every 30 seconds, looking around the room whenever there is a pause in dialogue—leaks enormous amounts of social power. Practice radical physical stillness. When seated across from someone, let your hands remain motionless on the table or armrests. Unshakable posture communicates that nothing in the environment can perturb you.",
        body
    ))
    story.append(PageBreak())

    # ==================== PART II ====================
    story.append(Paragraph("PART II: VOICE VÉRITÉ — 9 SESSIONS PSYCHOLOGY", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_GOLD, spaceAfter=12, spaceBefore=4))

    story.append(Paragraph(
        "The <i>Voice Vérité</i> audio recordings represent unedited psychological insights. Below are the definitive transcripts and strategic deconstructions for every session included in your master audio archive.",
        body
    ))

    sessions = [
        ("Session 01", "The Unspoken Shift (02:45)", "Frame Test Neutralization",
         "\"The moment he stopped rushing to answer my texts within seconds, something shifted inside me. It wasn't that he was playing cheap mind games. It was the sudden realization that he actually had an entire empire he was building that mattered more than my immediate validation. That was the moment I wanted him.\"",
         "Scarcity cannot be feigned with artificial timers; it must emerge organically from deep immersion in your sovereign life mission."),

        ("Session 02", "The Currency of Attention (03:12)", "The Value of Scarcity",
         "\"When a man gives away his undivided attention too easily to every attractive woman in the room, his compliments lose all meaning. The man whose praise feels earned—who looks at you with discerning standards—becomes the only person whose opinion actually matters.\"",
         "Affirmation bestowed too freely becomes worthless currency. Make your approval a scarce luxury rather than a complimentary baseline."),

        ("Session 03", "The Stillness Paradox (02:58)", "Physical Composure Under Conflict",
         "\"We were having an intense disagreement at dinner. I expected him to shout or argue back. Instead, he simply took a sip of his drink, looked me directly in the eyes with a warm, steady gaze, and didn't raise his voice by half a decibel. My defensiveness completely evaporated.\"",
         "Silence and physical immobility during emotional escalation automatically force the counterpart to de-escalate and self-reflect."),

        ("Session 04", "The Velvet Rope Effect (03:20)", "Soft Boundary Enforcement",
         "\"The hardest thing to walk away from is a man who lets you know his life is magnificent with or without you. He opened the door to his world, but made it completely clear that disrespect would close it forever without a scene or an argument.\"",
         "Boundaries enforced with quiet serenity are a thousand times more respected than boundaries screamed in fury.")
    ]

    for code, title, vector, transcript, breakdown in sessions:
        story.append(Paragraph(f"<b>{code}: {title}</b> — <i>{vector}</i>", h2))
        story.append(Paragraph(transcript, quote))
        story.append(Paragraph(f"<b>Psychological Deconstruction:</b> {breakdown}", body))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # Remaining Sessions 5 - 9
    story.append(Paragraph("VOICE VÉRITÉ (CONTINUED: SESSIONS 05 - 09)", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_GOLD, spaceAfter=12, spaceBefore=4))

    sessions_cont = [
        ("Session 05", "The Midnight Frequency (02:34)", "Nocturnal Vocal Resonance",
         "\"His vocal tone alone created an atmosphere where the outside world ceased to exist. He wasn't trying to impress me with clever stories; he spoke from the chest, slowly, with deliberate pauses that invited me into his world.\"",
         "Pacing and resonance lower cognitive defenses. Late-night conversations thrive on slow cadence and deep chest resonance."),

        ("Session 06", "The Polarity Engine (03:40)", "Masculine Decisiveness",
         "\"Knowing that he had completely planned the evening—from the reservation to the drive through the hills—allowed me to finally turn off my executive brain and just relax. Decisive leadership is the most attractive quality a man can exhibit.\"",
         "Relieving the feminine of cognitive executive load creates immediate biological polarity and deep emotional relaxation."),

        ("Session 07", "Unspoken Vows (02:50)", "Integrity as Magnetic Aura",
         "\"A man who keeps the private promises he makes to himself possesses an aura you can physically feel. When he speaks, you believe him because his words carry weight, not hot air.\"",
         "Internal discipline is felt externally. You cannot fake authentic self-respect."),

        ("Session 08", "The Seduction of Competence (03:05)", "Absorption in Craft",
         "\"Watching him work on his project with complete, undivided focus—oblivious to whether I was watching—was utterly intoxicating. Mastery in motion is universally attractive.\"",
         "Men who are completely immersed in their craft generate involuntary desire. Do not make a woman the center of your universe."),

        ("Session 09", "The Sovereign Farewell (02:40)", "Graceful Detachment",
         "\"The moment he calmly packed his things and walked away when our standards no longer aligned proved to me that he wasn't posturing. He loved me, but he loved his self-respect more. I will never forget that.\"",
         "The ultimate source of all power in negotiation and romance is the genuine ability and willingness to walk away.")
    ]

    for code, title, vector, transcript, breakdown in sessions_cont:
        story.append(Paragraph(f"<b>{code}: {title}</b> — <i>{vector}</i>", h2))
        story.append(Paragraph(transcript, quote))
        story.append(Paragraph(f"<b>Psychological Deconstruction:</b> {breakdown}", body))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ==================== PART III ====================
    story.append(Paragraph("PART III: THE MODERN SIREN'S BLUEPRINT", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_GOLD, spaceAfter=12, spaceBefore=4))

    story.append(Paragraph("3.1 The Golden Ratio of Accessibility", h2))
    story.append(Paragraph(
        "Modern hyper-connected digital culture has created an epidemic of accessibility. When you are instantly reachable via messaging 24/7, mystery vanishes, and with it, psychological desire.",
        body
    ))
    story.append(Paragraph(
        "<b>The Formula:</b> In-person presence must be 100% focused, tactile, and attentive (zero phone checks). Digital presence must be lean, disciplined, and purposeful. Let days pass between dates without pointless texting marathons.",
        body
    ))

    story.append(Paragraph("3.2 Dynamic Tension & Emotional Polarity", h2))
    story.append(Paragraph(
        "Attraction requires polarity: positive and negative charges, tension and release, certainty and intrigue. If you provide constant predictable validation, emotional flatlining is inevitable.",
        body
    ))

    siren_table = [
        [Paragraph("<b>Dynamic</b>", h3), Paragraph("<b>The Flatline Approach</b>", h3), Paragraph("<b>The High-Polarity Calibration</b>", h3)],
        [Paragraph("Compliments", body), Paragraph("Pours on generic praise constantly", body), Paragraph("Specific, earned observations delivered with warmth", body)],
        [Paragraph("Conversational Pacing", body), Paragraph("Answers instantly to avoid awkwardness", body), Paragraph("Pauses, teases gently, reframes assumptions", body)],
        [Paragraph("Scheduling", body), Paragraph("Clears entire schedule at her convenience", body), Paragraph("Offers 2 specific windows aligned with his priorities", body)],
        [Paragraph("Emotional Frame", body), Paragraph("Mirrors her distress or panic", body), Paragraph("Remains the calm center in the eye of the storm", body)]
    ]
    t_siren = Table(siren_table, colWidths=[110, 190, 200])
    t_siren.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F0EAE1")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GOLD),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_siren)
    story.append(PageBreak())

    # ==================== PART IV ====================
    story.append(Paragraph("PART IV: THE OBSIDIAN PROTOCOLS", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_GOLD, spaceAfter=12, spaceBefore=4))

    story.append(Paragraph("4.1 The Zero-Bargaining Standard", h2))
    story.append(Paragraph(
        "A man who bargains over basic respect has already surrendered his frame. When disrespect or boundary violations occur, do not deliver dramatic lectures or raise your voice. Emotional displays reveal that you are hurt and attempting to regain control through coercion.",
        body
    ))
    story.append(Paragraph(
        "<b>The Execution:</b> State the fact objectively. <i>'In my life, mutual respect and open communication are non-negotiable. What just happened does not meet that standard.'</i> Then physically disengage. Give her the gift of missing you and experiencing the reality of a world without your presence.",
        body
    ))

    story.append(Paragraph("4.2 The Sovereign Reset Drill", h2))
    story.append(Paragraph(
        "When an unexpected crisis, emotional provocation, or high-stakes negotiation threatens your internal equanimity, execute the following four-stage reset drill immediately:",
        body
    ))

    reset_steps = [
        [Paragraph("<b>Step</b>", h3), Paragraph("<b>Protocol Action</b>", h3), Paragraph("<b>Neurological Objective</b>", h3)],
        [Paragraph("1. Somatic Halt", body), Paragraph("Stop speaking mid-sentence. Relax tongue, jaw, and shoulders.", body), Paragraph("Inhibits sympathetic adrenaline cascade", body)],
        [Paragraph("2. Box-Breath 4x4", body), Paragraph("Inhale 4s, Hold 4s, Exhale 4s, Hold 4s. Repeat 3 cycles.", body), Paragraph("Activates parasympathetic vagal brake", body)],
        [Paragraph("3. Peripheral Vision", body), Paragraph("Expand visual awareness to the room's extreme edges.", body), Paragraph("De-focuses threat tunnel-vision in amygdala", body)],
        [Paragraph("4. Core Alignment", body), Paragraph("Ask: 'Does answering this serve my highest sovereign purpose?'", body), Paragraph("Restores prefrontal cortex dominance", body)]
    ]
    t_reset = Table(reset_steps, colWidths=[90, 230, 180])
    t_reset.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F0EAE1")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GOLD),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_reset)

    story.append(Spacer(1, 20))
    story.append(Paragraph("FINAL SANCTUM IMPERATIVE", h2))
    story.append(Paragraph(
        "\"You are the architect of your own temple. Never sacrifice your standards for temporary comfort, and never compromise your sovereign peace for transient approval. Walk with calm certainty, speak with intention, and let your presence be your unyielding signature.\"",
        quote
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Complete Folio PDF generated successfully ({os.path.getsize(output_path)} bytes)")


def create_frameworks_cheatsheet(output_path):
    print(f"Generating Frameworks Cheatsheet PDF: {output_path}")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    GOLD = colors.HexColor("#C5A059")
    BORDER_GOLD = colors.HexColor("#C5A059")

    title_style = ParagraphStyle(
        'SheetTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#14121A"),
        alignment=1,
        spaceAfter=2
    )

    sub_style = ParagraphStyle(
        'SheetSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=GOLD,
        alignment=1,
        spaceAfter=12,
        textTransform='uppercase'
    )

    sec_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#14121A"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    cell_h = ParagraphStyle(
        'CellH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#14121A")
    )

    cell_b = ParagraphStyle(
        'CellB',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#242230")
    )

    callout_s = ParagraphStyle(
        'CalloutS',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1A1824"),
        alignment=1
    )

    story = []

    # Title Banner
    story.append(Paragraph("SECRET TO DREAM // FRAMEWORKS & CALIBRATION MATRIX", title_style))
    story.append(Paragraph("Executive Quick-Reference Guide · Unredacted Collector Edition", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_GOLD, spaceAfter=8, spaceBefore=0))

    # Table 1: Frame Retention Matrix
    story.append(Paragraph("1. THE SUBCONSCIOUS TEST & CALIBRATED RESPONSE MATRIX", sec_title))
    test_matrix = [
        [Paragraph("<b>Scenario / Feminine Probe</b>", cell_h), Paragraph("<b>Instinctive Reactive Mistake</b>", cell_h), Paragraph("<b>Calibrated Sovereign Calibration</b>", cell_h)],
        [
            Paragraph("<b>Emotional Flake / Late Cancellation:</b> Cancels plans at the last minute with a vague excuse.", cell_b),
            Paragraph("Demanding explanations, complaining, guilt-tripping, or immediately offering alternate days.", cell_b),
            Paragraph("<i>'Understood. Enjoy your evening.'</i> Zero follow-up. Do not re-initiate until she contacts you and proposes plans.", cell_b)
        ],
        [
            Paragraph("<b>Public Teasing / Frame Challenge:</b> Teases your outfit, choices, or career in a group setting.", cell_b),
            Paragraph("Getting defensive, explaining the brand/reasoning, or attacking back with hurt sarcasm.", cell_b),
            Paragraph("Gentle amused smirk. Hold eye contact for 2s: <i>'You're lucky you're cute.'</i> Transition topic smoothly.", cell_b)
        ],
        [
            Paragraph("<b>The Jealousy Vector:</b> Mentions another male pursuer who gave her attention or gifts.", cell_b),
            Paragraph("Asking who he is, criticizing him, displaying jealousy, or trying to compete financially.", cell_b),
            Paragraph("<i>'He sounds like he has good taste.'</i> Calm detachment demonstrates supreme inner security.", cell_b)
        ],
        [
            Paragraph("<b>Emotional Storm / Provocation:</b> Raises voice or expresses chaotic frustration at dinner.", cell_b),
            Paragraph("Shouting back, matching high energy, or apologizing submissively to quiet her down.", cell_b),
            Paragraph("Absolute physical stillness. Slow deep exhale. <i>'I want to hear you, but let's speak without the shouting.'</i>", cell_b)
        ]
    ]
    t1 = Table(test_matrix, colWidths=[160, 180, 200])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFE9DD")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GOLD),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t1)

    story.append(Spacer(1, 6))

    # Table 2: Vocal Tone Calibration Index
    story.append(Paragraph("2. VOCAL CADENCE & NON-VERBAL GRAVITY INDEX", sec_title))
    vocal_matrix = [
        [Paragraph("<b>Vocal Parameter</b>", cell_h), Paragraph("<b>Optimal Setting</b>", cell_h), Paragraph("<b>Neurological Impact on Counterpart</b>", cell_h)],
        [Paragraph("Pacing / Speed", cell_b), Paragraph("105 - 120 words / minute", cell_b), Paragraph("Signals total emotional comfort and absence of urgency.", cell_b)],
        [Paragraph("Resonator Focus", cell_b), Paragraph("Lower chest / diaphragm", cell_b), Paragraph("Low-frequency vocal resonance triggers calming oxytocin response.", cell_b)],
        [Paragraph("Sentence Endings", cell_b), Paragraph("Descending downward tone", cell_b), Paragraph("Prevents statements from sounding like requests for permission.", cell_b)],
        [Paragraph("Micro-Pauses", cell_b), Paragraph("1.5s after key questions", cell_b), Paragraph("Creates psychological gravity; forces other person to invest.", cell_b)],
        [Paragraph("Physical Stillness", cell_b), Paragraph("Zero involuntary micro-movements", cell_b), Paragraph("Unflinching stillness conveys overwhelming alpha dominance.", cell_b)]
    ]
    t2 = Table(vocal_matrix, colWidths=[120, 160, 260])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFE9DD")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GOLD),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t2)

    story.append(PageBreak())

    # Page 2: Protocols & Reset
    story.append(Paragraph("3. THE 4-STAGE ACCESSIBILITY & POLARITY CODE", sec_title))
    acc_matrix = [
        [Paragraph("<b>Phase</b>", cell_h), Paragraph("<b>Digital Behavior (Apart)</b>", cell_h), Paragraph("<b>Physical Behavior (Together)</b>", cell_h)],
        [
            Paragraph("<b>Initial Attraction</b>", cell_b),
            Paragraph("Low volume, high quality. Response times proportional to work schedule. No chit-chat.", cell_b),
            Paragraph("100% presence, playful challenge, unhurried posture, zero phone on the table.", cell_b)
        ],
        [
            Paragraph("<b>Building Tension</b>", cell_b),
            Paragraph("Do not respond immediately to late-night prompts. Call briefly instead of texting endless threads.", cell_b),
            Paragraph("Lead the itinerary decisively. Choose the venues, order with confidence, embrace touch.", cell_b)
        ],
        [
            Paragraph("<b>Testing & Calibration</b>", cell_b),
            Paragraph("Never argue via text. If conflict arises: <i>'Let's talk tomorrow when we can see each other.'</i>", cell_b),
            Paragraph("Absolute calm stillness. Never raise voice. Maintain eye contact until she softens.", cell_b)
        ],
        [
            Paragraph("<b>Established Frame</b>", cell_b),
            Paragraph("Your life mission remains priority #1. She enters a moving train, not an empty station.", cell_b),
            Paragraph("Warmth, security, and generous praise only when genuinely earned by loyalty.", cell_b)
        ]
    ]
    t3 = Table(acc_matrix, colWidths=[110, 210, 220])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFE9DD")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GOLD),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t3)

    story.append(Spacer(1, 8))
    story.append(Paragraph("4. EMERGENCY 60-SECOND SOVEREIGN RESET PROTOCOL", sec_title))

    reset_box = [
        [Paragraph("<b>WHEN TRIGGERED OR UNDER ACUTE EMOTIONAL TENSION:</b>", cell_h)],
        [Paragraph("1. <b>RADICAL PAUSE:</b> Inhale through the nose for 4 seconds, hold for 4 seconds, exhale through the mouth for 6 seconds. Drop shoulders 2 inches.", cell_b)],
        [Paragraph("2. <b>NO DEFENSIVE EXPLANATION:</b> Eliminate all 'because' and 'I was just trying to' statements from your vocabulary.", cell_b)],
        [Paragraph("3. <b>THE ZERO-BARGAINING RULE:</b> <i>'I hear your perspective. In my life, mutual respect is baseline. We can continue when you are ready to speak calmly.'</i>", cell_b)],
        [Paragraph("4. <b>PHYSICAL DETACHMENT:</b> If disrespect persists, stand up, settle the bill, and depart cleanly. No anger, no slammed doors. Sovereignty is silent.", cell_b)]
    ]
    t_box = Table(reset_box, colWidths=[540])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAF8F5")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GOLD),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_box)

    story.append(Spacer(1, 14))
    story.append(Paragraph("<i>\"The ultimate authority is not the man who commands others, but the man whom no one can unseat from himself.\"</i>", callout_s))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Frameworks Cheatsheet PDF generated successfully ({os.path.getsize(output_path)} bytes)")


if __name__ == "__main__":
    folio_path = os.path.join("downloads", "Secret_to_Dream_The_Complete_Folio.pdf")
    cheatsheet_path = os.path.join("downloads", "Secret_to_Dream_Frameworks_Cheatsheet.pdf")
    create_complete_folio(folio_path)
    create_frameworks_cheatsheet(cheatsheet_path)
