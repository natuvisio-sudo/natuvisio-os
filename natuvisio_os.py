import streamlit as st
import pandas as pd
import numpy as np
import os
import io
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO ADMIN OS - PRODUCTION EDITION
# Dependencies: streamlit, pandas, numpy ONLY
# All 15 Critical Features | Zero Errors | Production Ready
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Admin OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 1. CONFIGURATION
# ============================================================================

ADMIN_PASS = "admin2025"
CSV_ORDERS = "orders_complete.csv"
CSV_PAYMENTS = "brand_payments.csv"
CSV_LOGS = "system_logs.csv"
PHI = 1.618

FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

BRANDS = {
    "HAKI HEAL": {
        "phone": "601158976276",
        "color": "#4ECDC4",
        "commission": 0.15,
        "iban": "TR90 0006 1000 0000 1234 5678 90",
        "products": {
            "HAKI HEAL CREAM": {"sku": "SKU-HAKI-CRM-01", "price": 450},
            "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY-01", "price": 380},
            "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP-01", "price": 120}
        }
    },
    "AURORACO": {
        "phone": "601158976276",
        "color": "#FF6B6B",
        "commission": 0.20,
        "iban": "TR90 0006 2000 0000 9876 5432 10",
        "products": {
            "AURORACO MATCHA EZMESI": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO KAKAO EZMESI": {"sku": "SKU-AUR-CACAO", "price": 550},
            "AURORACO SUPER GIDA": {"sku": "SKU-AUR-SUPER", "price": 800}
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
        "bell": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/></svg>',
        "download": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
        "search": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>',
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
                              url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
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
        
        .order-card-red {{
            border-left: 4px solid #EF4444;
            animation: pulse-red 2s infinite;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
        }}
        
        .order-card-green {{
            border-left: 4px solid #10B981;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
        }}
        
        .metric-card {{
            text-align: center;
            padding: {FIBO['md']}px;
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
        
        .status-badge {{
            display: inline-block;
            padding: 6px {FIBO['sm']}px;
            border-radius: 20px;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}
        
        .status-new {{ background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.4); }}
        .status-pending {{ background: rgba(251, 191, 36, 0.2); color: #FCD34D; border: 1px solid rgba(251, 191, 36, 0.4); }}
        .status-notified {{ background: rgba(59, 130, 246, 0.2); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.4); }}
        .status-dispatched {{ background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.4); }}
        .status-completed {{ background: rgba(139, 92, 246, 0.2); color: #A78BFA; border: 1px solid rgba(139, 92, 246, 0.4); }}
        
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
        
        ::-webkit-scrollbar {{ width: {FIBO['xs']}px; }}
        ::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.05); }}
        ::-webkit-scrollbar-thumb {{ background: rgba(78,205,196,0.3); border-radius: {FIBO['xs']}px; }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 4. DATABASE
# ============================================================================

def init_databases():
    if not os.path.exists(CSV_ORDERS):
        pd.DataFrame(columns=[
            "Order_ID", "Time", "Brand", "Customer", "Phone", "Address",
            "Items", "Total_Value", "Commission_Rate", "Commission_Amt",
            "Brand_Payout", "Status", "WhatsApp_Sent", "Tracking_Num",
            "Priority", "Notes", "Created_By", "Last_Modified"
        ]).to_csv(CSV_ORDERS, index=False)
    
    if not os.path.exists(CSV_PAYMENTS):
        pd.DataFrame(columns=[
            "Payment_ID", "Time", "Brand", "Amount", "Method", "Reference", "Notes"
        ]).to_csv(CSV_PAYMENTS, index=False)
    
    if not os.path.exists(CSV_LOGS):
        pd.DataFrame(columns=[
            "Log_ID", "Time", "Action", "User", "Order_ID", "Details"
        ]).to_csv(CSV_LOGS, index=False)

def load_orders():
    try:
        if os.path.exists(CSV_ORDERS):
            return pd.read_csv(CSV_ORDERS)
    except: pass
    return pd.DataFrame(columns=[
        "Order_ID", "Time", "Brand", "Customer", "Phone", "Address",
        "Items", "Total_Value", "Commission_Rate", "Commission_Amt",
        "Brand_Payout", "Status", "WhatsApp_Sent", "Tracking_Num",
        "Priority", "Notes", "Created_By", "Last_Modified"
    ])

def save_order(order_data):
    try:
        df = load_orders()
        df = pd.concat([df, pd.DataFrame([order_data])], ignore_index=True)
        df.to_csv(CSV_ORDERS, index=False)
        log_action("CREATE_ORDER", "admin", order_data['Order_ID'], f"Created {order_data['Order_ID']}")
        return True
    except Exception as e:
        st.error(f"Save error: {e}")
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

def save_payment(payment_data):
    try:
        df = load_payments()
        df = pd.concat([df, pd.DataFrame([payment_data])], ignore_index=True)
        df.to_csv(CSV_PAYMENTS, index=False)
        log_action("PAYMENT", "admin", "", f"Paid {payment_data['Brand']}")
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
    csv = df.to_csv(index=False)
    return csv

# ============================================================================
# 5. SESSION STATE
# ============================================================================

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'brand_lock' not in st.session_state:
    st.session_state.brand_lock = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# ============================================================================
# 6. ANALYTICS
# ============================================================================

def get_alerts():
    df = load_orders()
    alerts = []
    
    if df.empty:
        return alerts
    
    try:
        df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
        now = datetime.now()
        
        no_notify = df[df['WhatsApp_Sent'] == 'NO']
        if len(no_notify) > 0:
            alerts.append({
                'type': 'critical',
                'count': len(no_notify),
                'message': f"{len(no_notify)} orders need notification",
                'color': '#EF4444'
            })
        
        no_tracking = df[(df['Status'] == 'Notified') & (df['Tracking_Num'] == '')]
        if len(no_tracking) > 0:
            alerts.append({
                'type': 'warning',
                'count': len(no_tracking),
                'message': f"{len(no_tracking)} missing tracking",
                'color': '#F59E0B'
            })
        
        stuck = df[df['Status'].isin(['Pending', 'Notified'])]
        if len(stuck) > 0:
            stuck['hours_old'] = (now - stuck['Time']).dt.total_seconds() / 3600
            stuck_count = len(stuck[stuck['hours_old'] > 24])
            if stuck_count > 0:
                alerts.append({
                    'type': 'warning',
                    'count': stuck_count,
                    'message': f"{stuck_count} stuck > 24h",
                    'color': '#F59E0B'
                })
    except: pass
    
    return alerts

def get_vendor_health(brand):
    df = load_orders()
    if df.empty:
        return {}
    
    brand_df = df[df['Brand'] == brand]
    if brand_df.empty:
        return {}
    
    try:
        total_orders = len(brand_df)
        total_revenue = brand_df['Total_Value'].sum()
        notified_pct = (len(brand_df[brand_df['WhatsApp_Sent'] == 'YES']) / total_orders * 100) if total_orders > 0 else 0
        
        payments_df = load_payments()
        brand_payments = payments_df[payments_df['Brand'] == brand]
        total_paid = brand_payments['Amount'].sum() if not brand_payments.empty else 0
        total_owed = brand_df['Brand_Payout'].sum()
        payout_pending = total_owed - total_paid
        
        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'payout_pending': payout_pending,
            'notified_pct': notified_pct,
            'health_score': min(100, int(notified_pct))
        }
    except:
        return {}

def get_commission_shortcuts():
    df = load_orders()
    if df.empty:
        return {'today': 0, 'week': 0, 'month': 0, 'pending': 0, 'paid': 0}
    
    try:
        df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
        now = datetime.now()
        
        today = df[df['Time'].dt.date == now.date()]['Commission_Amt'].sum()
        week_ago = now - timedelta(days=7)
        week = df[df['Time'] >= week_ago]['Commission_Amt'].sum()
        month_ago = now - timedelta(days=30)
        month = df[df['Time'] >= month_ago]['Commission_Amt'].sum()
        
        pending = df[df['Status'] != 'Completed']['Commission_Amt'].sum()
        paid = df[df['Status'] == 'Completed']['Commission_Amt'].sum()
        
        return {
            'today': today,
            'week': week,
            'month': month,
            'pending': pending,
            'paid': paid
        }
    except:
        return {'today': 0, 'week': 0, 'month': 0, 'pending': 0, 'paid': 0}

def get_tasks():
    df = load_orders()
    tasks = []
    
    if df.empty:
        return tasks
    
    try:
        needs_notify = df[df['WhatsApp_Sent'] == 'NO']
        if len(needs_notify) > 0:
            for brand in needs_notify['Brand'].unique():
                count = len(needs_notify[needs_notify['Brand'] == brand])
                tasks.append(f"📲 Send {count} notification(s) to {brand}")
        
        needs_tracking = df[(df['Status'] == 'Notified') & (df['Tracking_Num'] == '')]
        if len(needs_tracking) > 0:
            for brand in needs_tracking['Brand'].unique():
                count = len(needs_tracking[needs_tracking['Brand'] == brand])
                tasks.append(f"📦 Add tracking for {count} {brand} order(s)")
        
        can_complete = df[df['Status'] == 'Dispatched']
        if len(can_complete) > 0:
            tasks.append(f"✅ Mark {len(can_complete)} order(s) as completed")
    except: pass
    
    return tasks

# ============================================================================
# 7. LOGIN
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
            <p style="opacity: 0.6; font-size: 12px;">PRODUCTION EDITION</p>
        </div>
        """, unsafe_allow_html=True)
        
        password = st.text_input("Password", type="password", key="login")
        
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            if st.button("🔓 UNLOCK", use_container_width=True):
                if password == ADMIN_PASS:
                    st.session_state.admin_logged_in = True
                    log_action("LOGIN", "admin", "", "Login successful")
                    st.rerun()
                else:
                    st.error("❌ ACCESS DENIED")
        
        with col_b2:
            if st.button("🚪 EXIT", use_container_width=True):
                st.info("Goodbye")

# ============================================================================
# 8. DASHBOARD
# ============================================================================

def dashboard():
    load_css()
    init_databases()
    
    # HEADER
    col_h1, col_h2, col_h3 = st.columns([5, 1, 1])
    
    with col_h1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: {FIBO['sm']}px;">
            {get_icon('mountain', '#4ECDC4', FIBO['lg'])}
            <div>
                <h1 style="margin:0;">ADMIN HQ</h1>
                <span style="font-size: 11px; opacity: 0.6;">COMPLETE OS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h2:
        if st.button("🎨"):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()
    
    with col_h3:
        with st.popover("👤"):
            st.markdown("**Founder Access**")
            st.markdown("Role: Admin")
            if st.button("🚪 Logout"):
                st.session_state.admin_logged_in = False
                st.session_state.cart = []
                st.session_state.brand_lock = None
                log_action("LOGOUT", "admin", "", "Logout")
                st.rerun()
    
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # ALERTS
    alerts = get_alerts()
    if alerts:
        st.markdown("### 🚨 Attention Required")
        cols = st.columns(len(alerts))
        for idx, alert in enumerate(alerts):
            with cols[idx]:
                st.markdown(f"""
                <div class="glass-card alert-card" style="border-top: 3px solid {alert['color']};">
                    <div style="text-align: center;">
                        <div style="font-size: {FIBO['lg']}px; font-weight: 800; color: {alert['color']};">
                            {alert['count']}
                        </div>
                        <div style="font-size: 10px; opacity: 0.7; text-transform: uppercase;">
                            {alert['message']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # TASKS
    tasks = get_tasks()
    if tasks:
        with st.expander("📋 Tasks", expanded=False):
            for task in tasks[:5]:
                st.markdown(f"• {task}")
    
    # METRICS
    df = load_orders()
    
    if not df.empty:
        comm = get_commission_shortcuts()
        
        col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)
        
        metrics_data = [
            (col_m1, len(df), "Total Orders", None),
            (col_m2, f"{comm['week']:,.0f}₺", "Week Comm", "#4ECDC4"),
            (col_m3, f"{comm['month']:,.0f}₺", "Month Comm", "#10B981"),
            (col_m4, f"{comm['pending']:,.0f}₺", "Pending", "#F59E0B"),
            (col_m5, len(df[df['WhatsApp_Sent'] == 'NO']), "New Orders", "#EF4444"),
            (col_m6, len(df[pd.to_datetime(df['Time'], errors='coerce').dt.date == datetime.now().date()]), "Today", None)
        ]
        
        for col, value, label, color in metrics_data:
            with col:
                border_style = f"border-top: 3px solid {color};" if color else ""
                color_style = f"color: {color};" if color else ""
                st.markdown(f"""
                <div class="glass-card metric-card" style="{border_style}">
                    <div class="metric-value" style="{color_style}">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # BRAND HEALTH
    st.markdown("### 📊 Brand Performance")
    
    brand_cols = st.columns(3)
    for idx, brand in enumerate(BRANDS.keys()):
        health = get_vendor_health(brand)
        if health:
            with brand_cols[idx]:
                color = '#10B981' if health['health_score'] > 80 else '#F59E0B'
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: {BRANDS[brand]['color']}; margin-bottom: {FIBO['sm']}px;">{brand}</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: {FIBO['xs']}px;">
                        <div>
                            <div style="font-size: 10px; opacity: 0.6;">ORDERS</div>
                            <div style="font-size: {FIBO['md']}px; font-weight: 700;">{health['total_orders']}</div>
                        </div>
                        <div>
                            <div style="font-size: 10px; opacity: 0.6;">REVENUE</div>
                            <div style="font-size: {FIBO['md']}px; font-weight: 700;">{health['total_revenue']:,.0f}₺</div>
                        </div>
                        <div>
                            <div style="font-size: 10px; opacity: 0.6;">PENDING</div>
                            <div style="font-size: {FIBO['md']}px; font-weight: 700; color: #F59E0B;">{health['payout_pending']:,.0f}₺</div>
                        </div>
                        <div>
                            <div style="font-size: 10px; opacity: 0.6;">HEALTH</div>
                            <div style="font-size: {FIBO['md']}px; font-weight: 700; color: {color};">{health['health_score']}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # TABS
    tabs = st.tabs([
        "🚀 NEW DISPATCH",
        "🔴 NEW ORDERS",
        "✅ PROCESSING",
        "📦 ALL ORDERS",
        "💰 FINANCIALS",
        "📥 EXPORT",
        "📊 ANALYTICS",
        "📜 LOGS"
    ])
    
    with tabs[0]:
        render_new_dispatch()
    
    with tabs[1]:
        render_new_orders()
    
    with tabs[2]:
        render_processing()
    
    with tabs[3]:
        render_all_orders()
    
    with tabs[4]:
        render_financials()
    
    with tabs[5]:
        render_export()
    
    with tabs[6]:
        render_analytics()
    
    with tabs[7]:
        render_logs()
    
    # FOOTER
    st.markdown("---")
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        st.markdown(f"{get_icon('activity', '#10B981', 16)} **System:** Online", unsafe_allow_html=True)
    with col_f2:
        st.markdown(f"{get_icon('clock', '#4ECDC4', 16)} **Updated:** {datetime.now().strftime('%H:%M:%S')}", unsafe_allow_html=True)
    with col_f3:
        st.markdown(f"**Cache:** {len(load_orders())} records")
    with col_f4:
        st.markdown(f"**Theme:** {st.session_state.theme.capitalize()}")

# ============================================================================
# 9. TAB RENDERERS
# ============================================================================

def render_new_dispatch():
    col_L, col_R = st.columns([PHI, 1])
    
    with col_L:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Customer")
        col_n, col_p = st.columns(2)
        with col_n:
            cust_name = st.text_input("Name", key="cust_name")
        with col_p:
            cust_phone = st.text_input("Phone", key="cust_phone")
        cust_addr = st.text_area("Address", key="cust_addr", height=80)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🛒 Products")
        
        if st.session_state.cart:
            st.info(f"🔒 {st.session_state.brand_lock}")
            active_brand = st.session_state.brand_lock
        else:
            active_brand = st.selectbox("Brand", list(BRANDS.keys()), key="brand_sel")
        
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
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 13px;">
            <div style="display: flex; justify-content: space-between;">
                <span>Price:</span>
                <span style="color: #4ECDC4; font-weight: 700;">{line_total:,.0f}₺</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Commission:</span>
                <span style="color: #FCD34D;">{comm_amt:,.0f}₺</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕ ADD", key="add_btn"):
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
        st.markdown("#### 📦 Cart")
        
        if st.session_state.cart:
            for item in st.session_state.cart:
                st.markdown(f"**{item['product']}** × {item['qty']} = {item['subtotal']:,.0f}₺")
            
            total = sum(i['subtotal'] for i in st.session_state.cart)
            total_comm = sum(i['comm_amt'] for i in st.session_state.cart)
            
            st.markdown(f"""
            <div style="background: rgba(78,205,196,0.2); border: 1px solid rgba(78,205,196,0.3); 
                 border-radius: 8px; padding: 13px; margin: 13px 0;">
                <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 21px;">
                    <span>Total:</span>
                    <span style="color: #4ECDC4;">{total:,.0f}₺</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px;">
                    <span>Comm:</span>
                    <span style="color: #FCD34D;">{total_comm:,.0f}₺</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            priority = st.selectbox("Priority", ["Standard", "🚨 URGENT", "🧊 Cold"], key="priority")
            
            if st.button("⚡ CREATE", type="primary", key="create_btn"):
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
                        'Priority': priority,
                        'Notes': '',
                        'Created_By': 'admin',
                        'Last_Modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    if save_order(order_data):
                        st.success(f"✅ {order_id}")
                        st.session_state.cart = []
                        st.session_state.brand_lock = None
                        st.rerun()
                else:
                    st.error("Fill details!")
            
            if st.button("🗑️ Clear", key="clear_btn"):
                st.session_state.cart = []
                st.session_state.brand_lock = None
                st.rerun()
        else:
            st.info("Empty")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_new_orders():
    st.markdown("### 🔴 New Orders")
    
    df = load_orders()
    if df.empty:
        st.info("No orders")
        return
    
    new_orders = df[df['WhatsApp_Sent'] == 'NO'].sort_values('Time', ascending=False)
    
    if new_orders.empty:
        st.success("✅ All processed!")
        return
    
    for idx, row in new_orders.iterrows():
        st.markdown(f"""
        <div class="glass-card alert-card">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <h3>{row['Order_ID']}</h3>
                    <span class="status-badge status-new">NEW</span>
                </div>
                <div style="text-align: right;">
                    <h3>{row['Total_Value']:,.0f}₺</h3>
                </div>
            </div>
            <div style="margin-top: 13px;">
                <strong>{row['Brand']}</strong> | {row['Customer']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"📲 Notify", key=f"notify_{idx}"):
            df.at[idx, 'WhatsApp_Sent'] = 'YES'
            df.at[idx, 'Status'] = 'Notified'
            update_orders(df)
            log_action("NOTIFY", "admin", row['Order_ID'], f"Notified {row['Brand']}")
            st.rerun()

def render_processing():
    st.markdown("### ✅ Processing")
    
    df = load_orders()
    if df.empty:
        st.info("No orders")
        return
    
    active = df[df['Status'].isin(['Pending', 'Notified', 'Dispatched'])]
    
    for idx, row in active.iterrows():
        card_class = "order-card-red" if row['WhatsApp_Sent'] == 'NO' else "order-card-green"
        
        st.markdown(f"""
        <div class="glass-card {card_class}">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <h3>{row['Order_ID']}</h3>
                    <span class="status-badge status-{row['Status'].lower()}">{row['Status']}</span>
                </div>
                <h3>{row['Total_Value']:,.0f}₺</h3>
            </div>
            <div style="margin-top: 13px;">
                {row['Brand']} | {row['Customer']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_a1, col_a2, col_a3 = st.columns(3)
        
        with col_a1:
            if row['WhatsApp_Sent'] == 'NO':
                if st.button("✅ Sent", key=f"sent_{idx}"):
                    df.at[idx, 'WhatsApp_Sent'] = 'YES'
                    df.at[idx, 'Status'] = 'Notified'
                    update_orders(df)
                    log_action("NOTIFIED", "admin", row['Order_ID'], "Marked")
                    st.rerun()
        
        with col_a2:
            if row['Status'] == 'Notified':
                tracking = st.text_input("Track", key=f"track_{idx}")
                if st.button("📦 Ship", key=f"ship_{idx}"):
                    if tracking:
                        df.at[idx, 'Tracking_Num'] = tracking
                        df.at[idx, 'Status'] = 'Dispatched'
                        update_orders(df)
                        log_action("DISPATCH", "admin", row['Order_ID'], tracking)
                        st.rerun()
        
        with col_a3:
            if row['Status'] == 'Dispatched':
                if st.button("✅ Done", key=f"done_{idx}"):
                    df.at[idx, 'Status'] = 'Completed'
                    update_orders(df)
                    log_action("COMPLETE", "admin", row['Order_ID'], "Done")
                    st.rerun()

def render_all_orders():
    st.markdown("### 📦 All Orders")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        search = st.text_input("🔍 Search", key="search")
    with col_s2:
        brand_filt = st.multiselect("Brand", list(BRANDS.keys()), key="brand_f")
    with col_s3:
        status_filt = st.multiselect("Status", ["Pending", "Notified", "Dispatched", "Completed"], key="status_f")
    
    df = load_orders()
    if df.empty:
        st.info("No orders")
        return
    
    filtered = df.copy()
    
    if search:
        filtered = filtered[
            filtered['Order_ID'].str.contains(search, case=False, na=False) |
            filtered['Customer'].str.contains(search, case=False, na=False) |
            filtered['Phone'].str.contains(search, case=False, na=False)
        ]
    
    if brand_filt:
        filtered = filtered[filtered['Brand'].isin(brand_filt)]
    
    if status_filt:
        filtered = filtered[filtered['Status'].isin(status_filt)]
    
    st.markdown(f"**{len(filtered)}** orders")
    st.dataframe(filtered.sort_values('Time', ascending=False), use_container_width=True, hide_index=True)

def render_financials():
    st.markdown("### 💰 Financials")
    
    df = load_orders()
    df_pay = load_payments()
    
    if df.empty:
        st.info("No data")
        return
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        st.metric("Sales", f"{df['Total_Value'].sum():,.0f}₺")
    with col_f2:
        st.metric("Commission", f"{df['Commission_Amt'].sum():,.0f}₺")
    with col_f3:
        st.metric("Payout", f"{df['Brand_Payout'].sum():,.0f}₺")
    with col_f4:
        rate = df['Commission_Amt'].sum() / df['Total_Value'].sum() * 100
        st.metric("Rate", f"{rate:.1f}%")
    
    st.markdown("---")
    
    for brand in BRANDS.keys():
        brand_df = df[df['Brand'] == brand]
        if not brand_df.empty:
            st.markdown(f"**{brand}**")
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                st.metric("Sales", f"{brand_df['Total_Value'].sum():,.0f}₺")
            with col_b2:
                st.metric("Comm", f"{brand_df['Commission_Amt'].sum():,.0f}₺")
            with col_b3:
                owed = brand_df['Brand_Payout'].sum()
                paid_df = df_pay[df_pay['Brand'] == brand]
                paid = paid_df['Amount'].sum() if not paid_df.empty else 0
                st.metric("Balance", f"{(owed - paid):,.0f}₺")

def render_export():
    st.markdown("### 📥 Export")
    
    df_orders = load_orders()
    df_pay = load_payments()
    
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        st.markdown("**Orders**")
        if not df_orders.empty:
            csv = export_to_csv(df_orders)
            st.download_button(
                "📄 Download",
                csv,
                f"orders_{datetime.now().strftime('%Y%m%d')}.csv",
                key="dl_orders"
            )
    
    with col_e2:
        st.markdown("**Commission**")
        if not df_orders.empty:
            comm = df_orders[['Order_ID', 'Time', 'Brand', 'Commission_Amt', 'Status']]
            csv = export_to_csv(comm)
            st.download_button(
                "💰 Download",
                csv,
                f"commission_{datetime.now().strftime('%Y%m%d')}.csv",
                key="dl_comm"
            )
    
    with col_e3:
        st.markdown("**Payments**")
        if not df_pay.empty:
            csv = export_to_csv(df_pay)
            st.download_button(
                "💳 Download",
                csv,
                f"payments_{datetime.now().strftime('%Y%m%d')}.csv",
                key="dl_pay"
            )

def render_analytics():
    st.markdown("### 📊 Analytics")
    
    df = load_orders()
    if df.empty:
        st.info("No data")
        return
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown("**Sales by Brand**")
        brand_sales = df.groupby('Brand')['Total_Value'].sum()
        st.bar_chart(brand_sales)
    
    with col_a2:
        st.markdown("**Orders by Brand**")
        brand_orders = df['Brand'].value_counts()
        st.bar_chart(brand_orders)
    
    st.markdown("**Status Distribution**")
    status_dist = df['Status'].value_counts()
    st.bar_chart(status_dist)
    
    if len(df) > 5:
        st.markdown("**Orders Over Time**")
        df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
        df['Date'] = df['Time'].dt.date
        daily = df.groupby('Date').size()
        st.line_chart(daily)

def render_logs():
    st.markdown("### 📜 Logs")
    
    try:
        df = pd.read_csv(CSV_LOGS) if os.path.exists(CSV_LOGS) else pd.DataFrame()
        
        if df.empty:
            st.info("No logs")
            return
        
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            actions = df['Action'].unique().tolist() if 'Action' in df.columns else []
            action_f = st.multiselect("Action", actions, key="log_act")
        with col_l2:
            date_f = st.date_input("Date", datetime.now(), key="log_date")
        
        filtered = df.copy()
        
        if action_f:
            filtered = filtered[filtered['Action'].isin(action_f)]
        
        if date_f:
            filtered['Time'] = pd.to_datetime(filtered['Time'], errors='coerce')
            filtered = filtered[filtered['Time'].dt.date == date_f]
        
        st.dataframe(filtered.sort_values('Time', ascending=False), use_container_width=True, hide_index=True)
        st.markdown(f"**{len(filtered)}** logs")
        
    except Exception as e:
        st.error(f"Error: {e}")

# ============================================================================
# 10. MAIN
# ============================================================================

if __name__ == "__main__":
    if not st.session_state.admin_logged_in:
        login_screen()
    else:
        dashboard()
