import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- CSS חזק לתיקון עברית ואנגלית משולבת ---
st.markdown("""
    <style>
    /* הופך את כל האתר לימין לשמאל */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    /* שומר על נוסחאות אנגליות משמאל לימין שלא יתהפכו */
    .katex {
        direction: ltr !important;
        display: inline-block !important;
    }
    /* תיקון לכיווניות של טקסט בתוך כפתורים ורדיו */
    div[role="radiogroup"] {
        direction: rtl;
        text-align: right;
    }
    label {
        direction: rtl;
        text-align: right;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

def heb(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- מאגר שאלות עם עיצוב מוגן ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {
            "topic": "Diffusion",
            "q": "מה קורה למרחק הדיפוזיה $L_p$ אם נקטין את זמן החיים $\\tau_p$?",
            "opts": ["1. הוא יגדל", "2. הוא יקטן", "3. לא ישתנה"],
            "ans": 1,
            "explain": "לפי נוסחה (7): $L_p = \\sqrt{D_p \\tau_p}$. הקטנת זמן החיים מקטינה את המרחק שהמטען עובר."
        },
        {
            "topic": "PN Junction",
            "q": "באיזה צד של צומת $P^+N$ אזור המחסור $W$ יהיה רחב יותר?",
            "opts": ["1. בצד P (המסומם חזק)", "2. בצד N (המסומם חלש)", "3. בשניהם במידה שווה"],
            "ans": 1,
            "explain": "אזור המחסור תמיד חודר יותר עמוק לצד שבו ריכוז האילוח נמוך יותר."
        }
    ]

# --- ממשק משתמש ---
st.title("🎓 סימולטור מל''מ - אריאל")

if 'idx' not in st.session_state: st.session_state.idx = 0
curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.5, 1])

with col1:
    st.write(f"### נושא: {curr['topic']}")
    st.markdown(f"#### {curr['q']}")
    
    # הצגת התשובות
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    if st.button("בדוק תשובה"):
        if curr['opts'].index(ans) == curr['ans']:
            st.balloons()
            st.success("✅ נכון מאוד! " + curr['explain'])
        else:
            st.error("❌ לא נכון. " + curr['explain'])

    if st.button("שאלה הבאה ➡️"):
        st.session_state.idx += 1
        st.rerun()

with col2:
    # סימולציה ויזואלית פשוטה
    st.write("### המחשה גרפית")
    fig, ax = plt.subplots(figsize=(5,3))
    x = np.linspace(0, 5, 100)
    # גרף דעיכה עבור השאלה הראשונה
    ax.plot(x, np.exp(-x), color='blue', label=heb('דעיכת מטען'))
    ax.set_title(heb('מרחק דיפוזיה'))
    st.pyplot(fig)
