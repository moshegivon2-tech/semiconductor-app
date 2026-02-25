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
    .stApp { direction: rtl; text-align: right; background-color: #f8f9fa; }
    .stMarkdown p, .stMarkdown span { direction: rtl; display: block; font-size: 1.1rem; }
    .katex { direction: ltr !important; display: inline-block !important; font-size: 1.2rem; color: #1e3a8a; }
    div[role="radiogroup"] { direction: rtl; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def heb(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- מאגר שאלות מורחב מהקבצים שלך ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג N ארוך בהזרקה חלשה. מה נכון לגבי החלק החשוך?", "opts": ["א. ריכוז האלקטרונים קבוע", "ב. ריכוז עודף האלקטרונים גדול מעודף החורים", "ג. ריכוז החורים קבוע"], "ans": 0, "explain": "במוליך למחצה מסוג N בהזרקה חלשה, ריכוז האלקטרונים בחלק החשוך נשאר קבוע בקירוב[cite: 5]."},
        {"topic": "PN Junction", "type": "field", "q": "הזרם בדיודת צומת PN הוא תמיד:", "opts": ["א. סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים", "ב. תלוי אקספוננציאלית בממתח החיצוני", "ג. בכיוון מנוגד למתח"], "ans": 0, "explain": "הזרם הכולל הוא סכום זרמי הסחיפה והדיפוזיה של שני סוגי המובילים[cite: 9]."},
        {"topic": "Equilibrium", "type": "ni", "q": "במל''מ סוג N בשיווי משקל, מה נכון תמיד?", "opts": ["א. ריכוז האלקטרונים שווה לריכוז הסיגים", "ב. מכפלת ריכוז האלקטרונים בחורים תלויה אקספוננציאלית בטמפרטורה", "ג. ריכוז החורים קבוע בכל החומר"], "ans": 1, "explain": "מכפלת הריכוזים $n \cdot p = n_i^2$ תלויה אקספוננציאלית בטמפרטורה[cite: 14]."},
        {"topic": "BJT", "type": "bjt", "q": "מה נדרש בטרנזיסטור ביפולרי (BJT) כדי שיתפקד כראוי?", "opts": ["א. צומת בסיס-קולקטור בממתח קדמי", "ב. רוחב הבסיס קטן ממרחק הדיפוזיה", "ג. זרם בסיס גדול מהקולקטור"], "ans": 1, "explain": "כדי שהמטענים יגיעו לקולקטור, רוחב הבסיס חייב להיות קטן ממרחק הדיפוזיה $W \ll L$[cite: 17]."},
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS, אם מעלים את המתח $V_{GS}$:", "opts": ["א. הזרם גדל תמיד אם הטרנזיסטור אינו בקיטעון", "ב. הזרם גדל לינארית תמיד", "ג. הזרם קבוע"], "ans": 0, "explain": "עליית מתח השער מעבר לסף מגדילה את זרם הניקוז[cite: 23]."},
        {"topic": "PN Junction", "type": "field", "q": "מה נכון עבור צומת PN בשיווי משקל בטמפרטורת החדר?", "opts": ["א. אין שום זרימה של נושאי מטען", "ב. זרם החורים מנטרל בדיוק את זרם האלקטרונים", "ג. אין שדה חשמלי פנימי"], "ans": 1, "explain": "בשיווי משקל, הזרם הכולל של כל סוג מוביל מטען מתאפס[cite: 31]."},
        {"topic": "Physics", "type": "ni", "q": "במל''מ סוג P בשיווי משקל, איזה משפט נכון תמיד?", "opts": ["א. ריכוז החורים קבוע", "ב. קצב הגנרציה של החורים שווה לקצב הריקומבינציה שלהם", "ג. אין דיפוזיה של חורים"], "ans": 1, "explain": "בשיווי משקל תרמי קצב הגנרציה שווה תמיד לקצב הריקומבינציה[cite: 38]."},
        {"topic": "NMOS", "type": "cv", "q": "איזה משפט תמיד שגוי עבור NMOS?", "opts": ["א. מטען האינברסיה בקרבת השפך גדול מאשר בקרבת המקור", "ב. הזרם גדל עם עלית $V_{DS}$", "ג. הזרם גדל עם עלית $V_{GS}$"], "ans": 0, "explain": "בשל מפל המתח לאורך התעלה, ריכוז המטענים ליד השפך (Drain) תמיד קטן או שווה לריכוז ליד המקור."},
        {"topic": "PN Junction", "type": "field", "q": "בהשוואה בין דיודה קצרה לארוכה עם אותם סיגומים:", "opts": ["א. הזרם בממתח קדמי קטן בדיודה הארוכה", "ב. המתח המובנה גדול בדיודה הקצרה", "ג. השדה המקסימלי גדול בדיודה הארוכה"], "ans": 0, "explain": "בדיודה ארוכה הגרדיאנט קטן יותר ולכן הזרם נמוך יותר מדיודה קצרה[cite: 60]."},
        {"topic": "MOS", "type": "cv", "q": "בקבל MOS החליפו את התחמוצת בחומר עם מקדם דיאלקטרי גבוה יותר (High-k). מה נכון?", "opts": ["א. קיבול התחמוצת לא השתנה", "ב. קיבול המחסור לא השתנה", "ג. מתח הסף לא השתנה"], "ans": 1, "explain": "קיבול המחסור תלוי בסימום המצע ולא במקדם של שכבת הבידוד[cite: 65]."},
        {"topic": "Temperature", "type": "ni", "q": "מה נכון לגבי המוליכות בעת העלאת הטמפרטורה במל''מ אקסטרינזי?", "opts": ["א. גדלה בכל התחומים", "ב. המוליכות יכולה לקטון בתחום האקסטרינזי", "ג. קטנה בתחום האינטרינזי"], "ans": 1, "explain": "בתחום האקסטרינזי, ירידת הניידות עקב פיזורי סריג יכולה להוריד את המוליכות למרות הריכוז הקבוע[cite: 72]."},
        {"topic": "MOSFET", "type": "cv", "q": "נתון NMOS. אם מגדילים את ריכוז הסימום $N_A$ במצע, מתח הסף $V_T$:", "opts": ["א. לא ישתנה", "ב. יקטן", "ג. יגדל"], "ans": 2, "explain": "הגדלת סימום המצע מגדילה את מטען המחסור הדרוש להגעה לאינברסיה ולכן מעלה את $V_T$[cite: 95]."}
    ]

# --- פונקציות סימולציה ---
def plot_sim(q_type):
    fig, ax = plt.subplots(figsize=(5, 3.5))
    if q_type == "ni":
        t = np.linspace(250, 600, 100); ni = 1e10 * (t/300)**3 * np.exp(-1.12/(2*8.6e-5*t))
        ax.semilogy(t, ni, color='#1e3a8a'); ax.set_title(heb("ריכוז אינטרינזי מול טמפרטורה"))
    elif q_type == "field":
        x = np.linspace(-2, 2, 100); e = np.where(x < 0, 2+x, 2-2*x); e[x > 1] = 0; e[x < -2] = 0
        ax.fill_between(x, e, color='red', alpha=0.2); ax.plot(x, e, 'r'); ax.set_title(heb("שדה חשמלי בצומת"))
    elif q_type == "cv":
        v = np.linspace(-3, 3, 100); c = np.where(v < 0, 1, 0.4)
        ax.plot(v, c, color='green', lw=2); ax.set_title(heb("אופיין קיבול-מתח"))
    elif q_type == "decay":
        x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='orange'); ax.set_title(heb("דעיכת מטענים בחושך"))
    elif q_type == "bjt":
        ax.text(0.5, 0.5, heb("אמיטר (E) -> בסיס (B) -> קולקטור (C)"), ha='center'); ax.axis('off')
    st.pyplot(fig)

# --- ממשק משתמש ---
st.title("🎓 " + "סימולטור מל''מ אריאל - מאגר שאלות מבחן")
if 'idx' not in st.session_state: st.session_state.idx = 0
curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.5, 1])
with col1:
    st.info(f"שאלה {st.session_state.idx + 1} מתוך {len(st.session_state.questions)}")
    st.subheader(heb(curr['topic']))
    st.markdown(f"**{curr['q']}**")
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    if st.button("בדוק תשובה ✅"):
        if curr['opts'].index(ans) == curr['ans']:
            st.success("נכון מאוד! " + curr['explain'])
            st.balloons()
        else: st.error("טעות. הסבר: " + curr['explain'])
    if st.button("שאלה הבאה ➡️"):
        st.session_state.idx += 1; st.rerun()

with col2:
    st.write("### המחשה פיזיקלית")
    plot_sim(curr['type'])

st.divider()
st.caption("פותח בהתאם לסילבוס אריאל | כולל שאלות ממקבצי פתרונות רשמיים [cite: 1-96]")
