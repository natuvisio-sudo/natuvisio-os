"""
================================================================================
 NATUVISIO OPERATIONS SYSTEM v8.0
 Production-Grade Brand Partner Portal & Admin Command Center
 
 Architecture: Streamlit + CSV Persistence
 Design System: Glass Morphism, Premium Wellness Aesthetic
 Standards: WCAG 2.1 AA Compliant, Mobile-First
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import time
import hashlib
import urllib.parse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Operations",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%235b7354'><path d='M12 2L2 22h20L12 2z'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Security
ADMIN_CREDENTIALS = {
    "admin@natuvisio.com": hashlib.sha256("admin2025".encode()).hexdigest()
}

# Database Files
DB_ORDERS = "orders_complete.csv"
DB_PAYMENTS = "brand_payments.csv"
DB_INVOICES = "brand_invoices.csv"
DB_LOGS = "system_logs.csv"
DB_PARTNERS = "partners.csv"
DB_MESSAGES = "messages.csv"

# Design Tokens
TOKENS = {
    "space_xs": 8,
    "space_sm": 13,
    "space_md": 21,
    "space_lg": 34,
    "space_xl": 55,
    "radius_sm": 8,
    "radius_md": 12,
    "radius_lg": 16,
    "phi": 1.618
}

# Assets
LOGO_URL = "https://res.cloudinary.com/deb1j92hy/image/upload/f_auto,q_auto/v1764805291/natuvisio_logo_gtqtfs.png"
BG_IMAGE = "https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp"

# Timezone
TZ_IST = ZoneInfo("Europe/Istanbul")
TZ_UTC = ZoneInfo("UTC")

def now_ist():
    return datetime.now(TZ_IST)

def now_utc():
    return datetime.now(TZ_UTC)

# Order States
class OrderStatus:
    PENDING = "Pending"
    ACCEPTED = "Accepted_by_Brand"
    REJECTED = "Rejected_by_Brand"
    DISPATCHED = "Dispatched"
    COMPLETED_BRAND = "Completed_Brand_Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

# Brand Configuration
BRANDS = {
    "HAKI HEAL": {
        "phone": "905359264991",
        "email": "haki@natuvisio.com",
        "color": "#4ECDC4",
        "color_dark": "#3BA99E",
        "commission": 0.15,
        "iban": "TR90 0006 1000 0000 1234 5678 90",
        "account_name": "Haki Heal Ltd. Sti.",
        "products": {
            "HAKI HEAL KREM": {"sku": "SKU-HAKI-CRM-01", "price": 450},
            "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY-01", "price": 380},
            "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP-01", "price": 120}
        }
    },
    "AURORACO": {
        "phone": "905359264991",
        "email": "aurora@natuvisio.com",
        "color": "#FF6B6B",
        "color_dark": "#E55555",
        "commission": 0.20,
        "iban": "TR90 0006 2000 0000 9876 5432 10",
        "account_name": "Auroraco Gida A.S.",
        "products": {
            "AURORACO MATCHA EZMESI": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO KAKAO EZMESI": {"sku": "SKU-AUR-CACAO", "price": 550},
            "AURORACO SUPER GIDA": {"sku": "SKU-AUR-SUPER", "price": 800}
        }
    },
    "LONGEVICALS": {
        "phone": "905359264991",
        "email": "long@natuvisio.com",
        "color": "#95E1D3",
        "color_dark": "#7BCFC0",
        "commission": 0.12,
        "iban": "TR90 0001 5000 0000 1122 3344 55",
        "account_name": "Longevicals Saglik Urunleri",
        "products": {
            "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
            "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
        }
    }
}

# ============================================================================
# SVG ICON SYSTEM
# ============================================================================

class Icons:
    @staticmethod
    def render(name, color="#5b7354", size=20):
        icons = {
            "mountain": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m8 3 4 8 5-5 5 15H2L8 3z"/></svg>',
            "package": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16.5 9.4 7.55 4.24"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/></svg>',
            "truck": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/></svg>',
            "check_circle": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
            "x_circle": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
            "clock": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
            "dollar": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
            "message": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
            "inbox": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>',
            "send": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>',
            "file_text": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
            "bar_chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>',
            "users": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
            "settings": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
            "log_out": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>',
            "alert_triangle": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
            "bell": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
            "mail": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
            "phone": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
            "copy": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
            "plus": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
            "trash": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>',
            "eye": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
            "external_link": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>',
            "refresh": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>',
            "filter": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>',
            "download": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
            "calendar": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
            "shield": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
            "activity": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
            "help": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
            "user": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
            "lock": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
        }
        return icons.get(name, "")

# ============================================================================
# DESIGN SYSTEM - CSS
# ============================================================================

def load_design_system():
    st.markdown(f"""
    <style>
        /* ================================================================
           NATUVISIO DESIGN SYSTEM v8.0
           Premium Glass Morphism + Wellness Aesthetic
           ================================================================ */
        
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&display=swap');
        
        :root {{
            --nv-primary: #5b7354;
            --nv-primary-dark: #4a6043;
            --nv-primary-light: #7a9471;
            --nv-accent: #4ECDC4;
            --nv-accent-warm: #F4A261;
            --nv-danger: #DC3545;
            --nv-warning: #F59E0B;
            --nv-success: #10B981;
            --nv-text: #1a1a2e;
            --nv-text-muted: #64748b;
            --nv-glass-bg: rgba(255, 255, 255, 0.72);
            --nv-glass-border: rgba(91, 115, 84, 0.15);
            --nv-glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            --nv-radius: {TOKENS['radius_md']}px;
            --nv-transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        .stApp {{
            background-image: 
                linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(245,245,240,0.2) 100%),
                url("{BG_IMAGE}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--nv-text);
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6,
        .nv-heading {{
            font-family: 'Newsreader', Georgia, serif !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em !important;
            color: var(--nv-text) !important;
        }}
        
        /* Glass Cards */
        .nv-glass {{
            background: var(--nv-glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--nv-glass-border);
            border-radius: var(--nv-radius);
            box-shadow: var(--nv-glass-shadow);
            transition: var(--nv-transition);
        }}
        
        .nv-glass:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
        }}
        
        .nv-card {{
            background: var(--nv-glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--nv-glass-border);
            border-radius: var(--nv-radius);
            padding: {TOKENS['space_md']}px;
            margin-bottom: {TOKENS['space_sm']}px;
            box-shadow: var(--nv-glass-shadow);
        }}
        
        .nv-card-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: {TOKENS['space_sm']}px;
            padding-bottom: {TOKENS['space_sm']}px;
            border-bottom: 1px solid var(--nv-glass-border);
        }}
        
        .nv-card-title {{
            font-family: 'DM Sans', sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: var(--nv-text);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Metrics */
        .nv-metric {{
            text-align: center;
            padding: {TOKENS['space_md']}px;
        }}
        
        .nv-metric-value {{
            font-family: 'Newsreader', Georgia, serif;
            font-size: 32px;
            font-weight: 700;
            color: var(--nv-text);
            line-height: 1.1;
            letter-spacing: -0.03em;
        }}
        
        .nv-metric-label {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--nv-text-muted);
            margin-bottom: 6px;
        }}
        
        .nv-metric-delta {{
            font-size: 12px;
            font-weight: 500;
            margin-top: 4px;
        }}
        
        .nv-metric-delta.positive {{ color: var(--nv-success); }}
        .nv-metric-delta.negative {{ color: var(--nv-danger); }}
        
        /* Buttons */
        div.stButton > button {{
            background: linear-gradient(135deg, var(--nv-primary), var(--nv-primary-dark)) !important;
            color: white !important;
            border: none !important;
            padding: {TOKENS['space_sm']}px {TOKENS['space_md']}px !important;
            border-radius: 8px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            letter-spacing: 0.3px !important;
            transition: var(--nv-transition) !important;
            box-shadow: 0 4px 14px rgba(91, 115, 84, 0.3) !important;
        }}
        
        div.stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(91, 115, 84, 0.4) !important;
        }}
        
        div.stButton > button:active {{
            transform: translateY(0) !important;
        }}
        
        /* Form Inputs */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div,
        .stNumberInput > div > div > input {{
            background: rgba(255, 255, 255, 0.8) !important;
            border: 1px solid var(--nv-glass-border) !important;
            border-radius: 8px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 14px !important;
            transition: var(--nv-transition) !important;
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: var(--nv-primary) !important;
            box-shadow: 0 0 0 3px rgba(91, 115, 84, 0.15) !important;
        }}
        
        /* Status Badges */
        .nv-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .nv-badge-pending {{
            background: rgba(245, 158, 11, 0.15);
            color: #B45309;
        }}
        
        .nv-badge-accepted {{
            background: rgba(59, 130, 246, 0.15);
            color: #1D4ED8;
        }}
        
        .nv-badge-dispatched {{
            background: rgba(139, 92, 246, 0.15);
            color: #6D28D9;
        }}
        
        .nv-badge-completed {{
            background: rgba(16, 185, 129, 0.15);
            color: #047857;
        }}
        
        .nv-badge-rejected {{
            background: rgba(220, 53, 69, 0.15);
            color: #B91C1C;
        }}
        
        /* Alert Banners */
        .nv-alert {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 18px;
            border-radius: var(--nv-radius);
            margin-bottom: {TOKENS['space_sm']}px;
            backdrop-filter: blur(10px);
        }}
        
        .nv-alert-warning {{
            background: rgba(245, 158, 11, 0.12);
            border-left: 3px solid var(--nv-warning);
        }}
        
        .nv-alert-danger {{
            background: rgba(220, 53, 69, 0.1);
            border-left: 3px solid var(--nv-danger);
            animation: nv-pulse 2s infinite;
        }}
        
        .nv-alert-success {{
            background: rgba(16, 185, 129, 0.1);
            border-left: 3px solid var(--nv-success);
        }}
        
        .nv-alert-info {{
            background: rgba(59, 130, 246, 0.1);
            border-left: 3px solid #3B82F6;
        }}
        
        .nv-alert-text {{
            font-size: 13px;
            font-weight: 600;
            color: var(--nv-text);
        }}
        
        .nv-alert-subtext {{
            font-size: 11px;
            color: var(--nv-text-muted);
            margin-top: 2px;
        }}
        
        @keyframes nv-pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.85; }}
        }}
        
        /* Dividers */
        .nv-divider {{
            height: 1px;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(91, 115, 84, 0.25), 
                transparent
            );
            margin: {TOKENS['space_lg']}px 0;
        }}
        
        /* Tables */
        .nv-table-container {{
            background: var(--nv-glass-bg);
            border-radius: var(--nv-radius);
            overflow: hidden;
            border: 1px solid var(--nv-glass-border);
        }}
        
        /* Message Bubbles */
        .nv-message {{
            max-width: 75%;
            padding: 12px 16px;
            border-radius: 16px;
            margin-bottom: 8px;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        .nv-message-outgoing {{
            background: var(--nv-primary);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 4px;
        }}
        
        .nv-message-incoming {{
            background: rgba(255, 255, 255, 0.9);
            color: var(--nv-text);
            margin-right: auto;
            border-bottom-left-radius: 4px;
            border: 1px solid var(--nv-glass-border);
        }}
        
        .nv-message-meta {{
            font-size: 10px;
            color: var(--nv-text-muted);
            margin-top: 4px;
        }}
        
        /* Footer */
        .nv-footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(15px);
            border-top: 1px solid var(--nv-glass-border);
            padding: 12px 24px;
            font-size: 11px;
            color: var(--nv-text-muted);
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nv-footer-left {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .nv-footer-status {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .nv-footer-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--nv-success);
            animation: nv-pulse 2s infinite;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: transparent;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: rgba(91, 115, 84, 0.3);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(91, 115, 84, 0.5);
        }}
        
        /* Hide Streamlit Elements */
        #MainMenu, header, footer {{ visibility: hidden; }}
        .stDeployButton {{ display: none; }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            background: rgba(255, 255, 255, 0.5);
            padding: 4px;
            border-radius: 10px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            font-family: 'DM Sans', sans-serif;
            font-weight: 500;
            font-size: 13px;
            padding: 8px 16px;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: var(--nv-primary) !important;
            color: white !important;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: rgba(255, 255, 255, 0.6) !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }}
        
        /* Unread Badge */
        .nv-unread-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 20px;
            height: 20px;
            padding: 0 6px;
            border-radius: 10px;
            background: var(--nv-danger);
            color: white;
            font-size: 11px;
            font-weight: 700;
        }}
        
        /* Quick Action Links */
        .nv-quick-action {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
            transition: var(--nv-transition);
        }}
        
        .nv-quick-action-whatsapp {{
            background: rgba(37, 211, 102, 0.15);
            color: #128C7E;
        }}
        
        .nv-quick-action-whatsapp:hover {{
            background: rgba(37, 211, 102, 0.25);
        }}
        
        .nv-quick-action-email {{
            background: rgba(59, 130, 246, 0.15);
            color: #1D4ED8;
        }}
        
        .nv-quick-action-email:hover {{
            background: rgba(59, 130, 246, 0.25);
        }}
        
        /* Order Card */
        .nv-order-card {{
            background: var(--nv-glass-bg);
            border: 1px solid var(--nv-glass-border);
            border-radius: var(--nv-radius);
            padding: {TOKENS['space_md']}px;
            margin-bottom: {TOKENS['space_sm']}px;
            transition: var(--nv-transition);
        }}
        
        .nv-order-card:hover {{
            border-color: var(--nv-primary);
            box-shadow: 0 4px 20px rgba(91, 115, 84, 0.15);
        }}
        
        .nv-order-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }}
        
        .nv-order-id {{
            font-family: 'DM Sans', sans-serif;
            font-size: 16px;
            font-weight: 700;
            color: var(--nv-primary);
        }}
        
        .nv-order-time {{
            font-size: 11px;
            color: var(--nv-text-muted);
        }}
        
        .nv-order-details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            font-size: 13px;
        }}
        
        .nv-order-label {{
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--nv-text-muted);
            margin-bottom: 2px;
        }}
        
        .nv-order-value {{
            font-weight: 600;
            color: var(--nv-text);
        }}
        
        /* Financial Summary */
        .nv-finance-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px dashed rgba(91, 115, 84, 0.15);
        }}
        
        .nv-finance-row:last-child {{
            border-bottom: none;
            padding-top: 12px;
            margin-top: 4px;
            border-top: 2px solid var(--nv-primary);
        }}
        
        .nv-finance-label {{
            color: var(--nv-text-muted);
            font-size: 13px;
        }}
        
        .nv-finance-value {{
            font-weight: 700;
            font-size: 14px;
        }}
        
        .nv-finance-value.highlight {{
            color: var(--nv-accent);
            font-size: 18px;
        }}
        
        /* Conversation List */
        .nv-conversation-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            transition: var(--nv-transition);
        }}
        
        .nv-conversation-item:hover {{
            background: rgba(91, 115, 84, 0.08);
        }}
        
        .nv-conversation-item.active {{
            background: rgba(91, 115, 84, 0.12);
        }}
        
        .nv-conversation-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
            color: white;
        }}
        
        .nv-conversation-info {{
            flex: 1;
            min-width: 0;
        }}
        
        .nv-conversation-name {{
            font-weight: 600;
            font-size: 14px;
            color: var(--nv-text);
        }}
        
        .nv-conversation-preview {{
            font-size: 12px;
            color: var(--nv-text-muted);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        /* System Health Indicator */
        .nv-health {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11px;
            color: var(--nv-text-muted);
        }}
        
        .nv-health-indicator {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }}
        
        .nv-health-good {{ background: var(--nv-success); }}
        .nv-health-warning {{ background: var(--nv-warning); }}
        .nv-health-error {{ background: var(--nv-danger); }}
        
        /* Padding for footer */
        .main .block-container {{
            padding-bottom: 80px;
        }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATABASE LAYER
# ============================================================================

class Database:
    @staticmethod
    def init_all():
        """Initialize all database files with proper schemas"""
        
        # Orders
        if not os.path.exists(DB_ORDERS):
            pd.DataFrame(columns=[
                "Order_ID", "Time_UTC", "Time_IST", "Brand", "Customer", "Phone", 
                "Email", "Address", "Items", "Total_Value", "Commission_Rate", 
                "Commission_Amt", "Brand_Payout", "Status", "WhatsApp_Sent", 
                "Tracking_Num", "Courier", "Priority", "Notes", "Created_By", 
                "Last_Modified_UTC", "Last_Modified_IST"
            ]).to_csv(DB_ORDERS, index=False)
        
        # Payments
        if not os.path.exists(DB_PAYMENTS):
            pd.DataFrame(columns=[
                "Payment_ID", "Time_UTC", "Time_IST", "Brand", "Amount", "Method",
                "Reference", "Status", "Proof_File", "Notes", "Invoice_Sent",
                "Invoice_Date", "Invoice_Number", "Invoice_Explanation"
            ]).to_csv(DB_PAYMENTS, index=False)
        
        # Invoices
        if not os.path.exists(DB_INVOICES):
            pd.DataFrame(columns=[
                "Invoice_ID", "Time_UTC", "Time_IST", "Brand", "Amount", 
                "Date_Range", "Invoice_Number", "Status", "Notes"
            ]).to_csv(DB_INVOICES, index=False)
        
        # System Logs
        if not os.path.exists(DB_LOGS):
            pd.DataFrame(columns=[
                "Log_ID", "Time_UTC", "Time_IST", "Action", "User", "Role",
                "Brand", "Order_ID", "Details", "IP_Address"
            ]).to_csv(DB_LOGS, index=False)
        
        # Partners
        if not os.path.exists(DB_PARTNERS):
            partners = []
            for brand_name, brand_data in BRANDS.items():
                partners.append({
                    "partner_email": brand_data["email"],
                    "password_hash": hashlib.sha256(f"{brand_name.lower().replace(' ', '')}2025".encode()).hexdigest(),
                    "brand_name": brand_name,
                    "created_at_utc": now_utc().isoformat(),
                    "created_at_ist": now_ist().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "Active"
                })
            pd.DataFrame(partners).to_csv(DB_PARTNERS, index=False)
        
        # Messages
        if not os.path.exists(DB_MESSAGES):
            pd.DataFrame(columns=[
                "Message_ID", "Time_UTC", "Time_IST", "From_Role", "From_Brand",
                "To_Role", "To_Brand", "Order_ID", "Channel", "Subject", "Body",
                "Read_By_Admin", "Read_By_Brand"
            ]).to_csv(DB_MESSAGES, index=False)
    
    @staticmethod
    def load(file_path):
        """Safely load a CSV file"""
        try:
            return pd.read_csv(file_path)
        except Exception:
            return pd.DataFrame()
    
    @staticmethod
    def save(df, file_path):
        """Safely save a DataFrame to CSV"""
        try:
            df.to_csv(file_path, index=False)
            return True
        except Exception as e:
            st.error(f"Database save error: {e}")
            return False
    
    @staticmethod
    def orders():
        return Database.load(DB_ORDERS)
    
    @staticmethod
    def payments():
        return Database.load(DB_PAYMENTS)
    
    @staticmethod
    def invoices():
        return Database.load(DB_INVOICES)
    
    @staticmethod
    def logs():
        return Database.load(DB_LOGS)
    
    @staticmethod
    def partners():
        return Database.load(DB_PARTNERS)
    
    @staticmethod
    def messages():
        return Database.load(DB_MESSAGES)

# ============================================================================
# LOGGING SYSTEM
# ============================================================================

def log_action(action, user, role, brand="", order_id="", details=""):
    """Log an action to the system logs"""
    try:
        df = Database.logs()
        log_entry = {
            "Log_ID": f"LOG-{now_utc().strftime('%Y%m%d%H%M%S%f')[:17]}",
            "Time_UTC": now_utc().isoformat(),
            "Time_IST": now_ist().strftime("%Y-%m-%d %H:%M:%S"),
            "Action": action,
            "User": user,
            "Role": role,
            "Brand": brand,
            "Order_ID": order_id,
            "Details": details[:500] if details else "",
            "IP_Address": ""
        }
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        Database.save(df, DB_LOGS)
    except Exception:
        pass

# ============================================================================
# MESSAGE SYSTEM
# ============================================================================

class MessageSystem:
    @staticmethod
    def send(from_role, from_brand, to_role, to_brand, subject, body, order_id="", channel="panel"):
        """Send a message"""
        df = Database.messages()
        message = {
            "Message_ID": f"MSG-{now_utc().strftime('%Y%m%d%H%M%S%f')[:17]}",
            "Time_UTC": now_utc().isoformat(),
            "Time_IST": now_ist().strftime("%Y-%m-%d %H:%M:%S"),
            "From_Role": from_role,
            "From_Brand": from_brand,
            "To_Role": to_role,
            "To_Brand": to_brand,
            "Order_ID": order_id,
            "Channel": channel,
            "Subject": subject,
            "Body": body,
            "Read_By_Admin": "Yes" if from_role == "admin" else "No",
            "Read_By_Brand": "Yes" if from_role == "partner" else "No"
        }
        df = pd.concat([df, pd.DataFrame([message])], ignore_index=True)
        Database.save(df, DB_MESSAGES)
        log_action("MESSAGE_SENT", from_brand if from_role == "partner" else "Admin", 
                   from_role, from_brand if from_role == "partner" else to_brand, 
                   order_id, f"Subject: {subject}")
        return True
    
    @staticmethod
    def get_unread_count_admin():
        """Get unread message count for admin"""
        df = Database.messages()
        if df.empty:
            return 0
        return len(df[(df["To_Role"] == "admin") & (df["Read_By_Admin"] == "No")])
    
    @staticmethod
    def get_unread_count_brand(brand):
        """Get unread message count for a brand"""
        df = Database.messages()
        if df.empty:
            return 0
        return len(df[(df["To_Brand"] == brand) & (df["To_Role"] == "partner") & (df["Read_By_Brand"] == "No")])
    
    @staticmethod
    def mark_read_admin(brand=None):
        """Mark messages as read by admin"""
        df = Database.messages()
        if df.empty:
            return
        mask = (df["To_Role"] == "admin") & (df["Read_By_Admin"] == "No")
        if brand:
            mask = mask & (df["From_Brand"] == brand)
        df.loc[mask, "Read_By_Admin"] = "Yes"
        Database.save(df, DB_MESSAGES)
    
    @staticmethod
    def mark_read_brand(brand):
        """Mark messages as read by brand"""
        df = Database.messages()
        if df.empty:
            return
        mask = (df["To_Brand"] == brand) & (df["To_Role"] == "partner") & (df["Read_By_Brand"] == "No")
        df.loc[mask, "Read_By_Brand"] = "Yes"
        Database.save(df, DB_MESSAGES)
    
    @staticmethod
    def get_conversation(brand):
        """Get all messages for a brand conversation"""
        df = Database.messages()
        if df.empty:
            return pd.DataFrame()
        mask = (df["From_Brand"] == brand) | (df["To_Brand"] == brand)
        return df[mask].sort_values("Time_UTC", ascending=True)

# ============================================================================
# ORDER MANAGEMENT
# ============================================================================

class OrderManager:
    @staticmethod
    def create(brand, customer, phone, email, address, items, total_value, 
               commission_rate, commission_amt, brand_payout, created_by="admin"):
        """Create a new order"""
        df = Database.orders()
        order = {
            "Order_ID": f"NV-{now_ist().strftime('%m%d%H%M%S')}",
            "Time_UTC": now_utc().isoformat(),
            "Time_IST": now_ist().strftime("%Y-%m-%d %H:%M:%S"),
            "Brand": brand,
            "Customer": customer,
            "Phone": phone,
            "Email": email,
            "Address": address,
            "Items": items,
            "Total_Value": total_value,
            "Commission_Rate": commission_rate,
            "Commission_Amt": commission_amt,
            "Brand_Payout": brand_payout,
            "Status": OrderStatus.PENDING,
            "WhatsApp_Sent": "No",
            "Tracking_Num": "",
            "Courier": "",
            "Priority": "Standard",
            "Notes": "",
            "Created_By": created_by,
            "Last_Modified_UTC": now_utc().isoformat(),
            "Last_Modified_IST": now_ist().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.concat([df, pd.DataFrame([order])], ignore_index=True)
        if Database.save(df, DB_ORDERS):
            log_action("ORDER_CREATED", created_by, "admin", brand, order["Order_ID"], 
                       f"Created order for {customer}")
            return order["Order_ID"]
        return None
    
    @staticmethod
    def update_status(order_id, new_status, user, role, brand="", notes=""):
        """Update order status"""
        df = Database.orders()
        mask = df["Order_ID"] == order_id
        if mask.any():
            df.loc[mask, "Status"] = new_status
            df.loc[mask, "Last_Modified_UTC"] = now_utc().isoformat()
            df.loc[mask, "Last_Modified_IST"] = now_ist().strftime("%Y-%m-%d %H:%M:%S")
            if notes:
                df.loc[mask, "Notes"] = notes
            if Database.save(df, DB_ORDERS):
                log_action("STATUS_CHANGE", user, role, brand, order_id, 
                           f"Status changed to {new_status}")
                return True
        return False
    
    @staticmethod
    def update_tracking(order_id, tracking_num, courier, user, role, brand=""):
        """Update tracking information"""
        df = Database.orders()
        mask = df["Order_ID"] == order_id
        if mask.any():
            df.loc[mask, "Tracking_Num"] = tracking_num
            df.loc[mask, "Courier"] = courier
            df.loc[mask, "Status"] = OrderStatus.DISPATCHED
            df.loc[mask, "Last_Modified_UTC"] = now_utc().isoformat()
            df.loc[mask, "Last_Modified_IST"] = now_ist().strftime("%Y-%m-%d %H:%M:%S")
            if Database.save(df, DB_ORDERS):
                log_action("TRACKING_ADDED", user, role, brand, order_id, 
                           f"Tracking: {courier} - {tracking_num}")
                return True
        return False
    
    @staticmethod
    def mark_notified(order_id):
        """Mark order as notified via WhatsApp"""
        df = Database.orders()
        mask = df["Order_ID"] == order_id
        if mask.any():
            df.loc[mask, "WhatsApp_Sent"] = "Yes"
            df.loc[mask, "Last_Modified_UTC"] = now_utc().isoformat()
            df.loc[mask, "Last_Modified_IST"] = now_ist().strftime("%Y-%m-%d %H:%M:%S")
            Database.save(df, DB_ORDERS)
            log_action("WHATSAPP_SENT", "Admin", "admin", "", order_id, "WhatsApp notification sent")

# ============================================================================
# PAYMENT MANAGEMENT
# ============================================================================

class PaymentManager:
    @staticmethod
    def create(brand, amount, method, reference, notes=""):
        """Create a payment record"""
        df = Database.payments()
        payment = {
            "Payment_ID": f"PAY-{now_utc().strftime('%Y%m%d%H%M%S')}",
            "Time_UTC": now_utc().isoformat(),
            "Time_IST": now_ist().strftime("%Y-%m-%d %H:%M:%S"),
            "Brand": brand,
            "Amount": amount,
            "Method": method,
            "Reference": reference,
            "Status": "Confirmed",
            "Proof_File": "",
            "Notes": notes,
            "Invoice_Sent": "No",
            "Invoice_Date": "",
            "Invoice_Number": "",
            "Invoice_Explanation": ""
        }
        df = pd.concat([df, pd.DataFrame([payment])], ignore_index=True)
        if Database.save(df, DB_PAYMENTS):
            log_action("PAYMENT_RECORDED", "Admin", "admin", brand, "", 
                       f"Payment of {amount:,.2f} TL recorded")
            return True
        return False
    
    @staticmethod
    def update_invoice_status(payment_id, invoice_sent, invoice_date, invoice_number):
        """Update invoice status for a payment"""
        df = Database.payments()
        mask = df["Payment_ID"] == payment_id
        if mask.any():
            df.loc[mask, "Invoice_Sent"] = invoice_sent
            df.loc[mask, "Invoice_Date"] = invoice_date
            df.loc[mask, "Invoice_Number"] = invoice_number
            return Database.save(df, DB_PAYMENTS)
        return False

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

def init_session():
    """Initialize session state"""
    defaults = {
        "admin_logged_in": False,
        "admin_email": None,
        "partner_logged_in": False,
        "partner_brand": None,
        "partner_email": None,
        "cart": [],
        "cart_brand": None,
        "active_conversation": None,
        "login_mode": "admin"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_header(title, subtitle="", brand_color=None):
    """Render page header"""
    accent = brand_color or "#5b7354"
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px;">
        <img src="{LOGO_URL}" style="height: 48px;" onerror="this.style.display='none'">
        <div>
            <h1 style="margin: 0; font-size: 26px; color: {accent};">{title}</h1>
            <span style="font-size: 12px; color: var(--nv-text-muted); letter-spacing: 0.5px;">
                {subtitle}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric(label, value, icon=None, accent=None, delta=None):
    """Render a metric card"""
    icon_html = Icons.render(icon, accent or "#5b7354", 20) if icon else ""
    delta_html = ""
    if delta:
        delta_class = "positive" if delta > 0 else "negative"
        delta_html = f'<div class="nv-metric-delta {delta_class}">{delta:+.1f}%</div>'
    
    st.markdown(f"""
    <div class="nv-card nv-metric" style="border-top: 3px solid {accent or '#5b7354'};">
        <div class="nv-metric-label">{label}</div>
        <div class="nv-metric-value" style="color: {accent or 'var(--nv-text)'};">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def render_alert(message, alert_type="info", submessage=""):
    """Render an alert banner"""
    icons_map = {
        "warning": ("alert_triangle", "#F59E0B"),
        "danger": ("alert_triangle", "#DC3545"),
        "success": ("check_circle", "#10B981"),
        "info": ("bell", "#3B82F6")
    }
    icon_name, color = icons_map.get(alert_type, ("bell", "#3B82F6"))
    icon_html = Icons.render(icon_name, color, 20)
    
    sub_html = f'<div class="nv-alert-subtext">{submessage}</div>' if submessage else ""
    
    st.markdown(f"""
    <div class="nv-alert nv-alert-{alert_type}">
        {icon_html}
        <div>
            <div class="nv-alert-text">{message}</div>
            {sub_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_divider():
    """Render a divider line"""
    st.markdown('<div class="nv-divider"></div>', unsafe_allow_html=True)

def render_status_badge(status):
    """Render a status badge"""
    status_map = {
        OrderStatus.PENDING: ("pending", "Beklemede"),
        OrderStatus.ACCEPTED: ("accepted", "Onaylandi"),
        OrderStatus.REJECTED: ("rejected", "Reddedildi"),
        OrderStatus.DISPATCHED: ("dispatched", "Kargoda"),
        OrderStatus.COMPLETED_BRAND: ("completed", "Marka Onayladi"),
        OrderStatus.COMPLETED: ("completed", "Tamamlandi"),
        OrderStatus.CANCELLED: ("rejected", "Iptal")
    }
    badge_class, label = status_map.get(status, ("pending", status))
    return f'<span class="nv-badge nv-badge-{badge_class}">{label}</span>'

def render_footer():
    """Render the system footer"""
    time_ist = now_ist().strftime("%H:%M:%S")
    
    # Get system stats
    orders_count = len(Database.orders())
    messages_count = len(Database.messages())
    
    st.markdown(f"""
    <div class="nv-footer">
        <div class="nv-footer-left">
            <div class="nv-footer-status">
                <span class="nv-footer-dot"></span>
                <span>Sistem Aktif</span>
            </div>
            <span>Istanbul: {time_ist}</span>
            <span>Siparisler: {orders_count}</span>
            <span>Mesajlar: {messages_count}</span>
        </div>
        <div>
            NATUVISIO Operations v8.0 · Dahili Kullanim
        </div>
    </div>
    """, unsafe_allow_html=True)

def generate_whatsapp_link(phone, message):
    """Generate WhatsApp link"""
    encoded_msg = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded_msg}"

def generate_email_link(to, subject, body):
    """Generate mailto link"""
    encoded_subject = urllib.parse.quote(subject)
    encoded_body = urllib.parse.quote(body)
    return f"mailto:{to}?subject={encoded_subject}&body={encoded_body}"

# ============================================================================
# LOGIN SCREEN
# ============================================================================

def render_login():
    """Render the login screen"""
    load_design_system()
    Database.init_all()
    
    st.markdown("<div style='height: 8vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        # Logo
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 32px;">
            <img src="{LOGO_URL}" style="height: 80px; margin-bottom: 16px;">
            <h1 style="margin: 0; font-size: 32px; color: #5b7354;">NATUVISIO</h1>
            <p style="color: var(--nv-text-muted); font-size: 13px; margin-top: 8px;">
                Operations Management System
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login mode toggle
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        
        mode_cols = st.columns(2)
        with mode_cols[0]:
            if st.button("Yonetici Girisi", use_container_width=True, 
                        type="primary" if st.session_state.login_mode == "admin" else "secondary"):
                st.session_state.login_mode = "admin"
                st.rerun()
        with mode_cols[1]:
            if st.button("Partner Girisi", use_container_width=True,
                        type="primary" if st.session_state.login_mode == "partner" else "secondary"):
                st.session_state.login_mode = "partner"
                st.rerun()
        
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        if st.session_state.login_mode == "admin":
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                {Icons.render("shield", "#5b7354", 32)}
                <h3 style="margin: 12px 0 4px;">Yonetici Paneli</h3>
                <p style="font-size: 12px; color: var(--nv-text-muted);">Tam erisim yetkisi</p>
            </div>
            """, unsafe_allow_html=True)
            
            email = st.text_input("E-posta", placeholder="admin@natuvisio.com")
            password = st.text_input("Sifre", type="password")
            
            if st.button("Giris Yap", use_container_width=True, type="primary"):
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                if email in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[email] == password_hash:
                    st.session_state.admin_logged_in = True
                    st.session_state.admin_email = email
                    log_action("LOGIN", email, "admin", "", "", "Admin login successful")
                    st.rerun()
                else:
                    st.error("Gecersiz kimlik bilgileri")
        
        else:
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                {Icons.render("users", "#5b7354", 32)}
                <h3 style="margin: 12px 0 4px;">Partner Portali</h3>
                <p style="font-size: 12px; color: var(--nv-text-muted);">Marka hesabiniza erisin</p>
            </div>
            """, unsafe_allow_html=True)
            
            email = st.text_input("Partner E-posta", placeholder="marka@natuvisio.com")
            password = st.text_input("Sifre", type="password", key="partner_pwd")
            
            if st.button("Partner Girisi", use_container_width=True, type="primary"):
                partners = Database.partners()
                user = partners[partners["partner_email"] == email]
                
                if not user.empty:
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    if user.iloc[0]["password_hash"] == password_hash:
                        st.session_state.partner_logged_in = True
                        st.session_state.partner_brand = user.iloc[0]["brand_name"]
                        st.session_state.partner_email = email
                        log_action("LOGIN", email, "partner", user.iloc[0]["brand_name"], "", 
                                   "Partner login successful")
                        st.rerun()
                    else:
                        st.error("Gecersiz sifre")
                else:
                    st.error("Hesap bulunamadi")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Demo credentials hint
        st.markdown("""
        <div style="text-align: center; margin-top: 24px; font-size: 11px; color: var(--nv-text-muted);">
            <details>
                <summary style="cursor: pointer;">Demo Bilgileri</summary>
                <div style="margin-top: 8px; text-align: left; background: rgba(255,255,255,0.5); padding: 12px; border-radius: 8px;">
                    <strong>Admin:</strong> admin@natuvisio.com / admin2025<br>
                    <strong>Haki Heal:</strong> haki@natuvisio.com / hakiheal2025<br>
                    <strong>Auroraco:</strong> aurora@natuvisio.com / auroraco2025<br>
                    <strong>Longevicals:</strong> long@natuvisio.com / longevicals2025
                </div>
            </details>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ADMIN DASHBOARD
# ============================================================================

def render_admin_dashboard():
    """Render the admin dashboard"""
    load_design_system()
    
    # Header
    col_h1, col_h2 = st.columns([6, 1])
    with col_h1:
        render_header("Yonetim Merkezi", "NATUVISIO Operations v8.0")
    with col_h2:
        unread = MessageSystem.get_unread_count_admin()
        badge_html = f'<span class="nv-unread-badge">{unread}</span>' if unread > 0 else ""
        
        st.markdown(f"""
        <div style="display: flex; gap: 12px; justify-content: flex-end; align-items: center;">
            <span style="font-size: 12px; color: var(--nv-text-muted);">{st.session_state.admin_email}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Cikis", use_container_width=True):
            log_action("LOGOUT", st.session_state.admin_email, "admin")
            st.session_state.admin_logged_in = False
            st.session_state.admin_email = None
            st.rerun()
    
    # Alerts
    df_orders = Database.orders()
    pending_notify = len(df_orders[df_orders["WhatsApp_Sent"] == "No"]) if not df_orders.empty else 0
    pending_track = len(df_orders[(df_orders["Status"] == OrderStatus.ACCEPTED) & 
                                  ((df_orders["Tracking_Num"].isna()) | (df_orders["Tracking_Num"] == ""))]) if not df_orders.empty else 0
    
    if pending_notify > 0:
        render_alert(f"{pending_notify} siparis bildirim bekliyor", "danger", "Operasyon sekmesinde islem yapin")
    if pending_track > 0:
        render_alert(f"{pending_track} siparisin kargo takip numarasi eksik", "warning")
    
    unread_messages = MessageSystem.get_unread_count_admin()
    if unread_messages > 0:
        render_alert(f"{unread_messages} okunmamis mesaj var", "info", "Partner Mesajlari sekmesini kontrol edin")
    
    # Metrics
    total_revenue = df_orders["Total_Value"].sum() if not df_orders.empty else 0
    total_commission = df_orders["Commission_Amt"].sum() if not df_orders.empty else 0
    pending_orders = len(df_orders[df_orders["Status"] == OrderStatus.PENDING]) if not df_orders.empty else 0
    total_orders = len(df_orders)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        render_metric("Toplam Ciro", f"{total_revenue:,.0f} TL", "dollar")
    with col_m2:
        render_metric("Net Komisyon", f"{total_commission:,.0f} TL", "bar_chart", "#4ECDC4")
    with col_m3:
        render_metric("Bekleyen Islem", str(pending_orders), "clock", "#F59E0B")
    with col_m4:
        render_metric("Toplam Siparis", str(total_orders), "package")
    
    render_divider()
    
    # Tabs
    tabs = st.tabs([
        "Yeni Sevkiyat",
        "Operasyon",
        "Fatura ve Odeme",
        "Tum Siparisler",
        "Partner Mesajlari",
        "Analitik",
        "Sistem Kayitlari"
    ])
    
    with tabs[0]:
        render_admin_new_dispatch()
    with tabs[1]:
        render_admin_operations()
    with tabs[2]:
        render_admin_finance()
    with tabs[3]:
        render_admin_all_orders()
    with tabs[4]:
        render_admin_messages()
    with tabs[5]:
        render_admin_analytics()
    with tabs[6]:
        render_admin_logs()
    
    render_footer()

def render_admin_new_dispatch():
    """Render new dispatch/order creation"""
    col_left, col_right = st.columns([TOKENS["phi"], 1])
    
    with col_left:
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="nv-card-header">{Icons.render("user", "#5b7354")} <span class="nv-card-title">Musteri Bilgileri</span></div>', unsafe_allow_html=True)
        
        col_n, col_p = st.columns(2)
        with col_n:
            cust_name = st.text_input("Ad Soyad", key="dispatch_name")
        with col_p:
            cust_phone = st.text_input("Telefon", key="dispatch_phone")
        
        col_e, col_a = st.columns([1, 2])
        with col_e:
            cust_email = st.text_input("E-posta", key="dispatch_email")
        with col_a:
            cust_addr = st.text_area("Adres", height=80, key="dispatch_addr")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="nv-card-header">{Icons.render("package", "#5b7354")} <span class="nv-card-title">Urun Secimi</span></div>', unsafe_allow_html=True)
        
        if st.session_state.cart:
            render_alert(f"Kilitli Marka: {st.session_state.cart_brand}", "info")
            active_brand = st.session_state.cart_brand
        else:
            active_brand = st.selectbox("Marka", list(BRANDS.keys()), key="dispatch_brand")
        
        brand_data = BRANDS[active_brand]
        products = list(brand_data["products"].keys())
        
        col_p, col_q = st.columns([3, 1])
        with col_p:
            product = st.selectbox("Urun", products, key="dispatch_product")
        with col_q:
            qty = st.number_input("Adet", min_value=1, value=1, key="dispatch_qty")
        
        prod_info = brand_data["products"][product]
        unit_price = prod_info["price"]
        line_total = unit_price * qty
        comm_amt = line_total * brand_data["commission"]
        payout = line_total - comm_amt
        
        st.markdown(f"""
        <div style="background: rgba(91,115,84,0.08); padding: 12px; border-radius: 8px; margin: 12px 0;">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; text-align: center;">
                <div>
                    <div class="nv-order-label">Birim Fiyat</div>
                    <div style="font-weight: 600;">{unit_price:,.0f} TL</div>
                </div>
                <div>
                    <div class="nv-order-label">Satir Toplami</div>
                    <div style="font-weight: 600;">{line_total:,.0f} TL</div>
                </div>
                <div>
                    <div class="nv-order-label">Komisyon</div>
                    <div style="font-weight: 600; color: var(--nv-warning);">{comm_amt:,.0f} TL</div>
                </div>
                <div>
                    <div class="nv-order-label">Marka Payi</div>
                    <div style="font-weight: 600; color: var(--nv-accent);">{payout:,.0f} TL</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sepete Ekle", use_container_width=True):
            st.session_state.cart.append({
                "brand": active_brand,
                "product": product,
                "sku": prod_info["sku"],
                "qty": qty,
                "unit_price": unit_price,
                "subtotal": line_total,
                "comm_amt": comm_amt,
                "payout": payout
            })
            st.session_state.cart_brand = active_brand
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="nv-card-header">{Icons.render("package", "#5b7354")} <span class="nv-card-title">Sepet</span></div>', unsafe_allow_html=True)
        
        if st.session_state.cart:
            for i, item in enumerate(st.session_state.cart):
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.5); padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <strong style="font-size: 13px;">{item['product']}</strong>
                        <span style="background: var(--nv-accent); color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px;">x{item['qty']}</span>
                    </div>
                    <div style="font-size: 12px; color: var(--nv-text-muted);">
                        {item['unit_price']:,.0f} TL x {item['qty']} = <strong>{item['subtotal']:,.0f} TL</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            total = sum(i["subtotal"] for i in st.session_state.cart)
            total_comm = sum(i["comm_amt"] for i in st.session_state.cart)
            total_payout = sum(i["payout"] for i in st.session_state.cart)
            
            st.markdown(f"""
            <div style="background: rgba(78,205,196,0.1); padding: 16px; border-radius: 8px; margin-top: 16px;">
                <div class="nv-finance-row">
                    <span class="nv-finance-label">Urun Toplami</span>
                    <span class="nv-finance-value">{total:,.0f} TL</span>
                </div>
                <div class="nv-finance-row">
                    <span class="nv-finance-label">Komisyon</span>
                    <span class="nv-finance-value" style="color: var(--nv-warning);">{total_comm:,.0f} TL</span>
                </div>
                <div class="nv-finance-row">
                    <span class="nv-finance-label">Markaya Net</span>
                    <span class="nv-finance-value highlight">{total_payout:,.0f} TL</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
            
            if st.button("Siparisi Olustur", type="primary", use_container_width=True):
                if cust_name and cust_phone:
                    items_str = ", ".join([f"{i['product']} (x{i['qty']})" for i in st.session_state.cart])
                    
                    order_id = OrderManager.create(
                        brand=st.session_state.cart_brand,
                        customer=cust_name,
                        phone=cust_phone,
                        email=cust_email,
                        address=cust_addr,
                        items=items_str,
                        total_value=total,
                        commission_rate=BRANDS[st.session_state.cart_brand]["commission"],
                        commission_amt=total_comm,
                        brand_payout=total_payout,
                        created_by=st.session_state.admin_email
                    )
                    
                    if order_id:
                        st.success(f"Siparis olusturuldu: {order_id}")
                        st.session_state.cart = []
                        st.session_state.cart_brand = None
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("Musteri bilgilerini giriniz")
            
            if st.button("Sepeti Temizle", use_container_width=True):
                st.session_state.cart = []
                st.session_state.cart_brand = None
                st.rerun()
        else:
            st.markdown("""
            <div style="text-align: center; padding: 40px 20px; color: var(--nv-text-muted);">
                <div style="margin-bottom: 12px; opacity: 0.5;">Sepet Bos</div>
                <div style="font-size: 12px;">Urun ekleyerek baslayin</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_admin_operations():
    """Render operations management"""
    df = Database.orders()
    
    if df.empty:
        render_alert("Henuz siparis bulunmuyor", "info")
        return
    
    # Pending notifications
    st.markdown(f'<h3 style="margin-bottom: 16px;">{Icons.render("bell", "#F59E0B")} Bildirim Bekleyenler</h3>', unsafe_allow_html=True)
    
    pending_notify = df[df["WhatsApp_Sent"] == "No"]
    
    if pending_notify.empty:
        render_alert("Tum siparisler bildirildi", "success")
    else:
        for idx, row in pending_notify.iterrows():
            brand_data = BRANDS.get(row["Brand"], {})
            phone = brand_data.get("phone", "")
            
            msg = f"""YENI SIPARIS: {row['Order_ID']}
Urunler: {row['Items']}
Musteri: {row['Customer']}
Adres: {row['Address']}
Marka Payi: {row['Brand_Payout']:,.0f} TL"""
            
            wa_link = generate_whatsapp_link(phone, msg)
            
            with st.expander(f"{row['Order_ID']} - {row['Brand']} ({row['Customer']})", expanded=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="font-size: 13px;">
                        <strong>Urunler:</strong> {row['Items']}<br>
                        <strong>Adres:</strong> {row['Address']}<br>
                        <strong>Marka Payi:</strong> {row['Brand_Payout']:,.0f} TL
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <a href="{wa_link}" target="_blank" class="nv-quick-action nv-quick-action-whatsapp">
                        {Icons.render("phone", "#128C7E", 16)} WhatsApp ile Bildir
                    </a>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("Bildirildi Olarak Isaretle", key=f"notify_{idx}"):
                        OrderManager.mark_notified(row["Order_ID"])
                        st.rerun()
    
    render_divider()
    
    # Tracking needed
    st.markdown(f'<h3 style="margin-bottom: 16px;">{Icons.render("truck", "#5b7354")} Takip Numarasi Beklenenler</h3>', unsafe_allow_html=True)
    
    pending_track = df[(df["Status"].isin([OrderStatus.PENDING, OrderStatus.ACCEPTED])) & 
                       ((df["Tracking_Num"].isna()) | (df["Tracking_Num"] == ""))]
    
    if pending_track.empty:
        render_alert("Takip numarasi bekleyen siparis yok", "success")
    else:
        for idx, row in pending_track.iterrows():
            with st.expander(f"{row['Order_ID']} - {row['Brand']}"):
                col1, col2 = st.columns(2)
                with col1:
                    tracking = st.text_input("Takip Numarasi", key=f"track_{idx}")
                with col2:
                    courier = st.selectbox("Kargo Firmasi", 
                                          ["Yurtici", "Aras", "MNG", "PTT", "Surat", "Diger"],
                                          key=f"courier_{idx}")
                
                if st.button("Kaydet ve Kargola", key=f"ship_{idx}"):
                    if tracking:
                        if OrderManager.update_tracking(row["Order_ID"], tracking, courier, 
                                                       st.session_state.admin_email, "admin"):
                            st.success("Kargo bilgisi kaydedildi")
                            time.sleep(0.5)
                            st.rerun()
                    else:
                        st.error("Takip numarasi giriniz")
    
    render_divider()
    
    # Complete orders
    st.markdown(f'<h3 style="margin-bottom: 16px;">{Icons.render("check_circle", "#10B981")} Tamamlanmaya Hazir</h3>', unsafe_allow_html=True)
    
    dispatched = df[df["Status"] == OrderStatus.DISPATCHED]
    
    if dispatched.empty:
        render_alert("Tamamlanacak siparis yok", "info")
    else:
        for idx, row in dispatched.iterrows():
            col1, col2, col3 = st.columns([2, 2, 1])
            col1.write(f"**{row['Order_ID']}** - {row['Brand']}")
            col2.write(f"Takip: {row['Tracking_Num']}")
            if col3.button("Tamamla", key=f"complete_{idx}"):
                OrderManager.update_status(row["Order_ID"], OrderStatus.COMPLETED,
                                          st.session_state.admin_email, "admin")
                st.rerun()

def render_admin_finance():
    """Render finance and payment management"""
    df_orders = Database.orders()
    df_payments = Database.payments()
    
    for brand_name, brand_data in BRANDS.items():
        with st.expander(f"{brand_name} Finans Yonetimi", expanded=True):
            brand_orders = df_orders[df_orders["Brand"] == brand_name] if not df_orders.empty else pd.DataFrame()
            
            # Completed orders total
            completed = brand_orders[brand_orders["Status"] == OrderStatus.COMPLETED] if not brand_orders.empty else pd.DataFrame()
            total_completed = completed["Brand_Payout"].sum() if not completed.empty else 0
            completed_count = len(completed)
            
            # Pending orders
            pending = brand_orders[~brand_orders["Status"].isin([OrderStatus.COMPLETED, OrderStatus.CANCELLED])] if not brand_orders.empty else pd.DataFrame()
            total_pending = pending["Brand_Payout"].sum() if not pending.empty else 0
            
            # Payments made
            brand_payments = df_payments[df_payments["Brand"] == brand_name] if not df_payments.empty else pd.DataFrame()
            total_paid = brand_payments["Amount"].sum() if not brand_payments.empty else 0
            
            # Net due
            net_due = total_completed - total_paid
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="nv-card" style="border-left: 4px solid var(--nv-accent);">
                    <div class="nv-order-label">Kesilmesi Gereken Fatura</div>
                    <div style="font-size: 24px; font-weight: 700;">{total_completed:,.2f} TL</div>
                    <div style="font-size: 11px; color: var(--nv-text-muted);">({completed_count} tamamlanan siparis)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="nv-card" style="border-left: 4px solid var(--nv-warning);">
                    <div class="nv-order-label">Bekleyen Siparisler</div>
                    <div style="font-size: 24px; font-weight: 700;">{total_pending:,.2f} TL</div>
                    <div style="font-size: 11px; color: var(--nv-text-muted);">(Henuz tamamlanmadi)</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Invoice description
            comm_rate = int(brand_data["commission"] * 100)
            invoice_desc = f"NATUVISIO satis komisyon hizmeti - {brand_name} - Siparis adedi: {completed_count} - Komisyon: %{comm_rate} - Net tutar: {total_completed:,.2f} TL"
            
            st.markdown("**Fatura Aciklamasi:**")
            st.code(invoice_desc)
            
            # Bank transfer info
            st.markdown("**Banka Transfer Bilgileri:**")
            st.info(f"**Alici:** {brand_data['account_name']}\n\n**IBAN:** {brand_data['iban']}\n\n**Tutar:** {net_due:,.2f} TL")
            
            if net_due > 0:
                if st.button(f"Odeme Yapildi ({net_due:,.0f} TL)", key=f"pay_{brand_name}"):
                    if PaymentManager.create(brand_name, net_due, "Bank Transfer", 
                                            f"Manual - {st.session_state.admin_email}"):
                        st.balloons()
                        st.success("Odeme kaydedildi")
                        time.sleep(1)
                        st.rerun()
            else:
                render_alert("Tum odemeler tamamlandi", "success")
    
    render_divider()
    
    # Payment history
    st.markdown("### Odeme Gecmisi")
    
    if not df_payments.empty:
        st.dataframe(
            df_payments[["Time_IST", "Brand", "Amount", "Method", "Invoice_Sent", "Invoice_Number"]],
            use_container_width=True,
            column_config={
                "Time_IST": "Tarih",
                "Brand": "Marka",
                "Amount": st.column_config.NumberColumn("Tutar", format="%.2f TL"),
                "Method": "Yontem",
                "Invoice_Sent": "Fatura Durumu",
                "Invoice_Number": "Fatura No"
            }
        )
        
        # Update invoice status
        with st.expander("Fatura Durumu Guncelle"):
            payment_ids = df_payments["Payment_ID"].tolist()
            selected_payment = st.selectbox("Odeme Sec", payment_ids)
            
            col1, col2 = st.columns(2)
            with col1:
                invoice_sent = st.selectbox("Fatura Kesildi mi?", ["No", "Yes"])
            with col2:
                invoice_number = st.text_input("Fatura Numarasi")
            
            invoice_date = st.date_input("Fatura Tarihi")
            
            if st.button("Guncelle"):
                if PaymentManager.update_invoice_status(selected_payment, invoice_sent, 
                                                       str(invoice_date), invoice_number):
                    st.success("Guncellendi")
                    st.rerun()
    else:
        render_alert("Henuz odeme kaydı yok", "info")

def render_admin_all_orders():
    """Render all orders view"""
    df = Database.orders()
    
    if df.empty:
        render_alert("Henuz siparis bulunmuyor", "info")
        return
    
    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        brand_filter = st.multiselect("Marka", list(BRANDS.keys()))
    with col_f2:
        status_filter = st.multiselect("Durum", [
            OrderStatus.PENDING, OrderStatus.ACCEPTED, OrderStatus.DISPATCHED,
            OrderStatus.COMPLETED, OrderStatus.REJECTED
        ])
    with col_f3:
        search = st.text_input("Ara (Siparis ID, Musteri)")
    
    filtered = df.copy()
    
    if brand_filter:
        filtered = filtered[filtered["Brand"].isin(brand_filter)]
    if status_filter:
        filtered = filtered[filtered["Status"].isin(status_filter)]
    if search:
        search_lower = search.lower()
        filtered = filtered[
            filtered["Order_ID"].str.lower().str.contains(search_lower, na=False) |
            filtered["Customer"].str.lower().str.contains(search_lower, na=False)
        ]
    
    st.markdown(f"**{len(filtered)}** siparis bulundu")
    
    st.dataframe(
        filtered[["Order_ID", "Time_IST", "Brand", "Customer", "Items", "Total_Value", 
                 "Brand_Payout", "Status", "Tracking_Num"]].sort_values("Time_IST", ascending=False),
        use_container_width=True,
        column_config={
            "Order_ID": "Siparis ID",
            "Time_IST": "Tarih",
            "Brand": "Marka",
            "Customer": "Musteri",
            "Items": "Urunler",
            "Total_Value": st.column_config.NumberColumn("Toplam", format="%.0f TL"),
            "Brand_Payout": st.column_config.NumberColumn("Marka Payi", format="%.0f TL"),
            "Status": "Durum",
            "Tracking_Num": "Takip No"
        }
    )
    
    # Export
    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "CSV Olarak Indir",
        csv_data,
        f"orders_{now_ist().strftime('%Y%m%d')}.csv",
        "text/csv"
    )

def render_admin_messages():
    """Render admin messaging interface"""
    st.markdown("### Partner Mesajlari")
    
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown("**Markalar**")
        
        for brand_name, brand_data in BRANDS.items():
            unread = 0
            messages = Database.messages()
            if not messages.empty:
                unread = len(messages[(messages["From_Brand"] == brand_name) & 
                                     (messages["To_Role"] == "admin") & 
                                     (messages["Read_By_Admin"] == "No")])
            
            badge_html = f'<span class="nv-unread-badge">{unread}</span>' if unread > 0 else ""
            
            is_active = st.session_state.active_conversation == brand_name
            
            if st.button(f"{brand_name} {badge_html}", key=f"conv_{brand_name}", 
                        use_container_width=True,
                        type="primary" if is_active else "secondary"):
                st.session_state.active_conversation = brand_name
                MessageSystem.mark_read_admin(brand_name)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        active_brand = st.session_state.active_conversation
        
        if active_brand:
            brand_data = BRANDS[active_brand]
            
            st.markdown(f"""
            <div class="nv-card-header">
                <div class="nv-conversation-avatar" style="background: {brand_data['color']};">
                    {active_brand[0]}
                </div>
                <span class="nv-card-title">{active_brand}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Message history
            conversation = MessageSystem.get_conversation(active_brand)
            
            st.markdown('<div style="height: 300px; overflow-y: auto; padding: 16px; background: rgba(255,255,255,0.3); border-radius: 8px; margin-bottom: 16px;">', unsafe_allow_html=True)
            
            if conversation.empty:
                st.markdown('<div style="text-align: center; color: var(--nv-text-muted); padding: 40px;">Henuz mesaj yok</div>', unsafe_allow_html=True)
            else:
                for _, msg in conversation.iterrows():
                    is_outgoing = msg["From_Role"] == "admin"
                    msg_class = "nv-message-outgoing" if is_outgoing else "nv-message-incoming"
                    
                    st.markdown(f"""
                    <div class="nv-message {msg_class}">
                        <div style="font-weight: 600; margin-bottom: 4px;">{msg['Subject']}</div>
                        <div>{msg['Body']}</div>
                        <div class="nv-message-meta">{msg['Time_IST']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Send message
            with st.form(f"reply_{active_brand}"):
                subject = st.text_input("Konu")
                body = st.text_area("Mesaj", height=100)
                
                # Order reference
                df_orders = Database.orders()
                brand_orders = df_orders[df_orders["Brand"] == active_brand] if not df_orders.empty else pd.DataFrame()
                order_options = ["Genel"] + brand_orders["Order_ID"].tolist() if not brand_orders.empty else ["Genel"]
                order_ref = st.selectbox("Ilgili Siparis", order_options)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("Gonder", type="primary"):
                        if subject and body:
                            MessageSystem.send(
                                from_role="admin",
                                from_brand="NATUVISIO",
                                to_role="partner",
                                to_brand=active_brand,
                                subject=subject,
                                body=body,
                                order_id=order_ref if order_ref != "Genel" else ""
                            )
                            st.success("Mesaj gonderildi")
                            st.rerun()
                        else:
                            st.error("Konu ve mesaj giriniz")
                
                with col2:
                    # Quick actions
                    email_link = generate_email_link(
                        brand_data["email"],
                        f"NATUVISIO: {subject}",
                        body
                    )
                    wa_link = generate_whatsapp_link(
                        brand_data["phone"],
                        f"NATUVISIO: {subject}\n\n{body}"
                    )
                    
                    st.markdown(f"""
                    <div style="display: flex; gap: 8px; margin-top: 8px;">
                        <a href="{email_link}" class="nv-quick-action nv-quick-action-email">
                            {Icons.render("mail", "#1D4ED8", 14)} E-posta
                        </a>
                        <a href="{wa_link}" target="_blank" class="nv-quick-action nv-quick-action-whatsapp">
                            {Icons.render("phone", "#128C7E", 14)} WhatsApp
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 80px 40px; color: var(--nv-text-muted);">
                <div style="margin-bottom: 12px; opacity: 0.5;">Konusma Secilmedi</div>
                <div style="font-size: 13px;">Soldaki listeden bir marka secin</div>
            </div>
            """, unsafe_allow_html=True)

def render_admin_analytics():
    """Render analytics dashboard"""
    df = Database.orders()
    
    if df.empty:
        render_alert("Analiz icin yeterli veri yok", "info")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Marka Bazli Satis**")
        brand_sales = df.groupby("Brand")["Total_Value"].sum()
        st.bar_chart(brand_sales)
    
    with col2:
        st.markdown("**Durum Dagilimi**")
        status_dist = df["Status"].value_counts()
        st.bar_chart(status_dist)
    
    render_divider()
    
    # Summary stats
    st.markdown("### Ozet Istatistikler")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_order = df["Total_Value"].mean()
        render_metric("Ortalama Siparis", f"{avg_order:,.0f} TL", "bar_chart")
    
    with col2:
        total_comm = df["Commission_Amt"].sum()
        render_metric("Toplam Komisyon", f"{total_comm:,.0f} TL", "dollar", "#4ECDC4")
    
    with col3:
        completed_rate = len(df[df["Status"] == OrderStatus.COMPLETED]) / len(df) * 100 if len(df) > 0 else 0
        render_metric("Tamamlanma Orani", f"%{completed_rate:.1f}", "check_circle", "#10B981")
    
    with col4:
        render_metric("Toplam Marka", str(len(BRANDS)), "users")

def render_admin_logs():
    """Render system logs"""
    df = Database.logs()
    
    if df.empty:
        render_alert("Henuz log kaydı yok", "info")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        action_filter = st.multiselect("Islem Tipi", df["Action"].unique().tolist())
    with col2:
        role_filter = st.multiselect("Rol", df["Role"].unique().tolist())
    with col3:
        search = st.text_input("Ara")
    
    filtered = df.copy()
    
    if action_filter:
        filtered = filtered[filtered["Action"].isin(action_filter)]
    if role_filter:
        filtered = filtered[filtered["Role"].isin(role_filter)]
    if search:
        search_lower = search.lower()
        filtered = filtered[
            filtered.apply(lambda row: search_lower in str(row.values).lower(), axis=1)
        ]
    
    st.markdown(f"**{len(filtered)}** kayit bulundu")
    
    st.dataframe(
        filtered[["Time_IST", "Action", "User", "Role", "Brand", "Order_ID", "Details"]].sort_values("Time_IST", ascending=False),
        use_container_width=True,
        column_config={
            "Time_IST": "Tarih/Saat",
            "Action": "Islem",
            "User": "Kullanici",
            "Role": "Rol",
            "Brand": "Marka",
            "Order_ID": "Siparis ID",
            "Details": "Detaylar"
        },
        height=500
    )
    
    # Export
    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Loglari Indir",
        csv_data,
        f"system_logs_{now_ist().strftime('%Y%m%d')}.csv",
        "text/csv"
    )

# ============================================================================
# PARTNER DASHBOARD
# ============================================================================

def render_partner_dashboard():
    """Render the partner dashboard"""
    load_design_system()
    
    brand = st.session_state.partner_brand
    brand_data = BRANDS[brand]
    
    # Header
    col_h1, col_h2 = st.columns([6, 1])
    
    with col_h1:
        render_header("Partner Portali", brand, brand_data["color"])
    
    with col_h2:
        unread = MessageSystem.get_unread_count_brand(brand)
        if unread > 0:
            st.markdown(f'<span class="nv-unread-badge">{unread}</span>', unsafe_allow_html=True)
        
        if st.button("Cikis"):
            log_action("LOGOUT", st.session_state.partner_email, "partner", brand)
            st.session_state.partner_logged_in = False
            st.session_state.partner_brand = None
            st.session_state.partner_email = None
            st.rerun()
    
    # Load data
    df_orders = Database.orders()
    brand_orders = df_orders[df_orders["Brand"] == brand] if not df_orders.empty else pd.DataFrame()
    
    # Alerts
    new_orders = brand_orders[brand_orders["Status"] == OrderStatus.PENDING] if not brand_orders.empty else pd.DataFrame()
    if len(new_orders) > 0:
        render_alert(f"{len(new_orders)} yeni siparis bekliyor", "danger", "Hemen onaylayin")
    
    unread_msgs = MessageSystem.get_unread_count_brand(brand)
    if unread_msgs > 0:
        render_alert(f"{unread_msgs} okunmamis mesaj var", "info")
    
    # Metrics
    total_orders = len(brand_orders)
    total_earnings = brand_orders["Brand_Payout"].sum() if not brand_orders.empty else 0
    completed = len(brand_orders[brand_orders["Status"] == OrderStatus.COMPLETED]) if not brand_orders.empty else 0
    pending = len(brand_orders[brand_orders["Status"].isin([OrderStatus.PENDING, OrderStatus.ACCEPTED])]) if not brand_orders.empty else 0
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        render_metric("Toplam Siparis", str(total_orders), "package", brand_data["color"])
    with col_m2:
        render_metric("Toplam Kazanc", f"{total_earnings:,.0f} TL", "dollar", "#4ECDC4")
    with col_m3:
        render_metric("Tamamlanan", str(completed), "check_circle", "#10B981")
    with col_m4:
        render_metric("Bekleyen", str(pending), "clock", "#F59E0B")
    
    render_divider()
    
    # Tabs
    tabs = st.tabs([
        "Yeni Siparisler",
        "Kargo Takip",
        "Tamamlanan",
        "Finansal Ozet",
        "Mesajlar",
        "Islem Kayitlari"
    ])
    
    with tabs[0]:
        render_partner_inbox(brand, brand_orders)
    with tabs[1]:
        render_partner_shipping(brand, brand_orders)
    with tabs[2]:
        render_partner_completed(brand, brand_orders)
    with tabs[3]:
        render_partner_finance(brand, brand_orders)
    with tabs[4]:
        render_partner_messages(brand)
    with tabs[5]:
        render_partner_logs(brand)
    
    render_footer()

def render_partner_inbox(brand, brand_orders):
    """Render partner inbox for new orders"""
    new_orders = brand_orders[brand_orders["Status"] == OrderStatus.PENDING] if not brand_orders.empty else pd.DataFrame()
    
    if new_orders.empty:
        render_alert("Bekleyen yeni siparis yok", "success")
        return
    
    for idx, row in new_orders.iterrows():
        st.markdown(f"""
        <div class="nv-order-card">
            <div class="nv-order-header">
                <div>
                    <span class="nv-order-id">{row['Order_ID']}</span>
                    <div class="nv-order-time">{row['Time_IST']}</div>
                </div>
                {render_status_badge(row['Status'])}
            </div>
            <div class="nv-order-details">
                <div>
                    <div class="nv-order-label">Musteri</div>
                    <div class="nv-order-value">{row['Customer']}</div>
                </div>
                <div>
                    <div class="nv-order-label">Telefon</div>
                    <div class="nv-order-value">{row['Phone']}</div>
                </div>
                <div>
                    <div class="nv-order-label">Adres</div>
                    <div class="nv-order-value">{row['Address']}</div>
                </div>
                <div>
                    <div class="nv-order-label">Urunler</div>
                    <div class="nv-order-value">{row['Items']}</div>
                </div>
            </div>
            <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--nv-glass-border);">
                <div class="nv-finance-row">
                    <span class="nv-finance-label">Siparis Toplami</span>
                    <span class="nv-finance-value">{row['Total_Value']:,.0f} TL</span>
                </div>
                <div class="nv-finance-row">
                    <span class="nv-finance-label">Komisyon (%{int(row['Commission_Rate']*100)})</span>
                    <span class="nv-finance-value" style="color: var(--nv-warning);">-{row['Commission_Amt']:,.0f} TL</span>
                </div>
                <div class="nv-finance-row">
                    <span class="nv-finance-label">Net Kazanc</span>
                    <span class="nv-finance-value highlight">{row['Brand_Payout']:,.0f} TL</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Siparisi Onayla", key=f"accept_{row['Order_ID']}", type="primary"):
                df = Database.orders()
                mask = df["Order_ID"] == row["Order_ID"]
                if mask.any():
                    OrderManager.update_status(row["Order_ID"], OrderStatus.ACCEPTED,
                                              st.session_state.partner_email, "partner", brand)
                    st.success("Siparis onaylandi! Simdi kargo bilgilerini girebilirsiniz.")
                    time.sleep(1)
                    st.rerun()
        
        with col2:
            if st.button("Siparisi Reddet", key=f"reject_{row['Order_ID']}"):
                df = Database.orders()
                mask = df["Order_ID"] == row["Order_ID"]
                if mask.any():
                    OrderManager.update_status(row["Order_ID"], OrderStatus.REJECTED,
                                              st.session_state.partner_email, "partner", brand,
                                              "Marka tarafindan reddedildi")
                    st.warning("Siparis reddedildi")
                    time.sleep(1)
                    st.rerun()
        
        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

def render_partner_shipping(brand, brand_orders):
    """Render shipping management for partner"""
    accepted = brand_orders[brand_orders["Status"] == OrderStatus.ACCEPTED] if not brand_orders.empty else pd.DataFrame()
    
    if accepted.empty:
        render_alert("Kargoya verilecek siparis yok", "info", "Oncelikle yeni siparisleri onaylayin")
        return
    
    for idx, row in accepted.iterrows():
        with st.expander(f"{row['Order_ID']} - {row['Customer']}", expanded=True):
            st.markdown(f"""
            <div style="font-size: 13px; margin-bottom: 16px;">
                <strong>Urunler:</strong> {row['Items']}<br>
                <strong>Adres:</strong> {row['Address']}<br>
                <strong>Kazanc:</strong> <span style="color: var(--nv-accent); font-weight: 700;">{row['Brand_Payout']:,.0f} TL</span>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                tracking = st.text_input("Kargo Takip Numarasi", key=f"pt_track_{row['Order_ID']}")
            with col2:
                courier = st.selectbox("Kargo Firmasi", 
                                      ["Yurtici", "Aras", "MNG", "PTT", "Surat", "Diger"],
                                      key=f"pt_courier_{row['Order_ID']}")
            
            if st.button("Kargoya Verildi", key=f"pt_ship_{row['Order_ID']}", type="primary"):
                if tracking:
                    if OrderManager.update_tracking(row["Order_ID"], tracking, courier,
                                                   st.session_state.partner_email, "partner", brand):
                        st.success("Kargo bilgisi kaydedildi!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("Lutfen takip numarasi giriniz")

def render_partner_completed(brand, brand_orders):
    """Render completed orders for partner"""
    completed = brand_orders[brand_orders["Status"].isin([OrderStatus.DISPATCHED, OrderStatus.COMPLETED, OrderStatus.COMPLETED_BRAND])] if not brand_orders.empty else pd.DataFrame()
    
    if completed.empty:
        render_alert("Henuz tamamlanan siparis yok", "info")
        return
    
    st.dataframe(
        completed[["Order_ID", "Time_IST", "Customer", "Items", "Brand_Payout", "Status", "Tracking_Num"]],
        use_container_width=True,
        column_config={
            "Order_ID": "Siparis ID",
            "Time_IST": "Tarih",
            "Customer": "Musteri",
            "Items": "Urunler",
            "Brand_Payout": st.column_config.NumberColumn("Kazanc", format="%.0f TL"),
            "Status": "Durum",
            "Tracking_Num": "Takip No"
        }
    )

def render_partner_finance(brand, brand_orders):
    """Render financial summary for partner"""
    df_payments = Database.payments()
    brand_payments = df_payments[df_payments["Brand"] == brand] if not df_payments.empty else pd.DataFrame()
    
    # Calculate totals
    completed = brand_orders[brand_orders["Status"] == OrderStatus.COMPLETED] if not brand_orders.empty else pd.DataFrame()
    total_earned = completed["Brand_Payout"].sum() if not completed.empty else 0
    
    total_paid = brand_payments["Amount"].sum() if not brand_payments.empty else 0
    balance = total_earned - total_paid
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_metric("Toplam Hakedis", f"{total_earned:,.0f} TL", "dollar", "#4ECDC4")
    with col2:
        render_metric("Odenen", f"{total_paid:,.0f} TL", "check_circle", "#10B981")
    with col3:
        render_metric("Kalan Bakiye", f"{balance:,.0f} TL", "clock", "#F59E0B")
    
    render_divider()
    
    st.markdown("### Odeme Gecmisi")
    
    if not brand_payments.empty:
        st.dataframe(
            brand_payments[["Time_IST", "Amount", "Method", "Reference", "Status"]],
            use_container_width=True,
            column_config={
                "Time_IST": "Tarih",
                "Amount": st.column_config.NumberColumn("Tutar", format="%.2f TL"),
                "Method": "Yontem",
                "Reference": "Referans",
                "Status": "Durum"
            }
        )
    else:
        render_alert("Henuz odeme alinamadi", "info")

def render_partner_messages(brand):
    """Render messaging interface for partner"""
    # Mark messages as read
    MessageSystem.mark_read_brand(brand)
    
    st.markdown("### Yonetici ile Iletisim")
    
    # Message history
    conversation = MessageSystem.get_conversation(brand)
    
    st.markdown('<div style="height: 350px; overflow-y: auto; padding: 16px; background: rgba(255,255,255,0.3); border-radius: 8px; margin-bottom: 16px;">', unsafe_allow_html=True)
    
    if conversation.empty:
        st.markdown('<div style="text-align: center; color: var(--nv-text-muted); padding: 60px;">Henuz mesaj yok. Asagidan mesaj gondererek iletisime gecin.</div>', unsafe_allow_html=True)
    else:
        for _, msg in conversation.iterrows():
            is_outgoing = msg["From_Role"] == "partner"
            msg_class = "nv-message-outgoing" if is_outgoing else "nv-message-incoming"
            sender = brand if is_outgoing else "NATUVISIO"
            
            st.markdown(f"""
            <div class="nv-message {msg_class}">
                <div style="font-size: 10px; opacity: 0.7; margin-bottom: 4px;">{sender}</div>
                <div style="font-weight: 600; margin-bottom: 4px;">{msg['Subject']}</div>
                <div>{msg['Body']}</div>
                <div class="nv-message-meta">{msg['Time_IST']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Send message form
    with st.form("partner_message"):
        subject = st.text_input("Konu")
        body = st.text_area("Mesajiniz", height=100)
        
        # Order reference
        df_orders = Database.orders()
        brand_orders = df_orders[df_orders["Brand"] == brand] if not df_orders.empty else pd.DataFrame()
        order_options = ["Genel"] + brand_orders["Order_ID"].tolist() if not brand_orders.empty else ["Genel"]
        order_ref = st.selectbox("Ilgili Siparis (Opsiyonel)", order_options)
        
        if st.form_submit_button("Mesaj Gonder", type="primary"):
            if subject and body:
                MessageSystem.send(
                    from_role="partner",
                    from_brand=brand,
                    to_role="admin",
                    to_brand="NATUVISIO",
                    subject=subject,
                    body=body,
                    order_id=order_ref if order_ref != "Genel" else ""
                )
                st.success("Mesajiniz gonderildi!")
                st.rerun()
            else:
                st.error("Lutfen konu ve mesaj giriniz")

def render_partner_logs(brand):
    """Render activity logs for partner"""
    df = Database.logs()
    
    if df.empty:
        render_alert("Henuz islem kaydı yok", "info")
        return
    
    # Filter by brand
    brand_logs = df[(df["Brand"] == brand) | (df["User"] == st.session_state.partner_email)]
    
    if brand_logs.empty:
        render_alert("Markaniza ait kayit bulunamadi", "info")
        return
    
    st.dataframe(
        brand_logs[["Time_IST", "Action", "Order_ID", "Details"]].sort_values("Time_IST", ascending=False),
        use_container_width=True,
        column_config={
            "Time_IST": "Tarih/Saat",
            "Action": "Islem",
            "Order_ID": "Siparis ID",
            "Details": "Detaylar"
        },
        height=400
    )

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    init_session()
    Database.init_all()
    
    if st.session_state.admin_logged_in:
        render_admin_dashboard()
    elif st.session_state.partner_logged_in:
        render_partner_dashboard()
    else:
        render_login()

if __name__ == "__main__":
    main()
