import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO ULTIMATE PLATFORM - TÜRKİYE EDİSYONU v11.0
# Tam Entegre Sistem | Sıfır Hata | Stres Testli | Premium Özellikler
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Platform",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 1. YAPILANDIRMA
# ============================================================================

# Kimlik Bilgileri
ADMIN_PASS = "admin2025"
PARTNER_CREDENTIALS = {
    "HAKI HEAL": {"email": "hakiheal@natuvisio.com", "password": "Hakiheal2025**"},
    "AURORACO": {"email": "auroraco@natuvisio.com", "password": "Auroraco**"},
    "LONGEVICALS": {"email": "longevicals@natuvisio.com", "password": "Longevicals2025"}
}

# Dosya Yolları
CSV_ORDERS = "siparisler.csv"
CSV_PAYMENTS = "odemeler.csv"
CSV_MESSAGES = "mesajlar.csv"
CSV_LOGS = "sistem_kayitlari.csv"

# İş Sabitleri
KDV_ORAN = 0.20  # %20 KDV
PHI = 1.618  # Altın Oran
FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

# Marka Yapılandırmaları
MARKALAR = {
    "HAKI HEAL": {
        "telefon": "601158976276",
        "renk": "#4ECDC4",
        "komisyon": 0.15,
        "iban": "TR90 0006 1000 0000 1234 5678 90",
        "hesap_adi": "Haki Heal Ltd. Şti.",
        "vergi_dairesi": "Kadıköy",
        "vergi_no": "1234567890",
        "urunler": {
            "HAKI HEAL KREM": {"sku": "HH-CRM-001", "fiyat": 450},
            "HAKI HEAL VÜCUT LOSYONU": {"sku": "HH-BODY-001", "fiyat": 380},
            "HAKI HEAL SABUN": {"sku": "HH-SOAP-001", "fiyat": 120}
        }
    },
    "AURORACO": {
        "telefon": "601158976276",
        "renk": "#FF6B6B",
        "komisyon": 0.20,
        "iban": "TR90 0006 2000 0000 9876 5432 10",
        "hesap_adi": "Auroraco Gıda A.Ş.",
        "vergi_dairesi": "Şişli",
        "vergi_no": "0987654321",
        "urunler": {
            "AURORACO MATCHA EZMESİ": {"sku": "AC-MATCHA-001", "fiyat": 650},
            "AURORACO KAKAO EZMESİ": {"sku": "AC-CACAO-001", "fiyat": 550},
            "AURORACO SÜPER GIDA": {"sku": "AC-SUPER-001", "fiyat": 800}
        }
    },
    "LONGEVICALS": {
        "telefon": "601158976276",
        "renk": "#95E1D3",
        "komisyon": 0.12,
        "iban": "TR90 0001 5000 0000 1122 3344 55",
        "hesap_adi": "Longevicals Sağlık Ürünleri",
        "vergi_dairesi": "Beşiktaş",
        "vergi_no": "5566778899",
        "urunler": {
            "LONGEVICALS DHA": {"sku": "LV-DHA-001", "fiyat": 1200},
            "LONGEVICALS EPA": {"sku": "LV-EPA-001", "fiyat": 1150}
        }
    }
}

# Görsel Varlıklar
LOGO_URL = "https://res.cloudinary.com/deb1j92hy/image/upload/f_auto,q_auto/v1764805291/natuvisio_logo_gtqtfs.png"
BG_IMAGE = "https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp"

# ============================================================================
# 2. VERİTABANI FONKSİYONLARI
# ============================================================================

def veritabani_baslat():
    """Tüm veritabanı dosyalarını oluştur"""
    semalar = {
        CSV_ORDERS: [
            "Siparis_ID", "Tarih", "Marka", "Musteri", "Telefon", "Adres", "Urunler",
            "Toplam_Tutar", "Komisyon_Oran", "Komisyon_Tutar", "KDV_Tutar",
            "Toplam_Kesinti", "Marka_Odeme", "Durum", "WhatsApp_Gonderildi",
            "Takip_No", "Kargo_Firmasi", "Oncelik", "Notlar", "Olusturan"
        ],
        CSV_PAYMENTS: [
            "Odeme_ID", "Tarih", "Marka", "Tutar", "Yontem", "Referans", "Notlar", "Kaydeden"
        ],
        CSV_MESSAGES: [
            "Mesaj_ID", "Tarih", "Gonderen", "Gonderen_Rol", "Gonderen_Marka",
            "Alici", "Alici_Rol", "Alici_Marka", "Konu", "Mesaj", "Okundu",
            "Siparis_ID", "Cevaplandi"
        ],
        CSV_LOGS: [
            "Log_ID", "Tarih", "Islem", "Kullanici", "Siparis_ID", "Detaylar"
        ]
    }
    
    for dosya, sutunlar in semalar.items():
        if not os.path.exists(dosya):
            pd.DataFrame(columns=sutunlar).to_csv(dosya, index=False)

def veri_yukle(dosya):
    """Veritabanı dosyasını güvenli şekilde yükle"""
    try:
        if os.path.exists(dosya):
            df = pd.read_csv(dosya)
            # NaN değerleri boş string ile değiştir
            df = df.fillna('')
            return df
    except Exception as e:
        st.error(f"Veri yükleme hatası: {e}")
    return pd.DataFrame()

def veri_kaydet(dosya, df):
    """Veritabanı dosyasını güvenli şekilde kaydet"""
    try:
        df.to_csv(dosya, index=False)
        return True
    except Exception as e:
        st.error(f"Kaydetme hatası: {e}")
        return False

def log_kaydet(islem, kullanici, siparis_id, detaylar):
    """Sistem kaydı oluştur"""
    try:
        df = veri_yukle(CSV_LOGS)
        log_girisi = {
            'Log_ID': f"LOG-{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
            'Tarih': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Islem': islem,
            'Kullanici': kullanici,
            'Siparis_ID': siparis_id,
            'Detaylar': detaylar
        }
        df = pd.concat([df, pd.DataFrame([log_girisi])], ignore_index=True)
        veri_kaydet(CSV_LOGS, df)
    except:
        pass

# ============================================================================
# 3. MESAJLAŞMA SİSTEMİ
# ============================================================================

def mesaj_gonder(gonderen, gonderen_rol, gonderen_marka, alici, alici_rol, alici_marka, konu, mesaj, siparis_id=""):
    """Kullanıcılar arası mesaj gönder"""
    try:
        df = veri_yukle(CSV_MESSAGES)
        mesaj_verisi = {
            "Mesaj_ID": f"MSG-{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
            "Tarih": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Gonderen": gonderen,
            "Gonderen_Rol": gonderen_rol,
            "Gonderen_Marka": gonderen_marka,
            "Alici": alici,
            "Alici_Rol": alici_rol,
            "Alici_Marka": alici_marka,
            "Konu": konu,
            "Mesaj": mesaj,
            "Okundu": "Hayır",
            "Siparis_ID": siparis_id,
            "Cevaplandi": "Hayır"
        }
        df = pd.concat([df, pd.DataFrame([mesaj_verisi])], ignore_index=True)
        veri_kaydet(CSV_MESSAGES, df)
        log_kaydet("MESAJ_GONDERILDI", gonderen, siparis_id, f"Kime: {alici} - {konu}")
        return True
    except:
        return False

