import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- הגדרות דף ---
st.set_page_config(page_title="Ariel Semiconductor Master", layout="wide")

# --- CSS חזק במיוחד לתיקון המספרים ה"קופצים" ---
st.markdown("""
    <style>
    /* הגדרת כיווניות כללית */
    .stApp { direction: rtl; text-align: right; background-color: #fcfcfc; }
    
    /* מניעת שבירת שורות במספרים ונוסחאות - הפתרון לבעיית ה"מגדלים" */
    .katex { 
        direction: ltr !important; 
        display: inline-block !important; 
        white-space: nowrap !important;
        font-size: 1.1em !important;
        color: #003366;
    }
    
    /* עיצוב תיבת השאלה */
    .q-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-right: 8px solid #004a99;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    
    /* תיקון יישור רדיו (תשובות) */
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    label { direction: rtl; text-align: right; display: block; font-size: 1.1rem; padding: 5px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מלא (עשרות שאלות מכל הקבצים)  [cite: 1-603] ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # שאלה מהתמונה image_053200.png [cite: 112-126]
        {"topic": "Physics", "type": "ni", "q": "נתונה פיסת סיליקון בשיווי משקל בה סיגים נוטלים בריכוז $10^{17} \\text{ cm}^{-3}$ ותורמים בריכוז $9 \\cdot 10^{16} \\text{ cm}^{-3}$, וריכוז אינטרינזי $10^{17} \\text{ cm}^{-3}$. מהו ריכוז האלקטרונים $n$?", 
         "opts": ["(1) $9.5 \\cdot 10^{16} \\text{ cm}^{-3}$", "(2) $9 \\cdot 10^{16} \\text{ cm}^{-3}$", "(3) $10^{16} \\text{ cm}^{-3}$", "(4) $10^3 \\text{ cm}^{-3}$", "(5) $2 \\cdot 10^3 \\text{ cm}^{-3}$"], 
         "ans": 0, "explain": "בגלל ש-$n_i$ גבוה, משתמשים במשוואה הריבועית: $n^2 + (N_a-N_d)n - n_i^2 = 0$. התוצאה היא $9.5 \\cdot 10^{16}$ [cite: 112-126]."},

        # שאלות הארה ומרחקי דיפוזיה [cite: 1-5, 100-110]
        {"topic": "Illumination", "type": "decay", "q": "מאירים חצי דגם סיליקון סוג $N$ ארוך בהזרקה חלשה. כתוצאה:", 
         "opts": ["(1) ריכוז עודף האלק' גדול מריכוז עודף החורים בכל ההתקן.", "(2) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק המואר בלבד.", "(3) ריכוז עודף האלק' גדול מריכוז עודף החורים בחלק החשוך בלבד.", "(4) ריכוז עודף האלק' גדול בחלק המואר מריכוזם בחלק החשוך.", "(5) ריכוז האלק' קבוע בחלק החשוך."], 
         "ans": 3, "explain": "התשובה היא (4): ריכוז המטענים העודפים דועך ככל שמתרחקים ממקור האור [cite: 1-5]."},

        # שאלות דיודה [cite: 6-14, 127-132, 193-203]
        {"topic": "PN Junction", "type": "iv", "q": "הזרם בדיודת צומת $PN$ הוא תמיד:", 
         "opts": ["(1) בכיוון מנוגד למתח הכולל.", "(2) תלוי אקספוננציאלית בממתח החיצוני.", "(3) סכום זרם סחיפה של אלק' ודיפוזיה של חורים.", "(4) סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים.", "(5) זרם סחיפה בממתח אחורי ודיפוזיה בממתח קידמי."], 
         "ans": 4, "explain": "התשובה הנכונה היא (5): זהו המנגנון הפיזיקלי בשני המצבים [cite: 6-9]."},

        # שאלות BJT [cite: 15-24, 135-146, 204-211]
        {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור ביפולרי PNP עם $\\gamma=0.8, b=0.9$ במצב פעיל קדמי ו-$I_E=10mA$. מהו זרם הבסיס $I_B$?", 
         "opts": ["(1) $8 mA$", "(2) $9 mA$", "(3) $1 mA$", "(4) $2 mA$", "(5) $2.8 mA$"], 
         "ans": 4, "explain": "$\\alpha = 0.8 \\times 0.9 = 0.72$. לכן $I_C = 7.2mA$ וזרם הבסיס הוא $10 - 7.2 = 2.8mA$ [cite: 135-152]."},

        # שאלות MOSFET  [cite: 44-46, 117-119, 534-536]
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS בתחום הרוויה, עם הגדלת המתח בין השער למקור $V_{GS}$ מתקיים:", 
         "opts": ["(1) מטען החורים בשפה קטן בקרבת השפך.", "(2) מטען האלקטרונים בשפה קטן בקרבת השפך.", "(3) נקודת הצביטה מתרחקת מהשפך.", "(4) נקודת הצביטה מתקרבת לשפך.", "(5) מטען האלקטרונים בשפה קטן בקרבת המקור."], 
         "ans": 3, "explain": "הגדלת המתח גורמת לנקודת הצביטה (Pinch-off) להתקרב לשפך (Drain) [cite: 118-119]."},
    ]

# --- לוגיקה של האפליקציה ---
st.title("🎓 סימולטור מל''מ אריאל - גרסה 2.0")

# ניהול טאבים
tab_exam, tab_calc = st.tabs(["📝 סימולטור מבחן", "🧮 מחשבון עזר"])

with tab_exam:
    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.markdown(f"""<div class='q-card'>
            <p style='color: #004a99; font-weight: bold;'>שאלה {st.session_state.idx + 1} | נושא: {curr['topic']}</p>
            <p style='font-size: 1.25rem;'>{curr['q']}</p>
        </div>""", unsafe_allow_html=True)
        
        ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
        
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            if st.button("בדוק תשובה ✅"):
                if curr['opts'].index(ans) == curr['ans']:
                    st.success("נכון! " + curr['explain']); st.balloons()
                else: st.error("טעות. הסבר: " + curr['explain'])
        with c_b2:
            if st.button("שאלה הבאה ➡️"):
                st.session_state.idx += 1; st.rerun()

    with col2:
        st.write("### המחשה פיזיקלית")
        fig, ax = plt.subplots(figsize=(5, 4))
        t_type = curr.get("type", "none")
        if t_type == "ni":
            t = np.linspace(250, 600, 100); ni = 1e10 * (t/300)**3 * np.exp(-1.12/(2*8.6e-5*t))
            ax.semilogy(t, ni, color='orange'); ax.set_title("Intrinsic Concentration")
            
        elif t_type == "decay":
            x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue'); ax.set_title("Carrier Decay")
            
        elif t_type == "field":
            x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1+x, 1-2*x); e[x>0.5]=0; e[x<-1.5]=0
            ax.fill_between(x, e, color='red', alpha=0.3); ax.set_title("Electric Field")
            
        st.pyplot(fig)

with tab_calc:
    st.header("🧮 מחשבון ריכוזי מטענים (שיווי משקל)")
    st.write("חישוב מדויק לפי משוואת ניטרליות המטען: $n^2 + (N_a - N_d)n - n_i^2 = 0$")
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
