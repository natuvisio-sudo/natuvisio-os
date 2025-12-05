# app.py
"""
NATUVISIO Health Hub – Frontend Prototype
Built with Streamlit (Python) + embedded HTML/CSS (frontend layer)

Run with:
    streamlit run app.py
"""

import streamlit as st
from datetime import datetime
import pytz

# ------------------------------------------------------------------
# 1) PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="NATUVISIO Health Hub",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------
# 2) GLOBAL CSS – NEW ZAPIENS STYLE, BUT NATUVISIO BRANDING
# ------------------------------------------------------------------
def inject_global_css():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --nv-bg: #f5f1e8;
  --nv-bg-soft: #faf6f0;
  --nv-bg-card: #ffffff;
  --nv-text: #111827;
  --nv-muted: #6b7280;
  --nv-border-subtle: rgba(15, 23, 42, 0.06);
  --nv-accent: #ff7a3c;         /* warm orange (like NewZapiens) */
  --nv-accent-soft: rgba(255, 122, 60, 0.08);
  --nv-brand: #5b7354;          /* NATUVISIO sage */
  --nv-brand-soft: rgba(91, 115, 84, 0.08);
  --nv-radius-card: 22px;
  --nv-shadow-soft: 0 18px 45px rgba(15, 23, 42, 0.06);
}

/* Reset Streamlit default background */
.stApp {
  background-color: var(--nv-bg) !important;
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Hide default menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background: transparent;}

/* Layout max width */
.block-container {
  padding-top: 0.5rem !important;
  padding-bottom: 4rem !important;
  max-width: 1200px;
}

/* Top nav */
.nv-nav {
  position: sticky;
  top: 0;
  z-index: 99;
  backdrop-filter: blur(12px);
  background: linear-gradient(to bottom,
    rgba(245,241,232,0.95),
    rgba(245,241,232,0.88),
    rgba(245,241,232,0.00)
  );
  padding: 14px 0 8px;
}

.nv-nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.nv-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 15px;
}

.nv-logo-mark {
  width: 26px;
  height: 26px;
  border-radius: 99px;
  background: radial-gradient(circle at 30% 20%, #ffe1cb, #ff7a3c);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #111827;
  font-size: 16px;
}

.nv-nav-links {
  display: flex;
  align-items: center;
  gap: 18px;
  font-size: 13px;
}

.nv-nav-link {
  color: var(--nv-muted);
  text-decoration: none;
  cursor: pointer;
  transition: color 0.2s ease, transform 0.1s ease;
}

.nv-nav-link:hover {
  color: var(--nv-text);
  transform: translateY(-1px);
}

.nv-nav-cta {
  padding: 7px 14px;
  border-radius: 999px;
  border: 1px solid rgba(17, 24, 39, 0.1);
  font-size: 13px;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  background: #111827;
  color: #f9fafb !important;
}

.nv-nav-cta span {
  font-size: 11px;
  opacity: 0.8;
}

/* Hero section */
.nv-hero {
  padding: 40px 0 32px;
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
  gap: 40px;
  align-items: center;
}

@media (max-width: 900px) {
  .nv-hero {
    grid-template-columns: minmax(0, 1fr);
    padding-top: 24px;
  }
}

.nv-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--nv-accent-soft);
  color: #7c2d12;
  font-size: 11px;
  font-weight: 500;
  margin-bottom: 12px;
}

.nv-pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--nv-accent);
}

.nv-hero-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 600;
  font-size: clamp(32px, 4vw, 42px);
  letter-spacing: -0.04em;
  line-height: 1.1;
  color: var(--nv-text);
  margin-bottom: 12px;
}

.nv-hero-title span {
  font-weight: 700;
}

.nv-hero-sub {
  font-size: 15px;
  color: var(--nv-muted);
  max-width: 460px;
  margin-bottom: 18px;
}

.nv-hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
}

.nv-btn-primary {
  padding: 10px 18px;
  border-radius: 999px;
  border: none;
  background: radial-gradient(circle at 0 0, #ffe3d1, #ff7a3c);
  color: #111827;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 14px 30px rgba(148, 64, 20, 0.16);
}

.nv-btn-secondary {
  padding: 10px 16px;
  border-radius: 999px;
  border: 1px solid rgba(17, 24, 39, 0.1);
  background: #fdfbf7;
  color: #111827;
  font-size: 13px;
  cursor: pointer;
}

.nv-hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 11px;
  color: var(--nv-muted);
}

/* Right hero card */
.nv-hero-card {
  background: var(--nv-bg-soft);
  border-radius: 30px;
  padding: 22px 22px 18px;
  box-shadow: var(--nv-shadow-soft);
  border: 1px solid var(--nv-border-subtle);
}

.nv-hero-card-title {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 4px;
}

