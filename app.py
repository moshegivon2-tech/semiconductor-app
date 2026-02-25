import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# פונקציה לתיקון עברית (עבור כותרות וגרפים)
def heb(text):
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# --- קבועים פיזיקליים מדף הנוסחאות ---
Q = 1.6e-19
NI_300 = 1.4e10
VT_300 = 0.026
EPS0 = 8.85e-14
EPS_SI = 11.8 * EPS0
EPS_OX = 3.9 * EPS0
K_BOLTZ = 1.38e-23
K_EV = 8.617e-5

# --- פונקציות עזר פיזיקליות ---
def get_ni(T):
    return NI_300 * (T/300)**1.5 * np.exp(-(1.12/(2*K_EV)) * (1/T - 1/300))

# --- מאגר שאלות מורחב מהקבצים ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"topic": "Physics", "q": "מאירים חצי דגם סיליקון N ארוך. מה נכון לגבי החלק החשוך?", "opts": ["א. ריכוז אלקטרונים קבוע", "ב. ריכוז חורים קבוע", "ג. השדה החשמלי מקסימלי"], "ans": 0, "explain": "נוסחה 12: בהזרקה חלשה הרוב לא משתנה משמעותית."},
        {"topic": "Illumination", "q": "בוצעו שני ניסויים: בראשון הארה בעוצמה P ובשני 2P. מה המרחק הממוצע L שחודר המטען?", "opts": ["א. שווה בשניהם", "ב. כפול בשני", "ג. גדול פי שורש 2 בשני"], "ans": 0, "explain": "L = sqrt(D*tau). זו תכונת חומר, לא תלויה בעוצמת האור."},
        {"topic": "PN Junction", "q": "מה קורה ל-Vbi אם נעלה טמפרטורה?", "opts": ["א. גדל", "ב. קטן", "ג. לא משתנה"], "ans": 1, "explain": "ni גדל אקספוננציאלית בתוך הלוגריתם, מה שמוריד את Vbi."},
        {"topic": "MOS", "q": "מהו פוטנציאל השפה בסף אינברסיה חזקה?", "opts": ["א. phi_f", "ב. 2*phi_f", "ג. 0"], "ans": 1, "explain": "נוסחה 63: תנאי הסף הוא phi_s = 2*phi_f."},
        {"topic": "BJT", "q": "בטרנזיסטור PNP, מה תפקיד צומת CB בפעיל קדמי?", "opts": ["א. הזרקת חורים", "ב. איסוף חורים", "ג. יצירת אלקטרונים"], "ans": 1, "explain": "השדה החזק במחסור CB 'אוסף' את החורים שמגיעים מהאמיטר."},
    ]

# --- ממשק משתמש - תפריט צד ---
st.sidebar.title(heb("מעבדת המל''מ - אריאל"))
mode = st.sidebar.selectbox(heb("בחר מודול:"), [
    heb("טיפים למבחן (מוקשים)"),
    heb("מחשבון PN Junction"),
    heb("מחשבון MOS Capacitor"),
    heb("מחשבון BJT - אברס מול"),
    heb("מעבדת טמפרטורה ואות קטן"),
    heb("מבחן תרגול 100")
])

# --- מודול 0: טיפים למבחן ---
if mode == heb("טיפים למבחן (מוקשים)"):
    st.header(heb("צ'ק-ליסט למבחן: איפה כולם נופלים?"))
    st.write(heb("ריכוז המוקשים של פרופ' שחם:"))
    
    with st.expander(heb("יחידות מידה - המלכודת הכי גדולה")):
        st.error(heb("חובה להפוך nm ל-cm!"))
        st.latex(r"t_{ox}[cm] = t_{ox}[nm] \cdot 10^{-7}")
        st.write(heb("בלי ההמרה הזו, כל ה-Vt וה-Cox ייצאו לא הגיוניים."))

    with st.expander(heb("דיודה קצרה מול ארוכה")):
        st.info(heb("אם W << L בשאלה - זו דיודה קצרה! השתמשו בנוסחה 40."))

