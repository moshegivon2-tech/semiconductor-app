import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Ariel Semiconductor Master", layout="wide")

# פונקציה לתיקון עברית בגרפים
def heb(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- CSS לתיקון RTL ושילוב אנגלית/LaTeX ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #f8f9fa; }
    .stMarkdown p, .stMarkdown span { direction: rtl; display: block; }
    .katex { direction: ltr !important; display: inline-block !important; font-size: 1.1em; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    label { direction: rtl; text-align: right; display: block; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מלא עם 5 תשובות - מתוקן לפי המקבץ  ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # שאלה א' 
        {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג $N$ ארוך בהזרקה חלשה. כתוצאה:", 
         "opts": ["(1) ריכוז עודף האלק' גדול מריכוז עודף החורים בכל ההתקן.", 
                  "(2) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק המואר בלבד.", 
                  "(3) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק החשוך בלבד.", 
                  "(4) ריכוז עודף האלק' גדול בחלק המואר מריכוזם בחלק החשוך.", 
                  "(5) ריכוז האלק' קבוע בחלק החשוך."], 
         "ans": 3, "explain": "בגלל תהליך הגנרציה והדיפוזיה, ריכוז המטענים העודפים תמיד מקסימלי באזור המואר ודועך לתוך האזור החשוך[cite: 5]."},

        # שאלה ב' - מתוקן לפי ההערה שלך 
        {"topic": "PN Junction", "type": "iv", "q": "הזרם בדיודת צומת $PN$ הוא תמיד:", 
         "opts": ["(1) בכיוון מנוגד למתח הכולל.", 
                  "(2) תלוי אקספוננציאלית בממתח החיצוני.", 
                  "(3) סכום זרם סחיפה של אלק' ודיפוזיה של חורים.", 
                  "(4) סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים.", 
                  "(5) זרם סחיפה בממתח אחורי ודיפוזיה בממתח קידמי."], 
         "ans": 4, "explain": "זהו התיאור הפיזיקלי המדויק של מנגנוני הזרם הדומיננטיים בכל סוג ממתח[cite: 9]."},

        # שאלה ג' [cite: 10-14]
        {"topic": "Equilibrium", "type": "ni", "q": "במל''מ סוג $N$ בשיווי משקל, איזה מהמשפטים הבאים תמיד נכון?", 
         "opts": ["(1) ריכוז החורים קבוע בכל החומר.", 
                  "(2) ריכוז האלקטרונים שווה לריכוז הסיגים.", 
                  "(3) ריכוז האלקטרונים תלוי אקספוננציאלית בטמפרטורה.", 
                  "(4) מכפלת ריכוז האלקטרונים בחורים תלויה אקספוננציאלית בטמפרטורה.", 
                  "(5) ריכוז האלקטרונים קבוע בכל החומר."], 
         "ans": 3, "explain": "מכיוון ש-$n \cdot p = n_i^2$, והריכוז האינטרינזי תלוי אקספוננציאלית ב-$T$, גם המכפלה תלויה כך[cite: 14]."},

        # שאלה ד' [cite: 15-19]
        {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור ביפולרי נדרש כי:", 
         "opts": ["(1) צומת בסיס-קולקטור יהיה בממתח אחורי.", 
                  "(2) רוחב הבסיס קטן ממרחק הדיפוזיה.", 
                  "(3) זרם הבסיס קטן מזרם הקולקטור.", 
                  "(4) רוחב הבסיס קטן מרוחב אזור המחסור של צומת בסיס-קולקטור.", 
                  "(5) רוחב הבסיס קטן מרוחב אזור המחסור של צומת בסיס-אמיטר."], 
         "ans": 1, "explain": "כדי להבטיח הולכה יעילה ללא ריקומבינציה משמעותית, הבסיס חייב להיות קצר ממרחק הדיפוזיה $W \ll L$[cite: 17]."},

        # שאלה ה' [cite: 20-24]
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS מעלים את המתח $V_{GS}$. כתוצאה זרם הטרנזיסטור:", 
         "opts": ["(1) גדל עם המתח אלא אם כן הטרנ' ברוויה.", 
                  "(2) גדל לינארית עם המתח תמיד.", 
                  "(3) קבוע כל עוד הוא קטן מ-$V_{DS}$.", 
                  "(4) גדל תמיד עם המתח אם הטרנ' אינו בקטעון.", 
                  "(5) גדל תמיד מתכונתית לריבוע המתח."], 
         "ans": 3, "explain": "הגדלת מתח השער מעבר למתח הסף מגדילה את כמות המטען בתעלה ולכן את הזרם[cite: 23]."},

        # שאלה ו' [cite: 25-27]
        {"topic": "Physics", "type": "decay", "q": "בניסוי עם עוצמת הארה $P$ ו-$2P$, המרחק הממוצע שחודר עודף המטען בחושך הינו:", 
         "opts": ["(6) כפול בניסוי השני.", "(7) שווה בשני הניסויים.", 
                  "(8) גדול פי $\sqrt{2}$ בניסוי השני.", "(9) גדול פי $\ln 2$ בניסוי השני.", 
                  "(10) גדול פי $2e$ בניסוי השני."], 
         "ans": 1, "explain": "מרחק הדיפוזיה $L = \sqrt{D\tau}$ תלוי רק בתכונות החומר ולא בעוצמת האור[cite: 26]."},

        # שאלה י' [cite: 44-46]
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS, איזה מהמשפטים תמיד שגוי:", 
         "opts": ["(6) מתח השפך אף פעם לא קטן ממתח המקור.", 
                  "(7) אם הטרנזיסטור אינו קטוע הזרם ממשיך לגדול עם $V_{GS}$.", 
                  "(8) הזרם גדל עם עליית $V_{DS}$.", 
                  "(9) מטען האינברסיה בקרבת השפך גדול מאשר בקרבת המקור.", 
                  "(10) הזרם גדל מתכונתית לריבוע מתח השער."], 
         "ans": 3, "explain": "מטען האינברסיה דועך ככל שמתקרבים לשפך בגלל מפל המתח לאורך התעלה[cite: 46]."},
    ]

