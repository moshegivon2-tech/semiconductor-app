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

# --- CSS לתיקון RTL ושמירה על סדר האנגלית/LaTeX ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #f8f9fa; }
    .stMarkdown p, .stMarkdown span { direction: rtl; display: block; }
    .katex { direction: ltr !important; display: inline-block !important; font-size: 1.1em; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    label { direction: rtl; text-align: right; display: block; font-size: 1rem; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מלא מהקבצים שלך  ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # --- פרק 1: פיזיקה והארה ---
        {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג $N$ ארוך בהזרקה חלשה. כתוצאה: [cite: 1]", 
         "opts": ["(1) ריכוז עודף האלק' גדול מריכוז עודף החורים בכל ההתקן.", "(2) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק המואר בלבד.", "(3) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק החשוך בלבד.", "(4) ריכוז עודף האלק' גדול בחלק המואר מריכוזם בחלק החשוך.", "(5) ריכוז האלק' קבוע בחלק החשוך."], 
         "ans": 3, "explain": "הארה יוצרת מטענים עודפים באזור המואר, וריכוזם דועך אקספוננציאלית ככל שמתרחקים לאזור החשוך [cite: 1-5]."},

        {"topic": "Physics", "type": "decay", "q": "בניסוי עם עוצמת הארה $P$ ובניסוי עם $4P$, המרחק הממוצע $L$ שחודר עודף המטען בחושך הינו: [cite: 100]", 
         "opts": ["(1) שווה בשני הניסויים.", "(2) כפול בניסוי השני.", "(3) פי ארבעה בניסוי השני.", "(4) גדול פי $4 \\ln$ בניסוי השני.", "(5) גדול פי $e^4$ בניסוי השני."], 
         "ans": 0, "explain": "מרחק הדיפוזיה $L = \\sqrt{D \\tau}$ הוא תכונת חומר ואינו תלוי בעוצמת ההארה [cite: 107-110]."},

        # --- פרק 2: צומת PN ודיודות ---
        {"topic": "PN Junction", "type": "iv", "q": "הזרם בדיודת צומת $PN$ הוא תמיד: [cite: 6]", 
         "opts": ["(1) בכיוון מנוגד למתח הכולל.", "(2) תלוי אקספוננציאלית בממתח החיצוני.", "(3) סכום זרם סחיפה של אלק' ודיפוזיה של חורים.", "(4) סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים.", "(5) זרם סחיפה בממתח אחורי ודיפוזיה בממתח קידמי."], 
         "ans": 4, "explain": "זהו התיאור הפיזיקלי המדויק של המנגנונים הדומיננטיים בממתח אחורי וקדמי [cite: 6-9]."},

        {"topic": "PN Junction", "type": "field", "q": "בדיודת צומת בממתח קדמי, איזה משפט שגוי תמיד? [cite: 41]", 
         "opts": ["(1) המתח הכולל קטן מהמתח המובנה.", "(2) הזרם בממתח אחורי גדל עם המתח.", "(3) הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה.", "(4) השדה המקסימלי בצומת המטלורגי.", "(5) המתח המובנה נופל בעיקר על הצד הפחות מסומם."], 
         "ans": 2, "explain": "בדיודה קצרה הגרדיאנט חד יותר, לכן הזרם תמיד גדול יותר מאשר בדיודה ארוכה [cite: 41-43]."},

        # --- פרק 3: חישובים מספריים ---
        {"topic": "Physics", "type": "ni", "q": "נתונה פיסת סיליקון בשיווי משקל: $N_a=10^{17}, N_d=9 \\cdot 10^{16}, n_i=10^{17} \\text{ cm}^{-3}$. מהו ריכוז האלקטרונים $n$? [cite: 112]", 
         "opts": ["(1) $9.5 \\cdot 10^{16} \\text{ cm}^{-3}$", "(2) $9 \\cdot 10^{16} \\text{ cm}^{-3}$", "(3) $10^{16} \\text{ cm}^{-3}$", "(4) $10^3 \\text{ cm}^{-3}$", "(5) $2 \\cdot 10^3 \\text{ cm}^{-3}$"], 
         "ans": 0, "explain": "נשתמש במשוואה הריבועית: $n^2 + (N_a-N_d)n - n_i^2 = 0$. פתרון המשוואה עבור הנתונים נותן $9.5 \\cdot 10^{16}$ [cite: 112-118]."},

        # --- פרק 4: טרנזיסטורים ---
        {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור ביפולרי PNP עם $\\gamma=0.8, b=0.9$ במצב פעיל קדמי ו-$I_E=10mA$. מהו זרם הבסיס $I_B$? [cite: 135]", 
         "opts": ["(1) $8 mA$", "(2) $9 mA$", "(3) $1 mA$", "(4) $2 mA$", "(5) $2.8 mA$"], 
         "ans": 4, "explain": "$\\alpha = 0.8 \\times 0.9 = 0.72$. לכן $I_C = 7.2mA$ וזרם הבסיס הוא $10 - 7.2 = 2.8mA$ [cite: 147-152]."},

        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS איזה מהמשפטים תמיד שגוי? [cite: 44]", 
         "opts": ["(1) מתח השפך אף פעם לא קטן ממתח המקור.", "(2) אם הטרנ' אינו קטוע הזרם גדל עם $V_{GS}$.", "(3) הזרם גדל עם עליית $V_{DS}$.", "(4) מטען האינברסיה ליד השפך גדול מאשר ליד המקור.", "(5) הזרם גדל ריבועית עם מתח השער."], 
         "ans": 3, "explain": "מטען האינברסיה קטן ככל שמתקרבים לשפך בגלל מפל המתח לאורך התעלה [cite: 44-46]."}
    ]

