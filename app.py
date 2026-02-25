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

# --- CSS מתקדם ל-RTL ושילוב אנגלית תקנית ---
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

# --- מאגר שאלות ענק מהקבצים  ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # --- דף 1 ---
        {"topic": "Physics", "type": "decay", "q": "א. בוצעו שני ניסויים של הארת חצי דגם מל''מ, בראשון בעוצמה $P$ ובשני פי ארבעה ($4P$). המרחק הממוצע שחודר עודף המטען בחלק החשוך הינו: [cite: 100-110]", 
         "opts": ["(1) שווה בשני הניסויים.", "(2) כפול בניסוי השני.", "(3) פי ארבעה בניסוי השני.", "(4) גדול פי $4 \ln$ בניסוי השני.", "(5) גדול פי $e^4$ בניסוי השני."], 
         "ans": 0, "explain": "מרחק הדיפוזיה $L = \\sqrt{D \\tau}$ הוא תכונת חומר ואינו תלוי בעוצמת ההארה[cite: 107, 133]."},
        
        {"topic": "Physics", "type": "ni", "q": "ב. נתונה פיסת סיליקון בשיווי משקל: $N_a=10^{17}, N_d=9 \\cdot 10^{16}, n_i=10^{17} [cm^{-3}]$. מהו ריכוז האלקטרונים $n$? [cite: 112-126]", 
         "opts": ["(1) $9.5 \\cdot 10^{16} cm^{-3}$", "(2) $9 \\cdot 10^{16} cm^{-3}$", "(3) $10^{16} cm^{-3}$", "(4) $10^3 cm^{-3}$", "(5) $2 \\cdot 10^3 cm^{-3}$"], 
         "ans": 0, "explain": "נשתמש במשוואה: $n^2 + (N_a-N_d)n - n_i^2 = 0$. הצבת הנתונים נותנת בדיוק את תשובה 1 [cite: 114-118]."},

        {"topic": "PN Junction", "type": "field", "q": "ג. בדיודת צומת, איזה מהמשפטים הבאים שגוי תמיד? [cite: 127-132]", 
         "opts": ["(1) המתח המובנה נופל בעיקרו על הצד בעל ריכוז הסיגים הנמוך.", "(2) השדה המקסימלי בנקודת הצומת המטלורגי.", "(3) הזרם בממתח אחורי גדל (בגודלו) עם המתח.", "(4) הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה.", "(5) המתח הכולל בממתח קדמי קטן מהמתח המובנה."], 
         "ans": 3, "explain": "בדיודה קצרה הגרדיאנט חד יותר, לכן הזרם תמיד גדול יותר מאשר בדיודה ארוכה[cite: 131]."},

        {"topic": "BJT", "type": "bjt", "q": "ד. טרנזיסטור PNP עם $\\gamma=0.8, b=0.9$. במצב פעיל קדמי $I_E=10mA$. מהו זרם הבסיס $I_B$? [cite: 135-146]", 
         "opts": ["(1) $8 mA$", "(2) $9 mA$", "(3) $1 mA$", "(4) $2 mA$", "(5) $2.8 mA$"], 
         "ans": 4, "explain": "$\\alpha = 0.8 \\times 0.9 = 0.72$. לכן $I_C = 7.2mA$ וזרם הבסיס הוא $I_E - I_C = 2.8mA$ [cite: 147-152]."},

        # --- דף 2 ---
        {"topic": "Physics", "type": "ni", "q": "א. בפיסת סיליקון בה $N_d = n_i$, פי כמה גדול ריכוז האלקטרונים מזה של החורים? ", 
         "opts": ["(1) פי ארבעה.", "(2) פי שלושה.", "(3) פי שניים.", "(4) פי 1.5", "(5) פי 2.6"], 
         "ans": 4, "explain": "מפתרון משוואת הניטרליות מקבלים $n \\approx 1.618 n_i$ ו-$p \\approx 0.618 n_i$. היחס ביניהם הוא 2.6[cite: 168, 175]."},

        {"topic": "PN Junction", "type": "iv", "q": "ג. נתונה דיודה ארוכה עם $V_{bi}=0.7V$. מגדילים את הממתח הקדמי מ-0.3V ל-0.6V. התוצאה: [cite: 193-203]", 
         "opts": ["(1) קיבול המחסור וקיבול הדיפוזיה גדלים פי שניים.", "(2) קיבול המחסור קטן פי שניים וקיבול הדיפוזיה גדל פי שניים.", "(3) קיבול המחסור קטן פי $\\sqrt{2}$ וקיבול הדיפוזיה גדל פי שניים.", "(4) קיבול המחסור גדל פי שניים וקיבול הדיפוזיה גדל פי $10^5$.", "(5) קיבול המחסור גדל פי $\\sqrt{2}$ וקיבול הדיפוזיה גדל פי $10^5$."], 
         "ans": 4, "explain": "קיבול הדיפוזיה גדל אקספוננציאלית עם המתח. בשינוי של 0.3V הוא גדל פי $e^{0.3/0.026} \\approx 10^5$."},

        # --- דף 4 ---
        {"topic": "Breakdown", "type": "field", "q": "ד. כאשר מחממים דיודת סיליקון, פריצת מפולת (Avalanche) מתרחשת: [cite: 304-314]", 
         "opts": ["(1) במתח נמוך יותר כי הניידות יורדת.", "(2) במתח נמוך יותר כי רוחב המחסור קטן.", "(3) במתח נמוך יותר כי הריכוז גדל.", "(4) במתח גבוה יותר בגלל העלייה בתנודות התרמיות.", "(5) במתח גבוה יותר בגלל העלייה בזרם הרוויה."], 
         "ans": 3, "explain": "בטמפרטורה גבוהה יש יותר פיזורי סריג, המטענים מאבדים אנרגיה ודרוש מתח גבוה יותר כדי להגיע ליינון."},

        # --- דף 7 ---
        {"topic": "PN Junction", "type": "iv", "q": "ג. בדיודת צומת אידאלית קצרה עם $D_e = 2D_h$ וסיגומים שווים: [cite: 445-451]", 
         "opts": ["(1) זרם האלק' גדול פי 12 מזרם החורים.", "(2) זרם החורים גדול פי 2 מזרם האלק'.", "(3) זרם האלק' כפול מזרם החורים.", "(4) זרם החורים כפול מזרם האלק'.", "(5) זרמי האלק' והחורים שווים."], 
         "ans": 2, "explain": "מכיוון שהזרם פרופורציונלי למקדם הדיפוזיה ($D$), זרם האלקטרונים יהיה כפול [cite: 450-451]."}
    ]