# --- ממשק משתמש ---
st.title("🎓 סימולטור מל''מ - אריאל (מתוקן)")

if 'idx' not in st.session_state: st.session_state.idx = 0
curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.6, 1])

with col1:
    st.info(f"שאלה {st.session_state.idx + 1} מתוך {len(st.session_state.questions)}")
    st.markdown(f"### נושא: {heb(curr['topic'])}")
    st.markdown(f"#### {curr['q']}")
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button("בדוק תשובה ✅"):
            if curr['opts'].index(ans) == curr['ans']:
                st.success("נכון! " + curr['explain']); st.balloons()
            else: st.error("טעות. רמז: " + curr['explain'])
    with btn2:
        if st.button("שאלה הבאה ➡️"):
            st.session_state.idx += 1; st.rerun()

with col2:
    st.write("### המחשה פיזיקלית")
    fig, ax = plt.subplots(figsize=(5, 4))
    t_type = curr.get("type", "none")
    
    if t_type == "decay":
        x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue', lw=2)
        ax.set_title(heb("דעיכת נושאי מטען")); 
    elif t_type == "field":
        x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1.5+x, 1.5-3*x); e[x > 0.5] = 0; e[x < -1.5] = 0
        ax.fill_between(x, e, color='red', alpha=0.3); ax.set_title(heb("פילוג שדה חשמלי")); 
    elif t_type == "cv":
        v = np.linspace(-3, 3, 100); c = np.where(v < 0, 1, 0.4)
        ax.plot(v, c, 'g', lw=2); ax.set_title(heb("אופיין קיבול-מתח")); 
    elif t_type == "ni":
        t = np.linspace(250, 600, 100); ni = 1e10 * (t/300)**3 * np.exp(-1.12/(2*8.6e-5*t))
        ax.semilogy(t, ni, 'orange'); ax.set_title(heb("ריכוז ni מול טמפרטורה")); 
    elif t_type == "bjt":
        ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3))
        ax.text(0.2, 0.5, "E"); ax.text(0.35, 0.5, "B"); ax.text(0.6, 0.5, "C"); ax.axis('off'); 
    
    st.pyplot(fig)

st.divider()
st.caption("מבוסס על מקבץ השאלות הרשמי של אריאל .")
