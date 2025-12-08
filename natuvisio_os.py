import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO ADMIN OS - COMPLETE OPERATING SYSTEM
# Full Integration: Logistics + Financials + Analytics + Approvals
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Admin OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CONFIGURATION
# ============================================================================

ADMIN_PASS = "admin2025"
CSV_ORDERS = "orders_master.csv"
CSV_PAYMENTS = "brand_payments.csv"

# Fibonacci Design Constants
FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

# Brand Configuration with Commission Rates
BRANDS = {
    "HAKI HEAL": {
        "commission": 0.15,  # 15%
        "phone": "601158976276",
        "color": "#4ECDC4",
        "iban": "TR90 0006 1000 0000 1234 5678 90",
        "products": {
            "HAKI HEAL CREAM": {"sku": "SKU-HAKI-CRM", "price": 450},
            "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY", "price": 380},
            "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP", "price": 120}
        }
    },
    "AURORACO": {
        "commission": 0.20,  # 20%
        "phone": "601158976276",
        "color": "#FF6B6B",
        "iban": "TR90 0006 2000 0000 9876 5432 10",
        "products": {
            "AURORACO MATCHA": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO CACAO": {"sku": "SKU-AUR-CACAO", "price": 550},
            "AURORACO SUPER": {"sku": "SKU-AUR-SUPER", "price": 800}
        }
    },
    "LONGEVICALS": {
        "commission": 0.12,  # 12%
        "phone": "601158976276",
        "color": "#95E1D3",
        "iban": "TR90 0001 5000 0000 1122 3344 55",
        "products": {
            "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
            "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
        }
    }
}

# ============================================================================
# PREMIUM STYLING
# ============================================================================

