import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import time
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO YÖNETİM SİSTEMİ - V6.1 (LOGO FIX + OS FOOTER)
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Admin OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 1. AYARLAR (CONFIG)
# ============================================================================

ADMIN_PASS = "admin2025"
CSV_ORDERS = "orders_complete.csv"
CSV_PAYMENTS = "brand_payments.csv" 
CSV_INVOICES = "brand_invoices.csv" 
CSV_LOGS = "system_logs.csv"
PHI = 1.618

FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

# FIXED LOGO URL (PNG Format for Web Compatibility)
LOGO_URL = "https://res.cloudinary.com/deb1j92hy/image/upload/f_auto,q_auto/v1764805291/natuvisio_logo_gtqtfs.png"
BG_IMAGE = "https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp"

BRANDS = {
    "HAKI HEAL": {
        "phone": "601158976276",
        "color": "#4ECDC4",
        "commission": 0.15,
        "iban": "TR90 0006 1000 0000 1234 5678 90",
        "account_name": "Haki Heal Ltd. Şti.",
        "products": {
            "HAKI HEAL KREM": {"sku": "SKU-HAKI-CRM-01", "price": 450},
            "HAKI HEAL VÜCUT LOSYONU": {"sku": "SKU-HAKI-BODY-01", "price": 380},
            "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP-01", "price": 120}
        }
    },
    "AURORACO": {
        "phone": "601158976276",
        "color": "#FF6B6B",
        "commission": 0.20,
        "iban": "TR90 0006 2000 0000 9876 5432 10",
        "account_name": "Auroraco Gıda A.Ş.",
        "products": {
            "AURORACO MATCHA EZMESİ": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO KAKAO EZMESİ": {"sku": "SKU-AUR-CACAO", "price": 550},
            "AURORACO SÜPER GIDA": {"sku": "SKU-AUR-SUPER", "price": 800}
        }
    },
    "LONGEVICALS": {
        "phone": "601158976276",
        "color": "#95E1D3",
        "commission": 0.12,
        "iban": "TR90 0001 5000 0000 1122 3344 55",
        "account_name": "Longevicals Sağlık Ürünleri",
        "products": {
            "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
            "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
        }
    }
}

# ============================================================================
# 2. İKON SETİ (ICONS)
# ============================================================================

def get_icon(name, color="#5b7354", size=24):
    icons = {
        "mountain": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M3 20L9 8L12 14L15 6L21 20H3Z"/></svg>',
        "alert": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3"><path d="M20 6L9 17L4 12"/></svg>',
        "bill": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><line x1="6" y1="8" x2="6" y2="8"/><line x1="10" y1="8" x2="18" y2="8"/><line x1="6" y1="12" x2="6" y2="12"/><line x1="10" y1="12" x2="18" y2="12"/><line x1="6" y1="16" x2="6" y2="16"/><line x1="10" y1="16" x2="18" y2="16"/></svg>',
        "money": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "clock": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "activity": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        "log": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>'
    }
    return icons.get(name, "")

# ============================================================================
# 3. CSS & RETINA THEME ENGINE
# ============================================================================

