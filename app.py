import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

def heb(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- CSS חזק לתיקון RTL ותצוגת מספרים ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #f8f9fa; }
    .stMarkdown p, .stMarkdown span, .stMarkdown h3 { direction: rtl; display: block; }
    /* שמירה על נוסחאות אנגליות ומספרים משמאל לימין */
    .katex { direction: ltr !important; display: inline-block !important; font-size: 1.15em !important; color: #1e3a8a; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    label { direction: rtl; text-align: right; display: block; padding: 5px; font-size: 1.1rem; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; background-color: #004a99; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- יצירת טאבים ---
tab1, tab2, tab3 = st.tabs(["📝 סימולטור מבחן", "🧮 מחשבון ריכוזים", "📋 דף נוסחאות"])

# --- טאב 1: סימולטור מבחן ---
with tab1:
    if 'questions' not in st.session_state:
        st.session_state.questions = [
            # דף 1 [cite: 1-24, 97-111]
            {"topic": "Physics", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג $N$ ארוך בהזרקה חלשה. כתוצאה: [cite: 1-5]", 
             "opts": ["(1) ריכוז עודף האלק' גדול מריכוז עודף החורים בכל ההתקן.", "(2) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק המואר בלבד.", "(3) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק החשוך בלבד.", "(4) ריכוז עודף האלק' גדול בחלק המואר מריכוזם בחלק החשוך.", "(5) ריכוז האלק' קבוע בחלק החשוך."], 
             "ans": 3, "explain": "בשל תהליך הגנרציה והדיפוזיה, ריכוז המטענים העודפים מקסימלי באזור המואר ודועך אקספוננציאלית לאזור החשוך[cite: 5]."},

            {"topic": "PN Junction", "type": "iv", "q": "הזרם בדיודת צומת $PN$ הוא תמיד: [cite: 6-9]", 
             "opts": ["(1) בכיוון מנוגד למתח הכולל.", "(2) תלוי אקספוננציאלית בממתח החיצוני.", "(3) סכום זרם סחיפה של אלק' ודיפוזיה של חורים.", "(4) סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים.", "(5) זרם סחיפה בממתח אחורי ודיפוזיה בממתח קידמי."], 
             "ans": 4, "explain": "זהו התיאור המדויק של מנגנוני הזרם הדומיננטיים בכל סוג ממתח[cite: 9]."},

            {"topic": "Physics", "type": "ni", "q": "נתונה פיסת סיליקון בשיווי משקל: $N_a=10^{17}$, $N_d=9\\cdot 10^{16}$, $n_i=10^{17} \\text{ cm}^{-3}$. מהו ריכוז האלקטרונים $n$?", 
             "opts": ["(1) $9.5\\cdot 10^{16} \\text{ cm}^{-3}$", "(2) $9\\cdot 10^{16} \\text{ cm}^{-3}$", "(3) $10^{16} \\text{ cm}^{-3}$", "(4) $10^3 \\text{ cm}^{-3}$", "(5) $2\\cdot 10^3 \\text{ cm}^{-3}$"], 
             "ans": 0, "explain": "נשתמש במשוואה $n^2 + (N_a-N_d)n - n_i^2 = 0$. הצבת הנתונים נותנת בדיוק $9.5\\cdot 10^{16}$[cite: 117]."},

            # דף 2 [cite: 25-46, 180-215]
            {"topic": "Physics", "type": "decay", "q": "בניסוי עם עוצמת הארה $P$ ובניסוי עם $4P$, המרחק הממוצע שחודר עודף המטען בחושך הינו: [cite: 25-27, 100-110]", 
             "opts": ["(1) שווה בשני הניסויים.", "(2) כפול בניסוי השני.", "(3) פי ארבעה בניסוי השני.", "(4) גדול פי $4\\ln$ בניסוי השני.", "(5) גדול פי $e^4$ בניסוי השני."], 
             "ans": 0, "explain": "מרחק הדיפוזיה $L = \\sqrt{D\\tau}$ הוא תכונת חומר ואינו תלוי בעוצמת ההארה[cite: 26, 107]."},

            {"topic": "PN Junction", "type": "field", "q": "בדיודת צומת בממתח קדמי, איזה מהמשפטים הבאים שגוי תמיד? [cite: 41-43, 127-132]", 
             "opts": ["(1) המתח המובנה נופל בעיקרו על הצד בעל סימום נמוך.", "(2) השדה המקסימלי בנקודת הצומת המטלורגי.", "(3) הזרם בממתח אחורי גדל (בגודלו) עם המתח.", "(4) הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה.", "(5) המתח הכולל בממתח קדמי קטן מהמתח המובנה."], 
             "ans": 3, "explain": "בדיודה קצרה הגרדיאנט חד יותר, ולכן הזרם תמיד גדול יותר מאשר בדיודה ארוכה[cite: 42, 131]."},

            # דף 3 [cite: 47-65, 216-251]
            {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור $PNP$ בתחום הפעיל הקדמי, איזה משפט שגוי? [cite: 47-49]", 
             "opts": ["(1) זרם האלק' מהבסיס לאמיטר צריך להיות קטן.", "(2) זרם החורים מהאמיטר מגיע ברובו לקולקטור.", "(3) יש להגביר את הריקומבינציה בבסיס.", "(4) אלקטרונים מהבסיס זורמים אל האמיטר.", "(5) רוחב הבסיס קטן בהרבה מ-$L$."], 
             "ans": 2, "explain": "הגברת הריקומבינציה בבסיס מקטינה את ההגבר ולכן היא שגויה תמיד[cite: 49]."},

            {"topic": "MOS", "type": "cv", "q": "בקבל $MOS$ אידיאלי החליפו את התחמוצת בחומר עם $k$ גבוה יותר. מה נכון תמיד? [cite: 62-65, 315-323]", 
             "opts": ["(1) מתח הסף לא השתנה.", "(2) השדה בתחמוצת לא השתנה.", "(3) מתח יישור הפסים לא השתנה.", "(4) קיבול התחמוצת לא השתנה.", "(5) קיבול המחסור לא השתנה."], 
             "ans": 4, "explain": "קיבול המחסור תלוי בסימום המצע ובמתח, לא בחומר הדיאלקטרי של השער[cite: 65]."},

            # דף 4 [cite: 66-96, 252-326]
            {"topic": "Conductivity", "type": "ni", "q": "כשמעלים טמפרטורה במל''מ אקסטרינזי, מה נכון לגבי המוליכות? [cite: 66-72, 217-222]", 
             "opts": ["(1) גדלה בכל התחומים.", "(2) גדלה רק בתחום האינטרינזי.", "(3) קטנה בתחום הקיפאון.", "(4) קטנה בתחום האינטרינזי.", "(5) יכולה לקטון בתחום האקסטרינזי."], 
             "ans": 4, "explain": "בתחום האקסטרינזי הניידות קטנה עקב פיזורי סריג, מה שעלול להוריד את המוליכות[cite: 72, 222]."},

            {"topic": "NMOS", "type": "cv", "q": "נתון NMOS. אם מגדילים את סימום המצע $N_a$, כיצד ישתנה מתח $V_t$? [cite: 91-96, 549-558]", 
             "opts": ["(1) לא ישתנה יחסית לשער המקורי.", "(2) אין קשר בין סימום המצע ל-$V_t$.", "(3) יקטן בהשוואה להתקן המקורי.", "(4) יגדל בהשוואה להתקן המקורי.", "(5) ההתקן יהפוך להיות אידיאלי."], 
             "ans": 3, "explain": "הגדלת סימום המצע מעלה את המטען הדרוש לאינברסיה ולכן מעלה את $V_t$[cite: 95]."}
        ]

    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.info(f"שאלה {st.session_state.idx + 1} מתוך המאגר")
        st.markdown(f"### נושא: {heb(curr['topic'])}")
        st.markdown(f"#### {curr['q']}")
        ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
        
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("בדוק תשובה ✅"):
                if curr['opts'].index(ans) == curr['ans']:
                    st.success("נכון מאוד! " + curr['explain']); st.balloons()
                else: st.error("טעות. הסבר: " + curr['explain'])
        with c_b2:
            if st.button("שאלה הבאה ➡️"):
                st.session_state.idx += 1; st.rerun()

    with col2:
        st.write("### המחשה פיזיקלית")
        fig, ax = plt.subplots(figsize=(5, 4))
        t_type = curr.get("type", "none")
        if t_type == "decay":
            x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue', lw=2)
            ax.set_title(heb("דעיכת נושאי מטען"))
            
        elif t_type == "ni":
            t_v = np.linspace(250, 600, 100); ni_v = 1e10 * (t_v/300)**3 * np.exp(-1.12/(2*8.6e-5*t_v))
            ax.semilogy(t_v, ni_v, color='orange'); ax.set_title(heb("ריכוז ni מול טמפרטורה"))
            
        elif t_type == "field":
            x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1.5+x, 1.5-3*x); e[x>0.5]=0; e[x<-1.5]=0
            ax.fill_between(x, e, color='red', alpha=0.3); ax.set_title(heb("פילוג שדה חשמלי"))
            
        elif t_type == "bjt":
            ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3))
            ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3))
            ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3))
            ax.text(0.2, 0.5, "E"); ax.text(0.35, 0.5, "B"); ax.text(0.6, 0.5, "C"); ax.axis('off')
            
        elif t_type == "cv":
            v = np.linspace(-3, 3, 100); c = np.where(v < 0, 1, 0.4)
            ax.plot(v, c, 'g', lw=2); ax.set_title(heb("אופיין קיבול-מתח"))
            
        st.pyplot(fig)