# --- לוגיקה של האפליקציה ---
st.title("🎓 " + "סימולטור מל''מ אריאל")

if 'idx' not in st.session_state:
    st.session_state.idx = 0

curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.6, 1])

with col1:
    st.info(f"שאלה {st.session_state.idx + 1} מתוך {len(st.session_state.questions)}")
    st.markdown(f"### נושא: {heb(curr['topic'])}")
    st.markdown(f"#### {curr['q']}")
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("בדוק תשובה ✅"):
            if curr['opts'].index(ans) == curr['ans']:
                st.success("נכון מאוד! " + curr['explain']); st.balloons()
            else: st.error("טעות. הסבר: " + curr['explain'])
    with c2:
        if st.button("שאלה הבאה ➡️"):
            st.session_state.idx += 1; st.rerun()

with col2:
    st.write("### המחשה פיזיקלית")
    fig, ax = plt.subplots(figsize=(5, 4))
    t_type = curr.get("type", "none")
    
    # --- תיקון שגיאת ה-Indentation (יישור הקוד) ---
    if t_type == "decay":
        x = np.linspace(0, 5, 100)
        ax.plot(x, np.exp(-x), color='blue', lw=2)
        ax.set_title(heb("דעיכת נושאי מטען"))
        
    
    elif t_type == "field":
        x = np.linspace(-2, 2, 100)
        e = np.where(x < 0, 1.5+x, 1.5-3*x)
        e[x > 0.5] = 0; e[x < -1.5] = 0
        ax.fill_between(x, e, color='red', alpha=0.3)
        ax.set_title(heb("פילוג שדה חשמלי בצומת"))
        
        
    elif t_type == "ni":
        t_vals = np.linspace(250, 600, 100)
        ni_vals = 1e10 * (t_vals/300)**3 * np.exp(-1.12/(2*8.6e-5*t_vals))
        ax.semilogy(t_vals, ni_vals, color='orange')
        ax.set_title(heb("ריכוז ni מול טמפרטורה"))
        
        
    elif t_type == "bjt":
        ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3))
        ax.text(0.2, 0.5, "E"); ax.text(0.35, 0.5, "B"); ax.text(0.6, 0.5, "C"); ax.axis('off')
        
        
    elif t_type == "cv":
        v_vals = np.linspace(-3, 3, 100); c_vals = np.where(v_vals < 0, 1, 0.4)
        ax.plot(v_vals, c_vals, 'g', lw=2); ax.set_title(heb("אופיין קיבול-מתח (C-V)"))
        
    
    st.pyplot(fig)

st.divider()
st.caption("מבוסס על מקבצי השאלות הרשמיים .")
