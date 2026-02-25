import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- CSS חזק לתיקון תצוגה ומניעת "מגדלי מספרים" ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #fcfcfc; }
    
    /* מניעת שבירת שורות בתוך נוסחאות וכפיית כיוון LTR */
    .katex { 
        direction: ltr !important; 
        display: inline-block !important; 
        white-space: nowrap !important;
        font-size: 1.2em !important;
        color: #003366;
    }
    
    .q-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-right: 10px solid #004a99;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    div[role="radiogroup"] label { direction: rtl; text-align: right; display: block; padding: 10px 0; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מעודכן (הנתונים עברו לתשובות) ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # שאלה חישובית מהתמונה [cite: 16-20, 112-126]
        {
            "topic": "Physics", "type": "ni", 
            "q": "נתונה פיסת סיליקון בשיווי משקל. מהו ריכוז האלקטרונים בהינתן הנתונים הבאים?", 
            "opts": [
                r"(1) $N_a=10^{17}, N_d=9\cdot 10^{16}, n_i=10^{17} \rightarrow n = 9.5 \cdot 10^{16} \text{ cm}^{-3}$", 
                r"(2) $N_a=10^{17}, N_d=9\cdot 10^{16}, n_i=10^{17} \rightarrow n = 9 \cdot 10^{16} \text{ cm}^{-3}$", 
                r"(3) $N_a=10^{17}, N_d=9\cdot 10^{16}, n_i=10^{17} \rightarrow n = 10^{16} \text{ cm}^{-3}$", 
                r"(4) $n = 10^3 \text{ cm}^{-3}$", 
                r"(5) $n = 2 \cdot 10^3 \text{ cm}^{-3}$"
            ], 
            "ans": 0, "explain": "נשתמש במשוואה הריבועית לניטרליות מטען המביאה בחשבון את הריכוז האינטרינזי הגבוה."
        },
        # שאלה על BJT [cite: 39-56, 135-152]
        {
            "topic": "BJT", "type": "bjt", 
            "q": "נתון טרנזיסטור PNP הפועל בתחום הפעיל הקדמי. מהו זרם הבסיס לפי הפרמטרים הבאים?", 
            "opts": [
                r"(1) $\gamma=0.8, b=0.9, I_E=10mA \rightarrow I_B = 8 mA$", 
                r"(2) $\gamma=0.8, b=0.9, I_E=10mA \rightarrow I_B = 9 mA$", 
                r"(3) $\gamma=0.8, b=0.9, I_E=10mA \rightarrow I_B = 1 mA$", 
                r"(4) $I_B = 2 mA$", 
                r"(5) $\gamma=0.8, b=0.9, I_E=10mA \rightarrow I_B = 2.8 mA$"
            ], 
            "ans": 4, "explain": "הגבר הזרם הוא המכפלה של גמא ב-b, ומכאן מחשבים את זרם הקולט והבסיס."
        },
        # שאלה תיאורטית - מרחק דיפוזיה [cite: 4, 107-110]
        {
            "topic": "Illumination", "type": "decay", 
            "q": "כיצד משתנה המרחק הממוצע אותו יחדור עודף המטען בחלק החשוך אם נשנה את עוצמת ההארה?", 
            "opts": [
                "(1) עוצמת הארה P מול 4P -> המרחק שווה בשני הניסויים.", 
                "(2) עוצמת הארה P מול 4P -> המרחק יוכפל בניסוי השני.", 
                "(3) המרחק יגדל פי 4 בניסוי השני.", 
                "(4) המרחק יגדל פי שורש 2.", 
                "(5) המרחק יקטן פי 2."
            ], 
            "ans": 0, "explain": "מרחק הדיפוזיה תלוי רק בתכונות החומר (D ו-tau) ולא בעוצמת האור."
        }
    ]

# --- יצירת טאבים ---
tab1, tab2 = st.tabs(["📝 סימולטור מבחן", "🧮 מחשבון ונתונים"])

with tab1:
    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.markdown(f"""<div class='q-card'>
            <p style='color: #004a99; font-weight: bold;'>שאלה {st.session_state.idx + 1} | נושא: {curr['topic']}</p>
            <p style='font-size: 1.25rem;'>{curr['q']}</p>
        </div>""", unsafe_allow_html=True)
        
        ans = st.radio("בחר תשובה (הנתונים מופיעים כאן):", curr['opts'], key=f"q_{st.session_state.idx}")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("בדוק תשובה ✅"):
                if curr['opts'].index(ans) == curr['ans']:
                    st.success("נכון מאוד!"); st.balloons()
                else: st.error("טעות. הסבר: " + curr['explain'])
        with c2:
            if st.button("שאלה הבאה ➡️"):
                st.session_state.idx += 1; st.rerun()

    with col2:
        st.write("### המחשה פיזיקלית")
        fig, ax = plt.subplots(figsize=(5, 4))
        if curr['type'] == "ni":
            t = np.linspace(250, 600, 100); ni_v = 1e10 * (t/300)**3 * np.exp(-1.12/(2*8.6e-5*t))
            ax.semilogy(t, ni_v, color='orange'); ax.set_title("Intrinsic Concentration")
        elif curr['type'] == "decay":
            x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue', lw=2); ax.set_title("Carrier Decay")
        elif curr['type'] == "bjt":
            ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3)); ax.text(0.15, 0.5, "E")
            ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3)); ax.text(0.32, 0.5, "B")
            ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3)); ax.text(0.55, 0.5, "C")
            ax.axis('off')
        st.pyplot(fig)

with tab2:
    st.header("🧮 נתונים פיזיקליים ומחשבון")
    
    st.subheader("📋 קבועים חשובים (ב-300K)")
    st_c1, st_c2, st_c3 = st.columns(3)
    st_c1.latex(r"q = 1.6 \cdot 10^{-19} \text{ C}")
    st_c2.latex(r"k = 8.617 \cdot 10^{-5} \text{ eV/K}")
    st_c3.latex(r"\epsilon_{Si} = 11.7 \cdot \epsilon_0")
    
    st.divider()
    st.write("### מחשבון ריכוזים מהיר")
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1: na_v = st.number_input("$N_a$ [cm⁻³]", value=1.0e17, format="%.2e")
    with col_i2: nd_v = st.number_input("$N_d$ [cm⁻³]", value=9.0e16, format="%.2e")
    with col_i3: ni_v = st.number_input("$n_i$ [cm⁻³]", value=1.0e17, format="%.2e")
    
    diff = na_v - nd_v
    n_res = (-diff + np.sqrt(diff**2 + 4*ni_v**2)) / 2
    p_res = ni_v**2 / n_res
    
    st.write(f"**תוצאה:**")
    st.latex(r"n = " + f"{n_res:.3e}" + r" \text{ cm}^{-3}")
    st.latex(r"p = " + f"{p_res:.3e}" + r" \text{ cm}^{-3}")