# --- טאב 2: מחשבון ריכוזים ---
with tab2:
    st.header("🧮 מחשבון ריכוזים (שיווי משקל)")
    st.write("פותר את משוואת ניטרליות המטען המלאה: $n^2 + (N_a - N_d)n - n_i^2 = 0$")
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1: na_in = st.number_input("$N_a$ [cm⁻³]", value=1.0e17, format="%.2e")
    with col_i2: nd_in = st.number_input("$N_d$ [cm⁻³]", value=9.0e16, format="%.2e")
    with col_i3: ni_in = st.number_input("$n_i$ [cm⁻³]", value=1.0e17, format="%.2e")
    
    diff = na_in - nd_in
    n_res = (-diff + np.sqrt(diff**2 + 4*ni_in**2)) / 2
    p_res = ni_in**2 / n_res
    st.divider()
    r1, r2 = st.columns(2)
    r1.metric("ריכוז אלקטרונים $n$", f"{n_res:.3e}")
    r2.metric("ריכוז חורים $p$", f"{p_res:.3e}")

# --- טאב 3: סיכום נוסחאות ---
with tab3:
    st.header("📋 דף נוסחאות מהיר")
    st.latex(r"n \cdot p = n_i^2 \approx T^3 e^{-E_g/kT}")
    st.latex(r"V_{bi} = \frac{kT}{q} \ln\left(\frac{N_a N_d}{n_i^2}\right)")
    st.latex(r"W = \sqrt{\frac{2\epsilon_s}{q}(V_{bi}-V_a)\left(\frac{1}{N_a}+\frac{1}{N_d}\right)}")
