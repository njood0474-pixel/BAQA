
# BAQĀ — Hospital-Ready Streamlit App
import streamlit as st, pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime

st.set_page_config(page_title="BAQĀ – Decision Intelligence", page_icon="🎗️", layout="wide")

# Load CSS
css_path = Path("assets/style.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

LOGO = Path("assets/logo.png")
APP_NAME = "BAQĀ – Big-data Analytics for Quality of Life & Assurance"

# Session
if "entered" not in st.session_state: st.session_state.entered = False
if "auth" not in st.session_state: st.session_state.auth = {"role": None, "ok": False, "user": ""}
if "risk_prob" not in st.session_state: st.session_state.risk_prob = 0.45

def topbar():
    c1,c2 = st.columns([6,1])
    with c1:
        st.markdown('<div class="topbar">', unsafe_allow_html=True)
        x1,x2 = st.columns([0.08,0.92])
        with x1:
            if LOGO.exists(): st.image(str(LOGO), use_column_width=True)
            else: st.write("**BAQĀ**")
        with x2:
            role_txt = st.session_state.auth.get("role") or "Guest"
            st.markdown(f"<div class='brand'><div class='title'>BAQĀ – Decision Intelligence</div><span class='rolepill'>{role_txt}</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.session_state.auth.get("ok") and st.button("Logout"):
            st.session_state.auth = {"role": None, "ok": False, "user": ""}
            st.session_state.entered = False
            st.rerun()

def splash():
    st.markdown('<div class="splash">', unsafe_allow_html=True)
    dots = [(12,10),(85,20),(15,80),(80,75),(55,12),(35,18),(90,55),(10,55),(50,88),(28,72),(72,32),(38,86),(63,82),(70,15)]
    for i,(x,y) in enumerate(dots):
        g = " g" if i%3==0 else ""
        st.markdown(f'<div class="dot{g}" style="left:{x}%; top:{y}%; animation-delay:{0.2*i}s"></div>', unsafe_allow_html=True)
    for (cx,cy,h,rot) in [(50,22,120,-20),(52,24,140,35),(48,24,110,12),(35,30,160,-10),(65,30,145,18),(25,60,120,-38)]:
        st.markdown(f'<div class="line" style="left:{cx}%; top:{cy}%; height:{h}px; transform: rotate({rot}deg)"></div>', unsafe_allow_html=True)
    if LOGO.exists():
        st.markdown('<div class="logoGlow"></div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns([1,1,1]); 
        with c2: st.image(str(LOGO), width=150)
    else:
        c1,c2,c3 = st.columns([1,1,1]); 
        with c2: st.markdown("<h2 style='text-align:center;'>BAQĀ</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='introText'><div style='font-size:1.25rem; font-weight:600; letter-spacing:.2px; margin-bottom:6px;'>{APP_NAME}</div><div style='opacity:.85'>Connecting every specialty. Unifying every dataset. Predicting outcomes. Enhancing life.</div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    if st.button("Enter BAQĀ"): st.session_state.entered=True; st.rerun()

def login():
    st.markdown('<div class="hero"><h3>Welcome to BAQĀ</h3><p class="subtitle">Sign in to access the dashboards.</p></div>', unsafe_allow_html=True)
    col = st.columns([1.2,1,1.2])[1]
    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        role = st.selectbox("Role", ["Decision-Maker","Physician"])
        user = st.text_input("Username", placeholder="admin / doc")
        pwd  = st.text_input("Password", type="password", placeholder="••••••••")
        ok = st.button("Sign in")
        st.caption("Demo – Decision-Maker: admin/admin123 · Physician: doc/doc123")
        st.markdown('</div>', unsafe_allow_html=True)
    if ok:
        if (role=="Decision-Maker" and user=="admin" and pwd=="admin123") or (role=="Physician" and user=="doc" and pwd=="doc123"):
            st.session_state.auth = {"role": role, "ok": True, "user": user}
            st.rerun()
        else:
            st.error("Invalid credentials")

def about_page():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown("<h3>Welcome to <strong>BAQĀ</strong></h3>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>BAQĀ is an intelligent data-driven platform that integrates multi-source medical data to assist healthcare professionals and decision-makers in predicting cancer outcomes, optimizing interventions, and improving patients’ quality of life.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to Decision Dashboard"):
            st.session_state.auth["role"] = "Decision-Maker"; st.rerun()
    with col2:
        if st.button("Go to Physician Panel"):
            st.session_state.auth["role"] = "Physician"; st.rerun()

def view_decision():
    topbar()
    st.markdown('<div class="hero"><h3>Decision-Makers Dashboard</h3><p class="subtitle">Demo data — replace with governed sources (registries/EMR/BI).</p></div>', unsafe_allow_html=True)
    rng = np.random.default_rng(seed=2025)
    c1,c2,c3,c4 = st.columns(4)
    metrics = {"Cases Included": f"{int(rng.integers(20000,36000)):,}","Deaths Included": f"{int(rng.integers(11000,18000)):,}","Overall Risk Level": rng.choice(["Low","Moderate","High"], p=[0.25,0.55,0.20]),"Five-year Mortality": f"{round(rng.uniform(0.10,0.18)*100,1)}%"}
    for col,(k,v) in zip([c1,c2,c3,c4], metrics.items()):
        with col: st.markdown(f"<div class='card kpi'><div class='label'>{k}</div><div class='value'>{v}</div></div>", unsafe_allow_html=True)
    A,B = st.columns([1.35,1])
    with A:
        st.subheader("Mortality Risk by Region (demo)")
        regions = ["Makkah","Riyadh","Eastern","Madinah","Qassim","Asir","Tabuk"]
        values = rng.integers(10,100,len(regions))
        fig, ax = plt.subplots(); ax.bar(regions, values); ax.set_ylabel("Risk Index"); ax.set_title("Risk by Region"); st.pyplot(fig)
    with B:
        st.subheader("High-Risk Factors")
        factors = ["Cardiovascular Disease","Diabetes","Older Age","CKD","Leukemia","Liver Disease","Hypertension"]
        perc = rng.integers(6,26,len(factors))
        fig2, ax2 = plt.subplots(); ax2.barh(factors, perc); ax2.set_xlabel("Contribution (%)"); st.pyplot(fig2)

def export_pdf(patient_dict, risk_prob, logo_path:Path):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from datetime import datetime
    buf_path = Path("patient_report.pdf")
    c = canvas.Canvas(str(buf_path), pagesize=A4)
    w, h = A4
    try:
        if logo_path.exists():
            c.drawImage(ImageReader(str(logo_path)), 40, h-120, width=90, height=90, mask='auto')
    except Exception: pass
    c.setFont("Helvetica-Bold", 16); c.drawString(150, h-60, "BAQĀ – Patient Assessment Report")
    c.setFont("Helvetica", 10); c.drawString(150, h-78, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.line(40, h-130, w-40, h-130)
    y = h-160; c.setFont("Helvetica-Bold", 12); c.drawString(40, y, "Patient Info:"); y -= 18; c.setFont("Helvetica", 11)
    for k,v in patient_dict.items(): c.drawString(52, y, f"{k}: {v}"); y -= 16
    y -= 10; c.setFont("Helvetica-Bold", 12); c.drawString(40, y, "Risk Summary:"); y -= 18
    lvl = "Low" if risk_prob<0.33 else "Moderate" if risk_prob<0.66 else "High"
    c.setFont("Helvetica", 11); c.drawString(52, y, f"Estimated 1-year mortality probability: {risk_prob*100:.1f}%"); y -= 16
    c.drawString(52, y, f"Risk Level: {lvl}")
    c.showPage(); c.save(); return buf_path

def view_physician():
    topbar()
    st.markdown("<div class='hero'><h3>Patient Assessment</h3><p class='subtitle'>Leukemia mortality risk — demo model (not for clinical use).</p></div>", unsafe_allow_html=True)
    c1,c2 = st.columns([1.05,1])
    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        age = st.selectbox("Age", list(range(18,90)), index=50)
        mutation = st.selectbox("Genetic Mutation", ["None","FLT3-ITD","NPM1","IDH1","IDH2"], index=1)
        response = st.selectbox("Treatment Response", ["Complete","Partial","Stable","Progression"], index=1)
        ldh = st.number_input("LDH Level (U/L)", value=520, min_value=80, max_value=2000, step=10)
        predict = st.button("Predict")
        st.caption("Demo only — replace with validated, peer-reviewed model and governed thresholds.")
        st.markdown("</div>", unsafe_allow_html=True)
    if predict:
        score = (age-50)*0.02 + (0.6 if mutation=="FLT3-ITD" else 0.25 if mutation in ["IDH1","IDH2"] else 0.15 if mutation=="NPM1" else 0) + (0.3 if response=="Partial" else 0.7 if response=="Progression" else -0.25 if response=="Complete" else 0.1) + max(0, (ldh-250)/500)*0.5
        st.session_state.risk_prob = float(1/(1+np.exp(-score)))
    rp = float(st.session_state.risk_prob)
    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**LEUKEMIA MORTALITY RISK**")
        angle = -90 + rp*180
        st.markdown(f"<div class='gauge'><div class='needle' style='transform: translateX(-50%) rotate({angle}deg);'></div></div>", unsafe_allow_html=True)
        st.markdown(f"<p>Risk Level: <span class='tag'>{'Low' if rp<0.33 else 'Moderate' if rp<0.66 else 'High'}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p>Estimated 1-year mortality probability: <strong>{rp*100:.1f}%</strong></p>", unsafe_allow_html=True)
        pdf_btn = st.button("Export PDF Report")
        st.markdown("</div>", unsafe_allow_html=True)
    x,y = st.columns(2)
    with x:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**Risk Factors**")
        st.write(f"- Age: {age}"); st.write(f"- Mutation: {mutation}"); st.write(f"- Treatment response: {response}"); st.write(f"- LDH: {ldh} U/L")
        st.markdown("</div>", unsafe_allow_html=True)
    with y:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**Survival Probability (demo curve)**")
        t = np.linspace(0, 5, 60); baseline = 0.95*np.exp(-0.2*t); adj = np.clip(1 - rp*0.7, 0.2, 1.0); curve = baseline*adj
        fig, ax = plt.subplots(); ax.plot(t, curve); ax.set_xlabel("Time (years)"); ax.set_ylabel("Probability"); ax.set_ylim(0,1.0); st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)
    if 'pdf_ready' not in st.session_state: st.session_state.pdf_ready = None
    if 'pdf_name' not in st.session_state: st.session_state.pdf_name = None
    if st.session_state.get('risk_prob') is not None and 'pdf_btn' in locals() and pdf_btn:
        pdata = {"Age": age, "Mutation": mutation, "Response": response, "LDH": f"{ldh} U/L"}
        path = export_pdf(pdata, rp, LOGO)
        st.session_state.pdf_ready = path; st.session_state.pdf_name = f"BAQA_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    if st.session_state.pdf_ready:
        with open(st.session_state.pdf_ready, "rb") as f: st.download_button("Download PDF", f, file_name=st.session_state.pdf_name, mime="application/pdf")

# Router
if not st.session_state.entered:
    splash()
else:
    if not st.session_state.auth.get("ok"):
        login()
        # After successful login, show About page automatically
        if st.session_state.auth.get("ok"):
            about_page()
    else:
        # Show About page once then route to chosen role
        if st.session_state.get("show_about_once", True):
            st.session_state.show_about_once = False
            about_page()
        else:
            if st.session_state.auth["role"] == "Decision-Maker":
                view_decision()
            else:
                view_physician()

st.markdown("---")
st.caption("Trusted references: WHO · IARC GLOBOCAN · NCCN · ClinicalTrials.gov. Demo only — not for clinical use.")