# --- ממשק המשתמש ---
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
    t = curr.get("type", "none")
    if t == "decay":
        x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue'); ax.set_title(heb("דעיכת מטענים"))
        
    elif t == "field":
        x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1+x, 1-2*x); e[x>0.5]=0; e[x<-1]=0
        ax.fill_between(x, e, color='red', alpha=0.3); ax.set_title(heb("שדה חשמלי בצומת"))
        
    elif t == "ni":
        temp = np.linspace(250, 600, 100); ni = 1e10 * (temp/300)**3 * np.exp(-1.12/(2*8.6e-5*temp))
        ax.semilogy(temp, ni, color='orange'); ax.set_title(heb("ריכוז אינטרינזי"))
        
    elif t == "bjt":
        ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3))
        ax.text(0.2, 0.5, "E"); ax.text(0.35, 0.5, "B"); ax.text(0.6, 0.5, "C"); ax.axis('off')
        
    elif t == "cv":
        v = np.linspace(-3, 3, 100); c = np.where(v < 0, 1, 0.4)
        ax.plot(v, c, 'g', lw=2); ax.set_title(heb("אופיין קיבול-מתח"))
        
    st.pyplot(fig)

st.divider()
st.caption("מבוסס על מקבץ השאלות הרשמי של אריאל . בהצלחה!")
