# theme.py

COLORS = {
    "bg": "#1B1F24",               # Deep Royal Dark
    "card_bg": "#232830",          # Slightly lighter for cards
    "accent_primary": "#D4AF37",   # Royal Gold
    "accent_high": "#E63946",      # Elegant Red
    "accent_med": "#D4AF37",       # Royal Gold
    "accent_low": "#6096BA",       # Subtle Blue
    "text_main": "#F8F9FA",        # Off-white text
    "text_muted": "#8B949E",       # Muted gray text
    "separator": "#30363D",        # Dark gray for dividers
}

# Define font families here so it's perfectly modular!
HEADING_FONT = "Palatino Linotype"  # A highly stylish, elegant classic serif
BODY_FONT = "Segoe UI"              # A clean, modern sans-serif for readability

FONTS = {
    "h1": (HEADING_FONT, 28, "bold"),
    "h2": (HEADING_FONT, 14, "bold"),
    "body": (BODY_FONT, 11),
    "body_bold": (BODY_FONT, 11, "bold"),
    "body_strike": (BODY_FONT, 11, "overstrike"),
    "small": (BODY_FONT, 9)
}

PRIORITY_CONFIG = {
    "High":   {"fg": COLORS["accent_high"], "order": 0},
    "Medium": {"fg": COLORS["accent_med"], "order": 1},
    "Low":    {"fg": COLORS["accent_low"], "order": 2},
}

PRIORITY_LABELS = list(PRIORITY_CONFIG.keys())
