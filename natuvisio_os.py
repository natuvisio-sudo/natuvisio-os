import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import time
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO YÖNETİM SİSTEMİ - TÜRKÇE VERSİYON (v4.0)
# Finansal Motor + Fatura Takibi + Marka Ödemeleri
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
CSV_PAYMENTS = "brand_payments.csv" # Ödemeler (Bizim markaya gönderdiğimiz)
CSV_INVOICES = "brand_invoices.csv" # Faturalar (Bizim markaya kestiğimiz)
CSV_LOGS = "system_logs.csv"
PHI = 1.618

FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

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

def get_icon(name, color="#ffffff", size=24):
    icons = {
        "mountain": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M3 20L9 8L12 14L15 6L21 20H3Z"/></svg>',
        "alert": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3"><path d="M20 6L9 17L4 12"/></svg>',
        "bill": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><line x1="6" y1="8" x2="6" y2="8"/><line x1="10" y1="8" x2="18" y2="8"/><line x1="6" y1="12" x2="6" y2="12"/><line x1="10" y1="12" x2="18" y2="12"/><line x1="6" y1="16" x2="6" y2="16"/><line x1="10" y1="16" x2="18" y2="16"/></svg>',
        "money": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "clock": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "activity": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
    }
    return icons.get(name, "")

# ============================================================================
# 3. CSS TASARIM SİSTEMİ
# ============================================================================

