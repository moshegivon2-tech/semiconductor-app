import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- פונקציית תיקון עברית פשוטה לגרפים ---
# אם הטקסט עדיין הפוך, פשוט נוריד את ה-[::-1]
def heb(text):
    if not text: return ""
    return text[::-1] 

# הגדרות דף
st.set_page_config(page_title="Ariel Semi Master", layout="wide")

# CSS להצמדת הממשק לימין
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    [data-testid="stSidebar"] { direction: rtl; text-align: right; }
    .katex { direction: ltr !important; display: inline-block !important; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מורחב ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {
            "topic": "Diffusion",
            "type": "decay",
            "q": "מה קורה למרחק הדיפוזיה $L_p$ אם נקטין את זמן החיים $\\tau_p$?",
            "opts": ["1. יגדל", "2. יקטן", "3. לא ישתנה"],
            "ans": 1,
            "explain": "לפי נוסחה (7): $L_p = \\sqrt{D_p \\tau_p}$. פחות זמן לחיות = פחות מרחק לעבור."
        },
        {
            "topic": "PN Junction",
            "type": "field",
            "q": "היכן השדה החשמלי הוא מקסימלי בצומת PN בשיווי משקל?",
            "opts": ["1. בקצוות אזור המחסור", "2. במטלורגיית הצומת (x=0)", "3. מחוץ לאזור המחסור"],
            "ans": 1,
            "explain": "לפי נוסחה (34), השדה גדל ליניארית בתוך אזור המחסור ומגיע לשיאו במגע בין הצמתים."
        },
        {
            "topic": "Physics",
            "type": "ni",
            "q": "איך משתנה הריכוז האינטרינזי $n_i$ עם עליית הטמפרטורה?",
            "opts": ["1. עולה אקספוננציאלית", "2. יורד ליניארית", "3. לא משתנה"],
            "ans": 0,
            "explain": "נוסחה (17): $n_i$ תלוי חזק בטמפרטורה דרך האקספוננט."
        },
        {
            "topic": "MOS",
            "type": "cv",
            "q": "באיזה תחום עבודה נמצא קבל MOS אם הקיבול שלו הוא $C_{ox}$?",
            "opts": ["1. אקומולציה", "2. מחסור (Depletion)", "3. אינברסיה חזקה"],
            "ans": 0,
            "explain": "באקומולציה מטענים נצמדים לתחמוצת ולכן הקיבול מקסימלי."
        }
    ]

st.title("🎓 סימולטור מל''מ - אוניברסיטת אריאל")

if 'idx' not in st.session_state:
    st.session_state.idx = 0

curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"נושא: {curr['topic']}")
    st.markdown(f"### {curr['q']}")
    
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    if st.button("בדוק תשובה"):
        if curr['opts'].index(ans) == curr['ans']:
            st.success("✅ נכון! " + curr['explain'])
            st.balloons()
        else:
            st.error("❌ טעות. רמז: " + curr['explain'])

    if st.button("שאלה הבאה ➡️"):
        st.session_state.idx += 1
        st.rerun()

with col2:
    st.write("### המחשה גרפית")
    fig, ax = plt.subplots(figsize=(5, 4))
    
    if curr['type'] == "decay":
        x = np.linspace(0, 5, 100)
        ax.plot(x, np.exp(-x), color='blue', lw=2)
        ax.set_title(heb("דעיכת ריכוז המיעוט"))
        ax.set_xlabel(heb("מרחק"))
        
        
    elif curr['type'] == "field":
        x = np.linspace(-2, 2, 100)
        e = np.where(x < 0, 1+x, 1-x)
        e[x > 1] = 0; e[x < -1] = 0
        ax.fill_between(x, e, color='red', alpha=0.3)
        ax.set_title(heb("שדה חשמלי בצומת"))
        

    elif curr['type'] == "ni":
        t = np.linspace(200, 500, 100)
        ni = 1e10 * (t/300)**1.5 * np.exp(-5000*(1/t - 1/300))
        ax.semilogy(t, ni, color='green')
        ax.set_title(heb("ריכוז אינטרינזי מול טמפרטורה"))
        

    elif curr['type'] == "cv":
        v = np.linspace(-2, 2, 100)
        c = np.where(v < 0, 1, 0.4)
        ax.plot(v, c, color='purple', lw=2)
        ax.set_title(heb("אופיין קיבול מתח"))
        

    st.pyplot(fig)

st.divider()
st.info("פותח עבור הסטודנטים באריאל. בהצלחה במבחן!")