def load_css(theme="light"):
    if theme == "light":
        overlay_color = "rgba(255, 255, 255, 0.15)"
        glass_bg = "rgba(255, 255, 255, 0.65)"
        glass_border = "rgba(91, 115, 84, 0.2)"
        text_color = "#0f172a"
        subtext_color = "#475569"
        input_bg = "rgba(255, 255, 255, 0.75)"
        shadow = "0 4px 24px rgba(0, 0, 0, 0.06)"
        btn_gradient = "linear-gradient(135deg, #5b7354, #4a6b45)"
    else:
        overlay_color = "rgba(15, 23, 42, 0.85)"
        glass_bg = "rgba(255, 255, 255, 0.04)"
        glass_border = "rgba(255, 255, 255, 0.08)"
        text_color = "#ffffff"
        subtext_color = "rgba(255, 255, 255, 0.6)"
        input_bg = "rgba(0, 0, 0, 0.3)"
        shadow = "0 8px 32px rgba(0, 0, 0, 0.3)"
        btn_gradient = "linear-gradient(135deg, #4ECDC4, #44A08D)"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        .stApp {{
            background-image: linear-gradient({overlay_color}, {overlay_color}), 
                              url("{BG_IMAGE}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: {text_color};
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        /* RADIANT REMINDER BUTTON */
        .radiant-reminder {{
            background: rgba(255, 0, 0, 0.08);
            border-left: 3px solid #ef4444;
            color: #b91c1c;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-weight: 600;
            font-size: 13px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            animation: pulse-red 1.8s infinite ease-in-out;
            cursor: pointer;
            text-decoration: none;
            backdrop-filter: blur(8px);
        }}
        
        @keyframes pulse-red {{
            0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }}
            70% {{ box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
        }}

        .glass-card {{
            background: {glass_bg};
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid {glass_border};
            border-radius: {FIBO['sm']}px;
            padding: {FIBO['md']}px;
            margin-bottom: {FIBO['sm']}px;
            box-shadow: {shadow};
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }}
        
        .glass-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(0,0,0,0.08);
        }}
        
        .metric-value {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 26px;
            font-weight: 800;
            color: {text_color};
            letter-spacing: -0.02em;
        }}
        
        .metric-label {{
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: {subtext_color};
            font-weight: 700;
            margin-bottom: 4px;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: {text_color} !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em !important;
        }}
        
        div.stButton > button {{
            background: {btn_gradient} !important;
            color: white !important;
            border: none !important;
            padding: {FIBO['sm']}px {FIBO['md']}px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            font-size: 13px !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(91, 115, 84, 0.25) !important;
        }}
        
        div.stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(91, 115, 84, 0.4) !important;
        }}
        
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {{
            background: {input_bg} !important;
            border: 1px solid {glass_border} !important;
            color: {text_color} !important;
            border-radius: 8px !important;
            font-size: 14px !important;
        }}
        
        /* RADIANT SEPARATOR */
        .radiant-line {{
            background: linear-gradient(90deg, rgba(91,115,84,0), rgba(91,115,84,0.3), rgba(91,115,84,0));
            height: 1px;
            margin: 35px 0;
            width: 100%;
        }}
        
        .stCheckbox label {{ color: {text_color} !important; }}
        #MainMenu, header, footer {{ visibility: hidden; }}
        
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(91,115,84,0.4); border-radius: 3px; }}
        
        /* OS FOOTER */
        .os-footer {{
            margin-top: 50px;
            padding: 30px;
            border-top: 1px solid rgba(91, 115, 84, 0.15);
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            color: {subtext_color};
            background: {glass_bg};
            backdrop-filter: blur(10px);
        }}
        
        .os-footer-logo {{
            height: 24px;
            margin-bottom: 15px;
            opacity: 0.8;
        }}
        
        .os-status-dot {{
            height: 8px;
            width: 8px;
            background-color: #10B981;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
        }}
        
        .os-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            max-width: 900px;
            margin: 0 auto;
            text-align: left;
        }}
    </style>
    """, unsafe_allow_html=True)

def radiant_line():
    st.markdown('<div class="radiant-line"></div>', unsafe_allow_html=True)

# ============================================================================
# 4. VERİTABANI YÖNETİMİ
# ============================================================================

def init_databases():
    if not os.path.exists(CSV_ORDERS):
        pd.DataFrame(columns=[
            "Order_ID", "Time", "Brand", "Customer", "Phone", "Address",
            "Items", "Total_Value", "Commission_Rate", "Commission_Amt",
            "Brand_Payout", "Status", "WhatsApp_Sent", "Tracking_Num",
            "Priority", "Notes", "Created_By", "Last_Modified"
        ]).to_csv(CSV_ORDERS, index=False)
    
    if not os.path.exists(CSV_PAYMENTS):
        pd.DataFrame(columns=[
            "Payment_ID", "Time", "Brand", "Amount", "Method", "Reference", 
            "Status", "Proof_File", "Notes", 
            "Fatura_Sent", "Fatura_Date", "Fatura_Explanation"
        ]).to_csv(CSV_PAYMENTS, index=False)
    else:
        df = pd.read_csv(CSV_PAYMENTS)
        if "Fatura_Sent" not in df.columns:
            df["Fatura_Sent"] = "No"
            df["Fatura_Date"] = ""
            df["Fatura_Explanation"] = ""
            df.to_csv(CSV_PAYMENTS, index=False)
        
    if not os.path.exists(CSV_INVOICES):
        pd.DataFrame(columns=[
            "Invoice_ID", "Time", "Brand", "Amount", "Date_Range", 
            "Invoice_Number", "Status", "Notes"
        ]).to_csv(CSV_INVOICES, index=False)
    
    if not os.path.exists(CSV_LOGS):
        pd.DataFrame(columns=[
            "Log_ID", "Time", "Action", "User", "Order_ID", "Details"
        ]).to_csv(CSV_LOGS, index=False)

def load_orders():
    try: return pd.read_csv(CSV_ORDERS)
    except: return pd.DataFrame()

def load_payments():
    try: return pd.read_csv(CSV_PAYMENTS)
    except: return pd.DataFrame()

def load_invoices():
    try: return pd.read_csv(CSV_INVOICES)
    except: return pd.DataFrame()

def load_logs():
    try: return pd.read_csv(CSV_LOGS)
    except: return pd.DataFrame(columns=["Log_ID", "Time", "Action", "User", "Order_ID", "Details"])

def save_order(order_data):
    try:
        df = load_orders()
        df = pd.concat([df, pd.DataFrame([order_data])], ignore_index=True)
        df.to_csv(CSV_ORDERS, index=False)
        log_action("SİPARİŞ_OLUŞTURULDU", "admin", order_data['Order_ID'], f"Oluşturuldu: {order_data['Order_ID']}")
        return True
    except Exception as e:
        st.error(f"Kayıt hatası: {e}")
        return False

def update_orders(df):
    try:
        df.to_csv(CSV_ORDERS, index=False)
        return True
    except: return False

def save_payment(payment_data):
    try:
        df = load_payments()
        df = pd.concat([df, pd.DataFrame([payment_data])], ignore_index=True)
        df.to_csv(CSV_PAYMENTS, index=False)
        log_action("ÖDEME_KAYDI", "admin", "", f"{payment_data['Brand']} ödemesi kaydedildi")
        return True
    except: return False

def update_payments(df):
    try:
        df.to_csv(CSV_PAYMENTS, index=False)
        return True
    except: return False

def save_invoice(invoice_data):
    try:
        df = load_invoices()
        df = pd.concat([df, pd.DataFrame([invoice_data])], ignore_index=True)
        df.to_csv(CSV_INVOICES, index=False)
        log_action("FATURA_KESİLDİ", "admin", "", f"{invoice_data['Brand']} faturası oluşturuldu")
        return True
    except: return False

def log_action(action, user, order_id, details):
    try:
        df = load_logs()
        log_entry = {
            'Log_ID': f"LOG-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Action': action,
            'User': user,
            'Order_ID': order_id,
            'Details': details
        }
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        df.to_csv(CSV_LOGS, index=False)
    except: pass

def export_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# ============================================================================
# 5. OTURUM YÖNETİMİ
# ============================================================================

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'brand_lock' not in st.session_state:
    st.session_state.brand_lock = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'light' 

# ============================================================================
# 6. GİRİŞ EKRANI
# ============================================================================

def login_screen():
    load_css(st.session_state.theme)
    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:20px;">
            <img src="{LOGO_URL}" style="width:120px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));" onerror="this.style.display='none'">
            <div style="font-family:'Space Grotesk'; font-size:32px; font-weight:800; color:#5b7354; margin-top:10px;">NATUVISIO</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['xl']}px;">
            <h2>YÖNETİM GİRİŞİ</h2>
            <p style="opacity: 0.6; font-size: 13px; margin-bottom:20px;">GÜVENLİ OPERASYON SİSTEMİ v6.1</p>
        """, unsafe_allow_html=True)
        
        password = st.text_input("Erişim Şifresi", type="password", key="login", label_visibility="collapsed", placeholder="Şifrenizi Giriniz")
        
        if st.button("🔓 SİSTEME GİRİŞ", use_container_width=True):
            if password == ADMIN_PASS:
                st.session_state.admin_logged_in = True
                log_action("GİRİŞ", "admin", "", "Başarılı giriş")
                st.rerun()
            else:
                st.error("❌ Hatalı şifre")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# 7. ANA PANEL (DASHBOARD)