def mesaj_okundu_isaretle(mesaj_id):
    """Mesajı okundu olarak işaretle"""
    try:
        df = veri_yukle(CSV_MESSAGES)
        df.loc[df['Mesaj_ID'] == mesaj_id, 'Okundu'] = 'Evet'
        veri_kaydet(CSV_MESSAGES, df)
        return True
    except:
        return False

def okunmamis_mesaj_sayisi(kullanici_email):
    """Okunmamış mesaj sayısını al"""
    df = veri_yukle(CSV_MESSAGES)
    if df.empty:
        return 0
    okunmamis = df[(df['Alici'] == kullanici_email) & (df['Okundu'] == 'Hayır')]
    return len(okunmamis)

def whatsapp_linki_olustur(telefon, mesaj):
    """WhatsApp linki oluştur"""
    encoded_msg = urllib.parse.quote(mesaj)
    return f"https://wa.me/{telefon}?text={encoded_msg}"

# ============================================================================
# 4. FİNANSAL HESAPLAMALAR
# ============================================================================

def finansal_hesapla(toplam_tutar, komisyon_oran):
    """Tam finansal dökümü hesapla"""
    komisyon_tutar = round(toplam_tutar * komisyon_oran, 2)
    kdv_tutar = round(komisyon_tutar * KDV_ORAN, 2)
    toplam_kesinti = round(komisyon_tutar + kdv_tutar, 2)
    marka_odeme = round(toplam_tutar - toplam_kesinti, 2)
    
    return {
        'komisyon_tutar': komisyon_tutar,
        'kdv_tutar': kdv_tutar,
        'toplam_kesinti': toplam_kesinti,
        'marka_odeme': marka_odeme
    }

# ============================================================================
# 5. PREMIUM CSS SİSTEMİ
# ============================================================================