def load_css(theme="dark"):
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        .stApp {{
            background-image: linear-gradient(rgba(15, 23, 42, 0.92), rgba(15, 23, 42, 0.96)), 
                              url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }}
        
        .glass-card {{
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur({FIBO['md']}px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: {FIBO['sm']}px;
            padding: {FIBO['md']}px;
            margin-bottom: {FIBO['sm']}px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        .glass-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.15);
        }}
        
        .metric-value {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
        }}
        
        .metric-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: rgba(255,255,255,0.5);
            font-weight: 600;
        }}
        
        h1, h2, h3, h4 {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: #ffffff !important;
            font-weight: 700 !important;
        }}
        
        /* Butonlar */
        div.stButton > button {{
            background: linear-gradient(135deg, #4ECDC4, #44A08D) !important;
            color: white !important;
            border: none !important;
            padding: {FIBO['sm']}px {FIBO['md']}px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            transition: all 0.3s ease !important;
        }}
        
        div.stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(78, 205, 196, 0.3);
        }}
        
        /* Girdi Alanları */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {{
            background: rgba(0,0,0,0.3) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }}
        
        #MainMenu, header, footer {{ visibility: hidden; }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.05); }}
        ::-webkit-scrollbar-thumb {{ background: rgba(78,205,196,0.3); border-radius: 3px; }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 4. VERİTABANI YÖNETİMİ
# ============================================================================

def init_databases():
    # Sipariş Veritabanı
    if not os.path.exists(CSV_ORDERS):
        pd.DataFrame(columns=[
            "Order_ID", "Time", "Brand", "Customer", "Phone", "Address",
            "Items", "Total_Value", "Commission_Rate", "Commission_Amt",
            "Brand_Payout", "Status", "WhatsApp_Sent", "Tracking_Num",
            "Priority", "Notes", "Created_By", "Last_Modified"
        ]).to_csv(CSV_ORDERS, index=False)
    
    # Ödemeler (Giden Para)
    if not os.path.exists(CSV_PAYMENTS):
        pd.DataFrame(columns=[
            "Payment_ID", "Time", "Brand", "Amount", "Method", "Reference", 
            "Status", "Proof_File", "Notes"
        ]).to_csv(CSV_PAYMENTS, index=False)
        
    # Faturalar (Kesilen Fatura)
    if not os.path.exists(CSV_INVOICES):
        pd.DataFrame(columns=[
            "Invoice_ID", "Time", "Brand", "Amount", "Date_Range", 
            "Invoice_Number", "Status", "Notes"
        ]).to_csv(CSV_INVOICES, index=False)
    
    # Log Kayıtları
    if not os.path.exists(CSV_LOGS):
        pd.DataFrame(columns=[
            "Log_ID", "Time", "Action", "User", "Order_ID", "Details"
        ]).to_csv(CSV_LOGS, index=False)

# --- Yükleme Fonksiyonları ---
def load_orders():
    try: return pd.read_csv(CSV_ORDERS)
    except: return pd.DataFrame()

def load_payments():
    try: return pd.read_csv(CSV_PAYMENTS)
    except: return pd.DataFrame()

def load_invoices():
    try: return pd.read_csv(CSV_INVOICES)
    except: return pd.DataFrame()

# --- Kayıt Fonksiyonları ---
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
        df = pd.read_csv(CSV_LOGS) if os.path.exists(CSV_LOGS) else pd.DataFrame()
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
# 5. OTURUM YÖNETİMİ (SESSION)
# ============================================================================

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'brand_lock' not in st.session_state:
    st.session_state.brand_lock = None

# ============================================================================
# 6. GİRİŞ EKRANI
# ============================================================================

def login_screen():
    load_css()
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['xl']}px;">
            <div style="font-size: {FIBO['xl']}px; margin-bottom: {FIBO['sm']}px;">🏔️</div>
            <h2>NATUVISIO ADMIN</h2>
            <p style="opacity: 0.6; font-size: 12px;">TÜRKÇE OPERASYON SİSTEMİ</p>
        </div>
        """, unsafe_allow_html=True)
        
        password = st.text_input("Erişim Şifresi", type="password", key="login")
        
        if st.button("🔓 GİRİŞ YAP", use_container_width=True):
            if password == ADMIN_PASS:
                st.session_state.admin_logged_in = True
                log_action("GİRİŞ", "admin", "", "Başarılı giriş")
                st.rerun()
            else:
                st.error("❌ Hatalı şifre")

# ============================================================================
# 7. ANA PANEL (DASHBOARD)
# ============================================================================

def dashboard():
    load_css()
    init_databases()
    
    # --- BAŞLIK ---
    col_h1, col_h2 = st.columns([6, 1])
    with col_h1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: {FIBO['sm']}px;">
            {get_icon('mountain', '#4ECDC4', FIBO['lg'])}
            <div>
                <h1 style="margin:0;">YÖNETİM MERKEZİ</h1>
                <span style="font-size: 11px; opacity: 0.6;">TAM YETKİLİ ERİŞİM</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h2:
        if st.button("🚪 Çıkış"):
            st.session_state.admin_logged_in = False
            st.session_state.cart = []
            st.rerun()
            
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # --- ÜST METRİKLER ---
    df = load_orders()
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    total_rev = df['Total_Value'].sum() if not df.empty else 0
    total_comm = df['Commission_Amt'].sum() if not df.empty else 0
    pending_count = len(df[df['Status'] == 'Pending'])
    
    with col_m1:
        st.markdown(f"""<div class="glass-card" style="text-align:center;">
            <div class="metric-label">TOPLAM CİRO</div>
            <div class="metric-value">{total_rev:,.0f}₺</div>
        </div>""", unsafe_allow_html=True)
        
    with col_m2:
        st.markdown(f"""<div class="glass-card" style="text-align:center; border-top: 3px solid #4ECDC4;">
            <div class="metric-label">NET KOMİSYON</div>
            <div class="metric-value" style="color:#4ECDC4;">{total_comm:,.0f}₺</div>
        </div>""", unsafe_allow_html=True)
        
    with col_m3:
        st.markdown(f"""<div class="glass-card" style="text-align:center; border-top: 3px solid #F59E0B;">
            <div class="metric-label">BEKLEYEN İŞLEM</div>
            <div class="metric-value" style="color:#F59E0B;">{pending_count}</div>
        </div>""", unsafe_allow_html=True)
        
    with col_m4:
        st.markdown(f"""<div class="glass-card" style="text-align:center;">
            <div class="metric-label">TOPLAM SİPARİŞ</div>
            <div class="metric-value">{len(df)}</div>
        </div>""", unsafe_allow_html=True)

    # --- SEKMELER ---
    tabs = st.tabs([
        "🚀 YENİ SEVKİYAT", 
        "✅ OPERASYON", 
        "📑 MUTABAKAT & FİNANS", 
        "📦 TÜM SİPARİŞLER",
        "📊 ANALİTİK"
    ])
    
    with tabs[0]: render_new_dispatch()
    with tabs[1]: render_operations()
    with tabs[2]: render_financial_obligations() # YENİ MODÜL
    with tabs[3]: render_all_orders()
    with tabs[4]: render_analytics()

# ============================================================================
# 8. YENİ SEVKİYAT MODÜLÜ (NEW DISPATCH)
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
        line_total = prod_details['price'] * qty
        comm_amt = line_total * brand_data['commission']
        
        if st.button("➕ Sepete Ekle"):
            st.session_state.cart.append({
                "brand": active_brand,
                "product": prod,
                "sku": prod_details['sku'],
                "qty": qty,
                "subtotal": line_total,
                "comm_amt": comm_amt
            })
            st.session_state.brand_lock = active_brand
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_R:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📦 Sepet Özeti")
        
        if st.session_state.cart:
            for item in st.session_state.cart:
                st.markdown(f"**{item['product']}** x{item['qty']} = {item['subtotal']:,.0f}₺")
            
            total = sum(i['subtotal'] for i in st.session_state.cart)
            total_comm = sum(i['comm_amt'] for i in st.session_state.cart)
            
            st.markdown(f"""
            <div style="background: rgba(78,205,196,0.2); padding: 10px; border-radius: 8px; margin: 10px 0;">
                <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:18px;">
                    <span>TOPLAM:</span>
                    <span>{total:,.0f}₺</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
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
                        'Brand_Payout': total - total_comm,
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
# 9. OPERASYON MODÜLÜ (OPERATIONS)
# ============================================================================

