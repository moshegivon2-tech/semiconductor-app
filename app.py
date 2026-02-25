import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Ariel Semiconductor Master", layout="wide")

# פונקציה לתיקון עברית בגרפים (הופכת את המלל בגרף בלבד)
def heb(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- CSS מתקדם לתיקון RTL ושמירה על סדר האנגלית/LaTeX ---
st.markdown("""
    <style>
    /* הגדרת כיווניות כללית לימין-לשמאל */
    .stApp { 
        direction: rtl; 
        text-align: right; 
        background-color: #f4f7f9; 
    }
    /* שמירה על נוסחאות אנגליות משמאל לימין שלא יתהפכו */
    .katex { 
        direction: ltr !important; 
        display: inline-block !important; 
        font-size: 1.1em; 
        color: #1e3a8a;
    }
    /* תיקון ליישור כפתורי הרדיו (תשובות) */
    div[role="radiogroup"] { 
        direction: rtl; 
        text-align: right; 
    }
    label { 
        direction: rtl; 
        text-align: right; 
        display: block; 
        font-size: 1rem;
    }
    /* כותרות */
    h1, h2, h3, h4 { 
        text-align: right; 
        direction: rtl; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מלא מהקבצים שלך  ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # שאלות הארה ופיזיקה [cite: 1-5, 25-27, 100-110]
        {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג $N$ ארוך בהזרקה חלשה. כתוצאה: [cite: 1-5]", 
         "opts": ["(1) ריכוז עודף האלק' גדול מריכוז עודף החורים בכל ההתקן.", "(2) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק המואר בלבד.", "(3) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק החשוך בלבד.", "(4) ריכוז עודף האלק' גדול בחלק המואר מריכוזם בחלק החשוך.", "(5) ריכוז האלק' קבוע בחלק החשוך."], 
         "ans": 3, "explain": "בשל תהליך הגנרציה והדיפוזיה, ריכוז המטענים העודפים מקסימלי באזור המואר ודועך לתוך האזור החשוך[cite: 5]."},

        # שאלות חישוביות
        {"topic": "Physics", "type": "ni", "q": "נתונה פיסת סיליקון בשיווי משקל: $N_a=10^{17}, N_d=9 \\cdot 10^{16}, n_i=10^{17} \\text{ cm}^{-3}$. מהו ריכוז האלקטרונים $n$? [cite: 116]", 
         "opts": ["(1) $9.5 \\cdot 10^{16} \\text{ cm}^{-3}$", "(2) $9 \\cdot 10^{16} \\text{ cm}^{-3}$", "(3) $10^{16} \\text{ cm}^{-3}$", "(4) $10^3 \\text{ cm}^{-3}$", "(5) $2 \\cdot 10^3 \\text{ cm}^{-3}$"], 
         "ans": 0, "explain": "נשתמש במשוואה הריבועית: $n^2 + (N_a-N_d)n - n_i^2 = 0$. הצבת הנתונים נותנת $9.5 \\cdot 10^{16}$[cite: 117]."},

        # שאלות דיודה וצומת PN [cite: 6-14, 29-34, 41-43, 127-132]
        {"topic": "PN Junction", "type": "iv", "q": "הזרם בדיודת צומת $PN$ הוא תמיד: [cite: 6]", 
         "opts": ["(1) בכיוון מנוגד למתח הכולל.", "(2) תלוי אקספוננציאלית בממתח החיצוני.", "(3) סכום זרם סחיפה של אלק' ודיפוזיה של חורים.", "(4) סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים.", "(5) זרם סחיפה בממתח אחורי ודיפוזיה בממתח קידמי."], 
         "ans": 4, "explain": "זהו התיאור הפיזיקלי המדויק של המנגנונים הדומיננטיים בממתח אחורי וקדמי[cite: 9]."},

        {"topic": "PN Junction", "type": "field", "q": "בדיודת צומת בממתח קדמי, איזה מהמשפטים הבאים שגוי תמיד? [cite: 41, 127]", 
         "opts": ["(1) המתח הכולל קטן מהמתח המובנה.", "(2) הזרם בממתח אחורי גדל עם המתח.", "(3) הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה.", "(4) השדה החשמלי מקסימלי בצומת המטלורגי.", "(5) המתח המובנה נופל בעקרו על הצד הפחות מסומם."], 
         "ans": 2, "explain": "בדיודה קצרה הגרדיאנט חד יותר, לכן הזרם תמיד גדול יותר מאשר בדיודה ארוכה[cite: 42, 131]."},

        # שאלות BJT ו-MOS [cite: 15-24, 44-49, 86-96, 135-160]
        {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור ביפולרי נדרש כי: [cite: 15]", 
         "opts": ["(1) צומת בסיס-קולקטור יהיה בממתח אחורי.", "(2) רוחב הבסיס קטן ממרחק הדיפוזיה.", "(3) זרם הבסיס קטן מזרם הקולקטור.", "(4) רוחב הבסיס קטן מרוחב אזור המחסור של צומת BC.", "(5) רוחב הבסיס קטן מרוחב אזור המחסור של צומת BE."], 
         "ans": 1, "explain": "הדרישה הקריטית היא $W \\ll L$ כדי להבטיח מעבר יעיל של מטענים לקולקטור[cite: 17]."},

        {"topic": "MOSFET", "type": "cv", "q": "בטרנזיסטור NMOS איזה מהמשפטים תמיד שגוי? [cite: 44, 157]", 
         "opts": ["(1) מתח השפך אף פעם לא קטן ממתח המקור.", "(2) אם הטרנזיסטור אינו קטוע הזרם ממשיך לגדול עם $V_{GS}$.", "(3) הזרם גדל עם עליית $V_{DS}$.", "(4) מטען האינברסיה בקרבת השפך גדול מאשר בקרבת המקור.", "(5) הזרם גדל מתכונתית לריבוע מתח השער."], 
         "ans": 3, "explain": "מטען האינברסיה קטן ככל שמתקרבים לשפך בגלל מפל המתח לאורך התעלה[cite: 46, 158]."},
    ]

# --- לוגיקה של האפליקציה ---
st.title("🎓 " + "סימולטור מל''מ אריאל - מאגר שאלות מבחן")

if 'idx' not in st.session_state: st.session_state.idx = 0
curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.6, 1])

with col1:
    st.info(f"שאלה {st.session_state.idx + 1} מתוך {len(st.session_state.questions)}")
    st.markdown(f"### נושא: {heb(curr['topic'])}")
    st.markdown(f"#### {curr['q']}")
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    b1, b2 = st.columns(2)
    with b1:
        if st.button("בדוק תשובה ✅"):
            if curr['opts'].index(ans) == curr['ans']:
                st.success("נכון מאוד! " + curr['explain']); st.balloons()
            else: st.error("טעות. הסבר: " + curr['explain'])
    with b2:
        if st.button("שאלה הבאה ➡️"):
            st.session_state.idx += 1; st.rerun()

with col2:
    st.write("### המחשה פיזיקלית")
    fig, ax = plt.subplots(figsize=(5, 4))
    t_type = curr.get("type", "none")
    
    if t_type == "decay":
        x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue', lw=2)
        ax.set_title(heb("דעיכת נושאי מטען"));     elif t_type == "field":
        x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1.5+x, 1.5-3*x); e[x > 0.5] = 0; e[x < -1.5] = 0
        ax.fill_between(x, e, color='red', alpha=0.3); ax.set_title(heb("פילוג שדה חשמלי"));     elif t_type == "ni":
        t = np.linspace(250, 600, 100); ni = 1e10 * (t/300)**3 * np.exp(-1.12/(2*8.6e-5*t))
        ax.semilogy(t, ni, 'orange'); ax.set_title(heb("ריכוז ni מול טמפרטורה"));     elif t_type == "bjt":
        ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3))
        ax.text(0.2, 0.5, "E"); ax.text(0.35, 0.5, "B"); ax.text(0.6, 0.5, "C"); ax.axis('off');     elif t_type == "cv":
        v = np.linspace(-3, 3, 100); c = np.where(v < 0, 1, 0.4)
        ax.plot(v, c, 'g', lw=2); ax.set_title(heb("אופיין קיבול-מתח"));     
    st.pyplot(fig)

st.divider()
st.caption("מבוסס על מקבץ השאלות הרשמי של אריאל .")
