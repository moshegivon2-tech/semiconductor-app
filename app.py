import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- הזרקת CSS לתיקון עברית ו-RTL לכל האתר ---
st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    /* תיקון לכיווניות של נוסחאות מתמטיות שלא יתהפכו */
    .stMarkdown p, .stMarkdown span {
        direction: rtl;
        display: block;
    }
    .katex {
        direction: ltr !important;
        display: inline-block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# פונקציה לגרפים בלבד
def heb_graph(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- מאגר שאלות מעודכן (הדולרים עכשיו יעבדו!) ---
questions = [
    {
        "topic": "Physics",
        "q": "מה קורה לריכוז $n_i$ כאשר הטמפרטורה $T$ עולה?",
        "opts": ["1. גדל אקספוננציאלית", "2. קטן ליניארית", "3. נשאר קבוע"],
        "ans": 0,
        "explain": "לפי נוסחה (17), הריכוז האינטרינזי תלוי בטמפרטורה בצורה חזקה מאוד."
    },
    {
        "topic": "PN Junction",
        "q": "בצומת PN בממתח Reverse, מה קורה לרוחב אזור המחסור $W$?",
        "opts": ["1. הוא קטן", "2. הוא גדל", "3. הוא לא משתנה"],
        "ans": 1,
        "explain": "נוסחה (28): המתח האחורי מגדיל את הפוטנציאל הכולל ולכן ה-W גדל."
    },
    {
        "topic": "MOS",
        "q": "מהו מתח הסף $V_T$ כאשר מגדילים את עובי האוקסיד $t_{ox}$?",
        "opts": ["1. גדל", "2. קטן", "3. נשאר קבוע"],
        "ans": 0,
        "explain": "נוסחה (64): הגדלת $t_{ox}$ מקטינה את $C_{ox}$, מה שמעלה את מתח הסף."
    }
]

# --- ממשק המשתמש ---
st.title("🎓 מאסטר מל''מ - אריאל")

tab1, tab2 = st.tabs(["תרגול שאלות", "מחשבון הנדסי"])

with tab1:
    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = questions[st.session_state.idx]
    
    st.subheader(f"נושא: {curr['topic']}")
    st.write(f"### {curr['q']}")
    
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    if st.button("בדוק תשובה"):
        if curr['opts'].index(ans) == curr['ans']:
            st.balloons()
            st.success("✅ נכון מאוד!")
        else:
            st.error(f"❌ טעות. הסבר: {curr['explain']}")

    if st.button("שאלה הבאה"):
        st.session_state.idx = (st.session_state.idx + 1) % len(questions)
        st.rerun()

with tab2:
    st.header("מחשבון מהיר")
    na = st.number_input("Na [cm^-3]", value=1e16, format="%.1e")
    vbi = 0.026 * np.log((na * 1e16) / 1.4e10**2)
    st.write(f"פוטנציאל מגע: $V_{{bi}} = {vbi:.3f}$ V")

    # גרף
    fig, ax = plt.subplots(figsize=(6,3))
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.exp(-x/2))
    ax.set_title(heb_graph("דעיכת נושאי מטען"))
    st.pyplot(fig)
