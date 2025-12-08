import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime, timedelta
import urllib.parse
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# 🏔️ NATUVISIO OS - TITANIUM EDITION (V14.0)
# Tam Entegre Lojistik & Finansal İşletim Sistemi
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO OS",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 1. AYARLAR & VERİ YAPISI (CONFIGURATION)
# ============================================================================

# --- GÜVENLİK ---
ADMIN_PASS = "admin2025"
PARTNER_CREDENTIALS = {
    "HAKI HEAL": "haki123",
    "AURORACO": "aurora2025",
    "LONGEVICALS": "longsci"
}

# --- DOSYA YOLLARI (VERİTABANI) ---
DB_DISPATCH = "dispatch_db.csv"   # Lojistik Hareketleri
DB_FINANCE = "finance_db.csv"     # Finansal Kayıtlar
DB_PAYMENTS = "payments_db.csv"   # Ödemeler
DB_INVOICES = "invoices_db.csv"   # Faturalar
DB_LOGS = "system_logs.csv"       # Denetim İzleri

# --- TASARIM SABİTLERİ ---
THEME = {
    "primary": "#4A6B45",         # Natuvisio Sage Green
    "secondary": "#2D4A2B",       # Forest Green
    "accent": "#D4AF37",          # Gold (Premium)
    "danger": "#C53030",          # Alert Red
    "success": "#2F855A",         # Success Green
    "bg_overlay": "rgba(248, 250, 248, 0.92)", # Çok açık gri/yeşil overlay (Okunabilirlik için)
}

LOGO_URL = "https://res.cloudinary.com/deb1j92hy/image/upload/f_auto,q_auto/v1764805291/natuvisio_logo_gtqtfs.png"
BG_IMAGE = "https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp"

# --- İŞ MANTIĞI & ANLAŞMALAR ---
KDV_ORANI = 0.20  # %20 KDV

MARKALAR = {
    "HAKI HEAL": {
        "komisyon": 0.15,
        "telefon": "601158976276",
        "renk": "#4ECDC4",
        "iban": "TR90 0006 1000 0000 1122 3344 55",
        "unvan": "Haki Heal Kozmetik Ltd. Şti."
    },
    "AURORACO": {
        "komisyon": 0.20,
        "telefon": "601158976276",
        "renk": "#FF6B6B",
        "iban": "TR90 0006 2000 0000 5566 7788 99",
        "unvan": "Auroraco Gıda A.Ş."
    },
    "LONGEVICALS": {
        "komisyon": 0.12,
        "telefon": "601158976276",
        "renk": "#95E1D3",
        "iban": "TR90 0001 5000 0000 9988 7766 55",
        "unvan": "Longevicals Sağlık Ürünleri A.Ş."
    }
}

URUN_KATALOGU = {
    "HAKI HEAL": {
        "HAKI HEAL KREM (50ml)": {"sku": "HH-CRM-01", "fiyat": 450},
        "HAKI HEAL VÜCUT LOSYONU": {"sku": "HH-BDY-01", "fiyat": 380},
        "HAKI HEAL SABUN": {"sku": "HH-SBN-01", "fiyat": 120}
    },
    "AURORACO": {
        "AURORACO MATCHA": {"sku": "AC-MTC-01", "fiyat": 650},
        "AURORACO KAKAO": {"sku": "AC-COC-01", "fiyat": 550},
        "AURORACO SUPERFOOD": {"sku": "AC-SPR-01", "fiyat": 800}
    },
    "LONGEVICALS": {
        "LONGEVICALS DHA": {"sku": "LG-DHA-01", "fiyat": 1200},
        "LONGEVICALS EPA": {"sku": "LG-EPA-01", "fiyat": 1150}
    }
}

# ============================================================================
# 2. VERİTABANI MOTORU (DATABASE ENGINE)
# ============================================================================

