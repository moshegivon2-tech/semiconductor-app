import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- הזרקת CSS ל-RTL ונוסחאות ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .stMarkdown p, .stMarkdown span { direction: rtl; display: block; }
    .katex { direction: ltr !important; display: inline-block !important; }
    div[role="radiogroup"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

def heb(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- מאגר שאלות ענק עם סוגי סימולציות ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"topic": "Physics", "type": "ni", "q": "איך משתנה ריכוז המובילים האינטרינזי $n_i$ עם עליית הטמפרטורה?", "opts": ["1. עולה אקספוננציאלית", "2. יורד ליניארית", "3. לא משתנה"], "ans": 0, "explain": "נוסחה (17): $n_i$ תלוי ב-$e^{-E_g/2kT}$. שינוי קטן ב-$T$ מקפיץ אותו."},
        {"topic": "PN Junction", "type": "field", "q": "היכן נופל עיקר המתח המובנה $V_{bi}$ בצומת $P^+N$?", "opts": ["1. על הצד המסומם חזק (P)", "2. על הצד המסומם חלש (N)", "3. שווה על שניהם"], "ans": 1, "explain": "נוסחה (31): רוב המחסור והמתח נופלים על הצד הפחות מסומם."},
        {"topic": "Diffusion", "type": "decay", "q": "מה קורה למרחק הדיפוזיה $L_p$ אם נקטין את זמן החיים $\\tau_p$?", "opts": ["1. יגדל", "2. יקטן", "3. יישאר קבוע"], "ans": 1, "explain": "נוסחה (7): $L_p = \\sqrt{D_p \\tau_p}$. פחות זמן לחיות = פחות מרחק לעבור."},
        {"topic": "MOS", "type": "cv", "q": "באיזה תחום עבודה נמצא קבל MOS אם קיבולו שווה ל-$C_{ox}$?", "opts": ["1. אקומולציה", "2. מחסור (Depletion)", "3. אינברסיה חזקה בתדר גבוה"], "ans": 0, "explain": "באקומולציה, מטענים נצמדים לתחמוצת והקיבול הוא המקסימלי."},
        {"topic": "BJT", "type": "bjt", "q": "בתחום 'פעיל קדמי', איך מוטים הצמתים בטרנזיסטור $NPN$?", "opts": ["1. EB קדמי, CB אחורי", "2. שניהם קדמיים", "3. שניהם אחוריים"], "ans": 0, "explain": "זה המצב הקלאסי להגברה - הזרקה מהאמיטר ואיסוף בקולקטור."},
        {"topic": "PN Junction", "type": "iv", "q": "איך משתנה זרם הרוויה $I_0$ אם נגדיל את שטח הצומת פי 2?", "opts": ["1. יקטן פי 2", "2. יגדל פי 2", "3. לא ישתנה"], "ans": 1, "explain": "נוסחה (39): הזרם פרופורציונלי לשטח הצומת $A$."},
    ]

# --- פונקציות לסימולציות גרפיות ---
def plot_simulation(q_type):
    fig, ax = plt.subplots(figsize=(5, 3))
    if q_type == "ni":
        t = np.linspace(200, 500, 100)
        ni = 1e10 * (t/300)**1.5 * np.exp(-5000*(1/t - 1/300))
        ax.semilogy(t, ni, 'r'); ax.set_title(heb("ריכוז $n_i$ מול טמפרטורה"))
    elif q_type == "field":
        x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1+x, 1-x/0.5); e[x > 0.5] = 0; e[x < -1] = 0
        ax.fill_between(x, e, color='blue', alpha=0.3); ax.set_title(heb("פילוג שדה חשמלי $E$"))
    elif q_type == "cv":
        v = np.linspace(-2, 2, 100); c = np.where(v < 0, 1, np.where(v < 1, 1/(1+v), 0.5))
        ax.plot(v, c, 'g'); ax.set_title(heb("עקומת קיבול $C-V$"))
    elif q_type == "decay":
        x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), 'orange'); ax.set_title(heb("דעיכת נושאי מטען בחושך"))
    elif q_type == "iv":
        v = np.linspace(-0.5, 0.7, 100); i = 1e-12 * (np.exp(v/0.026)-1)
        ax.plot(v, i, 'red'); ax.set_ylim(-0.1e-3, 0.5e-3); ax.set_title(heb("אופיין זרם-מתח $I-V$"))
    st.pyplot(fig)

# --- ממשק משתמש ---
st.title("🎓 סימולטור מל''מ - אוניברסיטת אריאל")

if 'idx' not in st.session_state: st.session_state.idx = 0
curr = st.session_state.questions[st.session_state.idx]

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader(f"נושא: {curr['topic']}")
    st.write(f"### {curr['q']}")
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    if st.button("בדוק תשובה"):
        if curr['opts'].index(ans) == curr['ans']:
            st.balloons(); st.success("✅ נכון! " + curr['explain'])
        else:
            st.error("❌ טעות. רמז: " + curr['explain'])

    if st.button("שאלה הבאה ➡️"):
        st.session_state.idx = (st.session_state.idx + 1) % len(st.session_state.questions)
        st.rerun()

with col2:
    st.write("### סימולציה ויזואלית")
    plot_simulation(curr['type'])

st.divider()
st.info("פותח עבור הסטודנטים להנדסת חשמל באריאל. בהצלחה במבחן!")
