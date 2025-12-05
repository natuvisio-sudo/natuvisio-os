import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import time
from datetime import datetime, timedelta
import urllib.parse
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

# ============================================================================
# 🏔️ NATUVISIO OS v10.0 - UNIFIED SYNC & ACTION EDITION
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 1. CONSTANTS & ASSETS
# ============================================================================

ADMIN_PASS = "admin2025"
CSV_ORDERS = "orders_complete.csv"
CSV_PAYMENTS = "brand_payments.csv" 
CSV_INVOICES = "brand_invoices.csv" 
CSV_LOGS = "system_logs.csv"
CSV_PARTNERS = "partners.csv"
CSV_MESSAGES = "messages.csv"

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
# 2. DESIGN SYSTEM (CSS & JS)
# ============================================================================

def load_css_js():
    st.markdown("""
    <script>
    function updateClock() {
        const now = new Date();
        const options = { timeZone: 'Europe/Istanbul', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        const timeString = now.toLocaleTimeString('tr-TR', options);
        document.getElementById('live-clock').innerHTML = timeString + ' <span style="opacity:0.5; font-size:10px;">IST</span>';
    }
    setInterval(updateClock, 1000);
    </script>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{ box-sizing: border-box; }}
        
        .stApp {{
            background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), 
                              url("{BG_IMAGE}");
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }}
        
        .glass-card {{
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease, border-color 0.2s;
        }}
        .glass-card:hover {{
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-1px);
        }}

        h1, h2, h3, h4 {{ font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.02em; }}
        
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {{
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px);
        }}

        div.stButton > button {{
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}
        div.stButton > button:hover {{
            background: linear-gradient(135deg, #4ECDC4, #44A08D) !important;
            border-color: transparent !important;
            box-shadow: 0 0 15px rgba(78, 205, 196, 0.4);
        }}

        .os-footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(20px);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding: 10px 30px;
            font-size: 11px;
            color: rgba(255, 255, 255, 0.5);
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 9999;
        }}
        .status-dot {{ width: 6px; height: 6px; background: #10B981; border-radius: 50%; box-shadow: 0 0 8px #10B981; margin-right: 8px; }}
        .footer-clock {{ font-family: 'Space Grotesk', monospace; font-weight: 700; color: #fff; }}

        .radiant-reminder {{
            background: rgba(255, 0, 0, 0.08);
            border-left: 3px solid #ef4444;
            color: #b91c1c;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-weight: 600;
            font-size: 13px;
            animation: pulse-red 2s infinite;
        }}
        @keyframes pulse-red {{ 0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }} 70% {{ box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }} }}

        #MainMenu, header, footer {{ visibility: hidden; }}
        .block-container {{ padding-bottom: 80px; }}
    </style>
    """, unsafe_allow_html=True)

def radiant_line():
    st.markdown('<div style="height:1px; background:linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent); margin:30px 0;"></div>', unsafe_allow_html=True)

# ============================================================================
# 3. DATABASE ENGINE
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
        pd.DataFrame(columns=["Payment_ID", "Time", "Brand", "Amount", "Method", "Reference", "Status", "Proof_File", "Notes", "Fatura_Sent", "Fatura_Date", "Fatura_Explanation"]).to_csv(CSV_PAYMENTS, index=False)
    
    if not os.path.exists(CSV_INVOICES):
        pd.DataFrame(columns=["Invoice_ID", "Time", "Brand", "Amount", "Date_Range", "Invoice_Number", "Status", "Notes"]).to_csv(CSV_INVOICES, index=False)
    
    if not os.path.exists(CSV_LOGS):
        pd.DataFrame(columns=["Log_ID", "Time", "Action", "User", "Order_ID", "Details"]).to_csv(CSV_LOGS, index=False)

    if not os.path.exists(CSV_PARTNERS):
        data = {
            "partner_email": ["haki@natuvisio.com", "aurora@natuvisio.com", "long@natuvisio.com"],
            "password": ["haki2025", "aurora2025", "long2025"], 
            "brand_name": ["HAKI HEAL", "AURORACO", "LONGEVICALS"],
            "created_at": [datetime.now()]*3,
            "status": ["Active"]*3
        }
        pd.DataFrame(data).to_csv(CSV_PARTNERS, index=False)

    if not os.path.exists(CSV_MESSAGES):
        pd.DataFrame(columns=["Message_ID", "Time_UTC", "Time_IST", "From_Role", "From_Brand", "To_Role", "To_Brand", "Order_ID", "Channel", "Subject", "Body", "Read_By_Admin", "Read_By_Brand"]).to_csv(CSV_MESSAGES, index=False)

