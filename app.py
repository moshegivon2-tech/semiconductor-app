import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- CSS חזק לנעילת המספרים והנוסחאות בשורה אחת ---
st.markdown("""
    <style>
    /* כיווניות כללית לימין */
    .stApp { 
        direction: rtl; 
        text-align: right; 
        background-color: #f8f9fa; 
    }
    
    /* פתרון ה"מגדלים": מניעת שבירה וכפיית כיוון LTR לנוסחאות בלבד */
    .katex { 
        direction: ltr !important; 
        display: inline-block !important; 
        white-space: nowrap !important;
        unicode-bidi: isolate !important;
        font-size: 1.1em !important;
    }
    
    /* עיצוב תיבת השאלה */
    .q-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-right: 8px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* יישור תשובות */
    div[role="radiogroup"] label { 
        direction: rtl; 
        text-align: right; 
        display: block; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מלא ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # שאלה חישובית מהתמונה
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
            "explain": "נשתמש במשוואה הריבועית לניטרליות מטען: $n^2 + (N_a - N_d)n - n_i^2 = 0$. פתרון המשוואה עבור הנתונים נותן בדיוק $9.5 \\cdot 10^{16}$."
        },
        # [cite_start]שאלת דיודה מהמבחן [cite: 31-36]
        {
            "topic": "PN Junction", 
            "type": "field", 
            "q": "בדיודת צומת, איזה מהמשפטים הבאים שגוי תמיד?", 
            "opts": [
                "(1) המתח המובנה נופל בעקרו על הצד בעל ריכוז הסיגים הנמוך.", 
                "(2) השדה החשמלי מקסימלי בצומת בנקודת הצומת המטלורגי.", 
                "(3) הזרם בממתח אחורי גדל (בגודלו) עם המתח.", 
                "(4) הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה.", 
                "(5) המתח הכולל על הצומת בממתח קדמי קטן מהמתח המובנה."
            ], 
            "ans": 3, 
            [cite_start]"explain": "בדיודה קצרה הגרדיאנט חד יותר, ולכן הזרם בה תמיד גדול יותר מאשר בדיודה ארוכה[cite: 35]."
        }
    ]

# --- לוגיקת האפליקציה ---
st.title("🎓 סימולטור מל''מ - אוניברסיטת אריאל")

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
        temp = np.linspace(250, 600, 100)
        ni_v = 1e10 * (temp/300)**3 * np.exp(-1.12/(2*8.6e-5*temp))
        ax.semilogy(temp, ni_v, color='orange')
        ax.set_title("Intrinsic Carrier Concentration")
    elif t_type == "field":
        x = np.linspace(-2, 2, 100)
        e = np.where(x < 0, 1+x, 1-2*x)
        e[x>0.5]=0; e[x<-1.5]=0
        ax.fill_between(x, e, color='red', alpha=0.3)
        ax.set_title("Electric Field in Junction")
    
    st.pyplot(fig)

st.divider()
[cite_start]st.caption("מבוסס על מקבצי השאלות הרשמיים [cite: 1-507]")
