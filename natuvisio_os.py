import streamlit as st
import pandas as pd
import os
import io
import time
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO ADMIN OS - V8.0 (ENTERPRISE EDITION)
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
    # Dispatch: Physical movement
    if not os.path.exists(CSV_DISPATCH):
        pd.DataFrame(columns=[
            "Order_ID", "Time", "Brand", "Customer", "Phone", "Address",
            "Items", "Total_Value", "Status", "Tracking_Num", "WhatsApp_Sent", 
            "Notes", "Priority"
        ]).to_csv(CSV_DISPATCH, index=False)
    
    # Finance: Transaction split per order
    if not os.path.exists(CSV_FINANCE):
        pd.DataFrame(columns=[
            "Order_ID", "Time", "Brand", "Total_Sale", "Commission_Rate",
            "Commission_Amt", "Payable_To_Brand", "Invoice_Ref", "Payment_Status"
        ]).to_csv(CSV_FINANCE, index=False)

    # Invoices: Official Commission Invoices
    if not os.path.exists(CSV_INVOICES):
        pd.DataFrame(columns=[
            "Invoice_Ref", "Date", "Brand", "Total_Commission", "KDV", 
            "Total_Due", "Sent_Status", "Paid_Status"
        ]).to_csv(CSV_INVOICES, index=False)

    # Payouts: Bank Transfers to Brands
    if not os.path.exists(CSV_PAYOUTS):
        pd.DataFrame(columns=[
            "Payout_ID", "Time", "Brand", "Amount", "Method", 
            "Reference", "Notes"
        ]).to_csv(CSV_PAYOUTS, index=False)

    # Logs: Audit Trail
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
    # Simplified icons for UI
    icons = {
        "mountain": "🏔️", "alert": "⚠️", "check": "✅", "bill": "🧾",
        "money": "💰", "clock": "⏳", "truck": "🚚"
    }
    return icons.get(name, "📦")

# ============================================================================
# 3. PREMIUM DESIGN SYSTEM (CSS)
# ============================================================================

