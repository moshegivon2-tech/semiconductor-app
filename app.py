import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- CSS חזק לתיקון "מגדלי המספרים" והדולרים ---
st.markdown("""
    <style>
    /* כיווניות כללית לימין */
    .stApp { direction: rtl; text-align: right; background-color: #fcfcfc; }
    
    /* פתרון ה"מגדלים": מניעת שבירת שורות בתוך נוסחאות וכפיית כיוון LTR */
    .katex { 
        direction: ltr !important; 
        display: inline-block !important; 
        white-space: nowrap !important;
        unicode-bidi: isolate !important;
        font-size: 1.2em !important;
        color: #003366;
    }
    
    /* עיצוב תיבת השאלה */
    .q-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        border-right: 10px solid #004a99;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    
    /* יישור תשובות */
    div[role="radiogroup"] label { direction: rtl; text-align: right; display: block; padding: 12px 0; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מלא מכל הקבצים ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # שאלה חישובית מהתמונה [cite: 16-20, 112-126]
        {
            "topic": "Physics", "type": "ni", 
            "q": r"נתונה פיסת סיליקון בשיווי משקל בה $N_a = 10^{17} \text{ cm}^{-3}$ ו-$N_d = 9 \cdot 10^{16} \text{ cm}^{-3}$, וריכוז אינטרינזי $n_i = 10^{17} \text{ cm}^{-3}$. מהו ריכוז האלקטרונים $n$?", 
            "opts": [r"(1) $9.5 \cdot 10^{16} \text{ cm}^{-3}$", r"(2) $9 \cdot 10^{16} \text{ cm}^{-3}$", r"(3) $10^{16} \text{ cm}^{-3}$", r"(4) $10^3 \text{ cm}^{-3}$", r"(5) $2 \cdot 10^3 \text{ cm}^{-3}$"], 
            "ans": 0, "explain": r"משוואת ניטרליות המטען: $n + N_a = p + N_d$. עם $p = n_i^2/n$, פתרון המשוואה הריבועית נותן $9.5 \cdot 10^{16}$."
        },
        # שאלת הארה [cite: 4-14, 100-110]
        {
            "topic": "Illumination", "type": "decay", 
            "q": "בוצעו שני ניסויים של הארת חצי דגם מל''מ, בראשון בעוצמה $P$ ובשני בעוצמה $4P$. המרחק הממוצע $L$ שחודר עודף המטען בחושך הינו:", 
            "opts": ["(1) שווה בשני הניסויים.", "(2) כפול בניסוי השני.", "(3) פי ארבעה בניסוי השני.", "(4) גדול פי $4 \ln$ בניסוי השני.", "(5) גדול פי $e^4$ בניסוי השני."], 
            "ans": 0, "explain": "מרחק הדיפוזיה $L = \\sqrt{D \tau}$ הוא תכונת חומר ואינו תלוי בעוצמת האור[cite: 110]."
        },
        # שאלת סימון בבסיס BJT [cite: 140-145]
        {
            "topic": "BJT", "type": "bjt", 
            "q": "בטרנזיסטור ביפולרי, הגדלת ריכוז הסיגים בבסיס:", 
            "opts": ["(1) מגדילה את הגבר הזרם האחורי.", "(2) מקטינה את הגבר הזרם הקדמי.", "(3) אינה משפיעה על הגבר הזרם האחורי.", "(4) אינה משפיעה על הגבר הזרם הקדמי.", "(5) מגדילה את הגבר הזרם הקדמי."], 
            "ans": 1, "explain": "הגדלת סימום הבסיס מעלה את זרם המטענים מהבסיס לאמיטר ומורידה את יעילות ההזרקה."
        },
        # שאלת דיודה אידיאלית קצרה [cite: 353-355]
        {
            "topic": "PN Junction", "type": "iv", 
            "q": r"בדיודת צומת אידאלית קצרה עם $D_e = 2D_h$ וסיגומים שווים:", 
            "opts": ["(1) זרם האלקטרונים גדול פי 12 מזרם החורים.", "(2) זרם החורים גדול פי 2 מזרם האלקטרונים.", "(3) זרם האלקטרונים כפול מזרם החורים.", "(4) זרם החורים כפול מזרם האלקטרונים.", "(5) זרמי האלקטרונים והחורים שווים."], 
            "ans": 2, "explain": "הזרם פרופורציונלי למקדם הדיפוזיה. בגלל $D_e = 2D_h$, זרם האלקטרונים יהיה כפול."
        },
        # שאלת NMOS בשגוי [cite: 61-63, 117-119]
        {
            "topic": "NMOS", "type": "cv", 
            "q": "בטרנזיסטור NMOS איזה מהמשפטים הבאים שגוי תמיד:", 
            "opts": ["(1) הזרם גדל עם עליית $V_{GS}$.", "(2) מטען האינברסיה בקרבת השפך גדול מאשר בקרבת המקור.", "(3) הזרם גדל מתכונתית לריבוע מתח השער.", "(4) אם הטרנזיסטור אינו קטוע, הזרם ממשיך לגדול עם עליית $V_{GS}$.", "(5) מתח השפך אף פעם לא קטן ממתח המקור."], 
            "ans": 1, "explain": "בשל מפל המתח לאורך התעלה, ריכוז המטענים ליד המקור תמיד גדול יותר מאשר ליד השפך."
        }
    ]

# --- לוגיקת האפליקציה ---
st.title("🎓 סימולטור מל''מ - אוניברסיטת אריאל")

tab_sim, tab_calc = st.tabs(["📝 סימולטור מבחן", "🧮 מחשבון עזר"])

with tab_sim:
    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.markdown(f"""<div class='q-card'>
            <p style='color: #004a99; font-weight: bold;'>שאלה {st.session_state.idx + 1} | נושא: {curr['topic']}</p>
            <p style='font-size: 1.25rem;'>{curr['q']}</p>
        </div>""", unsafe_allow_html=True)
        
        ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("בדוק תשובה ✅"):
                if curr['opts'].index(ans) == curr['ans']:
                    st.success("נכון מאוד!"); st.balloons()
                else: st.error("טעות. הסבר: " + curr['explain'])
        with c2:
            if st.button("שאלה הבאה ➡️"):
                st.session_state.idx += 1; st.rerun()

    with col2:
        st.write("### המחשה פיזיקלית")
        fig, ax = plt.subplots(figsize=(5, 4))
        if curr['type'] == "ni":
            t = np.linspace(250, 600, 100); ni = 1e10 * (t/300)**3 * np.exp(-1.12/(2*8.6e-5*t))
            ax.semilogy(t, ni, color='orange'); ax.set_title("Intrinsic Concentration")
        elif curr['type'] == "decay":
            x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue', lw=2); ax.set_title("Carrier Decay")
        elif curr['type'] == "field":
            x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1+x, 1-2*x); e[x>0.5]=0; e[x<-1.5]=0
            ax.fill_between(x, e, color='red', alpha=0.3); ax.set_title("Electric Field")
        st.pyplot(fig)

with tab_calc:
    st.header("🧮 מחשבון ריכוזי מטענים (שיווי משקל)")
    st.write("מחשב את $n$ ו-$p$ לפי משוואת ניטרליות המטען המלאה.")
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1: na_val = st.number_input("$N_a$ [cm⁻³]", value=1.0e17, format="%.2e")
    with col_i2: nd_val = st.number_input("$N_d$ [cm⁻³]", value=9.0e16, format="%.2e")
    with col_i3: ni_val = st.number_input("$n_i$ [cm⁻³]", value=1.0e17, format="%.2e")
    diff = na_val - nd_val
    n_res = (-diff + np.sqrt(diff**2 + 4*ni_val**2)) / 2
    p_res = ni_val**2 / n_res
    st.divider()
    r1, r2 = st.columns(2)
    r1.metric("ריכוז אלקטרונים $n$", f"{n_res:.3e}")
    r2.metric("ריכוז חורים $p$", f"{p_res:.3e}")
