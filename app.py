import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- CSS חזק לתיקון עברית ו-RTL ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .katex { direction: ltr !important; display: inline-block !important; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    label { direction: rtl; text-align: right; display: block; }
    </style>
    """, unsafe_allow_html=True)

def heb(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- מאגר שאלות מורחב עם סוגי גרפים (Type) ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {
            "topic": "Diffusion",
            "type": "decay",
            "q": "מה קורה למרחק הדיפוזיה $L_p$ אם נקטין את זמן החיים $\\tau_p$?",
            "opts": ["1. הוא יגדל", "2. הוא יקטן", "3. לא ישתנה"],
            "ans": 1,
            "explain": "לפי נוסחה (7): $L_p = \\sqrt{D_p \\tau_p}$. הקטנת זמן החיים מקטינה את המרחק שהמטען עובר."
        },
        {
            "topic": "PN Junction",
            "type": "field",
            "q": "היכן השדה החשמלי הוא מקסימלי בצומת $PN$ בשיווי משקל?",
            "opts": ["1. בקצוות אזור המחסור", "2. בדיוק במטלורגיית הצומת (x=0)", "3. מחוץ לאזור המחסור"],
            "ans": 1,
            "explain": "לפי נוסחה (34), השדה גדל ליניארית בתוך אזור המחסור ומגיע לשיאו בדיוק בנקודת המגע בין P ל-N."
        },
        {
            "topic": "Physics",
            "type": "ni",
            "q": "איך משתנה הריכוז האינטרינזי $n_i$ עם עליית הטמפרטורה?",
            "opts": ["1. עולה אקספוננציאלית", "2. יורד ליניארית", "3. נשאר קבוע"],
            "ans": 0,
            "explain": "נוסחה (17): $n_i$ תלוי ב-$T^{1.5}$ ובאקספוננט של הטמפרטורה, לכן הוא גדל מאוד עם החום."
        },
        {
            "topic": "MOS",
            "type": "cv",
            "q": "מה קורה לקיבול הדיפרנציאלי בתחום האקומולציה?",
            "opts": ["1. הוא שואף ל-$C_{ox}$", "2. הוא שואף לאפס", "3. הוא מינימלי"],
            "ans": 0,
            "explain": "באקומולציה, המטענים נצמדים לתחמוצת ולכן הקיבול הנמדד הוא קיבול האוקסיד בלבד."
        }
    ]

# --- פונקציה ליצירת גרף דינמי לפי סוג השאלה ---
def plot_dynamic_sim(q_type):
    fig, ax = plt.subplots(figsize=(5, 3))
    
    if q_type == "decay":
        x = np.linspace(0, 5, 100)
        ax.plot(x, np.exp(-x), color='blue', lw=2)
        ax.set_title(heb("דעיכת ריכוז נושאי מטען מיעוט"))
        ax.set_xlabel(heb("מרחק"))
        
    elif q_type == "field":
        x = np.linspace(-2, 2, 100)
        e = np.where(x < 0, 2+x, 2-2*x); e[x > 1] = 0; e[x < -2] = 0
        ax.fill_between(x, e, color='red', alpha=0.3)
        ax.plot(x, e, color='red', lw=2)
        ax.set_title(heb("פילוג שדה חשמלי בצומת"))
        ax.set_xlabel(heb("מיקום x"))

    elif q_type == "ni":
        t = np.linspace(200, 500, 100)
        ni = 1e10 * (t/300)**1.5 * np.exp(-5000*(1/t - 1/300))
        ax.semilogy(t, ni, color='green', lw=2)
        ax.set_title(heb("ריכוז ni כפונקציה של טמפרטורה"))
        ax.set_xlabel("Temperature [K]")

    elif q_type == "cv":
        v = np.linspace(-2, 2, 100)
        c = np.where(v < 0, 1, np.where(v < 1, 1/(1+v), 0.4))
        ax.plot(v, c, color='purple', lw=2)
        ax.set_title(heb("עקומת קיבול C-V (תדר גבוה)"))
        ax.set_xlabel("Voltage [V]")

    st.pyplot(fig)

# --- ממשק משתמש ---
st.title("🎓 סימולטור מל''מ - אריאל")

if 'idx' not in st.session_state: st.session_state.idx = 0
curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.5, 1])

with col1:
    st.write(f"### נושא: {heb(curr['topic'])}")
    st.markdown(f"#### {curr['q']}")
    
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    if st.button("בדוק תשובה"):
        if curr['opts'].index(ans) == curr['ans']:
            st.balloons()
            st.success("✅ נכון! " + curr['explain'])
        else:
            st.error("❌ לא נכון. " + curr['explain'])

    if st.button("שאלה הבאה ➡️"):
        st.session_state.idx += 1
        st.rerun()

with col2:
    st.write(f"### {heb('המחשה גרפית')}")
    # כאן קורה הקסם - הפונקציה מקבלת את ה-type של השאלה הנוכחית
    plot_dynamic_sim(curr['type'])