def load_csv(filename):
    try: return pd.read_csv(filename)
    except: return pd.DataFrame()

def load_logs():
    try: return pd.read_csv(CSV_LOGS)
    except: return pd.DataFrame(columns=["Log_ID", "Time", "Action", "User", "Order_ID", "Details"])

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

def save_csv(df, filename):
    df.to_csv(filename, index=False)

# ============================================================================
# 4. SESSION STATE
# ============================================================================

if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'is_partner_logged_in' not in st.session_state: st.session_state.is_partner_logged_in = False
if 'partner_brand' not in st.session_state: st.session_state.partner_brand = None
if 'cart' not in st.session_state: st.session_state.cart = []
if 'brand_lock' not in st.session_state: st.session_state.brand_lock = None

# ============================================================================
# 5. SCREENS (VIEWS)
# ============================================================================

def login_screen():
    load_css_js()
    init_databases()
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:30px;">
            <img src="{LOGO_URL}" style="width:140px; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));" onerror="this.style.display='none'">
        </div>
        """, unsafe_allow_html=True)
        
        t_adm, t_prt = st.tabs(["👑 YÖNETİCİ", "🤝 PARTNER"])
        with t_adm:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            password = st.text_input("GÜVENLİK ANAHTARI", type="password", key="adm_pass")
            if st.button("GİRİŞ YAP", use_container_width=True, key="btn_adm"):
                if password == ADMIN_PASS:
                    st.session_state.admin_logged_in = True
                    log_action("LOGIN", "admin", "", "Success")
                    st.rerun()
                else: st.error("Erişim Reddedildi")
            st.markdown('</div>', unsafe_allow_html=True)
        with t_prt:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            email = st.text_input("E-POSTA", key="prt_email")
            pwd = st.text_input("ŞİFRE", type="password", key="prt_pass")
            if st.button("PARTNER GİRİŞİ", use_container_width=True, key="btn_prt"):
                partners = load_csv(CSV_PARTNERS)
                user = partners[partners['partner_email'] == email]
                if not user.empty and str(user.iloc[0]['password']) == str(pwd):
                    st.session_state.is_partner_logged_in = True
                    st.session_state.partner_brand = user.iloc[0]['brand_name']
                    log_action("LOGIN", st.session_state.partner_brand, "", "Success")
                    st.rerun()
                else: st.error("Hatalı Bilgiler")
            st.markdown('</div>', unsafe_allow_html=True)
    render_footer()

def admin_dashboard():
    load_css_js()
    init_databases()
    # Header
    c1, c2 = st.columns([6, 1])
    with c1: st.markdown(f"<div style='display:flex;align-items:center;gap:15px;'><img src='{LOGO_URL}' style='height:35px;'><div style='border-left:1px solid rgba(255,255,255,0.2);padding-left:15px;'><div style='font-weight:700;font-size:14px;letter-spacing:1px;'>ADMIN OS v10.0</div><div style='font-size:10px;opacity:0.6;'>MASTER CONTROL</div></div></div>", unsafe_allow_html=True)
    with c2: 
        if st.button("ÇIKIŞ YAP"): st.session_state.admin_logged_in = False; st.rerun()
    radiant_line()
    # Alerts
    df_orders = load_csv(CSV_ORDERS)
    pending_notify = len(df_orders[df_orders['WhatsApp_Sent'] == 'NO'])
    if pending_notify > 0: st.markdown(f"""<div class="radiant-reminder">⚠️ {pending_notify} SİPARİŞ BİLDİRİM BEKLİYOR!</div>""", unsafe_allow_html=True)
    # Tabs
    tabs = st.tabs(["🚀 YENİ SEVKİYAT", "✅ OPERASYON", "🏦 FİNANS", "📦 SİPARİŞLER", "📊 RAPOR", "💬 MESAJLAR", "📜 LOGLAR"])
    with tabs[0]: render_new_dispatch()
    with tabs[1]: render_operations()
    with tabs[2]: render_brand_payout_hq()
    with tabs[3]: render_all_orders()
    with tabs[4]: render_analytics()
    with tabs[5]: render_messaging("NATUVISIO", "admin")
    with tabs[6]: render_logs_advanced()
    render_footer()

def partner_dashboard():
    load_css_js()
    brand = st.session_state.partner_brand
    # Header
    c1, c2 = st.columns([6, 1])
    with c1: st.markdown(f"<div style='display:flex;align-items:center;gap:15px;'><img src='{LOGO_URL}' style='height:35px;'><div style='border-left:1px solid rgba(255,255,255,0.2);padding-left:15px;'><div style='font-weight:700;font-size:14px;letter-spacing:1px;'>PARTNER PORTAL</div><div style='font-size:10px;color:{BRANDS[brand]['color']};font-weight:bold;'>{brand}</div></div></div>", unsafe_allow_html=True)
    with c2: 
        if st.button("ÇIKIŞ YAP"): st.session_state.is_partner_logged_in = False; st.rerun()
    radiant_line()
    # Partner Logic
    df_orders = load_csv(CSV_ORDERS)
    my_orders = df_orders[df_orders['Brand'] == brand]
    # Tabs
    tabs = st.tabs(["📥 YENİ SİPARİŞLER", "🚚 KARGO", "✅ GEÇMİŞ", "💰 HAKEDİŞ", "💬 MESAJLAR"])
    with tabs[0]: # New Orders
        pending = my_orders[my_orders['Status'] == 'Pending']
        if pending.empty: st.info("Bekleyen sipariş yok.")
        for idx, row in pending.iterrows():
            with st.expander(f"🆕 {row['Order_ID']}", expanded=True):
                st.write(f"**Ürün:** {row['Items']}")
                st.write(f"**Adres:** {row['Address']}")
                if st.button("✅ Onayla (Hazırlanıyor)", key=f"p_acc_{row['Order_ID']}"):
                    real_idx = df_orders.index[df_orders['Order_ID'] == row['Order_ID']][0]
                    df_orders.at[real_idx, 'Status'] = 'Notified'
                    df_orders.at[real_idx, 'WhatsApp_Sent'] = 'YES'
                    save_csv(df_orders, CSV_ORDERS)
                    st.rerun()
    with tabs[1]: # Shipping
        shipping = my_orders[my_orders['Status'] == 'Notified']
        if shipping.empty: st.info("Kargolanacak ürün yok.")
        for idx, row in shipping.iterrows():
            with st.expander(f"📦 {row['Order_ID']}", expanded=True):
                tn = st.text_input("Takip No", key=f"tn_{row['Order_ID']}")
                if st.button("Kargola", key=f"shp_{row['Order_ID']}"):
                    if tn:
                        real_idx = df_orders.index[df_orders['Order_ID'] == row['Order_ID']][0]
                        df_orders.at[real_idx, 'Status'] = 'Dispatched'
                        df_orders.at[real_idx, 'Tracking_Num'] = tn
                        save_csv(df_orders, CSV_ORDERS)
                        st.rerun()
    with tabs[2]: st.dataframe(my_orders[my_orders['Status'].isin(['Dispatched', 'Completed'])])
    with tabs[3]: # Finance
        completed = my_orders[my_orders['Status'] == 'Completed']['Brand_Payout'].sum()
        st.metric("Toplam Hakediş", f"{completed:,.2f}₺")
    with tabs[4]: render_messaging(brand, "partner")
    render_footer()

# ============================================================================
# 6. MODULES
# ============================================================================

def render_footer():
    st.markdown("""
    <div class="os-footer">
        <div style="display:flex; align-items:center; gap:8px;">
            <div class="status-dot"></div><span>SYSTEM OPERATIONAL</span>
        </div>
        <div id="live-clock" class="footer-clock">--:--:--</div>
        <div style="opacity:0.6;">CONFIDENTIAL • NATUVISIO INTERNAL USE ONLY</div>
    </div>
    """, unsafe_allow_html=True)

def render_logs_advanced():
    st.markdown("### 📜 Log Kayıtları")
    df = load_logs()
    st.dataframe(df.sort_values('Time', ascending=False), use_container_width=True)

def render_messaging(brand, role):
    st.markdown("### 💬 Mesajlar")
    df = load_csv(CSV_MESSAGES)
    
    with st.form("msg"):
        txt = st.text_area("Mesaj Yaz")
        target = st.selectbox("Alıcı", list(BRANDS.keys())) if role == 'admin' else "ADMIN"
        if st.form_submit_button("Gönder"):
            new_msg = pd.DataFrame([{
                "Message_ID": f"MSG-{int(time.time())}",
                "Time_UTC": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "From_Brand": brand if role == 'partner' else "ADMIN",
                "To_Brand": target,
                "Body": txt,
                "Read_By_Admin": "Yes" if role == 'admin' else "No",
                "Read_By_Brand": "No" if role == 'admin' else "Yes"
            }])
            df = pd.concat([df, new_msg], ignore_index=True)
            save_csv(df, CSV_MESSAGES)
            st.success("Gönderildi")

def render_new_dispatch():
    c1, c2 = st.columns([PHI, 1])
    with c1:
        st.markdown('<div class="glass-card"><h4>👤 Müşteri</h4>', unsafe_allow_html=True)
        cust = st.text_input("İsim")
        phone = st.text_input("Telefon")
        addr = st.text_area("Adres")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card"><h4>🛒 Ürün</h4>', unsafe_allow_html=True)
        if st.session_state.cart:
            active_brand = st.session_state.brand_lock
            st.info(f"🔒 {active_brand}")
        else:
            active_brand = st.selectbox("Marka", list(BRANDS.keys()))
            
        prod = st.selectbox("Ürün", list(BRANDS[active_brand]['products'].keys()))
        qty = st.number_input("Adet", 1, value=1)
        
        if st.button("Ekle"):
            price = BRANDS[active_brand]['products'][prod]['price']
            comm = BRANDS[active_brand]['commission']
            st.session_state.cart.append({
                "brand": active_brand, "product": prod, "qty": qty, "price": price,
                "subtotal": price*qty, "comm_amt": (price*qty)*comm, "payout": (price*qty)*(1-comm)
            })
            st.session_state.brand_lock = active_brand
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card"><h4>📦 Sepet</h4>', unsafe_allow_html=True)
        if st.session_state.cart:
            for item in st.session_state.cart:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; margin-bottom:10px;">
                    <div style="font-weight:bold;">{item['product']} x{item['qty']}</div>
                    <div style="font-size:12px; opacity:0.7;">{item['price']}₺ (birim)</div>
                    <hr style="border-color:rgba(255,255,255,0.1); margin:5px 0;">
                    <div style="display:flex; justify-content:space-between; font-size:13px;">
                        <span>Toplam:</span> <strong>{item['subtotal']:,.0f}₺</strong>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:12px; color:#FCD34D;">
                        <span>Komisyon:</span> <span>{item['comm_amt']:,.0f}₺</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:12px; color:#4ECDC4; font-weight:bold;">
                        <span>Marka Net:</span> <span>{item['payout']:,.0f}₺</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("SİPARİŞİ OLUŞTUR", type="primary"):
                order_id = f"NV-{datetime.now().strftime('%m%d%H%M')}"
                total = sum(x['subtotal'] for x in st.session_state.cart)
                save_order({
                    "Order_ID": order_id,
                    "Time": datetime.now().strftime('%Y-%m-%d %H:%M'),
                    "Brand": st.session_state.brand_lock,
                    "Customer": cust, "Phone": phone, "Address": addr,
                    "Items": str([f"{x['product']} (x{x['qty']})" for x in st.session_state.cart]),
                    "Total_Value": total,
                    "Commission_Amt": sum(x['comm_amt'] for x in st.session_state.cart),
                    "Brand_Payout": sum(x['payout'] for x in st.session_state.cart),
                    "Status": "Pending",
                    "WhatsApp_Sent": "NO"
                })
                st.session_state.cart = []
                st.session_state.brand_lock = None
                st.success("Sipariş alındı")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_operations():
    radiant_line()
    st.markdown("### ✅ Operasyon Yönetimi")
    df = load_csv(CSV_ORDERS)
    
    # Advanced WhatsApp Logic
    new_orders = df[df['WhatsApp_Sent'] == 'NO']
    if not new_orders.empty:
        for idx, row in new_orders.iterrows():
            with st.expander(f"🔴 {row['Order_ID']} - {row['Brand']}", expanded=True):
                brand_meta = BRANDS[row['Brand']]
                
                wa_msg = f"""━━━━━━━━━━━━━━━━━━
📦 YENİ SİPARİŞ BİLDİRİMİ  
NATUVISIO → {row['Brand']}

👤 MÜŞTERİ BİLGİLERİ  
• Ad Soyad: {row['Customer']}  
• Telefon: {row['Phone']}  
• Adres: {row['Address']}

🛒 SİPARİŞ DETAYLARI  
• Ürün: {row['Items']}  
• Toplam Satış Bedeli: {row['Total_Value']}₺  
• Sipariş No: {row['Order_ID']}

💰 KOMİSYON & ÖDEME DAĞILIMI  
• Komisyon Tutarı: {row['Commission_Amt']}₺  
• Markaya Net Ödeme: {row['Brand_Payout']}₺  

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
                        save_csv(df, CSV_ORDERS)
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

# ============================================================================
# 7. MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    if st.session_state.admin_logged_in:
        admin_dashboard()
    elif st.session_state.is_partner_logged_in:
        partner_dashboard()
    else:
        login_screen()
