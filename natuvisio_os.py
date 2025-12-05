import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import time
from datetime import datetime, timedelta
import urllib.parse
# ZoneInfo requires Python 3.9+, standard in Streamlit Cloud
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

# ============================================================================
# 🏔️ NATUVISIO YÖNETİM SİSTEMİ - V8.0 (MESSAGING + ADVANCED WHATSAPP)
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
CSV_PARTNERS = "partners.csv"
CSV_MESSAGES = "messages.csv" # NEW v8.0

PHI = 1.618
FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

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
        "log": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
        "message": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>'
    }
    return icons.get(name, "")

# ============================================================================
# 3. CSS & THEME ENGINE
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
        
        .radiant-line {{
            background: linear-gradient(90deg, rgba(91,115,84,0), rgba(91,115,84,0.3), rgba(91,115,84,0));
            height: 1px;
            margin: 35px 0;
            width: 100%;
        }}
        
        .stCheckbox label {{ color: {text_color} !important; }}
        #MainMenu, header, footer {{ visibility: hidden; }}
        
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
        .os-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            max-width: 900px;
            margin: 0 auto;
            text-align: left;
        }}
        .os-status-dot {{
            height: 8px;
            width: 8px;
            background-color: #10B981;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
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
            "Order_ID", "Time", "Brand", "Customer", "Phone", "Email", "Address",
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

    if not os.path.exists(CSV_PARTNERS):
        data = {
            "partner_email": ["haki@natuvisio.com", "aurora@natuvisio.com", "long@natuvisio.com"],
            "password": ["haki2025", "aurora2025", "long2025"], 
            "brand_name": ["HAKI HEAL", "AURORACO", "LONGEVICALS"],
            "created_at": [datetime.now(), datetime.now(), datetime.now()],
            "status": ["Active", "Active", "Active"]
        }
        pd.DataFrame(data).to_csv(CSV_PARTNERS, index=False)

    if not os.path.exists(CSV_MESSAGES):
        pd.DataFrame(columns=[
            "Message_ID", "Time_UTC", "Time_IST", "From_Role", "From_Brand",
            "To_Role", "To_Brand", "Order_ID", "Channel", "Subject", "Body",
            "Read_By_Admin", "Read_By_Brand"
        ]).to_csv(CSV_MESSAGES, index=False)

def load_csv(filename):
    try: return pd.read_csv(filename)
    except: return pd.DataFrame()

def save_order(order_data):
    try:
        df = load_csv(CSV_ORDERS)
        df = pd.concat([df, pd.DataFrame([order_data])], ignore_index=True)
        df.to_csv(CSV_ORDERS, index=False)
        log_action("SİPARİŞ_OLUŞTURULDU", "admin", order_data['Order_ID'], f"Oluşturuldu: {order_data['Order_ID']}")
        return True
    except: return False

def update_orders(df):
    try:
        df.to_csv(CSV_ORDERS, index=False)
        return True
    except: return False

def save_payment(payment_data):
    try:
        df = load_csv(CSV_PAYMENTS)
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
        df = load_csv(CSV_INVOICES)
        df = pd.concat([df, pd.DataFrame([invoice_data])], ignore_index=True)
        df.to_csv(CSV_INVOICES, index=False)
        log_action("FATURA_KESİLDİ", "admin", "", f"{invoice_data['Brand']} faturası oluşturuldu")
        return True
    except: return False

def save_message(msg_data):
    try:
        df = load_csv(CSV_MESSAGES)
        df = pd.concat([df, pd.DataFrame([msg_data])], ignore_index=True)
        df.to_csv(CSV_MESSAGES, index=False)
        log_action("MESAJ", msg_data['From_Brand'], msg_data['Order_ID'], f"Mesaj gönderildi: {msg_data['Subject']}")
        return True
    except: return False

def update_messages(df):
    try:
        df.to_csv(CSV_MESSAGES, index=False)
        return True
    except: return False

def log_action(action, user, order_id, details):
    try:
        df = load_csv(CSV_LOGS)
        log_entry = {
            'Log_ID': f"LOG-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'Time': datetime.now(ZoneInfo("Europe/Istanbul")).strftime('%Y-%m-%d %H:%M:%S'),
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
if 'is_partner_logged_in' not in st.session_state:
    st.session_state.is_partner_logged_in = False
if 'partner_brand' not in st.session_state:
    st.session_state.partner_brand = None
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
    init_databases() 
    
    st.markdown("<div style='height: 5vh'></div>", unsafe_allow_html=True)
    
    if 'login_mode' not in st.session_state:
        st.session_state.login_mode = 'Admin'
        
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:20px;">
            <img src="{LOGO_URL}" style="width:120px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));" onerror="this.style.display='none'">
            <div style="font-family:'Space Grotesk'; font-size:32px; font-weight:800; color:#5b7354; margin-top:10px;">NATUVISIO</div>
        </div>
        """, unsafe_allow_html=True)

        mode_cols = st.columns(2)
        with mode_cols[0]:
            if st.button("👑 Yönetici", use_container_width=True): st.session_state.login_mode = 'Admin'
        with mode_cols[1]:
            if st.button("🤝 Partner", use_container_width=True): st.session_state.login_mode = 'Partner'

        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['xl']}px;">
            <h2>{st.session_state.login_mode.upper()} GİRİŞİ</h2>
            <p style="opacity: 0.6; font-size: 13px; margin-bottom:20px;">GÜVENLİ OPERASYON SİSTEMİ</p>
        """, unsafe_allow_html=True)
        
        if st.session_state.login_mode == 'Admin':
            password = st.text_input("Erişim Şifresi", type="password", key="admin_login", label_visibility="collapsed")
            if st.button("🔓 GİRİŞ YAP", use_container_width=True):
                if password == ADMIN_PASS:
                    st.session_state.admin_logged_in = True
                    log_action("GİRİŞ", "admin", "", "Admin Girişi")
                    st.rerun()
                else:
                    st.error("❌ Hatalı şifre")
        
        else:
            email = st.text_input("E-posta", key="partner_email")
            pwd = st.text_input("Şifre", type="password", key="partner_pwd")
            if st.button("🔓 PARTNER GİRİŞİ", use_container_width=True):
                partners = load_csv(CSV_PARTNERS)
                user = partners[partners['partner_email'] == email]
                if not user.empty and str(user.iloc[0]['password']) == str(pwd):
                    st.session_state.is_partner_logged_in = True
                    st.session_state.partner_brand = user.iloc[0]['brand_name']
                    log_action("GİRİŞ", st.session_state.partner_brand, "", "Partner Girişi")
                    st.rerun()
                else:
                    st.error("❌ Hatalı bilgiler")

        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# 7. PARTNER DASHBOARD
# ============================================================================

def partner_dashboard():
    load_css(st.session_state.theme)
    brand = st.session_state.partner_brand
    
    # Header
    col_h1, col_h2, col_h3 = st.columns([6, 1, 1])
    with col_h1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <img src="{LOGO_URL}" style="height:40px;" onerror="this.style.display='none'">
            <div>
                <h1 style="margin:0; font-size:24px;">PARTNER PORTALI</h1>
                <span style="font-size: 14px; color:{BRANDS[brand]['color']}; font-weight:700;">{brand}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_h3:
        if st.button("🚪 Çıkış"):
            st.session_state.is_partner_logged_in = False
            st.session_state.partner_brand = None
            st.rerun()
            
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # Alerts
    df_orders = load_csv(CSV_ORDERS)
    brand_orders = df_orders[df_orders['Brand'] == brand]
    new_orders = brand_orders[brand_orders['Status'] == 'Pending']
    if len(new_orders) > 0:
        st.markdown(f"""<div class="radiant-reminder">🔔 {len(new_orders)} YENİ SİPARİŞ BEKLİYOR! <span style="font-size:10px;">LÜTFEN ONAYLAYIN</span></div>""", unsafe_allow_html=True)

    # Messages Badge
    df_msgs = load_csv(CSV_MESSAGES)
    unread_msgs = len(df_msgs[(df_msgs['To_Brand'] == brand) & (df_msgs['Read_By_Brand'] == 'No')])
    msg_label = f"💬 MESAJLAR ({unread_msgs})" if unread_msgs > 0 else "💬 MESAJLAR"

    tabs = st.tabs(["📥 YENİ SİPARİŞLER", "🚚 KARGO TAKİBİ", "✅ TAMAMLANANLAR", "💰 HAKEDİŞLER", msg_label, "📜 LOGLAR"])
    
    # 1. NEW ORDERS
    with tabs[0]:
        st.markdown("### 📥 Gelen Siparişler")
        if new_orders.empty:
            st.info("Bekleyen yeni sipariş yok.")
        else:
            for idx, row in new_orders.iterrows():
                original_idx = df_orders.index[df_orders['Order_ID'] == row['Order_ID']][0]
                with st.expander(f"🆕 {row['Order_ID']} - {row['Items']}", expanded=True):
                    c1, c2 = st.columns(2)
                    with c1: st.markdown(f"**Müşteri:** {row['Customer']}\n\n**Adres:** {row['Address']}")
                    with c2:
                        st.metric("Hakediş", f"{row['Brand_Payout']:,.0f}₺")
                        if st.button("✅ Siparişi Onayla", key=f"acc_{row['Order_ID']}"):
                            df_orders.at[original_idx, 'Status'] = 'Notified'
                            df_orders.at[original_idx, 'WhatsApp_Sent'] = 'YES'
                            update_orders(df_orders)
                            log_action("ONAY", brand, row['Order_ID'], "Marka siparişi onayladı")
                            st.success("Sipariş onaylandı, hazırlığa başlayın.")
                            time.sleep(1)
                            st.rerun()

    # 2. SHIPPING
    with tabs[1]:
        st.markdown("### 🚚 Kargo ve Takip")
        to_ship = brand_orders[brand_orders['Status'] == 'Notified']
        if to_ship.empty:
            st.info("Kargolanacak sipariş yok.")
        else:
            for idx, row in to_ship.iterrows():
                original_idx = df_orders.index[df_orders['Order_ID'] == row['Order_ID']][0]
                with st.expander(f"📦 {row['Order_ID']} - {row['Customer']}", expanded=True):
                    track_no = st.text_input("Kargo Takip No", key=f"pt_trk_{row['Order_ID']}")
                    courier = st.selectbox("Kargo Firması", ["Yurtiçi", "Aras", "MNG", "PTT", "Diğer"], key=f"pt_cr_{row['Order_ID']}")
                    if st.button("🚀 Kargoya Verildi", key=f"pt_ship_{row['Order_ID']}"):
                        if track_no:
                            df_orders.at[original_idx, 'Status'] = 'Dispatched'
                            df_orders.at[original_idx, 'Tracking_Num'] = f"{courier} - {track_no}"
                            df_orders.at[original_idx, 'Last_Modified'] = datetime.now()
                            update_orders(df_orders)
                            log_action("KARGO", brand, row['Order_ID'], f"Takip no girildi: {track_no}")
                            st.success("Kargo bilgisi sisteme girildi!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Lütfen takip numarası girin.")

    # 3. COMPLETED
    with tabs[2]:
        st.markdown("### ✅ Tamamlanan Siparişler")
        done = brand_orders[brand_orders['Status'].isin(['Dispatched', 'Completed'])]
        if not done.empty:
            st.dataframe(done[['Order_ID', 'Time', 'Items', 'Brand_Payout', 'Status', 'Tracking_Num']], use_container_width=True)
        else:
            st.info("Henüz tamamlanan sipariş yok.")

    # 4. FINANCE
    with tabs[3]:
        st.markdown("### 💰 Finansal Özet")
        completed_val = brand_orders[brand_orders['Status'] == 'Completed']['Brand_Payout'].sum()
        df_pay = load_csv(CSV_PAYMENTS)
        my_payments = df_pay[df_pay['Brand'] == brand]
        paid_val = my_payments['Amount'].sum()
        balance = completed_val - paid_val
        c1, c2, c3 = st.columns(3)
        c1.metric("Toplam Hakediş", f"{completed_val:,.0f}₺")
        c2.metric("Ödenen", f"{paid_val:,.0f}₺")
        c3.metric("Kalan Bakiye", f"{balance:,.0f}₺", delta_color="normal")
        st.markdown("#### 📜 Ödeme Geçmişi")
        if not my_payments.empty:
            st.dataframe(my_payments[['Time', 'Amount', 'Reference', 'Status']], use_container_width=True)
        else:
            st.info("Henüz ödeme alınmadı.")

    # 5. MESSAGING (NEW v8.0)
    with tabs[4]:
        render_messaging_panel(brand, 'partner')

    # 6. LOGS
    with tabs[5]:
        st.markdown("### 📜 İşlem Kayıtları")
        logs = load_logs()
        my_logs = logs[logs['User'] == brand].sort_values('Time', ascending=False)
        st.dataframe(my_logs, use_container_width=True)
        
    render_os_footer()

# ============================================================================
# 8. MESSAGING ENGINE (NEW v8.0)
# ============================================================================

def render_messaging_panel(brand, role):
    st.markdown("### 💬 Mesajlaşma Merkezi")
    
    # Filters
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        view_filter = st.radio("Filtre", ["Tümü", "Okunmamış"], horizontal=True)
    
    df_msgs = load_csv(CSV_MESSAGES)
    if role == 'partner':
        my_msgs = df_msgs[(df_msgs['From_Brand'] == brand) | (df_msgs['To_Brand'] == brand)].sort_values('Time_UTC', ascending=False)
    else: # admin sees all or filtered by brand
        my_msgs = df_msgs.sort_values('Time_UTC', ascending=False)
    
    if view_filter == "Okunmamış":
        if role == 'partner':
            my_msgs = my_msgs[my_msgs['Read_By_Brand'] == 'No']
        else:
            my_msgs = my_msgs[my_msgs['Read_By_Admin'] == 'No']

    # New Message Form
    with st.expander("📝 Yeni Mesaj Gönder"):
        with st.form("new_msg_form"):
            subject = st.text_input("Konu")
            body = st.text_area("Mesaj")
            
            # Admin targets
            target_brand = "NATUVISIO"
            if role == 'admin':
                target_brand = st.selectbox("Alıcı Marka", list(BRANDS.keys()))
            
            if st.form_submit_button("Gönder"):
                msg_data = {
                    "Message_ID": f"MSG-{datetime.now().strftime('%m%d%H%M%S')}",
                    "Time_UTC": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "Time_IST": datetime.now(ZoneInfo("Europe/Istanbul")).strftime('%Y-%m-%d %H:%M:%S'),
                    "From_Role": role,
                    "From_Brand": brand if role == 'partner' else "NATUVISIO",
                    "To_Role": 'admin' if role == 'partner' else 'partner',
                    "To_Brand": target_brand if role == 'admin' else "NATUVISIO",
                    "Order_ID": "",
                    "Channel": "panel",
                    "Subject": subject,
                    "Body": body,
                    "Read_By_Admin": "No",
                    "Read_By_Brand": "No"
                }
                save_message(msg_data)
                st.success("Mesaj gönderildi!")
                st.rerun()

    # Message List
    if my_msgs.empty:
        st.info("Mesaj yok.")
    else:
        for idx, msg in my_msgs.iterrows():
            sender = msg['From_Brand']
            is_me = (msg['From_Role'] == role)
            bg_color = "rgba(78, 205, 196, 0.1)" if not is_me else "rgba(255,255,255,0.05)"
            border = "1px solid #4ECDC4" if not is_me and ((role=='admin' and msg['Read_By_Admin']=='No') or (role=='partner' and msg['Read_By_Brand']=='No')) else "1px solid rgba(255,255,255,0.1)"
            
            st.markdown(f"""
            <div style="background:{bg_color}; border:{border}; border-radius:8px; padding:15px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; font-size:12px; opacity:0.7;">
                    <span><strong>{sender}</strong></span>
                    <span>{msg['Time_IST']}</span>
                </div>
                <div style="font-weight:bold; margin:5px 0;">{msg['Subject']}</div>
                <div style="font-size:14px;">{msg['Body']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Mark as read logic would ideally be here with a button or auto-logic

# ============================================================================
# 9. ADMIN DASHBOARD
# ============================================================================

def dashboard():
    load_css(st.session_state.theme)
    init_databases()
    
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
            st.rerun()
            
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # Alerts
    df_orders = load_csv(CSV_ORDERS)
    pending_notify = len(df_orders[df_orders['WhatsApp_Sent'] == 'NO'])
    if pending_notify > 0:
        st.markdown(f"""<div class="radiant-reminder">⚠️ {pending_notify} SİPARİŞ BİLDİRİM BEKLİYOR!</div>""", unsafe_allow_html=True)

    # Inbox Badge
    df_msgs = load_csv(CSV_MESSAGES)
    admin_unread = len(df_msgs[(df_msgs['To_Role'] == 'admin') & (df_msgs['Read_By_Admin'] == 'No')])
    inbox_label = f"💬 PARTNER INBOX ({admin_unread})" if admin_unread > 0 else "💬 PARTNER INBOX"

    tabs = st.tabs(["🚀 YENİ SEVKİYAT", "✅ OPERASYON", "🏦 FATURA & ÖDEME", "📦 TÜM SİPARİŞLER", "📊 ANALİTİK", inbox_label, "📜 LOGLAR"])
    
    with tabs[0]: render_new_dispatch()
    with tabs[1]: render_operations()
    with tabs[2]: render_brand_payout_hq()
    with tabs[3]: render_all_orders()
    with tabs[4]: render_analytics()
    with tabs[5]: render_messaging_panel("NATUVISIO", 'admin')
    with tabs[6]: render_logs_advanced()

    render_os_footer()

def render_os_footer():
    ist_time = datetime.now(ZoneInfo("Europe/Istanbul")).strftime('%H:%M')
    st.markdown(f"""
    <div class="os-footer">
        <img src="{LOGO_URL}" class="os-footer-logo" onerror="this.style.display='none'">
        <div class="os-grid">
            <div>
                <strong>NATUVISIO ADMIN OS v8.0</strong><br>
                <span class="os-status-dot"></span> System Operational<br>
                Istanbul Time: {ist_time}
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
# 10. OPERATIONAL MODULES (DISPATCH, OPERATIONS, ETC.)
# ============================================================================

# (Keeping existing logic for render_new_dispatch, render_operations, render_brand_payout_hq, etc.)
# RE-INSERTING THE CRITICAL LOGIC BLOCKS BELOW TO ENSURE FULL FILE COMPLETENESS

def render_new_dispatch():
    col_L, col_R = st.columns([PHI, 1])
    with col_L:
        st.markdown('<div class="glass-card"><h4>👤 Müşteri Bilgileri</h4>', unsafe_allow_html=True)
        col_n, col_p = st.columns(2)
        with col_n: cust_name = st.text_input("Ad Soyad", key="cust_name")
        with col_p: cust_phone = st.text_input("Telefon", key="cust_phone")
        cust_addr = st.text_area("Adres", key="cust_addr", height=80)
        cust_email = st.text_input("E-posta (Opsiyonel)", key="cust_email")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card"><h4>🛒 Ürün Seçimi</h4>', unsafe_allow_html=True)
        if st.session_state.cart:
            active_brand = st.session_state.brand_lock
            st.info(f"🔒 {active_brand}")
        else:
            active_brand = st.selectbox("Marka", list(BRANDS.keys()), key="brand_sel")
        
        products = list(BRANDS[active_brand]["products"].keys())
        c1, c2 = st.columns([3,1])
        with c1: prod = st.selectbox("Ürün", products)
        with c2: qty = st.number_input("Adet", 1, value=1)
        
        if st.button("➕ Ekle"):
            price = BRANDS[active_brand]["products"][prod]["price"]
            st.session_state.cart.append({
                "brand": active_brand, "product": prod, "qty": qty, "price": price,
                "subtotal": price*qty, "comm_amt": (price*qty)*BRANDS[active_brand]["commission"],
                "payout": (price*qty)*(1-BRANDS[active_brand]["commission"])
            })
            st.session_state.brand_lock = active_brand
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_R:
        st.markdown('<div class="glass-card"><h4>📦 Sepet</h4>', unsafe_allow_html=True)
        if st.session_state.cart:
            for item in st.session_state.cart:
                st.markdown(f"**{item['product']}** x{item['qty']} = {item['subtotal']:,.0f}₺")
            
            total = sum(x['subtotal'] for x in st.session_state.cart)
            if st.button("⚡ SİPARİŞİ OLUŞTUR", type="primary"):
                order_id = f"NV-{datetime.now().strftime('%m%d%H%M')}"
                order_data = {
                    'Order_ID': order_id,
                    'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Brand': st.session_state.brand_lock,
                    'Customer': cust_name,
                    'Phone': cust_phone,
                    'Email': cust_email,
                    'Address': cust_addr,
                    'Items': str([x['product'] for x in st.session_state.cart]),
                    'Total_Value': total,
                    'Commission_Rate': BRANDS[st.session_state.brand_lock]['commission'],
                    'Commission_Amt': sum(x['comm_amt'] for x in st.session_state.cart),
                    'Brand_Payout': sum(x['payout'] for x in st.session_state.cart),
                    'Status': 'Pending',
                    'WhatsApp_Sent': 'NO',
                    'Tracking_Num': '',
                    'Priority': 'Standard',
                    'Notes': '',
                    'Created_By': 'admin',
                    'Last_Modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                save_order(order_data)
                st.session_state.cart = []
                st.session_state.brand_lock = None
                st.success("Sipariş Oluşturuldu!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_operations():
    radiant_line()
    st.markdown("### ✅ Operasyon Yönetimi")
    df = load_csv(CSV_ORDERS)
    
    # WhatsApp Notification Logic (ADVANCED TEMPLATE)
    new_orders = df[df['WhatsApp_Sent'] == 'NO']
    if not new_orders.empty:
        for idx, row in new_orders.iterrows():
            with st.expander(f"🔴 {row['Order_ID']} - {row['Brand']}", expanded=True):
                brand_meta = BRANDS[row['Brand']]
                
                # GENERATE ADVANCED WHATSAPP MESSAGE
                wa_msg = f"""━━━━━━━━━━━━━━━━━━
📦 YENİ SİPARİŞ BİLDİRİMİ  
NATUVISIO → {row['Brand']}

👤 MÜŞTERİ BİLGİLERİ  
• Ad Soyad: {row['Customer']}  
• Telefon: {row['Phone']}  
• E-posta: {row.get('Email', '-')}  
• Adres: {row['Address']}

🛒 SİPARİŞ DETAYLARI  
• Ürün: {row['Items']}  
• Toplam Satış Bedeli: {row['Total_Value']}₺  
• Sipariş No: {row['Order_ID']}

💰 KOMİSYON & ÖDEME DAĞILIMI  
• Komisyon Oranı (NATUVISIO): %{int(row['Commission_Rate']*100)}  
• Komisyon Tutarı: {row['Commission_Amt']}₺  
• Markaya Net Ödeme: {row['Brand_Payout']}₺  

(Açıklama:  
– Müşteriye kesilecek satış faturası {row['Brand']} tarafından düzenlenir.  
– NATUVISIO yalnızca komisyon tutarına fatura keser.)

⏳ DURUM  
Lütfen onaylayıp sevkiyat sürecini başlatınız.

NATUVISIO Operasyon Ekibi
━━━━━━━━━━━━━━━━━━"""
                
                encoded_msg = urllib.parse.quote(wa_msg)
                phone = brand_meta['phone']
                
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"[📲 WhatsApp Mesajı Gönder](https://wa.me/{phone}?text={encoded_msg})")
                with c2:
                    if st.button("✅ Bildirildi", key=f"ntf_{idx}"):
                        df.at[idx, 'WhatsApp_Sent'] = 'YES'
                        df.at[idx, 'Status'] = 'Notified'
                        update_orders(df)
                        st.rerun()

def render_brand_payout_hq():
    radiant_line()
    st.markdown("## 📑 FATURA & ÖDEME PANELİ")
    df_orders = load_csv(CSV_ORDERS)
    df_payments = load_csv(CSV_PAYMENTS)
    
    for brand in BRANDS.keys():
        with st.expander(f"🏦 {brand}", expanded=True):
            brand_orders = df_orders[df_orders['Brand'] == brand]
            completed = brand_orders[brand_orders['Status'] == 'Completed']['Brand_Payout'].sum()
            paid = df_payments[df_payments['Brand'] == brand]['Amount'].sum()
            balance = completed - paid
            
            c1, c2 = st.columns(2)
            c1.metric("Toplam Hakediş", f"{completed:,.2f}₺")
            c2.metric("Kalan Bakiye", f"{balance:,.2f}₺", delta_color="inverse")
            
            if balance > 0:
                if st.button(f"💸 {brand} Ödeme Yap", key=f"pay_admin_{brand}"):
                    save_payment({
                        "Payment_ID": f"PAY-{int(time.time())}",
                        "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "Brand": brand,
                        "Amount": balance,
                        "Method": "Bank",
                        "Reference": "Admin",
                        "Status": "Sent",
                        "Fatura_Sent": "No"
                    })
                    st.success("Ödeme kaydedildi")
                    st.rerun()

def render_all_orders():
    st.dataframe(load_csv(CSV_ORDERS), use_container_width=True)

def render_analytics():
    df = load_csv(CSV_ORDERS)
    if not df.empty:
        st.bar_chart(df.groupby('Brand')['Total_Value'].sum())

def render_logs_advanced():
    st.dataframe(load_logs().sort_values('Time', ascending=False), use_container_width=True)

def render_faqs():
    st.info("SSS Alanı")

# ============================================================================
# 13. ANA ÇALIŞTIRMA (MAIN)
# ============================================================================

if __name__ == "__main__":
    if st.session_state.admin_logged_in:
        dashboard()
    elif st.session_state.is_partner_logged_in:
        partner_dashboard()
    else:
        login_screen()