# ============================================================================

def dashboard():
    load_css(st.session_state.theme)
    init_databases()
    
    # --- HEADER ---
    col_h1, col_h2, col_h3 = st.columns([6, 1, 1])
    with col_h1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <img src="{LOGO_URL}" style="height:45px;" onerror="this.style.display='none'">
            <div>
                <h1 style="margin:0; font-size:24px;">YÖNETİM MERKEZİ</h1>
                <span style="font-size: 11px; opacity: 0.7; letter-spacing:1px; font-weight:600;">RETINA EDITION</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h2:
        if st.button("☀️/🌙", key="theme_toggle"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()

    with col_h3:
        if st.button("🚪 Çıkış"):
            st.session_state.admin_logged_in = False
            st.session_state.cart = []
            st.rerun()
            
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # --- RADIANT REMINDERS ---
    df_orders = load_orders()
    pending_notify = len(df_orders[df_orders['WhatsApp_Sent'] == 'NO'])
    pending_track = len(df_orders[(df_orders['Status'] == 'Notified') & (df_orders['Tracking_Num'].isna())])
    
    if pending_notify > 0:
        st.markdown(f"""<div class="radiant-reminder">⚠️ {pending_notify} SİPARİŞ BİLDİRİM BEKLİYOR! <span style="font-size:10px; opacity:0.7;">OPERASYON'A GİT</span></div>""", unsafe_allow_html=True)
    if pending_track > 0:
        st.markdown(f"""<div class="radiant-reminder">📦 {pending_track} KARGO TAKİP NO EKSİK! <span style="font-size:10px; opacity:0.7;">OPERASYON'A GİT</span></div>""", unsafe_allow_html=True)

    # --- METRICS ---
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    total_rev = df_orders['Total_Value'].sum() if not df_orders.empty else 0
    total_comm = df_orders['Commission_Amt'].sum() if not df_orders.empty else 0
    pending_count = len(df_orders[df_orders['Status'] == 'Pending'])
    
    with col_m1:
        st.markdown(f"""<div class="glass-card" style="text-align:center;"><div class="metric-label">TOPLAM CİRO</div><div class="metric-value">{total_rev:,.0f}₺</div></div>""", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""<div class="glass-card" style="text-align:center; border-top: 3px solid #4ECDC4;"><div class="metric-label">NET KOMİSYON</div><div class="metric-value" style="color:#4ECDC4;">{total_comm:,.0f}₺</div></div>""", unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""<div class="glass-card" style="text-align:center; border-top: 3px solid #F59E0B;"><div class="metric-label">BEKLEYEN İŞLEM</div><div class="metric-value" style="color:#F59E0B;">{pending_count}</div></div>""", unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""<div class="glass-card" style="text-align:center;"><div class="metric-label">TOPLAM SİPARİŞ</div><div class="metric-value">{len(df_orders)}</div></div>""", unsafe_allow_html=True)

    radiant_line()

    tabs = st.tabs([
        "🚀 YENİ SEVKİYAT", 
        "✅ OPERASYON", 
        "🏦 FATURA & ÖDEME", 
        "📦 TÜM SİPARİŞLER",
        "📊 ANALİTİK",
        "❔ REHBER",
        "📜 LOG KAYITLARI"
    ])
    
    with tabs[0]: render_new_dispatch()
    with tabs[1]: render_operations()
    with tabs[2]: render_brand_payout_hq()
    with tabs[3]: render_all_orders()
    with tabs[4]: render_analytics()
    with tabs[5]: render_faqs()
    with tabs[6]: render_logs_advanced()

    # --- OS FOOTER (NEW v6.1) ---
    render_os_footer()

def render_os_footer():
    st.markdown(f"""
    <div class="os-footer">
        <img src="{LOGO_URL}" class="os-footer-logo" onerror="this.style.display='none'">
        <div class="os-grid">
            <div>
                <strong>NATUVISIO ADMIN OS v6.1</strong><br>
                <span class="os-status-dot"></span> System Operational<br>
                Last Sync: {datetime.now().strftime('%H:%M:%S')}
            </div>
            <div>
                <strong>DATA INTEGRITY</strong><br>
                Orders: orders_complete.csv<br>
                Financials: brand_payments.csv
            </div>
            <div>
                <strong>OPERATIONS</strong><br>
                Support: operations@natuvisio.com<br>
                Emergency: +90 535 926 49 91
            </div>
            <div>
                <strong>SECURITY</strong><br>
                Log Active. Unauthorized access prohibited.<br>
                Internal Use Only.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# 8. YENİ SEVKİYAT MODÜLÜ
# ============================================================================

def render_new_dispatch():
    col_L, col_R = st.columns([PHI, 1])
    
    with col_L:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Müşteri Bilgileri")
        col_n, col_p = st.columns(2)
        with col_n: cust_name = st.text_input("Ad Soyad", key="cust_name")
        with col_p: cust_phone = st.text_input("Telefon", key="cust_phone")
        cust_addr = st.text_area("Adres", key="cust_addr", height=80)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🛒 Ürün Seçimi")
        
        if st.session_state.cart:
            st.info(f"🔒 Kilitli Marka: {st.session_state.brand_lock}")
            active_brand = st.session_state.brand_lock
        else:
            active_brand = st.selectbox("Marka Seçiniz", list(BRANDS.keys()), key="brand_sel")
            
        brand_data = BRANDS[active_brand]
        products = list(brand_data["products"].keys())
        
        col_p, col_q = st.columns([3, 1])
        with col_p: prod = st.selectbox("Ürün", products, key="prod_sel")
        with col_q: qty = st.number_input("Adet", 1, value=1, key="qty")
        
        prod_details = brand_data["products"][prod]
        unit_price = prod_details['price']
        line_total = unit_price * qty
        comm_amt = line_total * brand_data['commission']
        payout = line_total - comm_amt
        
        if st.button("➕ Sepete Ekle"):
            st.session_state.cart.append({
                "brand": active_brand,
                "product": prod,
                "sku": prod_details['sku'],
                "qty": qty,
                "unit_price": unit_price,
                "subtotal": line_total,
                "comm_amt": comm_amt,
                "payout": payout
            })
            st.session_state.brand_lock = active_brand
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_R:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📦 Sepet Özeti")
        
        if st.session_state.cart:
            for item in st.session_state.cart:
                item_html = f"""
<div style="background: rgba(128,128,128,0.05); border-radius: 8px; padding: 12px; margin-bottom: 10px; border: 1px solid rgba(128,128,128,0.1);">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
<span style="font-weight:700; font-size:14px;">{item['product']}</span>
<span style="background:rgba(78,205,196,0.2); color:#4ECDC4; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:bold;">x{item['qty']}</span>
</div>
<div style="font-size:12px; opacity:0.7; margin-bottom:8px; border-bottom:1px dashed rgba(128,128,128,0.3); padding-bottom:8px;">
{item['unit_price']:,.0f}₺ <span style="opacity:0.5;">(birim)</span> &times; {item['qty']} = <strong>{item['subtotal']:,.0f}₺</strong>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; font-size:11px;">
<div style="background:rgba(252, 211, 77, 0.1); padding:4px; border-radius:4px; text-align:center;">
<div style="color:#FCD34D; opacity:0.8;">Komisyon</div>
<div style="color:#FCD34D; font-weight:bold;">{item['comm_amt']:,.0f}₺</div>
</div>
<div style="background:rgba(78, 205, 196, 0.1); padding:4px; border-radius:4px; text-align:center;">
<div style="color:#4ECDC4; opacity:0.8;">Marka Ödemesi</div>
<div style="color:#4ECDC4; font-weight:bold;">{item['payout']:,.0f}₺</div>
</div>
</div>
</div>
"""
                st.markdown(item_html, unsafe_allow_html=True)
            
            total = sum(i['subtotal'] for i in st.session_state.cart)
            total_comm = sum(i['comm_amt'] for i in st.session_state.cart)
            total_pay = sum(i['payout'] for i in st.session_state.cart)
            
            summary_html = f"""
<div style="background: rgba(78,205,196,0.1); padding: 15px; border-radius: 8px; margin: 15px 0;">
<div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:4px;">
<span>Ürün Toplam:</span>
<span style="font-weight:bold;">{total:,.0f}₺</span>
</div>
<div style="display:flex; justify-content:space-between; font-size:14px; color:#FCD34D; margin-bottom:8px;">
<span>Top. Komisyon:</span>
<span style="font-weight:bold;">{total_comm:,.0f}₺</span>
</div>
<div style="margin: 5px 0; border-top: 1px dashed rgba(128,128,128,0.3);"></div>
<div style="display:flex; justify-content:space-between; font-weight:bold; font-size:18px; color:#4ECDC4; margin-top:8px;">
<span>MARKAYA NET:</span>
<span>{total_pay:,.0f}₺</span>
</div>
</div>
"""
            st.markdown(summary_html, unsafe_allow_html=True)
            
            if st.button("⚡ SİPARİŞİ OLUŞTUR", type="primary"):
                if cust_name and cust_phone:
                    order_id = f"NV-{datetime.now().strftime('%m%d%H%M')}"
                    items_str = ", ".join([f"{i['product']} (x{i['qty']})" for i in st.session_state.cart])
                    
                    order_data = {
                        'Order_ID': order_id,
                        'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Brand': st.session_state.brand_lock,
                        'Customer': cust_name,
                        'Phone': cust_phone,
                        'Address': cust_addr,
                        'Items': items_str,
                        'Total_Value': total,
                        'Commission_Rate': BRANDS[st.session_state.brand_lock]['commission'],
                        'Commission_Amt': total_comm,
                        'Brand_Payout': total_pay,
                        'Status': 'Pending',
                        'WhatsApp_Sent': 'NO',
                        'Tracking_Num': '',
                        'Priority': 'Standard',
                        'Notes': '',
                        'Created_By': 'admin',
                        'Last_Modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    if save_order(order_data):
                        st.success(f"✅ Sipariş {order_id} oluşturuldu!")
                        st.session_state.cart = []
                        st.session_state.brand_lock = None
                        st.rerun()
                else:
                    st.error("Müşteri bilgilerini giriniz!")
            
            if st.button("🗑️ Sepeti Temizle"):
                st.session_state.cart = []
                st.session_state.brand_lock = None
                st.rerun()
        else:
            st.info("Sepet boş")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 9. OPERASYON MODÜLÜ
# ============================================================================

def render_operations():
    radiant_line()
    st.markdown("### ✅ Operasyon Yönetimi")
    df = load_orders()
    
    new_orders = df[df['WhatsApp_Sent'] == 'NO']
    if not new_orders.empty:
        st.warning(f"⚠️ {len(new_orders)} sipariş markaya bildirilmedi!")
        for idx, row in new_orders.iterrows():
            with st.expander(f"🔴 {row['Order_ID']} - {row['Brand']} ({row['Customer']})", expanded=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    phone = BRANDS[row['Brand']]['phone']
                    msg = urllib.parse.quote(f"YENİ SİPARİŞ: {row['Order_ID']}\n{row['Items']}\nTeslimat: {row['Address']}")
                    st.markdown(f"[📲 WhatsApp Mesajı Gönder](https://wa.me/{phone}?text={msg})")
                with col2:
                    if st.button("✅ Bildirildi", key=f"ntf_{idx}"):
                        df.at[idx, 'WhatsApp_Sent'] = 'YES'
                        df.at[idx, 'Status'] = 'Notified'
                        update_orders(df)
                        st.rerun()
    
    pending_track = df[(df['Status'] == 'Notified') & (df['Tracking_Num'].isna() | (df['Tracking_Num'] == ''))]
    if not pending_track.empty:
        st.info("📦 Takip numarası bekleyen siparişler")
        for idx, row in pending_track.iterrows():
            with st.expander(f"⏳ {row['Order_ID']} - {row['Brand']}"):
                track = st.text_input("Takip No Giriniz", key=f"track_{idx}")
                if st.button("Kargola", key=f"ship_{idx}"):
                    df.at[idx, 'Tracking_Num'] = track
                    df.at[idx, 'Status'] = 'Dispatched'
                    update_orders(df)
                    st.success("Kargolandı!")
                    st.rerun()

    dispatched = df[df['Status'] == 'Dispatched']
    if not dispatched.empty:
        st.markdown("---")
        st.markdown("#### ✅ Tamamlanmayı Bekleyenler")
        for idx, row in dispatched.iterrows():
            col1, col2, col3 = st.columns([2, 2, 1])
            col1.write(f"**{row['Order_ID']}**")
            col2.write(f"Takip: {row['Tracking_Num']}")
            if col3.button("Tamamla", key=f"comp_{idx}"):
                df.at[idx, 'Status'] = 'Completed'
                update_orders(df)
                st.rerun()

# ============================================================================
# 10. FATURA & ÖDEME PANELİ
# ============================================================================

def render_brand_payout_hq():
    radiant_line()
    st.markdown("## 📑 FATURA & ÖDEME PANELİ (BRAND PAYOUT HQ)")
    
    df_orders = load_orders()
    df_payments = load_payments()
    
    for brand in BRANDS.keys():
        with st.expander(f"🏦 {brand} FİNANS YÖNETİMİ", expanded=True):
            brand_meta = BRANDS[brand]
            brand_orders = df_orders[df_orders['Brand'] == brand]
            
            completed_df = brand_orders[brand_orders['Status'] == 'Completed']
            payout_completed = completed_df['Brand_Payout'].sum() if not completed_df.empty else 0
            count_completed = len(completed_df)
            
            pending_df = brand_orders[brand_orders['Status'].isin(['Pending', 'Notified', 'Dispatched'])]
            payout_pending = pending_df['Brand_Payout'].sum() if not pending_df.empty else 0
            
            brand_paid_df = df_payments[df_payments['Brand'] == brand]
            total_paid = brand_paid_df['Amount'].sum() if not brand_paid_df.empty else 0
            
            net_transfer_due = payout_completed - total_paid
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #4ECDC4;">
                    <div style="font-size:12px; opacity:0.7;">KESİLMESİ GEREKEN FATURA TUTARI</div>
                    <div style="font-size:24px; font-weight:bold;">{payout_completed:,.2f}₺</div>
                    <div style="font-size:11px; opacity:0.6;">(Tamamlanan {count_completed} Sipariş)</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #F59E0B;">
                    <div style="font-size:12px; opacity:0.7;">HENÜZ TAMAMLANMAMIŞ SİPARİŞLER</div>
                    <div style="font-size:24px; font-weight:bold;">{payout_pending:,.2f}₺</div>
                    <div style="font-size:11px; opacity:0.6;">(Bekleyen/Kargoda)</div>
                </div>
                """, unsafe_allow_html=True)
            
            comm_rate = int(brand_meta['commission'] * 100)
            fatura_desc = f"NATUVISIO satış komisyon hizmeti – {brand} – Toplam sipariş adedi: {count_completed} – Komisyon oranı: %{comm_rate} – Net marka ödemesi: {payout_completed:,.2f}₺"
            
            st.markdown("#### 🧾 Fatura Açıklaması (Otomatik)")
            st.code(fatura_desc, language="text")
            
            st.markdown("#### 💸 Banka Transfer Talimatı")
            col_bank1, col_bank2 = st.columns([2, 1])
            with col_bank1:
                st.info(f"**Alıcı:** {brand_meta['account_name']}  \n**IBAN:** {brand_meta['iban']}  \n**Tutar:** {net_transfer_due:,.2f}₺")
            with col_bank2:
                transfer_desc = f"NATUVISIO {brand} satış ödemesi – {datetime.now().strftime('%d.%m.%Y')} – Toplam: {net_transfer_due:,.0f}TL"
                st.code(transfer_desc, language="text")
            
            if net_transfer_due > 0:
                if st.button(f"💸 {brand} - ÖDEMEYİ YAPTIM ({net_transfer_due:,.0f}₺)", key=f"pay_{brand}"):
                    payment_data = {
                        "Payment_ID": f"PAY-{datetime.now().strftime('%m%d%H%M%S')}",
                        "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "Brand": brand,
                        "Amount": net_transfer_due,
                        "Method": "Bank Transfer",
                        "Reference": "Admin Manual",
                        "Status": "Confirmed",
                        "Proof_File": "",
                        "Notes": "Payout HQ üzerinden ödendi",
                        "Fatura_Sent": "No",
                        "Fatura_Date": "",
                        "Fatura_Explanation": ""
                    }
                    if save_payment(payment_data):
                        st.balloons()
                        st.success("Ödeme sisteme işlendi!")
                        time.sleep(1)
                        st.rerun()
            else:
                st.success("✅ Tüm ödemeler yapıldı.")

    radiant_line()
    st.markdown("### 📋 Fatura Durum Tablosu (Cross-Check)")
    df_payments = load_payments()
    if not df_payments.empty:
        st.dataframe(df_payments[['Time', 'Brand', 'Amount', 'Fatura_Sent', 'Fatura_Date']], use_container_width=True)
        with st.form("update_fatura_status"):
            st.write("Fatura Durumu Güncelle")
            pay_ids = df_payments['Payment_ID'].tolist()
            selected_pay = st.selectbox("İşlem Seçiniz (Payment ID)", pay_ids)
            col_f1, col_f2 = st.columns(2)
            with col_f1: new_status = st.checkbox("Fatura Kesildi mi? (YES)", value=False)
            with col_f2: new_date = st.date_input("Fatura Tarihi")
            if st.form_submit_button("Durumu Güncelle"):
                idx = df_payments.index[df_payments['Payment_ID'] == selected_pay][0]
                df_payments.at[idx, 'Fatura_Sent'] = "YES" if new_status else "NO"
                df_payments.at[idx, 'Fatura_Date'] = str(new_date)
                update_payments(df_payments)
                st.success("Güncellendi!")
                st.rerun()
    else:
        st.info("Henüz ödeme kaydı yok.")

# ============================================================================
# 11. LOGS & ANALYTICS
# ============================================================================

def render_logs_advanced():
    radiant_line()
    st.markdown(f"## 📜 LOG KAYITLARI <span style='font-size:12px; opacity:0.6; vertical-align:middle;'>GELİŞMİŞ MODÜL</span>", unsafe_allow_html=True)
    
    df_logs = load_logs()
    
    if df_logs.empty:
        st.info("Henüz sistem kaydı bulunmuyor.")
        return

    # SEARCH
    search_query = st.text_input("🔍 Log Ara (ID, İşlem, Kullanıcı, Detay...)", key="log_search")
    
    # FILTERS
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        unique_actions = df_logs['Action'].unique().tolist()
        filter_action = st.multiselect("İşlem Tipi Filtrele", unique_actions)
    with col_f2:
        unique_users = df_logs['User'].unique().tolist()
        filter_user = st.multiselect("Kullanıcı Filtrele", unique_users)

    filtered_df = df_logs.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values.tostring().lower(), axis=1)
        ]
    if filter_action:
        filtered_df = filtered_df[filtered_df['Action'].isin(filter_action)]
    if filter_user:
        filtered_df = filtered_df[filtered_df['User'].isin(filter_user)]

    st.markdown(f"**{len(filtered_df)}** kayıt bulundu.")
    st.dataframe(
        filtered_df.sort_values('Time', ascending=False),
        use_container_width=True,
        column_config={
            "Log_ID": "Log ID",
            "Time": "Tarih/Saat",
            "Action": "İşlem Türü",
            "User": "Kullanıcı",
            "Details": "Detaylar"
        },
        height=500
    )
    
    csv = export_to_csv(filtered_df)
    st.download_button(
        label="📥 Logları İndir (CSV)",
        data=csv,
        file_name=f"system_logs_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv',
    )

def render_all_orders():
    radiant_line()
    st.markdown("### 📦 Tüm Sipariş Geçmişi")
    df = load_orders()
    if not df.empty:
        st.dataframe(df.sort_values('Time', ascending=False), use_container_width=True)
    else:
        st.info("Kayıt yok")

def render_analytics():
    radiant_line()
    st.markdown("### 📊 Analitik Raporlar")
    df = load_orders()
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Marka Bazlı Satış**")
            st.bar_chart(df.groupby('Brand')['Total_Value'].sum())
        with col2:
            st.markdown("**Durum Dağılımı**")
            st.bar_chart(df['Status'].value_counts())

def render_faqs():
    radiant_line()
    st.markdown("## ❔ SSS & Operasyon Akış Rehberi")
    with st.expander("1. Genel bakış: Bu panel ne yapıyor?", expanded=True):
        st.markdown("""Bu panel, NATUVISIO'nun tüm marka partnerleri için tek merkezden sevkiyat, finans ve mutabakat yönetimini sağlar.""")
    with st.expander("2. Sipariş akışı: İlk adımdan marka ödemesine kadar", expanded=False):
        st.markdown("""1. YENİ SEVKİYAT > Sipariş Gir\n2. OPERASYON > WhatsApp Gönder\n3. Kargo Takip > Gir & Tamamla\n4. FATURA & ÖDEME > Marka Hakedişini Öde""")

# ============================================================================
# 12. ANA ÇALIŞTIRMA (MAIN)
# ============================================================================

if __name__ == "__main__":
    if not st.session_state.admin_logged_in:
        login_screen()
    else:
        dashboard()