# --- מודול 1: PN Junction ---
elif mode == heb("מחשבון PN Junction"):
    st.header(heb("מחשבון צומת PN"))
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

    # גרף שדה
    fig, ax = plt.subplots(figsize=(6,3))
    x_pn = np.array([-1, 0, 1]); e_pn = np.array([0, -emax, 0])
    ax.plot(x_pn, e_pn, 'r'); ax.set_title(heb("פילוג שדה חשמלי")); st.pyplot(fig)
    

# --- מודול 2: MOS ---
elif mode == heb("מחשבון MOS Capacitor"):
    st.header(heb("מחשבון קבל MOS"))
    col1, col2 = st.columns(2)
    with col1:
        na_m = st.number_input("Na [cm^-3]", value=1e16, format="%.1e")
        tox = st.number_input("tox [nm]", value=20.0)
    
    phi_f = VT_300 * np.log(na_m / NI_300)
    cox = EPS_OX / (tox * 1e-7)
    vt = 2*phi_f + (np.sqrt(2*EPS_SI*Q*na_m*2*phi_f)/cox)

    with col2:
        st.metric(heb("מתח סף (Vt)"), f"{vt:.3f} V")
        st.write(f"Cox = {cox*1e9:.2f} nF/cm^2")

    # גרף C-V איכותי
    v_axis = np.linspace(-2, 2, 100)
    c_axis = np.where(v_axis < 0, 1, np.where(v_axis < vt, 0.4 + 0.6*(1-v_axis/vt), 0.4))
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(v_axis, c_axis, 'g'); ax.set_title(heb("אופיין C-V (תדר גבוה)")); st.pyplot(fig)
    

# --- מודול 3: BJT ---
elif mode == heb("מחשבון BJT - אברס מול"):
    st.header(heb("מודל אברס-מול (BJT)"))
    veb = st.slider("Veb [V]", -1.0, 1.0, 0.7)
    vcb = st.slider("Vcb [V]", -5.0, 1.0, -2.0)
    ies = 1e-14; ics = 2e-14; af = 0.99; ar = 0.5
    
    ie = ies*(np.exp(veb/0.026)-1) - ar*ics*(np.exp(vcb/0.026)-1)
    ic = af*ies*(np.exp(veb/0.026)-1) - ics*(np.exp(vcb/0.026)-1)
    
    st.subheader(heb("זרמים:"))
    st.write(f"Ie = {ie:.3e} A | Ic = {ic:.3e} A")
    

# --- מודול 4: טמפרטורה ואות קטן ---
elif mode == heb("מעבדת טמפרטורה ואות קטן"):
    st.header(heb("השפעות טמפרטורה ואות קטן"))
    temp = st.slider(heb("טמפרטורה [K]"), 200, 600, 300)
    ni_t = get_ni(temp)
    st.metric("ni(T)", f"{ni_t:.2e} cm^-3")
    
    st.divider()
    idc = st.number_input(heb("זרם DC [mA]"), value=1.0) * 1e-3
    rd = 0.026 / idc
    st.metric(heb("התנגדות דיפרנציאלית (rd)"), f"{rd:.2f} Ohm")

# --- מודול 5: מבחן תרגול ---
elif mode == heb("מבחן תרגול 100"):
    st.header(heb("תרגול שאלות ממבחני שחם"))
    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]
    
    st.subheader(heb(curr["q"]))
    choice = st.radio(heb("בחר תשובה:"), curr["opts"])
    
    if st.button(heb("בדוק")):
        if curr["opts"].index(choice) == curr["ans"]:
            st.balloons(); st.success(heb("נכון מאוד!"))
        else:
            st.error(heb("טעות. ") + heb(curr["explain"]))
    
    if st.button(heb("שאלה הבאה")):
        st.session_state.idx += 1; st.rerun()
