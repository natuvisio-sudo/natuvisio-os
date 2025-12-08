import streamlit as st
import pandas as pd
import numpy as np
import os
import io
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO MULTI-USER SYSTEM v8.0
# Complete Role-Based Platform: Admin | Partners | Dietitian
# Dependencies: streamlit, pandas, numpy ONLY
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Platform",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 1. CONFIGURATION
# ============================================================================

# Passwords
ADMIN_PASS = "admin2025"
USER_CREDENTIALS = {
    "hakiheal@natuvisio.com": {"password": "Hakiheal2025**", "role": "partner", "brand": "HAKI HEAL"},
    "auroraco@natuvisio.com": {"password": "Auroraco**", "role": "partner", "brand": "AURORACO"},
    "juliana@natuvisio.com": {"password": "Juliana2025.", "role": "dietitian", "brand": "DRJULIANA"}
}

# Files
CSV_ORDERS = "orders_complete.csv"
CSV_PAYMENTS = "brand_payments.csv"
CSV_LOGS = "system_logs.csv"
CSV_PARTNERS = "partners.csv"
CSV_MESSAGES = "messages.csv"
CSV_STOCK = "stock_inventory.csv"

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
        "products": {
            "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
            "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
        }
    },
    "DRJULIANA": {
        "phone": "601158976276",
        "color": "#A78BFA",
        "commission": 0.25,
        "iban": "TR90 0001 7000 0000 3344 5566 77",
        "products": {
            "CONSULTATION": {"sku": "SKU-JUL-CONSULT", "price": 1500},
            "DIET PLAN": {"sku": "SKU-JUL-DIET", "price": 2500},
            "FOLLOW-UP": {"sku": "SKU-JUL-FOLLOW", "price": 800}
        }
    }
}

# ============================================================================
# 2. ICONS
# ============================================================================

def get_icon(name, color="#ffffff", size=24):
    icons = {
        "mountain": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M3 20L9 8L12 14L15 6L21 20H3Z"/></svg>',
        "alert": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3"><path d="M20 6L9 17L4 12"/></svg>',
        "message": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
        "box": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',
        "user": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
        "clock": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "activity": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
    }
    return icons.get(name, "")

# ============================================================================
# 3. CSS
# ============================================================================

def load_css(theme="dark"):
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        .stApp {{
            background-image: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.92)), 
                              url("{BG_IMAGE}");
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }}
        
        .glass-card {{
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur({FIBO['md']}px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: {FIBO['sm']}px;
            padding: {FIBO['md']}px;
            margin-bottom: {FIBO['sm']}px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }}
        
        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 48px rgba(0,0,0,0.4);
        }}
        
        .alert-card {{
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #EF4444;
            animation: pulse-red 2s infinite;
        }}
        
        @keyframes pulse-red {{
            0%, 100% {{ box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }}
            50% {{ box-shadow: 0 0 40px rgba(239, 68, 68, 0.5); }}
        }}
        
        .metric-value {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: {FIBO['lg']}px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: {FIBO['xs']}px;
        }}
        
        .metric-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: rgba(255,255,255,0.6);
            font-weight: 600;
        }}
        
        .message-card {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 13px;
            margin-bottom: 8px;
        }}
        
        .message-from-admin {{
            border-left: 3px solid #4ECDC4;
        }}
        
        .message-from-user {{
            border-left: 3px solid #A78BFA;
        }}
        
        .unread-badge {{
            background: #EF4444;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }}
        
        h1, h2, h3, h4 {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: #ffffff !important;
            font-weight: 700 !important;
        }}
        
        div.stButton > button {{
            background: linear-gradient(135deg, #4ECDC4, #44A08D) !important;
            color: white !important;
            border: none !important;
            padding: {FIBO['sm']}px {FIBO['md']}px !important;
            border-radius: {FIBO['xs']}px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            transition: all 0.3s ease !important;
        }}
        
        div.stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(78, 205, 196, 0.4);
        }}
        
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {{
            background: rgba(0,0,0,0.3) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            color: #ffffff !important;
            border-radius: {FIBO['xs']}px !important;
        }}
        
        #MainMenu, header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 4. DATABASE INITIALIZATION
# ============================================================================