def load_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=Inter:wght@300;400;600&display=swap');

        /* RESET & BACKGROUND */
        .stApp {{
            background-image: linear-gradient(rgba(240, 242, 240, 0.95), rgba(240, 242, 240, 0.98)), 
                              url("{BG_IMAGE}");
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #1a202c;
        }}

        /* GLASS CONTAINERS - CLEAR VIEW PALETTE */
        .glass-card {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            margin-bottom: 20px;
        }}

        /* TYPOGRAPHY */
        h1, h2, h3, h4 {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: #2d3748 !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }}
        
        /* METRIC CARDS */
        .metric-container {{
            text-align: center;
            padding: 10px;
        }}
        .metric-value {{
            font-family: 'Space Grotesk';
            font-size: 28px;
            font-weight: 700;
            color: #2f855a;
        }}
        .metric-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #718096;
            font-weight: 600;
        }}

        /* BUTTONS */
        div.stButton > button {{
            background: #2f855a !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 5px rgba(47, 133, 90, 0.2) !important;
        }}
        div.stButton > button:hover {{
            background: #276749 !important;
            transform: translateY(-1px);
        }}

        /* INPUTS */
        .stTextInput>div>div>input {{
            background: white !important;
            border: 1px solid #e2e8f0 !important;
            color: #2d3748 !important;
            border-radius: 6px !important;
        }}

        /* TIMELINE */
        .status-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .status-pending {{ background: #FEFCBF; color: #744210; }}
        .status-notified {{ background: #BEE3F8; color: #2C5282; }}
        .status-dispatched {{ background: #C6F6D5; color: #22543D; }}
        .status-completed {{ background: #E9D8FD; color: #553C9A; }}

        #MainMenu, header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 4. ADMIN DASHBOARD
# ============================================================================

def admin_dashboard():
    load_css()
    init_databases()
    
    # Header
    c1, c2 = st.columns([6,1])
    with c1: 
        st.markdown(f"## 🏔️ NATUVISIO ADMIN OS")
        st.markdown("**Role:** Master Operator | **Status:** Online")
    with c2:
        if st.button("🚪 LOGOUT"):
            st.session_state.admin_logged_in = False
            st.rerun()
    st.markdown("---")

    # Metrics Overview
    df_disp = get_db(CSV_DISPATCH)
    df_fin = get_db(CSV_FINANCE)
    
    if not df_disp.empty and not df_fin.empty:
        total_rev = df_fin['Total_Sale'].sum()
        total_comm = df_fin['Commission_Amt'].sum()
        pending_ops = len(df_disp[df_disp['Status'] == 'Pending'])
        
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f"<div class='glass-card metric-container'><div class='metric-value'>{len(df_disp)}</div><div class='metric-label'>TOPLAM SİPARİŞ</div></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='glass-card metric-container'><div class='metric-value'>{total_rev:,.0f}₺</div><div class='metric-label'>TOPLAM CİRO</div></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='glass-card metric-container'><div class='metric-value' style='color:#2f855a;'>{total_comm:,.0f}₺</div><div class='metric-label'>KOMİSYON GELİRİ</div></div>", unsafe_allow_html=True)
        with m4: st.markdown(f"<div class='glass-card metric-container'><div class='metric-value' style='color:#c53030;'>{pending_ops}</div><div class='metric-label'>BEKLEYEN İŞLEM</div></div>", unsafe_allow_html=True)

    # MASTER NAVIGATION
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
            
            cust_name = st.text_input("Müşteri Adı Soyadı")
            cust_phone = st.text_input("Telefon (905...)")
            cust_addr = st.text_area("Adres")
            
            st.markdown("---")
            if st.session_state.cart:
                act_brand = st.session_state.cart[0]['Brand']
                st.info(f"Kilitli Marka: {act_brand}")
            else:
                act_brand = st.selectbox("Marka Seçiniz", list(BRAND_CONTRACTS.keys()))
            
            cp, cq = st.columns([3, 1])
            with cp: prod = st.selectbox("Ürün", list(PRODUCT_DB[act_brand].keys()))
            with cq: qty = st.number_input("Adet", 1, value=1)
            
            if st.button("➕ Sepete Ekle"):
                p_data = PRODUCT_DB[act_brand][prod]
                rate = BRAND_CONTRACTS[act_brand]["commission"]
                tot = p_data['price'] * qty
                comm = tot * rate
                st.session_state.cart.append({
                    "Brand": act_brand, "Product": prod, "Qty": qty, 
                    "Total": tot, "Comm": comm, "Payable": tot - comm
                })
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with c_cart:
            st.markdown('<div class="glass-card"><h4>📦 Sepet Özeti</h4>', unsafe_allow_html=True)
            if st.session_state.cart:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.dataframe(cart_df[["Product", "Qty", "Total"]], hide_index=True)
                
                total_val = cart_df['Total'].sum()
                st.markdown(f"<h3 style='text-align:right'>{total_val:,.0f} TL</h3>", unsafe_allow_html=True)
                
                if st.button("⚡ SİPARİŞİ ONAYLA"):
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
                            "Commission_Amt": cart_df['Comm'].sum(), "Payable_To_Brand": cart_df['Payable'].sum(),
                            "Invoice_Ref": "", "Payment_Status": "Unpaid"
                        })
                        
                        log_action("SİPARİŞ", "Admin", f"Sipariş oluşturuldu: {oid}")
                        st.success("Sipariş başarıyla oluşturuldu!")
                        st.session_state.cart = []
                        st.rerun()
                    else:
                        st.error("Müşteri bilgileri eksik.")
                
                if st.button("Sepeti Temizle"):
                    st.session_state.cart = []
                    st.rerun()
            else:
                st.info("Sepet boş.")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- 2. SİPARİŞ TAKİBİ (Live View) ---
    with tabs[1]:
        st.markdown("### 🔭 Aktif Sipariş Takibi")
        df = get_db(CSV_DISPATCH)
        if not df.empty:
            active_df = df[df['Status'].isin(['Pending', 'Notified', 'Dispatched'])].sort_values("Time", ascending=False)
            st.dataframe(active_df, use_container_width=True)
        else:
            st.info("Aktif sipariş bulunmuyor.")

    # --- 3. OPERASYON (Action Center) ---
    with tabs[2]:
        st.markdown("### ✅ Operasyon Merkezi")
        df = get_db(CSV_DISPATCH)
        pending_ntf = df[df['WhatsApp_Sent'] == 'NO'].sort_values("Time", ascending=False)
        
        if not pending_ntf.empty:
            st.warning(f"⚠️ {len(pending_ntf)} Sipariş Bildirim Bekliyor")
            for idx, row in pending_ntf.iterrows():
                with st.container():
                    st.markdown(f"""<div class='glass-card' style='border-left: 5px solid #e53e3e;'>
                        <b>{row['Order_ID']}</b> | {row['Brand']} | {row['Customer']}
                    </div>""", unsafe_allow_html=True)
                    
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        if st.button("✅ Bildirildi İşaretle", key=f"ntf_{idx}"):
                            # Use boolean indexing to update
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
        st.markdown("#### 📦 Kargo Onayı Bekleyenler")
        pending_ship = df[(df['Status'] == 'Notified') & (df['Tracking_Num'].isna())]
        if not pending_ship.empty:
            st.dataframe(pending_ship[['Order_ID', 'Brand', 'Customer', 'Items']])

    # --- 4. FATURA & ÖDEME (General) ---
    with tabs[3]:
        st.markdown("### 🏦 Genel Finansal Durum")
        fin_df = get_db(CSV_FINANCE)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="glass-card"><h5>Tahsil Edilen (GMV)</h5>', unsafe_allow_html=True)
            st.metric("Toplam Satış", f"{fin_df['Total_Sale'].sum():,.0f} TL")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="glass-card"><h5>Markalara Ödenecek</h5>', unsafe_allow_html=True)
            st.metric("Borç Bakiyesi", f"{fin_df['Payable_To_Brand'].sum():,.0f} TL")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- 5. MARKA ÖDEMELERİ (Payouts) ---
    with tabs[4]:
        st.markdown("### 💵 Marka Ödeme Yönetimi (Vendor Payouts)")
        c_pay_L, c_pay_R = st.columns([1, 2])
        
        with c_pay_L:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            p_brand = st.selectbox("Marka Seçiniz", list(BRAND_CONTRACTS.keys()))
            
            # Calc Balance
            fin_df = get_db(CSV_FINANCE)
            pay_df = get_db(CSV_PAYOUTS)
            
            sales = fin_df[fin_df['Brand'] == p_brand]['Payable_To_Brand'].sum()
            paid = pay_df[pay_df['Brand'] == p_brand]['Amount'].sum()
            balance = sales - paid
            
            st.metric("Ödenmesi Gereken Bakiye", f"{balance:,.2f} TL")
            st.caption(f"IBAN: {BRAND_CONTRACTS[p_brand]['iban']}")
            st.caption(f"Alıcı: {BRAND_CONTRACTS[p_brand]['bank_name']}")
            
            # Copyable Bank Explanation
            bank_exp = f"NATUVISIO ODEME {p_brand} {datetime.now().strftime('%m/%Y')}"
            st.code(bank_exp, language="text")
            
            amt = st.number_input("Ödenecek Tutar", 0.0, float(balance) if balance > 0 else 0.0)
            
            if st.button("Ödemeyi Kaydet"):
                if amt > 0:
                    pid = f"PAY-{datetime.now().strftime('%m%d%H%M')}"
                    pay_df = get_db(CSV_PAYOUTS)
                    save_db(CSV_PAYOUTS, pay_df, {
                        "Payout_ID": pid, "Time": datetime.now(), "Brand": p_brand,
                        "Amount": amt, "Method": "Bank", "Notes": bank_exp
                    })
                    log_action("ÖDEME", "Admin", f"{p_brand} ödemesi: {amt} TL")
                    st.success("Ödeme Kaydedildi!")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_pay_R:
            st.markdown("#### Ödeme Geçmişi")
            st.dataframe(pay_df[pay_df['Brand'] == p_brand] if not pay_df.empty else pd.DataFrame(), use_container_width=True)

    # --- 6. MARKA FATURALANDIRMA (Invoicing) ---
    with tabs[5]:
        st.markdown("### 🧾 Komisyon Faturalandırma")
        fin_df = get_db(CSV_FINANCE)
        inv_df = get_db(CSV_INVOICES)
        
        # Identify uninvoiced orders
        pending_inv = fin_df[fin_df['Invoice_Ref'].isna() | (fin_df['Invoice_Ref'] == "")]
        
        c1, c2 = st.columns([2, 1])
        with c1:
            if not pending_inv.empty:
                st.dataframe(pending_inv[['Order_ID', 'Brand', 'Commission_Amt']])
            else:
                st.info("Faturalandırılacak işlem yok.")
                
        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            t_brand = st.selectbox("Fatura Kesilecek Marka", list(BRAND_CONTRACTS.keys()))
            
            if st.button("Fatura Oluştur (Draft)"):
                items = pending_inv[pending_inv['Brand'] == t_brand]
                if not items.empty:
                    ref = f"INV-{datetime.now().strftime('%Y%m')}-{t_brand[:3]}"
                    comm_tot = items['Commission_Amt'].sum()
                    kdv = comm_tot * 0.20
                    
                    save_db(CSV_INVOICES, inv_df, {
                        "Invoice_Ref": ref, "Date": datetime.now().date(), "Brand": t_brand,
                        "Total_Commission": comm_tot, "KDV": kdv, "Total_Due": comm_tot + kdv,
                        "Sent_Status": "Pending", "Paid_Status": "Unpaid"
                    })
                    
                    # Update finance ledger
                    for idx in items.index:
                        fin_df.at[idx, 'Invoice_Ref'] = ref
                    update_db(CSV_FINANCE, fin_df)
                    
                    log_action("FATURA", "Admin", f"{ref} oluşturuldu")
                    st.success(f"{ref} oluşturuldu!")
                    st.rerun()
                else:
                    st.warning("Bu marka için bekleyen komisyon yok.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("#### Fatura Kayıtları")
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
                st.bar_chart(df['Brand'].value_counts())
            with t2:
                st.line_chart(df.groupby('Time')['Total_Value'].sum())
            with t3:
                # Need to parse items string for robust product analytics, simple count for now
                st.info("Ürün bazlı detaylar için veritabanı genişletiliyor...")
            with t4:
                st.bar_chart(fin.groupby('Brand')['Commission_Amt'].sum())
        else:
            st.info("Veri yok.")

    # --- 9. REHBER (SOP) ---
    with tabs[8]:
        st.markdown("### ❔ Operasyon Rehberi (SOP)")
        with st.expander("1. Sipariş Nasıl Girilir?", expanded=True):
            st.write("1. 'YENİ SEVKİYAT' sekmesine gidin.\n2. Müşteri bilgilerini girin.\n3. Sepete ürünleri ekleyin.\n4. 'FLASH DISPATCH' butonuna basın.")
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
        if st.button("Çıkış"):
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
