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

# --- CSS לתיקון RTL ונוסחאות ---
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    .katex { direction: ltr !important; display: inline-block !important; }
    h1, h2, h3, h4 { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מורחב מהקבצים שלך  ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # דף 1
        {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג $N$ ארוך בהזרקה חלשה. מה נכון לגבי החלק החשוך? [cite: 1-5]", "opts": ["1) ריכוז עודף האלק' גדול מריכוז עודף החורים", "2) ריכוז האלק' קבוע בחלק החשוך", "3) ריכוז החורים קבוע"], "ans": 1, "explain": "במוליך למחצה מסוג $N$ בהזרקה חלשה, ריכוז נושאי הרוב בחלק החשוך נשאר קבוע בקירוב[cite: 5]."},
        {"topic": "PN Junction", "type": "field", "q": "הזרם בדיודת צומת $PN$ הוא תמיד: [cite: 6-9]", "opts": ["1) סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים", "2) תלוי אקספוננציאלית בממתח החיצוני", "3) בכיוון מנוגד למתח הכולל"], "ans": 0, "explain": "הזרם הוא סכום מרכיבי הסחיפה והדיפוזיה של שני סוגי המובילים[cite: 9]."},
        {"topic": "Equilibrium", "type": "ni", "q": "במל''מ סוג $N$ בשיווי משקל, מה נכון תמיד? [cite: 10-14]", "opts": ["1) ריכוז האלקטרונים שווה לריכוז הסיגים", "2) מכפלת ריכוז האלקטרונים בחורים תלויה אקספוננציאלית בטמפרטורה", "3) ריכוז החורים קבוע בכל החומר"], "ans": 1, "explain": "מכפלת הריכוזים $n \cdot p = n_i^2$ תלויה בטמפרטורה דרך הריכוז האינטרינזי[cite: 14]."},
        {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור ביפולרי נדרש כי: [cite: 15-19]", "opts": ["1) צומת בסיס-קולקטור יהיה בממתח קדמי", "2) רוחב הבסיס קטן ממרחק הדיפוזיה", "3) זרם הבסיס גדול מזרם הקולקטור"], "ans": 1, "explain": "כדי שהמטענים יחצו את הבסיס, רוחב הבסיס חייב להיות קטן ממרחק הדיפוזיה $W \ll L$[cite: 17]."},
        {"topic": "NMOS", "type": "cv", "q": "ב-NMOS מעלים את המתח $V_{GS}$. מה קורה לזרם הטרנזיסטור? [cite: 20-24]", "opts": ["1) גדל תמיד עם המתח אם הטרנ' אינו בקיטעון", "2) גדל לינארית תמיד", "3) קבוע כל עוד הוא קטן ממתח הסף"], "ans": 0, "explain": "אם הטרנזיסטור פתוח, הגדלת מתח השער מעבר לסף תגדיל את הזרם[cite: 23]."},
        
        # דף 2
        {"topic": "Illumination", "type": "decay", "q": "בניסוי עם עוצמת הארה $P$ ובניסוי עם $2P$, המרחק הממוצע שחודר עודף המטען הוא: [cite: 25-27]", "opts": ["1) כפול בניסוי השני", "2) שווה בשני הניסויים", "3) גדול פי $\sqrt{2}$ בניסוי השני"], "ans": 1, "explain": "מרחק הדיפוזיה $L = \sqrt{D \tau}$ הוא תכונה של החומר ואינו תלוי בעוצמת ההארה[cite: 26]."},
        {"topic": "PN Junction", "type": "field", "q": "סמן משפט נכון עבור צומת $PN$ בשיווי משקל: [cite: 29-34]", "opts": ["1) אין שום זרימה של נושאי מטען", "2) אלקטרונים זורמים מצד $N$ לצד $P$ בדיפוזיה", "3) אין זרם סחיפה כי אין שדה"], "ans": 1, "explain": "בשיווי משקל יש זרמי דיפוזיה וסחיפה המבטלים זה את זה. אלקטרונים בדיפוזיה זורמים מ-$N$ ל-$P$[cite: 34]."},
        {"topic": "Physics", "type": "ni", "q": "במל''מ סוג $P$ בשיווי משקל, מה נכון תמיד? [cite: 35-40]", "opts": ["1) ריכוז החורים קבוע", "2) קצב הגנרציה של החורים שווה לקצב הריקומבינציה שלהם", "3) אין דיפוזיה של חורים"], "ans": 1, "explain": "בשיווי משקל תרמי, קצב הגנרציה והריקומבינציה חייבים להיות שווים[cite: 38]."},
        {"topic": "PN Junction", "type": "field", "q": "בדיודת צומת בממתח קדמי, איזה משפט שגוי תמיד? [cite: 41-43]", "opts": ["1) השדה החשמלי מקסימלי בנקודת הצומת המטלורגי", "2) הזרם בממתח אחורי גדל עם המתח", "3) המתח המובנה נופל בעיקרו על הצד בעל הסימום הנמוך"], "ans": 1, "explain": "בדיודה אידיאלית הזרם האחורי הוא $I_0$ וקבוע עם המתח[cite: 42]."},
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS, איזה משפט תמיד שגוי? [cite: 44-46]", "opts": ["1) מטען האינברסיה בקרבת השפך גדול מאשר בקרבת המקור", "2) הזרם גדל עם עליית $V_{GS}$", "3) מתח השפך אף פעם לא קטן ממתח המקור"], "ans": 0, "explain": "מטען האינברסיה קטן ככל שמתקרבים לשפך בגלל מפל המתח לאורך התעלה."},

        # דף 3
        {"topic": "PNP BJT", "type": "bjt", "q": "בטרנזיסטור PNP בתחום הפעיל הקדמי, איזה משפט שגוי? [cite: 47-49]", "opts": ["1) זרם החורים מהאמיטר מגיע ברובו לקולקטור", "2) יש להגביר את הריקומבינציה בבסיס", "3) רוחב הבסיס קטן בהרבה ממרחק הדיפוזיה"], "ans": 1, "explain": "הגברת הריקומבינציה בבסיס מקטינה את הגבר הטרנזיסטור, לכן זהו צעד שגוי[cite: 49]."},
        {"topic": "Physics", "type": "ni", "q": "כדי לקבל הערכה של אנרגיית הפער ($E_g$) יש למדוד את: [cite: 54-57]", "opts": ["1) המוליכות כתלות בטמפרטורה", "2) הקיבול הדיפרנציאלי כתלות במתח", "3) הניידות כתלות במתח"], "ans": 0, "explain": "מדידת המוליכות בטמפרטורות שונות מאפשרת לחלץ את $E_g$ מתוך התלות של $n_i$[cite: 57]."},
        {"topic": "PN Junction", "type": "field", "q": "בהשוואה בין דיודה קצרה לארוכה (אותם סיגומים): [cite: 58-61]", "opts": ["1) הזרם בממתח קדמי קטן בדיודה הארוכה", "2) המתח המובנה גדול בדיודה הקצרה", "3) רוחב אזור המחסור קצר בדיודה הקצרה"], "ans": 0, "explain": "בדיודה ארוכה הגרדיאנט קטן יותר ולכן הזרם בממתח קדמי נמוך יותר[cite: 60]."},
        {"topic": "MOS", "type": "cv", "q": "בקבל MOS החליפו את התחמוצת בחומר עם מקדם דיאלקטרי גבוה יותר. מה נכון? [cite: 62-65]", "opts": ["1) קיבול התחמוצת לא השתנה", "2) קיבול המחסור לא השתנה", "3) מתח הסף לא השתנה"], "ans": 1, "explain": "קיבול המחסור ($C_j$) תלוי בסימום המצע ולא במבודד[cite: 65]."},

        # דף 4
        {"topic": "Conductivity", "type": "ni", "q": "כשמעלים טמפרטורה של מל''מ אקסטרינזי, מה נכון לגבי המוליכות? [cite: 66-72]", "opts": ["1) גדלה בכל התחומים", "2) יכולה לקטון בתחום האקסטרינזי", "3) קטנה בתחום האינטרינזי"], "ans": 1, "explain": "בתחום האקסטרינזי המוליכות יכולה לקטון עקב ירידה בניידות המובילים[cite: 72]."},
        {"topic": "NMOS", "type": "cv", "q": "נתון NMOS. אם מגדילים את ריכוז הסימום $N_A$ במצע, מתח הסף $V_T$: [cite: 91-96]", "opts": ["1) לא ישתנה", "2) יקטן", "3) יגדל"], "ans": 2, "explain": "הגדלת $N_A$ מגדילה את מטען המחסור המקסימלי הנדרש לסף, ולכן $V_T$ גדל[cite: 95]."}
    ]

# --- ממשק משתמש ---
st.title("🎓 " + "סימולטור מל''מ אריאל - מאגר שאלות מבחן")
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
        else: st.error("טעות. הסבר: " + curr['explain'])
    if st.button("שאלה הבאה ➡️"):
        st.session_state.idx += 1; st.rerun()

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
