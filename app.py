import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- CSS לתיקון RTL ותצוגה ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #fcfcfc; }
    .katex { direction: ltr !important; display: inline-block !important; }
    .q-card { background-color: white; padding: 25px; border-radius: 15px; border-right: 10px solid #004a99; box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-bottom: 25px; }
    div[role="radiogroup"] label { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 סימולטור מל''מ אריאל - גרסת ה-Master")

# --- מאגר שאלות ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"topic": "Physics", "type": "ni", "q": "מהו ריכוז האלקטרונים בפיסת סיליקון בשיווי משקל? (Na=10^17, Nd=9*10^16, ni=10^17)", 
         "opts": ["9.51e16", "1e16", "1e17", "1.05e17"], "ans": 0, "explain": "שימוש במשוואה הריבועית המלאה."},
        {"topic": "PN Junction", "type": "field", "q": "איזה משפט שגוי עבור דיודת צומת בממתח קדמי?", 
         "opts": ["המתח קטן מ-Vbi", "הזרם באחורי גדל עם המתח", "הזרם בקצרה קטן מאשר בארוכה", "השדה מקסימלי בצומת"], "ans": 2, "explain": "בדיודה קצרה הזרם תמיד גדול יותר."},
    ] # כאן אפשר להוסיף את כל שאר ה-60 שאלות

# --- טאבים ---
t1, t2, t3 = st.tabs(["📝 מבחן", "🧮 מחשבון PN", "📋 דף נוסחאות"])

with t1:
    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]
    st.markdown(f"<div class='q-card'><b>{curr['q']}</b></div>", unsafe_allow_html=True)
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    if st.button("בדוק ✅"):
        if curr['opts'].index(ans) == curr['ans']: st.success("נכון!")
        else: st.error(f"טעות. {curr['explain']}")
    if st.button("הבא ➡️"): st.session_state.idx += 1; st.rerun()

with t2:
    st.subheader("מחשבון $V_{bi}$ ורוחב מחסור")
    na = st.number_input("Na", value=1e17)
    nd = st.number_input("Nd", value=1e16)
    vbi = 0.0259 * np.log((na * nd) / 1e20)
    st.metric("מתח מובנה Vbi", f"{vbi:.3f} V")

with t3:
    st.latex(r"V_{bi} = V_t \ln\left(\frac{N_a N_d}{n_i^2}\right)")
