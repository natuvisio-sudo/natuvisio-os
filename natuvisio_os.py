import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os
import io
import time
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO YÖNETİM SİSTEMİ - V6.0 (LIQUID GRADIENT EDITION)
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Admin OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 1. AYARLAR (CONFIG)
# ============================================================================

ADMIN_PASS = "admin2025"
CSV_ORDERS = "orders_complete.csv"
CSV_PAYMENTS = "brand_payments.csv" 
CSV_INVOICES = "brand_invoices.csv" 
CSV_LOGS = "system_logs.csv"
PHI = 1.618

FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

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

# ============================================================================
# 2. İKON SETİ (ICONS)
# ============================================================================

def get_icon(name, color="#ffffff", size=24):
    icons = {
        "mountain": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M3 20L9 8L12 14L15 6L21 20H3Z"/></svg>',
        "alert": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3"><path d="M20 6L9 17L4 12"/></svg>',
        "bill": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><line x1="6" y1="8" x2="6" y2="8"/><line x1="10" y1="8" x2="18" y2="8"/><line x1="6" y1="12" x2="6" y2="12"/><line x1="10" y1="12" x2="18" y2="12"/><line x1="6" y1="16" x2="6" y2="16"/><line x1="10" y1="16" x2="18" y2="16"/></svg>',
        "money": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "clock": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "activity": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
    }
    return icons.get(name, "")

# ============================================================================
# 3. CSS & LIQUID BACKGROUND INJECTION
# ============================================================================

def inject_liquid_background():
    # Embed the full HTML/JS/WebGL code as a background component
    # This runs in an iframe, so we style it to cover the screen
    html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    body, html { margin: 0; padding: 0; overflow: hidden; width: 100%; height: 100%; }
    canvas { display: block; }
  </style>