def render_operations():
    st.markdown("### ✅ Operasyon Yönetimi")
    df = load_orders()
    
    # Whatsapp Gönderilmeyenler
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
    
    # Takip No Bekleyenler
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

    # Tamamlanacaklar
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
# 10. FİNANSAL YÜKÜMLÜLÜKLER MODÜLÜ (NEW FINANCIAL ENGINE)
# ============================================================================

def render_financial_obligations():
    st.markdown("## 📑 MUTABAKAT VE FİNANS")
    
    tab_inv, tab_pay = st.tabs(["📄 FATURA (ALACAKLAR)", "💸 ÖDEME (BORÇLAR)"])
    
    df_orders = load_orders()
    df_invoices = load_invoices()
    df_payments = load_payments()
    
    # Sadece tamamlanmış siparişler finansallaşır
    completed_orders = df_orders[df_orders['Status'] == 'Completed']
    
    # --- TAB 1: FATURA (KOMİSYON ALACAKLARI) ---
    with tab_inv:
        st.markdown("### 📥 Fatura Açılacak Tutarlar (Bizim Alacağımız)")
        
        for brand in BRANDS.keys():
            brand_orders = completed_orders[completed_orders['Brand'] == brand]
            
            # Hesaplamalar
            total_comm_due = brand_orders['Commission_Amt'].sum()
            
            # Kesilmiş faturalar
            brand_invoices = df_invoices[df_invoices['Brand'] == brand]
            total_invoiced = brand_invoices['Amount'].sum() if not brand_invoices.empty else 0
            
            not_invoiced = total_comm_due - total_invoiced
            
            with st.expander(f"📄 {brand} - Fatura Bekleyen: {not_invoiced:,.2f}₺", expanded=(not_invoiced > 0)):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="font-size:12px; opacity:0.7;">TOPLAM KOMİSYON HAKEDİŞİ</div>
                        <div style="font-size:24px; font-weight:bold;">{total_comm_due:,.2f}₺</div>
                        <hr style="border-color: rgba(255,255,255,0.1);">
                        <div style="font-size:12px; opacity:0.7;">HENÜZ FATURALAŞMAMIŞ</div>
                        <div style="font-size:24px; font-weight:bold; color:#4ECDC4;">{not_invoiced:,.2f}₺</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("#### 📝 Fatura Kes")
                    if not_invoiced > 0:
                        inv_amount = st.number_input("Fatura Tutarı", value=float(not_invoiced), key=f"inv_amt_{brand}")
                        inv_date = st.date_input("Fatura Tarihi", datetime.now(), key=f"inv_date_{brand}")
                        inv_no = st.text_input("Fatura No (örn: GIB2025...)", key=f"inv_no_{brand}")
                        
                        if st.button("✅ Faturayı İşle", key=f"btn_inv_{brand}"):
                            inv_data = {
                                "Invoice_ID": f"INV-{datetime.now().strftime('%m%d%H%M')}",
                                "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "Brand": brand,
                                "Amount": inv_amount,
                                "Date_Range": str(inv_date),
                                "Invoice_Number": inv_no,
                                "Status": "Issued",
                                "Notes": "Otomatik oluşturuldu"
                            }
                            if save_invoice(inv_data):
                                st.success("Fatura sisteme işlendi!")
                                time.sleep(1)
                                st.rerun()
                    else:
                        st.success("Tüm komisyonlar faturalandırıldı.")
                        
                # Fatura Geçmişi Tablosu
                if not brand_invoices.empty:
                    st.markdown("###### 📜 Kesilen Faturalar")
                    st.dataframe(brand_invoices[['Time', 'Invoice_Number', 'Amount', 'Status']], use_container_width=True)

    # --- TAB 2: ÖDEME (MARKA HAKEDİŞLERİ) ---
    with tab_pay:
        st.markdown("### 📤 Yapılacak Ödemeler (Marka Hakedişleri)")
        
        for brand in BRANDS.keys():
            brand_orders = completed_orders[completed_orders['Brand'] == brand]
            
            # Hesaplamalar
            total_payout_due = brand_orders['Brand_Payout'].sum()
            
            # Yapılan Ödemeler
            brand_payments = df_payments[df_payments['Brand'] == brand]
            total_paid = brand_payments['Amount'].sum() if not brand_payments.empty else 0
            
            balance_to_pay = total_payout_due - total_paid
            
            # Renk kodu: Borç varsa kırmızı, yoksa yeşil
            header_color = "#EF4444" if balance_to_pay > 10 else "#10B981"
            
            with st.expander(f"💸 {brand} - Ödenecek: {balance_to_pay:,.2f}₺"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 4px solid {header_color};">
                        <div style="font-size:12px; opacity:0.7;">TOPLAM HAKEDİŞ</div>
                        <div style="font-size:20px; font-weight:bold;">{total_payout_due:,.2f}₺</div>
                        
                        <div style="font-size:12px; opacity:0.7; margin-top:10px;">GÖNDERİLEN</div>
                        <div style="font-size:20px; font-weight:bold;">{total_paid:,.2f}₺</div>
                        
                        <div style="font-size:12px; opacity:0.7; margin-top:10px;">KALAN BAKİYE</div>
                        <div style="font-size:28px; font-weight:bold; color:{header_color};">{balance_to_pay:,.2f}₺</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info(f"🏦 IBAN: {BRANDS[brand]['iban']}\n👤 {BRANDS[brand]['account_name']}")
                
                with col2:
                    st.markdown("#### 💳 Ödeme Emri Gir")
                    if balance_to_pay > 0:
                        pay_amt = st.number_input("Gönderilecek Tutar", value=float(balance_to_pay), key=f"pay_amt_{brand}")
                        pay_ref = st.text_input("Dekont / Referans No", key=f"pay_ref_{brand}")
                        
                        st.markdown(f"*Açıklama Önerisi:* NATUVISIO {brand} Hakediş Ödemesi")
                        
                        if st.button("🚀 Ödemeyi Kaydet", key=f"btn_pay_{brand}"):
                            pay_data = {
                                "Payment_ID": f"PAY-{datetime.now().strftime('%m%d%H%M')}",
                                "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "Brand": brand,
                                "Amount": pay_amt,
                                "Method": "Bank Transfer",
                                "Reference": pay_ref,
                                "Status": "Sent",
                                "Proof_File": "",
                                "Notes": "Admin onayıyla gönderildi"
                            }
                            if save_payment(pay_data):
                                st.success("Ödeme kaydı oluşturuldu!")
                                time.sleep(1)
                                st.rerun()
                    else:
                        st.success("Borç bakiyesi bulunmuyor.")
                
                # Ödeme Geçmişi
                if not brand_payments.empty:
                    st.markdown("###### 📜 Ödeme Geçmişi")
                    st.dataframe(brand_payments[['Time', 'Amount', 'Reference', 'Status']], use_container_width=True)

# ============================================================================
# 11. DİĞER FONKSİYONLAR
# ============================================================================

def render_all_orders():
    st.markdown("### 📦 Tüm Sipariş Geçmişi")
    df = load_orders()
    if not df.empty:
        st.dataframe(df.sort_values('Time', ascending=False), use_container_width=True)
    else:
        st.info("Kayıt yok")

def render_analytics():
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

# ============================================================================
# 12. ANA ÇALIŞTIRMA (MAIN)
# ============================================================================

if __name__ == "__main__":
    if not st.session_state.admin_logged_in:
        login_screen()
    else:
        dashboard()
