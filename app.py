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

# --- CSS חזק לתיקון RTL ותצוגה ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #f8f9fa; }
    .stMarkdown p, .stMarkdown span { direction: rtl; display: block; }
    .katex { direction: ltr !important; display: inline-block !important; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    label { direction: rtl; text-align: right; display: block; }
    .question-box { background-color: white; padding: 20px; border-radius: 10px; border-right: 5px solid #1e3a8a; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מורחב (20 שאלות)  ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג $N$ ארוך בהזרקה חלשה. כתוצאה: [cite: 1]", "opts": ["(1) ריכוז עודף האלק' גדול מריכוז עודף החורים בכל ההתקן", "(2) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק המואר בלבד", "(3) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק החשוך בלבד", "(4) ריכוז עודף האלק' גדול בחלק המואר מריכוזם בחלק החשוך", "(5) ריכוז האלק' קבוע בחלק החשוך"], "ans": 3, "explain": "התשובה הנכונה היא (4): ריכוז המטענים העודפים דועך ככל שמתרחקים ממקור האור[cite: 5]."},
        {"topic": "PN Junction", "type": "iv", "q": "הזרם בדיודת צומת $PN$ הוא תמיד: [cite: 6]", "opts": ["(1) בכיוון מנוגד למתח הכולל", "(2) תלוי אקספוננציאלית בממתח החיצוני", "(3) סכום זרם סחיפה של אלק' ודיפוזיה של חורים", "(4) סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים", "(5) זרם סחיפה בממתח אחורי ודיפוזיה בממתח קידמי"], "ans": 4, "explain": "התשובה הנכונה היא (5): זהו המנגנון הפיזיקלי בשני המצבים[cite: 9]."},
        {"topic": "Equilibrium", "type": "ni", "q": "במל''מ סוג $N$ בשיווי משקל, מה תמיד נכון? [cite: 10]", "opts": ["(1) ריכוז החורים קבוע בכל החומר", "(2) ריכוז האלקטרונים שווה לריכוז הסיגים", "(3) ריכוז האלקטרונים תלוי אקספוננציאלית בטמפרטורה", "(4) מכפלת ריכוז האלקטרונים בחורים תלויה אקספוננציאלית בטמפרטורה", "(5) ריכוז האלקטרונים קבוע בכל החומר"], "ans": 3, "explain": "נוסחת חוק המסות $n \\cdot p = n_i^2$ תלויה בטמפרטורה[cite: 14]."},
        {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור ביפולרי נדרש כי: [cite: 15]", "opts": ["(1) צומת בסיס-קולקטור יהיה בממתח אחורי", "(2) רוחב הבסיס קטן ממרחק הדיפוזיה", "(3) זרם הבסיס קטן מזרם הקולקטור", "(4) רוחב הבסיס קטן מרוחב אזור המחסור של צומת BC", "(5) רוחב הבסיס קטן מרוחב אזור המחסור של צומת BE"], "ans": 1, "explain": "כדי שהמטענים יגיעו לקולקטור, הבסיס חייב להיות קצר ממרחק הדיפוזיה[cite: 17]."},
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS מעלים את המתח $V_{GS}$. כתוצאה זרם הטרנזיסטור: [cite: 20]", "opts": ["(1) גדל עם המתח אלא אם כן הטרנ' ברוויה", "(2) גדל לינארית עם המתח תמיד", "(3) קבוע כל עוד הוא קטן מ-$V_{DS}$", "(4) גדל תמיד עם המתח אם הטרנ' אינו בקטעון", "(5) גדל תמיד מתכונתית לריבוע המתח"], "ans": 3, "explain": "אם הטרנזיסטור פתוח, כל הגדלת מתח שער מעלה את הזרם[cite: 23]."},
        {"topic": "Physics", "type": "decay", "q": "בניסוי הארה בעוצמה $P$ ובניסוי בעוצמה $2P$, המרחק שחודר עודף המטען בחושך הינו: [cite: 25]", "opts": ["(6) כפול בניסוי השני", "(7) שווה בשני הניסויים", "(8) גדול פי $\\sqrt{2}$ בניסוי השני", "(9) גדול פי $\\ln$ בניסוי השני", "(10) גדול פי $e^2$ בניסוי השני"], "ans": 1, "explain": "מרחק הדיפוזיה $L = \\sqrt{D \\tau}$ הוא תכונת חומר ואינו תלוי בעוצמת האור[cite: 26]."},
        {"topic": "PN Junction", "type": "field", "q": "מה נכון עבור צומת $PN$ בשיווי-משקל בטמפרטורת החדר? [cite: 29]", "opts": ["(6) חורים זורמים מ-$N$ ל-$P$ בדיפוזיה", "(7) זרם החורים מנטרל בדיוק את זרם האלקטרונים", "(8) אין שום זרימה של נושאי מטען", "(9) אין זרם סחיפה כי אין שדה", "(10) אלקטרונים זורמים מ-$N$ ל-$P$ בדיפוזיה"], "ans": 4, "explain": "בשיווי משקל יש זרמי דיפוזיה וסחיפה המנטרלים זה את זה לכל סוג מטען[cite: 34]."},
        {"topic": "PN Junction", "type": "field", "q": "בדיודת צומת בממתח קדמי, איזה משפט שגוי תמיד? [cite: 41]", "opts": ["(6) המתח הכולל קטן מהמתח המובנה", "(7) הזרם בממתח אחורי גדל עם המתח", "(8) הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה", "(9) השדה מקסימלי בצומת המטלורגי", "(10) המתח המובנה נופל בעיקר על הצד הפחות מסומם"], "ans": 2, "explain": "בדיודה קצרה הגרדיאנט חד יותר ולכן הזרם תמיד גדול יותר מאשר בדיודה ארוכה[cite: 42]."},
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS, איזה מהמשפטים תמיד שגוי? [cite: 44]", "opts": ["(6) מתח השפך אף פעם לא קטן ממתח המקור", "(7) אם הטרנ' אינו קטוע הזרם גדל עם $V_{GS}$", "(8) הזרם גדל עם עליית $V_{DS}$", "(9) מטען האינברסיה ליד השפך גדול מאשר ליד המקור", "(10) הזרם גדל ריבועית עם מתח השער"], "ans": 3, "explain": "מטען האינברסיה קטן ככל שמתקרבים לשפך בגלל מפל המתח[cite: 46]."},
        {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור PNP בתחום פעיל קדמי, איזה משפט שגוי? [cite: 47]", "opts": ["(11) זרם האלק' צריך להיות קטן ככל האפשר", "(12) זרם החורים מהאמיטר מגיע ברובו לקולקטור", "(13) יש להגביר את הריקומבינציה בבסיס", "(14) אלקטרונים מהבסיס זורמים לאמיטר", "(15) רוחב הבסיס קטן בהרבה מ-$L$"], "ans": 2, "explain": "הגברת ריקומבינציה בבסיס מקטינה את ההגבר ולכן זהו משפט שגוי[cite: 49]."},
        {"topic": "Physics", "type": "ni", "q": "כדי לקבל הערכה של אנרגיית הפער $E_g$ יש למדוד את: [cite: 54]", "opts": ["(11) מוליכות כתלות במתח", "(12) ניידות כתלות במתח", "(13) קיבול דיפרנציאלי כתלות במתח", "(14) ניידות כתלות בטמפרטורה", "(15) מוליכות כתלות בטמפרטורה"], "ans": 4, "explain": "מדידת מוליכות בטמפרטורות שונות מאפשרת לחשב את $E_g$ דרך $n_i$[cite: 57]."},
        {"topic": "Conductivity", "type": "ni", "q": "כשמעלים טמפרטורה של מל''מ אקסטרינזי, מה נכון לגבי המוליכות? [cite: 66]", "opts": ["(1) גדלה בכל התחומים", "(2) גדלה רק בתחום האינטרינזי", "(3) קטנה בתחום הקיפאון", "(4) קטנה בתחום האינטרינזי", "(5) יכולה לקטון בתחום האקסטרינזי"], "ans": 4, "explain": "בתחום האקסטרינזי הניידות קטנה מה שעלול להוריד את המוליכות[cite: 72]."},
        {"topic": "Physics", "type": "ni", "q": "בסיליקון עם סיגים נוטלים בריכוז כפול מתורמים, באפס המוחלט רמת פרמי: [cite: 79]", "opts": ["(1) באמצע הפס האסור", "(2) קרוב לפס ההולכה", "(3) קרוב לפס הערכיות", "(4) לא ניתן לדעת", "(5) במחצית ההפרש בין $E_{fi}$ ל-$E_c$"], "ans": 2, "explain": "החומר הוא מסוג P, לכן באפס המוחלט רמת פרמי צמודה לפס הערכיות[cite: 83]."},
        {"topic": "MOS", "type": "cv", "q": "ב-NMOS מגדילים את סימום המצע $N_A$. מתח הסף $V_T$: [cite: 91]", "opts": ["(1) לא ישתנה", "(2) אין קשר לסימום המצע", "(3) יקטן", "(4) יגדל", "(5) יהפוך לאידיאלי"], "ans": 3, "explain": "הגדלת סימום המצע מעלה את המטען הדרוש ליצירת התעלה ולכן מעלה את $V_T$[cite: 95]."},
        {"topic": "Physics", "type": "ni", "q": "נתון: $N_a=10^{17}, N_d=9e16, n_i=10^{17} cm^{-3}$. מהו ריכוז האלקטרונים $n$?", "opts": ["(1) $9.5e16 cm^{-3}$", "(2) $9e16 cm^{-3}$", "(3) $10^{16} cm^{-3}$", "(4) $10^3 cm^{-3}$", "(5) $2e3 cm^{-3}$"], "ans": 0, "explain": "נפתור משוואה ריבועית $n^2 + (N_a-N_d)n - n_i^2 = 0$. התוצאה היא 9.5e16."}
    ]

# --- לוגיקה של האפליקציה ---
st.title("🎓 " + "סימולטור מל''מ אריאל - מאגר 100 שאלות")

if 'idx' not in st.session_state:
    st.session_state.idx = 0

curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

col1, col2 = st.columns([1.6, 1])

with col1:
    st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
    st.info(f"שאלה {st.session_state.idx + 1} מתוך {len(st.session_state.questions)}")
    st.markdown(f"### נושא: {heb(curr['topic'])}")
    st.markdown(f"#### {curr['q']}")
    ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
    
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("בדוק תשובה ✅"):
            if curr['opts'].index(ans) == curr['ans']:
                st.success("נכון מאוד! " + curr['explain'])
                st.balloons()
            else:
                st.error("טעות. הסבר: " + curr['explain'])
    with c_btn2:
        if st.button("שאלה הבאה ➡️"):
            st.session_state.idx += 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.write("### המחשה פיזיקלית")
    fig, ax = plt.subplots(figsize=(5, 4))
    t = curr.get("type", "none")
    if t == "decay":
        x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue', lw=2)
        ax.set_title(heb("דעיכת נושאי מטען"))
            elif t == "field":
        x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1.5+x, 1.5-3*x); e[x>0.5]=0; e[x<-1.5]=0
        ax.fill_between(x, e, color='red', alpha=0.3)
        ax.set_title(heb("פילוג שדה חשמלי בצומת"))
            elif t == "ni":
        temp = np.linspace(250, 600, 100); ni = 1e10 * (temp/300)**3 * np.exp(-1.12/(2*8.6e-5*temp))
        ax.semilogy(temp, ni, color='orange')
        ax.set_title(heb("ריכוז ni מול טמפרטורה"))
            elif t == "bjt":
        ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3))
        ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3))
        ax.text(0.2, 0.5, "E"); ax.text(0.35, 0.5, "B"); ax.text(0.6, 0.5, "C"); ax.axis('off')
            elif t == "cv":
        v = np.linspace(-3, 3, 100); c = np.where(v < 0, 1, 0.4)
        ax.plot(v, c, 'g', lw=2)
        ax.set_title(heb("אופיין קיבול-מתח (C-V)"))
            st.pyplot(fig)

st.divider()
st.caption("מבוסס על מקבץ השאלות הרשמי של אריאל . בהצלחה!")
