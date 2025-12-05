import streamlit as st
import pandas as pd
import numpy as np
import os
import time
from datetime import datetime
import urllib.parse

# ============================================================================
# 1. SYSTEM CONFIGURATION & ASSETS
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Constants ---
CSV_FILE = "natuvisio_db.csv"
ADMIN_PASS = "admin2025"
CURRENCY = "₺"

# --- Brand Metadata (Source of Truth) ---
BRANDS = {
    "HAKI HEAL": {"color": "#4ECDC4", "commission": 0.15, "phone": "905551234567"},
    "AURORACO": {"color": "#FF6B6B", "commission": 0.20, "phone": "905559876543"},
    "LONGEVICALS": {"color": "#95E1D3", "commission": 0.12, "phone": "905551122334"}
}

# --- Premium Design System ---
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;600&display=swap');
        
        /* BACKGROUND & MAIN */
        .stApp {
            background-image: linear-gradient(rgba(15, 23, 42, 0.92), rgba(15, 23, 42, 0.95)), 
                              url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }
        
        /* GLASS CARDS */
        .glass-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .glass-card:hover {
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }

        /* GLOW ALERTS */
        .glow-red { border-left: 3px solid #EF4444; box-shadow: 0 0 15px rgba(239, 68, 68, 0.15); }
        .glow-green { border-left: 3px solid #10B981; box-shadow: 0 0 15px rgba(16, 185, 129, 0.15); }
        .glow-gold { border-left: 3px solid #F59E0B; box-shadow: 0 0 15px rgba(245, 158, 11, 0.15); }

        /* TYPOGRAPHY */
        h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.03em; }
        
        /* UTILS */
        .metric-val { font-family: 'Space Grotesk'; font-size: 28px; font-weight: 700; }
        .metric-lbl { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7; }
        .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; text-transform: uppercase; }
        
        /* HIDE STREAMLIT ELEMENTS */
        #MainMenu, header, footer { visibility: hidden; }
        .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 2. DATA ENGINE (The "Stripe" Logic)
# ============================================================================

def init_db():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=[
            "order_id", "timestamp", "brand", "customer", "phone", "address", 
            "items", "total_val", "comm_rate", "comm_amt", "payout_amt", 
            "status", "whatsapp_sent", "tracking", "notes"
        ])
        df.to_csv(CSV_FILE, index=False)

def get_data():
    try:
        return pd.read_csv(CSV_FILE)
    except:
        init_db()
        return pd.read_csv(CSV_FILE)

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

def create_order(brand, cust, phone, addr, items, total, notes=""):
    df = get_data()
    
    # Financial Logic
    rate = BRANDS[brand]['commission']
    comm = total * rate
    payout = total - comm
    
    new_order = {
        "order_id": f"NV-{int(time.time())}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "brand": brand,
        "customer": cust,
        "phone": phone,
        "address": addr,
        "items": items,
        "total_val": total,
        "comm_rate": rate,
        "comm_amt": comm,
        "payout_amt": payout,
        "status": "New",
        "whatsapp_sent": "NO",
        "tracking": "",
        "notes": notes
    }
    
    df = pd.concat([df, pd.DataFrame([new_order])], ignore_index=True)
    save_data(df)
    return new_order['order_id']

# ============================================================================
# 3. UI COMPONENTS
# ============================================================================

