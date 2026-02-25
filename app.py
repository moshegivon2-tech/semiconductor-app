import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- CSS חזק לתיקון ה"מגדלים" וה-RTL ---
st.markdown("""
    <style>
    /* הגדרת כיוון כללי לימין */
    .stApp { 
        direction: rtl; 
        text-align: right; 
        background-color: #f8f9fa; 
    }
    
    /* פתרון ה"מגדלים": מניעת שבירת שורות בתוך נוסחאות וכפיית כיוון LTR */
    .katex { 
        direction: ltr !important; 
        display: inline-block !important; 
        white-space: nowrap !important;
        unicode-bidi: isolate !important;
        font-size: 1.1em !important;
        color: #003366;
    }
    
    /* יישור תיבת השאלה והתשובות */
    .q-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-right: 8px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    div[role="radiogroup"] label { 
        direction: rtl; 
        text-align: right; 
        display: block; 
        padding: 8px 0;
    }
    
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- יצירת טאבים ---
tab1, tab2 = st.tabs(["📝 סימולטור מבחן", "🧮 מחשבון ריכוזים"])

# --- טאב 1: סימולטור מבחן ---
with tab1:
    if 'questions' not in st.session_state:
        st.session_state.questions = [
            # שאלה חישובית מהתמונה image_053200.png
            {
                "topic": "Physics", 
                "type": "ni", 
                "q": "נתונה פיסת סיליקון בשיווי משקל בה סיגים נוטלים ($N_a$) בריכוז $10^{17} \\text{ cm}^{-3}$ ותורמים ($N_d$) בריכוז $9 \\cdot 10^{16} \\text{ cm}^{-3}$, וריכוז אינטרינזי ($n_i$) של $10^{17} \\text{ cm}^{-3}$. מהו ריכוז האלקטרונים ($n$)?", 
                "opts": [
                    "(1) $9.5 \\cdot 10^{16} \\text{ cm}^{-3}$", 
                    "(2) $9 \\cdot 10^{16} \\text{ cm}^{-3}$", 
                    "(3) $10^{16} \\text{ cm}^{-3}$", 
                    "(4) $10^3 \\text{ cm}^{-3}$", 
                    "(5) $2 \\cdot 10^3 \\text{ cm}^{-3}$"
                ], 
                "ans": 0, 
                "explain": "נשתמש במשוואה הריבועית לניטרליות מטען: $n^2 + (N_a - N_d)n - n_i^2 = 0$. פתרון המשוואה נותן בדיוק $9.5 \\cdot 10^{16}$[cite: 117]."
            },
            # שאלת הארה [cite: 4, 100-110]
            {
                "topic": "Illumination", 
                "type": "decay", 
                "q": "בוצעו שני ניסויים של הארת חצי דגם מל''מ, בראשון בעוצמה $P$ ובשני פי ארבעה ($4P$). המרחק הממוצע $L$ שחודר עודף המטען בחלק החשוך הינו: [cite: 4, 100-110]", 
                "opts": [
                    "(1) שווה בשני הניסויים.", 
                    "(2) כפול בניסוי השני.", 
                    "(3) פי ארבעה בניסוי השני.", 
                    "(4) גדול פי $4 \\ln$ בניסוי השני.", 
                    "(5) גדול פי $e^4$ בניסוי השני."
                ], 
                "ans": 1, 
                "explain": "מרחק הדיפוזיה $L = \\sqrt{D \\tau}$ הוא תכונת חומר ואינו תלוי בעוצמת ההארה [cite: 107-110]."
            },
            # שאלת דיודה [cite: 31-36]
            {
                "topic": "PN Junction", 
                "type": "field", 
                "q": "בדיודת צומת, איזה מהמשפטים הבאים שגוי תמיד? [cite: 31-36]", 
                "opts": [
                    "(1) המתח המובנה נופל בעקרו על הצד בעל ריכוז הסיגים הנמוך.", 
                    "(2) השדה החשמלי מקסימלי בצומת בנקודת הצומת המטלורגי.", 
                    "(3) הזרם בממתח אחורי גדל (בגודלו) עם המתח.", 
                    "(4) הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה.", 
                    "(5) המתח הכולל על הצומת בממתח קדמי קטן מהמתח המובנה."
                ], 
                "ans": 3, 
                "explain": "בדיודה קצרה הגרדיאנט חד יותר, ולכן הזרם בה תמיד גדול יותר מאשר בדיודה ארוכה[cite: 35]."
            },
            # שאלת BJT [cite: 39-56]
            {
                "topic": "BJT", 
                "type": "bjt", 
                "q": "נתון טרנזיסטור PNP עם $\\gamma=0.8$ ו-$b=0.9$. במצב פעיל קדמי $I_E=10mA$. מהו זרם הבסיס $I_B$? [cite: 39-56]", 
                "opts": [
                    "(1) $8 mA$", 
                    "(2) $9 mA$", 
                    "(3) $1 mA$", 
                    "(4) $2 mA$", 
                    "(5) $2.8 mA$"
                ], 
                "ans": 4, 
                "explain": "$\\alpha = \\gamma \\cdot b = 0.72$. לכן $I_C = 7.2mA$ וזרם הבסיס הוא $I_E - I_C = 2.8mA$ [cite: 55-56]."
            }
        ]

    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

    col1, col2 = st.columns([1.6, 1])

    with col1:
        st.markdown(f"""<div class='q-card'>
            <p style='color: #1e3a8a; font-weight: bold;'>שאלה {st.session_state.idx + 1} | נושא: {curr['topic']}</p>
            <p style='font-size: 1.2rem;'>{curr['q']}</p>
        </div>""", unsafe_allow_html=True)
        
        ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button("בדוק תשובה ✅"):
                if curr['opts'].index(ans) == curr['ans']:
                    st.success("נכון מאוד! " + curr['explain']); st.balloons()
                else: st.error("טעות. הסבר: " + curr['explain'])
        with b2:
            if st.button("שאלה הבאה ➡️"):
                st.session_state.idx += 1; st.rerun()

    with col2:
        st.write("### המחשה פיזיקלית")
        fig, ax = plt.subplots(figsize=(5, 4))
        t_type = curr.get("type", "none")
        if t_type == "ni":
            temp = np.linspace(250, 600, 100); ni_v = 1e10 * (temp/300)**3 * np.exp(-1.12/(2*8.6e-5*temp))
            ax.semilogy(temp, ni_v, color='orange'); ax.set_title("Intrinsic Concentration")
            # 
        elif t_type == "decay":
            x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue', lw=2); ax.set_title("Carrier Decay")
            # 
        elif t_type == "field":
            x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1+x, 1-2*x); e[x>0.5]=0; e[x<-1.5]=0
            ax.fill_between(x, e, color='red', alpha=0.3); ax.set_title("Electric Field")
            # 
        elif t_type == "bjt":
            ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3))
            ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3))
            ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3))
            ax.text(0.2, 0.5, "E"); ax.text(0.35, 0.5, "B"); ax.text(0.6, 0.5, "C"); ax.axis('off')
            # 
        st.pyplot(fig)

# --- טאב 2: מחשבון ריכוזים ---
with tab2:
    st.header("🧮 מחשבון ריכוזי מטענים (שיווי משקל)")
    st.write("פותר את משוואת ניטרליות המטען: $n^2 + (N_a - N_d)n - n_i^2 = 0$")
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1: na_val = st.number_input("$N_a$ [cm⁻³]", value=1.0e17, format="%.2e")
    with col_i2: nd_val = st.number_input("$N_d$ [cm⁻³]", value=9.0e16, format="%.2e")
    with col_i3: ni_val = st.number_input("$n_i$ [cm⁻³]", value=1.0e17, format="%.2e")
    diff = na_val - nd_val
    n_res = (-diff + np.sqrt(diff**2 + 4*ni_val**2)) / 2
    p_res = ni_val**2 / n_res
    st.divider()
    r1, r2 = st.columns(2)
    r1.metric("ריכוז אלקטרונים $n$", f"{n_res:.3e}")
    r2.metric("ריכוז חורים $p$", f"{p_res:.3e}")
