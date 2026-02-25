import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
import arabic_reshaper

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# פונקציה לתיקון עברית בגרפים
def heb(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# --- CSS לתיקון RTL, יישור אנגלית ונוסחאות ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #f8f9fa; }
    .stMarkdown p, .stMarkdown span { direction: rtl; display: block; }
    .katex { direction: ltr !important; display: inline-block !important; font-size: 1.1em; color: #1e3a8a; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    label { direction: rtl; text-align: right; display: block; font-size: 1.05rem; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 10px; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- יצירת טאבים ---
tab1, tab2, tab3 = st.tabs(["📝 סימולטור מבחן", "🧮 מחשבון ריכוזים", "📋 סיכום נוסחאות"])

# --- טאב 1: סימולטור מבחן ---
with tab1:
    if 'questions' not in st.session_state:
        st.session_state.questions = [
            # שאלות הארה ומרחק דיפוזיה [cite: 100-110, 25-27]
            {"topic": "Physics", "type": "decay", "q": "בוצעו שני ניסויים של הארת חצי דגם מל''מ, בראשון בעוצמה $P$ ובשני פי ארבעה ($4P$). המרחק הממוצע $L$ שחודר עודף המטען בחלק החשוך הינו:", 
             "opts": ["(1) כפול בניסוי השני.", "(2) שווה בשני הניסויים.", "(3) פי ארבעה בניסוי השני.", "(4) גדול פי $4 \\ln$ בניסוי השני.", "(5) גדול פי $e^4$ בניסוי השני."], 
             "ans": 1, "explain": "מרחק הדיפוזיה $L=\\sqrt{D\\tau}$ הוא תכונת חומר ואינו תלוי בעוצמת ההארה[cite: 107]."},
            
            # שאלות חישוביות - ריכוזים
            {"topic": "Physics", "type": "ni", "q": "נתונה פיסת סיליקון בשיווי משקל: $N_a=10^{17}, N_d=9\\cdot 10^{16}, n_i=10^{17} [cm^{-3}]$. מהו ריכוז האלקטרונים $n$?", 
             "opts": ["(1) $9.5\\cdot 10^{16} cm^{-3}$", "(2) $9\\cdot 10^{16} cm^{-3}$", "(3) $10^{16} cm^{-3}$", "(4) $10^{3} cm^{-3}$", "(5) $2\\cdot 10^{3} cm^{-3}$"], 
             "ans": 0, "explain": "נשתמש במשוואה $n^2+(N_a-N_d)n-n_i^2=0$. הצבת הנתונים נותנת בדיוק $9.5\\cdot 10^{16}$[cite: 114]."},
            
            # שאלות דיודה וצומת PN [cite: 6-9, 41-43, 127-132]
            {"topic": "PN Junction", "type": "iv", "q": "הזרם בדיודת צומת $PN$ הוא תמיד:", 
             "opts": ["(1) בכיוון מנוגד למתח הכולל.", "(2) תלוי אקספוננציאלית בממתח החיצוני.", "(3) סכום זרם סחיפה של אלק' ודיפוזיה של חורים.", "(4) סכום זרם סחיפה של חורים ודיפוזיה של אלקטרונים.", "(5) זרם סחיפה בממתח אחורי ודיפוזיה בממתח קידמי."], 
             "ans": 4, "explain": "זהו התיאור הפיזיקלי המדויק של מנגנוני הזרם בשני המצבים[cite: 9]."},
            
            {"topic": "PN Junction", "type": "field", "q": "בדיודת צומת בממתח קדמי, איזה מהמשפטים הבאים שגוי תמיד?", 
             "opts": ["(6) המתח הכולל קטן מהמתח המובנה.", "(7) הזרם בממתח אחורי גדל עם המתח.", "(8) הזרם בממתח קדמי גדול בדיודה ארוכה מאשר בקצרה.", "(9) השדה המקסימלי בצומת המטלורגי.", "(10) המתח המובנה נופל בעקרו על הצד הפחות מסומם."], 
             "ans": 2, "explain": "בדיודה קצרה הגרדיאנט חד יותר ולכן הזרם גדול יותר מדיודה ארוכה[cite: 42]."},

            # שאלות BJT [cite: 15-19, 135-146, 204-211]
            {"topic": "BJT", "type": "bjt", "q": "בטרנזיסטור ביפולרי מסוג $PNP$ עם $\\gamma=0.8, b=0.9$, וזרם אמיטר $I_E=10mA$, מהו זרם הבסיס $I_B$?", 
             "opts": ["(1) $8 mA$", "(2) $9 mA$", "(3) $1 mA$", "(4) $2 mA$", "(5) $2.8 mA$"], 
             "ans": 4, "explain": "$\\alpha = 0.8 \\times 0.9 = 0.72$. לכן $I_C = 7.2mA$ וזרם הבסיס הוא $10 - 7.2 = 2.8mA$ [cite: 147-152]."},
            
            # שאלות MOSFET ו-MOS [cite: 44-46, 62-65, 534-536]
            {"topic": "MOSFET", "type": "cv", "q": "בטרנזיסטור $NMOS$ איזה מהמשפטים תמיד שגוי?", 
             "opts": ["(6) מתח השפך אף פעם לא קטן ממתח המקור.", "(7) אם הטרנזיסטור אינו קטוע הזרם ממשיך לגדול עם $V_{GS}$.", "(8) הזרם גדל עם עליית $V_{DS}$.", "(9) מטען האינברסיה בקרבת השפך גדול מאשר בקרבת המקור.", "(10) הזרם גדל ריבועית עם מתח השער."], 
             "ans": 3, "explain": "מטען האינברסיה דועך לכיוון השפך בגלל מפל המתח לאורך התעלה[cite: 46]."}
        ]

    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]

    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.info(f"שאלה {st.session_state.idx + 1} מתוך המאגר המלא [cite: 1-603]")
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
        if t_type == "decay":
            x = np.linspace(0, 5, 100); ax.plot(x, np.exp(-x), color='blue', lw=2); ax.set_title(heb("דעיכת נושאי מטען"))
            
        elif t_type == "field":
            x = np.linspace(-2, 2, 100); e = np.where(x < 0, 1.5+x, 1.5-3*x); e[x>0.5]=0; e[x<-1.5]=0
            ax.fill_between(x, e, color='red', alpha=0.3); ax.set_title(heb("פילוג שדה חשמלי"))
            
        elif t_type == "ni":
            t_vals = np.linspace(250, 600, 100); ni_vals = 1e10 * (t_vals/300)**3 * np.exp(-1.12/(2*8.6e-5*t_vals))
            ax.semilogy(t_vals, ni_vals, color='orange'); ax.set_title(heb("ריכוז ni מול טמפרטורה"))
            
        elif t_type == "bjt":
            ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3))
            ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3))
            ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3))
            ax.text(0.2, 0.5, "E"); ax.text(0.35, 0.5, "B"); ax.text(0.6, 0.5, "C"); ax.axis('off')
            
        elif t_type == "cv":
            v_v = np.linspace(-3, 3, 100); c_v = np.where(v_v < 0, 1, 0.4)
            ax.plot(v_v, c_v, 'g', lw=2); ax.set_title(heb("אופיין קיבול-מתח"))
            
        st.pyplot(fig)

