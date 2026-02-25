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

# --- CSS חזק לתיקון התצוגה - מונע את הבלגן במספרים ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #f8f9fa; }
    /* עיצוב תיבת השאלה כדי שהנוסחאות לא יקפצו */
    .question-container {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-right: 6px solid #1e3a8a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        line-height: 1.8;
    }
    /* הכרחת נוסחאות להישאר משמאל לימין */
    .katex { direction: ltr !important; display: inline-block !important; font-size: 1.15em !important; }
    div[role="radiogroup"] label { direction: rtl; text-align: right; display: block; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מלא ומדויק מהקבצים שלך ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # שאלה חישובית מהתמונה (image_053200.png)
        {"topic": "Physics", "type": "ni", "q": "נתונה פיסת סיליקון בשיווי משקל בה סיגים נוטלים ($N_a$) בריכוז $10^{17} \\text{ cm}^{-3}$ ותורמים ($N_d$) בריכוז $9 \\cdot 10^{16} \\text{ cm}^{-3}$, וריכוז אינטרינזי ($n_i$) של $10^{17} \\text{ cm}^{-3}$. מהו ריכוז האלקטרונים ($n$)? ", 
         "opts": ["(1) $9.5 \\cdot 10^{16} \\text{ cm}^{-3}$", "(2) $9 \\cdot 10^{16} \\text{ cm}^{-3}$", "(3) $10^{16} \\text{ cm}^{-3}$", "(4) $10^3 \\text{ cm}^{-3}$", "(5) $2 \\cdot 10^3 \\text{ cm}^{-3}$"], 
         "ans": 0, "explain": "בגלל ש-$n_i$ גבוה, משתמשים במשוואה הריבועית: $n^2 + (N_a - N_d)n - n_i^2 = 0$. הצבת הנתונים נותנת בדיוק $9.5 \\cdot 10^{16}$."},
        
        # שאלת הארה (מקבץ שאלות עמ' 1) [cite: 1-5]
        {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג $N$ ארוך בהזרקה חלשה. כתוצאה: [cite: 1-5]", 
         "opts": ["(1) ריכוז עודף האלק' גדול מריכוז עודף החורים בכל ההתקן.", "(2) ריכוז עודף האלק' גדול מריכוז עודף החורים במואר בלבד.", "(3) ריכוז עודף האלק' גדול מריכוז עודף החורים בחשוך בלבד.", "(4) ריכוז עודף האלק' גדול בחלק המואר מריכוזם בחלק החשוך.", "(5) ריכוז האלק' קבוע בחלק החשוך."], 
         "ans": 3, "explain": "ריכוז העודף מקסימלי באזור המואר ודועך אקספוננציאלית לתוך האזור החשוך."},

        # שאלת זרם דיודה [cite: 6-9]
        {"topic": "PN Junction", "type": "iv", "q": "הזרם בדיודת צומת $PN$ הוא תמיד: [cite: 6-9]", 
         "opts": ["(1) בכיוון מנוגד למתח הכולל.", "(2) תלוי אקספוננציאלית בממתח החיצוני.", "(3) סכום זרם סחיפה של אלק' ודיפוזיה של חורים.", "(4) סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים.", "(5) זרם סחיפה בממתח אחורי ודיפוזיה בממתח קידמי."], 
         "ans": 4, "explain": "זהו התיאור הפיזיקלי המדויק של מנגנוני הזרם הדומיננטיים."},

        # שאלת BJT [cite: 15-19]
        {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור ביפולרי נדרש כי: [cite: 15-19]", 
         "opts": ["(1) צומת בסיס-קולקטור יהיה בממתח אחורי.", "(2) רוחב הבסיס קטן ממרחק הדיפוזיה.", "(3) זרם הבסיס קטן מזרם הקולקטור.", "(4) רוחב הבסיס קטן מרוחב המחסור ב-BC.", "(5) רוחב הבסיס קטן מרוחב המחסור ב-BE."], 
         "ans": 1, "explain": "התנאי $W \\ll L$ קריטי כדי שהמטענים יגיעו לקולקטור ללא ריקומבינציה."},

        # שאלת NMOS שגוי [cite: 44-46]
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS, איזה מהמשפטים תמיד שגוי? [cite: 44-46]", 
         "opts": ["(6) מתח השפך אף פעם לא קטן ממתח המקור.", "(7) אם הטרנ' לא קטוע הזרם גדל עם $V_{GS}$.", "(8) הזרם גדל עם עליית $V_{DS}$.", "(9) מטען האינברסיה ליד השפך גדול מליד המקור.", "(10) הזרם גדל ריבועית עם מתח השער."], 
         "ans": 3, "explain": "בגלל מפל המתח, ריכוז המטענים ליד המקור תמיד גדול יותר מאשר ליד השפך."}
    ]

# --- לוגיקה של האפליקציה ---
st.title("🎓 " + "סימולטור מל''מ אריאל - גרסה מתוקנת")

if 'idx' not in st.session_state: st.session_state.idx = 0
curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.6, 1])

with col1:
    # הצגת השאלה בתוך תיבה מעוצבת למניעת בלגן
    st.markdown(f"""
    <div class="question-container">
        <p style='color: #1e3a8a; font-weight: bold;'>שאלה {st.session_state.idx + 1} | נושא: {heb(curr['topic'])}</p>
        <p style='font-size: 1.2em;'>{curr['q']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    ans = st.radio("בחר את התשובה הנכונה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    col_btns = st.columns(2)
    with col_btns[0]:
        if st.button("בדוק תשובה ✅"):
            if curr['opts'].index(ans) == curr['ans']:
                st.success("נכון מאוד! " + curr['explain']); st.balloons()
            else: st.error("טעות. הסבר: " + curr['explain'])
    with col_btns[1]:
        if st.button("שאלה הבאה ➡️"):
            st.session_state.idx += 1; st.rerun()

with col2:
    st.write("### המחשה פיזיקלית")
    fig, ax = plt.subplots(figsize=(5, 4))
    t_type = curr.get("type", "none")
    
    if t_type == "decay":
        x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue', lw=2)
        ax.set_title(heb("דעיכת נושאי מטען"));     elif t_type == "ni":
        temp = np.linspace(250, 600, 100); ni = 1e10 * (temp/300)**3 * np.exp(-1.12/(2*8.6e-5*temp))
        ax.semilogy(temp, ni, color='orange'); ax.set_title(heb("ריכוז ni מול טמפרטורה"));     elif t_type == "bjt":
        ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3))
        ax.text(0.2, 0.5, "E"); ax.text(0.35, 0.5, "B"); ax.text(0.6, 0.5, "C"); ax.axis('off');     elif t_type == "cv":
        v = np.linspace(-3, 3, 100); c = np.where(v < 0, 1, 0.4)
        ax.plot(v, c, 'g', lw=2); ax.set_title(heb("אופיין קיבול-מתח"));     
    st.pyplot(fig)

st.divider()
st.caption("מבוסס על מקבצי השאלות הרשמיים של אריאל [cite: 1-603].")
