import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- פונקציה לתיקון עברית בגרפים בלבד ---
def heb(text):
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# הגדרות דף
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# קבועים
Q = 1.6e-19
VT_300 = 0.026
NI_300 = 1.4e10
EPS_SI = 11.8 * 8.85e-14
EPS_OX = 3.9 * 8.85e-14

# --- ממשק המשתמש (בלי פונקציית heb!) ---
st.sidebar.title("מעבדת המל''מ - אריאל")
mode = st.sidebar.selectbox("בחר מודול:", [
    "מחשבון PN Junction",
    "מחשבון MOS Capacitor",
    "מבחן תרגול"
])

if mode == "מחשבון PN Junction":
    st.header("מחשבון צומת PN")
    col1, col2 = st.columns(2)
    with col1:
        na = st.number_input("Na [cm^-3]", value=1e17, format="%.1e")
        nd = st.number_input("Nd [cm^-3]", value=1e16, format="%.1e")
    
    vbi = VT_300 * np.log((na * nd) / NI_300**2)
    w = np.sqrt((2*EPS_SI/Q)*(1/na + 1/nd)*vbi)
    emax = (Q*nd*(w*na/(na+nd))) / EPS_SI

    with col2:
        st.success(f"Vbi = {vbi:.3f} V")
        st.success(f"W = {w*1e4:.3f} um")
        st.success(f"Emax = {emax:.2e} V/cm")

    # גרף שדה - כאן חייבים להשתמש ב-heb לכותרות!
    fig, ax = plt.subplots(figsize=(6,3))
    x_pn = np.array([-1, 0, 1]); e_pn = np.array([0, -emax, 0])
    ax.plot(x_pn, e_pn, 'r')
    ax.set_title(heb("פילוג שדה חשמלי בצומת"))
    ax.set_xlabel(heb("מרחק"))
    st.pyplot(fig)
    

elif mode == "מחשבון MOS Capacitor":
    st.header("מחשבון קבל MOS")
    na_m = st.number_input("Na [cm^-3]", value=1e16, format="%.1e")
    tox = st.number_input("tox [nm]", value=20.0)
    
    phi_f = VT_300 * np.log(na_m / NI_300)
    cox = EPS_OX / (tox * 1e-7)
    vt = 2*phi_f + (np.sqrt(2*EPS_SI*Q*na_m*2*phi_f)/cox)
    
    st.metric("מתח סף (Vt)", f"{vt:.3f} V")
    

elif mode == "מבחן תרגול":
    st.header("תרגול שאלות")
    st.write("שאלה: מה קורה ל-Vbi כשהטמפרטורה עולה?")
    choice = st.radio("בחר תשובה:", ["גדל", "קטן", "לא משתנה"])
    if st.button("בדוק"):
        if choice == "קטן":
            st.success("נכון!")
        else:
            st.error("טעות, נסה שוב.")