def init_db():
    """Sistem başlangıcında veritabanı bütünlüğünü kontrol eder"""
    schemas = {
        DB_DISPATCH: ["Siparis_ID", "Tarih", "Marka", "Musteri", "Telefon", "Adres", "Urunler_Str", "Toplam_Tutar", "Durum", "Takip_No", "Kargo_Firmasi", "Bildirim_Durumu", "Notlar"],
        DB_FINANCE: ["Siparis_ID", "Tarih", "Marka", "Satis_Tutar", "Komisyon_Oran", "Komisyon_Tutar", "KDV_Tutar", "Toplam_Kesinti", "Marka_Hakedis", "Fatura_Ref", "Odeme_Durumu"],
        DB_PAYMENTS: ["Odeme_ID", "Tarih", "Marka", "Tutar", "Yontem", "Aciklama", "Kaydeden"],
        DB_INVOICES: ["Fatura_ID", "Tarih", "Donem", "Marka", "Matrah", "KDV_Tutar", "Toplam_Fatura", "Durum", "Gonderildi"],
        DB_LOGS: ["Log_ID", "Zaman", "Kullanici", "Islem", "Detay"]
    }
    for file, cols in schemas.items():
        if not os.path.exists(file):
            pd.DataFrame(columns=cols).to_csv(file, index=False)

def get_data(file):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame()

def save_data(file, df, new_row=None):
    if new_row is not None:
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(file, index=False)
    return df

def update_data(file, df):
    df.to_csv(file, index=False)

def log_audit(user, action, details):
    df = get_data(DB_LOGS)
    new_log = {
        "Log_ID": f"LOG-{int(time.time())}",
        "Zaman": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Kullanici": user, "Islem": action, "Detay": details
    }
    save_data(DB_LOGS, df, new_log)

# ============================================================================
# 3. PREMIUM UI & CSS (TASARIM MOTORU)
# ============================================================================