</head>
<body>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script>
    // --- PASTE YOUR WEBGL JAVASCRIPT HERE (MINIFIED FOR BREVITY) ---
    // (I am including the core logic you provided to make it work)
    
    class TouchTexture {
      constructor() {
        this.size = 64;
        this.width = this.height = this.size;
        this.maxAge = 64;
        this.radius = 0.25 * this.size;
        this.speed = 1 / this.maxAge;
        this.trail = [];
        this.last = null;
        this.initTexture();
      }
      initTexture() {
        this.canvas = document.createElement("canvas");
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        this.ctx = this.canvas.getContext("2d");
        this.ctx.fillStyle = "black";
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.texture = new THREE.Texture(this.canvas);
      }
      update() {
        this.clear();
        let speed = this.speed;
        for (let i = this.trail.length - 1; i >= 0; i--) {
          const point = this.trail[i];
          let f = point.force * speed * (1 - point.age / this.maxAge);
          point.x += point.vx * f;
          point.y += point.vy * f;
          point.age++;
          if (point.age > this.maxAge) {
            this.trail.splice(i, 1);
          } else {
            this.drawPoint(point);
          }
        }
        this.texture.needsUpdate = true;
      }
      clear() {
        this.ctx.fillStyle = "black";
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
      }
      addTouch(point) {
        let force = 0;
        let vx = 0;
        let vy = 0;
        const last = this.last;
        if (last) {
          const dx = point.x - last.x;
          const dy = point.y - last.y;
          if (dx === 0 && dy === 0) return;
          const dd = dx * dx + dy * dy;
          let d = Math.sqrt(dd);
          vx = dx / d;
          vy = dy / d;
          force = Math.min(dd * 20000, 2.0);
        }
        this.last = { x: point.x, y: point.y };
        this.trail.push({ x: point.x, y: point.y, age: 0, force, vx, vy });
      }
      drawPoint(point) {
        const pos = {
          x: point.x * this.width,
          y: (1 - point.y) * this.height
        };
        let intensity = 1;
        if (point.age < this.maxAge * 0.3) {
          intensity = Math.sin((point.age / (this.maxAge * 0.3)) * (Math.PI / 2));
        } else {
          const t = 1 - (point.age - this.maxAge * 0.3) / (this.maxAge * 0.7);
          intensity = -t * (t - 2);
        }
        intensity *= point.force;
        const radius = this.radius;
        let color = `${((point.vx + 1) / 2) * 255}, ${((point.vy + 1) / 2) * 255}, ${intensity * 255}`;
        let offset = this.size * 5;
        this.ctx.shadowOffsetX = offset;
        this.ctx.shadowOffsetY = offset;
        this.ctx.shadowBlur = radius * 1;
        this.ctx.shadowColor = `rgba(${color},${0.2 * intensity})`;
        this.ctx.beginPath();
        this.ctx.fillStyle = "rgba(255,0,0,1)";
        this.ctx.arc(pos.x - offset, pos.y - offset, radius, 0, Math.PI * 2);
        this.ctx.fill();
      }
    }

    class GradientBackground {
      constructor(sceneManager) {
        this.sceneManager = sceneManager;
        this.mesh = null;
        this.uniforms = {
          uTime: { value: 0 },
          uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
          uColor1: { value: new THREE.Vector3(0.945, 0.353, 0.133) },
          uColor2: { value: new THREE.Vector3(0.039, 0.055, 0.153) },
          uColor3: { value: new THREE.Vector3(0.945, 0.353, 0.133) },
          uColor4: { value: new THREE.Vector3(0.039, 0.055, 0.153) },
          uColor5: { value: new THREE.Vector3(0.945, 0.353, 0.133) },
          uColor6: { value: new THREE.Vector3(0.039, 0.055, 0.153) },
          uSpeed: { value: 1.2 },
          uIntensity: { value: 1.8 },
          uTouchTexture: { value: null },
          uGrainIntensity: { value: 0.08 },
          uZoom: { value: 1.0 },
          uDarkNavy: { value: new THREE.Vector3(0.039, 0.055, 0.153) },
          uGradientSize: { value: 1.0 },
          uGradientCount: { value: 6.0 },
          uColor1Weight: { value: 1.0 },
          uColor2Weight: { value: 1.0 }
        };
      }
      init() {
        const viewSize = this.sceneManager.getViewSize();
        const geometry = new THREE.PlaneGeometry(viewSize.width, viewSize.height, 1, 1);
        const material = new THREE.ShaderMaterial({
          uniforms: this.uniforms,
          vertexShader: `varying vec2 vUv;void main(){vec3 pos=position.xyz;gl_Position=projectionMatrix*modelViewMatrix*vec4(pos,1.);vUv=uv;}`,
          fragmentShader: `
            uniform float uTime;uniform vec2 uResolution;uniform vec3 uColor1;uniform vec3 uColor2;uniform vec3 uColor3;uniform vec3 uColor4;uniform vec3 uColor5;uniform vec3 uColor6;uniform float uSpeed;uniform float uIntensity;uniform sampler2D uTouchTexture;uniform float uGrainIntensity;uniform float uZoom;uniform vec3 uDarkNavy;uniform float uGradientSize;uniform float uGradientCount;uniform float uColor1Weight;uniform float uColor2Weight;varying vec2 vUv;
            #define PI 3.14159265359
            float grain(vec2 uv,float time){vec2 grainUv=uv*uResolution*0.5;float grainValue=fract(sin(dot(grainUv+time,vec2(12.9898,78.233)))*43758.5453);return grainValue*2.0-1.0;}
            vec3 getGradientColor(vec2 uv,float time){float gradientRadius=uGradientSize;vec2 center1=vec2(0.5+sin(time*uSpeed*0.4)*0.4,0.5+cos(time*uSpeed*0.5)*0.4);vec2 center2=vec2(0.5+cos(time*uSpeed*0.6)*0.5,0.5+sin(time*uSpeed*0.45)*0.5);vec2 center3=vec2(0.5+sin(time*uSpeed*0.35)*0.45,0.5+cos(time*uSpeed*0.55)*0.45);vec2 center4=vec2(0.5+cos(time*uSpeed*0.5)*0.4,0.5+sin(time*uSpeed*0.4)*0.4);vec2 center5=vec2(0.5+sin(time*uSpeed*0.7)*0.35,0.5+cos(time*uSpeed*0.6)*0.35);vec2 center6=vec2(0.5+cos(time*uSpeed*0.45)*0.5,0.5+sin(time*uSpeed*0.65)*0.5);float dist1=length(uv-center1);float dist2=length(uv-center2);float dist3=length(uv-center3);float dist4=length(uv-center4);float dist5=length(uv-center5);float dist6=length(uv-center6);float influence1=1.0-smoothstep(0.0,gradientRadius,dist1);float influence2=1.0-smoothstep(0.0,gradientRadius,dist2);float influence3=1.0-smoothstep(0.0,gradientRadius,dist3);float influence4=1.0-smoothstep(0.0,gradientRadius,dist4);float influence5=1.0-smoothstep(0.0,gradientRadius,dist5);float influence6=1.0-smoothstep(0.0,gradientRadius,dist6);vec2 rotatedUv1=uv-0.5;float angle1=time*uSpeed*0.15;rotatedUv1=vec2(rotatedUv1.x*cos(angle1)-rotatedUv1.y*sin(angle1),rotatedUv1.x*sin(angle1)+rotatedUv1.y*cos(angle1));rotatedUv1+=0.5;vec2 rotatedUv2=uv-0.5;float angle2=-time*uSpeed*0.12;rotatedUv2=vec2(rotatedUv2.x*cos(angle2)-rotatedUv2.y*sin(angle2),rotatedUv2.x*sin(angle2)+rotatedUv2.y*cos(angle2));rotatedUv2+=0.5;float radialGradient1=length(rotatedUv1-0.5);float radialGradient2=length(rotatedUv2-0.5);float radialInfluence1=1.0-smoothstep(0.0,0.8,radialGradient1);float radialInfluence2=1.0-smoothstep(0.0,0.8,radialGradient2);vec3 color=vec3(0.0);color+=uColor1*influence1*(0.55+0.45*sin(time*uSpeed))*uColor1Weight;color+=uColor2*influence2*(0.55+0.45*cos(time*uSpeed*1.2))*uColor2Weight;color+=uColor3*influence3*(0.55+0.45*sin(time*uSpeed*0.8))*uColor1Weight;color+=uColor4*influence4*(0.55+0.45*cos(time*uSpeed*1.3))*uColor2Weight;color+=uColor5*influence5*(0.55+0.45*sin(time*uSpeed*1.1))*uColor1Weight;color+=uColor6*influence6*(0.55+0.45*cos(time*uSpeed*0.9))*uColor2Weight;color+=mix(uColor1,uColor3,radialInfluence1)*0.45*uColor1Weight;color+=mix(uColor2,uColor4,radialInfluence2)*0.4*uColor2Weight;color=clamp(color,vec3(0.0),vec3(1.0))*uIntensity;float luminance=dot(color,vec3(0.299,0.587,0.114));color=mix(vec3(luminance),color,1.35);color=pow(color,vec3(0.92));float brightness1=length(color);float mixFactor1=max(brightness1*1.2,0.15);color=mix(uDarkNavy,color,mixFactor1);float maxBrightness=1.0;float brightness=length(color);if(brightness>maxBrightness){color=color*(maxBrightness/brightness);}return color;}
            void main(){vec2 uv=vUv;vec4 touchTex=texture2D(uTouchTexture,uv);float vx=-(touchTex.r*2.0-1.0);float vy=-(touchTex.g*2.0-1.0);float intensity=touchTex.b;uv.x+=vx*0.8*intensity;uv.y+=vy*0.8*intensity;vec2 center=vec2(0.5);float dist=length(uv-center);float ripple=sin(dist*20.0-uTime*3.0)*0.04*intensity;float wave=sin(dist*15.0-uTime*2.0)*0.03*intensity;uv+=vec2(ripple+wave);vec3 color=getGradientColor(uv,uTime);float grainValue=grain(uv,uTime);color+=grainValue*uGrainIntensity;float timeShift=uTime*0.5;color.r+=sin(timeShift)*0.02;color.g+=cos(timeShift*1.4)*0.02;color.b+=sin(timeShift*1.2)*0.02;float brightness2=length(color);float mixFactor2=max(brightness2*1.2,0.15);color=mix(uDarkNavy,color,mixFactor2);color=clamp(color,vec3(0.0),vec3(1.0));float maxBrightness=1.0;float brightness=length(color);if(brightness>maxBrightness){color=color*(maxBrightness/brightness);}gl_FragColor=vec4(color,1.0);}
          `
        });
        this.mesh = new THREE.Mesh(geometry, material);
        this.mesh.position.z = 0;
        this.sceneManager.scene.add(this.mesh);
      }
      update(delta) { if (this.uniforms.uTime) this.uniforms.uTime.value += delta; }
      onResize(width, height) {
        const viewSize = this.sceneManager.getViewSize();
        if (this.mesh) { this.mesh.geometry.dispose(); this.mesh.geometry = new THREE.PlaneGeometry(viewSize.width, viewSize.height, 1, 1); }
        if (this.uniforms.uResolution) this.uniforms.uResolution.value.set(width, height);
      }
    }

    class App {
      constructor() {
        this.renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance", alpha: false, stencil: false, depth: false });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.body.appendChild(this.renderer.domElement);
        this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 10000);
        this.camera.position.z = 50;
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0e27);
        this.clock = new THREE.Clock();
        this.touchTexture = new TouchTexture();
        this.gradientBackground = new GradientBackground(this);
        this.gradientBackground.uniforms.uTouchTexture.value = this.touchTexture.texture;
        this.init();
      }
      init() {
        this.gradientBackground.init();
        this.tick();
        window.addEventListener("resize", () => this.onResize());
        window.addEventListener("mousemove", (ev) => this.onMouseMove(ev));
        window.addEventListener("touchmove", (ev) => this.onTouchMove(ev));
      }
      onTouchMove(ev) { const touch = ev.touches[0]; this.onMouseMove({ clientX: touch.clientX, clientY: touch.clientY }); }
      onMouseMove(ev) {
        this.mouse = { x: ev.clientX / window.innerWidth, y: 1 - ev.clientY / window.innerHeight };
        this.touchTexture.addTouch(this.mouse);
      }
      getViewSize() {
        const fovInRadians = (this.camera.fov * Math.PI) / 180;
        const height = Math.abs(this.camera.position.z * Math.tan(fovInRadians / 2) * 2);
        return { width: height * this.camera.aspect, height };
      }
      update(delta) {
        this.touchTexture.update();
        this.gradientBackground.update(delta);
      }
      render() {
        const delta = this.clock.getDelta();
        const clampedDelta = Math.min(delta, 0.1);
        this.renderer.render(this.scene, this.camera);
        this.update(clampedDelta);
      }
      tick() {
        this.render();
        requestAnimationFrame(() => this.tick());
      }
      onResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.gradientBackground.onResize(window.innerWidth, window.innerHeight);
      }
    }
    new App();
  </script>
