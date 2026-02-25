import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# הגדרות דף
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# CSS לתיקון RTL ותצוגה
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .katex { direction: ltr !important; display: inline-block !important; }
    .q-card { background-color: white; padding: 20px; border-radius: 10px; border-right: 5px solid #004a99; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 סימולטור מל''מ אריאל")

# כאן מגיע שאר הקוד של השאלות והמחשבונים שנתתי לך קודם...
# וודא שאין כאן טקסט חופשי או אימוג'ים שלא בתוך גרשיים