def load_styles():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Inter:wght@400;500;600&display=swap');

        /* --- ANA YAPILANDIRMA --- */
        .stApp {{
            background-image: linear-gradient({THEME['bg_overlay']}, {THEME['bg_overlay']}), url("{BG_IMAGE}");
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #1a1a1a;
        }}

        /* --- NAVIGASYON --- */
        [data-testid="stSidebar"] {{
            background-color: #ffffff;
            border-right: 1px solid rgba(0,0,0,0.08);
            box-shadow: 4px 0 24px rgba(0,0,0,0.02);
        }}

        /* --- KART TASARIMI (GLASSMORPHISM V3) --- */
        .nv-card {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 10px 15px -3px rgba(0, 0, 0, 0.02);
            margin-bottom: 20px;
            transition: transform 0.2s ease;
        }}
        .nv-card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08); }}

        /* --- METRİKLER --- */
        .metric-box {{
            text-align: center;
            padding: 16px;
            border-radius: 12px;
            background: white;
            border: 1px solid #e2e8f0;
        }}
        .metric-val {{ font-family: 'Plus Jakarta Sans'; font-size: 28px; font-weight: 800; color: {THEME['primary']}; }}
        .metric-lbl {{ font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }}

        /* --- STATUS BADGES (DURUM ETİKETLERİ) --- */
        .badge {{ padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; }}
        .badge-pending {{ background: #FFF7ED; color: #C05621; border: 1px solid #FEEBC8; }}
        .badge-active {{ background: #E6FFFA; color: #2C7A7B; border: 1px solid #B2F5EA; }}
        .badge-done {{ background: #F0F5FF; color: #434190; border: 1px solid #E2E8F0; }}

        /* --- BUTONLAR & GİRDİLER --- */
        .stButton button {{
            background-color: {THEME['primary']} !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.6rem 1.2rem !important;
            box-shadow: 0 4px 6px rgba(74, 107, 69, 0.2) !important;
        }}
        .stButton button:hover {{ background-color: {THEME['secondary']} !important; transform: translateY(-1px); }}
        
        input, select, textarea {{
            background-color: #ffffff !important;
            border: 1px solid #cbd5e0 !important;
            color: #1a202c !important;
            border-radius: 8px !important;
        }}

        /* --- TYPOGRAPHY --- */
        h1, h2, h3 {{ font-family: 'Plus Jakarta Sans', sans-serif !important; color: #1a202c !important; letter-spacing: -0.5px; }}
        
        /* HIDE STREAMLIT CHROME */
        #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 4. STATE MANAGEMENT
# ============================================================================

if 'page' not in st.session_state: st.session_state.page = 'login'
if 'role' not in st.session_state: st.session_state.role = None
if 'brand_user' not in st.session_state: st.session_state.brand_user = None
if 'cart' not in st.session_state: st.session_state.cart = []
if 'brand_lock' not in st.session_state: st.session_state.brand_lock = None

# ============================================================================
# 5. GİRİŞ EKRANI (LOGIN)
# ============================================================================

def render_login():
    load_styles()
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown(f"""
        <div class="nv-card" style="text-align: center; padding: 40px;">
            <img src="{LOGO_URL}" style="width: 80px; margin-bottom: 20px;">
            <h2 style="margin: 0;">NATUVISIO OS</h2>
            <p style="color: #64748b; font-size: 13px; font-weight: 500;">TITANIUM EDITION v14.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        mode = st.radio("Giriş Modu", ["Yönetici (Admin)", "Partner"], horizontal=True, label_visibility="collapsed")
        
        if mode == "Partner":
            brand_select = st.selectbox("Marka Seçiniz", list(BRAND_CREDENTIALS.keys()))
        
        pwd = st.text_input("Erişim Şifresi", type="password")
        
        if st.button("GÜVENLİ GİRİŞ", use_container_width=True):
            if mode == "Yönetici (Admin)":
                if pwd == ADMIN_PASS:
                    st.session_state.role = "ADMIN"
                    st.session_state.page = "admin_home"
                    log_audit("Admin", "Giris", "Başarılı")
                    st.rerun()
                else:
                    st.error("Hatalı Şifre")
            else:
                if pwd == BRAND_CREDENTIALS.get(brand_select):
                    st.session_state.role = "PARTNER"
                    st.session_state.brand_user = brand_select
                    st.session_state.page = "partner_home"
                    log_audit(brand_select, "Giris", "Başarılı")
                    st.rerun()
                else:
                    st.error("Hatalı Marka Şifresi")

    st.markdown("""<div style="text-align:center; margin-top:50px; color:#94a3b8; font-size:11px;">🔒 NATUVISIO INTERNAL SYSTEM • UNAUTHORIZED ACCESS PROHIBITED</div>""", unsafe_allow_html=True)

# ============================================================================
# 6. ADMIN DASHBOARD - MAIN MODULES
# ============================================================================

def render_admin():
    load_styles()
    init_db()
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.image(LOGO_URL, width=50)
        st.markdown("### YÖNETİM MERKEZİ")
        st.markdown("**Master Operator**")
        st.markdown("---")
        
        menu = st.radio("NAVİGASYON", [
            "🚀 YENİ SEVKİYAT", 
            "🚀 SİPARİŞ TAKİBİ", 
            "✅ OPERASYON", 
            "🏦 FATURA & ÖDEME", 
            "📦 TÜM SİPARİŞLER", 
            "📊 ANALİTİKLER", 
            "❔ REHBER", 
            "📜 LOG KAYITLARI",
            "📥 EXPORT DATA"
        ])
        
        st.markdown("---")
        if st.button("🔴 ÇIKIŞ YAP"):
            st.session_state.role = None
            st.session_state.page = 'login'
            st.rerun()

    # --- TOP KPI BAR ---
    df_disp = get_data(DB_DISPATCH)
    df_fin = get_data(DB_FINANCE)
    
    if not df_disp.empty and not df_fin.empty:
        rev = df_fin['Satis_Tutar'].sum()
        comm = df_fin['Komisyon_Tutar'].sum()
        pending = len(df_disp[df_disp['Durum'] == 'Beklemede'])
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='metric-box'><div class='metric-val'>{len(df_disp)}</div><div class='metric-lbl'>Toplam Sipariş</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-box'><div class='metric-val'>{rev:,.0f}₺</div><div class='metric-lbl'>Toplam Ciro</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-box'><div class='metric-val' style='color:{THEME['primary']};'>{comm:,.0f}₺</div><div class='metric-lbl'>Net Komisyon</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='metric-box'><div class='metric-val' style='color:{THEME['danger']};'>{pending}</div><div class='metric-lbl'>İşlem Bekleyen</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # --- MODULE 1: NEW DISPATCH ---
    if menu == "🚀 YENİ SEVKİYAT":
        st.subheader("📝 Yeni Sipariş Oluştur")
        c_form, c_summ = st.columns([1.5, 1])
        
        with c_form:
            st.markdown('<div class="nv-card">', unsafe_allow_html=True)
            cust_name = st.text_input("Müşteri Adı Soyadı")
            cust_phone = st.text_input("Telefon (905...)")
            cust_addr = st.text_area("Adres", height=80)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="nv-card">', unsafe_allow_html=True)
            if st.session_state.cart:
                act_brand = st.session_state.cart[0]['Marka']
                st.info(f"🔒 Kilitli Marka: {act_brand}")
            else:
                act_brand = st.selectbox("Marka Seçiniz", list(MARKALAR.keys()))
            
            c1, c2 = st.columns([3, 1])
            with c1: prod = st.selectbox("Ürün", list(URUN_KATALOGU[act_brand].keys()))
            with c2: qty = st.number_input("Adet", 1, value=1)
            
            if st.button("➕ Sepete Ekle", use_container_width=True):
                p_data = URUN_KATALOGU[act_brand][prod]
                
                # Financial Calculation (Per Item)
                tutar = p_data['fiyat'] * qty
                kom = tutar * MARKALAR[act_brand]['komisyon']
                kdv = kom * KDV_ORANI
                kesinti = kom + kdv
                hakedis = tutar - kesinti
                
                st.session_state.cart.append({
                    "Marka": act_brand, "Urun": prod, "Adet": qty, 
                    "Tutar": tutar, "Komisyon": kom, "KDV": kdv, "Hakedis": hakedis
                })
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c_summ:
            st.markdown('<div class="nv-card">', unsafe_allow_html=True)
            st.markdown("#### 📦 Sepet Özeti")
            if st.session_state.cart:
                df_cart = pd.DataFrame(st.session_state.cart)
                st.dataframe(df_cart[['Urun', 'Adet', 'Tutar']], hide_index=True)
                
                tot_val = df_cart['Tutar'].sum()
                tot_hakedis = df_cart['Hakedis'].sum()
                
                st.markdown(f"<h3 style='text-align:right'>{tot_val:,.0f} TL</h3>", unsafe_allow_html=True)
                st.info(f"Markaya Ödenecek Net: {tot_hakedis:,.2f} TL")
                
                if st.button("⚡ SİPARİŞİ ONAYLA", type="primary"):
                    if cust_name and cust_phone:
                        oid = f"NV-{datetime.now().strftime('%m%d%H%M')}"
                        items = ", ".join([f"{x['Urun']} (x{x['Adet']})" for x in st.session_state.cart])
                        
                        # 1. Log Dispatch
                        d_df = get_data(DB_DISPATCH)
                        save_data(DB_DISPATCH, d_df, {
                            "Siparis_ID": oid, "Tarih": datetime.now(), "Marka": act_brand,
                            "Musteri": cust_name, "Telefon": cust_phone, "Adres": cust_addr,
                            "Urunler_Str": items, "Toplam_Tutar": tot_val, "Durum": "Beklemede",
                            "Takip_No": "", "Kargo_Firmasi": "", "Bildirim_Durumu": "Bekliyor", "Notlar": ""
                        })
                        
                        # 2. Log Finance
                        f_df = get_data(DB_FINANCE)
                        save_data(DB_FINANCE, f_df, {
                            "Siparis_ID": oid, "Tarih": datetime.now(), "Marka": act_brand,
                            "Satis_Tutar": tot_val, "Komisyon_Oran": MARKALAR[act_brand]['komisyon'],
                            "Komisyon_Tutar": df_cart['Komisyon'].sum(), "KDV_Tutar": df_cart['KDV'].sum(),
                            "Toplam_Kesinti": df_cart['Komisyon'].sum() + df_cart['KDV'].sum(),
                            "Marka_Hakedis": tot_hakedis, "Fatura_Ref": "", "Odeme_Durumu": "Bekliyor"
                        })
                        
                        log_audit("Admin", "Siparis", f"{oid} oluşturuldu")
                        st.success("Sipariş başarıyla oluşturuldu!")
                        st.session_state.cart = []
                        st.rerun()
                    else:
                        st.error("Müşteri bilgileri eksik.")
                
                if st.button("Temizle"):
                    st.session_state.cart = []
                    st.rerun()
            else:
                st.info("Sepet boş.")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- MODULE 2: ORDER TRACKING (SIPARIS TAKIBI) ---
    elif menu == "🚀 SİPARİŞ TAKİBİ":
        st.subheader("🔭 Aktif Siparişler")
        df = get_data(DB_DISPATCH)
        
        # Filtreler
        c1, c2 = st.columns(2)
        with c1: f_marka = st.multiselect("Marka Filtrele", list(MARKALAR.keys()))
        with c2: f_durum = st.multiselect("Durum Filtrele", df['Durum'].unique())
        
        if f_marka: df = df[df['Marka'].isin(f_marka)]
        if f_durum: df = df[df['Durum'].isin(f_durum)]
        
        st.dataframe(
            df.sort_values('Tarih', ascending=False),
            column_config={
                "Durum": st.column_config.SelectboxColumn("Durum", width="medium", options=["Beklemede", "Bildirildi", "Kargolandi", "Tamamlandi"], disabled=True),
                "Toplam_Tutar": st.column_config.NumberColumn("Tutar", format="%d ₺")
            },
            use_container_width=True, hide_index=True
        )

    # --- MODULE 3: OPERATIONS (OPERASYON) ---
    elif menu == "✅ OPERASYON":
        st.subheader("⚡ Operasyon Merkezi")
        df = get_data(DB_DISPATCH)
        
        # 1. Bildirim Bekleyenler
        pending = df[df['Bildirim_Durumu'] == 'Bekliyor']
        if not pending.empty:
            st.warning(f"{len(pending)} Sipariş Marka Bildirimi Bekliyor")
            for idx, row in pending.iterrows():
                with st.expander(f"🔴 {row['Siparis_ID']} - {row['Marka']}", expanded=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        # WhatsApp Link Generator
                        phone = MARKALAR[row['Marka']]['telefon']
                        msg = f"YENİ SİPARİŞ: {row['Siparis_ID']}\n{row['Urunler_Str']}\n\nMüşteri: {row['Musteri']}\nAdres: {row['Adres']}\n\nMüşteriye Kesilecek Fatura Tutarı: {row['Toplam_Tutar']} TL (KDV Dahil)"
                        link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                        st.markdown(f'[📲 WhatsApp Mesajı Gönder]({link})')
                    with c2:
                        if st.button("✅ Bildirildi", key=f"ntf_{idx}"):
                            mask = df['Siparis_ID'] == row['Siparis_ID']
                            df.loc[mask, 'Bildirim_Durumu'] = 'Bildirildi'
                            df.loc[mask, 'Durum'] = 'Bildirildi'
                            update_data(DB_DISPATCH, df)
                            st.rerun()
        else:
            st.success("Tüm bildirimler tamamlandı.")
            
        st.markdown("---")
        
        # 2. Manuel Kargo Girişi
        st.markdown("#### 📦 Manuel Kargo Girişi")
        waiting_ship = df[(df['Durum'] == 'Bildirildi') & (df['Takip_No'].isna() | (df['Takip_No'] == ""))]
        
        if not waiting_ship.empty:
            for idx, row in waiting_ship.iterrows():
                with st.container():
                    c1, c2, c3 = st.columns([2, 3, 1])
                    c1.write(f"**{row['Siparis_ID']}**")
                    track = c2.text_input("Takip No", key=f"trk_{idx}", label_visibility="collapsed")
                    if c3.button("Kaydet", key=f"sav_{idx}"):
                        mask = df['Siparis_ID'] == row['Siparis_ID']
                        df.loc[mask, 'Takip_No'] = track
                        df.loc[mask, 'Durum'] = 'Kargolandi'
                        update_data(DB_DISPATCH, df)
                        st.success("Kargolandı!")
                        st.rerun()
        else:
            st.info("Kargo bekleyen sipariş yok.")

    # --- MODULE 4: FINANCE (FATURA & ÖDEME) ---
    elif menu == "🏦 FATURA & ÖDEME":
        st.subheader("💰 Finansal Yönetim")
        
        tab1, tab2 = st.tabs(["💵 Marka Ödemeleri (Gider)", "🧾 Komisyon Faturaları (Gelir)"])
        
        # TAB 1: PAYABLES (Borçlar)
        with tab1:
            col_L, col_R = st.columns([1, 2])
            df_fin = get_data(DB_FINANCE)
            df_pay = get_data(DB_PAYMENTS)
            
            with col_L:
                st.markdown('<div class="nv-card">', unsafe_allow_html=True)
                sel_brand = st.selectbox("Marka Seçiniz", list(MARKALAR.keys()))
                
                # Bakiye Hesaplama
                # Toplam Hakediş (Markaya ödenecek)
                total_hakedis = df_fin[df_fin['Marka'] == sel_brand]['Marka_Hakedis'].sum()
                # Toplam Ödenen
                total_paid = df_pay[df_pay['Marka'] == sel_brand]['Tutar'].sum()
                balance = total_hakedis - total_paid
                
                st.metric("Ödenecek Bakiye", f"{balance:,.2f} TL")
                st.markdown(f"**IBAN:** {MARKALAR[sel_brand]['iban']}")
                
                # Copyable Bank Explanation
                bank_desc = f"NATUVISIO Hakedis Odemesi {sel_brand} {datetime.now().strftime('%m/%Y')}"
                st.code(bank_desc, language="text")
                st.caption("Banka açıklama kısmına yapıştırınız.")
                
                pay_amt = st.number_input("Ödeme Tutarı", 0.0, float(balance) if balance > 0 else 0.0)
                
                if st.button("✅ Ödemeyi Kaydet"):
                    if pay_amt > 0:
                        pid = f"PAY-{int(time.time())}"
                        save_data(DB_PAYMENTS, df_pay, {
                            "Odeme_ID": pid, "Tarih": datetime.now(), "Marka": sel_brand,
                            "Tutar": pay_amt, "Yontem": "Banka", "Aciklama": bank_desc, "Kaydeden": "Admin"
                        })
                        log_audit("Admin", "Odeme", f"{sel_brand} ödemesi: {pay_amt}")
                        st.success("Ödeme Kaydedildi!")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_R:
                st.markdown("#### Ödeme Geçmişi")
                if not df_pay.empty:
                    st.dataframe(df_pay[df_pay['Marka'] == sel_brand], use_container_width=True)

        # TAB 2: RECEIVABLES (Alacaklar/Faturalar)
        with tab2:
            df_inv = get_data(DB_INVOICES)
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown('<div class="nv-card">', unsafe_allow_html=True)
                inv_brand = st.selectbox("Fatura Kesilecek Marka", list(MARKALAR.keys()), key="inv_br")
                
                # Find uninvoiced orders
                uninvoiced = df_fin[(df_fin['Marka'] == inv_brand) & (df_fin['Fatura_Ref'].isna() | (df_fin['Fatura_Ref'] == ""))]
                
                if not uninvoiced.empty:
                    comm_tot = uninvoiced['Komisyon_Tutar'].sum()
                    kdv_tot = uninvoiced['KDV_Tutar'].sum()
                    inv_total = comm_tot + kdv_tot
                    
                    st.write(f"Komisyon: {comm_tot:,.2f} TL")
                    st.write(f"KDV (%20): {kdv_tot:,.2f} TL")
                    st.markdown(f"### Toplam: {inv_total:,.2f} TL")
                    
                    if st.button("📄 Faturayı Oluştur"):
                        fid = f"INV-{datetime.now().strftime('%Y%m')}-{inv_brand[:3]}"
                        save_data(DB_INVOICES, df_inv, {
                            "Fatura_ID": fid, "Tarih": datetime.now().date(), "Donem": datetime.now().strftime('%Y-%m'),
                            "Marka": inv_brand, "Matrah": comm_tot, "KDV_Tutar": kdv_tot, "Toplam_Fatura": inv_total,
                            "Durum": "Bekliyor", "Gonderildi": "Hayır"
                        })
                        
                        # Update Ledger
                        for idx in uninvoiced.index:
                            df_fin.at[idx, 'Fatura_Ref'] = fid
                        update_data(DB_FINANCE, df_fin)
                        
                        st.success(f"{fid} Oluşturuldu!")
                        st.rerun()
                else:
                    st.info("Faturalandırılacak işlem yok.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c2:
                st.markdown("#### Kesilen Faturalar")
                if not df_inv.empty:
                    # Action button to mark as sent
                    for idx, row in df_inv.iterrows():
                        with st.expander(f"{row['Fatura_ID']} - {row['Marka']} ({row['Toplam_Fatura']} TL)"):
                            if row['Gonderildi'] == 'Hayır':
                                if st.button("📧 Gönderildi Olarak İşaretle", key=f"sent_{row['Fatura_ID']}"):
                                    df_inv.at[idx, 'Gonderildi'] = 'Evet'
                                    update_data(DB_INVOICES, df_inv)
                                    st.rerun()
                            else:
                                st.success("✅ Markaya Gönderildi")

    # --- OTHER MODULES ---
    elif menu == "📊 ANALİTİKLER":
        df = get_data(DB_DISPATCH)
        if not df.empty:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### Marka Bazlı Satış")
                st.bar_chart(df.groupby("Marka")["Toplam_Tutar"].sum())
            with c2:
                st.markdown("### Durum Dağılımı")
                fig = px.pie(df, names='Durum')
                st.plotly_chart(fig)
    
    elif menu == "❔ REHBER":
        st.markdown("### 📘 Operasyon Rehberi (SOP)")
        with st.expander("1. Sipariş Nasıl Girilir?", expanded=True):
            st.write("1. 'Yeni Sevkiyat' menüsüne gidin.\n2. Müşteri bilgilerini girin.\n3. Sepete ürünleri ekleyin.\n4. 'Siparişi Onayla' butonuna basın.")
        with st.expander("2. Marka Ödemesi Nasıl Hesaplanır?"):
            st.write("Sistem; Satış Tutarı - (Komisyon + KDV) formülü ile net ödemeyi otomatik hesaplar ve 'Finansallar' sekmesinde gösterir.")

    elif menu == "📜 LOG KAYITLARI":
        st.dataframe(get_data(DB_LOGS).sort_values("Zaman", ascending=False), use_container_width=True)
        
    elif menu == "📥 EXPORT DATA":
        c1, c2, c3, c4 = st.columns(4)
        def convert(df): return df.to_csv(index=False).encode('utf-8')
        with c1: st.download_button("Siparişler", convert(get_data(DB_DISPATCH)), "orders.csv")
        with c2: st.download_button("Finans", convert(get_data(DB_FINANCE)), "finance.csv")
        with c3: st.download_button("Ödemeler", convert(get_data(DB_PAYMENTS)), "payments.csv")
        with c4: st.download_button("Faturalar", convert(get_data(DB_INVOICES)), "invoices.csv")
    
    elif menu == "📦 TÜM SİPARİŞLER":
        st.dataframe(get_data(DB_DISPATCH), use_container_width=True)

# ============================================================================
# 7. PARTNER DASHBOARD (PARTNER PORTAL)
# ============================================================================

def render_partner():
    load_styles()
    init_db()
    brand = st.session_state.brand_user
    
    # Header
    c1, c2 = st.columns([6,1])
    with c1: st.markdown(f"## 📦 {brand} PORTAL")
    with c2: 
        if st.button("ÇIKIŞ"):
            st.session_state.page = 'login'
            st.session_state.role = None
            st.rerun()
    st.markdown("---")
    
    tabs = st.tabs(["📋 SİPARİŞLER", "🚚 KARGO GİRİŞİ", "💰 HESABIM"])
    
    df_disp = get_data(DB_DISPATCH)
    brand_df = df_disp[df_disp['Marka'] == brand]
    
    with tabs[0]: # Orders
        st.dataframe(brand_df[['Siparis_ID', 'Tarih', 'Urunler_Str', 'Durum', 'Takip_No']], use_container_width=True)
        
    with tabs[1]: # Shipping
        pending = brand_df[brand_df['Durum'].isin(['Beklemede', 'Bildirildi'])]
        if not pending.empty:
            for idx, row in pending.iterrows():
                with st.expander(f"📦 {row['Siparis_ID']} - {row['Musteri']}"):
                    st.write(f"**Adres:** {row['Adres']}")
                    st.write(f"**Ürünler:** {row['Urunler_Str']}")
                    
                    track = st.text_input("Kargo Takip No", key=f"p_trk_{idx}")
                    if st.button("Kargola", key=f"p_shp_{idx}"):
                        orig_idx = df_disp[df_disp['Siparis_ID'] == row['Siparis_ID']].index[0]
                        df_disp.at[orig_idx, 'Takip_No'] = track
                        df_disp.at[orig_idx, 'Durum'] = 'Kargolandi'
                        update_data(DB_DISPATCH, df_disp)
                        st.success("Kargolandı!")
                        st.rerun()
        else:
            st.info("Kargolanacak sipariş yok.")
            
    with tabs[2]: # Finance
        df_fin = get_data(DB_FINANCE)
        my_fin = df_fin[df_fin['Marka'] == brand]
        
        total_hakedis = my_fin['Marka_Hakedis'].sum()
        df_pay = get_data(DB_PAYMENTS)
        my_pay = df_pay[df_pay['Marka'] == brand]
        paid = my_pay['Tutar'].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Toplam Hakediş", f"{total_hakedis:,.0f} TL")
        c2.metric("Alınan Ödeme", f"{paid:,.0f} TL")
        c3.metric("Bakiye", f"{(total_hakedis - paid):,.0f} TL")
        
        st.markdown("#### Ödeme Geçmişi")
        st.dataframe(my_pay, use_container_width=True)

# ============================================================================
# 8. MAIN ROUTER
# ============================================================================

if __name__ == "__main__":
    if st.session_state.page == 'login':
        render_login()
    elif st.session_state.page == 'admin_home' and st.session_state.role == 'ADMIN':
        render_admin()
    elif st.session_state.page == 'partner_home' and st.session_state.role == 'PARTNER':
        render_partner()
    else:
        st.session_state.page = 'login'
        st.rerun()