</body>
</html>
    """
    
    # Inject full screen background
    components.html(html_code, height=0, width=0) # Height 0 because we style it with CSS to be fixed background
    
    # CSS to make the iframe cover the screen behind everything
    st.markdown("""
    <style>
        iframe {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            border: none;
        }
    </style>
    """, unsafe_allow_html=True)

def load_ui_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        /* Make Streamlit background transparent so WebGL shows through */
        .stApp {{
            background: transparent !important;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }}
        
        /* Transparent Glass Cards for Retina Clarity */
        .glass-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: {FIBO['sm']}px;
            padding: {FIBO['md']}px;
            margin-bottom: {FIBO['sm']}px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }}
        
        .glass-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.08);
        }}
        
        /* Typography */
        .metric-value {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        .metric-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: rgba(255,255,255,0.7);
            font-weight: 600;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        
        /* Input Fields Transparency */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {{
            background: rgba(0,0,0,0.3) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px);
        }}
        
        /* Buttons */
        div.stButton > button {{
            background: linear-gradient(135deg, rgba(78, 205, 196, 0.8), rgba(68, 160, 141, 0.8)) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            backdrop-filter: blur(4px);
            padding: {FIBO['sm']}px {FIBO['md']}px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            transition: all 0.3s ease !important;
        }}
        
        div.stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 0 15px rgba(78, 205, 196, 0.4);
        }}
        
        #MainMenu, header, footer {{ visibility: hidden; }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.2); border-radius: 3px; }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 4. VERİTABANI YÖNETİMİ
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
            "Payment_ID", "Time", "Brand", "Amount", "Method", "Reference", 
            "Status", "Proof_File", "Notes", 
            "Fatura_Sent", "Fatura_Date", "Fatura_Explanation"
        ]).to_csv(CSV_PAYMENTS, index=False)
    else:
        df = pd.read_csv(CSV_PAYMENTS)
        if "Fatura_Sent" not in df.columns:
            df["Fatura_Sent"] = "No"
            df["Fatura_Date"] = ""
            df["Fatura_Explanation"] = ""
            df.to_csv(CSV_PAYMENTS, index=False)
        
    if not os.path.exists(CSV_INVOICES):
        pd.DataFrame(columns=[
            "Invoice_ID", "Time", "Brand", "Amount", "Date_Range", 
            "Invoice_Number", "Status", "Notes"
        ]).to_csv(CSV_INVOICES, index=False)
    
    if not os.path.exists(CSV_LOGS):
        pd.DataFrame(columns=[
            "Log_ID", "Time", "Action", "User", "Order_ID", "Details"
        ]).to_csv(CSV_LOGS, index=False)

def load_orders():
    try: return pd.read_csv(CSV_ORDERS)
    except: return pd.DataFrame()

def load_payments():
    try: return pd.read_csv(CSV_PAYMENTS)
    except: return pd.DataFrame()

def load_invoices():
    try: return pd.read_csv(CSV_INVOICES)
    except: return pd.DataFrame()

def save_order(order_data):
    try:
        df = load_orders()
        df = pd.concat([df, pd.DataFrame([order_data])], ignore_index=True)
        df.to_csv(CSV_ORDERS, index=False)
        return True
    except Exception as e:
        st.error(f"Kayıt hatası: {e}")
        return False

def update_orders(df):
    try:
        df.to_csv(CSV_ORDERS, index=False)
        return True
    except: return False

def save_payment(payment_data):
    try:
        df = load_payments()
        df = pd.concat([df, pd.DataFrame([payment_data])], ignore_index=True)
        df.to_csv(CSV_PAYMENTS, index=False)
        return True
    except: return False

def update_payments(df):
    try:
        df.to_csv(CSV_PAYMENTS, index=False)
        return True
    except: return False

def save_invoice(invoice_data):
    try:
        df = load_invoices()
        df = pd.concat([df, pd.DataFrame([invoice_data])], ignore_index=True)
        df.to_csv(CSV_INVOICES, index=False)
        return True
    except: return False

# ============================================================================
# 5. OTURUM YÖNETİMİ
# ============================================================================

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'brand_lock' not in st.session_state:
    st.session_state.brand_lock = None

# ============================================================================
# 6. GİRİŞ EKRANI
# ============================================================================

def login_screen():
    inject_liquid_background()
    load_ui_css()
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['xl']}px;">
            <div style="font-size: {FIBO['xl']}px; margin-bottom: {FIBO['sm']}px;">🏔️</div>
            <h2>NATUVISIO ADMIN</h2>
            <p style="opacity: 0.6; font-size: 12px;">LIQUID EDITION v6.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        password = st.text_input("Erişim Şifresi", type="password", key="login")
        
        if st.button("🔓 GİRİŞ YAP", use_container_width=True):
            if password == ADMIN_PASS:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Hatalı şifre")

# ============================================================================
# 7. ANA PANEL (DASHBOARD)
# ============================================================================

def dashboard():
    inject_liquid_background()
    load_ui_css()
    init_databases()
    
    col_h1, col_h2, col_h3 = st.columns([6, 1, 1])
    with col_h1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: {FIBO['sm']}px;">
            {get_icon('mountain', '#4ECDC4', FIBO['lg'])}
            <div>
                <h1 style="margin:0;">YÖNETİM MERKEZİ</h1>
                <span style="font-size: 11px; opacity: 0.6;">TAM YETKİLİ ERİŞİM</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h3:
        if st.button("🚪 Çıkış"):
            st.session_state.admin_logged_in = False
            st.session_state.cart = []
            st.rerun()
            
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    df = load_orders()
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    total_rev = df['Total_Value'].sum() if not df.empty else 0
    total_comm = df['Commission_Amt'].sum() if not df.empty else 0
    pending_count = len(df[df['Status'] == 'Pending'])
    
    with col_m1:
        st.markdown(f"""<div class="glass-card" style="text-align:center;"><div class="metric-label">TOPLAM CİRO</div><div class="metric-value">{total_rev:,.0f}₺</div></div>""", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""<div class="glass-card" style="text-align:center;"><div class="metric-label">NET KOMİSYON</div><div class="metric-value" style="color:#4ECDC4;">{total_comm:,.0f}₺</div></div>""", unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""<div class="glass-card" style="text-align:center;"><div class="metric-label">BEKLEYEN İŞLEM</div><div class="metric-value" style="color:#F59E0B;">{pending_count}</div></div>""", unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""<div class="glass-card" style="text-align:center;"><div class="metric-label">TOPLAM SİPARİŞ</div><div class="metric-value">{len(df)}</div></div>""", unsafe_allow_html=True)

    tabs = st.tabs([
        "🚀 YENİ SEVKİYAT", 
        "✅ OPERASYON", 
        "🏦 FATURA & ÖDEME PANELİ", 
        "📦 TÜM SİPARİŞLER",
        "📊 ANALİTİK",
        "❔ SSS & AKIŞ REHBERİ"
    ])
    
    with tabs[0]: render_new_dispatch()
    with tabs[1]: render_operations()
    with tabs[2]: render_brand_payout_hq()
    with tabs[3]: render_all_orders()
    with tabs[4]: render_analytics()
    with tabs[5]: render_faqs()

