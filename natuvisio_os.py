import streamlit as st
import pandas as pd
import numpy as np
import os
import io
from datetime import datetime, timedelta
import urllib.parse
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================================
# 🏔️ NATUVISIO ULTIMATE PLATFORM v9.0
# Complete Enterprise System with Messaging, Financial Transparency & Premium UI
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Platform",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 1. CONFIGURATION
# ============================================================================

# Credentials
ADMIN_PASS = "admin2025"
PARTNER_CREDENTIALS = {
    "HAKI HEAL": {"email": "hakiheal@natuvisio.com", "password": "Hakiheal2025**"},
    "AURORACO": {"email": "auroraco@natuvisio.com", "password": "Auroraco**"},
    "LONGEVICALS": {"email": "longevicals@natuvisio.com", "password": "Longevicals2025"}
}

# File paths
CSV_ORDERS = "orders_master.csv"
CSV_FINANCE = "financial_ledger.csv"
CSV_PAYMENTS = "brand_payments.csv"
CSV_MESSAGES = "messages.csv"
CSV_LOGS = "system_logs.csv"

# Business constants
KDV_RATE = 0.20  # 20% VAT
PHI = 1.618  # Golden ratio
FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

# Brand configurations
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

# Assets
LOGO_URL = "https://res.cloudinary.com/deb1j92hy/image/upload/f_auto,q_auto/v1764805291/natuvisio_logo_gtqtfs.png"
BG_IMAGE = "https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp"

# ============================================================================
# 2. PREMIUM CSS SYSTEM
# ============================================================================