.nv-hero-card-sub {
  font-size: 12px;
  color: var(--nv-muted);
  margin-bottom: 14px;
}

.nv-metric-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0,1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.nv-metric {
  padding: 10px 10px 9px;
  border-radius: 14px;
  background: #ffffff;
  border: 1px solid rgba(15,23,42,0.04);
}

.nv-metric-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--nv-muted);
  margin-bottom: 3px;
}

.nv-metric-value {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 600;
  font-size: 17px;
}

.nv-metric-detail {
  font-size: 10px;
  color: var(--nv-muted);
}

/* Section wrappers */
.nv-section {
  margin-top: 40px;
  margin-bottom: 10px;
}

.nv-section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 16px;
}

.nv-section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px;
  letter-spacing: -0.03em;
}

.nv-section-kicker {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--nv-muted);
}

/* Cards */
.nv-card-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

@media (max-width: 1000px) {
  .nv-card-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media (max-width: 700px) {
  .nv-card-grid {
    grid-template-columns: minmax(0, 1fr);
  }
}

.nv-card {
  background: var(--nv-bg-card);
  border-radius: var(--nv-radius-card);
  padding: 16px 16px 14px;
  border: 1px solid var(--nv-border-subtle);
  box-shadow: 0 10px 28px rgba(15,23,42,0.03);
}

.nv-card-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 999px;
  background: var(--nv-brand-soft);
  color: var(--nv-brand);
  margin-bottom: 8px;
}

.nv-card-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
}

.nv-card-body {
  font-size: 13px;
  color: var(--nv-muted);
  margin-bottom: 12px;
}

.nv-card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: var(--nv-muted);
}

/* Reviews (simple) */
.nv-review {
  border-radius: 18px;
  padding: 14px 14px 12px;
  background: #111827;
  color: #f9fafb;
  border: 1px solid rgba(248, 250, 252, 0.08);
}

.nv-review-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.nv-avatar {
  width: 26px;
  height: 26px;
  border-radius: 999px;
  background: linear-gradient(135deg, #ff7a3c, #f97316);
}

.nv-review-name {
  font-size: 13px;
  font-weight: 500;
}

.nv-review-detail {
  font-size: 11px;
  opacity: 0.8;
}

/* Footer */
.nv-footer {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid rgba(17, 24, 39, 0.08);
  font-size: 11px;
  color: var(--nv-muted);
}

.nv-footer-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: space-between;
  align-items: baseline;
}

/* Small helper badge */
.nv-badge-soft {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 7px;
  font-size: 10px;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.03);
  color: var(--nv-muted);
}

/* Anchor offsets for smooth scroll targeting */
.anchor {
  scroll-margin-top: 80px;
}
</style>
""",
        unsafe_allow_html=True,
    )


inject_global_css()

# ------------------------------------------------------------------
# 3) TOP NAV
# ------------------------------------------------------------------
with st.container():
    st.markdown(
        """
<div class="nv-nav">
  <div class="nv-nav-inner">
    <div class="nv-logo">
      <div class="nv-logo-mark">N</div>
      <div>NATUVISIO <span style="opacity:0.6;">HEALTH HUB</span></div>
    </div>
    <div class="nv-nav-links">
      <a class="nv-nav-link" href="#hero">Overview</a>
      <a class="nv-nav-link" href="#stacks">Health stacks</a>
      <a class="nv-nav-link" href="#reviews">Reviews</a>
      <a class="nv-nav-link" href="#magazine">Articles</a>
      <a class="nv-nav-link" href="#footer">About</a>
      <a class="nv-nav-cta" href="mailto:hello@natuvisio.com">
        Partner with us
        <span>Brand / Klinik / Diyetisyen</span>
      </a>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# 4) HERO SECTION