# --- טאב 2: מחשבון ריכוזים ---
with tab2:
    st.header("🧮 מחשבון ריכוזי מטענים (שיווי משקל)")
    st.write("פותר את משוואת ניטרליות המטען המלאה: $n^2 + (N_a - N_d)n - n_i^2 = 0$")
    
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1: na_val = st.number_input("ריכוז אקספטורים $N_a$ [cm⁻³]", value=1.0e17, format="%.2e")
    with col_in2: nd_val = st.number_input("ריכוז דונורים $N_d$ [cm⁻³]", value=9.0e16, format="%.2e")
    with col_in3: ni_val = st.number_input("ריכוז אינטרינזי $n_i$ [cm⁻³]", value=1.0e17, format="%.2e")
    
    diff = na_val - nd_val
    n_res = (-diff + np.sqrt(diff**2 + 4*ni_val**2)) / 2
    p_res = ni_val**2 / n_res
    
    st.divider()
    r1, r2 = st.columns(2)
    r1.metric("ריכוז אלקטרונים $n$", f"{n_res:.3e}")
    r2.metric("ריכוז חורים $p$", f"{p_res:.3e}")
    st.info("שימוש במשוואה הריבועית מבטיח דיוק גם כאשר $n_i$ גבוה[cite: 114].")

# --- טאב 3: סיכום נוסחאות ---
with tab3:
    st.header("📋 סיכום נוסחאות קריטיות")
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        st.subheader("פיזיקה ודיפוזיה")
        st.latex(r"n \cdot p = n_i^2 \approx T^3 e^{-E_g/kT}")
        st.latex(r"L_p = \sqrt{D_p \tau_p}")
        st.latex(r"J_{diff,p} = -q D_p \frac{dp}{dx}")
    with c_f2:
        st.subheader("צומת PN")
        st.latex(r"V_{bi} = \frac{kT}{q} \ln\left(\frac{N_a N_d}{n_i^2}\right)")
        st.latex(r"W = \sqrt{\frac{2 \epsilon_s}{q} (V_{bi} - V_a) \left(\frac{1}{N_a} + \frac{1}{N_d}\right)}")
        st.latex(r"I = I_0 (e^{qV_a/kT} - 1)")
    st.divider()
    st.subheader("טרנזיסטורים")
    st.latex(r"\text{BJT: } \alpha = \gamma \cdot b, \quad \beta = \frac{\alpha}{1-\alpha}")
    st.latex(r"\text{MOSFET (Sat): } I_D = \frac{W}{2L} \mu C_{ox} (V_{GS} - V_T)^2")
