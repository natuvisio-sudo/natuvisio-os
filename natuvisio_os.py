import streamlit as st
import pandas as pd
import os
import io
import time
from datetime import datetime, timedelta, date
import urllib.parse
import plotly.express as px  # NEW: Premium Charts

# ============================================================================
# 🏔️ NATUVISIO ADMIN OS - V12.0 (PREMIUM ANALYTICS & LEGAL EDITION)
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Bridge OS",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 1. CONFIGURATION & DATA MODELS
# ============================================================================

# --- CREDENTIALS ---
ADMIN_PASS = "admin2025"
BRAND_CREDENTIALS = {
    "HAKI HEAL": "haki123",
    "AURORACO": "aurora2025",
    "LONGEVICALS": "longsci"
}

# --- DATABASE FILES ---
CSV_DISPATCH = "dispatch_history.csv"
CSV_FINANCE = "financial_ledger.csv"
CSV_INVOICES = "invoice_registry.csv"
CSV_PAYOUTS = "payout_history.csv"
CSV_LOGS = "system_logs.csv"

# --- UI CONSTANTS ---
PHI = 1.618
FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}
LOGO_URL = "https://res.cloudinary.com/deb1j92hy/image/upload/f_auto,q_auto/v1764805291/natuvisio_logo_gtqtfs.png"
BG_IMAGE = "https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp"

# --- BUSINESS LOGIC ---
KDV_RATE = 0.20 

BRAND_CONTRACTS = {
    "HAKI HEAL": {
        "commission": 0.15,
        "phone": "601158976276",
        "color": "#4ECDC4",
        "iban": "TR90 0006 1000 0000 1234 5678 90",
        "email": "finance@hakiheal.com",
        "bank_name": "Haki Heal Ltd. Şti."
    },
    "AURORACO": {
        "commission": 0.20,
        "phone": "601158976276",
        "color": "#FF6B6B",
        "iban": "TR90 0006 2000 0000 9876 5432 10",
        "email": "ops@auroraco.com",
        "bank_name": "Auroraco Gıda A.Ş."
    },
    "LONGEVICALS": {
        "commission": 0.12,
        "phone": "601158976276",
        "color": "#95E1D3",
        "iban": "TR90 0001 5000 0000 1122 3344 55",
        "email": "accounting@longevicals.com",
        "bank_name": "Longevicals Sağlık A.Ş."
    }
}

PRODUCT_DB = {
    "HAKI HEAL": {
        "HAKI HEAL KREM": {"sku": "SKU-HAKI-CRM", "price": 450},
        "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY", "price": 380},
        "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP", "price": 120}
    },
    "AURORACO": {
        "AURORACO MATCHA": {"sku": "SKU-AUR-MATCHA", "price": 650},
        "AURORACO CACAO": {"sku": "SKU-AUR-CACAO", "price": 550},
        "AURORACO SUPER": {"sku": "SKU-AUR-SUPER", "price": 800}
    },
    "LONGEVICALS": {
        "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
        "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
    }
}

# ============================================================================
# 2. CORE ENGINE (DATABASE & HELPERS)
# ============================================================================

def init_databases():
    """Ensure all CSV ledgers exist with correct headers"""
    if not os.path.exists(CSV_DISPATCH):
        pd.DataFrame(columns=[
            "Order_ID", "Time", "Brand", "Customer", "Phone", "Address",
            "Items", "Total_Value", "Status", "Tracking_Num", "WhatsApp_Sent", 
            "Notes", "Priority"
        ]).to_csv(CSV_DISPATCH, index=False)
    
    if not os.path.exists(CSV_FINANCE):
        pd.DataFrame(columns=[
            "Order_ID", "Time", "Brand", "Total_Sale", "Commission_Rate",
            "Commission_Amt", "KDV_Amt", "Total_Deduction", "Payable_To_Brand", 
            "Invoice_Ref", "Payment_Status"
        ]).to_csv(CSV_FINANCE, index=False)

    if not os.path.exists(CSV_INVOICES):
        pd.DataFrame(columns=[
            "Invoice_Ref", "Date", "Brand", "Total_Commission", "Total_KDV", 
            "Total_Invoice_Amt", "Order_Count", "Sent_Status", "Paid_Status", "Notes"
        ]).to_csv(CSV_INVOICES, index=False)

    if not os.path.exists(CSV_PAYOUTS):
        pd.DataFrame(columns=[
            "Payout_ID", "Time", "Brand", "Amount", "Method", 
            "Reference", "Notes"
        ]).to_csv(CSV_PAYOUTS, index=False)

    if not os.path.exists(CSV_LOGS):
        pd.DataFrame(columns=[
            "Log_ID", "Time", "Action", "User", "Details"
        ]).to_csv(CSV_LOGS, index=False)

