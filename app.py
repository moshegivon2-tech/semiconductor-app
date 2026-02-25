import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- הגדרות דף ---
st.set_page_config(page_title="Ariel Semiconductor Master", layout="wide")

# פונקציית עברית לגרפים בלבד (היפוך ידני למניעת באגים)
def heb(text):
    return text[::-1] if text else ""

# CSS ל-RTL מלא ושמירה על נוסחאות
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #f4f7f9; }
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { direction: rtl; }
    .katex { direction: ltr !important; display: inline-block !important; font-size: 1.1em; color: #003366; }
    div[role="radiogroup"] { direction: rtl; }
    .stButton>button { background-color: #004a99; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מורחב  ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # קבוצה 1: פיזיקה והארה [cite: 1-5, 25-27]
        {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג $N$ ארוך בהזרקה חלשה. מה נכון לגבי החלק החשוך?", "opts": ["א. ריכוז עודף האלק' גדול מריכוז עודף החורים", "ב. ריכוז האלק' קבוע בחלק החשוך", "ג. ריכוז החורים קבוע"], "ans": 1, "explain": "במוליך למחצה מסוג $N$ בהזרקה חלשה, ריכוז האלקטרונים (נושאי הרוב) נשאר קבוע בקירוב[cite: 5]."},
        {"topic": "Physics", "type": "decay", "q": "בניסוי עם עוצמת הארה $P$ ובניסוי עם $2P$, מה המרחק הממוצע שחודר עודף המטען בחלק החשוך?", "opts": ["א. כפול בניסוי השני", "ב. שווה בשני הניסויים", "ג. גדול פי $\sqrt{2}$ בניסוי השני"], "ans": 1, "explain": "מרחק הדיפוזיה $L = \sqrt{D \tau}$ הוא תכונת חומר ואינו תלוי בעוצמת האור[cite: 26]."},
        
        # קבוצה 2: צומת PN [cite: 6-14, 29-34, 41-43, 50-53, 58-61]
        {"topic": "PN Junction", "type": "iv", "q": "הזרם בדיודת צומת $PN$ הוא תמיד:", "opts": ["א. בכיוון מנוגד למתח הכולל", "ב. סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים", "ג. תלוי אקספוננציאלית בממתח החיצוני"], "ans": 1, "explain": "הזרם הכולל מורכב ממרכיבי הסחיפה והדיפוזיה של המטענים[cite: 9]."},
        {"topic": "Equilibrium", "type": "ni", "q": "במל''מ סוג $N$ בשיווי משקל, מה תמיד נכון?", "opts": ["א. ריכוז האלקטרונים שווה לריכוז הסיגים", "ב. מכפלת ריכוז האלקטרונים בחורים תלויה אקספוננציאלית בטמפרטורה", "ג. ריכוז החורים קבוע בכל החומר"], "ans": 1, "explain": "מכפלת הריכוזים $n \cdot p = n_i^2$ תלויה אקספוננציאלית בטמפרטורה[cite: 14]."},
        {"topic": "Equilibrium", "type": "field", "q": "סמן משפט נכון עבור צומת $PN$ בשיווי-משקל בטמפרטורת החדר:", "opts": ["א. אלקטרונים זורמים מצד $N$ לצד $P$ בדיפוזיה", "ב. זרם החורים מנטרל בדיוק את זרם האלקטרונים", "ג. אין שום זרימה של נושאי מטען"], "ans": 0, "explain": "בשיווי משקל קיימים זרמי דיפוזיה וסחיפה שווים ומנוגדים; אלקטרונים נעים בדיפוזיה מריכוז גבוה ($N$) לנמוך ($P$)[cite: 34]."},
        {"topic": "PN Junction", "type": "field", "q": "בדיודת צומת בממתח קדמי, איזה משפט שגוי תמיד?", "opts": ["א. השדה החשמלי מקסימלי בצומת המטלורגי", "ב. הזרם בממתח אחורי גדל עם המתח", "ג. הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה"], "ans": 2, "explain": "בדיודה קצרה הגרדיאנט חריף יותר, ולכן הזרם בה גדול יותר מאשר בדיודה ארוכה תחת אותו מתח[cite: 42, 60]."},

        # קבוצה 3: טרנזיסטורים (BJT & MOS) [cite: 15-24, 44-49, 62-65, 86-96]
        {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור ביפולרי נדרש כי:", "opts": ["א. צומת בסיס-קולקטור יהיה בממתח אחורי", "ב. רוחב הבסיס קטן ממרחק הדיפוזיה", "ג. זרם הבסיס קטן מזרם הקולקטור"], "ans": 1, "explain": "זהו התנאי הקריטי להעברת מטענים מהאמיטר לקולקטור ללא ריקומבינציה מלאה בבסיס[cite: 17]."},
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS מעלים את $V_{GS}$. כתוצאה זרם הטרנזיסטור:", "opts": ["א. גדל תמיד עם המתח אם הטרנ' אינו בקטעון", "ב. גדל לינארית תמיד", "ג. קבוע כל עוד הוא קטן מ-$V_{DS}$"], "ans": 0, "explain": "הגדלת מתח השער מעלה את כמות מטעני האינברסיה ולכן את הזרם[cite: 23]."},
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS, איזה משפט תמיד שגוי?", "opts": ["א. מתח השפך אף פעם לא קטן ממתח המקור", "ב. מטען האינברסיה בקרבת השפך גדול מאשר בקרבת המקור", "ג. הזרם גדל עם עליית $V_{GS}$"], "ans": 1, "explain": "בשל מפל המתח לאורך התעלה, ריכוז המטענים קטן ככל שמתקרבים לשפך (Drain)[cite: 46]."},
        {"topic": "MOS", "type": "cv", "q": "בקבל MOS החליפו את התחמוצת בחומר עם מקדם יחסי גבוה יותר. מה נכון תמיד?", "opts": ["א. מתח הסף לא השתנה", "ב. קיבול המחסור לא השתנה", "ג. קיבול התחמוצת לא השתנה"], "ans": 1, "explain": "קיבול המחסור ($C_j$) תלוי בסימום המצע, לא בחומר המבודד."},
        {"topic": "MOS", "type": "cv", "q": "נתון NMOS. כיצד ישתנה מתח $V_T$ אם נגדיל את ריכוז הסימום $N_A$ במצע?", "opts": ["א. לא ישתנה", "ב. יקטן", "ג. יגדל"], "ans": 2, "explain": "הגדלת $N_A$ מעלה את מטען המחסור המקסימלי הנדרש ליצירת אינברסיה, ולכן $V_T$ עולה[cite: 95]."},

        # קבוצה 4: טמפרטורה ומוליכות [cite: 54-57, 66-72, 79-85]
        {"topic": "Physics", "type": "ni", "q": "כדי לקבל הערכה של אנרגיית הפער ($E_g$) יש למדוד את:", "opts": ["א. המוליכות כתלות במתח", "ב. הקיבול הדיפרנציאלי כתלות במתח", "ג. המוליכות כתלות בטמפרטורה"], "ans": 2, "explain": "אנרגיית הפער משפיעה ישירות על הקשר בין הטמפרטורה לריכוז המובילים והמוליכות[cite: 57]."},
        {"topic": "Conductivity", "type": "ni", "q": "כשמעלים טמפרטורה של מל''מ אקסטרינזי, מה נכון לגבי המוליכות?", "opts": ["א. גדלה בכל התחומים", "ב. יכולה לקטון בתחום האקסטרינזי", "ג. קטנה בתחום האינטרינזי"], "ans": 1, "explain": "בתחום האקסטרינזי הניידות ($\mu$) קטנה עקב פיזורי סריג, מה שעלול להוריד את המוליכות למרות הריכוז הקבוע."},
    ]

# --- ממשק משתמש ---
st.title("🎓 סימולטור מל''מ - אריאל")

if 'idx' not in st.session_state: st.session_state.idx = 0
curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.5, 1])

with col1:
    st.info(f"שאלה {st.session_state.idx + 1} מתוך {len(st.session_state.questions)}")
    st.subheader(f"נושא: {curr['topic']}")
    st.markdown(f"### {curr['q']}")
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("בדוק תשובה ✅"):
            if curr['opts'].index(ans) == curr['ans']:
                st.success("נכון מאוד! " + curr['explain']); st.balloons()
            else: st.error("טעות. רמז: " + curr['explain'])
    with c_btn2:
        if st.button("שאלה הבאה ➡️"):
            st.session_state.idx += 1; st.rerun()

with col2:
    st.write("### המחשה פיזיקלית")
    fig, ax = plt.subplots(figsize=(5, 4))
    q_type = curr.get("type", "none")
    
    if q_type == "ni":
        t = np.linspace(250, 500, 100); ni = 1e10 * (t/300)**1.5 * np.exp(-5000*(1/t - 1/300))
        ax.semilogy(t, ni, 'r'); ax.set_title(heb("ריכוז אינטרינזי מול טמפרטורה"))
        
    elif q_type == "field":
        x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1.5+x, 1.5-3*x); e[x > 0.5] = 0; e[x < -1.5] = 0
        ax.fill_between(x, e, color='blue', alpha=0.3); ax.set_title(heb("שדה חשמלי בצומת"))
        
    elif q_type == "cv":
        v = np.linspace(-3, 3, 100); c = np.where(v < 0, 1, np.where(v < 1, 1 - 0.5*v, 0.4))
        ax.plot(v, c, 'g', lw=2); ax.set_title(heb("עקומת קיבול-מתח"))
        
    elif q_type == "decay":
        x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), 'orange'); ax.set_title(heb("דעיכת נושאי מטען"))
        
    elif q_type == "bjt":
        ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3))
        ax.text(0.2, 0.5, "E"); ax.text(0.35, 0.5, "B"); ax.text(0.6, 0.5, "C")
        ax.set_title(heb("מבנה טרנזיסטור")); ax.axis('off')
        
    
    st.pyplot(fig)

st.divider()
st.caption("מבוסס על מקבץ פתרונות אריאל . בהצלחה!")
