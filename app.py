import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Ariel Semiconductor Master", layout="wide")

# פונקציה לתיקון עברית בגרפים בלבד
def heb(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- CSS מעודכן - שומר על ה-RTL בלי לשבור את הנוסחאות ---
st.markdown("""
    <style>
    /* הגדרת כיווניות כללית לאתר */
    .main {
        direction: rtl;
        text-align: right;
    }
    /* תיקון ספציפי לכפתורי בחירה (Radio) */
    div[role="radiogroup"] {
        direction: rtl;
        text-align: right;
    }
    /* שמירה על נוסחאות אנגליות משמאל לימין */
    .katex {
        direction: ltr !important;
        display: inline-block !important;
    }
    /* תיקון לכותרות שיהיו בימין */
    h1, h2, h3, h4 {
        text-align: right;
        direction: rtl;
    }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מהקבצים שלך  ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג N ארוך בהזרקה חלשה. מה נכון לגבי החלק החשוך? [cite: 1, 5]", "opts": ["א. ריכוז האלקטרונים קבוע", "ב. ריכוז עודף האלקטרונים גדול מעודף החורים", "ג. ריכוז החורים קבוע"], "ans": 0, "explain": "במוליך למחצה מסוג N בהזרקה חלשה, ריכוז האלקטרונים בחלק החשוך נשאר קבוע בקירוב[cite: 5]."},
        {"topic": "PN Junction", "type": "field", "q": "הזרם בדיודת צומת PN הוא תמיד: [cite: 6, 9]", "opts": ["א. סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים", "ב. תלוי אקספוננציאלית בממתח החיצוני", "ג. בכיוון מנוגד למתח"], "ans": 0, "explain": "הזרם הכולל הוא סכום זרמי הסחיפה והדיפוזיה של שני סוגי המובילים[cite: 8, 9]."},
        {"topic": "Diffusion", "type": "decay", "q": "מה קורה למרחק הדיפוזיה $L_p$ אם נקטין את זמן החיים $\\tau_p$? [cite: 26]", "opts": ["א. הוא יגדל", "ב. הוא יקטן", "ג. לא ישתנה"], "ans": 1, "explain": "לפי נוסחה (7), מרחק הדיפוזיה תלוי בשורש זמן החיים: $L_p = \\sqrt{D_p \\tau_p}$[cite: 26, 27]."},
        {"topic": "MOS", "type": "cv", "q": "נתון NMOS. כיצד ישתנה מתח הסף $V_T$ אם נגדיל את ריכוז הסימום $N_A$ במצע? [cite: 91, 95]", "opts": ["א. לא ישתנה", "ב. יקטן", "ג. יגדל"], "ans": 2, "explain": "הגדלת סימום המצע מגדילה את מטען המחסור המקסימלי ולכן מעלה את מתח הסף $V_T$[cite: 92, 95]."},
        {"topic": "BJT", "type": "bjt", "q": "מה מהבאים שגוי עבור טרנזיסטור PNP בתחום פעיל קדמי? [cite: 47, 49]", "opts": ["א. רוחב הבסיס $W$ קטן בהרבה ממרחק הדיפוזיה", "ב. יש להגביר את הריקומבינציה בבסיס", "ג. רוב זרם החורים מהאמיטר מגיע לקולקטור"], "ans": 1, "explain": "הגדלת הריקומבינציה בבסיס פוגעת ביעילות הטרנזיסטור ולכן זהו משפט שגוי[cite: 49]."},
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS, איזה משפט תמיד שגוי? [cite: 44, 46]", "opts": ["א. מטען האינברסיה ליד השפך (Drain) גדול מאשר ליד המקור", "ב. הזרם גדל עם עליית $V_{GS}$", "ג. מתח השפך אף פעם לא קטן ממתח המקור"], "ans": 0, "explain": "בשל מפל המתח לאורך התעלה, ריכוז המטענים ליד המקור תמיד גדול יותר[cite: 46]."}
    ]

# --- ממשק משתמש ---
st.title("🎓 " + "סימולטור מל''מ אריאל")

if 'idx' not in st.session_state: st.session_state.idx = 0
curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.5, 1])

with col1:
    st.info(f"שאלה {st.session_state.idx + 1} מתוך {len(st.session_state.questions)}")
    st.markdown(f"### נושא: {curr['topic']}")
    st.markdown(f"#### {curr['q']}")
    
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    if st.button("בדוק תשובה ✅"):
        if curr['opts'].index(ans) == curr['ans']:
            st.success("נכון מאוד! " + curr['explain'])
            st.balloons()
        else:
            st.error("טעות. הסבר: " + curr['explain'])
            
    if st.button("שאלה הבאה ➡️"):
        st.session_state.idx += 1
        st.rerun()

with col2:
    st.write("### המחשה פיזיקלית")
    fig, ax = plt.subplots(figsize=(5, 4))
    
    if curr['type'] == "ni":
        t = np.linspace(250, 600, 100); ni = 1e10 * (t/300)**3 * np.exp(-1.12/(2*8.6e-5*t))
        ax.semilogy(t, ni, color='#1e3a8a'); ax.set_title(heb("ריכוז אינטרינזי מול טמפרטורה"))
    elif curr['type'] == "field":
        x = np.linspace(-2, 2, 100); e = np.where(x < 0, 2+x, 2-2*x); e[x > 1] = 0; e[x < -2] = 0
        ax.fill_between(x, e, color='red', alpha=0.2); ax.plot(x, e, 'r'); ax.set_title(heb("שדה חשמלי בצומת"))
    elif curr['type'] == "cv":
        v = np.linspace(-3, 3, 100); c = np.where(v < 0, 1, 0.4)
        ax.plot(v, c, color='green', lw=2); ax.set_title(heb("אופיין קיבול-מתח"))
    elif curr['type'] == "decay":
        x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='orange'); ax.set_title(heb("דעיכת מטענים בחושך"))
    elif curr['type'] == "bjt":
        ax.text(0.5, 0.5, heb("אמיטר (E) -> בסיס (B) -> קולקטור (C)"), ha='center'); ax.axis('off')
    
    st.pyplot(fig)

st.divider()
st.caption("מבוסס על מקבץ השאלות הרשמי של אריאל ")