def card_metric(label, value, color="#ffffff"):
    st.markdown(f"""
    <div class="glass-card" style="padding: 15px; text-align: center; border-top: 2px solid {color};">
        <div class="metric-lbl" style="color: {color};">{label}</div>
        <div class="metric-val">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def render_order_card(row, is_admin=True):
    # Dynamic Class for Glow
    glow = "glow-red" if row['status'] == "New" else "glow-gold" if row['status'] == "Notified" else "glow-green"
    
    with st.container():
        st.markdown(f"""
        <div class="glass-card {glow}">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <h3 style="margin:0;">{row['order_id']}</h3>
                    <span style="font-size: 12px; opacity: 0.6;">{row['timestamp']} • {row['brand']}</span>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 700; font-size: 20px;">{row['total_val']:,.0f} {CURRENCY}</div>
                    <div style="font-size: 12px; color: #10B981;">Payout: {row['payout_amt']:,.0f} {CURRENCY}</div>
                </div>
            </div>
            <div style="margin-top: 15px; font-size: 14px; opacity: 0.8;">
                <strong>📦 {row['items']}</strong><br>
                👤 {row['customer']} ({row['phone']})<br>
                📍 {row['address']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# 4. PANELS (Views)
# ============================================================================

def founder_hq():
    st.markdown("## 🏔️ Founder Command Center")
    df = get_data()
    
    # --- METRICS ---
    total_rev = df['total_val'].sum() if not df.empty else 0
    total_comm = df['comm_amt'].sum() if not df.empty else 0
    pending = len(df[df['status'] == "New"])
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: card_metric("Total Revenue", f"{total_rev:,.0f} {CURRENCY}", "#4ECDC4")
    with c2: card_metric("Net Commission", f"{total_comm:,.0f} {CURRENCY}", "#FF6B6B")
    with c3: card_metric("Action Needed", pending, "#EF4444")
    with c4: card_metric("Total Orders", len(df), "#95E1D3")
    
    # --- TABS ---
    t1, t2, t3 = st.tabs(["🔥 OPERATIONS", "📝 CREATE ORDER", "📊 DATA"])
    
    # Operations Tab
    with t1:
        if pending > 0:
            st.error(f"🚨 {pending} Orders require immediate dispatch notification!")
        
        # Display Active Orders
        active_orders = df[df['status'].isin(["New", "Notified"])]
        if active_orders.empty:
            st.success("✅ All systems clear. No pending orders.")
        else:
            for idx, row in active_orders.iterrows():
                render_order_card(row)
                
                c_act1, c_act2 = st.columns([1, 4])
                
                # WhatsApp Logic
                phone_clean = BRANDS[row['brand']]['phone']
                msg = urllib.parse.quote(f"🚨 NEW ORDER: {row['order_id']}\n{row['items']}\nShip to: {row['address']}")
                wa_link = f"https://wa.me/{phone_clean}?text={msg}"
                
                with c_act1:
                    st.link_button("📲 WhatsApp", wa_link)
                with c_act2:
                    if row['status'] == "New":
                        if st.button("✅ Mark Notified", key=f"ntf_{row['order_id']}"):
                            df.at[idx, 'status'] = "Notified"
                            save_data(df)
                            st.rerun()
                    elif row['status'] == "Notified":
                        tracking = st.text_input("Tracking #", key=f"trk_{row['order_id']}")
                        if st.button("🚚 Dispatch", key=f"dsp_{row['order_id']}"):
                            if tracking:
                                df.at[idx, 'status'] = "Dispatched"
                                df.at[idx, 'tracking'] = tracking
                                save_data(df)
                                st.rerun()

    # Create Order Tab
    with t2:
        with st.form("new_order"):
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                brand = st.selectbox("Brand", list(BRANDS.keys()))
                cust = st.text_input("Customer Name")
                phone = st.text_input("Phone")
            with c_f2:
                items = st.text_input("Items (e.g. 2x Matcha)")
                total = st.number_input("Total Value", min_value=0.0)
                addr = st.text_area("Address")
            
            if st.form_submit_button("🚀 Launch Order"):
                create_order(brand, cust, phone, addr, items, total)
                st.success("Order Created!")
                time.sleep(1)
                st.rerun()

    # Data Tab
    with t3:
        st.dataframe(df, use_container_width=True)

def partner_portal(brand_name):
    st.markdown(f"## 📦 {brand_name} Partner Portal")
    df = get_data()
    my_orders = df[df['brand'] == brand_name]
    
    # Financials
    my_rev = my_orders['payout_amt'].sum() if not my_orders.empty else 0
    to_ship = len(my_orders[my_orders['status'] == "Notified"])
    
    c1, c2 = st.columns(2)
    with c1: card_metric("My Revenue", f"{my_rev:,.0f} {CURRENCY}", BRANDS[brand_name]['color'])
    with c2: card_metric("Pending Ship", to_ship, "#EF4444")
    
    st.markdown("### 📋 My Orders")
    if my_orders.empty:
        st.info("No orders yet.")
    else:
        st.dataframe(my_orders[['order_id', 'timestamp', 'items', 'status', 'tracking']], use_container_width=True)

# ============================================================================
# 5. MAIN APP ROUTER
# ============================================================================

def main():
    load_css()
    init_db()
    
    # --- LOGIN SCREEN ---
    if 'user_role' not in st.session_state:
        st.markdown("<div style='height: 20vh'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,1,1])
        with c2:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 40px;">🏔️</div>
                <h2>NATUVISIO OS</h2>
                <p style="opacity: 0.6;">Secure Logistics Access</p>
            </div>
            """, unsafe_allow_html=True)
            
            pwd = st.text_input("Enter Passkey", type="password")
            
            if st.button("AUTHENTICATE"):
                if pwd == ADMIN_PASS:
                    st.session_state.user_role = "ADMIN"
                    st.rerun()
                elif pwd == "aurora123":
                    st.session_state.user_role = "AURORACO"
                    st.rerun()
                elif pwd == "haki123":
                    st.session_state.user_role = "HAKI HEAL"
                    st.rerun()
                elif pwd == "long123":
                    st.session_state.user_role = "LONGEVICALS"
                    st.rerun()
                else:
                    st.error("Access Denied")
        return

    # --- LOGGED IN VIEW ---
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_role}")
        if st.button("LOGOUT"):
            del st.session_state.user_role
            st.rerun()
            
    # Route
    if st.session_state.user_role == "ADMIN":
        founder_hq()
    else:
        partner_portal(st.session_state.user_role)

if __name__ == "__main__":
    main()