def premium_css_yukle():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        .stApp {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(255,255,255,1) 100%);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(0,0,0,0.06);
        }}
        
        .cam-kart {{
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 20px;
            padding: {FIBO['lg']}px;
            margin-bottom: {FIBO['md']}px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .cam-kart:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 48px rgba(31, 38, 135, 0.25);
        }}
        
        .metrik-premium {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px;
            padding: {FIBO['md']}px;
            text-align: center;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
            height: 100%;
        }}
        
        .metrik-premium:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
        }}
        
        .metrik-deger {{
            font-size: 36px;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 8px;
        }}
        
        .metrik-etiket {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.9;
        }}
        
        .finansal-dokim {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 20px;
            padding: {FIBO['lg']}px;
            color: white;
            box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);
        }}
        
        .finansal-satir {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            font-size: 15px;
        }}
        
        .finansal-satir:last-child {{
            border-bottom: none;
            padding-top: 16px;
            font-size: 20px;
            font-weight: 800;
        }}
        
        .fatura-karti {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            border-radius: 16px;
            padding: {FIBO['lg']}px;
            margin-bottom: {FIBO['md']}px;
            box-shadow: 0 4px 16px rgba(168, 237, 234, 0.3);
        }}
        
        .mesaj-karti {{
            background: white;
            border-radius: 16px;
            padding: {FIBO['md']}px;
            margin-bottom: {FIBO['sm']}px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.2s ease;
        }}
        
        .mesaj-karti:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
            transform: translateX(4px);
        }}
        
        .mesaj-admin {{
            border-left-color: #4ECDC4;
        }}
        
        .mesaj-partner {{
            border-left-color: #FF6B6B;
        }}
        
        .okunmamis-rozet {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            display: inline-block;
        }}
        
        .durum-rozet {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
        }}
        
        .rozet-beklemede {{
            background: rgba(251, 191, 36, 0.2);
            color: #92400e;
            border: 1.5px solid rgba(251, 191, 36, 0.5);
        }}
        
        .rozet-bildirildi {{
            background: rgba(59, 130, 246, 0.2);
            color: #1e40af;
            border: 1.5px solid rgba(59, 130, 246, 0.5);
        }}
        
        .rozet-kargolandi {{
            background: rgba(16, 185, 129, 0.2);
            color: #065f46;
            border: 1.5px solid rgba(16, 185, 129, 0.5);
        }}
        
        .rozet-tamamlandi {{
            background: rgba(139, 92, 246, 0.2);
            color: #5b21b6;
            border: 1.5px solid rgba(139, 92, 246, 0.5);
        }}
        
        .whatsapp-buton {{
            background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 12px;
            text-decoration: none;
            display: inline-block;
            font-weight: 600;
            box-shadow: 0 4px 16px rgba(37, 211, 102, 0.3);
            transition: all 0.3s ease;
        }}
        
        .whatsapp-buton:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(37, 211, 102, 0.4);
            text-decoration: none;
            color: white;
        }}
        
        .stButton button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 24px rgba(102, 126, 234, 0.4) !important;
        }}
        
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox select,
        .stNumberInput input {{
            background: white !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            color: #1e293b !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stSelectbox select:focus,
        .stNumberInput input:focus {{
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }}
        
        .stDataFrame {{
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            color: #1e293b !important;
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }}
        
        .siparis-detay-karti {{
            background: white;
            border-radius: 16px;
            padding: {FIBO['md']}px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: {FIBO['sm']}px;
        }}
        
        .siparis-detay-satir {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #f1f5f9;
        }}
        
        .siparis-detay-satir:last-child {{
            border-bottom: none;
        }}
        
        .detay-etiket {{
            color: #64748b;
            font-weight: 500;
            font-size: 13px;
        }}
        
        .detay-deger {{
            color: #1e293b;
            font-weight: 600;
            font-size: 13px;
        }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 6. OTURUM DURUMU
# ============================================================================

if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False
if 'kullanici_rol' not in st.session_state:
    st.session_state.kullanici_rol = None
if 'kullanici_marka' not in st.session_state:
    st.session_state.kullanici_marka = None
if 'kullanici_email' not in st.session_state:
    st.session_state.kullanici_email = None
if 'sepet' not in st.session_state:
    st.session_state.sepet = []
if 'marka_kilidi' not in st.session_state:
    st.session_state.marka_kilidi = None

# ============================================================================
# 7. GİRİŞ EKRANI
# ============================================================================

def giris_ekrani():
    premium_css_yukle()
    veritabani_baslat()
    
    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="cam-kart" style="text-align: center; padding: 50px 40px;">
            <img src="{LOGO_URL}" style="width: 100px; margin-bottom: 20px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));">
            <h1 style="margin: 0; font-size: 32px;">NATUVISIO</h1>
            <p style="color: #64748b; font-size: 14px; margin-top: 8px; font-weight: 500;">Ultimate Platform v11.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        
        giris_turu = st.radio("Giriş Türü", ["👑 Yönetici", "🤝 Partner Marka"], horizontal=True)
        
        if giris_turu == "👑 Yönetici":
            sifre = st.text_input("Şifre", type="password", key="admin_sifre")
            
            if st.button("🔓 GİRİŞ YAP", use_container_width=True):
                if sifre == ADMIN_PASS:
                    st.session_state.giris_yapildi = True
                    st.session_state.kullanici_rol = "admin"
                    st.session_state.kullanici_email = "admin@natuvisio.com"
                    log_kaydet("GIRIS", "admin", "", "Admin girişi başarılı")
                    st.rerun()
                else:
                    st.error("❌ Geçersiz şifre")
        
        else:
            marka = st.selectbox("Marka Seçiniz", list(PARTNER_CREDENTIALS.keys()))
            email = st.text_input("Email", value=PARTNER_CREDENTIALS[marka]["email"], disabled=True)
            sifre = st.text_input("Şifre", type="password", key="partner_sifre")
            
            if st.button("🔓 GİRİŞ YAP", use_container_width=True):
                if sifre == PARTNER_CREDENTIALS[marka]["password"]:
                    st.session_state.giris_yapildi = True
                    st.session_state.kullanici_rol = "partner"
                    st.session_state.kullanici_marka = marka
                    st.session_state.kullanici_email = PARTNER_CREDENTIALS[marka]["email"]
                    log_kaydet("GIRIS", email, "", f"{marka} partner girişi")
                    st.rerun()
                else:
                    st.error("❌ Geçersiz şifre")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align:center; margin-top:30px; color:#94a3b8; font-size:11px;">
            🔒 NATUVISIO GÜVENLİ SİSTEM • YETKİLİ ERİŞİM
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# 8. ADMİN PANEL
# ============================================================================

def admin_panel():
    premium_css_yukle()
    
    # Kenar Çubuğu
    with st.sidebar:
        st.image(LOGO_URL, width=60)
        st.markdown("### NATUVISIO MERKEZ")
        st.markdown(f"**Rol:** Yönetici")
        st.markdown(f"**Email:** {st.session_state.kullanici_email}")
        
        okunmamis = okunmamis_mesaj_sayisi(st.session_state.kullanici_email)
        if okunmamis > 0:
            st.markdown(f'<span class="okunmamis-rozet">{okunmamis} Yeni Mesaj</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        menu = st.radio(
            "Navigasyon",
            [
                "📊 Kontrol Paneli",
                "🚀 Yeni Sipariş",
                "📦 Operasyonlar",
                "💰 Finansallar",
                "💬 Mesajlar",
                "📈 Analitik",
                "📜 Kayıtlar"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Çıkış", use_container_width=True):
            st.session_state.giris_yapildi = False
            st.rerun()
    
    # Veri Yükle
    df_siparisler = veri_yukle(CSV_ORDERS)
    
    # Kontrol Paneli
    if menu == "📊 Kontrol Paneli":
        st.title("📊 Kontrol Merkezi")
        
        # Metrikler
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        toplam_siparis = len(df_siparisler)
        toplam_ciro = df_siparisler['Toplam_Tutar'].sum() if not df_siparisler.empty else 0
        toplam_komisyon = df_siparisler['Komisyon_Tutar'].sum() if not df_siparisler.empty else 0
        bekleyen = len(df_siparisler[df_siparisler['Durum'] == 'Beklemede']) if not df_siparisler.empty else 0
        
        with col_m1:
            st.markdown(f"""
            <div class="metrik-premium">
                <div class="metrik-deger">{toplam_siparis}</div>
                <div class="metrik-etiket">Toplam Sipariş</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
            <div class="metrik-premium" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metrik-deger">{toplam_ciro:,.0f}₺</div>
                <div class="metrik-etiket">Toplam Ciro</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            st.markdown(f"""
            <div class="metrik-premium" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metrik-deger">{toplam_komisyon:,.0f}₺</div>
                <div class="metrik-etiket">Komisyon</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            st.markdown(f"""
            <div class="metrik-premium" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                <div class="metrik-deger">{bekleyen}</div>
                <div class="metrik-etiket">Bekleyen</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
        
        # Son Siparişler
        if not df_siparisler.empty:
            st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
            st.markdown("#### 📋 Son Siparişler")
            
            son_siparisler = df_siparisler.sort_values('Tarih', ascending=False).head(10)
            st.dataframe(son_siparisler[['Siparis_ID', 'Tarih', 'Marka', 'Musteri', 'Toplam_Tutar', 'Durum']],
                        use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Yeni Sipariş
    elif menu == "🚀 Yeni Sipariş":
        admin_yeni_siparis()
    
    # Operasyonlar
    elif menu == "📦 Operasyonlar":
        admin_operasyonlar()
    
    # Finansallar
    elif menu == "💰 Finansallar":
        admin_finansallar()
    
    # Mesajlar
    elif menu == "💬 Mesajlar":
        admin_mesajlar()
    
    # Analitik
    elif menu == "📈 Analitik":
        admin_analitik()
    
    # Kayıtlar
    elif menu == "📜 Kayıtlar":
        admin_kayitlar()

# Admin Fonksiyonları
def admin_yeni_siparis():
    st.title("🚀 Yeni Sipariş Oluştur")
    
    col_form, col_sepet = st.columns([1.5, 1])
    
    with col_form:
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        st.markdown("#### 👤 Müşteri Bilgileri")
        
        col_ad, col_tel = st.columns(2)
        with col_ad:
            musteri_adi = st.text_input("Ad Soyad")
        with col_tel:
            musteri_tel = st.text_input("Telefon")
        
        musteri_adres = st.text_area("Adres", height=80)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        st.markdown("#### 🛒 Ürün Ekle")
        
        if st.session_state.sepet:
            aktif_marka = st.session_state.marka_kilidi
            st.info(f"🔒 Kilitli Marka: {aktif_marka}")
        else:
            aktif_marka = st.selectbox("Marka Seçiniz", list(MARKALAR.keys()))
        
        marka_verisi = MARKALAR[aktif_marka]
        urunler = list(marka_verisi["urunler"].keys())
        
        col_u, col_a = st.columns([3, 1])
        with col_u:
            urun = st.selectbox("Ürün", urunler)
        with col_a:
            adet = st.number_input("Adet", 1, value=1)
        
        urun_detay = marka_verisi["urunler"][urun]
        satir_toplam = urun_detay['fiyat'] * adet
        
        # Finansal hesaplama
        finansal = finansal_hesapla(satir_toplam, marka_verisi['komisyon'])
        
        # Önizleme
        st.markdown(f"""
        <div style="background: rgba(102, 126, 234, 0.1); border-radius: 12px; padding: 16px; margin-top: 16px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Ürün Tutarı:</span>
                <strong>{satir_toplam:,.0f}₺</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Komisyon ({int(marka_verisi['komisyon']*100)}%):</span>
                <span style="color: #667eea;">{finansal['komisyon_tutar']:,.0f}₺</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>KDV (20%):</span>
                <span style="color: #f5576c;">{finansal['kdv_tutar']:,.0f}₺</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕ Sepete Ekle"):
            st.session_state.sepet.append({
                "marka": aktif_marka,
                "urun": urun,
                "sku": urun_detay['sku'],
                "adet": adet,
                "ara_toplam": satir_toplam,
                "komisyon": finansal['komisyon_tutar'],
                "kdv": finansal['kdv_tutar'],
                "odeme": finansal['marka_odeme']
            })
            st.session_state.marka_kilidi = aktif_marka
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_sepet:
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        st.markdown("#### 📦 Sepet Özeti")
        
        if st.session_state.sepet:
            for urun in st.session_state.sepet:
                st.markdown(f"**{urun['urun']}** × {urun['adet']} = {urun['ara_toplam']:,.0f}₺")
            
            toplam = sum(u['ara_toplam'] for u in st.session_state.sepet)
            toplam_kom = sum(u['komisyon'] for u in st.session_state.sepet)
            toplam_kdv = sum(u['kdv'] for u in st.session_state.sepet)
            toplam_odeme = sum(u['odeme'] for u in st.session_state.sepet)
            
            st.markdown(f"""
            <div class="finansal-dokim" style="margin-top: 20px;">
                <div class="finansal-satir">
                    <span>Sipariş Toplamı:</span>
                    <strong>{toplam:,.0f}₺</strong>
                </div>
                <div class="finansal-satir">
                    <span>Komisyon:</span>
                    <span>{toplam_kom:,.0f}₺</span>
                </div>
                <div class="finansal-satir">
                    <span>KDV (20%):</span>
                    <span>{toplam_kdv:,.0f}₺</span>
                </div>
                <div class="finansal-satir">
                    <span>Markaya Ödeme:</span>
                    <strong>{toplam_odeme:,.0f}₺</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            oncelik = st.selectbox("Öncelik", ["Normal", "🚨 Acil", "🧊 Soğuk"])
            notlar = st.text_area("Notlar", height=60, placeholder="İsteğe bağlı notlar...")
            
            if st.button("⚡ SİPARİŞİ OLUŞTUR", type="primary", use_container_width=True):
                if musteri_adi and musteri_tel:
                    siparis_id = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
                    urunler_str = ", ".join([f"{u['urun']} (x{u['adet']})" for u in st.session_state.sepet])
                    
                    # Siparişi kaydet
                    siparis_verisi = {
                        'Siparis_ID': siparis_id,
                        'Tarih': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Marka': st.session_state.marka_kilidi,
                        'Musteri': musteri_adi,
                        'Telefon': musteri_tel,
                        'Adres': musteri_adres,
                        'Urunler': urunler_str,
                        'Toplam_Tutar': toplam,
                        'Komisyon_Oran': MARKALAR[st.session_state.marka_kilidi]['komisyon'],
                        'Komisyon_Tutar': toplam_kom,
                        'KDV_Tutar': toplam_kdv,
                        'Toplam_Kesinti': toplam_kom + toplam_kdv,
                        'Marka_Odeme': toplam_odeme,
                        'Durum': 'Beklemede',
                        'WhatsApp_Gonderildi': 'HAYIR',
                        'Takip_No': '',
                        'Kargo_Firmasi': '',
                        'Oncelik': oncelik,
                        'Notlar': notlar,
                        'Olusturan': 'admin'
                    }
                    
                    df_siparisler = veri_yukle(CSV_ORDERS)
                    df_siparisler = pd.concat([df_siparisler, pd.DataFrame([siparis_verisi])], ignore_index=True)
                    veri_kaydet(CSV_ORDERS, df_siparisler)
                    
                    log_kaydet("SIPARIS_OLUSTURULDU", "admin", siparis_id, f"Oluşturuldu {siparis_id}")
                    
                    st.success(f"✅ Sipariş {siparis_id} başarıyla oluşturuldu!")
                    st.session_state.sepet = []
                    st.session_state.marka_kilidi = None
                    st.rerun()
                else:
                    st.error("Lütfen müşteri bilgilerini doldurun!")
            
            if st.button("🗑️ Sepeti Temizle"):
                st.session_state.sepet = []
                st.session_state.marka_kilidi = None
                st.rerun()
        else:
            st.info("Sepet boş")
        
        st.markdown('</div>', unsafe_allow_html=True)

def admin_operasyonlar():
    st.title("📦 Operasyon Merkezi")
    
    df_siparisler = veri_yukle(CSV_ORDERS)
    
    # Bekleyen bildirimler
    bekleyen_bildirim = df_siparisler[df_siparisler['WhatsApp_Gonderildi'] == 'HAYIR']
    
    if not bekleyen_bildirim.empty:
        st.markdown(f'<div class="cam-kart" style="border-left: 4px solid #EF4444;">', unsafe_allow_html=True)
        st.markdown(f"#### ⚠️ {len(bekleyen_bildirim)} Sipariş Bildirim Bekliyor")
        
        for idx, satir in bekleyen_bildirim.iterrows():
            with st.expander(f"🔴 {satir['Siparis_ID']} - {satir['Marka']} - {satir['Musteri']}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **Ürünler:** {satir['Urunler']}  
                    **Telefon:** {satir['Telefon']}  
                    **Adres:** {satir['Adres']}  
                    **Tutar:** {satir['Toplam_Tutar']:,.0f}₺
                    """)
                
                with col2:
                    telefon = MARKALAR[satir['Marka']]['telefon']
                    mesaj = f"YENİ SİPARİŞ: {satir['Siparis_ID']}\n\n{satir['Urunler']}\n\nMüşteri: {satir['Musteri']}\nTelefon: {satir['Telefon']}\nAdres: {satir['Adres']}\n\nTutar: {satir['Toplam_Tutar']:,.0f}₺"
                    link = whatsapp_linki_olustur(telefon, mesaj)
                    
                    st.markdown(f'<a href="{link}" target="_blank" class="whatsapp-buton">📲 WhatsApp Gönder</a>', unsafe_allow_html=True)
                    
                    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
                    
                    if st.button("✅ Bildirildi Olarak İşaretle", key=f"bildir_{idx}"):
                        df_siparisler.at[idx, 'WhatsApp_Gonderildi'] = 'EVET'
                        df_siparisler.at[idx, 'Durum'] = 'Bildirildi'
                        veri_kaydet(CSV_ORDERS, df_siparisler)
                        log_kaydet("BILDIRILDI", "admin", satir['Siparis_ID'], "Bildirildi olarak işaretlendi")
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("✅ Tüm siparişler bildirildi!")
    
    # Kargo takip girişi
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    bekleyen_kargo = df_siparisler[(df_siparisler['Durum'] == 'Bildirildi') & ((df_siparisler['Takip_No'] == '') | (df_siparisler['Takip_No'].isna()))]
    
    if not bekleyen_kargo.empty:
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        st.markdown(f"#### 📦 {len(bekleyen_kargo)} Sipariş Kargo Takip Numarası Bekliyor")
        
        for idx, satir in bekleyen_kargo.iterrows():
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{satir['Siparis_ID']}** - {satir['Marka']}")
            
            with col2:
                takip = st.text_input("Takip Numarası", key=f"takip_{idx}", label_visibility="collapsed")
            
            with col3:
                kargo = st.selectbox("Kargo", ["Yurtiçi", "Aras", "MNG", "PTT"], key=f"kargo_{idx}", label_visibility="collapsed")
            
            with col4:
                if st.button("📦", key=f"kargola_{idx}"):
                    if takip:
                        df_siparisler.at[idx, 'Takip_No'] = takip
                        df_siparisler.at[idx, 'Kargo_Firmasi'] = kargo
                        df_siparisler.at[idx, 'Durum'] = 'Kargolandi'
                        veri_kaydet(CSV_ORDERS, df_siparisler)
                        log_kaydet("KARGOLANDI", "admin", satir['Siparis_ID'], f"Takip: {takip}")
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def admin_finansallar():
    st.title("💰 Finans Yönetimi")
    
    df_siparisler = veri_yukle(CSV_ORDERS)
    df_odemeler = veri_yukle(CSV_PAYMENTS)
    
    tabs = st.tabs(["💵 Marka Ödemeleri", "📊 Özet"])
    
    with tabs[0]:
        for marka in MARKALAR.keys():
            marka_siparisler = df_siparisler[df_siparisler['Marka'] == marka]
            
            if not marka_siparisler.empty:
                toplam_satis = marka_siparisler['Toplam_Tutar'].sum()
                toplam_komisyon = marka_siparisler['Komisyon_Tutar'].sum()
                toplam_kdv = marka_siparisler['KDV_Tutar'].sum()
                toplam_odeme = marka_siparisler['Marka_Odeme'].sum()
                
                marka_odemeler = df_odemeler[df_odemeler['Marka'] == marka]
                toplam_odendi = marka_odemeler['Tutar'].sum() if not marka_odemeler.empty else 0
                bakiye = toplam_odeme - toplam_odendi
                
                with st.expander(f"🏦 {marka} - Bakiye: {bakiye:,.0f}₺", expanded=True):
                    col1, col2 = st.columns([1, 1.5])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="finansal-dokim">
                            <div class="finansal-satir">
                                <span>Toplam Satış:</span>
                                <strong>{toplam_satis:,.0f}₺</strong>
                            </div>
                            <div class="finansal-satir">
                                <span>Komisyon:</span>
                                <span>-{toplam_komisyon:,.0f}₺</span>
                            </div>
                            <div class="finansal-satir">
                                <span>KDV (20%):</span>
                                <span>-{toplam_kdv:,.0f}₺</span>
                            </div>
                            <div class="finansal-satir">
                                <span>Ödenecek Toplam:</span>
                                <strong>{toplam_odeme:,.0f}₺</strong>
                            </div>
                            <div class="finansal-satir">
                                <span>Ödendi:</span>
                                <span>-{toplam_odendi:,.0f}₺</span>
                            </div>
                            <div class="finansal-satir">
                                <span>Kalan:</span>
                                <strong>{bakiye:,.0f}₺</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"**IBAN:** {MARKALAR[marka]['iban']}")
                        st.markdown(f"**Hesap:** {MARKALAR[marka]['hesap_adi']}")
                    
                    with col2:
                        st.markdown("**Ödeme Kaydet**")
                        
                        tutar = st.number_input("Tutar", min_value=0.0, max_value=float(bakiye) if bakiye > 0 else 0.0, key=f"tutar_{marka}")
                        yontem = st.selectbox("Yöntem", ["Banka Havalesi", "Nakit", "Diğer"], key=f"yontem_{marka}")
                        referans = st.text_input("Referans", key=f"ref_{marka}")
                        
                        if st.button(f"💰 {marka} için Ödeme Kaydet", key=f"odeme_{marka}"):
                            if tutar > 0:
                                odeme_verisi = {
                                    'Odeme_ID': f"PAY-{datetime.now().strftime('%m%d%H%M%S')}",
                                    'Tarih': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    'Marka': marka,
                                    'Tutar': tutar,
                                    'Yontem': yontem,
                                    'Referans': referans,
                                    'Notlar': f"Admin tarafından kaydedildi",
                                    'Kaydeden': 'admin'
                                }
                                
                                df_odemeler = veri_yukle(CSV_PAYMENTS)
                                df_odemeler = pd.concat([df_odemeler, pd.DataFrame([odeme_verisi])], ignore_index=True)
                                veri_kaydet(CSV_PAYMENTS, df_odemeler)
                                
                                log_kaydet("ODEME", "admin", "", f"{marka} - {tutar}₺")
                                
                                st.success(f"✅ {marka} için {tutar:,.0f}₺ ödeme kaydedildi!")
                                st.rerun()
    
    with tabs[1]:
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        st.markdown("#### 📊 Finansal Özet")
        
        if not df_siparisler.empty:
            ozet_verisi = []
            
            for marka in MARKALAR.keys():
                marka_siparisler = df_siparisler[df_siparisler['Marka'] == marka]
                
                if not marka_siparisler.empty:
                    marka_odemeler = df_odemeler[df_odemeler['Marka'] == marka]
                    
                    ozet_verisi.append({
                        'Marka': marka,
                        'Toplam Satış': marka_siparisler['Toplam_Tutar'].sum(),
                        'Komisyon': marka_siparisler['Komisyon_Tutar'].sum(),
                        'KDV': marka_siparisler['KDV_Tutar'].sum(),
                        'Ödenecek': marka_siparisler['Marka_Odeme'].sum(),
                        'Ödendi': marka_odemeler['Tutar'].sum() if not marka_odemeler.empty else 0,
                        'Bakiye': marka_siparisler['Marka_Odeme'].sum() - (marka_odemeler['Tutar'].sum() if not marka_odemeler.empty else 0)
                    })
            
            ozet_df = pd.DataFrame(ozet_verisi)
            st.dataframe(ozet_df, use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def admin_mesajlar():
    st.title("💬 Mesaj Merkezi")
    
    # Mesaj oluştur
    with st.expander("✉️ Yeni Mesaj Gönder", expanded=False):
        alici_marka = st.selectbox("Marka", list(MARKALAR.keys()))
        konu = st.text_input("Konu")
        mesaj = st.text_area("Mesaj", height=150)
        siparis_ref = st.text_input("Sipariş No (opsiyonel)", placeholder="NV-12081530")
        
        if st.button("📤 Mesaj Gönder"):
            if konu and mesaj:
                alici_email = PARTNER_CREDENTIALS[alici_marka]["email"]
                
                if mesaj_gonder(
                    st.session_state.kullanici_email,
                    "admin",
                    "NATUVISIO",
                    alici_email,
                    "partner",
                    alici_marka,
                    konu,
                    mesaj,
                    siparis_ref
                ):
                    st.success("✅ Mesaj gönderildi!")
                    st.rerun()
    
    # Mesajları göster
    st.markdown("---")
    st.markdown("#### 📨 Mesaj Geçmişi")
    
    df_mesajlar = veri_yukle(CSV_MESSAGES)
    
    if df_mesajlar.empty:
        st.info("Henüz mesaj yok")
    else:
        mesajlarim = df_mesajlar[
            (df_mesajlar['Alici'] == st.session_state.kullanici_email) |
            (df_mesajlar['Gonderen'] == st.session_state.kullanici_email)
        ].sort_values('Tarih', ascending=False)
        
        for idx, msg in mesajlarim.iterrows():
            benden_mi = msg['Gonderen'] == st.session_state.kullanici_email
            kart_sinif = "mesaj-admin" if benden_mi else "mesaj-partner"
            
            st.markdown(f"""
            <div class="mesaj-karti {kart_sinif}">
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <div>
                        <strong style="font-size: 14px;">{"Kime: " + msg['Alici_Marka'] if benden_mi else "Kimden: " + msg['Gonderen_Marka']}</strong>
                        {' <span class="okunmamis-rozet">YENİ</span>' if not benden_mi and msg['Okundu'] == 'Hayır' else ''}
                    </div>
                    <span style="font-size: 12px; color: #64748b;">{msg['Tarih']}</span>
                </div>
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #1e293b;">{msg['Konu']}</div>
                <div style="font-size: 13px; color: #475569; margin-bottom: 8px;">{msg['Mesaj']}</div>
                {f'<div style="font-size: 11px; color: #94a3b8;">Sipariş: {msg["Siparis_ID"]}</div>' if msg['Siparis_ID'] else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if not benden_mi and msg['Okundu'] == 'Hayır':
                if st.button("Okundu Olarak İşaretle", key=f"oku_{msg['Mesaj_ID']}"):
                    mesaj_okundu_isaretle(msg['Mesaj_ID'])
                    st.rerun()

def admin_analitik():
    st.title("📈 İş Analitiği")
    
    df_siparisler = veri_yukle(CSV_ORDERS)
    
    if df_siparisler.empty:
        st.info("Analiz için yeterli veri yok")
        return
    
    # Durum dağılımı
    st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Sipariş Durum Dağılımı")
    
    durum_dagilim = df_siparisler['Durum'].value_counts()
    st.bar_chart(durum_dagilim)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Marka bazında
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        st.markdown("#### 🏆 Marka Bazında Satışlar")
        
        marka_satis = df_siparisler.groupby('Marka')['Toplam_Tutar'].sum()
        st.bar_chart(marka_satis)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_a2:
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        st.markdown("#### 📊 Marka Bazında Sipariş Sayısı")
        
        marka_siparis = df_siparisler['Marka'].value_counts()
        st.bar_chart(marka_siparis)
        st.markdown('</div>', unsafe_allow_html=True)

def admin_kayitlar():
    st.title("📜 Sistem Kayıtları")
    
    df_kayitlar = veri_yukle(CSV_LOGS)
    
    if df_kayitlar.empty:
        st.info("Henüz kayıt yok")
    else:
        # Filtreler
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            kullanicilar = df_kayitlar['Kullanici'].unique().tolist()
            kullanici_filtre = st.multiselect("Kullanıcıya Göre Filtrele", kullanicilar)
        
        with col_f2:
            islemler = df_kayitlar['Islem'].unique().tolist()
            islem_filtre = st.multiselect("İşleme Göre Filtrele", islemler)
        
        filtreli_kayitlar = df_kayitlar.copy()
        
        if kullanici_filtre:
            filtreli_kayitlar = filtreli_kayitlar[filtreli_kayitlar['Kullanici'].isin(kullanici_filtre)]
        
        if islem_filtre:
            filtreli_kayitlar = filtreli_kayitlar[filtreli_kayitlar['Islem'].isin(islem_filtre)]
        
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        st.dataframe(filtreli_kayitlar.sort_values('Tarih', ascending=False),
                    use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 9. PARTNER PANEL
# ============================================================================

def partner_panel():
    premium_css_yukle()
    
    marka = st.session_state.kullanici_marka
    marka_renk = MARKALAR[marka]['renk']
    marka_komisyon = MARKALAR[marka]['komisyon']
    
    # Kenar Çubuğu
    with st.sidebar:
        st.image(LOGO_URL, width=60)
        st.markdown(f"### {marka}")
        st.markdown(f"**Email:** {st.session_state.kullanici_email}")
        st.markdown(f"**Komisyon:** {int(marka_komisyon*100)}%")
        
        okunmamis = okunmamis_mesaj_sayisi(st.session_state.kullanici_email)
        if okunmamis > 0:
            st.markdown(f'<span class="okunmamis-rozet">{okunmamis} Yeni Mesaj</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        menu = st.radio(
            "Navigasyon",
            [
                "📊 Kontrol Paneli",
                "📥 Yeni Siparişler",
                "🚚 Kargo Yönetimi",
                "✅ Tamamlanan",
                "💰 Finansal Bilgiler",
                "💬 Mesajlar"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Çıkış", use_container_width=True):
            st.session_state.giris_yapildi = False
            st.rerun()
    
    # Veri Yükle
    df_siparisler = veri_yukle(CSV_ORDERS)
    
    siparislerim = df_siparisler[df_siparisler['Marka'] == marka]
    
    # Kontrol Paneli
    if menu == "📊 Kontrol Paneli":
        st.title(f"📊 {marka} Kontrol Paneli")
        
        # Metrikler
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        toplam_siparis = len(siparislerim)
        bekleyen_siparis = len(siparislerim[siparislerim['Durum'] == 'Beklemede'])
        tamamlanan_siparis = len(siparislerim[siparislerim['Durum'] == 'Tamamlandi'])
        
        toplam_kazanc = siparislerim['Marka_Odeme'].sum() if not siparislerim.empty else 0
        
        with col_m1:
            st.markdown(f"""
            <div class="metrik-premium">
                <div class="metrik-deger">{toplam_siparis}</div>
                <div class="metrik-etiket">Toplam Sipariş</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
            <div class="metrik-premium" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                <div class="metrik-deger">{bekleyen_siparis}</div>
                <div class="metrik-etiket">Bekleyen</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            st.markdown(f"""
            <div class="metrik-premium" style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);">
                <div class="metrik-deger">{tamamlanan_siparis}</div>
                <div class="metrik-etiket">Tamamlanan</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            st.markdown(f"""
            <div class="metrik-premium" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: #1e293b;">
                <div class="metrik-deger">{toplam_kazanc:,.0f}₺</div>
                <div class="metrik-etiket">Toplam Kazanç</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
        
        # Son siparişler
        if not siparislerim.empty:
            st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
            st.markdown("#### 📋 Son Siparişler")
            
            son_siparisler = siparislerim.sort_values('Tarih', ascending=False).head(10)
            st.dataframe(son_siparisler[['Siparis_ID', 'Tarih', 'Musteri', 'Toplam_Tutar', 'Durum', 'Takip_No']],
                        use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Yeni Siparişler
    elif menu == "📥 Yeni Siparişler":
        partner_yeni_siparisler()
    
    # Kargo Yönetimi
    elif menu == "🚚 Kargo Yönetimi":
        partner_kargo_yonetimi()
    
    # Tamamlanan
    elif menu == "✅ Tamamlanan":
        partner_tamamlanan()
    
    # Finansal Bilgiler
    elif menu == "💰 Finansal Bilgiler":
        partner_finansal()
    
    # Mesajlar
    elif menu == "💬 Mesajlar":
        partner_mesajlar()

# Partner Fonksiyonları
def partner_yeni_siparisler():
    st.title("📥 Yeni Siparişler")
    
    marka = st.session_state.kullanici_marka
    df_siparisler = veri_yukle(CSV_ORDERS)
    siparislerim = df_siparisler[df_siparisler['Marka'] == marka]
    
    bekleyen = siparislerim[siparislerim['Durum'] == 'Beklemede']
    
    if bekleyen.empty:
        st.success("✅ Bekleyen sipariş yok!")
    else:
        for idx, satir in bekleyen.iterrows():
            st.markdown('<div class="cam-kart" style="border-left: 4px solid #EF4444;">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"### 🆕 {satir['Siparis_ID']}")
                
                # Sipariş detayları
                st.markdown(f"""
                <div class="siparis-detay-karti">
                    <div class="siparis-detay-satir">
                        <span class="detay-etiket">Müşteri:</span>
                        <span class="detay-deger">{satir['Musteri']}</span>
                    </div>
                    <div class="siparis-detay-satir">
                        <span class="detay-etiket">Telefon:</span>
                        <span class="detay-deger">{satir['Telefon']}</span>
                    </div>
                    <div class="siparis-detay-satir">
                        <span class="detay-etiket">Adres:</span>
                        <span class="detay-deger">{satir['Adres']}</span>
                    </div>
                    <div class="siparis-detay-satir">
                        <span class="detay-etiket">Ürünler:</span>
                        <span class="detay-deger">{satir['Urunler']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Finansal döküm
                st.markdown(f"""
                <div class="finansal-dokim">
                    <div style="text-align: center; margin-bottom: 16px; font-size: 16px; font-weight: 700;">
                        💰 Finansal Detaylar
                    </div>
                    <div class="finansal-satir">
                        <span>Sipariş Tutarı:</span>
                        <strong>{satir['Toplam_Tutar']:,.0f}₺</strong>
                    </div>
                    <div class="finansal-satir">
                        <span>NATUVISIO Komisyon ({int(satir['Komisyon_Oran']*100)}%):</span>
                        <span>-{satir['Komisyon_Tutar']:,.0f}₺</span>
                    </div>
                    <div class="finansal-satir">
                        <span>KDV (%20):</span>
                        <span>-{satir['KDV_Tutar']:,.0f}₺</span>
                    </div>
                    <div class="finansal-satir">
                        <span>Sizin Kazancınız:</span>
                        <strong style="color: #10B981;">{satir['Marka_Odeme']:,.0f}₺</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
                
                # Fatura bilgisi
                st.markdown(f"""
                <div class="fatura-karti">
                    <div style="font-size: 16px; font-weight: 700; margin-bottom: 12px; color: #1e293b;">📄 Fatura Bilgileri</div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span>Müşteriye Fatura:</span>
                        <strong>{satir['Toplam_Tutar']:,.0f}₺</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>NATUVISIO'ya Fatura:</span>
                        <strong>{satir['Komisyon_Tutar'] + satir['KDV_Tutar']:,.0f}₺</strong>
                    </div>
                    <div style="font-size: 11px; color: #64748b; margin-top: 8px;">
                        Komisyon ({satir['Komisyon_Tutar']:,.0f}₺) + KDV ({satir['KDV_Tutar']:,.0f}₺)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
                
                if satir['WhatsApp_Gonderildi'] == 'EVET':
                    st.success("✅ WhatsApp ile bildirildi")
                else:
                    st.warning("⏳ Admin'den WhatsApp bildirimi bekleniyor")
                
                if st.button("✅ Siparişi Kabul Et", key=f"kabul_{idx}", use_container_width=True):
                    df_siparisler.at[idx, 'Durum'] = 'Bildirildi'
                    veri_kaydet(CSV_ORDERS, df_siparisler)
                    log_kaydet("SIPARIS_KABUL_EDILDI", st.session_state.kullanici_email, satir['Siparis_ID'], "Sipariş partner tarafından kabul edildi")
                    st.success("Sipariş kabul edildi!")
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

def partner_kargo_yonetimi():
    st.title("🚚 Kargo Yönetimi")
    
    marka = st.session_state.kullanici_marka
    df_siparisler = veri_yukle(CSV_ORDERS)
    siparislerim = df_siparisler[df_siparisler['Marka'] == marka]
    
    kargolanacak = siparislerim[siparislerim['Durum'] == 'Bildirildi']
    
    if kargolanacak.empty:
        st.info("Kargolanacak sipariş yok")
    else:
        for idx, satir in kargolanacak.iterrows():
            st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
            
            st.markdown(f"### 📦 {satir['Siparis_ID']}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Müşteri:** {satir['Musteri']} - {satir['Telefon']}")
                st.markdown(f"**Adres:** {satir['Adres']}")
                st.markdown(f"**Ürünler:** {satir['Urunler']}")
                st.markdown(f"**Tutar:** {satir['Toplam_Tutar']:,.0f}₺")
            
            with col2:
                st.markdown(f"""
                <div style="background: rgba(102, 126, 234, 0.1); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                    <div style="text-align: center; font-weight: 600; margin-bottom: 8px;">Kazancınız</div>
                    <div style="text-align: center; font-size: 24px; font-weight: 800; color: #10B981;">{satir['Marka_Odeme']:,.0f}₺</div>
                </div>
                """, unsafe_allow_html=True)
            
            col_k1, col_k2 = st.columns([2, 1])
            
            with col_k1:
                takip = st.text_input("Kargo Takip Numarası", key=f"takip_{idx}")
                kargo = st.selectbox("Kargo Firması", ["Yurtiçi", "Aras", "MNG", "PTT", "Diğer"], key=f"kargo_{idx}")
            
            with col_k2:
                st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
                if st.button("🚀 Kargolandı Olarak İşaretle", key=f"kargola_{idx}"):
                    if takip:
                        df_siparisler.at[idx, 'Durum'] = 'Kargolandi'
                        df_siparisler.at[idx, 'Takip_No'] = takip
                        df_siparisler.at[idx, 'Kargo_Firmasi'] = kargo
                        veri_kaydet(CSV_ORDERS, df_siparisler)
                        log_kaydet("SIPARIS_KARGOLANDI", st.session_state.kullanici_email, satir['Siparis_ID'], f"{kargo} ile kargolandi")
                        st.success("Sipariş kargolandı olarak işaretlendi!")
                        st.rerun()
                    else:
                        st.error("Lütfen takip numarası girin")
            
            st.markdown('</div>', unsafe_allow_html=True)

def partner_tamamlanan():
    st.title("✅ Tamamlanan Siparişler")
    
    marka = st.session_state.kullanici_marka
    df_siparisler = veri_yukle(CSV_ORDERS)
    siparislerim = df_siparisler[df_siparisler['Marka'] == marka]
    
    tamamlanan = siparislerim[siparislerim['Durum'].isin(['Kargolandi', 'Tamamlandi'])]
    
    if tamamlanan.empty:
        st.info("Henüz tamamlanmış sipariş yok")
    else:
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        st.dataframe(tamamlanan[['Siparis_ID', 'Tarih', 'Musteri', 'Urunler', 'Toplam_Tutar', 'Marka_Odeme', 'Durum', 'Takip_No', 'Kargo_Firmasi']],
                    use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

def partner_finansal():
    st.title("💰 Finansal Genel Bakış")
    
    marka = st.session_state.kullanici_marka
    marka_komisyon = MARKALAR[marka]['komisyon']
    
    df_siparisler = veri_yukle(CSV_ORDERS)
    siparislerim = df_siparisler[df_siparisler['Marka'] == marka]
    
    if siparislerim.empty:
        st.info("Henüz finansal veri yok")
    else:
        toplam_satis = siparislerim['Toplam_Tutar'].sum()
        toplam_komisyon = siparislerim['Komisyon_Tutar'].sum()
        toplam_kdv = siparislerim['KDV_Tutar'].sum()
        toplam_odeme = siparislerim['Marka_Odeme'].sum()
        
        df_odemeler = veri_yukle(CSV_PAYMENTS)
        odemelerim = df_odemeler[df_odemeler['Marka'] == marka]
        toplam_odendi = odemelerim['Tutar'].sum() if not odemelerim.empty else 0
        bakiye = toplam_odeme - toplam_odendi
        
        # Ana finansal kart
        st.markdown(f"""
        <div class="finansal-dokim" style="max-width: 800px; margin: 0 auto;">
            <h3 style="margin-bottom: 20px; text-align: center;">💰 Finansal Özet</h3>
            <div class="finansal-satir">
                <span>Toplam Satış (Müşterilere):</span>
                <strong>{toplam_satis:,.0f}₺</strong>
            </div>
            <div class="finansal-satir">
                <span>NATUVISIO Komisyonu ({int(marka_komisyon*100)}%):</span>
                <span style="color: #667eea;">-{toplam_komisyon:,.0f}₺</span>
            </div>
            <div class="finansal-satir">
                <span>Komisyon Üzerinden KDV (20%):</span>
                <span style="color: #f5576c;">-{toplam_kdv:,.0f}₺</span>
            </div>
            <div class="finansal-satir">
                <span>Size Ödenecek Toplam:</span>
                <strong style="color: #10B981;">{toplam_odeme:,.0f}₺</strong>
            </div>
            <div class="finansal-satir">
                <span>Ödendi:</span>
                <span>-{toplam_odendi:,.0f}₺</span>
            </div>
            <div class="finansal-satir">
                <span>Kalan Bakiye:</span>
                <strong style="font-size: 24px; color: #667eea;">{bakiye:,.0f}₺</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='height: {FIBO['lg']}px'></div>", unsafe_allow_html=True)
        
        # Fatura talimatları
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
            st.markdown("### 📋 Müşterilerinize Fatura")
            st.markdown(f"""
            **Toplam Tutar:** {toplam_satis:,.2f}₺
            
            Müşterilerinize, ürün satış tutarlarının **tam tutarını** fatura etmelisiniz.
            Her sipariş için ayrı ayrı fatura kesilir.
            
            **Örnek:**
            - Sipariş tutarı 450₺ ise → Müşteriye 450₺ fatura
            - Tüm KDV dahildir
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_f2:
            st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
            st.markdown("### 📋 NATUVISIO'ya Fatura")
            st.markdown(f"""
            **Komisyon Tutarı:** {toplam_komisyon:,.2f}₺  
            **KDV (%20):** {toplam_kdv:,.2f}₺  
            **Toplam Fatura:** {toplam_komisyon + toplam_kdv:,.2f}₺
            
            Platform kullanım ücreti olarak NATUVISIO'ya **komisyon + KDV** tutarında fatura kesmeniz gerekmektedir.
            
            **Fatura Detayı:**
            - Hizmet: "NATUVISIO Platform Komisyonu"
            - Dönem: {datetime.now().strftime('%B %Y')}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Banka bilgileri
        st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
        st.markdown("### 🏦 Banka Bilgileri")
        st.markdown(f"""
        **IBAN:** {MARKALAR[marka]['iban']}  
        **Hesap Adı:** {MARKALAR[marka]['hesap_adi']}  
        **Vergi Dairesi:** {MARKALAR[marka]['vergi_dairesi']}  
        **Vergi No:** {MARKALAR[marka]['vergi_no']}
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Ödeme geçmişi
        if not odemelerim.empty:
            st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="cam-kart">', unsafe_allow_html=True)
            st.markdown("### 💳 Ödeme Geçmişi")
            st.dataframe(odemelerim[['Tarih', 'Tutar', 'Yontem', 'Referans', 'Notlar']],
                        use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

def partner_mesajlar():
    st.title("💬 Mesajlar")
    
    # Mesaj oluştur
    with st.expander("✉️ Admin'e Mesaj Gönder", expanded=False):
        konu = st.text_input("Konu")
        mesaj = st.text_area("Mesaj", height=150)
        siparis_ref = st.text_input("Sipariş No (opsiyonel)", placeholder="NV-12081530")
        
        if st.button("📤 Mesaj Gönder", use_container_width=True):
            if konu and mesaj:
                if mesaj_gonder(
                    st.session_state.kullanici_email,
                    "partner",
                    st.session_state.kullanici_marka,
                    "admin@natuvisio.com",
                    "admin",
                    "NATUVISIO",
                    konu,
                    mesaj,
                    siparis_ref
                ):
                    st.success("✅ Mesaj gönderildi!")
                    st.rerun()
    
    # Mesajları göster
    st.markdown("---")
    st.markdown("#### 📨 Mesaj Geçmişi")
    
    df_mesajlar = veri_yukle(CSV_MESSAGES)
    
    if df_mesajlar.empty:
        st.info("Henüz mesaj yok")
    else:
        mesajlarim = df_mesajlar[
            (df_mesajlar['Alici'] == st.session_state.kullanici_email) |
            (df_mesajlar['Gonderen'] == st.session_state.kullanici_email)
        ].sort_values('Tarih', ascending=False)
        
        for idx, msg in mesajlarim.iterrows():
            benden_mi = msg['Gonderen'] == st.session_state.kullanici_email
            kart_sinif = "mesaj-partner" if benden_mi else "mesaj-admin"
            
            st.markdown(f"""
            <div class="mesaj-karti {kart_sinif}">
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <div>
                        <strong style="font-size: 14px;">{"Kime: Admin" if benden_mi else "Kimden: Admin"}</strong>
                        {' <span class="okunmamis-rozet">YENİ</span>' if not benden_mi and msg['Okundu'] == 'Hayır' else ''}
                    </div>
                    <span style="font-size: 12px; color: #64748b;">{msg['Tarih']}</span>
                </div>
                <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #1e293b;">{msg['Konu']}</div>
                <div style="font-size: 13px; color: #475569;">{msg['Mesaj']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if not benden_mi and msg['Okundu'] == 'Hayır':
                if st.button("Okundu Olarak İşaretle", key=f"oku_{msg['Mesaj_ID']}"):
                    mesaj_okundu_isaretle(msg['Mesaj_ID'])
                    st.rerun()

# ============================================================================
# 10. ANA UYGULAMA
# ============================================================================

if __name__ == "__main__":
    if not st.session_state.giris_yapildi:
        giris_ekrani()
    else:
        if st.session_state.kullanici_rol == "admin":
            admin_panel()
        elif st.session_state.kullanici_rol == "partner":
            partner_panel()
