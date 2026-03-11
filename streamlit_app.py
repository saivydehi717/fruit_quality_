import streamlit as st
import numpy as np
from PIL import Image
import os

st.set_page_config(
    page_title="FruitAI Pro",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Force Light Theme + Custom CSS ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&family=Cormorant+Garamond:wght@600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Figtree', sans-serif !important;
    background-color: #f5f4f0 !important;
    color: #1a1814 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #1a1814 !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }
section[data-testid="stSidebar"] .stSlider label { color: rgba(255,255,255,0.7) !important; }

/* Main content */
.block-container { padding: 2rem 3rem !important; background: #f5f4f0 !important; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Upload area */
[data-testid="stFileUploader"] {
    background: #fff !important;
    border: 2px dashed #d4cfc4 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

/* Buttons */
.stButton > button {
    background: #1a1814 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Figtree', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-size: 12px !important;
}

/* Progress bar */
.stProgress > div > div { background: #1a7a4a !important; }

/* Spinner */
.stSpinner > div { border-top-color: #1a7a4a !important; }

/* Radio buttons */
[data-testid="stRadio"] label {
    background: #fff !important;
    border: 2px solid #e8e5de !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #1a1814 !important;
    cursor: pointer !important;
    transition: all .2s !important;
}
[data-testid="stRadio"] label:hover {
    border-color: #1a1814 !important;
    background: #f5f4f0 !important;
}
[data-testid="stRadio"] input:checked + div {
    color: #fff !important;
}
[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
    color: #1a1814 !important;
    font-weight: 600 !important;
}
/* Hide default radio circle */
[data-testid="stRadio"] input[type="radio"] { display: none !important; }

/* Cards */
.result-card {
    background: #ffffff;
    border: 1px solid #e8e5de;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.fruit-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 56px;
    font-weight: 700;
    letter-spacing: -2px;
    line-height: 1;
    color: #1a1814;
}
.fruit-emoji { font-size: 64px; line-height: 1; }
.badge {
    display: inline-block;
    padding: 8px 20px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 14px;
}
.fresh-badge  { background:#edf7f2; color:#1a7a4a; border:1.5px solid #b8dfc9; }
.rotten-badge { background:#fdf0f2; color:#9b2335; border:1.5px solid #e8b8c0; }
.nonfruit-badge { background:#eff2fb; color:#2d4a8a; border:1.5px solid #b8c4e8; }

.conf-card {
    background: #f5f4f0;
    border: 1px solid #e8e5de;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.conf-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #8a8478;
    margin-bottom: 8px;
}
.conf-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 52px;
    font-weight: 700;
    line-height: 1;
}
.pred-table {
    background: #fff;
    border: 1px solid #e8e5de;
    border-radius: 12px;
    overflow: hidden;
}
.pred-head {
    display: grid;
    grid-template-columns: 40px 1fr 80px;
    padding: 10px 16px;
    background: #f5f4f0;
    border-bottom: 1px solid #e8e5de;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #b0aa9e;
}
.pred-row {
    display: grid;
    grid-template-columns: 40px 1fr 80px;
    padding: 13px 16px;
    border-bottom: 1px solid #f0ede8;
    align-items: center;
    font-size: 13px;
}
.pred-row:last-child { border-bottom: none; }
.pred-row.top-row { background: linear-gradient(to right, rgba(26,122,74,0.04), transparent); }
.pred-rank {
    width: 24px; height: 24px;
    border-radius: 6px;
    background: #e8e5de;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: #8a8478;
}
.top-rank { background: #1a1814 !important; color: #fff !important; }
.pred-pct { font-weight: 700; text-align: right; }
.top-pct { color: #1a1814; }

.stat-card {
    background: #fff;
    border: 1px solid #e8e5de;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.stat-val {
    font-family: 'Cormorant Garamond', serif;
    font-size: 32px;
    font-weight: 700;
    color: #1a1814;
}
.stat-lbl {
    font-size: 10px;
    color: #b0aa9e;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 4px;
    font-weight: 600;
}

.page-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 52px;
    font-weight: 700;
    letter-spacing: -2px;
    line-height: 1;
    color: #1a1814;
}
.page-title span { color: #2a5c8a; }
.page-sub { font-size: 15px; color: #8a8478; margin-top: 8px; font-weight: 300; margin-bottom: 32px; }

.section-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #8a8478;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #e8e5de;
}
.empty-state {
    border: 2px dashed #e8e5de;
    border-radius: 12px;
    padding: 60px 20px;
    text-align: center;
    color: #b0aa9e;
}
.empty-icon { font-size: 48px; opacity: 0.4; display: block; margin-bottom: 12px; }
.empty-txt { font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────
@st.cache_resource
def load_model_cached():
    from tensorflow.keras.models import load_model as lm
    import gdown

    FILE_ID = "12L420Jqq2ldfHzLyY_kE2dRz8vh9rw3U"
    model_path = "best_fruit_model.h5"

    if os.path.exists("model/best_fruit_model.h5"):
        return lm("model/best_fruit_model.h5")

    if not os.path.exists(model_path):
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, model_path, quiet=False)

    if os.path.exists(model_path):
        return lm(model_path)
    return None

@st.cache_data
def get_classes():
    if os.path.exists("dataset/train"):
        return sorted(os.listdir("dataset/train"))
    return [
        "apple_fruit","banana_fruit","grape_fruit","mango_fruit","orange_fruit",
        "papaya_fruit","pineapple_fruit","pomegranate_fruit","strawberry_fruit","watermelon_fruit",
        "nonfruit_bottle","nonfruit_building","nonfruit_bus","nonfruit_car","nonfruit_cat",
        "nonfruit_chair","nonfruit_dog","nonfruit_laptop","nonfruit_mobile_phone","nonfruit_table",
        "rotten_apple_fruit","rotten_banana_fruit","rotten_grape_fruit","rotten_mango_fruit","rotten_orange_fruit",
        "rotten_papaya_fruit","rotten_pineapple_fruit","rotten_pomegranate_fruit","rotten_strawberry_fruit","rotten_watermelon_fruit"
    ]

# ── Helpers ───────────────────────────────────────────────────
def get_quality(cls):
    n = cls.lower()
    if n.startswith("rotten") or "rotten_" in n:
        return "rotten"
    if "nonfruit" in n or "non_fruit" in n:
        return "nonfruit"
    nk = ["car","bottle","building","chair","bus","cat","dog","laptop","mobile","phone","table"]
    if any(k in n for k in nk):
        return "nonfruit"
    return "fresh"

def clean_name(cls):
    n = cls.lower()
    if n.startswith("rotten_"):
        n = n[7:]
    for r in ["_fruit","nonfruit_","fruit_","non_fruit_"]:
        n = n.replace(r,"")
    return n.replace("_"," ").strip().title()

EMOJI = {"apple":"🍎","banana":"🍌","grape":"🍇","mango":"🥭","orange":"🍊",
         "pineapple":"🍍","strawberry":"🍓","watermelon":"🍉","papaya":"🍈","pomegranate":"🔴"}

def get_emoji(name):
    n = (name or "").lower()
    for k, v in EMOJI.items():
        if k in n: return v
    return "🍑"

def run_predict(img, model, class_names):
    arr = np.expand_dims(np.array(img.convert("RGB").resize((224,224))) / 255.0, axis=0)
    preds = model.predict(arr, verbose=0)[0]
    top3 = np.argsort(preds)[::-1][:3]
    return [{"class": class_names[i], "name": clean_name(class_names[i]),
             "confidence": round(float(preds[i])*100, 1)} for i in top3]

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍎 FruitAI Pro")
    st.markdown("**Quality Intelligence Platform v2.0**")
    st.divider()
    st.markdown("### 📊 Model Info")
    st.markdown("**Architecture:** MobileNetV2")
    st.markdown("**Input Size:** 224 × 224 px")
    st.markdown("**Classes:** 30 total")
    st.markdown("**Val Accuracy:** 89.8%")
    st.divider()
    st.markdown("### 📖 How to Use")
    st.markdown("1. Upload a fruit image")
    st.markdown("2. AI analyzes quality")
    st.markdown("3. Get Fresh / Rotten result")
    st.divider()
    conf_threshold = st.slider("Min Confidence %", 10, 90, 40, help="Results below this are marked uncertain")

# ── Load ──────────────────────────────────────────────────────
model = load_model_cached()
class_names = get_classes()

if model is None:
    st.error("❌ Model not found! Run `python train_model.py` first.")
    st.stop()
if not class_names:
    st.error("❌ Dataset folder not found!")
    st.stop()

# ── Header ────────────────────────────────────────────────────
st.markdown('<div class="page-title">Fruit Quality <span>Detection</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Upload a fruit image to receive instant AI-powered freshness classification</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

# ── Left — Input ──────────────────────────────────────────────
with col1:
    st.markdown('<div class="section-title">📷 Image Input</div>', unsafe_allow_html=True)
    input_mode = st.radio("Input method", ["Upload Image", "Use Camera"], horizontal=True, label_visibility="collapsed")
    img = None
    if input_mode == "Use Camera":
        cam = st.camera_input("Take photo", label_visibility="collapsed")
        if cam: img = Image.open(cam)
    else:
        up = st.file_uploader("Upload", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
        if up: img = Image.open(up)

    if img:
        st.image(img, use_container_width=True)
    else:
        st.markdown('''
        <div class="empty-state">
            <span class="empty-icon">📁</span>
            <div class="empty-txt">Upload or capture a fruit image</div>
        </div>''', unsafe_allow_html=True)

# ── Right — Result ────────────────────────────────────────────
with col2:
    st.markdown('<div class="section-title">🔬 Analysis Result</div>', unsafe_allow_html=True)

    if img is None:
        st.markdown('''
        <div class="empty-state">
            <span class="empty-icon">🔬</span>
            <div class="empty-txt">Submit an image to see results</div>
        </div>''', unsafe_allow_html=True)
    else:
        with st.spinner("Analyzing image..."):
            results = run_predict(img, model, class_names)

        top = results[0]
        quality = get_quality(top["class"])
        conf = top["confidence"]
        name = top["name"]
        emoji = get_emoji(name)

        if conf < conf_threshold:
            st.warning(f"⚠️ Low confidence ({conf}%) — try a clearer image")
        else:
            # Quality badge
            if quality == "fresh":
                badge = '<span class="badge fresh-badge">✦ Fresh — Good Quality</span>'
                conf_color = "#1a7a4a"
            elif quality == "rotten":
                badge = '<span class="badge rotten-badge">✦ Rotten — Poor Quality</span>'
                conf_color = "#9b2335"
            else:
                badge = '<span class="badge nonfruit-badge">✦ Non-Fruit Object</span>'
                conf_color = "#2d4a8a"

            # Result card
            st.markdown(f"""
            <div class="result-card">
                <div style="display:flex;align-items:center;gap:20px;margin-bottom:4px">
                    <div class="fruit-emoji">{emoji}</div>
                    <div>
                        <div class="fruit-name">{name}</div>
                        <div style="font-size:13px;color:#8a8478;margin-top:4px">{name} detected via AI analysis</div>
                        {badge}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Confidence
            st.markdown(f"""
            <div class="conf-card">
                <div class="conf-label">Confidence Score</div>
                <div class="conf-value" style="color:{conf_color}">{conf}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(int(conf))

            # Predictions table
            rows = ""
            for i, r in enumerate(results):
                top_cls = "top-row" if i == 0 else ""
                rank_cls = "top-rank" if i == 0 else ""
                pct_cls = "top-pct" if i == 0 else ""
                rows += f"""
                <div class="pred-row {top_cls}">
                    <div class="pred-rank {rank_cls}">{i+1}</div>
                    <div style="padding:0 10px;font-weight:{'600' if i==0 else '400'}">{r['name']}</div>
                    <div class="pred-pct {pct_cls}">{r['confidence']}%</div>
                </div>"""

            st.markdown(f"""
            <div class="pred-table">
                <div class="pred-head"><span>#</span><span>Classification</span><span style="text-align:right">Score</span></div>
                {rows}
            </div>
            """, unsafe_allow_html=True)

# ── Stats Footer ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
stats = [("30","Total Classes"),("89.8%","Val Accuracy"),("MobileNetV2","Architecture"),("224px","Input Size")]
for col, (val, lbl) in zip([c1,c2,c3,c4], stats):
    with col:
        st.markdown(f'<div class="stat-card"><div class="stat-val">{val}</div><div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)
