import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- פונקציית קסם לעברית מושלמת בממשק ---
def rtl(text):
    # עוטף את הטקסט ב-HTML שפוקד על הצמדה לימין וכיווניות RTL
    st.markdown(f'<div dir="rtl" style="text-align: right;">{text}</div>', unsafe_allow_html=True)

# --- פונקציה לגרפים בלבד ---
def heb_graph(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# הגדרות דף
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- מאגר שאלות עם שילוב אנגלית ---
questions = [
    {
        "q": "מה קורה לריכוז $n_i$ כאשר הטמפרטורה $T$ עולה?",
        "opts": ["1. גדל אקספוננציאלית", "2. קטן ליניארית", "3. נשאר קבוע"],
        "ans": 0,
        "explain": "לפי נוסחה (17), הריכוז האינטרינזי תלוי בטמפרטורה בצורה חזקה מאוד."
    },
    {
        "q": "בצומת PN בממתח Reverse, מה קורה לרוחב אזור המחסור $W$?",
        "opts": ["1. הוא קטן", "2. הוא גדל", "3. הוא הופך לאפס"],
        "ans": 1,
        "explain": "מתח אחורי מגדיל את פוטנציאל המחסום ולכן ה-W מתרחב."
    }
]

# תפריט צד
st.sidebar.markdown('<div dir="rtl" style="text-align: right;"><b>תפריט ניווט</b></div>', unsafe_allow_html=True)
mode = st.sidebar.radio("", ["מחשבון פתרונות", "תרגול שאלות"])

if mode == "מחשבון פתרונות":
    rtl("### מחשבון צומת PN")
    col1, col2 = st.columns(2)
    with col1:
        na = st.number_input("Na [cm^-3]", value=1e17, format="%.1e")
        nd = st.number_input("Nd [cm^-3]", value=1e16, format="%.1e")
    
    vbi = 0.026 * np.log((na * nd) / 1.4e10**2)
    
    with col2:
        rtl(f"**פוטנציאל מגע ($V_{{bi}}$):** {vbi:.3f} וולט")

    # גרף
    fig, ax = plt.subplots(figsize=(6,3))
    ax.set_title(heb_graph("פילוג שדה חשמלי בצומת"))
    st.pyplot(fig)
    

elif mode == "תרגול שאלות":
    rtl("### תרגול שאלות למבחן")
    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = questions[st.session_state.idx]
    
    rtl(f"**שאלה:** {curr['q']}")
    ans = st.radio("", curr['opts'])
    
    if st.button("בדוק תשובה"):
        if curr['opts'].index(ans) == curr['ans']:
            st.success("נכון!")
        else:
            rtl(f"טעות. הסבר: {curr['explain']}")