# ============================================================================
# 8. YENİ SEVKİYAT MODÜLÜ
# ============================================================================

def render_new_dispatch():
    col_L, col_R = st.columns([PHI, 1])
    
    with col_L:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Müşteri Bilgileri")
        col_n, col_p = st.columns(2)
        with col_n: cust_name = st.text_input("Ad Soyad", key="cust_name")
        with col_p: cust_phone = st.text_input("Telefon", key="cust_phone")
        cust_addr = st.text_area("Adres", key="cust_addr", height=80)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🛒 Ürün Seçimi")
        
        if st.session_state.cart:
            st.info(f"🔒 Kilitli Marka: {st.session_state.brand_lock}")
            active_brand = st.session_state.brand_lock
        else:
            active_brand = st.selectbox("Marka Seçiniz", list(BRANDS.keys()), key="brand_sel")
            
        brand_data = BRANDS[active_brand]
        products = list(brand_data["products"].keys())
        
        col_p, col_q = st.columns([3, 1])
        with col_p: prod = st.selectbox("Ürün", products, key="prod_sel")
        with col_q: qty = st.number_input("Adet", 1, value=1, key="qty")
        
        prod_details = brand_data["products"][prod]
        
        # Calculations
        unit_price = prod_details['price']
        line_total = unit_price * qty
        comm_amt = line_total * brand_data['commission']
        payout = line_total - comm_amt
        
        if st.button("➕ Sepete Ekle"):
            st.session_state.cart.append({
                "brand": active_brand,
                "product": prod,
                "sku": prod_details['sku'],
                "qty": qty,
                "unit_price": unit_price,
                "subtotal": line_total,
                "comm_amt": comm_amt,
                "payout": payout
            })
            st.session_state.brand_lock = active_brand
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_R:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📦 Sepet Özeti")
        
        if st.session_state.cart:
            for item in st.session_state.cart:
                # v5.3 FIX: Removed indentation from HTML string to prevent Code Block rendering
                item_html = f"""
<div style="background: rgba(255,255,255,0.03); border-radius: 8px; padding: 12px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.05);">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
<span style="font-weight:700; font-size:14px;">{item['product']}</span>
<span style="background:rgba(78,205,196,0.2); color:#4ECDC4; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:bold;">x{item['qty']}</span>
</div>
<div style="font-size:12px; opacity:0.7; margin-bottom:8px; border-bottom:1px dashed rgba(128,128,128,0.3); padding-bottom:8px;">
{item['unit_price']:,.0f}₺ <span style="opacity:0.5;">(birim)</span> &times; {item['qty']} = <strong style="color:#fff;">{item['subtotal']:,.0f}₺</strong>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; font-size:11px;">
<div style="background:rgba(252, 211, 77, 0.1); padding:4px; border-radius:4px; text-align:center;">
<div style="color:#FCD34D; opacity:0.8;">Komisyon</div>
<div style="color:#FCD34D; font-weight:bold;">{item['comm_amt']:,.0f}₺</div>
</div>
<div style="background:rgba(78, 205, 196, 0.1); padding:4px; border-radius:4px; text-align:center;">
<div style="color:#4ECDC4; opacity:0.8;">Marka Ödemesi</div>
<div style="color:#4ECDC4; font-weight:bold;">{item['payout']:,.0f}₺</div>
</div>
</div>
</div>
"""
                st.markdown(item_html, unsafe_allow_html=True)
            
            total = sum(i['subtotal'] for i in st.session_state.cart)
            total_comm = sum(i['comm_amt'] for i in st.session_state.cart)
            total_pay = sum(i['payout'] for i in st.session_state.cart)
            
            summary_html = f"""
<div style="background: rgba(78,205,196,0.1); padding: 15px; border-radius: 8px; margin: 15px 0;">
<div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:4px;">
<span>Ürün Toplam:</span>
<span style="font-weight:bold;">{total:,.0f}₺</span>
</div>
<div style="display:flex; justify-content:space-between; font-size:14px; color:#FCD34D; margin-bottom:8px;">
<span>Top. Komisyon:</span>
<span style="font-weight:bold;">{total_comm:,.0f}₺</span>
</div>
<div style="margin: 5px 0; border-top: 1px dashed rgba(255,255,255,0.2);"></div>
<div style="display:flex; justify-content:space-between; font-weight:bold; font-size:18px; color:#4ECDC4; margin-top:8px;">
<span>MARKAYA NET:</span>
<span>{total_pay:,.0f}₺</span>
</div>
</div>
"""
            st.markdown(summary_html, unsafe_allow_html=True)
            
            if st.button("⚡ SİPARİŞİ OLUŞTUR", type="primary"):
                if cust_name and cust_phone:
                    order_id = f"NV-{datetime.now().strftime('%m%d%H%M')}"
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
                        'Brand_Payout': total_pay,
                        'Status': 'Pending',
                        'WhatsApp_Sent': 'NO',
                        'Tracking_Num': '',
                        'Priority': 'Standard',
                        'Notes': '',
                        'Created_By': 'admin',
                        'Last_Modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    if save_order(order_data):
                        st.success(f"✅ Sipariş {order_id} oluşturuldu!")
                        st.session_state.cart = []
                        st.session_state.brand_lock = None
                        st.rerun()
                else:
                    st.error("Müşteri bilgilerini giriniz!")
            
            if st.button("🗑️ Sepeti Temizle"):
                st.session_state.cart = []
                st.session_state.brand_lock = None
                st.rerun()
        else:
            st.info("Sepet boş")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# 9. OPERASYON MODÜLÜ
