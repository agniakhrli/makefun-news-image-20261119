import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_star(draw, cx, cy, r_outer, r_inner, fill):
    points = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        angle = i * math.pi / 5 - math.pi / 2
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)

def main():
    # 1024x1024 Canvas, RGB
    width, height = 1024, 1024
    img = Image.new("RGB", (width, height), color="#f7f4ec") # Cream newsprint background
    draw = ImageDraw.Draw(img)

    base_dir = Path(__file__).parent
    font_regular_path = base_dir / "assets" / "DejaVuSans.ttf"
    font_bold_path = base_dir / "assets" / "DejaVuSans-Bold.ttf"

    # Load fonts with various sizes
    f_title = ImageFont.truetype(str(font_bold_path), 46)
    f_date = ImageFont.truetype(str(font_regular_path), 13)
    f_h1 = ImageFont.truetype(str(font_bold_path), 22)
    f_sub1 = ImageFont.truetype(str(font_regular_path), 13)
    f_body = ImageFont.truetype(str(font_regular_path), 11)
    f_h2 = ImageFont.truetype(str(font_bold_path), 15)
    f_h3 = ImageFont.truetype(str(font_bold_path), 13)

    ink_dark = "#1a1a1a"
    ink_muted = "#555555"
    border_color = "#d1c7bd"

    # Outer border / margins
    margin = 16
    usable_w = width - (2 * margin)

    # ---------------------------------------------------------
    # 1. MASTHEAD (y: 16 to 105)
    # ---------------------------------------------------------
    draw.line([(margin, 16), (width - margin, 16)], fill=ink_dark, width=3)
    draw.line([(margin, 20), (width - margin, 20)], fill=ink_dark, width=1)

    # Date & Meta top line
    meta_text = "VOL. IV NO. 323  •  THURSDAY, 19 NOVEMBER 2026  •  THE GLOBAL DAILY REVIEW  •  ONE DOLLAR"
    draw.text((margin, 25), meta_text, fill=ink_muted, font=f_date)

    # Main Title "THE WORLD"
    title_text = "THE WORLD"
    bbox = draw.textbbox((0, 0), title_text, font=f_title)
    t_w = bbox[2] - bbox[0]
    draw.text(((width - t_w) // 2, 42), title_text, fill=ink_dark, font=f_title)

    draw.line([(margin, 98), (width - margin, 98)], fill=ink_dark, width=1)
    draw.line([(margin, 102), (width - margin, 102)], fill=ink_dark, width=3)

    # ---------------------------------------------------------
    # 2. LEAD PANEL: SHENZHEN SUMMIT (y: 110 to 405)
    # ---------------------------------------------------------
    lead_y1, lead_y2 = 110, 405
    draw.rectangle([margin, lead_y1, width - margin, lead_y2], outline=border_color, width=1)
    
    # Accent color header banner for lead panel
    accent_lead = "#8b263e" # Crimson
    draw.rectangle([margin, lead_y1, width - margin, lead_y1 + 24], fill=accent_lead)
    draw.text((margin + 8, lead_y1 + 5), "WORLD LEAD STORY  •  APEC SIDE-SUMMIT IN SHENZHEN", fill="#ffffff", font=f_date)

    # Illustration area on the right / middle of lead panel (x: 540 to 1008, y: 140 to 350)
    ill_x1, ill_y1, ill_x2, ill_y2 = 540, 140, 1008, 350
    draw.rectangle([ill_x1, ill_y1, ill_x2, ill_y2], fill="#eef2f6", outline="#cbd5e1")
    
    # Draw Shenzhen Skyline silhouette in background
    skyline_y = ill_y2 - 35
    draw.rectangle([ill_x1 + 10, skyline_y - 45, ill_x1 + 45, skyline_y], fill="#94a3b8")
    draw.rectangle([ill_x1 + 50, skyline_y - 90, ill_x1 + 95, skyline_y], fill="#64748b")
    draw.rectangle([ill_x1 + 100, skyline_y - 65, ill_x1 + 140, skyline_y], fill="#94a3b8")
    draw.polygon([(ill_x1 + 72, skyline_y - 120), (ill_x1 + 72, skyline_y - 90), (ill_x1 + 75, skyline_y - 90), (ill_x1 + 75, skyline_y - 120)], fill="#475569") # spire
    draw.rectangle([ill_x1 + 180, skyline_y - 105, ill_x1 + 230, skyline_y], fill="#475569")
    draw.rectangle([ill_x1 + 240, skyline_y - 55, ill_x1 + 290, skyline_y], fill="#94a3b8")

    # Draw three flags (US, China, Russia)
    flag_y = ill_y1 + 15
    # US Flag (7 red, 6 white stripes, blue canton in upper hoist with 5x4 white dots)
    us_x1, us_y1, us_x2, us_y2 = ill_x1 + 30, flag_y, ill_x1 + 80, flag_y + 35
    for i in range(13):
        sy1 = us_y1 + int(i * 35 / 13)
        sy2 = us_y1 + int((i + 1) * 35 / 13)
        scol = "#b91c1c" if i % 2 == 0 else "#ffffff"
        draw.rectangle([us_x1, sy1, us_x2, sy2], fill=scol)
    # Blue canton
    draw.rectangle([us_x1, us_y1, us_x1 + 22, us_y1 + 18], fill="#3c3b6e")
    # 5x4 grid of white dots
    for r in range(4):
        for c in range(5):
            dx = us_x1 + int((c + 1) * 22 / 6)
            dy = us_y1 + int((r + 1) * 18 / 5)
            draw.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill="#ffffff")
    draw.rectangle([us_x1, us_y1, us_x2, us_y2], outline="#1e293b", width=1)

    # China Flag (solid red field with 5 yellow stars)
    cn_x1, cn_y1, cn_x2, cn_y2 = ill_x1 + 195, flag_y, ill_x1 + 245, flag_y + 35
    draw.rectangle([cn_x1, cn_y1, cn_x2, cn_y2], fill="#dc2626", outline="#1e293b")
    # Big star
    draw_star(draw, cn_x1 + 12, cn_y1 + 11, 5.0, 2.2, "#ffde00")
    # 4 small stars arcing
    small_star_coords = [
        (cn_x1 + 21, cn_y1 + 6),
        (cn_x1 + 26, cn_y1 + 11),
        (cn_x1 + 26, cn_y1 + 17),
        (cn_x1 + 21, cn_y1 + 22),
    ]
    for (scx, scy) in small_star_coords:
        draw_star(draw, scx, scy, 2.0, 0.9, "#ffde00")

    # Russia Flag (white / blue / red)
    ru_x1, ru_y1, ru_x2, ru_y2 = ill_x1 + 360, flag_y, ill_x1 + 410, flag_y + 35
    draw.rectangle([ru_x1, ru_y1, ru_x2, ru_y2], fill="#ffffff", outline="#1e293b")
    draw.rectangle([ru_x1, ru_y1 + 12, ru_x2, ru_y1 + 24], fill="#1e3a8a")
    draw.rectangle([ru_x1, ru_y1 + 24, ru_x2, ru_y2], fill="#dc2626")

    # Meeting table in illustration
    table_y = ill_y2 - 50
    draw.rectangle([ill_x1 + 40, table_y, ill_x2 - 40, table_y + 25], fill="#334155")
    # Three delegates silhouettes around table
    draw.ellipse([ill_x1 + 110, table_y - 22, ill_x1 + 138, table_y], fill="#1e293b")
    draw.ellipse([ill_x1 + 215, table_y - 22, ill_x1 + 243, table_y], fill="#1e293b")
    draw.ellipse([ill_x1 + 320, table_y - 22, ill_x1 + 348, table_y], fill="#1e293b")

    # Caption BELOW the illustration on the cream background in DARK ink (#2b4c7e)
    caption_text = "TRUMP  •  XI  •  PUTIN"
    f_caption = ImageFont.truetype(str(font_bold_path), 11)
    bbox_cap = draw.textbbox((0, 0), caption_text, font=f_caption)
    cap_w = bbox_cap[2] - bbox_cap[0]
    cap_x = ill_x1 + (ill_x2 - ill_x1 - cap_w) // 2
    cap_y = ill_y2 + 8
    draw.text((cap_x, cap_y), caption_text, fill="#2b4c7e", font=f_caption)

    # Lead Headline & Text (Left side: x: 30 to 520)
    lead_text_x = margin + 14
    lead_text_w = 490
    draw.text((lead_text_x, lead_y1 + 32), "TRUMP, XI AND PUTIN MEET IN SHENZHEN", fill=ink_dark, font=f_h1)
    draw.text((lead_text_x, lead_y1 + 60), "First three-way summit on APEC sidelines: arms control, Ukraine & Iran.", fill=accent_lead, font=f_sub1)

    lead_body = (
        "In a historic diplomatic milestone on the sidelines of the APEC forum in Shenzhen, "
        "Donald Trump, Xi Jinping and Vladimir Putin convened for their very first three-way summit. "
        "Before the trilateral session, Trump held separate 40-minute talks with Putin as well as bilateral discussions with Xi.\n\n"
        "High on the agenda were strategic nuclear arms control—with the New START treaty expiring—alongside "
        "the ongoing war in Ukraine and soaring tensions in the Middle East. "
        "President Trump stated afterwards that the three leaders are 'uniquely positioned' to collaboratively "
        "reduce the global stockpile of nuclear weapons."
    )
    # Wrap lead body text with well-proportioned line spacing to fill panel down to bottom
    y_cursor = lead_y1 + 86
    for paragraph in lead_body.split("\n\n"):
        lines = wrap_text(draw, paragraph, f_body, lead_text_w)
        for line in lines:
            draw.text((lead_text_x, y_cursor), line, fill=ink_dark, font=f_body)
            y_cursor += 16
        y_cursor += 8

    # ---------------------------------------------------------
    # 3. SECOND ROW (2 panels: Kerch Bridge & Gulf / Hormuz) (y: 413 to 640)
    # ---------------------------------------------------------
    row2_y1 = 413
    row2_h = 227
    col_w = (usable_w - 12) // 2
    
    # --- PANEL 2A: KERCH BRIDGE ---
    p2a_x1 = margin
    p2a_x2 = p2a_x1 + col_w
    p2a_y2 = row2_y1 + row2_h
    draw.rectangle([p2a_x1, row2_y1, p2a_x2, p2a_y2], outline=border_color, width=1)
    
    accent_p2b = "#2b4c7e" # Steel Blue
    draw.rectangle([p2a_x1, row2_y1, p2a_x2, row2_y1 + 22], fill=accent_p2b)
    draw.text((p2a_x1 + 8, row2_y1 + 4), "UKRAINE CONFLICT  •  KERCH BRIDGE", fill="#ffffff", font=f_date)

    # Illustration for Kerch Bridge
    kb_ill_x1, kb_ill_y1 = p2a_x1 + 15, row2_y1 + 28
    kb_ill_x2, kb_ill_y2 = p2a_x2 - 15, row2_y1 + 105
    # Sky band
    draw.rectangle([kb_ill_x1, kb_ill_y1, kb_ill_x2, kb_ill_y1 + 42], fill="#e0f2fe", outline="#bae6fd")
    # Sea band (darker blue at bottom)
    draw.rectangle([kb_ill_x1, kb_ill_y1 + 42, kb_ill_x2, kb_ill_y2], fill="#0284c7")

    # Bridge deck height and gap definition
    deck_y = kb_ill_y1 + 36
    gap_x1 = kb_ill_x1 + 150
    gap_x2 = kb_ill_x1 + 235

    # Vertical pillars going down into the water
    pillar_xs = [kb_ill_x1 + 50, kb_ill_x1 + 105, kb_ill_x1 + 280, kb_ill_x1 + 335, kb_ill_x1 + 390]
    for px in pillar_xs:
        draw.line([(px, deck_y), (px, kb_ill_y2)], fill="#334155", width=4)

    # Left bridge segment (horizontal, with tilted broken end at gap)
    draw.line([(kb_ill_x1 + 10, deck_y), (gap_x1 - 20, deck_y)], fill="#334155", width=5)
    draw.line([(gap_x1 - 20, deck_y), (gap_x1, deck_y + 12)], fill="#334155", width=5)

    # Right bridge segment
    draw.line([(gap_x2, deck_y), (kb_ill_x2 - 10, deck_y)], fill="#334155", width=5)

    # Short fallen deck segment half-submerged in water below gap
    draw.line([(gap_x1 + 15, kb_ill_y1 + 40), (gap_x1 + 55, kb_ill_y1 + 54)], fill="#475569", width=4)

    # Smoke rising from the gap (layered soft circles, lighter on top)
    smoke_cx = gap_x1 + 40
    draw.ellipse([smoke_cx - 22, kb_ill_y1 + 20, smoke_cx + 18, kb_ill_y1 + 45], fill="#64748b")
    draw.ellipse([smoke_cx - 8, kb_ill_y1 + 8, smoke_cx + 28, kb_ill_y1 + 32], fill="#94a3b8")
    draw.ellipse([smoke_cx + 2, kb_ill_y1 - 2, smoke_cx + 24, kb_ill_y1 + 18], fill="#cbd5e1")

    # Headline & Text for Kerch Bridge
    draw.text((p2a_x1 + 12, kb_ill_y2 + 6), "KERCH BRIDGE STRUCK FOR 3RD TIME", fill=ink_dark, font=f_h2)
    kb_body = (
        "Ukraine struck the strategic Kerch Bridge for the third time in a week, "
        "causing traffic suspension. The Russian-appointed head of Crimea confirmed "
        "the temporary closure following the previous strike that collapsed a road span."
    )
    y_c = kb_ill_y2 + 25
    for line in wrap_text(draw, kb_body, f_body, col_w - 24):
        draw.text((p2a_x1 + 12, y_c), line, fill=ink_dark, font=f_body)
        y_c += 15

    # --- PANEL 2B: GULF / HORMUZ ---
    p2b_x1 = p2a_x2 + 12
    p2b_x2 = width - margin
    p2b_y2 = row2_y1 + row2_h
    draw.rectangle([p2b_x1, row2_y1, p2b_x2, p2b_y2], outline=border_color, width=1)

    accent_p2b_col = "#b45309" # Amber/Rust
    draw.rectangle([p2b_x1, row2_y1, p2b_x2, row2_y1 + 22], fill=accent_p2b_col)
    draw.text((p2b_x1 + 8, row2_y1 + 4), "MIDDLE EAST  •  GULF & HORMUZ CRISIS", fill="#ffffff", font=f_date)

    # Illustration for Gulf / Hormuz
    gh_ill_x1, gh_ill_y1 = p2b_x1 + 15, row2_y1 + 28
    gh_ill_x2, gh_ill_y2 = p2b_x2 - 15, row2_y1 + 105
    draw.rectangle([gh_ill_x1, gh_ill_y1, gh_ill_x2, gh_ill_y2], fill="#fef3c7", outline="#fde68a")
    # Sea
    draw.rectangle([gh_ill_x1, gh_ill_y1 + 40, gh_ill_x2, gh_ill_y2], fill="#0284c7")
    # Tanker ship
    tanker_x = gh_ill_x1 + 60
    draw.rectangle([tanker_x, gh_ill_y1 + 55, tanker_x + 120, gh_ill_y1 + 72], fill="#475569")
    # Explosion on tanker engine room
    draw.ellipse([tanker_x + 95, gh_ill_y1 + 45, tanker_x + 125, gh_ill_y1 + 68], fill="#ea580c")
    # Missile arc toward Riyadh
    draw.arc([gh_ill_x1 + 100, gh_ill_y1 + 10, gh_ill_x2 - 20, gh_ill_y1 + 70], 180, 360, fill="#dc2626", width=2)

    # Headline & Text for Gulf
    draw.text((p2b_x1 + 12, gh_ill_y2 + 6), "IRAN ATTACKS GULF; IEA WARNS HORMUZ", fill=ink_dark, font=f_h2)
    gh_body = (
        "Iran launched attacks on Gulf states following US strikes on Qeshm island. "
        "A tanker suffered an engine-room strike in the Strait of Hormuz (UKMTO 212). "
        "The IEA called the crisis the greatest threat ever observed to global energy security."
    )
    y_c = gh_ill_y2 + 25
    for line in wrap_text(draw, gh_body, f_body, col_w - 24):
        draw.text((p2b_x1 + 12, y_c), line, fill=ink_dark, font=f_body)
        y_c += 15

    # ---------------------------------------------------------
    # 4. THIRD ROW (2 panels: ICJ Rohingya & COP31 Antalya) (y: 648 to 875)
    # ---------------------------------------------------------
    row3_y1 = 648
    row3_h = 227
    p3_y2 = row3_y1 + row3_h

    # --- PANEL 3A: ICJ ROHINGYA ---
    p3a_x1 = margin
    p3a_x2 = p3a_x1 + col_w
    draw.rectangle([p3a_x1, row3_y1, p3a_x2, p3_y2], outline=border_color, width=1)

    accent_p3a = "#1b4332" # Forest Green
    draw.rectangle([p3a_x1, row3_y1, p3a_x2, row3_y1 + 22], fill=accent_p3a)
    draw.text((p3a_x1 + 8, row3_y1 + 4), "INTERNATIONAL COURT  •  ICJ RULING", fill="#ffffff", font=f_date)

    # Illustration for ICJ Scales of Justice
    icj_ill_x1, icj_ill_y1 = p3a_x1 + 15, row3_y1 + 28
    icj_ill_x2, icj_ill_y2 = p3a_x2 - 15, row3_y1 + 105
    draw.rectangle([icj_ill_x1, icj_ill_y1, icj_ill_x2, icj_ill_y2], fill="#f0fdf4", outline="#bbf7d0")
    cx = (icj_ill_x1 + icj_ill_x2) // 2
    draw.line([(cx, icj_ill_y1 + 15), (cx, icj_ill_y2 - 15)], fill="#1e293b", width=3) # pillar
    draw.line([(cx - 35, icj_ill_y1 + 22), (cx + 35, icj_ill_y1 + 22)], fill="#1e293b", width=3) # beam
    # Left pan
    draw.line([(cx - 35, icj_ill_y1 + 22), (cx - 50, icj_ill_y1 + 55)], fill="#64748b", width=1)
    draw.line([(cx - 35, icj_ill_y1 + 22), (cx - 20, icj_ill_y1 + 55)], fill="#64748b", width=1)
    draw.arc([cx - 55, icj_ill_y1 + 50, cx - 15, icj_ill_y1 + 70], 0, 180, fill="#1e293b", width=2)
    # Right pan
    draw.line([(cx + 35, icj_ill_y1 + 22), (cx + 20, icj_ill_y1 + 55)], fill="#64748b", width=1)
    draw.line([(cx + 35, icj_ill_y1 + 22), (cx + 50, icj_ill_y1 + 55)], fill="#64748b", width=1)
    draw.arc([cx + 15, icj_ill_y1 + 50, cx + 55, icj_ill_y1 + 70], 0, 180, fill="#1e293b", width=2)

    # Headline & Text for ICJ
    draw.text((p3a_x1 + 12, icj_ill_y2 + 6), "ICJ RULES ON ROHINGYA GENOCIDE CASE", fill=ink_dark, font=f_h2)
    icj_body = (
        "The International Court of Justice issues its ruling on Gambia's genocide case against "
        "Myanmar regarding the 2017 military crackdown driving over 730,000 Rohingya to Bangladesh. "
        "No state has ever been found guilty of genocide by the ICJ."
    )
    y_c = icj_ill_y2 + 25
    for line in wrap_text(draw, icj_body, f_body, col_w - 24):
        draw.text((p3a_x1 + 12, y_c), line, fill=ink_dark, font=f_body)
        y_c += 15

    # --- PANEL 3B: COP31 ANTALYA ---
    p3b_x1 = p3a_x2 + 12
    p3b_x2 = width - margin
    draw.rectangle([p3b_x1, row3_y1, p3b_x2, p3_y2], outline=border_color, width=1)

    accent_p3b = "#0f766e" # Teal
    draw.rectangle([p3b_x1, row3_y1, p3b_x2, row3_y1 + 22], fill=accent_p3b)
    draw.text((p3b_x1 + 8, row3_y1 + 4), "CLIMATE SUMMIT  •  COP31 ANTALYA", fill="#ffffff", font=f_date)

    # Illustration for COP31
    cop_ill_x1, cop_ill_y1 = p3b_x1 + 15, row3_y1 + 28
    cop_ill_x2, cop_ill_y2 = p3b_x2 - 15, row3_y1 + 105
    draw.rectangle([cop_ill_x1, cop_ill_y1, cop_ill_x2, cop_ill_y2], fill="#f0fdfa", outline="#ccfbf1")
    cop_cx = (cop_ill_x1 + cop_ill_x2) // 2
    cop_cy = (cop_ill_y1 + cop_ill_y2) // 2 + 5
    draw.ellipse([cop_cx - 80, cop_cy - 20, cop_cx + 80, cop_cy + 25], fill="#0f766e", outline="#115e59")
    for angle_offset in [-60, -20, 20, 60]:
        dx = cop_cx + int(angle_offset * 1.1)
        dy = cop_cy + (15 if abs(angle_offset) > 30 else -25)
        draw.ellipse([dx - 8, dy - 8, dx + 8, dy + 8], fill="#334155")

    # Headline & Text for COP31
    draw.text((p3b_x1 + 12, cop_ill_y2 + 6), "COP31: MINISTERS PRESSED TO UNBLOCK TEXT", fill=ink_dark, font=f_h2)
    cop_body = (
        "In Antalya, Turkey, ministers met in informal sessions to unblock negotiations and adopt "
        "a final text. Delegates were urged to 'lean in and move faster' as a comprehensive climate deal "
        "remained elusive amid mounting pressure."
    )
    y_c = cop_ill_y2 + 25
    for line in wrap_text(draw, cop_body, f_body, col_w - 24):
        draw.text((p3b_x1 + 12, y_c), line, fill=ink_dark, font=f_body)
        y_c += 15

    # ---------------------------------------------------------
    # 5. BOTTOM STRIP: "ALSO TODAY" (y: 883 to 1008)
    # ---------------------------------------------------------
    bot_y1 = 883
    bot_y2 = 1008
    draw.rectangle([margin, bot_y1, width - margin, bot_y2], outline=border_color, width=1)
    
    accent_bot = "#374151" # Charcoal
    draw.rectangle([margin, bot_y1, width - margin, bot_y1 + 20], fill=accent_bot)
    draw.text((margin + 8, bot_y1 + 3), "ALSO TODAY IN GLOBAL NEWS", fill="#ffffff", font=f_date)

    col4_w = (usable_w - 24) // 4
    items = [
        ("BANGLADESH", "Yunus ancestral home torched amid violent unrest spreading across 28 districts."),
        ("ANTHROPIC IPO", "AI firm debuts on stock market with record-breaking US$79.4 billion raise."),
        ("VAN GOGH RECORD", "'Châtaigniers en fleurs' (1890) sells at Sotheby's New York for $190.4M."),
        ("UKRAINE & CYCLONE", "UK pledges 1,000 long-range drones; EU proposes €45B loan. Cyclone Akvan hits Odisha.")
    ]

    bx = margin + 8
    by = bot_y1 + 25
    for title, desc in items:
        draw.text((bx, by), title, fill=accent_bot, font=f_h3)
        y_item = by + 15
        for line in wrap_text(draw, desc, ImageFont.truetype(str(font_regular_path), 10), col4_w - 8):
            draw.text((bx, y_item), line, fill=ink_dark, font=ImageFont.truetype(str(font_regular_path), 10))
            y_item += 13
        bx += col4_w + 8

    # Ensure output directory exists and save
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    out_path = Path(output_dir) / "entry.png"
    img.save(out_path, "PNG")
    print(f"Successfully saved entry to {out_path}")

if __name__ == "__main__":
    main()