def get_svg_icon(name, size=24, color="#ffffff"):
    """Premium SVG icons"""
    icons = {
        "dashboard": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
        "orders": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M20 7H4L2 17H22L20 7Z"/><path d="M9 11V6C9 4.34315 10.3431 3 12 3C13.6569 3 15 4.34315 15 6V11"/></svg>',
        "truck": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
        "money": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/></svg>',
        "chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3"><path d="M20 6L9 17L4 12"/></svg>',
        "alert": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M12 2L2 20H22L12 2Z"/><line x1="12" y1="9" x2="12" y2="13"/><circle cx="12" cy="17" r="1"/></svg>',
        "whatsapp": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
    }
    return icons.get(name, "")

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* CORE THEME */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    #MainMenu, header, footer {{ visibility: hidden; }}
    
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.92)), 
                    url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Inter', -apple-system, sans-serif;
        color: #ffffff;
    }}
    
    .main {{ padding: {FIBO['md']}px; }}
    .block-container {{ padding-top: {FIBO['md']}px !important; max-width: 100% !important; }}

    /* GLASS CARDS */
    .glass-card {{
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur({FIBO['md']}px) saturate(180%);
        -webkit-backdrop-filter: blur({FIBO['md']}px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: {FIBO['sm']}px;
        padding: {FIBO['md']}px;
        margin-bottom: {FIBO['sm']}px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.15);
    }}

    /* TYPOGRAPHY */
    h1, h2, h3, h4, h5 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }}
    
    /* METRICS */
    .metric-card {{
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur({FIBO['sm']}px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: {FIBO['sm']}px;
        padding: {FIBO['sm']}px;
        text-align: center;
        transition: transform 0.3s ease;
    }}
    
    .metric-card:hover {{ transform: translateY(-4px); }}
    
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
        color: rgba(255, 255, 255, 0.6);
        font-weight: 600;
    }}

    /* STATUS BADGES */
    .status-badge {{
        display: inline-block;
        padding: 6px {FIBO['sm']}px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}
    
    .status-pending {{
        background: rgba(251, 191, 36, 0.2);
        color: #FCD34D;
        border: 1px solid rgba(251, 191, 36, 0.4);
    }}
    
    .status-notified {{
        background: rgba(59, 130, 246, 0.2);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.4);
    }}
    
    .status-dispatched {{
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }}
    
    .status-completed {{
        background: rgba(139, 92, 246, 0.2);
        color: #A78BFA;
        border: 1px solid rgba(139, 92, 246, 0.4);
    }}

    /* ORDER CARDS WITH GLOW */
    .order-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur({FIBO['sm']}px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: {FIBO['sm']}px;
        padding: {FIBO['md']}px;
        margin-bottom: {FIBO['sm']}px;
        position: relative;
        transition: all 0.3s ease;
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
    
    @keyframes pulse-red {{
        0%, 100% {{ box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }}
        50% {{ box-shadow: 0 0 40px rgba(239, 68, 68, 0.5); }}
    }}

    /* TIMELINE */
    .timeline-container {{
        display: flex;
        justify-content: space-between;
        position: relative;
        margin: {FIBO['sm']}px 0;
        padding: {FIBO['sm']}px 0;
    }}
    
    .timeline-line {{
        position: absolute;
        top: {FIBO['sm']}px;
        left: 0;
        width: 100%;
        height: 2px;
        background: rgba(255, 255, 255, 0.1);
        z-index: 0;
    }}
    
    .timeline-step {{
        position: relative;
        z-index: 1;
        text-align: center;
        flex: 1;
    }}
    
    .timeline-dot {{
        width: {FIBO['sm']}px;
        height: {FIBO['sm']}px;
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        margin: 0 auto {FIBO['xs']}px;
        transition: all 0.3s ease;
    }}
    
    .timeline-step.active .timeline-dot {{
        background: #4ECDC4;
        border-color: #4ECDC4;
        box-shadow: 0 0 15px #4ECDC4;
    }}
    
    .timeline-step-label {{
        font-size: 10px;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .timeline-step.active .timeline-step-label {{
        color: #4ECDC4;
        font-weight: 700;
    }}

    /* BUTTONS */
    .stButton > button {{
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: {FIBO['xs']}px !important;
        padding: {FIBO['xs']}px {FIBO['md']}px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: {FIBO['sm']}px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3) !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #44A08D 0%, #4ECDC4 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(78, 205, 196, 0.4) !important;
    }}

    /* INPUTS */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {{
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: {FIBO['xs']}px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {{
        background: rgba(0, 0, 0, 0.4) !important;
        border-color: rgba(78, 205, 196, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.1) !important;
    }}

    /* DATA TABLES */
    .dataframe {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur({FIBO['sm']}px);
        border-radius: {FIBO['xs']}px !important;
    }}
    
    .dataframe thead tr th {{
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-bottom: 2px solid rgba(78, 205, 196, 0.3) !important;
    }}
    
    .dataframe tbody tr td {{
        background: rgba(255, 255, 255, 0.02) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }}
    
    .dataframe tbody tr:hover td {{
        background: rgba(255, 255, 255, 0.06) !important;
    }}

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {{
        gap: {FIBO['xs']}px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: {FIBO['xs']}px;
        padding: {FIBO['xs']}px {FIBO['sm']}px;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 600;
        border: 1px solid transparent;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: rgba(78, 205, 196, 0.15) !important;
        color: #4ECDC4 !important;
        border-color: rgba(78, 205, 196, 0.3) !important;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def init_databases():
    """Initialize all database files"""
    
    # Orders Master Database
    if not os.path.exists(CSV_ORDERS):
        df_orders = pd.DataFrame(columns=[
            'Order_ID', 'Timestamp', 'Brand', 'Customer_Name', 'Customer_Phone', 
            'Customer_Address', 'Items', 'Total_Value', 'Commission_Rate', 
            'Commission_Amount', 'Brand_Payout', 'Status', 'WhatsApp_Sent',
            'Tracking_Number', 'Notes'
        ])
        df_orders.to_csv(CSV_ORDERS, index=False)
    
    # Brand Payments Database
    if not os.path.exists(CSV_PAYMENTS):
        df_payments = pd.DataFrame(columns=[
            'Payment_ID', 'Timestamp', 'Brand', 'Amount', 'Order_IDs', 
            'Payment_Method', 'Reference', 'Notes'
        ])
        df_payments.to_csv(CSV_PAYMENTS, index=False)

def load_orders():
    """Load orders database"""
    return pd.read_csv(CSV_ORDERS)

def save_order(order_data):
    """Save new order to database"""
    df = load_orders()
    new_df = pd.DataFrame([order_data])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(CSV_ORDERS, index=False)
    return df

def update_orders(df):
    """Update orders database"""
    df.to_csv(CSV_ORDERS, index=False)

def load_payments():
    """Load payments database"""
    return pd.read_csv(CSV_PAYMENTS)

def save_payment(payment_data):
    """Save new payment"""
    df = load_payments()
    new_df = pd.DataFrame([payment_data])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(CSV_PAYMENTS, index=False)
    return df

# ============================================================================
# AUTHENTICATION
# ============================================================================

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

def login_screen():
    """Admin login interface"""
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['xl']}px;">
            <div style="font-size: {FIBO['xl']}px; margin-bottom: {FIBO['sm']}px;">🏔️</div>
            <h2 style="margin-bottom: {FIBO['xs']}px;">ADMIN OS</h2>
            <p style="color: rgba(255, 255, 255, 0.6); font-size: 12px; letter-spacing: 0.1em;">
                NATUVISIO LOGISTICS COMMAND
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        password = st.text_input("Access Key", type="password", key="login_pass")
        
        if st.button("🔓 UNLOCK SYSTEM", use_container_width=True):
            if password == ADMIN_PASS:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ ACCESS DENIED")

# ============================================================================
# METRICS & ANALYTICS
# ============================================================================

def get_dashboard_metrics():
    """Calculate real-time dashboard metrics"""
    df = load_orders()
    
    if df.empty:
        return {
            'total_orders': 0,
            'total_revenue': 0,
            'total_commission': 0,
            'pending_approval': 0,
            'pending_dispatch': 0,
            'today_orders': 0
        }
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    today = datetime.now().date()
    
    return {
        'total_orders': len(df),
        'total_revenue': df['Total_Value'].sum(),
        'total_commission': df['Commission_Amount'].sum(),
        'pending_approval': len(df[df['WhatsApp_Sent'] == 'NO']),
        'pending_dispatch': len(df[df['Status'] == 'Notified']),
        'today_orders': len(df[df['Timestamp'].dt.date == today])
    }

def get_brand_analytics():
    """Get analytics by brand"""
    df = load_orders()
    
    if df.empty:
        return {}
    
    analytics = {}
    for brand in BRANDS.keys():
        brand_df = df[df['Brand'] == brand]
        analytics[brand] = {
            'orders': len(brand_df),
            'revenue': brand_df['Total_Value'].sum(),
            'commission': brand_df['Commission_Amount'].sum(),
            'payout': brand_df['Brand_Payout'].sum()
        }
    
    return analytics

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def admin_dashboard():
    """Main admin dashboard interface"""
    
    # Header
    col_h1, col_h2 = st.columns([6, 1])
    
    with col_h1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: {FIBO['sm']}px;">
            {get_svg_icon('dashboard', FIBO['lg'], '#4ECDC4')}
            <div>
                <h1 style="margin: 0; font-size: {FIBO['xl']}px;">ADMIN OS</h1>
                <span style="font-size: 12px; color: rgba(255, 255, 255, 0.6); letter-spacing: 0.1em;">
                    LOGISTICS COMMAND CENTER
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h2:
        if st.button("🚪 LOGOUT"):
            st.session_state.admin_logged_in = False
            st.rerun()
    
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # Main Navigation Tabs
    tabs = st.tabs([
        "📊 Dashboard",
        "🚀 New Order",
        "📦 Orders",
        "✅ Processing",
        "💰 Financials",
        "📈 Analytics",
        "💳 Payments"
    ])
    
    # ========================================================================
    # TAB 1: DASHBOARD
    # ========================================================================
    
    with tabs[0]:
        metrics = get_dashboard_metrics()
        
        # Metrics Row
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{metrics['total_orders']}</div>
                <div class="metric-label">Total Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{metrics['total_revenue']:,.0f}₺</div>
                <div class="metric-label">Total Revenue</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{metrics['total_commission']:,.0f}₺</div>
                <div class="metric-label">Commission</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card" style="border-top: 3px solid #EF4444;">
                <div class="metric-value" style="color: #EF4444;">{metrics['pending_approval']}</div>
                <div class="metric-label">Pending Approval</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="metric-card" style="border-top: 3px solid #F59E0B;">
                <div class="metric-value" style="color: #F59E0B;">{metrics['pending_dispatch']}</div>
                <div class="metric-label">Pending Dispatch</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown(f"""
            <div class="metric-card" style="border-top: 3px solid #10B981;">
                <div class="metric-value" style="color: #10B981;">{metrics['today_orders']}</div>
                <div class="metric-label">Today</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
        
        # Brand Performance
        st.markdown("### 📊 Brand Performance")
        
        brand_analytics = get_brand_analytics()
        
        if brand_analytics:
            col1, col2, col3 = st.columns(3)
            
            for idx, (brand, data) in enumerate(brand_analytics.items()):
                col = [col1, col2, col3][idx]
                brand_color = BRANDS[brand]['color']
                
                with col:
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4 style="color: {brand_color}; margin-bottom: {FIBO['sm']}px;">{brand}</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: {FIBO['sm']}px;">
                            <div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700;">{data['orders']}</div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.5);">ORDERS</div>
                            </div>
                            <div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700;">{data['revenue']:,.0f}₺</div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.5);">REVENUE</div>
                            </div>
                            <div>
                                <div style="font-size: {FIBO['sm']}px; font-weight: 700; color: #4ECDC4;">{data['commission']:,.0f}₺</div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.5);">COMMISSION</div>
                            </div>
                            <div>
                                <div style="font-size: {FIBO['sm']}px; font-weight: 700; color: #95E1D3;">{data['payout']:,.0f}₺</div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.5);">BRAND PAYOUT</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No data yet. Create your first order!")
        
        # Recent Orders
        st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
        st.markdown("### 📋 Recent Orders")
        
        df_orders = load_orders()
        if not df_orders.empty:
            recent = df_orders.sort_values('Timestamp', ascending=False).head(10)
            st.dataframe(
                recent[['Order_ID', 'Timestamp', 'Brand', 'Customer_Name', 'Total_Value', 'Status']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No orders yet.")
    
    # ========================================================================
    # TAB 2: NEW ORDER
    # ========================================================================
    
    with tabs[1]:
        st.markdown("### 🚀 Create New Order")
        
        if 'cart' not in st.session_state:
            st.session_state.cart = []
        if 'brand_lock' not in st.session_state:
            st.session_state.brand_lock = None
        
        col_left, col_right = st.columns([1.618, 1])
        
        with col_left:
            # Customer Information
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 👤 Customer Information")
            
            col_n, col_p = st.columns(2)
            with col_n:
                cust_name = st.text_input("Full Name", key="new_cust_name")
            with col_p:
                cust_phone = st.text_input("Phone (+90...)", key="new_cust_phone")
            
            cust_address = st.text_area("Delivery Address", key="new_cust_addr", height=89)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Product Selection
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🛒 Product Selection")
            
            # Brand Lock
            if st.session_state.cart:
                st.markdown(f"""
                <div style="background: rgba(78, 205, 196, 0.1); border: 1px solid rgba(78, 205, 196, 0.3); 
                     border-radius: {FIBO['xs']}px; padding: {FIBO['xs']}px {FIBO['sm']}px; margin-bottom: {FIBO['sm']}px;">
                    <span style="color: #4ECDC4;">🔒 Locked to: <strong>{st.session_state.brand_lock}</strong></span>
                </div>
                """, unsafe_allow_html=True)
                active_brand = st.session_state.brand_lock
            else:
                active_brand = st.selectbox("Select Brand", list(BRANDS.keys()), key="brand_select")
            
            # Product Selection
            products = list(BRANDS[active_brand]['products'].keys())
            
            col_p, col_q = st.columns([3, 1])
            with col_p:
                selected_product = st.selectbox("Product", products, key="product_select")
            with col_q:
                quantity = st.number_input("Qty", min_value=1, value=1, key="qty_input")
            
            product_data = BRANDS[active_brand]['products'][selected_product]
            
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); border-radius: {FIBO['xs']}px; 
                 padding: {FIBO['xs']}px {FIBO['sm']}px; margin-top: {FIBO['xs']}px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: rgba(255, 255, 255, 0.6);">SKU: {product_data['sku']}</span>
                    <span style="color: #4ECDC4; font-weight: 700;">{product_data['price']} ₺</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("➕ ADD TO CART", key="add_cart"):
                line_total = product_data['price'] * quantity
                comm_rate = BRANDS[active_brand]['commission']
                comm_amt = line_total * comm_rate
                
                st.session_state.cart.append({
                    'brand': active_brand,
                    'product': selected_product,
                    'sku': product_data['sku'],
                    'qty': quantity,
                    'price': product_data['price'],
                    'subtotal': line_total,
                    'comm_rate': comm_rate,
                    'comm_amt': comm_amt,
                    'brand_payout': line_total - comm_amt
                })
                st.session_state.brand_lock = active_brand
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📦 Cart Review")
            
            if st.session_state.cart:
                # Display cart items
                for idx, item in enumerate(st.session_state.cart):
                    st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.05); border-radius: {FIBO['xs']}px; 
                         padding: {FIBO['sm']}px; margin-bottom: {FIBO['xs']}px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: {FIBO['xs']}px;">
                            <div>
                                <div style="font-weight: 600;">{item['product']}</div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5);">
                                    {item['sku']} × {item['qty']}
                                </div>
                            </div>
                            <div style="font-weight: 700; color: #4ECDC4;">{item['subtotal']}₺</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Calculate totals
                total_value = sum(item['subtotal'] for item in st.session_state.cart)
                total_commission = sum(item['comm_amt'] for item in st.session_state.cart)
                total_payout = sum(item['brand_payout'] for item in st.session_state.cart)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(78, 205, 196, 0.2), rgba(149, 225, 211, 0.1)); 
                     border: 1px solid rgba(78, 205, 196, 0.3); border-radius: {FIBO['xs']}px; 
                     padding: {FIBO['sm']}px; margin-top: {FIBO['sm']}px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: {FIBO['xs']}px;">
                        <span>Total Value:</span>
                        <span style="font-weight: 700; font-size: {FIBO['md']}px;">{total_value:,.0f}₺</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: rgba(255,255,255,0.7); margin-bottom: 4px;">
                        <span>Commission ({BRANDS[st.session_state.brand_lock]['commission']*100}%):</span>
                        <span>{total_commission:,.0f}₺</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: rgba(255,255,255,0.7);">
                        <span>Brand Payout:</span>
                        <span>{total_payout:,.0f}₺</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<div style='height: {FIBO['sm']}px'></div>", unsafe_allow_html=True)
                
                priority = st.selectbox(
                    "Order Priority",
                    ["Standard", "🚨 URGENT", "🧊 Cold Chain"],
                    key="priority_select"
                )
                
                if st.button("⚡ CREATE ORDER", type="primary", use_container_width=True, key="create_order"):
                    if cust_name and cust_phone:
                        # Generate Order ID
                        order_id = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
                        
                        # Prepare items string
                        items_str = ", ".join([f"{i['product']} (x{i['qty']})" for i in st.session_state.cart])
                        
                        # Save order
                        order_data = {
                            'Order_ID': order_id,
                            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'Brand': st.session_state.brand_lock,
                            'Customer_Name': cust_name,
                            'Customer_Phone': cust_phone,
                            'Customer_Address': cust_address,
                            'Items': items_str,
                            'Total_Value': total_value,
                            'Commission_Rate': BRANDS[st.session_state.brand_lock]['commission'],
                            'Commission_Amount': total_commission,
                            'Brand_Payout': total_payout,
                            'Status': 'Pending',
                            'WhatsApp_Sent': 'NO',
                            'Tracking_Number': '',
                            'Notes': priority
                        }
                        
                        save_order(order_data)
                        
                        st.success(f"✅ Order {order_id} created successfully!")
                        
                        # Clear cart
                        st.session_state.cart = []
                        st.session_state.brand_lock = None
                        
                        st.rerun()
                    else:
                        st.error("⚠️ Please fill in customer name and phone!")
                
                if st.button("🗑️ Clear Cart", key="clear_cart"):
                    st.session_state.cart = []
                    st.session_state.brand_lock = None
                    st.rerun()
            else:
                st.markdown("""
                <div style="text-align: center; padding: {FIBO['xl']}px;">
                    <div style="font-size: {FIBO['xl']}px; opacity: 0.3; margin-bottom: {FIBO['sm']}px;">🛒</div>
                    <div style="color: rgba(255, 255, 255, 0.5);">Cart is empty</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # TAB 3: ALL ORDERS
    # ========================================================================
    
    with tabs[2]:
        st.markdown("### 📦 All Orders")
        
        df = load_orders()
        
        if not df.empty:
            # Filters
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                brand_filter = st.multiselect(
                    "Filter by Brand",
                    options=df['Brand'].unique().tolist(),
                    default=df['Brand'].unique().tolist(),
                    key="orders_brand_filter"
                )
            
            with col_f2:
                status_filter = st.multiselect(
                    "Filter by Status",
                    options=df['Status'].unique().tolist(),
                    default=df['Status'].unique().tolist(),
                    key="orders_status_filter"
                )
            
            with col_f3:
                date_range = st.selectbox(
                    "Date Range",
                    ["All Time", "Today", "This Week", "This Month"],
                    key="orders_date_filter"
                )
            
            # Apply filters
            filtered_df = df[
                (df['Brand'].isin(brand_filter)) &
                (df['Status'].isin(status_filter))
            ].copy()
            
            # Date filtering
            if date_range != "All Time":
                filtered_df['Timestamp'] = pd.to_datetime(filtered_df['Timestamp'])
                today = datetime.now().date()
                
                if date_range == "Today":
                    filtered_df = filtered_df[filtered_df['Timestamp'].dt.date == today]
                elif date_range == "This Week":
                    week_ago = today - timedelta(days=7)
                    filtered_df = filtered_df[filtered_df['Timestamp'].dt.date >= week_ago]
                elif date_range == "This Month":
                    month_ago = today - timedelta(days=30)
                    filtered_df = filtered_df[filtered_df['Timestamp'].dt.date >= month_ago]
            
            st.markdown(f"<div style='height: {FIBO['sm']}px'></div>", unsafe_allow_html=True)
            
            # Display table
            st.dataframe(
                filtered_df.sort_values('Timestamp', ascending=False),
                use_container_width=True,
                hide_index=True
            )
            
            # Summary
            col_s1, col_s2, col_s3 = st.columns(3)
            
            with col_s1:
                st.metric("Filtered Orders", len(filtered_df))
            with col_s2:
                st.metric("Total Value", f"{filtered_df['Total_Value'].sum():,.0f} ₺")
            with col_s3:
                st.metric("Avg Order Value", f"{filtered_df['Total_Value'].mean():,.0f} ₺" if len(filtered_df) > 0 else "0 ₺")
        else:
            st.info("No orders yet. Create your first order!")
    
    # ========================================================================
    # TAB 4: ORDER PROCESSING (with Approval Workflow)
    # ========================================================================
    
    with tabs[3]:
        st.markdown("### ✅ Order Processing & Approval")
        
        df = load_orders()
        
        if not df.empty:
            # Show orders that need action
            for idx, row in df.iterrows():
                # Determine card style based on WhatsApp status
                card_class = "order-card-red" if row['WhatsApp_Sent'] == 'NO' else "order-card-green"
                
                st.markdown(f"""
                <div class="order-card {card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: {FIBO['sm']}px;">
                        <div>
                            <h3 style="margin: 0;">{row['Order_ID']}</h3>
                            <div style="margin-top: {FIBO['xs']}px;">
                                <span class="status-badge status-{row['Status'].lower()}">{row['Status']}</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <h3 style="margin: 0;">{row['Total_Value']:,.0f} ₺</h3>
                            <div style="font-size: 11px; color: rgba(255, 255, 255, 0.5); margin-top: 4px;">
                                {row['Timestamp']}
                            </div>
                        </div>
                    </div>
                    
                    <div style="background: rgba(0, 0, 0, 0.2); border-radius: {FIBO['xs']}px; padding: {FIBO['sm']}px; margin-bottom: {FIBO['sm']}px;">
                        <div style="margin-bottom: {FIBO['xs']}px;">
                            <strong>Brand:</strong> <span style="color: {BRANDS[row['Brand']]['color']};">{row['Brand']}</span>
                        </div>
                        <div style="margin-bottom: {FIBO['xs']}px;">
                            <strong>Customer:</strong> {row['Customer_Name']} | {row['Customer_Phone']}
                        </div>
                        <div style="margin-bottom: {FIBO['xs']}px;">
                            <strong>Address:</strong> {row['Customer_Address']}
                        </div>
                        <div style="margin-bottom: {FIBO['xs']}px;">
                            <strong>Items:</strong> {row['Items']}
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: {FIBO['xs']}px; margin-top: {FIBO['sm']}px; padding-top: {FIBO['sm']}px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5);">COMMISSION</div>
                                <div style="font-weight: 700; color: #4ECDC4;">{row['Commission_Amount']:,.0f}₺</div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5);">BRAND PAYOUT</div>
                                <div style="font-weight: 700; color: #95E1D3;">{row['Brand_Payout']:,.0f}₺</div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5);">RATE</div>
                                <div style="font-weight: 700;">{row['Commission_Rate']*100:.0f}%</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Order Status Timeline
                steps = ["Pending", "Notified", "Dispatched", "Completed"]
                current_idx = steps.index(row['Status']) if row['Status'] in steps else 0
                
                timeline_html = '<div class="timeline-container"><div class="timeline-line"></div>'
                for step_idx, step in enumerate(steps):
                    active_class = "active" if step_idx <= current_idx else ""
                    timeline_html += f'''
                    <div class="timeline-step {active_class}">
                        <div class="timeline-dot"></div>
                        <div class="timeline-step-label">{step}</div>
                    </div>
                    '''
                timeline_html += '</div>'
                st.markdown(timeline_html, unsafe_allow_html=True)
                
                # Action Buttons
                col_a1, col_a2, col_a3 = st.columns(3)
                
                with col_a1:
                    if row['WhatsApp_Sent'] == 'NO':
                        # Generate WhatsApp link
                        phone = BRANDS[row['Brand']]['phone'].replace("+", "").replace(" ", "")
                        message = f"""*NATUVISIO DISPATCH ORDER*
━━━━━━━━━━━━━━━━━━━━
🆔 Order: {row['Order_ID']}
━━━━━━━━━━━━━━━━━━━━

👤 Customer: {row['Customer_Name']}
📞 Phone: {row['Customer_Phone']}
🏠 Address: {row['Customer_Address']}

━━━━━━━━━━━━━━━━━━━━
📦 ITEMS:

{row['Items']}

━━━━━━━━━━━━━━━━━━━━
💰 TOTAL: {row['Total_Value']:,.0f} ₺
💵 Your Payout: {row['Brand_Payout']:,.0f} ₺

⚡ Please pack and ship immediately.
Reply with tracking number."""
                        
                        url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"
                        
                        st.markdown(f"""
                        <a href="{url}" target="_blank" style="text-decoration: none;">
                            <div style="background: linear-gradient(135deg, #25D366, #128C7E); color: white; 
                                 padding: {FIBO['sm']}px; text-align: center; border-radius: {FIBO['xs']}px; 
                                 font-weight: 700; cursor: pointer;">
                                📲 SEND WHATSAPP
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
                        
                        if st.button("✅ Mark as Sent", key=f"approve_{idx}"):
                            df.at[idx, 'WhatsApp_Sent'] = 'YES'
                            df.at[idx, 'Status'] = 'Notified'
                            update_orders(df)
                            st.rerun()
                
                with col_a2:
                    if row['Status'] == 'Notified':
                        tracking = st.text_input("Tracking Number", key=f"track_{idx}")
                        if st.button("📦 Mark Dispatched", key=f"dispatch_{idx}"):
                            if tracking:
                                df.at[idx, 'Tracking_Number'] = tracking
                                df.at[idx, 'Status'] = 'Dispatched'
                                update_orders(df)
                                st.rerun()
                            else:
                                st.error("Enter tracking number!")
                
                with col_a3:
                    if row['Status'] == 'Dispatched':
                        if st.button("✅ Mark Completed", key=f"complete_{idx}"):
                            df.at[idx, 'Status'] = 'Completed'
                            update_orders(df)
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='height: {FIBO['sm']}px'></div>", unsafe_allow_html=True)
        else:
            st.info("No orders to process.")
    
    # ========================================================================
    # TAB 5: FINANCIALS
    # ========================================================================
    
    with tabs[4]:
        st.markdown("### 💰 Financial Dashboard")
        
        df = load_orders()
        
        if not df.empty:
            # Financial Summary
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            
            total_sales = df['Total_Value'].sum()
            total_commission = df['Commission_Amount'].sum()
            total_brand_payout = df['Brand_Payout'].sum()
            
            with col_f1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_sales:,.0f}₺</div>
                    <div class="metric-label">Total Sales</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_f2:
                st.markdown(f"""
                <div class="metric-card" style="border-top: 3px solid #4ECDC4;">
                    <div class="metric-value" style="color: #4ECDC4;">{total_commission:,.0f}₺</div>
                    <div class="metric-label">Total Commission</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_f3:
                st.markdown(f"""
                <div class="metric-card" style="border-top: 3px solid #95E1D3;">
                    <div class="metric-value" style="color: #95E1D3;">{total_brand_payout:,.0f}₺</div>
                    <div class="metric-label">Total Brand Payout</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_f4:
                commission_rate = (total_commission / total_sales * 100) if total_sales > 0 else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{commission_rate:.1f}%</div>
                    <div class="metric-label">Avg Commission Rate</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
            
            # Commission by Brand
            st.markdown("#### 📊 Commission Breakdown by Brand")
            
            for brand in BRANDS.keys():
                brand_df = df[df['Brand'] == brand]
                
                if not brand_df.empty:
                    brand_sales = brand_df['Total_Value'].sum()
                    brand_commission = brand_df['Commission_Amount'].sum()
                    brand_payout = brand_df['Brand_Payout'].sum()
                    brand_color = BRANDS[brand]['color']
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: {FIBO['sm']}px;">
                            <h4 style="margin: 0; color: {brand_color};">{brand}</h4>
                            <span style="font-size: 12px; color: rgba(255, 255, 255, 0.6);">
                                {len(brand_df)} orders
                            </span>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: {FIBO['md']}px;">
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5); margin-bottom: 4px;">
                                    SALES
                                </div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700;">
                                    {brand_sales:,.0f}₺
                                </div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5); margin-bottom: 4px;">
                                    COMMISSION ({BRANDS[brand]['commission']*100:.0f}%)
                                </div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700; color: #4ECDC4;">
                                    {brand_commission:,.0f}₺
                                </div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5); margin-bottom: 4px;">
                                    BRAND PAYOUT
                                </div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700; color: #95E1D3;">
                                    {brand_payout:,.0f}₺
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
            
            # Detailed Financial Table
            st.markdown("#### 📋 Detailed Financial Records")
            
            financial_view = df[[
                'Order_ID', 'Timestamp', 'Brand', 'Total_Value', 
                'Commission_Rate', 'Commission_Amount', 'Brand_Payout', 'Status'
            ]].copy()
            
            st.dataframe(
                financial_view.sort_values('Timestamp', ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No financial data yet.")
    
    # ========================================================================
    # TAB 6: ANALYTICS
    # ========================================================================
    
    with tabs[5]:
        st.markdown("### 📈 Business Analytics")
        
        df = load_orders()
        
        if not df.empty:
            # Revenue Charts
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                st.markdown("#### Sales by Brand")
                brand_sales = df.groupby('Brand')['Total_Value'].sum().sort_values(ascending=False)
                st.bar_chart(brand_sales)
            
            with col_c2:
                st.markdown("#### Orders by Brand")
                brand_orders = df['Brand'].value_counts()
                st.bar_chart(brand_orders)
            
            st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
            
            # Status Distribution
            col_c3, col_c4 = st.columns(2)
            
            with col_c3:
                st.markdown("#### Order Status Distribution")
                status_dist = df['Status'].value_counts()
                st.bar_chart(status_dist)
            
            with col_c4:
                st.markdown("#### Commission vs Payout")
                comparison = pd.DataFrame({
                    'Commission': df.groupby('Brand')['Commission_Amount'].sum(),
                    'Brand Payout': df.groupby('Brand')['Brand_Payout'].sum()
                })
                st.bar_chart(comparison)
            
            # Time Series (if enough data)
            if len(df) > 5:
                st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
                st.markdown("#### Orders Over Time")
                
                df_time = df.copy()
                df_time['Timestamp'] = pd.to_datetime(df_time['Timestamp'])
                df_time['Date'] = df_time['Timestamp'].dt.date
                daily_orders = df_time.groupby('Date').size()
                st.line_chart(daily_orders)
        else:
            st.info("Not enough data for analytics yet.")
    
    # ========================================================================
    # TAB 7: PAYMENTS TO BRANDS
    # ========================================================================
    
    with tabs[6]:
        st.markdown("### 💳 Brand Payment Management")
        
        df_orders = load_orders()
        df_payments = load_payments()
        
        if not df_orders.empty:
            # Payment Summary by Brand
            for brand in BRANDS.keys():
                brand_orders = df_orders[df_orders['Brand'] == brand]
                
                if not brand_orders.empty:
                    total_owed = brand_orders['Brand_Payout'].sum()
                    
                    # Calculate paid amount
                    brand_payments = df_payments[df_payments['Brand'] == brand]
                    total_paid = brand_payments['Amount'].sum() if not brand_payments.empty else 0
                    
                    balance = total_owed - total_paid
                    brand_color = BRANDS[brand]['color']
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: {FIBO['md']}px;">
                            <div>
                                <h3 style="margin: 0; color: {brand_color};">{brand}</h3>
                                <div style="font-size: 12px; color: rgba(255, 255, 255, 0.6); margin-top: 4px;">
                                    {len(brand_orders)} orders • {BRANDS[brand]['iban']}
                                </div>
                            </div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: {FIBO['md']}px; 
                             background: rgba(0, 0, 0, 0.2); border-radius: {FIBO['xs']}px; padding: {FIBO['md']}px;">
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5); margin-bottom: 4px;">
                                    TOTAL OWED
                                </div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700; color: #F59E0B;">
                                    {total_owed:,.0f}₺
                                </div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5); margin-bottom: 4px;">
                                    PAID
                                </div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700; color: #10B981;">
                                    {total_paid:,.0f}₺
                                </div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5); margin-bottom: 4px;">
                                    BALANCE
                                </div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700; color: {'#EF4444' if balance > 0 else '#4ECDC4'};">
                                    {balance:,.0f}₺
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Payment Action
                    with st.expander(f"💸 Record Payment for {brand}"):
                        col_p1, col_p2 = st.columns(2)
                        
                        with col_p1:
                            payment_amount = st.number_input(
                                "Payment Amount",
                                min_value=0.0,
                                max_value=float(balance) if balance > 0 else 0.0,
                                value=float(balance) if balance > 0 else 0.0,
                                key=f"pay_amt_{brand}"
                            )
                        
                        with col_p2:
                            payment_method = st.selectbox(
                                "Payment Method",
                                ["Bank Transfer", "Cash", "Check", "Other"],
                                key=f"pay_method_{brand}"
                            )
                        
                        payment_ref = st.text_input("Reference/Note", key=f"pay_ref_{brand}")
                        
                        if st.button(f"💰 Record Payment", key=f"pay_btn_{brand}"):
                            if payment_amount > 0:
                                payment_id = f"PAY-{datetime.now().strftime('%m%d%H%M%S')}"
                                
                                # Get order IDs for this brand
                                order_ids = ", ".join(brand_orders['Order_ID'].tolist()[:5])  # First 5
                                if len(brand_orders) > 5:
                                    order_ids += f" +{len(brand_orders)-5} more"
                                
                                payment_data = {
                                    'Payment_ID': payment_id,
                                    'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    'Brand': brand,
                                    'Amount': payment_amount,
                                    'Order_IDs': order_ids,
                                    'Payment_Method': payment_method,
                                    'Reference': payment_ref,
                                    'Notes': f"Payment to {brand}"
                                }
                                
                                save_payment(payment_data)
                                st.success(f"✅ Payment {payment_id} recorded successfully!")
                                st.rerun()
                            else:
                                st.error("Please enter a valid amount!")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Payment History
            st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
            st.markdown("### 📜 Payment History")
            
            if not df_payments.empty:
                st.dataframe(
                    df_payments.sort_values('Timestamp', ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No payments recorded yet.")
        else:
            st.info("No orders yet. Create orders first!")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

# Initialize databases
init_databases()

# Check authentication
if not st.session_state.admin_logged_in:
    login_screen()
else:
    admin_dashboard()