def init_databases():
    # Orders
    if not os.path.exists(CSV_ORDERS):
        pd.DataFrame(columns=[
            "Order_ID", "Time", "Brand", "Customer", "Phone", "Address",
            "Items", "Total_Value", "Commission_Rate", "Commission_Amt",
            "Brand_Payout", "Status", "WhatsApp_Sent", "Tracking_Num",
            "Priority", "Notes", "Created_By", "Last_Modified"
        ]).to_csv(CSV_ORDERS, index=False)
    
    # Payments
    if not os.path.exists(CSV_PAYMENTS):
        pd.DataFrame(columns=[
            "Payment_ID", "Time", "Brand", "Amount", "Method", "Reference", "Notes"
        ]).to_csv(CSV_PAYMENTS, index=False)
    
    # Logs
    if not os.path.exists(CSV_LOGS):
        pd.DataFrame(columns=[
            "Log_ID", "Time", "Action", "User", "Order_ID", "Details"
        ]).to_csv(CSV_LOGS, index=False)
    
    # Partners
    if not os.path.exists(CSV_PARTNERS):
        partners_data = []
        for email, data in USER_CREDENTIALS.items():
            partners_data.append({
                "Email": email,
                "Password": data["password"],
                "Role": data["role"],
                "Brand": data["brand"],
                "Status": "Active",
                "Created": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        pd.DataFrame(partners_data).to_csv(CSV_PARTNERS, index=False)
    
    # Messages
    if not os.path.exists(CSV_MESSAGES):
        pd.DataFrame(columns=[
            "Message_ID", "Time", "From_User", "From_Role", "To_User", 
            "To_Role", "Subject", "Body", "Read", "Order_ID"
        ]).to_csv(CSV_MESSAGES, index=False)
    
    # Stock Inventory (for dietitian)
    if not os.path.exists(CSV_STOCK):
        pd.DataFrame(columns=[
            "Stock_ID", "Time", "Product", "Action", "Quantity", 
            "Balance", "Notes", "Updated_By"
        ]).to_csv(CSV_STOCK, index=False)

# ============================================================================
# 5. DATABASE OPERATIONS
# ============================================================================

def load_orders():
    try:
        if os.path.exists(CSV_ORDERS):
            return pd.read_csv(CSV_ORDERS)
    except: pass
    return pd.DataFrame()

def save_order(order_data):
    try:
        df = load_orders()
        df = pd.concat([df, pd.DataFrame([order_data])], ignore_index=True)
        df.to_csv(CSV_ORDERS, index=False)
        log_action("CREATE_ORDER", st.session_state.get('user_email', 'admin'), order_data['Order_ID'], f"Created {order_data['Order_ID']}")
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def update_orders(df):
    try:
        df.to_csv(CSV_ORDERS, index=False)
        return True
    except: return False

def load_payments():
    try:
        if os.path.exists(CSV_PAYMENTS):
            return pd.read_csv(CSV_PAYMENTS)
    except: pass
    return pd.DataFrame()

def load_messages():
    try:
        if os.path.exists(CSV_MESSAGES):
            return pd.read_csv(CSV_MESSAGES)
    except: pass
    return pd.DataFrame()

def send_message(from_user, from_role, to_user, to_role, subject, body, order_id=""):
    try:
        df = load_messages()
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
        df.to_csv(CSV_MESSAGES, index=False)
        log_action("MESSAGE_SENT", from_user, order_id, f"To: {to_user}")
        return True
    except:
        return False

def mark_message_read(message_id):
    try:
        df = load_messages()
        df.loc[df['Message_ID'] == message_id, 'Read'] = 'Yes'
        df.to_csv(CSV_MESSAGES, index=False)
        return True
    except:
        return False

def get_unread_count(user_email):
    df = load_messages()
    if df.empty:
        return 0
    unread = df[(df['To_User'] == user_email) & (df['Read'] == 'No')]
    return len(unread)

def load_stock():
    try:
        if os.path.exists(CSV_STOCK):
            return pd.read_csv(CSV_STOCK)
    except: pass
    return pd.DataFrame()

def update_stock(product, action, quantity, notes=""):
    try:
        df = load_stock()
        current_balance = 0
        if not df.empty:
            product_stock = df[df['Product'] == product]
            if not product_stock.empty:
                current_balance = product_stock.iloc[-1]['Balance']
        
        if action == "ADD":
            new_balance = current_balance + quantity
        elif action == "REMOVE":
            new_balance = current_balance - quantity
        else:
            new_balance = current_balance
        
        stock_data = {
            "Stock_ID": f"STK-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Product": product,
            "Action": action,
            "Quantity": quantity,
            "Balance": new_balance,
            "Notes": notes,
            "Updated_By": st.session_state.get('user_email', 'system')
        }
        df = pd.concat([df, pd.DataFrame([stock_data])], ignore_index=True)
        df.to_csv(CSV_STOCK, index=False)
        log_action("STOCK_UPDATE", st.session_state.get('user_email', 'system'), "", f"{action} {quantity} {product}")
        return True
    except:
        return False

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
    load_css()
    init_databases()
    
    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:20px;">
            <img src="{LOGO_URL}" style="width:120px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">
            <h1 style="margin-top:10px;">NATUVISIO</h1>
            <p style="opacity: 0.6; font-size: 12px;">MULTI-USER PLATFORM</p>
        </div>
        """, unsafe_allow_html=True)
        
        login_type = st.radio("Select Login Type", ["Admin", "Partner/Dietitian"], horizontal=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        if login_type == "Admin":
            password = st.text_input("Admin Password", type="password", key="admin_pwd")
            
            if st.button("🔓 LOGIN", use_container_width=True):
                if password == ADMIN_PASS:
                    st.session_state.logged_in = True
                    st.session_state.user_role = "admin"
                    st.session_state.user_email = "admin@natuvisio.com"
                    log_action("LOGIN", "admin", "", "Admin login successful")
                    st.rerun()
                else:
                    st.error("❌ Invalid password")
        
        else:
            email = st.text_input("Email", key="partner_email")
            password = st.text_input("Password", type="password", key="partner_pwd")
            
            if st.button("🔓 LOGIN", use_container_width=True):
                if email in USER_CREDENTIALS and USER_CREDENTIALS[email]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.user_role = USER_CREDENTIALS[email]["role"]
                    st.session_state.user_brand = USER_CREDENTIALS[email]["brand"]
                    st.session_state.user_email = email
                    log_action("LOGIN", email, "", f"{USER_CREDENTIALS[email]['role']} login")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 8. ADMIN DASHBOARD
# ============================================================================

def admin_dashboard():
    load_css()
    
    # Header
    col_h1, col_h2, col_h3 = st.columns([5, 1, 1])
    
    with col_h1:
        unread = get_unread_count(st.session_state.user_email)
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            {get_icon('mountain', '#4ECDC4', 34)}
            <div>
                <h1 style="margin:0;">ADMIN HQ</h1>
                <span style="font-size: 11px; opacity: 0.6;">COMMAND CENTER</span>
            </div>
            <span class="unread-badge" style="margin-left:20px;">{unread} New</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h3:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # Metrics
    df = load_orders()
    
    if not df.empty:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div class="metric-label">TOTAL ORDERS</div>
                <div class="metric-value">{len(df)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; border-top: 3px solid #4ECDC4;">
                <div class="metric-label">REVENUE</div>
                <div class="metric-value" style="color:#4ECDC4;">{df['Total_Value'].sum():,.0f}₺</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; border-top: 3px solid #10B981;">
                <div class="metric-label">COMMISSION</div>
                <div class="metric-value" style="color:#10B981;">{df['Commission_Amt'].sum():,.0f}₺</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            pending = len(df[df['Status'] == 'Pending'])
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; border-top: 3px solid #F59E0B;">
                <div class="metric-label">PENDING</div>
                <div class="metric-value" style="color:#F59E0B;">{pending}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tabs
    tabs = st.tabs([
        "🚀 NEW DISPATCH",
        "📦 ALL ORDERS",
        "💬 MESSAGES",
        "📊 ANALYTICS",
        "👥 USER MANAGEMENT",
        "📜 LOGS"
    ])
    
    with tabs[0]:
        render_admin_dispatch()
    
    with tabs[1]:
        render_admin_orders()
    
    with tabs[2]:
        render_admin_messages()
    
    with tabs[3]:
        render_admin_analytics()
    
    with tabs[4]:
        render_user_management()
    
    with tabs[5]:
        render_admin_logs()

def render_admin_dispatch():
    col_L, col_R = st.columns([PHI, 1])
    
    with col_L:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Customer Information")
        
        col_n, col_p = st.columns(2)
        with col_n:
            cust_name = st.text_input("Name", key="cust_name")
        with col_p:
            cust_phone = st.text_input("Phone", key="cust_phone")
        cust_addr = st.text_area("Address", key="cust_addr", height=80)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🛒 Product Selection")
        
        if st.session_state.cart:
            active_brand = st.session_state.brand_lock
            st.info(f"🔒 Brand Locked: {active_brand}")
        else:
            active_brand = st.selectbox("Select Brand", list(BRANDS.keys()), key="brand_sel")
        
        brand_data = BRANDS[active_brand]
        products = list(brand_data["products"].keys())
        
        col_p, col_q = st.columns([3, 1])
        with col_p:
            prod = st.selectbox("Product", products, key="prod_sel")
        with col_q:
            qty = st.number_input("Qty", 1, value=1, key="qty")
        
        prod_details = brand_data["products"][prod]
        line_total = prod_details['price'] * qty
        comm_amt = line_total * brand_data['commission']
        
        if st.button("➕ ADD TO CART"):
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
        st.markdown("#### 📦 Cart Summary")
        
        if st.session_state.cart:
            for item in st.session_state.cart:
                st.markdown(f"**{item['product']}** × {item['qty']} = {item['subtotal']:,.0f}₺")
            
            total = sum(i['subtotal'] for i in st.session_state.cart)
            total_comm = sum(i['comm_amt'] for i in st.session_state.cart)
            
            st.markdown(f"""
            <div style="background: rgba(78,205,196,0.2); border-radius: 8px; padding: 13px; margin: 13px 0;">
                <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 21px;">
                    <span>Total:</span>
                    <span style="color: #4ECDC4;">{total:,.0f}₺</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px;">
                    <span>Commission:</span>
                    <span style="color: #FCD34D;">{total_comm:,.0f}₺</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("⚡ CREATE ORDER", type="primary"):
                if cust_name and cust_phone:
                    order_id = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
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
                        st.success(f"✅ Order {order_id} created!")
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

def render_admin_orders():
    st.markdown("### 📦 All Orders")
    
    df = load_orders()
    if df.empty:
        st.info("No orders yet")
        return
    
    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        brand_filter = st.multiselect("Filter by Brand", list(BRANDS.keys()))
    with col_f2:
        status_filter = st.multiselect("Filter by Status", ["Pending", "Notified", "Dispatched", "Completed"])
    
    filtered = df.copy()
    if brand_filter:
        filtered = filtered[filtered['Brand'].isin(brand_filter)]
    if status_filter:
        filtered = filtered[filtered['Status'].isin(status_filter)]
    
    st.dataframe(filtered.sort_values('Time', ascending=False), use_container_width=True, hide_index=True)

def render_admin_messages():
    st.markdown("### 💬 Messages")
    
    df_messages = load_messages()
    
    # Compose new message
    with st.expander("✉️ Send New Message", expanded=False):
        recipient_brand = st.selectbox("To", [b for b in BRANDS.keys() if b in USER_CREDENTIALS.values()])
        subject = st.text_input("Subject")
        body = st.text_area("Message", height=100)
        
        if st.button("📤 Send Message"):
            if subject and body:
                # Find recipient email
                recipient_email = None
                for email, data in USER_CREDENTIALS.items():
                    if data["brand"] == recipient_brand:
                        recipient_email = email
                        break
                
                if recipient_email:
                    if send_message(
                        st.session_state.user_email,
                        "admin",
                        recipient_email,
                        USER_CREDENTIALS[recipient_email]["role"],
                        subject,
                        body
                    ):
                        st.success("Message sent!")
                        st.rerun()
    
    # Display messages
    st.markdown("---")
    st.markdown("#### 📨 Inbox")
    
    if df_messages.empty:
        st.info("No messages")
    else:
        my_messages = df_messages[
            (df_messages['To_User'] == st.session_state.user_email) |
            (df_messages['From_User'] == st.session_state.user_email)
        ].sort_values('Time', ascending=False)
        
        for idx, msg in my_messages.iterrows():
            is_from_me = msg['From_User'] == st.session_state.user_email
            card_class = "message-from-admin" if is_from_me else "message-from-user"
            
            st.markdown(f"""
            <div class="message-card {card_class}">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <strong>{"To: " + msg['To_User'] if is_from_me else "From: " + msg['From_User']}</strong>
                    <span style="font-size: 11px; opacity: 0.6;">{msg['Time']}</span>
                </div>
                <div style="font-size: 13px; font-weight: 600; margin-bottom: 4px;">{msg['Subject']}</div>
                <div style="font-size: 12px; opacity: 0.8;">{msg['Body']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if not is_from_me and msg['Read'] == 'No':
                if st.button("Mark as Read", key=f"read_{msg['Message_ID']}"):
                    mark_message_read(msg['Message_ID'])
                    st.rerun()

def render_admin_analytics():
    st.markdown("### 📊 Analytics")
    
    df = load_orders()
    if df.empty:
        st.info("No data")
        return
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown("**Revenue by Brand**")
        brand_revenue = df.groupby('Brand')['Total_Value'].sum()
        st.bar_chart(brand_revenue)
    
    with col_a2:
        st.markdown("**Orders by Brand**")
        brand_orders = df['Brand'].value_counts()
        st.bar_chart(brand_orders)
    
    st.markdown("**Status Distribution**")
    status_dist = df['Status'].value_counts()
    st.bar_chart(status_dist)

def render_user_management():
    st.markdown("### 👥 User Management")
    
    partners_df = pd.read_csv(CSV_PARTNERS)
    st.dataframe(partners_df, use_container_width=True, hide_index=True)

def render_admin_logs():
    st.markdown("### 📜 System Logs")
    
    df_logs = pd.read_csv(CSV_LOGS) if os.path.exists(CSV_LOGS) else pd.DataFrame()
    
    if df_logs.empty:
        st.info("No logs")
        return
    
    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        user_filter = st.multiselect("Filter by User", df_logs['User'].unique().tolist())
    with col_f2:
        action_filter = st.multiselect("Filter by Action", df_logs['Action'].unique().tolist())
    
    filtered = df_logs.copy()
    if user_filter:
        filtered = filtered[filtered['User'].isin(user_filter)]
    if action_filter:
        filtered = filtered[filtered['Action'].isin(action_filter)]
    
    st.dataframe(filtered.sort_values('Time', ascending=False), use_container_width=True, hide_index=True)

# ============================================================================
# 9. PARTNER DASHBOARD
# ============================================================================

def partner_dashboard():
    load_css()
    brand = st.session_state.user_brand
    brand_color = BRANDS[brand]['color']
    
    # Header
    col_h1, col_h2 = st.columns([5, 1])
    
    with col_h1:
        unread = get_unread_count(st.session_state.user_email)
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <img src="{LOGO_URL}" style="height:40px;">
            <div>
                <h1 style="margin:0; color:{brand_color};">{brand}</h1>
                <span style="font-size: 11px; opacity: 0.6;">PARTNER PORTAL</span>
            </div>
            <span class="unread-badge" style="margin-left:20px;">{unread} New</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # Metrics
    df = load_orders()
    my_orders = df[df['Brand'] == brand]
    
    if not my_orders.empty:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div class="metric-label">MY ORDERS</div>
                <div class="metric-value">{len(my_orders)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            pending = len(my_orders[my_orders['Status'] == 'Pending'])
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; border-top: 3px solid #F59E0B;">
                <div class="metric-label">PENDING</div>
                <div class="metric-value" style="color:#F59E0B;">{pending}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            completed = len(my_orders[my_orders['Status'] == 'Completed'])
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; border-top: 3px solid #10B981;">
                <div class="metric-label">COMPLETED</div>
                <div class="metric-value" style="color:#10B981;">{completed}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            earnings = my_orders[my_orders['Status'] == 'Completed']['Brand_Payout'].sum()
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; border-top: 3px solid {brand_color};">
                <div class="metric-label">EARNINGS</div>
                <div class="metric-value" style="color:{brand_color};">{earnings:,.0f}₺</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tabs
    tabs = st.tabs([
        "📥 NEW ORDERS",
        "🚚 SHIPPING",
        "✅ COMPLETED",
        "💬 MESSAGES",
        "📊 MY STATS"
    ])
    
    with tabs[0]:
        render_partner_new_orders()
    
    with tabs[1]:
        render_partner_shipping()
    
    with tabs[2]:
        render_partner_completed()
    
    with tabs[3]:
        render_partner_messages()
    
    with tabs[4]:
        render_partner_stats()

def render_partner_new_orders():
    st.markdown("### 📥 New Orders")
    
    df = load_orders()
    brand = st.session_state.user_brand
    new_orders = df[(df['Brand'] == brand) & (df['Status'] == 'Pending')]
    
    if new_orders.empty:
        st.info("No pending orders")
        return
    
    for idx, row in new_orders.iterrows():
        with st.expander(f"🆕 {row['Order_ID']} - {row['Customer']}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Customer:** {row['Customer']}  
                **Phone:** {row['Phone']}  
                **Address:** {row['Address']}  
                **Items:** {row['Items']}
                """)
            
            with col2:
                st.metric("Your Payout", f"{row['Brand_Payout']:,.0f}₺")
                
                if st.button("✅ Accept Order", key=f"accept_{row['Order_ID']}"):
                    df.at[idx, 'Status'] = 'Notified'
                    df.at[idx, 'WhatsApp_Sent'] = 'YES'
                    update_orders(df)
                    log_action("ORDER_ACCEPTED", st.session_state.user_email, row['Order_ID'], "Order accepted by partner")
                    st.success("Order accepted!")
                    st.rerun()

def render_partner_shipping():
    st.markdown("### 🚚 Shipping Management")
    
    df = load_orders()
    brand = st.session_state.user_brand
    to_ship = df[(df['Brand'] == brand) & (df['Status'] == 'Notified')]
    
    if to_ship.empty:
        st.info("No orders to ship")
        return
    
    for idx, row in to_ship.iterrows():
        with st.expander(f"📦 {row['Order_ID']} - {row['Customer']}"):
            tracking = st.text_input("Tracking Number", key=f"track_{row['Order_ID']}")
            courier = st.selectbox("Courier", ["Yurtiçi", "Aras", "MNG", "PTT"], key=f"courier_{row['Order_ID']}")
            
            if st.button("🚀 Mark as Shipped", key=f"ship_{row['Order_ID']}"):
                if tracking:
                    df.at[idx, 'Status'] = 'Dispatched'
                    df.at[idx, 'Tracking_Num'] = f"{courier} - {tracking}"
                    update_orders(df)
                    log_action("ORDER_SHIPPED", st.session_state.user_email, row['Order_ID'], f"Shipped via {courier}")
                    st.success("Order marked as shipped!")
                    st.rerun()
                else:
                    st.error("Please enter tracking number")

def render_partner_completed():
    st.markdown("### ✅ Completed Orders")
    
    df = load_orders()
    brand = st.session_state.user_brand
    completed = df[(df['Brand'] == brand) & (df['Status'].isin(['Dispatched', 'Completed']))]
    
    if completed.empty:
        st.info("No completed orders")
        return
    
    st.dataframe(completed[['Order_ID', 'Time', 'Customer', 'Items', 'Brand_Payout', 'Status', 'Tracking_Num']], 
                use_container_width=True, hide_index=True)

def render_partner_messages():
    st.markdown("### 💬 Messages")
    
    df_messages = load_messages()
    
    # Compose
    with st.expander("✉️ Send Message to Admin", expanded=False):
        subject = st.text_input("Subject")
        body = st.text_area("Message", height=100)
        
        if st.button("📤 Send"):
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
    
    # Display
    st.markdown("---")
    st.markdown("#### 📨 My Messages")
    
    if df_messages.empty:
        st.info("No messages")
    else:
        my_messages = df_messages[
            (df_messages['To_User'] == st.session_state.user_email) |
            (df_messages['From_User'] == st.session_state.user_email)
        ].sort_values('Time', ascending=False)
        
        for idx, msg in my_messages.iterrows():
            is_from_me = msg['From_User'] == st.session_state.user_email
            card_class = "message-from-user" if is_from_me else "message-from-admin"
            
            st.markdown(f"""
            <div class="message-card {card_class}">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <strong>{"To: Admin" if is_from_me else "From: Admin"}</strong>
                    <span style="font-size: 11px; opacity: 0.6;">{msg['Time']}</span>
                </div>
                <div style="font-size: 13px; font-weight: 600; margin-bottom: 4px;">{msg['Subject']}</div>
                <div style="font-size: 12px; opacity: 0.8;">{msg['Body']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if not is_from_me and msg['Read'] == 'No':
                if st.button("Mark as Read", key=f"read_{msg['Message_ID']}"):
                    mark_message_read(msg['Message_ID'])
                    st.rerun()

def render_partner_stats():
    st.markdown("### 📊 My Statistics")
    
    df = load_orders()
    brand = st.session_state.user_brand
    my_orders = df[df['Brand'] == brand]
    
    if my_orders.empty:
        st.info("No data yet")
        return
    
    # Monthly performance
    my_orders['Month'] = pd.to_datetime(my_orders['Time']).dt.to_period('M')
    monthly = my_orders.groupby('Month').agg({
        'Order_ID': 'count',
        'Brand_Payout': 'sum'
    }).reset_index()
    monthly.columns = ['Month', 'Orders', 'Earnings']
    
    st.markdown("**Monthly Performance**")
    st.dataframe(monthly, use_container_width=True, hide_index=True)
    
    st.markdown("**Orders Over Time**")
    st.line_chart(my_orders.groupby('Month').size())

# ============================================================================
# 10. DIETITIAN DASHBOARD
# ============================================================================

def dietitian_dashboard():
    load_css()
    brand = st.session_state.user_brand
    
    # Header
    col_h1, col_h2 = st.columns([5, 1])
    
    with col_h1:
        unread = get_unread_count(st.session_state.user_email)
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <img src="{LOGO_URL}" style="height:40px;">
            <div>
                <h1 style="margin:0; color:#A78BFA;">DR. JULIANA</h1>
                <span style="font-size: 11px; opacity: 0.6;">DIETITIAN PANEL</span>
            </div>
            <span class="unread-badge" style="margin-left:20px;">{unread} New</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # Tabs
    tabs = st.tabs([
        "📦 STOCK INVENTORY",
        "💰 SALES & EARNINGS",
        "💬 MESSAGES",
        "📜 MY ACTIVITY"
    ])
    
    with tabs[0]:
        render_dietitian_stock()
    
    with tabs[1]:
        render_dietitian_sales()
    
    with tabs[2]:
        render_dietitian_messages()
    
    with tabs[3]:
        render_dietitian_activity()

def render_dietitian_stock():
    st.markdown("### 📦 Stock Inventory")
    
    # Current stock levels
    df_stock = load_stock()
    
    st.markdown("#### Current Stock Levels")
    
    if df_stock.empty:
        st.info("No stock records yet")
        current_stock = {}
    else:
        # Get latest balance for each product
        products = BRANDS["DRJULIANA"]["products"].keys()
        current_stock = {}
        
        for product in products:
            product_history = df_stock[df_stock['Product'] == product]
            if not product_history.empty:
                current_stock[product] = product_history.iloc[-1]['Balance']
            else:
                current_stock[product] = 0
        
        # Display as cards
        cols = st.columns(3)
        for idx, (product, balance) in enumerate(current_stock.items()):
            with cols[idx % 3]:
                color = "#10B981" if balance > 5 else "#EF4444"
                st.markdown(f"""
                <div class="glass-card" style="text-align:center; border-top: 3px solid {color};">
                    <div class="metric-label">{product}</div>
                    <div class="metric-value" style="color:{color};">{balance}</div>
                    <div style="font-size:10px; opacity:0.6;">UNITS IN STOCK</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Add/Remove stock
    st.markdown("---")
    st.markdown("#### Update Stock")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        product = st.selectbox("Product", list(BRANDS["DRJULIANA"]["products"].keys()))
    with col2:
        action = st.selectbox("Action", ["ADD", "REMOVE"])
    with col3:
        quantity = st.number_input("Quantity", min_value=1, value=1)
    
    notes = st.text_input("Notes (optional)")
    
    if st.button("🔄 Update Stock"):
        if update_stock(product, action, quantity, notes):
            st.success(f"Stock updated: {action} {quantity} units of {product}")
            st.rerun()
    
    # Stock history
    if not df_stock.empty:
        st.markdown("---")
        st.markdown("#### Stock Movement History")
        st.dataframe(df_stock.sort_values('Time', ascending=False), use_container_width=True, hide_index=True)

def render_dietitian_sales():
    st.markdown("### 💰 Sales & Earnings")
    
    df = load_orders()
    my_orders = df[df['Brand'] == "DRJULIANA"]
    
    if my_orders.empty:
        st.info("No sales yet")
        return
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sales", len(my_orders))
    with col2:
        total_revenue = my_orders['Total_Value'].sum()
        st.metric("Revenue", f"{total_revenue:,.0f}₺")
    with col3:
        total_earnings = my_orders[my_orders['Status'] == 'Completed']['Brand_Payout'].sum()
        st.metric("Earnings (Completed)", f"{total_earnings:,.0f}₺")
    
    # Sales breakdown
    st.markdown("---")
    st.markdown("#### Sales Breakdown by Service")
    
    service_sales = my_orders.groupby('Items').agg({
        'Order_ID': 'count',
        'Total_Value': 'sum',
        'Brand_Payout': 'sum'
    }).reset_index()
    service_sales.columns = ['Service', 'Count', 'Revenue', 'Your Earnings']
    
    st.dataframe(service_sales, use_container_width=True, hide_index=True)
    
    # Recent orders
    st.markdown("---")
    st.markdown("#### Recent Orders")
    st.dataframe(my_orders.sort_values('Time', ascending=False).head(10), use_container_width=True, hide_index=True)

def render_dietitian_messages():
    st.markdown("### 💬 Messages")
    
    df_messages = load_messages()
    
    # Compose
    with st.expander("✉️ Send Message to Admin", expanded=False):
        subject = st.text_input("Subject")
        body = st.text_area("Message", height=100)
        
        if st.button("📤 Send"):
            if subject and body:
                if send_message(
                    st.session_state.user_email,
                    "dietitian",
                    "admin@natuvisio.com",
                    "admin",
                    subject,
                    body
                ):
                    st.success("Message sent!")
                    st.rerun()
    
    # Display
    st.markdown("---")
    st.markdown("#### 📨 My Messages")
    
    if df_messages.empty:
        st.info("No messages")
    else:
        my_messages = df_messages[
            (df_messages['To_User'] == st.session_state.user_email) |
            (df_messages['From_User'] == st.session_state.user_email)
        ].sort_values('Time', ascending=False)
        
        for idx, msg in my_messages.iterrows():
            is_from_me = msg['From_User'] == st.session_state.user_email
            card_class = "message-from-user" if is_from_me else "message-from-admin"
            
            st.markdown(f"""
            <div class="message-card {card_class}">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <strong>{"To: Admin" if is_from_me else "From: Admin"}</strong>
                    <span style="font-size: 11px; opacity: 0.6;">{msg['Time']}</span>
                </div>
                <div style="font-size: 13px; font-weight: 600; margin-bottom: 4px;">{msg['Subject']}</div>
                <div style="font-size: 12px; opacity: 0.8;">{msg['Body']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if not is_from_me and msg['Read'] == 'No':
                if st.button("Mark as Read", key=f"read_{msg['Message_ID']}"):
                    mark_message_read(msg['Message_ID'])
                    st.rerun()

def render_dietitian_activity():
    st.markdown("### 📜 My Activity Logs")
    
    df_logs = pd.read_csv(CSV_LOGS) if os.path.exists(CSV_LOGS) else pd.DataFrame()
    
    if df_logs.empty:
        st.info("No activity yet")
        return
    
    my_logs = df_logs[df_logs['User'] == st.session_state.user_email].sort_values('Time', ascending=False)
    
    if my_logs.empty:
        st.info("No activity logged yet")
    else:
        st.dataframe(my_logs, use_container_width=True, hide_index=True)

# ============================================================================
# 11. MAIN ROUTING
# ============================================================================

if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_screen()
    else:
        if st.session_state.user_role == "admin":
            admin_dashboard()
        elif st.session_state.user_role == "partner":
            partner_dashboard()
        elif st.session_state.user_role == "dietitian":
            dietitian_dashboard()