def load_premium_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* === GLOBAL THEME === */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        .stApp {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        /* === SIDEBAR === */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.98) 100%);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(0,0,0,0.05);
        }}
        
        [data-testid="stSidebar"] .css-1d391kg {{
            padding: 2rem 1rem;
        }}
        
        /* === GLASS MORPHISM CARDS === */
        .glass-card {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 20px;
            padding: {FIBO['lg']}px;
            margin-bottom: {FIBO['md']}px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .glass-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 48px rgba(31, 38, 135, 0.25);
        }}
        
        .glass-card-dark {{
            background: rgba(30, 41, 59, 0.85);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #ffffff;
        }}
        
        /* === PREMIUM METRICS === */
        .metric-premium {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px;
            padding: {FIBO['md']}px;
            text-align: center;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
        }}
        
        .metric-premium:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
        }}
        
        .metric-value {{
            font-size: 36px;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 8px;
        }}
        
        .metric-label {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.9;
        }}
        
        /* === FINANCIAL BREAKDOWN CARD === */
        .fin-breakdown {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 20px;
            padding: {FIBO['lg']}px;
            color: white;
            box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);
        }}
        
        .fin-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }}
        
        .fin-row:last-child {{
            border-bottom: none;
            padding-top: 16px;
            font-size: 20px;
            font-weight: 800;
        }}
        
        /* === MESSAGE CARDS === */
        .message-card {{
            background: white;
            border-radius: 16px;
            padding: {FIBO['md']}px;
            margin-bottom: {FIBO['sm']}px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.2s ease;
        }}
        
        .message-card:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
            transform: translateX(4px);
        }}
        
        .message-from-admin {{
            border-left-color: #4ECDC4;
        }}
        
        .message-from-partner {{
            border-left-color: #FF6B6B;
        }}
        
        .unread-badge {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            display: inline-block;
        }}
        
        /* === STATUS BADGES === */
        .status-badge {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
        }}
        
        .badge-pending {{
            background: rgba(251, 191, 36, 0.2);
            color: #92400e;
            border: 1.5px solid rgba(251, 191, 36, 0.5);
        }}
        
        .badge-notified {{
            background: rgba(59, 130, 246, 0.2);
            color: #1e40af;
            border: 1.5px solid rgba(59, 130, 246, 0.5);
        }}
        
        .badge-dispatched {{
            background: rgba(16, 185, 129, 0.2);
            color: #065f46;
            border: 1.5px solid rgba(16, 185, 129, 0.5);
        }}
        
        .badge-completed {{
            background: rgba(139, 92, 246, 0.2);
            color: #5b21b6;
            border: 1.5px solid rgba(139, 92, 246, 0.5);
        }}
        
        /* === BUTTONS === */
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
        
        /* === INPUTS === */
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
        
        /* === DATAFRAME === */
        .stDataFrame {{
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        }}
        
        /* === HIDE STREAMLIT BRANDING === */
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header {{ visibility: hidden; }}
        
        /* === CUSTOM SCROLLBAR === */
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
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }}
        
        /* === HEADINGS === */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            color: #1e293b !important;
        }}
        
        /* === WHATSAPP BUTTON === */
        .whatsapp-btn {{
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
        
        .whatsapp-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(37, 211, 102, 0.4);
        }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 3. DATABASE OPERATIONS
# ============================================================================

def init_databases():
    """Initialize all CSV databases with proper schemas"""
    schemas = {
        CSV_ORDERS: [
            "Order_ID", "Time", "Brand", "Customer", "Phone", "Address", "Items",
            "Total_Value", "Commission_Rate", "Commission_Amt", "KDV_Amt", 
            "Brand_Payout", "Status", "WhatsApp_Sent", "Tracking_Num", 
            "Priority", "Notes", "Created_By", "Last_Modified"
        ],
        CSV_FINANCE: [
            "Order_ID", "Time", "Brand", "Total_Sale", "Commission_Rate",
            "Commission_Amt", "KDV_Amt", "Total_Deduction", "Payable_To_Brand",
            "Invoice_Ref", "Payment_Status"
        ],
        CSV_PAYMENTS: [
            "Payment_ID", "Time", "Brand", "Amount", "Method", "Reference", "Notes"
        ],
        CSV_MESSAGES: [
            "Message_ID", "Time", "From_User", "From_Role", "To_User", "To_Role",
            "Subject", "Body", "Read", "Order_ID"
        ],
        CSV_LOGS: [
            "Log_ID", "Time", "Action", "User", "Order_ID", "Details"
        ]
    }
    
    for file, columns in schemas.items():
        if not os.path.exists(file):
            pd.DataFrame(columns=columns).to_csv(file, index=False)

def load_db(file):
    """Safely load database file"""
    try:
        if os.path.exists(file):
            return pd.read_csv(file)
    except:
        pass
    return pd.DataFrame()

def save_db(file, df):
    """Safely save database file"""
    try:
        df.to_csv(file, index=False)
        return True
    except:
        return False

def log_action(action, user, order_id, details):
    """Log all system actions for audit trail"""
    try:
        df = load_db(CSV_LOGS)
        log_entry = {
            'Log_ID': f"LOG-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Action': action,
            'User': user,
            'Order_ID': order_id,
            'Details': details
        }
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        save_db(CSV_LOGS, df)
    except:
        pass

# ============================================================================
# 4. MESSAGING SYSTEM
# ============================================================================

def send_message(from_user, from_role, to_user, to_role, subject, body, order_id=""):
    """Send message between admin and partners"""
    try:
        df = load_db(CSV_MESSAGES)
        message_data = {
            "Message_ID": f"MSG-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "From_User": from_user,
            "From_Role": from_role,
            "To_User": to_user,
            "To_Role": to_role,
            "Subject": subject,
            "Body": body,
            "Read": "No",
            "Order_ID": order_id
        }
        df = pd.concat([df, pd.DataFrame([message_data])], ignore_index=True)
        save_db(CSV_MESSAGES, df)
        log_action("MESSAGE_SENT", from_user, order_id, f"To: {to_user} - {subject}")
        return True
    except:
        return False

def mark_message_read(message_id):
    """Mark message as read"""
    try:
        df = load_db(CSV_MESSAGES)
        df.loc[df['Message_ID'] == message_id, 'Read'] = 'Yes'
        save_db(CSV_MESSAGES, df)
        return True
    except:
        return False

def get_unread_count(user_email):
    """Get unread message count for user"""
    df = load_db(CSV_MESSAGES)
    if df.empty:
        return 0
    unread = df[(df['To_User'] == user_email) & (df['Read'] == 'No')]
    return len(unread)

# ============================================================================
# 5. FINANCIAL CALCULATIONS
# ============================================================================

def calculate_financials(total_value, commission_rate):
    """Calculate complete financial breakdown"""
    commission_amt = total_value * commission_rate
    kdv_amt = commission_amt * KDV_RATE
    total_deduction = commission_amt + kdv_amt
    brand_payout = total_value - total_deduction
    
    return {
        'commission_amt': commission_amt,
        'kdv_amt': kdv_amt,
        'total_deduction': total_deduction,
        'brand_payout': brand_payout
    }

# ============================================================================
# 6. SESSION STATE
# ============================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_brand' not in st.session_state:
    st.session_state.user_brand = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'brand_lock' not in st.session_state:
    st.session_state.brand_lock = None

# ============================================================================
# 7. LOGIN SCREEN
# ============================================================================

def login_screen():
    load_premium_css()
    init_databases()
    
    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 50px 40px;">
            <img src="{LOGO_URL}" style="width: 100px; margin-bottom: 20px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));">
            <h1 style="margin: 0; font-size: 32px;">NATUVISIO</h1>
            <p style="color: #64748b; font-size: 14px; margin-top: 8px; font-weight: 500;">Ultimate Platform v9.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        login_type = st.radio("Select Login Type", ["👑 Admin", "🤝 Partner"], horizontal=True)
        
        if login_type == "👑 Admin":
            password = st.text_input("Admin Password", type="password", key="admin_pwd")
            
            if st.button("🔓 LOGIN AS ADMIN", use_container_width=True):
                if password == ADMIN_PASS:
                    st.session_state.logged_in = True
                    st.session_state.user_role = "admin"
                    st.session_state.user_email = "admin@natuvisio.com"
                    log_action("LOGIN", "admin", "", "Admin login successful")
                    st.rerun()
                else:
                    st.error("❌ Invalid password")
        
        else:
            brand = st.selectbox("Select Brand", list(PARTNER_CREDENTIALS.keys()))
            email = st.text_input("Email", value=PARTNER_CREDENTIALS[brand]["email"], disabled=True)
            password = st.text_input("Password", type="password", key="partner_pwd")
            
            if st.button("🔓 LOGIN AS PARTNER", use_container_width=True):
                if password == PARTNER_CREDENTIALS[brand]["password"]:
                    st.session_state.logged_in = True
                    st.session_state.user_role = "partner"
                    st.session_state.user_brand = brand
                    st.session_state.user_email = PARTNER_CREDENTIALS[brand]["email"]
                    log_action("LOGIN", email, "", f"{brand} partner login")
                    st.rerun()
                else:
                    st.error("❌ Invalid password")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 8. ADMIN DASHBOARD
# ============================================================================

def admin_dashboard():
    load_premium_css()
    
    # Sidebar
    with st.sidebar:
        st.image(LOGO_URL, width=60)
        st.markdown("### NATUVISIO HQ")
        st.markdown(f"**Role:** Master Admin")
        st.markdown(f"**Email:** {st.session_state.user_email}")
        
        unread = get_unread_count(st.session_state.user_email)
        if unread > 0:
            st.markdown(f'<span class="unread-badge">{unread} New Messages</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        menu = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "🚀 New Order",
                "📦 Operations",
                "💰 Financials",
                "💬 Messages",
                "📈 Analytics",
                "📜 Logs"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    
    # Main content
    df_orders = load_db(CSV_ORDERS)
    df_finance = load_db(CSV_FINANCE)
    
    # ========================================================================
    # DASHBOARD
    # ========================================================================
    if menu == "📊 Dashboard":
        st.title("📊 Command Center")
        
        # Metrics
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        total_orders = len(df_orders)
        total_revenue = df_finance['Total_Sale'].sum() if not df_finance.empty else 0
        total_commission = df_finance['Commission_Amt'].sum() if not df_finance.empty else 0
        pending = len(df_orders[df_orders['Status'] == 'Pending']) if not df_orders.empty else 0
        
        with col_m1:
            st.markdown(f"""
            <div class="metric-premium">
                <div class="metric-value">{total_orders}</div>
                <div class="metric-label">Total Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
            <div class="metric-premium" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-value">{total_revenue:,.0f}₺</div>
                <div class="metric-label">Revenue</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            st.markdown(f"""
            <div class="metric-premium" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-value">{total_commission:,.0f}₺</div>
                <div class="metric-label">Commission</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            st.markdown(f"""
            <div class="metric-premium" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                <div class="metric-value">{pending}</div>
                <div class="metric-label">Pending</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
        
        # Charts
        if not df_finance.empty:
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("#### 📊 Revenue by Brand")
                brand_revenue = df_finance.groupby('Brand')['Total_Sale'].sum().reset_index()
                fig = px.bar(brand_revenue, x='Brand', y='Total_Sale', 
                           color='Brand', template="plotly_white",
                           color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_c2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("#### 🎯 Status Distribution")
                if not df_orders.empty:
                    status_dist = df_orders['Status'].value_counts().reset_index()
                    status_dist.columns = ['Status', 'Count']
                    fig = px.pie(status_dist, values='Count', names='Status',
                               template="plotly_white",
                               color_discrete_sequence=px.colors.qualitative.Pastel)
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent orders
        if not df_orders.empty:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📋 Recent Orders")
            recent = df_orders.sort_values('Time', ascending=False).head(10)
            st.dataframe(recent[['Order_ID', 'Time', 'Brand', 'Customer', 'Total_Value', 'Status']], 
                        use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # NEW ORDER
    # ========================================================================
    elif menu == "🚀 New Order":
        st.title("🚀 Create New Order")
        
        col_form, col_cart = st.columns([1.5, 1])
        
        with col_form:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 👤 Customer Information")
            
            col_n, col_p = st.columns(2)
            with col_n:
                cust_name = st.text_input("Name")
            with col_p:
                cust_phone = st.text_input("Phone")
            
            cust_addr = st.text_area("Address", height=80)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🛒 Add Products")
            
            if st.session_state.cart:
                active_brand = st.session_state.brand_lock
                st.info(f"🔒 Brand locked: {active_brand}")
            else:
                active_brand = st.selectbox("Select Brand", list(BRANDS.keys()))
            
            brand_data = BRANDS[active_brand]
            products = list(brand_data["products"].keys())
            
            col_p, col_q = st.columns([3, 1])
            with col_p:
                prod = st.selectbox("Product", products)
            with col_q:
                qty = st.number_input("Qty", 1, value=1)
            
            prod_details = brand_data["products"][prod]
            line_total = prod_details['price'] * qty
            
            # Calculate financials
            financials = calculate_financials(line_total, brand_data['commission'])
            
            # Show preview
            st.markdown(f"""
            <div style="background: rgba(102, 126, 234, 0.1); border-radius: 12px; padding: 16px; margin-top: 16px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Product Total:</span>
                    <strong>{line_total:,.0f}₺</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Commission ({int(brand_data['commission']*100)}%):</span>
                    <span style="color: #667eea;">{financials['commission_amt']:,.0f}₺</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>KDV (20%):</span>
                    <span style="color: #f5576c;">{financials['kdv_amt']:,.0f}₺</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("➕ Add to Cart"):
                st.session_state.cart.append({
                    "brand": active_brand,
                    "product": prod,
                    "sku": prod_details['sku'],
                    "qty": qty,
                    "subtotal": line_total,
                    "commission": financials['commission_amt'],
                    "kdv": financials['kdv_amt'],
                    "payout": financials['brand_payout']
                })
                st.session_state.brand_lock = active_brand
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_cart:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📦 Cart Summary")
            
            if st.session_state.cart:
                for item in st.session_state.cart:
                    st.markdown(f"**{item['product']}** × {item['qty']} = {item['subtotal']:,.0f}₺")
                
                total = sum(i['subtotal'] for i in st.session_state.cart)
                total_comm = sum(i['commission'] for i in st.session_state.cart)
                total_kdv = sum(i['kdv'] for i in st.session_state.cart)
                total_payout = sum(i['payout'] for i in st.session_state.cart)
                
                st.markdown(f"""
                <div class="fin-breakdown" style="margin-top: 20px;">
                    <div class="fin-row">
                        <span>Order Total:</span>
                        <strong>{total:,.0f}₺</strong>
                    </div>
                    <div class="fin-row">
                        <span>Commission:</span>
                        <span>{total_comm:,.0f}₺</span>
                    </div>
                    <div class="fin-row">
                        <span>KDV (20%):</span>
                        <span>{total_kdv:,.0f}₺</span>
                    </div>
                    <div class="fin-row">
                        <span>Brand Payout:</span>
                        <strong>{total_payout:,.0f}₺</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                priority = st.selectbox("Priority", ["Standard", "🚨 Urgent", "🧊 Cold"])
                
                if st.button("⚡ CREATE ORDER", type="primary", use_container_width=True):
                    if cust_name and cust_phone:
                        order_id = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
                        items_str = ", ".join([f"{i['product']} (x{i['qty']})" for i in st.session_state.cart])
                        
                        # Save order
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
                            'KDV_Amt': total_kdv,
                            'Brand_Payout': total_payout,
                            'Status': 'Pending',
                            'WhatsApp_Sent': 'NO',
                            'Tracking_Num': '',
                            'Priority': priority,
                            'Notes': '',
                            'Created_By': 'admin',
                            'Last_Modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        df_orders = load_db(CSV_ORDERS)
                        df_orders = pd.concat([df_orders, pd.DataFrame([order_data])], ignore_index=True)
                        save_db(CSV_ORDERS, df_orders)
                        
                        # Save financial record
                        finance_data = {
                            'Order_ID': order_id,
                            'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'Brand': st.session_state.brand_lock,
                            'Total_Sale': total,
                            'Commission_Rate': BRANDS[st.session_state.brand_lock]['commission'],
                            'Commission_Amt': total_comm,
                            'KDV_Amt': total_kdv,
                            'Total_Deduction': total_comm + total_kdv,
                            'Payable_To_Brand': total_payout,
                            'Invoice_Ref': '',
                            'Payment_Status': 'Unpaid'
                        }
                        
                        df_finance = load_db(CSV_FINANCE)
                        df_finance = pd.concat([df_finance, pd.DataFrame([finance_data])], ignore_index=True)
                        save_db(CSV_FINANCE, df_finance)
                        
                        log_action("CREATE_ORDER", "admin", order_id, f"Created {order_id}")
                        
                        st.success(f"✅ Order {order_id} created successfully!")
                        st.session_state.cart = []
                        st.session_state.brand_lock = None
                        st.rerun()
                    else:
                        st.error("Please fill customer details!")
                
                if st.button("🗑️ Clear Cart"):
                    st.session_state.cart = []
                    st.session_state.brand_lock = None
                    st.rerun()
            else:
                st.info("Cart is empty")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # OPERATIONS
    # ========================================================================
    elif menu == "📦 Operations":
        st.title("📦 Operations Center")
        
        # Pending notifications
        pending_notify = df_orders[df_orders['WhatsApp_Sent'] == 'NO']
        
        if not pending_notify.empty:
            st.markdown(f'<div class="glass-card" style="border-left: 4px solid #EF4444;">', unsafe_allow_html=True)
            st.markdown(f"#### ⚠️ {len(pending_notify)} Orders Need Notification")
            
            for idx, row in pending_notify.iterrows():
                with st.expander(f"🔴 {row['Order_ID']} - {row['Brand']} - {row['Customer']}", expanded=True):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"""
                        **Items:** {row['Items']}  
                        **Phone:** {row['Phone']}  
                        **Address:** {row['Address']}  
                        **Total:** {row['Total_Value']:,.0f}₺
                        """)
                    
                    with col2:
                        phone = BRANDS[row['Brand']]['phone']
                        msg = f"YENİ SİPARİŞ: {row['Order_ID']}\n\n{row['Items']}\n\nMüşteri: {row['Customer']}\nTelefon: {row['Phone']}\nAdres: {row['Address']}\n\nTutar: {row['Total_Value']:,.0f}₺"
                        link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                        
                        st.markdown(f'<a href="{link}" target="_blank" class="whatsapp-btn">📲 Send WhatsApp</a>', unsafe_allow_html=True)
                        
                        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
                        
                        if st.button("✅ Mark as Notified", key=f"notify_{idx}"):
                            df_orders.at[idx, 'WhatsApp_Sent'] = 'YES'
                            df_orders.at[idx, 'Status'] = 'Notified'
                            save_db(CSV_ORDERS, df_orders)
                            log_action("NOTIFIED", "admin", row['Order_ID'], "Marked as notified")
                            st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("✅ All orders have been notified!")
        
        # Tracking entry
        st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
        
        pending_tracking = df_orders[(df_orders['Status'] == 'Notified') & ((df_orders['Tracking_Num'].isna()) | (df_orders['Tracking_Num'] == ''))]
        
        if not pending_tracking.empty:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"#### 📦 {len(pending_tracking)} Orders Need Tracking")
            
            for idx, row in pending_tracking.iterrows():
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{row['Order_ID']}** - {row['Brand']}")
                
                with col2:
                    tracking = st.text_input("Tracking Number", key=f"track_{idx}", label_visibility="collapsed")
                
                with col3:
                    if st.button("📦 Ship", key=f"ship_{idx}"):
                        if tracking:
                            df_orders.at[idx, 'Tracking_Num'] = tracking
                            df_orders.at[idx, 'Status'] = 'Dispatched'
                            save_db(CSV_ORDERS, df_orders)
                            log_action("DISPATCH", "admin", row['Order_ID'], f"Tracking: {tracking}")
                            st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # FINANCIALS
    # ========================================================================
    elif menu == "💰 Financials":
        st.title("💰 Financial Management")
        
        tabs = st.tabs(["💵 Brand Payouts", "📊 Summary"])
        
        with tabs[0]:
            for brand in BRANDS.keys():
                brand_finance = df_finance[df_finance['Brand'] == brand]
                
                if not brand_finance.empty:
                    total_sales = brand_finance['Total_Sale'].sum()
                    total_commission = brand_finance['Commission_Amt'].sum()
                    total_kdv = brand_finance['KDV_Amt'].sum()
                    total_payout = brand_finance['Payable_To_Brand'].sum()
                    
                    df_payments = load_db(CSV_PAYMENTS)
                    brand_payments = df_payments[df_payments['Brand'] == brand]
                    total_paid = brand_payments['Amount'].sum() if not brand_payments.empty else 0
                    balance = total_payout - total_paid
                    
                    with st.expander(f"🏦 {brand} - Balance: {balance:,.0f}₺", expanded=True):
                        col1, col2 = st.columns([1, 1.5])
                        
                        with col1:
                            st.markdown(f"""
                            <div class="fin-breakdown">
                                <div class="fin-row">
                                    <span>Total Sales:</span>
                                    <strong>{total_sales:,.0f}₺</strong>
                                </div>
                                <div class="fin-row">
                                    <span>Commission:</span>
                                    <span>-{total_commission:,.0f}₺</span>
                                </div>
                                <div class="fin-row">
                                    <span>KDV (20%):</span>
                                    <span>-{total_kdv:,.0f}₺</span>
                                </div>
                                <div class="fin-row">
                                    <span>Total Payable:</span>
                                    <strong>{total_payout:,.0f}₺</strong>
                                </div>
                                <div class="fin-row">
                                    <span>Already Paid:</span>
                                    <span>-{total_paid:,.0f}₺</span>
                                </div>
                                <div class="fin-row">
                                    <span>Outstanding:</span>
                                    <strong>{balance:,.0f}₺</strong>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"**IBAN:** {BRANDS[brand]['iban']}")
                            st.markdown(f"**Account:** {BRANDS[brand]['account_name']}")
                        
                        with col2:
                            st.markdown("**Record Payment**")
                            
                            amount = st.number_input("Amount", min_value=0.0, max_value=float(balance) if balance > 0 else 0.0, key=f"amt_{brand}")
                            method = st.selectbox("Method", ["Bank Transfer", "Cash", "Other"], key=f"method_{brand}")
                            reference = st.text_input("Reference", key=f"ref_{brand}")
                            
                            if st.button(f"💰 Record Payment for {brand}", key=f"pay_{brand}"):
                                if amount > 0:
                                    payment_data = {
                                        'Payment_ID': f"PAY-{datetime.now().strftime('%m%d%H%M%S')}",
                                        'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                        'Brand': brand,
                                        'Amount': amount,
                                        'Method': method,
                                        'Reference': reference,
                                        'Notes': f"Payment recorded by admin"
                                    }
                                    
                                    df_payments = load_db(CSV_PAYMENTS)
                                    df_payments = pd.concat([df_payments, pd.DataFrame([payment_data])], ignore_index=True)
                                    save_db(CSV_PAYMENTS, df_payments)
                                    
                                    log_action("PAYMENT", "admin", "", f"{brand} - {amount}₺")
                                    
                                    st.success(f"✅ Payment of {amount:,.0f}₺ recorded for {brand}!")
                                    st.rerun()
        
        with tabs[1]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📊 Financial Summary")
            
            if not df_finance.empty:
                summary_data = []
                
                for brand in BRANDS.keys():
                    brand_finance = df_finance[df_finance['Brand'] == brand]
                    
                    if not brand_finance.empty:
                        df_payments = load_db(CSV_PAYMENTS)
                        brand_payments = df_payments[df_payments['Brand'] == brand]
                        
                        summary_data.append({
                            'Brand': brand,
                            'Total Sales': brand_finance['Total_Sale'].sum(),
                            'Commission': brand_finance['Commission_Amt'].sum(),
                            'KDV': brand_finance['KDV_Amt'].sum(),
                            'Payable': brand_finance['Payable_To_Brand'].sum(),
                            'Paid': brand_payments['Amount'].sum() if not brand_payments.empty else 0,
                            'Balance': brand_finance['Payable_To_Brand'].sum() - (brand_payments['Amount'].sum() if not brand_payments.empty else 0)
                        })
                
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # MESSAGES
    # ========================================================================
    elif menu == "💬 Messages":
        st.title("💬 Message Center")
        
        # Compose message
        with st.expander("✉️ Send New Message", expanded=False):
            recipient_brand = st.selectbox("To Brand", list(BRANDS.keys()))
            subject = st.text_input("Subject")
            body = st.text_area("Message", height=150)
            
            if st.button("📤 Send Message"):
                if subject and body:
                    recipient_email = PARTNER_CREDENTIALS[recipient_brand]["email"]
                    
                    if send_message(
                        st.session_state.user_email,
                        "admin",
                        recipient_email,
                        "partner",
                        subject,
                        body
                    ):
                        st.success("Message sent successfully!")
                        st.rerun()
        
        # Display messages
        st.markdown("---")
        st.markdown("#### 📨 Message History")
        
        df_messages = load_db(CSV_MESSAGES)
        
        if df_messages.empty:
            st.info("No messages yet")
        else:
            my_messages = df_messages[
                (df_messages['To_User'] == st.session_state.user_email) |
                (df_messages['From_User'] == st.session_state.user_email)
            ].sort_values('Time', ascending=False)
            
            for idx, msg in my_messages.iterrows():
                is_from_me = msg['From_User'] == st.session_state.user_email
                card_class = "message-from-admin" if is_from_me else "message-from-partner"
                
                st.markdown(f"""
                <div class="message-card {card_class}">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                        <div>
                            <strong style="font-size: 14px;">{"To: " + msg['To_User'] if is_from_me else "From: " + msg['From_User']}</strong>
                            {' <span class="unread-badge">NEW</span>' if not is_from_me and msg['Read'] == 'No' else ''}
                        </div>
                        <span style="font-size: 12px; color: #64748b;">{msg['Time']}</span>
                    </div>
                    <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #1e293b;">{msg['Subject']}</div>
                    <div style="font-size: 13px; color: #475569;">{msg['Body']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if not is_from_me and msg['Read'] == 'No':
                    if st.button("Mark as Read", key=f"read_{msg['Message_ID']}"):
                        mark_message_read(msg['Message_ID'])
                        st.rerun()
    
    # ========================================================================
    # ANALYTICS
    # ========================================================================
    elif menu == "📈 Analytics":
        st.title("📈 Business Analytics")
        
        if not df_finance.empty and not df_orders.empty:
            # Time series
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📅 Sales Over Time")
            
            df_orders_copy = df_orders.copy()
            df_orders_copy['Date'] = pd.to_datetime(df_orders_copy['Time']).dt.date
            daily_sales = df_orders_copy.groupby('Date')['Total_Value'].sum().reset_index()
            
            fig = px.line(daily_sales, x='Date', y='Total_Value', 
                         template="plotly_white",
                         labels={'Total_Value': 'Revenue (₺)', 'Date': 'Date'})
            fig.update_traces(line_color='#667eea', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Brand comparison
            col_a1, col_a2 = st.columns(2)
            
            with col_a1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("#### 🏆 Brand Performance")
                
                brand_stats = df_finance.groupby('Brand').agg({
                    'Total_Sale': 'sum',
                    'Commission_Amt': 'sum'
                }).reset_index()
                
                fig = px.bar(brand_stats, x='Brand', y=['Total_Sale', 'Commission_Amt'],
                           barmode='group', template="plotly_white",
                           color_discrete_sequence=['#667eea', '#f5576c'])
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_a2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("#### 🎯 Order Status")
                
                status_dist = df_orders['Status'].value_counts().reset_index()
                status_dist.columns = ['Status', 'Count']
                
                fig = px.pie(status_dist, values='Count', names='Status',
                           template="plotly_white",
                           color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Not enough data for analytics yet")
    
    # ========================================================================
    # LOGS
    # ========================================================================
    elif menu == "📜 Logs":
        st.title("📜 System Logs")
        
        df_logs = load_db(CSV_LOGS)
        
        if df_logs.empty:
            st.info("No logs yet")
        else:
            # Filters
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                users = df_logs['User'].unique().tolist()
                user_filter = st.multiselect("Filter by User", users)
            
            with col_f2:
                actions = df_logs['Action'].unique().tolist()
                action_filter = st.multiselect("Filter by Action", actions)
            
            filtered_logs = df_logs.copy()
            
            if user_filter:
                filtered_logs = filtered_logs[filtered_logs['User'].isin(user_filter)]
            
            if action_filter:
                filtered_logs = filtered_logs[filtered_logs['Action'].isin(action_filter)]
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.dataframe(filtered_logs.sort_values('Time', ascending=False), 
                        use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 9. PARTNER DASHBOARD
# ============================================================================

def partner_dashboard():
    load_premium_css()
    
    brand = st.session_state.user_brand
    brand_color = BRANDS[brand]['color']
    
    # Sidebar
    with st.sidebar:
        st.image(LOGO_URL, width=60)
        st.markdown(f"### {brand}")
        st.markdown(f"**Email:** {st.session_state.user_email}")
        
        unread = get_unread_count(st.session_state.user_email)
        if unread > 0:
            st.markdown(f'<span class="unread-badge">{unread} New Messages</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        menu = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "📥 New Orders",
                "🚚 Shipping",
                "✅ Completed",
                "💰 Financials",
                "💬 Messages"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    
    # Load data
    df_orders = load_db(CSV_ORDERS)
    df_finance = load_db(CSV_FINANCE)
    
    my_orders = df_orders[df_orders['Brand'] == brand]
    my_finance = df_finance[df_finance['Brand'] == brand]
    
    # ========================================================================
    # DASHBOARD
    # ========================================================================
    if menu == "📊 Dashboard":
        st.title(f"📊 {brand} Dashboard")
        
        # Metrics
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        total_orders = len(my_orders)
        pending_orders = len(my_orders[my_orders['Status'] == 'Pending'])
        completed_orders = len(my_orders[my_orders['Status'] == 'Completed'])
        
        total_earnings = my_finance['Payable_To_Brand'].sum() if not my_finance.empty else 0
        
        with col_m1:
            st.markdown(f"""
            <div class="metric-premium">
                <div class="metric-value">{total_orders}</div>
                <div class="metric-label">Total Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
            <div class="metric-premium" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                <div class="metric-value">{pending_orders}</div>
                <div class="metric-label">Pending</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            st.markdown(f"""
            <div class="metric-premium" style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);">
                <div class="metric-value">{completed_orders}</div>
                <div class="metric-label">Completed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            st.markdown(f"""
            <div class="metric-premium" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: #1e293b;">
                <div class="metric-value">{total_earnings:,.0f}₺</div>
                <div class="metric-label">Total Earnings</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
        
        # Recent orders
        if not my_orders.empty:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📋 Recent Orders")
            
            recent = my_orders.sort_values('Time', ascending=False).head(10)
            st.dataframe(recent[['Order_ID', 'Time', 'Customer', 'Total_Value', 'Status', 'Tracking_Num']], 
                        use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # NEW ORDERS
    # ========================================================================
    elif menu == "📥 New Orders":
        st.title("📥 New Orders")
        
        pending = my_orders[my_orders['Status'] == 'Pending']
        
        if pending.empty:
            st.success("✅ No pending orders!")
        else:
            for idx, row in pending.iterrows():
                st.markdown('<div class="glass-card" style="border-left: 4px solid #EF4444;">', unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"### 🆕 {row['Order_ID']}")
                    st.markdown(f"**Customer:** {row['Customer']}")
                    st.markdown(f"**Phone:** {row['Phone']}")
                    st.markdown(f"**Address:** {row['Address']}")
                    st.markdown(f"**Items:** {row['Items']}")
                
                with col2:
                    st.markdown(f"""
                    <div class="fin-breakdown">
                        <div class="fin-row">
                            <span>Order Total:</span>
                            <strong>{row['Total_Value']:,.0f}₺</strong>
                        </div>
                        <div class="fin-row">
                            <span>Commission:</span>
                            <span>-{row['Commission_Amt']:,.0f}₺</span>
                        </div>
                        <div class="fin-row">
                            <span>KDV (20%):</span>
                            <span>-{row['KDV_Amt']:,.0f}₺</span>
                        </div>
                        <div class="fin-row">
                            <span>Your Payout:</span>
                            <strong style="color: #10B981;">{row['Brand_Payout']:,.0f}₺</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
                    
                    if row['WhatsApp_Sent'] == 'YES':
                        st.success("✅ Notified via WhatsApp")
                    else:
                        st.warning("⏳ Awaiting WhatsApp notification from admin")
                    
                    if st.button("✅ Accept Order", key=f"accept_{idx}"):
                        df_orders.at[idx, 'Status'] = 'Notified'
                        save_db(CSV_ORDERS, df_orders)
                        log_action("ORDER_ACCEPTED", st.session_state.user_email, row['Order_ID'], "Order accepted by partner")
                        st.success("Order accepted!")
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # SHIPPING
    # ========================================================================
    elif menu == "🚚 Shipping":
        st.title("🚚 Shipping Management")
        
        to_ship = my_orders[my_orders['Status'] == 'Notified']
        
        if to_ship.empty:
            st.info("No orders to ship")
        else:
            for idx, row in to_ship.iterrows():
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                
                st.markdown(f"### 📦 {row['Order_ID']}")
                st.markdown(f"**Customer:** {row['Customer']} - {row['Phone']}")
                st.markdown(f"**Items:** {row['Items']}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    tracking = st.text_input("Tracking Number", key=f"track_{idx}")
                    courier = st.selectbox("Courier", ["Yurtiçi", "Aras", "MNG", "PTT", "Other"], key=f"courier_{idx}")
                
                with col2:
                    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
                    if st.button("🚀 Mark as Shipped", key=f"ship_{idx}"):
                        if tracking:
                            df_orders.at[idx, 'Status'] = 'Dispatched'
                            df_orders.at[idx, 'Tracking_Num'] = f"{courier} - {tracking}"
                            save_db(CSV_ORDERS, df_orders)
                            log_action("ORDER_SHIPPED", st.session_state.user_email, row['Order_ID'], f"Shipped via {courier}")
                            st.success("Order marked as shipped!")
                            st.rerun()
                        else:
                            st.error("Please enter tracking number")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # COMPLETED
    # ========================================================================
    elif menu == "✅ Completed":
        st.title("✅ Completed Orders")
        
        completed = my_orders[my_orders['Status'].isin(['Dispatched', 'Completed'])]
        
        if completed.empty:
            st.info("No completed orders yet")
        else:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.dataframe(completed[['Order_ID', 'Time', 'Customer', 'Items', 'Total_Value', 'Brand_Payout', 'Status', 'Tracking_Num']], 
                        use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # FINANCIALS
    # ========================================================================
    elif menu == "💰 Financials":
        st.title("💰 Financial Overview")
        
        if my_finance.empty:
            st.info("No financial data yet")
        else:
            total_sales = my_finance['Total_Sale'].sum()
            total_commission = my_finance['Commission_Amt'].sum()
            total_kdv = my_finance['KDV_Amt'].sum()
            total_payable = my_finance['Payable_To_Brand'].sum()
            
            df_payments = load_db(CSV_PAYMENTS)
            my_payments = df_payments[df_payments['Brand'] == brand]
            total_paid = my_payments['Amount'].sum() if not my_payments.empty else 0
            balance = total_payable - total_paid
            
            # Summary card
            st.markdown(f"""
            <div class="fin-breakdown" style="max-width: 600px; margin: 0 auto;">
                <h3 style="margin-bottom: 20px; text-align: center;">Financial Breakdown</h3>
                <div class="fin-row">
                    <span>Total Sales:</span>
                    <strong>{total_sales:,.0f}₺</strong>
                </div>
                <div class="fin-row">
                    <span>NATUVISIO Commission ({int(BRANDS[brand]['commission']*100)}%):</span>
                    <span style="color: #667eea;">-{total_commission:,.0f}₺</span>
                </div>
                <div class="fin-row">
                    <span>KDV on Commission (20%):</span>
                    <span style="color: #f5576c;">-{total_kdv:,.0f}₺</span>
                </div>
                <div class="fin-row">
                    <span>Total Payable to You:</span>
                    <strong style="color: #10B981;">{total_payable:,.0f}₺</strong>
                </div>
                <div class="fin-row">
                    <span>Already Paid:</span>
                    <span>-{total_paid:,.0f}₺</span>
                </div>
                <div class="fin-row">
                    <span>Outstanding Balance:</span>
                    <strong style="font-size: 24px; color: #667eea;">{balance:,.0f}₺</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<div style='height: {FIBO['lg']}px'></div>", unsafe_allow_html=True)
            
            # Instructions
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Invoice Instructions")
            st.markdown(f"""
            **To NATUVISIO (Your Commission Invoice):**
            - Amount: **{total_commission + total_kdv:,.2f}₺** (Commission + KDV)
            - Breakdown: {total_commission:,.2f}₺ (Commission) + {total_kdv:,.2f}₺ (20% KDV)
            - Description: "NATUVISIO platform commission for {brand} orders"
            
            **To Your Customers (Product Invoices):**
            - You should issue invoices for the **full product amounts** to your customers
            - Total customer invoices: **{total_sales:,.0f}₺**
            - Each order's full value should be invoiced to the respective customer
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Payment history
            if not my_payments.empty:
                st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 💳 Payment History")
                st.dataframe(my_payments[['Time', 'Amount', 'Method', 'Reference', 'Notes']], 
                            use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # MESSAGES
    # ========================================================================
    elif menu == "💬 Messages":
        st.title("💬 Messages")
        
        # Compose message
        with st.expander("✉️ Send Message to Admin", expanded=False):
            subject = st.text_input("Subject")
            body = st.text_area("Message", height=150)
            
            if st.button("📤 Send Message"):
                if subject and body:
                    if send_message(
                        st.session_state.user_email,
                        "partner",
                        "admin@natuvisio.com",
                        "admin",
                        subject,
                        body
                    ):
                        st.success("Message sent!")
                        st.rerun()
        
        # Display messages
        st.markdown("---")
        st.markdown("#### 📨 Message History")
        
        df_messages = load_db(CSV_MESSAGES)
        
        if df_messages.empty:
            st.info("No messages yet")
        else:
            my_messages = df_messages[
                (df_messages['To_User'] == st.session_state.user_email) |
                (df_messages['From_User'] == st.session_state.user_email)
            ].sort_values('Time', ascending=False)
            
            for idx, msg in my_messages.iterrows():
                is_from_me = msg['From_User'] == st.session_state.user_email
                card_class = "message-from-partner" if is_from_me else "message-from-admin"
                
                st.markdown(f"""
                <div class="message-card {card_class}">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                        <div>
                            <strong style="font-size: 14px;">{"To: Admin" if is_from_me else "From: Admin"}</strong>
                            {' <span class="unread-badge">NEW</span>' if not is_from_me and msg['Read'] == 'No' else ''}
                        </div>
                        <span style="font-size: 12px; color: #64748b;">{msg['Time']}</span>
                    </div>
                    <div style="font-size: 15px; font-weight: 600; margin-bottom: 8px; color: #1e293b;">{msg['Subject']}</div>
                    <div style="font-size: 13px; color: #475569;">{msg['Body']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if not is_from_me and msg['Read'] == 'No':
                    if st.button("Mark as Read", key=f"read_{msg['Message_ID']}"):
                        mark_message_read(msg['Message_ID'])
                        st.rerun()

# ============================================================================
# 10. MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_screen()
    else:
        if st.session_state.user_role == "admin":
            admin_dashboard()
        elif st.session_state.user_role == "partner":
            partner_dashboard()