def get_db(file):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame()

def save_db(file, df, new_row=None):
    if new_row is not None:
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(file, index=False)
    return df

def update_db(file, df):
    df.to_csv(file, index=False)

def log_action(action, user, details):
    df = get_db(CSV_LOGS)
    new_log = {
        "Log_ID": f"LOG-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Action": action,
        "User": user,
        "Details": details
    }
    save_db(CSV_LOGS, df, new_log)

def get_icon(name, color="#5b7354"):
    icons = {
        "mountain": "🏔️", "alert": "⚠️", "check": "✅", "bill": "🧾",
        "money": "💰", "clock": "⏳", "truck": "🚚"
    }
    return icons.get(name, "📦")

# ============================================================================
# 3. PREMIUM DESIGN SYSTEM
# ============================================================================

def load_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=Inter:wght@300;400;600&display=swap');

        /* BACKGROUND */
        .stApp {{
            background-image: linear-gradient(rgba(245, 245, 240, 0.90), rgba(245, 245, 240, 0.95)), 
                              url("{BG_IMAGE}");
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #000000;
        }}

        /* GLASS CONTAINERS */
        .glass-card {{
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(24px);
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            color: #000000 !important;
        }}
        
        .glass-card h4, .glass-card h3, .glass-card div {{
            color: #000000 !important;
        }}

        /* TYPOGRAPHY */
        h1, h2, h3, h4 {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: #1a1a1a !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }}
        
        /* METRICS */
        .metric-container {{ text-align: center; padding: 10px; }}
        .metric-value {{
            font-family: 'Space Grotesk';
            font-size: 32px;
            font-weight: 800;
            color: #000000;
            letter-spacing: -1px;
        }}
        .metric-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #4a5568;
            font-weight: 700;
        }}

        /* BUTTONS */
        div.stButton > button {{
            background: #2f855a !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 6px rgba(47, 133, 90, 0.2) !important;
        }}
        div.stButton > button:hover {{
            background: #276749 !important;
            transform: translateY(-1px);
        }}

        /* INPUTS */
        .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {{
            background: #ffffff !important;
            border: 1px solid #cbd5e0 !important;
            color: #000000 !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }}
        
        /* FOOTER */
        .legal-footer {{
            margin-top: 50px;
            padding: 20px;
            border-top: 1px solid rgba(0,0,0,0.1);
            text-align: center;
            font-size: 11px;
            color: #718096;
            font-family: 'Inter', sans-serif;
        }}

        #MainMenu, header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 4. SESSION STATE MANAGEMENT
# ============================================================================

if 'page' not in st.session_state: st.session_state.page = 'login'
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'logged_brand' not in st.session_state: st.session_state.logged_brand = None
if 'cart' not in st.session_state: st.session_state.cart = []
if 'selected_brand_lock' not in st.session_state: st.session_state.selected_brand_lock = None
if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'is_partner_logged_in' not in st.session_state: st.session_state.is_partner_logged_in = False

# ============================================================================
# 5. UI COMPONENT: SECURE FOOTER
# ============================================================================

def render_footer():
    st.markdown("""
    <div class="legal-footer">
        <p><strong>🔒 NATUVISIO OPERATING SYSTEM | INTERNAL USE ONLY</strong></p>
        <p>This platform and its data are strictly confidential. Unauthorized distribution to third parties is prohibited.</p>
        <p>In case of system error, contact <strong>admin@natuvisio.com</strong> immediately.</p>
        <p>© 2025 NATUVISIO Operations • Built for Speed, Science, and Trust</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# 6. VIEW: LOGIN SCREEN
# ============================================================================

def login_view():
    load_css()
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 40px;">
            <div style="font-size: 50px; margin-bottom: 20px;">🌿</div>
            <h2 style="margin-bottom: 10px;">NATUVISIO BRIDGE</h2>
            <p style="color: #4a5568; font-weight: 600; font-size: 12px; margin-bottom: 30px;">SECURE LOGISTICS OPERATING SYSTEM</p>
        </div>
        """, unsafe_allow_html=True)
        
        role = st.selectbox("Giriş Türü", ["Yönetici (Admin)", "Marka Partneri"], key="login_role_select")
        
        if role == "Marka Partneri":
            brand_user = st.selectbox("Marka Seçiniz", list(BRAND_CREDENTIALS.keys()), key="login_brand_select")
        
        pwd = st.text_input("Erişim Şifresi", type="password", key="login_password")
        
        if st.button("GİRİŞ YAP", use_container_width=True, key="login_btn"):
            if role == "Yönetici (Admin)":
                if pwd == ADMIN_PASS:
                    st.session_state.user_role = 'ADMIN'
                    st.session_state.admin_logged_in = True
                    st.session_state.page = 'admin_dashboard'
                    st.rerun()
                else:
                    st.error("Hatalı Yönetici Şifresi")
            
            elif role == "Marka Partneri":
                if pwd == BRAND_CREDENTIALS.get(brand_user):
                    st.session_state.user_role = 'PARTNER'
                    st.session_state.logged_brand = brand_user
                    st.session_state.is_partner_logged_in = True
                    st.session_state.page = 'partner_dashboard'
                    st.rerun()
                else:
                    st.error("Hatalı Marka Şifresi")
    
    render_footer()

# ============================================================================
# 7. VIEW: ADMIN DASHBOARD
# ============================================================================

def admin_dashboard():
    load_css()
    init_databases()
    
    # Header
    c1, c2 = st.columns([6,1])
    with c1: 
        st.markdown(f"## 🏔️ YÖNETİM MERKEZİ")
        st.markdown("**Yetki:** Master Operator | **Durum:** Çevrimiçi")
    with c2:
        if st.button("ÇIKIŞ YAP", key="admin_logout"):
            st.session_state.admin_logged_in = False
            st.session_state.page = 'login'
            st.rerun()
    st.markdown("---")

    # --- DATE RANGE FILTER ---
    c_date1, c_date2, c_gap = st.columns([2, 2, 4])
    with c_date1:
        start_date = st.date_input("Başlangıç Tarihi", value=datetime.now() - timedelta(days=30))
    with c_date2:
        end_date = st.date_input("Bitiş Tarihi", value=datetime.now())

    # --- METRICS & DATE FILTERING ---
    df_disp = get_db(CSV_DISPATCH)
    df_fin = get_db(CSV_FINANCE)
    
    if not df_disp.empty:
        df_disp['Time'] = pd.to_datetime(df_disp['Time'])
        mask = (df_disp['Time'].dt.date >= start_date) & (df_disp['Time'].dt.date <= end_date)
        df_disp_filtered = df_disp.loc[mask]
    else:
        df_disp_filtered = df_disp
        
    if not df_fin.empty:
        df_fin['Time'] = pd.to_datetime(df_fin['Time'])
        mask_f = (df_fin['Time'].dt.date >= start_date) & (df_fin['Time'].dt.date <= end_date)
        df_fin_filtered = df_fin.loc[mask_f]
    else:
        df_fin_filtered = df_fin

    total_rev = df_fin_filtered['Total_Sale'].sum() if not df_fin.empty else 0
    total_comm = df_fin_filtered['Commission_Amt'].sum() if not df_fin.empty else 0
    pending_ops = len(df_disp[df_disp['Status'] == 'Pending']) if not df_disp.empty else 0
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f"<div class='glass-card metric-container'><div class='metric-value'>{len(df_disp_filtered)}</div><div class='metric-label'>TOPLAM SİPARİŞ</div></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='glass-card metric-container'><div class='metric-value'>{total_rev:,.0f}₺</div><div class='metric-label'>TOPLAM CİRO</div></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='glass-card metric-container'><div class='metric-value' style='color:#2f855a;'>{total_comm:,.0f}₺</div><div class='metric-label'>NET GELİR</div></div>", unsafe_allow_html=True)
    with m4: st.markdown(f"<div class='glass-card metric-container'><div class='metric-value' style='color:#c53030;'>{pending_ops}</div><div class='metric-label'>BEKLEYEN İŞLEM</div></div>", unsafe_allow_html=True)

    # --- MARKALAR TRACKING TABLE (SYNCED & TIME-STAMPED) ---
    st.markdown("### 📊 Marka Performans Özeti")
    if not df_fin.empty:
        brand_stats = df_fin.groupby('Brand').agg({
            'Total_Sale': 'sum',
            'Commission_Amt': 'sum',
            'Payable_To_Brand': 'sum'
        }).reset_index()
        
        unpaid_stats = df_fin[df_fin['Payment_Status'] == 'Unpaid'].groupby('Brand')['Payable_To_Brand'].sum().reset_index()
        unpaid_stats.columns = ['Brand', 'Bekleyen_Odeme']
        
        final_stats = pd.merge(brand_stats, unpaid_stats, on='Brand', how='left').fillna(0)
        final_stats['Son Güncelleme'] = datetime.now().strftime('%H:%M:%S') # Live Snapshot
        
        st.dataframe(
            final_stats,
            column_config={
                "Brand": "Marka",
                "Total_Sale": st.column_config.NumberColumn("Toplam Satış", format="%d ₺"),
                "Commission_Amt": st.column_config.NumberColumn("Komisyon", format="%d ₺"),
                "Payable_To_Brand": st.column_config.NumberColumn("Toplam Hakediş", format="%d ₺"),
                "Bekleyen_Odeme": st.column_config.NumberColumn("Ödenecek (Bekleyen)", format="%d ₺"),
                "Son Güncelleme": "Sistem Saati"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Veri yok.")

    # --- MASTER NAVIGATION ---
    tabs = st.tabs([
        "🚀 YENİ SEVKİYAT", 
        "🚀 SİPARİŞ TAKİBİ", 
        "✅ OPERASYON", 
        "🏦 FATURA & ÖDEME", 
        "💵 MARKA ÖDEMELERİ", 
        "🧾 MARKA FATURALANDIRMA", 
        "📦 TÜM SİPARİŞLER", 
        "📊 ANALİTİKLER", 
        "❔ REHBER", 
        "📜 LOG KAYITLARI",
        "📥 EXPORT DATA"
    ])

    # --- 1. YENİ SEVKİYAT (New Dispatch) ---
    with tabs[0]:
        c_form, c_cart = st.columns([1.5, 1])
        with c_form:
            st.markdown('<div class="glass-card"><h4>📝 Sipariş Oluştur</h4>', unsafe_allow_html=True)
            if 'cart' not in st.session_state: st.session_state.cart = []
            
            cust_name = st.text_input("Müşteri Adı Soyadı", key="dispatch_cust_name")
            cust_phone = st.text_input("Telefon (905...)", key="dispatch_cust_phone")
            cust_addr = st.text_area("Adres", key="dispatch_cust_addr")
            
            st.markdown("---")
            if st.session_state.cart:
                act_brand = st.session_state.cart[0]['Brand']
                st.info(f"Kilitli Marka: {act_brand}")
            else:
                act_brand = st.selectbox("Marka Seçiniz", list(BRAND_CONTRACTS.keys()), key="dispatch_brand_select")
            
            cp, cq = st.columns([3, 1])
            with cp: prod = st.selectbox("Ürün", list(PRODUCT_DB[act_brand].keys()), key="dispatch_prod_select")
            with cq: qty = st.number_input("Adet", 1, value=1, key="dispatch_qty")
            
            if st.button("➕ Sepete Ekle", key="dispatch_add_btn"):
                p_data = PRODUCT_DB[act_brand][prod]
                rate = BRAND_CONTRACTS[act_brand]["commission"]
                tot = p_data['price'] * qty
                comm = tot * rate
                kdv = comm * KDV_RATE 
                deduction = comm + kdv
                payable = tot - deduction
                
                st.session_state.cart.append({
                    "Brand": act_brand, "Product": prod, "Qty": qty, 
                    "Total": tot, "Comm": comm, "KDV": kdv, "Deduction": deduction, "Payable": payable
                })
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with c_cart:
            st.markdown('<div class="glass-card"><h4>📦 Sepet Özeti</h4>', unsafe_allow_html=True)
            if st.session_state.cart:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.dataframe(cart_df[["Product", "Qty", "Total"]], hide_index=True)
                
                total_val = cart_df['Total'].sum()
                total_deduct = cart_df['Deduction'].sum()
                total_pay = cart_df['Payable'].sum()
                
                st.markdown(f"<h3 style='text-align:right'>{total_val:,.0f} TL</h3>", unsafe_allow_html=True)
                st.caption(f"Komisyon + KDV Kesintisi: {total_deduct:,.2f} TL")
                st.success(f"Markaya Ödenecek Net: {total_pay:,.2f} TL")
                
                if st.button("⚡ SİPARİŞİ ONAYLA", key="dispatch_confirm_btn"):
                    if cust_name and cust_phone:
                        oid = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
                        items = ", ".join([f"{x['Product']} (x{x['Qty']})" for x in st.session_state.cart])
                        
                        # Save Physical
                        d_df = get_db(CSV_DISPATCH)
                        save_db(CSV_DISPATCH, d_df, {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": act_brand,
                            "Customer": cust_name, "Phone": cust_phone, "Address": cust_addr,
                            "Items": items, "Total_Value": total_val,
                            "Status": "Pending", "Tracking_Num": "", "WhatsApp_Sent": "NO",
                            "Priority": "Standard", "Notes": ""
                        })
                        
                        # Save Finance
                        f_df = get_db(CSV_FINANCE)
                        save_db(CSV_FINANCE, f_df, {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": act_brand,
                            "Total_Sale": total_val, "Commission_Rate": BRAND_CONTRACTS[act_brand]['commission'],
                            "Commission_Amt": cart_df['Comm'].sum(), 
                            "KDV_Amt": cart_df['KDV'].sum(),
                            "Total_Deduction": total_deduct,
                            "Payable_To_Brand": total_pay,
                            "Invoice_Ref": "", "Payment_Status": "Unpaid"
                        })
                        
                        log_action("SİPARİŞ", "Admin", f"Sipariş oluşturuldu: {oid}")
                        st.success("Sipariş başarıyla oluşturuldu!")
                        st.session_state.cart = []
                        st.rerun()
                    else:
                        st.error("Müşteri bilgileri eksik.")
                
                if st.button("Sepeti Temizle", key="dispatch_clear_btn"):
                    st.session_state.cart = []
                    st.rerun()
            else:
                st.info("Sepet boş.")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- 2. SİPARİŞ TAKİBİ (Live View with Approved Details) ---
    with tabs[1]:
        st.markdown("### 🔭 Aktif Sipariş Takibi")
        df = get_db(CSV_DISPATCH)
        if not df.empty:
            active_df = df[df['Status'].isin(['Pending', 'Notified', 'Dispatched', 'Completed'])].sort_values("Time", ascending=False)
            
            st.dataframe(
                active_df,
                use_container_width=True,
                column_config={
                    "Status": st.column_config.SelectboxColumn("Durum", options=['Pending', 'Notified', 'Dispatched', 'Completed'], disabled=True),
                    "Tracking_Num": "Takip No",
                    "WhatsApp_Sent": "Bildirim"
                }
            )
        else:
            st.info("Aktif sipariş bulunmuyor.")

    # --- 3. OPERASYON (Action Center) ---
    with tabs[2]:
        st.markdown("### ✅ Operasyon Merkezi")
        df = get_db(CSV_DISPATCH)
        
        # A. Notifications
        pending_ntf = df[df['WhatsApp_Sent'] == 'NO'].sort_values("Time", ascending=False)
        if not pending_ntf.empty:
            st.warning(f"⚠️ {len(pending_ntf)} Sipariş Bildirim Bekliyor")
            for idx, row in pending_ntf.iterrows():
                with st.container():
                    st.markdown(f"""<div class='glass-card status-alert-red'>
                        <b>{row['Order_ID']}</b> | {row['Brand']} | {row['Customer']}
                    </div>""", unsafe_allow_html=True)
                    
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        if st.button("✅ Bildirildi İşaretle", key=f"ops_ntf_{idx}"):
                            mask = df['Order_ID'] == row['Order_ID']
                            df.loc[mask, 'WhatsApp_Sent'] = 'YES'
                            df.loc[mask, 'Status'] = 'Notified'
                            update_db(CSV_DISPATCH, df)
                            log_action("BİLDİRİM", "Admin", f"{row['Order_ID']} bildirildi")
                            st.rerun()
                    with c2:
                        phone = BRAND_CONTRACTS[row['Brand']]['phone']
                        msg = f"YENİ SİPARİŞ: {row['Order_ID']}\n{row['Items']}\n{row['Customer']}\nAdres: {row['Address']}"
                        link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                        st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><button style="background:#25D366 !important; border:none; color:white; padding:8px 16px; border-radius:4px;">📲 WhatsApp Mesajı Oluştur</button></a>', unsafe_allow_html=True)
        else:
            st.success("Tüm bildirimler tamamlandı.")
            
        st.markdown("---")
        
        # B. Manual Tracking Entry (NEW)
        st.markdown("#### 📦 Manuel Kargo Girişi")
        pending_ship = df[(df['Status'] == 'Notified') & (df['Tracking_Num'].isna() | (df['Tracking_Num'] == ''))]
        
        if not pending_ship.empty:
            for idx, row in pending_ship.iterrows():
                with st.expander(f"⏳ {row['Order_ID']} - {row['Brand']} (Kargo Bekliyor)"):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        track_input = st.text_input("Takip Numarası", key=f"manual_track_{idx}")
                    with c2:
                        if st.button("Kaydet ve Kargola", key=f"manual_ship_{idx}"):
                            if track_input:
                                mask = df['Order_ID'] == row['Order_ID']
                                df.loc[mask, 'Tracking_Num'] = track_input
                                df.loc[mask, 'Status'] = 'Dispatched'
                                update_db(CSV_DISPATCH, df)
                                log_action("KARGO", "Admin", f"{row['Order_ID']} kargolandı: {track_input}")
                                st.success("Kargo güncellendi!")
                                st.rerun()
                            else:
                                st.error("Takip no giriniz.")
        else:
            st.info("Kargo bekleyen sipariş yok.")

    # --- 4. FATURA & ÖDEME (General) ---
    with tabs[3]:
        st.markdown("### 🏦 Genel Finansal Durum")
        fin_df = get_db(CSV_FINANCE)
        
        if not fin_df.empty:
            # Breakdown per Brand
            st.markdown("#### Marka Bazlı Ödenecek Toplamlar")
            unpaid_breakdown = fin_df[fin_df['Payment_Status'] == 'Unpaid'].groupby('Brand')['Payable_To_Brand'].sum()
            
            if not unpaid_breakdown.empty:
                cols = st.columns(len(unpaid_breakdown))
                for i, (brand, amount) in enumerate(unpaid_breakdown.items()):
                    with cols[i]:
                        st.metric(f"{brand} Ödenecek", f"{amount:,.0f} TL")
            else:
                st.success("Tüm ödemeler yapılmış.")
        else:
            st.info("Finansal veri yok.")

    # --- 5. MARKA ÖDEMELERİ (Payouts) ---
    with tabs[4]:
        st.markdown("### 💵 Marka Ödeme Yönetimi (Vendor Payouts)")
        c_pay_L, c_pay_R = st.columns([1, 2])
        
        with c_pay_L:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            p_brand = st.selectbox("Marka Seçiniz", list(BRAND_CONTRACTS.keys()), key="payout_brand_select")
            
            # Calc Balance
            fin_df = get_db(CSV_FINANCE)
            
            # Sum of Payables for this brand where status is Unpaid
            brand_unpaid_df = fin_df[(fin_df['Brand'] == p_brand) & (fin_df['Payment_Status'] == 'Unpaid')]
            balance = brand_unpaid_df['Payable_To_Brand'].sum()
            
            st.metric("Ödenmesi Gereken Bakiye", f"{balance:,.2f} TL")
            st.caption(f"IBAN: {BRAND_CONTRACTS[p_brand]['iban']}")
            st.caption(f"Alıcı: {BRAND_CONTRACTS[p_brand]['bank_name']}")
            
            # Copyable Bank Explanation
            bank_exp = f"NATUVISIO ODEME {p_brand} {datetime.now().strftime('%m/%Y')}"
            st.code(bank_exp, language="text")
            st.caption("Açıklama kısmına yukarıdaki kodu yapıştırınız.")
            
            if st.button("✅ Ödemeyi Onayla (Bakiyeyi Sıfırla)", key="confirm_payout_btn"):
                if balance > 0:
                    pid = f"PAY-{datetime.now().strftime('%m%d%H%M')}"
                    pay_df = get_db(CSV_PAYOUTS)
                    save_db(CSV_PAYOUTS, pay_df, {
                        "Payout_ID": pid, "Time": datetime.now(), "Brand": p_brand,
                        "Amount": balance, "Method": "Bank", "Notes": bank_exp, "Reference": "Admin"
                    })
                    
                    # Update Ledger Status to Paid
                    for idx in brand_unpaid_df.index:
                        fin_df.at[idx, 'Payment_Status'] = 'Paid'
                    update_db(CSV_FINANCE, fin_df)
                    
                    log_action("ÖDEME", "Admin", f"{p_brand} ödemesi yapıldı: {balance} TL")
                    st.balloons()
                    st.success("Ödeme Başarıyla Kaydedildi!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.info("Ödenecek bakiye bulunmuyor.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_pay_R:
            st.markdown("#### Ödeme Geçmişi")
            pay_hist = get_db(CSV_PAYOUTS)
            if not pay_hist.empty:
                st.dataframe(pay_hist[pay_hist['Brand'] == p_brand], use_container_width=True)

    # --- 6. MARKA FATURALANDIRMA (Invoicing) ---
    with tabs[5]:
        st.markdown("### 🧾 Komisyon Faturalandırma")
        fin_df = get_db(CSV_FINANCE)
        inv_df = get_db(CSV_INVOICES)
        
        # Identify uninvoiced orders (Invoice_Ref is empty)
        pending_inv = fin_df[fin_df['Invoice_Ref'].isna() | (fin_df['Invoice_Ref'] == "")]
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("#### Faturalandırılmamış İşlemler")
            if not pending_inv.empty:
                st.dataframe(pending_inv[['Order_ID', 'Brand', 'Commission_Amt', 'KDV_Amt', 'Total_Deduction']], use_container_width=True)
            else:
                st.info("Faturalandırılacak işlem yok.")
                
        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            t_brand = st.selectbox("Fatura Kesilecek Marka", list(BRAND_CONTRACTS.keys()), key="invoice_brand_select")
            
            # Filter pending items for selected brand
            items = pending_inv[pending_inv['Brand'] == t_brand]
            
            if not items.empty:
                comm_sum = items['Commission_Amt'].sum()
                kdv_sum = items['KDV_Amt'].sum()
                total_invoice = comm_sum + kdv_sum
                
                st.write(f"**Komisyon Toplam:** {comm_sum:,.2f} TL")
                st.write(f"**KDV (%20):** {kdv_sum:,.2f} TL")
                st.markdown(f"### Toplam Fatura: {total_invoice:,.2f} TL")
                
                # Copyable Explanation
                inv_desc = f"Hizmet Bedeli - {t_brand} - {datetime.now().strftime('%B %Y')}"
                st.code(inv_desc, language="text")
                
                if st.button("✅ Faturayı Kestim / Gönderdim", key="invoice_sent_btn"):
                    ref = f"INV-{datetime.now().strftime('%Y%m')}-{t_brand[:3]}"
                    
                    save_db(CSV_INVOICES, inv_df, {
                        "Invoice_Ref": ref, "Date": datetime.now().date(), "Brand": t_brand,
                        "Total_Commission": comm_sum, "Total_KDV": kdv_sum, "Total_Invoice_Amt": total_invoice,
                        "Order_Count": len(items), "Sent_Status": "Sent", "Paid_Status": "Unpaid", "Notes": inv_desc
                    })
                    
                    # Update finance ledger with Invoice Ref
                    for idx in items.index:
                        fin_df.at[idx, 'Invoice_Ref'] = ref
                    update_db(CSV_FINANCE, fin_df)
                    
                    log_action("FATURA", "Admin", f"{ref} faturası kesildi")
                    st.success(f"Fatura {ref} sisteme işlendi!")
                    time.sleep(2)
                    st.rerun()
            else:
                st.warning("Bu marka için bekleyen işlem yok.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("#### Fatura Kayıtları (Sent Invoices)")
        st.dataframe(get_db(CSV_INVOICES), use_container_width=True)

    # --- 7. TÜM SİPARİŞLER (Archive) ---
    with tabs[6]:
        st.markdown("### 📦 Tüm Sipariş Arşivi")
        st.dataframe(get_db(CSV_DISPATCH).sort_values("Time", ascending=False), use_container_width=True)

    # --- 8. ANALİTİKLER (Detailed) ---
    with tabs[7]:
        st.markdown("### 📊 Detaylı Analitik")
        df = get_db(CSV_DISPATCH)
        fin = get_db(CSV_FINANCE)
        
        if not df.empty:
            t1, t2, t3, t4 = st.tabs(["MARKA", "TÜMÜ", "ÜRÜNLER", "KOMİSYON"])
            
            with t1:
                fig = px.pie(df, names='Brand', values='Total_Value', hole=0.5, color_discrete_sequence=['#4ECDC4', '#FF6B6B', '#95E1D3'])
                st.plotly_chart(fig, use_container_width=True)
            with t2:
                # Group by date for line chart
                df['Date'] = pd.to_datetime(df['Time']).dt.date
                daily_sales = df.groupby('Date')['Total_Value'].sum().reset_index()
                st.line_chart(daily_sales.set_index('Date'))
            with t3:
                st.info("Ürün bazlı detaylar için veritabanı genişletiliyor...")
            with t4:
                st.bar_chart(fin.groupby('Brand')['Commission_Amt'].sum())
        else:
            st.info("Veri yok.")

    # --- 9. REHBER (SOP) ---
    with tabs[8]:
        st.markdown("### ❔ Operasyon Rehberi (SOP)")
        with st.expander("1. Sipariş Nasıl Girilir?", expanded=True):
            st.write("1. 'YENİ SEVKİYAT' sekmesine gidin.\n2. Müşteri bilgilerini girin.\n3. Sepete ürünleri ekleyin.\n4. 'SİPARİŞİ ONAYLA' butonuna basın.")
        with st.expander("2. Marka Ödemesi Nasıl Yapılır?"):
            st.write("1. 'MARKA ÖDEMELERİ' sekmesine gidin.\n2. Bakiyeyi kontrol edin.\n3. Banka açıklamasını kopyalayıp transferi yapın.\n4. Tutarı sisteme girip kaydedin.")
        with st.expander("3. Komisyon Faturası Ne Zaman Kesilir?"):
            st.write("Her ayın sonunda 'MARKA FATURALANDIRMA' sekmesinden toplu fatura oluşturun.")

    # --- 10. LOGLAR ---
    with tabs[9]:
        st.markdown("### 📜 Sistem Logları")
        st.dataframe(get_db(CSV_LOGS).sort_values("Time", ascending=False), use_container_width=True)

    # --- 11. EXPORT ---
    with tabs[10]:
        st.markdown("### 📥 Veri Dışa Aktar")
        c1, c2, c3, c4 = st.columns(4)
        
        def convert_df(df): return df.to_csv(index=False).encode('utf-8')
        
        with c1:
            st.download_button("Siparişleri İndir", convert_df(get_db(CSV_DISPATCH)), "orders.csv", "text/csv")
        with c2:
            st.download_button("Finansal Kayıtları İndir", convert_df(get_db(CSV_FINANCE)), "finance.csv", "text/csv")
        with c3:
            st.download_button("Ödemeleri İndir", convert_df(get_db(CSV_PAYOUTS)), "payouts.csv", "text/csv")
        with c4:
            st.download_button("Faturaları İndir", convert_df(get_db(CSV_INVOICES)), "invoices.csv", "text/csv")
            
    render_footer()

# ============================================================================
# 7. PARTNER DASHBOARD (Simplified View)
# ============================================================================

def partner_dashboard():
    load_css()
    init_databases()
    brand = st.session_state.logged_brand
    
    # Header
    c1, c2 = st.columns([6,1])
    with c1: st.markdown(f"## 📦 {brand} PORTAL")
    with c2: 
        if st.button("Çıkış", key="partner_logout"):
            st.session_state.is_partner_logged_in = False
            st.rerun()
    st.markdown("---")
    
    # Logic similar to Admin but filtered for Brand
    df = get_db(CSV_DISPATCH)
    brand_df = df[df['Brand'] == brand]
    
    tabs = st.tabs(["📋 BEKLEYENLER", "✅ GEÇMİŞ", "💰 HESAP DURUMU"])
    
    with tabs[0]:
        pending = brand_df[brand_df['Status'].isin(['Order Received', 'Pending', 'Notified'])]
        if not pending.empty:
            for idx, row in pending.iterrows():
                with st.expander(f"🔔 {row['Order_ID']} | {row['Customer']}", expanded=True):
                    st.write(row['Items'])
                    st.write(f"Adres: {row['Address']}")
                    track = st.text_input("Takip No", key=f"p_trk_{idx}")
                    if st.button("Kargola", key=f"p_shp_{idx}"):
                        mask = df['Order_ID'] == row['Order_ID']
                        df.loc[mask, 'Tracking_Num'] = track
                        df.loc[mask, 'Status'] = 'Dispatched'
                        update_db(CSV_DISPATCH, df)
                        st.success("Güncellendi")
                        st.rerun()
        else:
            st.info("Bekleyen sipariş yok.")
            
    with tabs[2]:
        st.info("Finansal detaylar için yönetici ile iletişime geçiniz.")
    
    render_footer()

# ============================================================================
# 8. EXECUTION ROUTER
# ============================================================================

if __name__ == "__main__":
    if st.session_state.admin_logged_in:
        admin_dashboard()
    elif st.session_state.is_partner_logged_in:
        partner_dashboard()
    else:
        login_view()
