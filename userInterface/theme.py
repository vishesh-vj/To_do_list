# theme.py

COLORS = {
    "bg": "#121212",               # Dark background
    "card_bg": "#1E1E1E",          # Slightly lighter for cards
    "accent_pink": "#FF007F",      # Hot Pink (Funky/Gen-Z)
    "accent_green": "#39FF14",     # Lime Green
    "accent_cyan": "#00FFFF",      # Bright Cyan
    "accent_purple": "#8A2BE2",    # Electric Purple
    "text_main": "#FFFFFF",        # White text
    "text_muted": "#A0A0A0",       # Muted gray text
    "separator": "#333333",        # Dark gray for dividers
}

FONTS = {
    "h1": ("Comic Sans MS", 28, "bold"),       # Ironic Y2K Gen-Z style
    "h2": ("Comic Sans MS", 14, "bold"),
    "body": ("Verdana", 11),                   # Clean but slightly brutalist
    "body_bold": ("Verdana", 11, "bold"),
    "body_strike": ("Verdana", 11, "overstrike"),
    "small": ("Verdana", 9)
}

PRIORITY_CONFIG = {
    "🔴 High":   {"fg": COLORS["accent_pink"], "order": 0},
    "🟡 Medium": {"fg": COLORS["accent_purple"], "order": 1},
    "🔵 Low":    {"fg": COLORS["accent_cyan"], "order": 2},
}

PRIORITY_LABELS = list(PRIORITY_CONFIG.keys())
