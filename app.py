import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- CSS מתקדם לתיקון תצוגה, RTL ומניעת "מגדלי מספרים" ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #fcfcfc; }
    
    /* מניעת שבירת שורות בתוך נוסחאות וכפיית כיוון LTR */
    .katex { 
        direction: ltr !important; 
        display: inline-block !important; 
        white-space: nowrap !important;
        font-size: 1.15em !important;
        color: #003366;
    }
    
    /* עיצוב תיבת השאלה */
    .q-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-right: 10px solid #004a99;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    
    /* יישור תשובות */
    div[role="radiogroup"] label { direction: rtl; text-align: right; display: block; padding: 10px 0; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- יצירת טאבים למחשבון ולמבחן ---
tab1, tab2 = st.tabs(["📝 סימולטור מבחן", "🧮 מחשבון ריכוזים"])

# --- מאגר שאלות מלא ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # שאלה חישובית מהתמונה [cite: 16-20, 112-126]
        {
            "topic": "Physics", 
            "type": "ni", 
            "q": r"נתונה פיסת סיליקון בשיווי משקל בה $N_a = 10^{17} \text{ cm}^{-3}$ ו-$N_d = 9 \cdot 10^{16} \text{ cm}^{-3}$, וריכוז אינטרינזי $n_i = 10^{17} \text{ cm}^{-3}$. מהו ריכוז האלקטרונים $n$?", 
            "opts": [
                r"(1) $9.5 \cdot 10^{16} \text{ cm}^{-3}$", 
                r"(2) $9 \cdot 10^{16} \text{ cm}^{-3}$", 
                r"(3) $10^{16} \text{ cm}^{-3}$", 
                r"(4) $10^3 \text{ cm}^{-3}$", 
                r"(5) $2 \cdot 10^3 \text{ cm}^{-3}$"
            ], 
            "ans": 0, 
            "explain": r"נשתמש במשוואה הריבועית: $n^2 + (N_a - N_d)n - n_i^2 = 0$. הצבה נותנת $9.5 \cdot 10^{16}$."
        },
        # שאלת הארה [cite: 4, 100-110]
        {
            "topic": "Illumination", 
            "type": "decay", 
            "q": "בוצעו שני ניסויים של הארת חצי דגם מל''מ, בראשון בעוצמה $P$ ובשני פי ארבעה $4P$. המרחק הממוצע $L$ שחודר עודף המטען בחושך הינו:", 
            "opts": ["(1) שווה בשני הניסויים.", "(2) כפול בניסוי השני.", "(3) פי ארבעה בניסוי השני.", "(4) גדול פי $4 \ln$ בניסוי השני.", "(5) גדול פי $e^4$ בניסוי השני."], 
            "ans": 0, 
            "explain": "מרחק הדיפוזיה $L = \\sqrt{D \\tau}$ הוא תכונת חומר ואינו תלוי בעוצמת ההארה [cite: 107-110]."
        },
        # שאלת דיודה שגויה [cite: 31-36]
        {
            "topic": "PN Junction", 
            "type": "field", 
            "q": "בדיודת צומת, איזה מהמשפטים הבאים שגוי תמיד?", 
            "opts": ["(1) המתח המובנה נופל בעיקר על הצד בעל סימום נמוך.", "(2) השדה המקסימלי בנקודת הצומת המטלורגי.", "(3) הזרם בממתח אחורי גדל עם המתח.", "(4) הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה.", "(5) המתח הכולל בממתח קדמי קטן מהמתח המובנה."], 
            "ans": 3, 
            "explain": "בדיודה קצרה הגרדיאנט חד יותר ולכן הזרם תמיד גדול יותר מאשר בדיודה ארוכה[cite: 35]."
        }
    ]

with tab1:
    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.markdown(f"""<div class='q-card'>
            <p style='color: #004a99; font-weight: bold;'>שאלה {st.session_state.idx + 1} | נושא: {curr['topic']}</p>
            <p style='font-size: 1.25rem;'>{curr['q']}</p>
        </div>""", unsafe_allow_html=True)
        
        ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
        
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("בדוק תשובה ✅"):
                if curr['opts'].index(ans) == curr['ans']:
                    st.success("נכון מאוד!"); st.balloons()
                else: st.error("טעות. הסבר: " + curr['explain'])
        with c_b2:
            if st.button("שאלה הבאה ➡️"):
                st.session_state.idx += 1; st.rerun()

    with col2:
        st.write("### המחשה פיזיקלית")
        fig, ax = plt.subplots(figsize=(5, 4))
        if curr['type'] == "ni":
            t = np.linspace(250, 600, 100); ni = 1e10 * (t/300)**3 * np.exp(-1.12/(2*8.6e-5*t))
            ax.semilogy(t, ni, color='orange'); ax.set_title("Intrinsic Concentration")
            
        elif curr['type'] == "decay":
            x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue'); ax.set_title("Minority Carrier Decay")
            
        elif curr['type'] == "field":
            x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1+x, 1-2*x); e[x>0.5]=0; e[x<-1.5]=0
            ax.fill_between(x, e, color='red', alpha=0.3); ax.set_title("Electric Field")
            
        st.pyplot(fig)

with tab2:
    st.header("🧮 מחשבון ריכוזים (שיווי משקל)")
    st.write("פותר את המשוואה: $n^2 + (N_a - N_d)n - n_i^2 = 0$")
    c_in1, c_in2, c_in3 = st.columns(3)
    with c_in1: na_val = st.number_input("$N_a$ [cm⁻³]", value=1.0e17, format="%.2e")
    with c_in2: nd_val = st.number_input("$N_d$ [cm⁻³]", value=9.0e16, format="%.2e")
    with c_in3: ni_val = st.number_input("$n_i$ [cm⁻³]", value=1.0e17, format="%.2e")
    
    diff = na_val - nd_val
    n_res = (-diff + np.sqrt(diff**2 + 4*ni_val**2)) / 2
    p_res = ni_val**2 / n_res
    st.divider()
    r1, r2 = st.columns(2)
    r1.metric("ריכוז אלקטרונים $n$", f"{n_res:.3e}")
    r2.metric("ריכוז חורים $p$", f"{p_res:.3e}")