# ============================================================================

def render_operations():
    st.markdown("### ✅ Operasyon Yönetimi")
    df = load_orders()
    
    new_orders = df[df['WhatsApp_Sent'] == 'NO']
    if not new_orders.empty:
        st.warning(f"⚠️ {len(new_orders)} sipariş markaya bildirilmedi!")
        for idx, row in new_orders.iterrows():
            with st.expander(f"🔴 {row['Order_ID']} - {row['Brand']} ({row['Customer']})", expanded=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    phone = BRANDS[row['Brand']]['phone']
                    msg = urllib.parse.quote(f"YENİ SİPARİŞ: {row['Order_ID']}\n{row['Items']}\nTeslimat: {row['Address']}")
                    st.markdown(f"[📲 WhatsApp Mesajı Gönder](https://wa.me/{phone}?text={msg})")
                with col2:
                    if st.button("✅ Bildirildi", key=f"ntf_{idx}"):
                        df.at[idx, 'WhatsApp_Sent'] = 'YES'
                        df.at[idx, 'Status'] = 'Notified'
                        update_orders(df)
                        st.rerun()
    
    pending_track = df[(df['Status'] == 'Notified') & (df['Tracking_Num'].isna() | (df['Tracking_Num'] == ''))]
    if not pending_track.empty:
        st.info("📦 Takip numarası bekleyen siparişler")
        for idx, row in pending_track.iterrows():
            with st.expander(f"⏳ {row['Order_ID']} - {row['Brand']}"):
                track = st.text_input("Takip No Giriniz", key=f"track_{idx}")
                if st.button("Kargola", key=f"ship_{idx}"):
                    df.at[idx, 'Tracking_Num'] = track
                    df.at[idx, 'Status'] = 'Dispatched'
                    update_orders(df)
                    st.success("Kargolandı!")
                    st.rerun()

    dispatched = df[df['Status'] == 'Dispatched']
    if not dispatched.empty:
        st.markdown("---")
        st.markdown("#### ✅ Tamamlanmayı Bekleyenler")
        for idx, row in dispatched.iterrows():
            col1, col2, col3 = st.columns([2, 2, 1])
            col1.write(f"**{row['Order_ID']}**")
            col2.write(f"Takip: {row['Tracking_Num']}")
            if col3.button("Tamamla", key=f"comp_{idx}"):
                df.at[idx, 'Status'] = 'Completed'
                update_orders(df)
                st.rerun()

# ============================================================================
# 10. FATURA & ÖDEME PANELİ (BRAND PAYOUT HQ)
# ============================================================================

def render_brand_payout_hq():
    st.markdown("## 📑 FATURA & ÖDEME PANELİ (BRAND PAYOUT HQ)")
    
    df_orders = load_orders()
    df_payments = load_payments()
    
    for brand in BRANDS.keys():
        with st.expander(f"🏦 {brand} FİNANS YÖNETİMİ", expanded=True):
            brand_meta = BRANDS[brand]
            brand_orders = df_orders[df_orders['Brand'] == brand]
            
            completed_df = brand_orders[brand_orders['Status'] == 'Completed']
            payout_completed = completed_df['Brand_Payout'].sum() if not completed_df.empty else 0
            count_completed = len(completed_df)
            
            pending_df = brand_orders[brand_orders['Status'].isin(['Pending', 'Notified', 'Dispatched'])]
            payout_pending = pending_df['Brand_Payout'].sum() if not pending_df.empty else 0
            
            brand_paid_df = df_payments[df_payments['Brand'] == brand]
            total_paid = brand_paid_df['Amount'].sum() if not brand_paid_df.empty else 0
            
            net_transfer_due = payout_completed - total_paid
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #4ECDC4;">
                    <div style="font-size:12px; opacity:0.7;">KESİLMESİ GEREKEN FATURA TUTARI</div>
                    <div style="font-size:24px; font-weight:bold;">{payout_completed:,.2f}₺</div>
                    <div style="font-size:11px; opacity:0.6;">(Tamamlanan {count_completed} Sipariş)</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #F59E0B;">
                    <div style="font-size:12px; opacity:0.7;">HENÜZ TAMAMLANMAMIŞ SİPARİŞLER</div>
                    <div style="font-size:24px; font-weight:bold;">{payout_pending:,.2f}₺</div>
                    <div style="font-size:11px; opacity:0.6;">(Bekleyen/Kargoda)</div>
                </div>
                """, unsafe_allow_html=True)
            
            comm_rate = int(brand_meta['commission'] * 100)
            fatura_desc = f"NATUVISIO satış komisyon hizmeti – {brand} – Toplam sipariş adedi: {count_completed} – Komisyon oranı: %{comm_rate} – Net marka ödemesi: {payout_completed:,.2f}₺"
            
            st.markdown("#### 🧾 Fatura Açıklaması (Otomatik)")
            st.code(fatura_desc, language="text")
            
            st.markdown("#### 💸 Banka Transfer Talimatı")
            col_bank1, col_bank2 = st.columns([2, 1])
            with col_bank1:
                st.info(f"**Alıcı:** {brand_meta['account_name']}  \n**IBAN:** {brand_meta['iban']}  \n**Tutar:** {net_transfer_due:,.2f}₺")
            with col_bank2:
                transfer_desc = f"NATUVISIO {brand} satış ödemesi – {datetime.now().strftime('%d.%m.%Y')} – Toplam: {net_transfer_due:,.0f}TL"
                st.code(transfer_desc, language="text")
            
            if net_transfer_due > 0:
                if st.button(f"💸 {brand} - ÖDEMEYİ YAPTIM ({net_transfer_due:,.0f}₺)", key=f"pay_{brand}"):
                    payment_data = {
                        "Payment_ID": f"PAY-{datetime.now().strftime('%m%d%H%M%S')}",
                        "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "Brand": brand,
                        "Amount": net_transfer_due,
                        "Method": "Bank Transfer",
                        "Reference": "Admin Manual",
                        "Status": "Confirmed",
                        "Proof_File": "",
                        "Notes": "Payout HQ üzerinden ödendi",
                        "Fatura_Sent": "No",
                        "Fatura_Date": "",
                        "Fatura_Explanation": ""
                    }
                    if save_payment(payment_data):
                        st.balloons()
                        st.success("Ödeme sisteme işlendi!")
                        time.sleep(1)
                        st.rerun()
            else:
                st.success("✅ Tüm ödemeler yapıldı.")

    st.markdown("### 📋 Fatura Durum Tablosu (Cross-Check)")
    df_payments = load_payments()
    if not df_payments.empty:
        st.dataframe(df_payments[['Time', 'Brand', 'Amount', 'Fatura_Sent', 'Fatura_Date']], use_container_width=True)
        with st.form("update_fatura_status"):
            st.write("Fatura Durumu Güncelle")
            pay_ids = df_payments['Payment_ID'].tolist()
            selected_pay = st.selectbox("İşlem Seçiniz (Payment ID)", pay_ids)
            col_f1, col_f2 = st.columns(2)
            with col_f1: new_status = st.checkbox("Fatura Kesildi mi? (YES)", value=False)
            with col_f2: new_date = st.date_input("Fatura Tarihi")
            if st.form_submit_button("Durumu Güncelle"):
                idx = df_payments.index[df_payments['Payment_ID'] == selected_pay][0]
                df_payments.at[idx, 'Fatura_Sent'] = "YES" if new_status else "NO"
                df_payments.at[idx, 'Fatura_Date'] = str(new_date)
                update_payments(df_payments)
                st.success("Güncellendi!")
                st.rerun()
    else:
        st.info("Henüz ödeme kaydı yok.")

# ============================================================================
# 11. DİĞER FONKSİYONLAR
# ============================================================================

def render_all_orders():
    st.markdown("### 📦 Tüm Sipariş Geçmişi")
    df = load_orders()
    if not df.empty:
        st.dataframe(df.sort_values('Time', ascending=False), use_container_width=True)
    else:
        st.info("Kayıt yok")

def render_analytics():
    st.markdown("### 📊 Analitik Raporlar")
    df = load_orders()
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Marka Bazlı Satış**")
            st.bar_chart(df.groupby('Brand')['Total_Value'].sum())
        with col2:
            st.markdown("**Durum Dağılımı**")
            st.bar_chart(df['Status'].value_counts())

# ============================================================================
# 12. SSS & AKIŞ REHBERİ (YENİ - v5.4)
# ============================================================================

def render_faqs():
    st.markdown("## ❔ SSS & Operasyon Akış Rehberi")

    with st.expander("1. Genel bakış: Bu panel ne yapıyor?", expanded=True):
        st.markdown("""
        Bu panel, NATUVISIO'nun tüm marka partnerleri için (Haki Heal, Auroraco, Longevicals vb.) **tek merkezden sevkiyat, finans ve mutabakat** yönetimini sağlar.
        
        **Temel Özellikler:**
        * **Sipariş Girişi:** Müşteri ve ürün bilgilerini alıp otomatik komisyon hesabı yapar.
        * **İletişim:** Tek tıkla markaya özel WhatsApp sipariş mesajı oluşturur.
        * **Takip:** Kargo numaralarını işler ve sipariş durumunu (Pending → Completed) günceller.
        * **Finansal Zeka:** Tamamlanan siparişleri baz alarak hangi markaya ne kadar ödeme yapılması gerektiğini (Borç) ve markaya ne kadar fatura kesileceğini (Alacak) otomatik hesaplar.
        """)

    with st.expander("2. Sipariş akışı: İlk adımdan marka ödemesine kadar", expanded=False):
        st.markdown("""
        1.  **🚀 YENİ SEVKİYAT** sekmesine girin.
        2.  Müşteri bilgilerini (Ad Soyad, Telefon, Adres) girin.
        3.  Markayı ve ürünü seçip adeti girin → "➕ Sepete Ekle" deyin.
        4.  Sepet özetini kontrol edip **"⚡ SİPARİŞİ OLUŞTUR"** butonuna basın. (Sipariş Durumu: **Pending**)
        5.  **✅ OPERASYON** sekmesine geçin. İlgili siparişi bulun ve **"📲 WhatsApp Mesajı Gönder"** linkine tıklayarak markaya iletin.
        6.  Mesajı attıktan sonra **"✅ Bildirildi"** butonuna basın. (Durum: **Notified**, WhatsApp: **YES**)
        7.  Markadan kargo takip numarası geldiğinde, yine Operasyon sekmesinde "Takip No Giriniz" alanına yazıp **"Kargola"** deyin. (Durum: **Dispatched**)
        8.  Ürün müşteriye ulaştığında **"Tamamla"** butonuna basın. (Durum: **Completed**)
        9.  **🏦 FATURA & ÖDEME PANELİ** sekmesine gidin. Tamamlanan siparişlerin toplam tutarını görün.
        10. **"ÖDEMEYİ YAPTIM"** butonuna basarak ödemeyi sisteme işleyin.
        """)

    with st.expander("3. Komisyon ve marka ödemesi nasıl hesaplanıyor?", expanded=False):
        st.markdown("""
        Her markanın komisyon oranı sistemde (BRANDS sözlüğü içinde) sabittir:
        * **Haki Heal:** %15
        * **Auroraco:** %20
        * **Longevicals:** %12
        
        **Hesaplama Mantığı:**
        * `Birim Fiyat` (Unit Price) x `Adet` (Qty) = `Satır Toplamı` (Line Total)
        * `Satır Toplamı` x `Komisyon Oranı` = `Komisyon Tutarı` (Commission Amt)
        * `Satır Toplamı` - `Komisyon Tutarı` = `Marka Ödemesi` (Brand Payout)
        
        Bu değerler sipariş oluşturulduğu an `orders_complete.csv` dosyasına sabitlenerek kaydedilir. İleride komisyon oranları değişse bile eski siparişlerin finansal verisi bozulmaz.
        """)

    with st.expander("4. FATURA & ÖDEME PANELİ nasıl kullanılır?", expanded=False):
        st.markdown("""
        Bu panel her marka için iki kritik veriyi gösterir:
        
        **A) KESİLMESİ GEREKEN FATURA TUTARI (Sol Kutu - Mavi):**
        * Sadece durumu **"Completed"** (Tamamlandı) olan siparişlerin toplam tutarını baz alır.
        * Daha önce ödeme yapılmışsa bu tutardan düşülür.
        
        **B) HENÜZ TAMAMLANMAMIŞ SİPARİŞLER (Sağ Kutu - Turuncu):**
        * Kargoda veya hazırlık aşamasındaki siparişlerin tutarıdır. Bunlar henüz hakedişe dönüşmemiştir.
        
        **İşlem Adımları:**
        1.  Panel, o günkü tarih ile otomatik bir **"Banka Transfer Açıklaması"** üretir. Bunu banka uygulamanıza kopyalayın.
        2.  Ödemeyi bankadan yaptıktan sonra paneldeki **"💸 ÖDEMEYİ YAPTIM"** butonuna basın.
        3.  Bu işlem `brand_payments.csv` dosyasına "Confirmed" statüsünde yeni bir satır ekler ve bakiyeyi sıfırlar.
        4.  Daha sonra aynı sayfadaki **"Fatura Durum Tablosu"** bölümünden, ilgili ödeme için faturanın kesilip kesilmediğini işaretleyebilirsiniz.
        """)

    with st.expander("5. Sipariş durumları (Pending → Notified → Dispatched → Completed)", expanded=False):
        st.markdown("""
        * **🔴 Pending (Bekliyor):** Sipariş sisteme girildi ancak henüz markaya WhatsApp'tan iletilmedi.
        * **🔵 Notified (Bildirildi):** Markaya sipariş detayı atıldı. Markanın ürünü hazırlaması bekleniyor. (WhatsApp_Sent = YES)
        * **🟠 Dispatched (Kargolandı):** Marka kargo takip numarasını iletti ve sisteme girildi. Ürün yolda.
        * **🟢 Completed (Tamamlandı):** Ürün müşteriye ulaştı. Bu aşamaya gelen siparişin parası markaya ödenmeye hak kazanır (Hakedişe eklenir).
        """)

    with st.expander("6. Raporlama & kontrol: Hangi tablo neyi gösteriyor?", expanded=False):
        st.markdown("""
        * **📦 TÜM SİPARİŞLER:** `orders_complete.csv` dosyasındaki ham veriyi gösterir. Geçmişe dönük tüm kayıtlar buradadır.
        * **📊 ANALİTİK:** Marka bazlı ciro dağılımını ve sipariş durumlarını grafikleştirir.
        * **📋 Fatura Durum Tablosu:** (Fatura & Ödeme Paneli'nin en altında) Yapılan ödemelerin listesidir. Faturası kesilmiş mi, tarihi nedir buradan takip edilir.
        """)

    with st.expander("7. Önerilen günlük çalışma rutini", expanded=False):
        st.markdown("""
        1.  **Sabah:** `YENİ SEVKİYAT` ekranından gece gelen siparişleri girin.
        2.  **Öğle:** `OPERASYON` sekmesine geçin. Yeni siparişleri "Bildirildi" yapın. Dünden gelen takip numaralarını girip "Kargola" deyin.
        3.  **Akşam:** `FATURA & ÖDEME PANELİ`ne bakın. Tamamlanan siparişler için markalara ödeme çıkıp çıkmayacağını kontrol edin.
        4.  **Haftalık:** `ANALİTİK` sekmesinden hangi markanın daha çok sattığını inceleyin.
        """)

# ============================================================================
# 13. ANA ÇALIŞTIRMA (MAIN)
# ============================================================================

if __name__ == "__main__":
    if not st.session_state.admin_logged_in:
        login_screen()
    else:
        dashboard()
