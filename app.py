import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# פונקציה לתיקון עברית בגרפים
def heb(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- CSS לתיקון RTL ושמירה על סדר האנגלית/LaTeX ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #f8f9fa; }
    .stMarkdown p, .stMarkdown span { direction: rtl; display: block; }
    .katex { direction: ltr !important; display: inline-block !important; font-size: 1.1em; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    label { direction: rtl; text-align: right; display: block; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מורחב ומדויק  ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # שאלה א' - הארה [cite: 1-5]
        {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג $N$ ארוך בהזרקה חלשה. כתוצאה:", 
         "opts": ["(1) ריכוז עודף האלק' גדול מריכוז עודף החורים בכל ההתקן.", 
                  "(2) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק המואר בלבד.", 
                  "(3) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק החשוך בלבד.", 
                  "(4) ריכוז עודף האלק' גדול בחלק המואר מריכוזם בחלק החשוך.", 
                  "(5) ריכוז האלק' קבוע בחלק החשוך."], 
         "ans": 3, "explain": "האור יוצר מטענים עודפים באזור המואר, וריכוזם דועך ככל שמתרחקים לאזור החשוך[cite: 5]."},

        # שאלה ב' - זרם בדיודה 
        {"topic": "PN Junction", "type": "iv", "q": "הזרם בדיודת צומת $PN$ הוא תמיד:", 
         "opts": ["(1) בכיוון מנוגד למתח הכולל.", "(2) תלוי אקספוננציאלית בממתח החיצוני.", 
                  "(3) סכום זרם סחיפה של אלק' ודיפוזיה של חורים.", 
                  "(4) סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים.", 
                  "(5) זרם סחיפה בממתח אחורי ודיפוזיה בממתח קידמי."], 
         "ans": 4, "explain": "זהו התיאור הפיזיקלי המדויק של מנגנוני הזרם בשני המצבים."},

        # שאלה ג' - שיווי משקל סוג N [cite: 10-14]
        {"topic": "Equilibrium", "type": "ni", "q": "במל''מ סוג $N$ בשיווי משקל, איזה מהמשפטים הבאים תמיד נכון?", 
         "opts": ["(1) ריכוז החורים קבוע בכל החומר.", "(2) ריכוז האלקטרונים שווה לריכוז הסיגים.", 
                  "(3) ריכוז האלקטרונים תלוי אקספוננציאלית בטמפרטורה.", 
                  "(4) מכפלת ריכוז האלקטרונים בחורים תלויה אקספוננציאלית בטמפרטורה.", 
                  "(5) ריכוז האלקטרונים קבוע בכל החומר."], 
         "ans": 3, "explain": "מכפלת הריכוזים $n \cdot p = n_i^2$ והיא תלויה בטמפרטורה דרך $E_g$[cite: 14]."},

        # שאלה ז' - צומת PN [cite: 29-34]
        {"topic": "PN Junction", "type": "field", "q": "סמן את המשפט הנכון עבור צומת $PN$ בשיווי-משקל בטמפרטורת החדר:", 
         "opts": ["(6) חורים זורמים מצד $N$ לצד $P$ בדיפוזיה.", "(7) זרם החורים מנטרל בדיוק את זרם האלקטרונים.", 
                  "(8) אין שום זרימה של נושאי מטען (לא סחיפה ולא דיפוזיה).", 
                  "(9) אין זרם סחיפה כי אין שדה חשמלי.", 
                  "(10) אלקטרונים זורמים מצד $N$ לצד $P$ בדיפוזיה."], 
         "ans": 4, "explain": "אלקטרונים נעים בדיפוזיה מהריכוז הגבוה ($N$) אל הנמוך ($P$)[cite: 34]."},

        # שאלה ח' - שיווי משקל סוג P [cite: 35-40]
        {"topic": "Equilibrium", "type": "ni", "q": "במל''מ סוג $P$ בשיווי משקל, איזה מהמשפטים הבאים תמיד נכון?", 
         "opts": ["(6) ריכוז החורים קבוע בכל החומר.", "(7) ריכוז החורים גדול או שווה לריכוז הסיגים.", 
                  "(8) קצב הגנרציה של החורים שווה לקצב הריקומבינציה שלהם.", 
                  "(9) ריכוז החורים תלוי אקספוננציאלית בטמפרטורה.", 
                  "(10) אין דיפוזיה של חורים."], 
         "ans": 2, "explain": "בשיווי משקל תרמי קצב יצירת המטענים שווה לקצב היעלמותם[cite: 38]."},

        # שאלה ט' - שגוי תמיד [cite: 41-43]
        {"topic": "PN Junction", "type": "field", "q": "בדיודת צומת בממתח קדמי, איזה מהמשפטים הבאים שגוי תמיד:", 
         "opts": ["(6) המתח הכולל קטן (בגודלו) מהמתח המובנה.", "(7) הזרם בממתח אחורי גדל (בגודלו) עם המתח.", 
                  "(8) הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה עם אותם ריכוזים.", 
                  "(9) השדה החשמלי מקסימלי בצומת בנקודת הצומת המטלורגי.", 
                  "(10) המתח המובנה נופל בעקרו על הצד בעל ריכוז הסיגים הנמוך."], 
         "ans": 2, "explain": "זה שגוי כי בדיודה קצרה הגרדיאנט חד יותר ולכן הזרם דווקא גדול יותר[cite: 42]."},
    ]

# --- לוגיקה של האפליקציה ---
st.title("🎓 סימולטור מל''מ - אוניברסיטת אריאל")

if 'idx' not in st.session_state: st.session_state.idx = 0
curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.6, 1])

with col1:
    st.info(f"שאלה {st.session_state.idx + 1} מתוך {len(st.session_state.questions)}")
    st.markdown(f"### נושא: {heb(curr['topic'])}")
    st.markdown(f"#### {curr['q']}")
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("בדוק תשובה ✅"):
            if curr['opts'].index(ans) == curr['ans']:
                st.success("נכון מאוד! " + curr['explain']); st.balloons()
            else: st.error("טעות. רמז: " + curr['explain'])
    with col_b2:
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
    elif t_type == "ni":
        t = np.linspace(250, 600, 100); ni = 1e10 * (t/300)**3 * np.exp(-1.12/(2*8.6e-5*t))
        ax.semilogy(t, ni, 'orange'); ax.set_title(heb("ריכוז ni מול טמפרטורה")); 
    elif t_type == "iv":
        v = np.linspace(-1, 0.7, 100); i = 1e-12 * (np.exp(v/0.026)-1)
        ax.plot(v, i, 'red'); ax.set_title(heb("אופיין זרם-מתח (I-V)"))
    
    st.pyplot(fig)

st.divider()
st.caption("מבוסס על מקבץ השאלות הרשמי של אריאל .")