# ------------------------------------------------------------------
with st.container():
    st.markdown('<div id="hero" class="anchor"></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown(
            """
<div class="nv-hero">
  <div>
    <div class="nv-pill">
      <div class="nv-pill-dot"></div>
      Helping people make trusted health decisions, faster
    </div>
    <div class="nv-hero-title">
      Healthspan maximization<br/>
      <span>for busy beginners in Turkey</span>
    </div>
    <p class="nv-hero-sub">
      NATUVISIO Health Hub is a curated space where real people, real science
      and transparent brands meet. No abartılı vaadler, no noise — just
      the signal you need to choose wisely.
    </p>

    <div class="nv-hero-actions">
      <button class="nv-btn-primary" onclick="window.location.hash='#stacks';">
        Build my first health stack
      </button>
      <button class="nv-btn-secondary" onclick="window.location.hash='#magazine';">
        Read the science-first guide
      </button>
    </div>

    <div class="nv-hero-meta">
      <div>✔ 100% bağımsız incelemeler</div>
      <div>✔ Mikrobiyom & temel sağlık odaklı</div>
      <div>✔ Türkiye & Avrupa markaları</div>
    </div>
  </div>
""",
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            """
  <div class="nv-hero-card">
    <div class="nv-hero-card-title">Quick health snapshot</div>
    <div class="nv-hero-card-sub">
      Answer 3 questions, see which foundations you might be missing.
    </div>

    <div class="nv-metric-row">
      <div class="nv-metric">
        <div class="nv-metric-label">Gut & digestion</div>
        <div class="nv-metric-value">72/100</div>
        <div class="nv-metric-detail">Şişkinlik, enerji dalgalanması</div>
      </div>
      <div class="nv-metric">
        <div class="nv-metric-label">Stress & sleep</div>
        <div class="nv-metric-value">64/100</div>
        <div class="nv-metric-detail">Geç yatma, sabah yorgunluğu</div>
      </div>
      <div class="nv-metric">
        <div class="nv-metric-label">Movement</div>
        <div class="nv-metric-value">3x</div>
        <div class="nv-metric-detail">Haftalık hafif aktivite</div>
      </div>
    </div>

    <div style="font-size:12px; color:#4b5563;">
      This is a demo layout. In the full product, this card can be powered by
      a short questionnaire and your health stack engine.
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------
# 5) HOW IT WORKS SECTION
# ------------------------------------------------------------------
with st.container():
    st.markdown(
        """
<div class="nv-section">
  <div class="nv-section-header">
    <div>
      <div class="nv-section-kicker">HOW IT WORKS</div>
      <div class="nv-section-title">From information overload to calm decisions</div>
    </div>
    <div style="font-size:12px; color:var(--nv-muted); max-width:320px;">
      We don’t sell magic bullets. We help you see your foundations clearly:
      gut, sleep, stress, movement, bloodwork – then match you only with
      products and protocols that make sense.
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    step_cols = st.columns(3)
    steps = [
        (
            "1. Map your reality",
            "Answer a few evidence-backed questions about digestion, energy, sleep, stress and lifestyle. No diagnoses, just patterns.",
        ),
        (
            "2. See your foundations",
            "We highlight which systems are under-supported (örneğin mikrobiyom, mineral dengesi, nabız, nefes).",
        ),
        (
            "3. Curated stacks",
            "You see transparent supplement & ritual suggestions: what, why, how long – and which Turkish brands actually deliver.",
        ),
    ]
    for col, (title, desc) in zip(step_cols, steps):
        with col:
            st.markdown(
                f"""
<div class="nv-card" style="border-radius:18px;">
  <div class="nv-card-tag">
    <span style="width:7px; height:7px; border-radius:999px; background:#111827;"></span>
    Step
  </div>
  <div class="nv-card-title">{title}</div>
  <div class="nv-card-body">{desc}</div>
</div>
""",
                unsafe_allow_html=True,
            )

# ------------------------------------------------------------------
# 6) HEALTH STACKS SECTION
# ------------------------------------------------------------------
with st.container():
    st.markdown('<div id="stacks" class="anchor"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="nv-section">
  <div class="nv-section-header">
    <div>
      <div class="nv-section-kicker">HEALTH STACKS</div>
      <div class="nv-section-title">Evidence-aware stacks for real lives</div>
    </div>
    <div class="nv-badge-soft">Demo: sample stacks – connect to your real DB later</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    stacks = [
        {
            "tag": "Foundations",
            "title": "Gut & microbiome reset",
            "body": "For people with şişkinlik, kabızlık / ishal döngüsü, yorgunluk. Focus on fiber, polyphenols, humic/fulvic and gentle probiotics.",
            "score": "Science weight: high",
            "time": "3–6 months",
        },
        {
            "tag": "Performance",
            "title": "Workday focus & calm",
            "body": "For founders, uzmanlar, yoğun çalışanlar. L-theanine, magnesium glycinate, non-stim nitric oxide, breathwork anchors.",
            "score": "Science weight: medium-high",
            "time": "8–12 weeks",
        },
        {
            "tag": "Recovery",
            "title": "Sleep architecture support",
            "body": "For those who fall asleep late, wake up unrefreshed. Light hygiene, timing of meals, magnesium, glycine, circadian timing.",
            "score": "Science weight: medium",
            "time": "4–8 weeks",
        },
    ]

    st.markdown('<div class="nv-card-grid">', unsafe_allow_html=True)
    for stack in stacks:
        st.markdown(
            f"""
<div class="nv-card">
  <div class="nv-card-tag">{stack['tag']}</div>
  <div class="nv-card-title">{stack['title']}</div>
  <div class="nv-card-body">{stack['body']}</div>
  <div class="nv-card-meta">
    <span>{stack['score']}</span>
    <span>{stack['time']}</span>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# 7) REVIEWS SECTION
# ------------------------------------------------------------------
with st.container():
    st.markdown('<div id="reviews" class="anchor"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="nv-section">
  <div class="nv-section-header">
    <div>
      <div class="nv-section-kicker">LATEST REVIEWS</div>
      <div class="nv-section-title">Real experiences, no sponsored copy</div>
    </div>
    <div style="font-size:12px; color:var(--nv-muted); max-width:320px;">
      In the full product this block would pull from your review DB (app, web,
      Telegram, Instagram) and standardize formats.
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    review_cols = st.columns(3)
    reviews = [
        (
            "Elif, 34",
            "İstanbul · Kurumsal yönetici",
            "3 aydır mikrobiyom odaklı destek alıyorum. En büyük fark, sabah şişkinliğinin kaybolması ve odaklanma kapasitemdeki artış.",
        ),
        (
            "Mert, 29",
            "Ankara · Yazılım geliştirici",
            "Kafeinsiz performans desteği için önerilen stack’i denedim. Özellikle akşam anksiyetesinin azalması benim için kritik oldu.",
        ),
        (
            "Dr. Ayşe",
            "Aile hekimi",
            "Danışanlarım için şeffaf etiketli ve gerçek analiz sonuçları olan takviyeleri bulmak başlı başına bir iş. Buradaki filtreleme çok değerli.",
        ),
    ]
    for col, (name, detail, text) in zip(review_cols, reviews):
        with col:
            st.markdown(
                f"""
<div class="nv-review">
  <div class="nv-review-header">
    <div class="nv-avatar"></div>
    <div>
      <div class="nv-review-name">{name}</div>
      <div class="nv-review-detail">{detail}</div>
    </div>
  </div>
  <div style="font-size:12px; line-height:1.5; margin-top:2px;">
    {text}
  </div>
</div>
""",
                unsafe_allow_html=True,
            )

# ------------------------------------------------------------------
# 8) MAGAZINE SECTION
# ------------------------------------------------------------------
with st.container():
    st.markdown('<div id="magazine" class="anchor"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="nv-section">
  <div class="nv-section-header">
    <div>
      <div class="nv-section-kicker">MAGAZINE</div>
      <div class="nv-section-title">Slow, science-aware health education</div>
    </div>
    <div class="nv-badge-soft">Soon: connect this to your NATUVISIO content hub</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    article_cols = st.columns(3)
    articles = [
        (
            "Modern yaşamda bağırsak sessizliği",
            "Neden her 5 kişiden 1’i sindirim sorunu yaşıyor ve bu, karar verme hızımızı nasıl etkiliyor?",
            "9 min read",
        ),
        (
            "Nitric oxide & oxygen: stimülan olmadan performans",
            "Kafein bağımlısı olmadan, damar sağlığını ve dayanıklılığı artırmanın bilimsel yolları.",
            "7 min read",
        ),
        (
            "Şüpheci tüketici için takviye okuryazarlığı",
            "Etiket, içerik, analiz raporu, fiyat – hangisi gerçekten önemli, hangisi pazarlama oyunu?",
            "11 min read",
        ),
    ]
    for col, (title, desc, meta) in zip(article_cols, articles):
        with col:
            st.markdown(
                f"""
<div class="nv-card" style="border-radius:18px;">
  <div class="nv-card-title">{title}</div>
  <div class="nv-card-body">{desc}</div>
  <div class="nv-card-meta">
    <span>{meta}</span>
    <span style="text-decoration:underline; text-underline-offset:3px;">Read draft</span>
  </div>
</div>
""",
                unsafe_allow_html=True,
            )

# ------------------------------------------------------------------
# 9) FOOTER – LEGAL + CONTACT + TIMEZONE
# ------------------------------------------------------------------
istanbul_time = (
    datetime.now(pytz.timezone("Europe/Istanbul")).strftime("%d.%m.%Y · %H:%M")
)

with st.container():
    st.markdown('<div id="footer" class="anchor"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="nv-footer">
  <div class="nv-footer-row">
    <div style="max-width:420px;">
      <strong>NATUVISIO Health Hub</strong><br/>
      Helping people in Turkey make trusted, evidence-aware health decisions,
      starting from the foundations: gut, sleep, stress, movement.
      <br/><br/>
      <span style="opacity:0.75;">
        Products and content are not intended to diagnose, treat, cure or prevent any disease.
        All information is educational and should be cross-checked with your own healthcare professional.
      </span>
    </div>

    <div style="font-size:11px;">
      <div><strong>Contact</strong></div>
      <div>hello@natuvisio.com</div>
      <div>natuvisio.com</div>
      <div style="margin-top:6px;">Local time (Istanbul): {istanbul_time}</div>
    </div>

    <div style="font-size:11px; text-align:right; opacity:0.8;">
      © {datetime.now().year} NATUVISIO.<br/>
      All rights reserved. Experimental prototype UI built with Streamlit.
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
