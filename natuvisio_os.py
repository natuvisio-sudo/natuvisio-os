import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime, timedelta
import urllib.parse
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# 🏔️ NATUVISIO OPERATING SYSTEM - V13.0 (TIER 1 PREMIER EDITION)
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Bridge OS",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 1. CORE CONFIGURATION & ASSETS
# ============================================================================

# --- CREDENTIALS ---
ADMIN_PASS = "admin2025"
BRAND_CREDENTIALS = {
    "HAKI HEAL": "haki123",
    "AURORACO": "aurora2025",
    "LONGEVICALS": "longsci"
}

# --- FILES ---
CSV_DISPATCH = "dispatch_history.csv"
CSV_FINANCE = "financial_ledger.csv"
CSV_INVOICES = "invoice_registry.csv"
CSV_PAYOUTS = "payout_history.csv"
CSV_LOGS = "system_logs.csv"

# --- THEME CONSTANTS ---
THEME = {
    "primary": "#4ECDC4",
    "secondary": "#2f855a",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "glass_bg": "rgba(255, 255, 255, 0.75)",
    "glass_border": "rgba(255, 255, 255, 0.4)"
}

BG_IMAGE = "https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp"
LOGO_URL = "https://res.cloudinary.com/deb1j92hy/image/upload/f_auto,q_auto/v1764805291/natuvisio_logo_gtqtfs.png"

# --- BUSINESS LOGIC ---
KDV_RATE = 0.20
BRAND_CONTRACTS = {
    "HAKI HEAL": {"commission": 0.15, "phone": "601158976276", "color": "#4ECDC4", "iban": "TR90 0006 1000..."},
    "AURORACO": {"commission": 0.20, "phone": "601158976276", "color": "#FF6B6B", "iban": "TR90 0006 2000..."},
    "LONGEVICALS": {"commission": 0.12, "phone": "601158976276", "color": "#95E1D3", "iban": "TR90 0001 5000..."}
}
PRODUCT_DB = {
    "HAKI HEAL": {"HAKI HEAL KREM": {"sku": "SKU-HAKI-CRM", "price": 450}, "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP", "price": 120}},
    "AURORACO": {"AURORACO MATCHA": {"sku": "SKU-AUR-MATCHA", "price": 650}, "AURORACO CACAO": {"sku": "SKU-AUR-CACAO", "price": 550}},
    "LONGEVICALS": {"LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200}, "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}}
}

# ============================================================================
# 2. ROBUST DATABASE ENGINE
# ============================================================================

def init_databases():
    """Guarantees database integrity on startup"""
    schemas = {
        CSV_DISPATCH: ["Order_ID", "Time", "Brand", "Customer", "Phone", "Address", "Items", "Total_Value", "Status", "Tracking_Num", "WhatsApp_Sent", "Notes", "Priority"],
        CSV_FINANCE: ["Order_ID", "Time", "Brand", "Total_Sale", "Commission_Rate", "Commission_Amt", "KDV_Amt", "Total_Deduction", "Payable_To_Brand", "Invoice_Ref", "Payment_Status"],
        CSV_INVOICES: ["Invoice_Ref", "Date", "Brand", "Total_Commission", "KDV", "Total_Due", "Sent_Status", "Paid_Status", "Notes"],
        CSV_PAYOUTS: ["Payout_ID", "Time", "Brand", "Amount", "Method", "Reference", "Notes"],
        CSV_LOGS: ["Log_ID", "Time", "Action", "User", "Details"]
    }
    for file, cols in schemas.items():
        if not os.path.exists(file):
            pd.DataFrame(columns=cols).to_csv(file, index=False)

def get_db(file):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame()

def save_db(file, df, new_row=None):
    """Atomic save operation"""
    if new_row is not None:
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(file, index=False)
    return df

def update_db(file, df):
    df.to_csv(file, index=False)

def log_action(action, user, details):
    """Audit Trail Recorder"""
    df = get_db(CSV_LOGS)
    new_log = {
        "Log_ID": f"LOG-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Action": action, "User": user, "Details": details
    }
    save_db(CSV_LOGS, df, new_log)

# ============================================================================
# 3. PREMIUM UI SYSTEM (CSS)
# ============================================================================

def load_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

        /* === GLOBAL THEME === */
        .stApp {{
            background-image: linear-gradient(rgba(240, 242, 245, 0.95), rgba(240, 242, 245, 0.98)), url("{BG_IMAGE}");
            background-attachment: fixed;
            background-size: cover;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #1e293b;
        }}

        /* === SIDEBAR === */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.9);
            border-right: 1px solid rgba(0,0,0,0.05);
            backdrop-filter: blur(10px);
        }}

        /* === GLASS CARDS === */
        .glass-card {{
            background: {THEME['glass_bg']};
            backdrop-filter: blur(12px);
            border: 1px solid {THEME['glass_border']};
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            margin-bottom: 20px;
            transition: transform 0.2s ease;
        }}
        .glass-card:hover {{ transform: translateY(-2px); }}

        /* === METRICS === */
        .metric-card {{
            text-align: center;
            padding: 15px;
            border-radius: 12px;
            background: white;
            border: 1px solid #e2e8f0;
        }}
        .metric-val {{ font-size: 28px; font-weight: 800; color: #0f172a; }}
        .metric-lbl {{ font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }}
        
        /* === ALERTS & BADGES === */
        .status-badge {{
            padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; display: inline-block;
        }}
        .badge-red {{ background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; }}
        .badge-green {{ background: #F0FDF4; color: #166534; border: 1px solid #BBF7D0; }}
        
        /* === BUTTONS & INPUTS === */
        .stButton button {{
            background: linear-gradient(135deg, {THEME['secondary']}, #276749);
            color: white; border-radius: 8px; border: none; font-weight: 600; padding: 0.6rem 1.2rem;
            box-shadow: 0 2px 4px rgba(47, 133, 90, 0.2); transition: all 0.2s;
        }}
        .stButton button:hover {{ box-shadow: 0 4px 8px rgba(47, 133, 90, 0.3); transform: translateY(-1px); }}
        
        .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {{
            background: white; border: 1px solid #e2e8f0; border-radius: 8px; color: #1e293b;
        }}
        
        /* HIDE DEFAULT STREAMLIT CHROME */
        #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 4. STATE MANAGEMENT
# ============================================================================

if 'page' not in st.session_state: st.session_state.page = 'login'
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'logged_brand' not in st.session_state: st.session_state.logged_brand = None
if 'cart' not in st.session_state: st.session_state.cart = []
if 'selected_brand_lock' not in st.session_state: st.session_state.selected_brand_lock = None
if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'is_partner_logged_in' not in st.session_state: st.session_state.is_partner_logged_in = False

# ============================================================================
# 5. VIEW: LOGIN SCREEN
# ============================================================================

def login_view():
    load_css()
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 40px;">
            <div style="font-size: 48px; margin-bottom: 10px;">🌿</div>
            <h2 style="margin: 0; color: #1e293b;">NATUVISIO</h2>
            <p style="color: #64748b; font-size: 13px; font-weight: 500;">BRIDGE OPERATION SYSTEM v13.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        role = st.selectbox("Giriş Modu", ["Yönetici (Admin)", "Partner Marka"], label_visibility="collapsed")
        
        if role == "Partner Marka":
            brand_user = st.selectbox("Marka", list(BRAND_CREDENTIALS.keys()))
        
        pwd = st.text_input("Şifre", type="password")
        
        if st.button("GÜVENLİ GİRİŞ", use_container_width=True):
            if role == "Yönetici (Admin)":
                if pwd == ADMIN_PASS:
                    st.session_state.user_role = 'ADMIN'
                    st.session_state.admin_logged_in = True
                    st.session_state.page = 'admin_dashboard'
                    st.rerun()
                else:
                    st.error("Erişim Reddedildi")
            
            elif role == "Partner Marka":
                if pwd == BRAND_CREDENTIALS.get(brand_user):
                    st.session_state.user_role = 'PARTNER'
                    st.session_state.logged_brand = brand_user
                    st.session_state.is_partner_logged_in = True
                    st.session_state.page = 'partner_dashboard'
                    st.rerun()
                else:
                    st.error("Hatalı Şifre")
                    
    # Secure Footer
    st.markdown("""
    <div style="text-align:center; margin-top:50px; color:#94a3b8; font-size:11px;">
        🔒 NATUVISIO INTERNAL SYSTEM • AUTHORIZED ACCESS ONLY
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# 6. VIEW: ADMIN DASHBOARD (SUPERCHARGED)
# ============================================================================

def admin_dashboard():
    load_css()
    init_databases()
    
    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.image(LOGO_URL, width=40)
        st.markdown("### NATUVISIO HQ")
        st.markdown(f"**Operator:** Master Admin")
        st.markdown("---")
        
        menu = st.radio(
            "MENÜ",
            ["Genel Bakış", "Yeni Sevkiyat", "Operasyon", "Finansallar", "Veri Merkezi"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🔴 ÇIKIŞ YAP"):
            st.session_state.admin_logged_in = False
            st.rerun()

    # --- HEADER ---
    c1, c2 = st.columns([8, 2])
    with c1: st.title(f"🚀 {menu}")
    with c2: st.caption(f"Last Sync: {datetime.now().strftime('%H:%M')}")

    df_disp = get_db(CSV_DISPATCH)
    df_fin = get_db(CSV_FINANCE)

    # ========================================================================
    # MODULE: GENEL BAKIŞ (DASHBOARD)
    # ========================================================================
    if menu == "Genel Bakış":
        # 1. Top Metrics (Bento Box)
        total_rev = df_fin['Total_Sale'].sum() if not df_fin.empty else 0
        total_comm = df_fin['Commission_Amt'].sum() if not df_fin.empty else 0
        pending_ops = len(df_disp[df_disp['Status'] == 'Pending']) if not df_disp.empty else 0
        
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f"<div class='metric-card'><div class='metric-val'>{len(df_disp)}</div><div class='metric-lbl'>Toplam Sipariş</div></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='metric-card'><div class='metric-val'>{total_rev:,.0f}₺</div><div class='metric-lbl'>Toplam Hacim</div></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#2f855a;'>{total_comm:,.0f}₺</div><div class='metric-lbl'>Net Komisyon</div></div>", unsafe_allow_html=True)
        with m4: st.markdown(f"<div class='metric-card'><div class='metric-val' style='color:#EF4444;'>{pending_ops}</div><div class='metric-lbl'>Bekleyen</div></div>", unsafe_allow_html=True)
        
        st.markdown("### 📊 Marka Performansı")
        if not df_fin.empty:
            brand_stats = df_fin.groupby('Brand')['Total_Sale'].sum().reset_index()
            fig = px.bar(brand_stats, x='Brand', y='Total_Sale', color='Brand', title="Satış Dağılımı", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
            # Live Status Table
            st.markdown("### 🔭 Canlı Sipariş Akışı")
            st.dataframe(
                df_disp[['Order_ID', 'Time', 'Brand', 'Status', 'Total_Value']].sort_values('Time', ascending=False).head(10),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Status": st.column_config.Column("Durum", width="medium"),
                    "Total_Value": st.column_config.NumberColumn("Tutar", format="%d ₺")
                }
            )

    # ========================================================================
    # MODULE: YENİ SEVKİYAT (DISPATCH)
    # ========================================================================
    elif menu == "Yeni Sevkiyat":
        c_form, c_cart = st.columns([1.5, 1])
        
        with c_form:
            st.markdown('<div class="glass-card"><h4>📝 1. Sipariş Detayları</h4>', unsafe_allow_html=True)
            cust_name = st.text_input("Müşteri Adı Soyadı")
            cust_phone = st.text_input("Telefon (905...)")
            cust_addr = st.text_area("Adres", height=80)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="glass-card"><h4>🛒 2. Ürün Ekle</h4>', unsafe_allow_html=True)
            if st.session_state.cart:
                act_brand = st.session_state.cart[0]['Brand']
                st.info(f"🔒 Kilitli Marka: {act_brand}")
            else:
                act_brand = st.selectbox("Marka Seçiniz", list(BRAND_CONTRACTS.keys()))
            
            c_p, c_q = st.columns([3, 1])
            with c_p: prod = st.selectbox("Ürün", list(PRODUCT_DB[act_brand].keys()))
            with c_q: qty = st.number_input("Adet", 1, value=1)
            
            if st.button("➕ Sepete Ekle", use_container_width=True):
                p_data = PRODUCT_DB[act_brand][prod]
                rate = BRAND_CONTRACTS[act_brand]["commission"]
                tot = p_data['price'] * qty
                comm = tot * rate
                kdv = comm * KDV_RATE
                pay = tot - (comm + kdv)
                
                st.session_state.cart.append({
                    "Brand": act_brand, "Product": prod, "Qty": qty,
                    "Total": tot, "Comm": comm, "KDV": kdv, "Payable": pay
                })
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with c_cart:
            st.markdown('<div class="glass-card"><h4>📦 3. Sepet Özeti</h4>', unsafe_allow_html=True)
            if st.session_state.cart:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.dataframe(cart_df[["Product", "Qty", "Total"]], hide_index=True)
                
                total_val = cart_df['Total'].sum()
                st.markdown(f"<h3 style='text-align:right; color:#2f855a;'>{total_val:,.0f} TL</h3>", unsafe_allow_html=True)
                
                if st.button("⚡ SİPARİŞİ ONAYLA", type="primary", use_container_width=True):
                    if cust_name and cust_phone:
                        oid = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
                        items = ", ".join([f"{x['Product']} (x{x['Qty']})" for x in st.session_state.cart])
                        
                        # Log Physical
                        d_df = get_db(CSV_DISPATCH)
                        save_db(CSV_DISPATCH, d_df, {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": act_brand,
                            "Customer": cust_name, "Phone": cust_phone, "Address": cust_addr,
                            "Items": items, "Total_Value": total_val, "Status": "Pending", 
                            "WhatsApp_Sent": "NO", "Tracking_Num": ""
                        })
                        
                        # Log Financial
                        f_df = get_db(CSV_FINANCE)
                        save_db(CSV_FINANCE, f_df, {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": act_brand,
                            "Total_Sale": total_val, "Commission_Rate": BRAND_CONTRACTS[act_brand]['commission'],
                            "Commission_Amt": cart_df['Comm'].sum(), "KDV_Amt": cart_df['KDV'].sum(),
                            "Payable_To_Brand": cart_df['Payable'].sum(), "Invoice_Ref": "", "Payment_Status": "Unpaid"
                        })
                        
                        log_action("SİPARİŞ", "Admin", f"{oid} oluşturuldu")
                        st.success(f"✅ {oid} Başarıyla Oluşturuldu!")
                        st.session_state.cart = []
                        st.rerun()
                    else:
                        st.error("Müşteri bilgileri eksik!")
                
                if st.button("Temizle", use_container_width=True):
                    st.session_state.cart = []
                    st.rerun()
            else:
                st.info("Sepet boş")
            st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================================
    # MODULE: OPERASYON (OPERATIONS)
    # ========================================================================
    elif menu == "Operasyon":
        st.markdown("### ⚠️ Bekleyen Bildirimler")
        pending = df_disp[df_disp['WhatsApp_Sent'] == 'NO'].sort_values("Time", ascending=False)
        
        if not pending.empty:
            for idx, row in pending.iterrows():
                with st.expander(f"🔴 {row['Order_ID']} | {row['Brand']} | {row['Customer']}", expanded=True):
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        if st.button("✅ Bildirildi Olarak İşaretle", key=f"op_{idx}"):
                            # Update DB directly using mask to avoid index issues
                            df_disp.loc[df_disp['Order_ID'] == row['Order_ID'], 'WhatsApp_Sent'] = 'YES'
                            df_disp.loc[df_disp['Order_ID'] == row['Order_ID'], 'Status'] = 'Notified'
                            update_db(CSV_DISPATCH, df_disp)
                            st.rerun()
                    with c2:
                        phone = BRAND_CONTRACTS[row['Brand']]['phone']
                        msg = f"SİPARİŞ: {row['Order_ID']}\n{row['Items']}\n{row['Customer']}\n{row['Address']}"
                        link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                        st.markdown(f'<a href="{link}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:8px 16px; border-radius:6px;">📲 WhatsApp Mesajı Gönder</button></a>', unsafe_allow_html=True)
        else:
            st.success("Tüm bildirimler tamamlandı.")
            
        st.markdown("---")
        st.markdown("### 📦 Kargo Girişi (Manuel)")
        wait_ship = df_disp[(df_disp['Status'] == 'Notified') & (df_disp['Tracking_Num'].isna())]
        
        if not wait_ship.empty:
            for idx, row in wait_ship.iterrows():
                with st.container():
                    c1, c2, c3 = st.columns([2, 3, 1])
                    c1.write(f"**{row['Order_ID']}**")
                    track_in = c2.text_input("Takip No", key=f"trk_in_{idx}", label_visibility="collapsed", placeholder="Takip No Giriniz")
                    if c3.button("Kaydet", key=f"save_{idx}"):
                        if track_in:
                            df_disp.loc[df_disp['Order_ID'] == row['Order_ID'], 'Tracking_Num'] = track_in
                            df_disp.loc[df_disp['Order_ID'] == row['Order_ID'], 'Status'] = 'Dispatched'
                            update_db(CSV_DISPATCH, df_disp)
                            st.success("Kargolandı!")
                            st.rerun()

    # ========================================================================
    # MODULE: FİNANSALLAR (FINANCE)
    # ========================================================================
    elif menu == "Finansallar":
        tabs_fin = st.tabs(["💰 Marka Ödemeleri", "🧾 Fatura Yönetimi", "💵 Genel Bakiye"])
        
        # 1. PAYOUTS
        with tabs_fin[0]:
            c_L, c_R = st.columns([1, 2])
            with c_L:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                p_brand = st.selectbox("Marka Seçiniz", list(BRAND_CONTRACTS.keys()))
                
                # Calc logic
                sales = df_fin[df_fin['Brand'] == p_brand]['Payable_To_Brand'].sum()
                df_pay = get_db(CSV_PAYOUTS)
                paid = df_pay[df_pay['Brand'] == p_brand]['Amount'].sum() if not df_pay.empty else 0
                balance = sales - paid
                
                st.metric("Ödenecek Bakiye", f"{balance:,.2f} TL")
                st.caption(f"IBAN: {BRAND_CONTRACTS[p_brand]['iban']}")
                
                amt = st.number_input("Ödeme Tutarı", 0.0, float(balance) if balance > 0 else 0.0)
                desc = f"NATUVISIO ODEME {p_brand} {datetime.now().strftime('%m/%y')}"
                st.code(desc, language="text")
                
                if st.button("✅ Ödemeyi Kaydet"):
                    if amt > 0:
                        pid = f"PAY-{datetime.now().strftime('%m%d%H%M')}"
                        save_db(CSV_PAYOUTS, df_pay, {
                            "Payout_ID": pid, "Time": datetime.now(), "Brand": p_brand,
                            "Amount": amt, "Method": "Bank", "Reference": "Admin", "Notes": desc
                        })
                        log_action("ÖDEME", "Admin", f"{p_brand} - {amt} TL")
                        st.success("Ödeme Kaydedildi!")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with c_R:
                st.markdown("#### Ödeme Geçmişi")
                if not df_pay.empty:
                    st.dataframe(df_pay[df_pay['Brand'] == p_brand], use_container_width=True)

        # 2. INVOICING
        with tabs_fin[1]:
            col_inv, col_reg = st.columns([1, 2])
            with col_inv:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                t_brand = st.selectbox("Fatura Kesilecek Marka", list(BRAND_CONTRACTS.keys()), key="inv_brand")
                
                # Find uninvoiced items
                uninvoiced = df_fin[(df_fin['Brand'] == t_brand) & (df_fin['Invoice_Ref'].isna() | (df_fin['Invoice_Ref'] == ""))]
                
                if not uninvoiced.empty:
                    comm_tot = uninvoiced['Commission_Amt'].sum()
                    kdv_tot = uninvoiced['KDV_Amt'].sum()
                    total_inv = comm_tot + kdv_tot
                    
                    st.write(f"**Komisyon:** {comm_tot:,.2f} TL")
                    st.write(f"**KDV (%20):** {kdv_tot:,.2f} TL")
                    st.markdown(f"### Toplam: {total_inv:,.2f} TL")
                    
                    if st.button("Faturayı Oluştur"):
                        ref = f"INV-{datetime.now().strftime('%Y%m')}-{t_brand[:3]}"
                        df_inv = get_db(CSV_INVOICES)
                        save_db(CSV_INVOICES, df_inv, {
                            "Invoice_Ref": ref, "Date": datetime.now(), "Brand": t_brand,
                            "Total_Commission": comm_tot, "KDV": kdv_tot, "Total_Due": total_inv,
                            "Sent_Status": "Pending", "Paid_Status": "Unpaid"
                        })
                        
                        # Update ledger
                        for idx in uninvoiced.index:
                            df_fin.at[idx, 'Invoice_Ref'] = ref
                        update_db(CSV_FINANCE, df_fin)
                        st.success(f"{ref} Oluşturuldu!")
                        st.rerun()
                else:
                    st.info("Faturalanacak işlem yok.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_reg:
                st.markdown("#### Fatura Kayıtları")
                st.dataframe(get_db(CSV_INVOICES), use_container_width=True)

    # ========================================================================
    # MODULE: VERİ MERKEZİ (EXPORT & LOGS)
    # ========================================================================
    elif menu == "Veri Merkezi":
        t1, t2 = st.tabs(["📜 Sistem Logları", "📥 Export Center"])
        
        with t1:
            st.dataframe(get_db(CSV_LOGS).sort_values("Time", ascending=False), use_container_width=True)
            
        with t2:
            st.markdown("### Veri Dışa Aktar")
            c1, c2, c3, c4 = st.columns(4)
            def convert_df(df): return df.to_csv(index=False).encode('utf-8')
            
            with c1: st.download_button("Siparişler", convert_df(get_db(CSV_DISPATCH)), "orders.csv")
            with c2: st.download_button("Finansal Defter", convert_df(get_db(CSV_FINANCE)), "finance.csv")
            with c3: st.download_button("Ödemeler", convert_df(get_db(CSV_PAYOUTS)), "payouts.csv")
            with c4: st.download_button("Faturalar", convert_df(get_db(CSV_INVOICES)), "invoices.csv")

# ============================================================================
# 7. PARTNER DASHBOARD (Simplified)
# ============================================================================

def partner_dashboard():
    load_css()
    init_databases()
    brand = st.session_state.logged_brand
    
    st.markdown(f"## 📦 {brand} PORTAL")
    if st.button("Çıkış Yap"):
        st.session_state.is_partner_logged_in = False
        st.rerun()
    st.markdown("---")
    
    tabs = st.tabs(["📋 Bekleyenler", "✅ Geçmiş", "💰 Finans"])
    
    df = get_db(CSV_DISPATCH)
    brand_df = df[df['Brand'] == brand]
    
    with tabs[0]:
        pending = brand_df[brand_df['Status'].isin(['Pending', 'Notified'])]
        if not pending.empty:
            for idx, row in pending.iterrows():
                with st.expander(f"🔔 {row['Order_ID']} | {row['Customer']}", expanded=True):
                    st.write(row['Items'])
                    st.write(f"**Adres:** {row['Address']}")
                    
                    track = st.text_input("Kargo Takip No", key=f"p_trk_{idx}")
                    if st.button("Kargola", key=f"p_shp_{idx}"):
                        # Find original index
                        orig_idx = df[df['Order_ID'] == row['Order_ID']].index[0]
                        df.at[orig_idx, 'Tracking_Num'] = track
                        df.at[orig_idx, 'Status'] = 'Dispatched'
                        update_db(CSV_DISPATCH, df)
                        st.success("Güncellendi!")
                        st.rerun()
        else:
            st.info("Bekleyen sipariş yok.")

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
