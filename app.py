import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- הגדרות דף ---
st.set_page_config(page_title="Ariel Semiconductor Master", layout="wide")

# --- CSS חזק לתצוגה נקייה ומניעת "מגדלי מספרים" ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #fcfcfc; }
    
    /* מניעת שבירת שורות בתוך נוסחאות וכפיית כיוון LTR */
    .katex { 
        direction: ltr !important; 
        display: inline-block !important; 
        white-space: nowrap !important;
        unicode-bidi: isolate !important;
        font-size: 1.15em !important;
        color: #003366;
    }
    
    .q-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-right: 10px solid #004a99;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    
    div[role="radiogroup"] label { direction: rtl; text-align: right; display: block; padding: 10px 0; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות מורחב (20 שאלות מהמבחנים) ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        # 1. הארה ומרחק דיפוזיה [cite: 4, 107-110]
        {"topic": "Physics", "type": "decay", "q": "מה יקרה למרחק הממוצע שחודר עודף המטען בחלק החשוך אם נשנה את עוצמת ההארה?", 
         "opts": ["(1) עוצמה P מול 4P -> המרחק שווה בשני הניסויים", "(2) עוצמה P מול 4P -> המרחק יוכפל", "(3) המרחק יגדל פי 4", "(4) המרחק יקטן פי 2", "(5) המרחק יגדל פי שורש 2"], 
         "ans": 0, "explain": "מרחק הדיפוזיה $L = \\sqrt{D \\tau}$ תלוי בתכונות החומר בלבד[cite: 107]."},

        # 2. חישוב ריכוזים [cite: 16-20, 112-126]
        {"topic": "Physics", "type": "ni", "q": "מהו ריכוז האלקטרונים בפיסת סיליקון בשיווי משקל עם הנתונים הבאים?", 
         "opts": [r"(1) $N_a=10^{17}, N_d=9\cdot 10^{16}, n_i=10^{17} \rightarrow n = 9.5 \cdot 10^{16} \text{ cm}^{-3}$", r"(2) $n = 9 \cdot 10^{16} \text{ cm}^{-3}$", r"(3) $n = 10^{16} \text{ cm}^{-3}$", r"(4) $n = 10^3 \text{ cm}^{-3}$", r"(5) $n = 2 \cdot 10^3 \text{ cm}^{-3}$"], 
         "ans": 0, "explain": "בשל $n_i$ גבוה, משתמשים במשוואה הריבועית: $n^2 + (N_a - N_d)n - n_i^2 = 0$[cite: 117]."},

        # 3. זרם דיודה שגויה [cite: 31-36]
        {"topic": "PN Junction", "type": "field", "q": "בדיודת צומת בממתח קדמי, איזה מהמשפטים הבאים שגוי תמיד?", 
         "opts": ["(1) המתח הכולל קטן מהמתח המובנה", "(2) הזרם באחורי גדל עם המתח", "(3) הזרם בקצרה קטן מאשר בארוכה", "(4) הזרם בקדמי גדול בארוכה מאשר בקצרה", "(5) השדה מקסימלי בצומת המטלורגי"], 
         "ans": 3, "explain": "בדיודה קצרה הגרדיאנט חד יותר ולכן הזרם תמיד גדול יותר[cite: 35]."},

        # 4. זרם בסיס BJT [cite: 39-56, 135-146]
        {"topic": "BJT", "type": "bjt", "q": "נתון טרנזיסטור PNP במצב פעיל קדמי. מהו זרם הבסיס?", 
         "opts": [r"(1) $\gamma=0.8, b=0.9, I_E=10mA \rightarrow I_B = 8 mA$", r"(2) $I_B = 9 mA$", r"(3) $I_B = 1 mA$", r"(4) $I_B = 2 mA$", r"(5) $\gamma=0.8, b=0.9, I_E=10mA \rightarrow I_B = 2.8 mA$"], 
         "ans": 4, "explain": r"$\alpha = \gamma \cdot b = 0.72$. $I_C = 7.2mA$. לכן $I_B = I_E - I_C = 2.8mA$[cite: 147]."},

        # 5. NMOS שגוי [cite: 61-63, 117-119]
        {"topic": "NMOS", "type": "cv", "q": "בטרנזיסטור NMOS, איזה מהמשפטים הבאים שגוי תמיד?", 
         "opts": ["(1) מתח השפך אינו קטן ממתח המקור", "(2) מטען האינברסיה בשפך גדול מאשר במקור", "(3) הזרם גדל עם עליית Vgs", "(4) הזרם גדל עם עליית Vds", "(5) הזרם גדל ריבועית עם מתח השער"], 
         "ans": 1, "explain": "ריכוז המטענים דועך מהמקור לכיוון השפך בגלל מפל המתח[cite: 118]."},

        # 6. יחס ריכוזים [cite: 70-83, 165-179]
        {"topic": "Physics", "type": "ni", "q": "בפיסת סיליקון בה ריכוז התורמים שווה לריכוז האינטרינזי, פי כמה גדול ריכוז האלקטרונים מהחורים?", 
         "opts": ["(1) פי 1.5", "(2) פי 2.6", "(3) פי 2", "(4) פי 3", "(5) פי 4"], 
         "ans": 1, "explain": "מפתרון משוואת הניטרליות עם $N_d = n_i$ מקבלים יחס של 2.6[cite: 179]."},

        # 7. הצמדת דגמים [cite: 84-96, 180-192]
        {"topic": "Diffusion", "type": "decay", "q": "מצמידים שני דגמי סיליקון P עם זמני חיים שונים אחרי הארה ממושכת. מה יקרה?", 
         "opts": [r"(1) $\tau_A=1\mu s, \tau_B=2\mu s \rightarrow$ חורים מ-A ל-B", r"(2) חורים מ-B ל-A", r"(3) אלקטרונים בלבד מ-B ל-A", r"(4) אלקטרונים וחורים מ-A ל-B", r"(5) אלקטרונים וחורים מ-B ל-A"], 
         "ans": 4, "explain": "בדגם B יש יותר עודף מטענים בגלל זמן חיים ארוך יותר, לכן שניהם יפעפעו ל-A[cite: 192]."},

        # 8. קיבול דיודה [cite: 104-107, 193-203]
        {"topic": "PN Junction", "type": "cv", "q": "מגדילים ממתח קדמי מ-0.3V ל-0.6V. מה יקרה לקיבולים?", 
         "opts": ["(1) שניהם גדלים פי 2", "(2) מחסור קטן פי 2, דיפוזיה גדל פי 2", r"(3) מחסור גדל פי $\sqrt{2}$, דיפוזיה גדל פי $10^5$", "(4) שניהם גדלים פי 100", "(5) מחסור גדל פי 2, דיפוזיה גדל פי $10^5$"], 
         "ans": 2, "explain": "קיבול הדיפוזיה גדל אקספוננציאלית עם המתח[cite: 203]."},

        # 9. הגבר BJT [cite: 108-115, 204-211]
        {"topic": "BJT", "type": "bjt", "q": "מדוע הגבר הטרנזיסטור גרוע בחיבור פעיל אחורי בהשוואה לפעיל קדמי?", 
         "opts": ["(1) ממתח BE קטן מדי", "(2) רוחב בסיס גדול מדי", "(3) מטענים מהקולקטור לא מגיעים לפולט", "(4) זרם בסיס גדול מדי", "(5) ממתח BC גדול מדי"], 
         "ans": 2, "explain": "בשל חוסר סימטריה גיאומטרית, רוב המטענים אובדים בבסיס[cite: 211]."},

        # 10. פריצת מפולת [cite: 208-218, 304-314]
        {"topic": "Breakdown", "type": "field", "q": "כיצד משפיע חימום הדיודה על פריצת המפולת (Avalanche)?", 
         "opts": ["(1) במתח נמוך יותר (ניידות יורדת)", "(2) במתח נמוך יותר (W קטן)", "(3) במתח גבוה יותר (תנודות תרמיות)", "(4) במתח גבוה יותר (זרם רוויה)", "(5) לא משתנה"], 
         "ans": 2, "explain": "פיזורי סריג גדלים עם הטמפרטורה, מה שדורש שדה חזק יותר ליינון[cite: 217]."},

        # שאלות נוספות מקוצרות למקום...
        {"topic": "Physics", "type": "ni", "q": "איזו מדידה תאפשר להעריך את אנרגיית הפער Eg?", "opts": ["(1) מוליכות מול מתח", "(2) ניידות מול מתח", "(3) קיבול מול מתח", "(4) ניידות מול טמפרטורה", "(5) מוליכות מול טמפרטורה"], "ans": 4, "explain": "Eg משפיעה על ni שמשפיע על המוליכות בטמפרטורה גבוהה[cite: 57]."},
        {"topic": "Conductivity", "type": "ni", "q": "מה נכון לגבי מוליכות מל''מ אקסטרינזי בחימום?", "opts": ["(1) גדלה תמיד", "(2) גדלה רק באינטרינזי", "(3) קטנה בקיפאון", "(4) קטנה באקסטרינזי", "(5) קטנה רק באינטרינזי"], "ans": 3, "explain": "באקסטרינזי הניידות יורדת בגלל פיזורי סריג[cite: 126]."},
        {"topic": "Physics", "type": "ni", "q": "היכן ממוקמת רמת פרמי באפס המוחלט בחומר עם Na=2Nd?", "opts": ["(1) באמצע הפס", "(2) ליד פס הולכה", "(3) ליד פס ערכיות", "(4) ברמת הנוטלים", "(5) ברמת התורמים"], "ans": 3, "explain": "החומר הוא מסוג P, לכן באפס המוחלט Ef ברמת הנוטלים[cite: 133]."},
        {"topic": "BJT", "type": "bjt", "q": "איך משפיעה הגדלת סימום הבסיס ב-BJT?", "opts": ["(1) מגדילה הגבר אחורי", "(2) מקטינה הגבר קדמי", "(3) לא משפיעה על אחורי", "(4) לא משפיעה על קדמי", "(5) מגדילה הגבר קדמי"], "ans": 1, "explain": "סימום בסיס גבוה מוריד את יעילות ההזרקה מהאמיטר[cite: 142]."},
        {"topic": "MOS", "type": "cv", "q": "מה קורה בתוך שכבת האינברסיה בטרנזיסטור MOS?", "opts": ["(1) המל''מ אינטרינזי בתוך השכבה", "(2) המל''מ אינטרינזי מתחת לשכבה", "(3) המל''מ אינטרינזי בשפה", "(4) אין נקודה אינטרינזית", "(5) אינטרינזי בכל השכבה"], "ans": 1, "explain": "במעבר מ-P ל-N (אינברסיה) חייבת להיות נקודה אינטרינזית[cite: 147]."},
        {"topic": "PN Junction", "type": "iv", "q": "מה נכון לגבי זרמי דיודה אידאלית קצרה עם De=2Dh?", "opts": ["(1) זרם אלק' גדול פי 12", "(2) זרם חורים גדול פי 2", "(3) זרם אלק' כפול מחורים", "(4) זרם חורים כפול מאלק'", "(5) הזרמים שווים"], "ans": 2, "explain": "הזרם פרופורציונלי למקדם הדיפוזיה D[cite: 354]."},
        {"topic": "NMOS", "type": "cv", "q": "מה קורה לנקודת הצביטה (Pinch-off) עם הגדלת Vgs?", "opts": ["(1) מתרחקת מהשפך", "(2) מתקרבת לשפך", "(3) לא זזה", "(4) נעלמת", "(5) עוברת למקור"], "ans": 1, "explain": "הגדלת Vgs מרחיבה את התעלה ודוחפת את הצביטה לכיוון השפך[cite: 118]."},
        {"topic": "Physics", "type": "decay", "q": "מה קורה אם מאירים נקודתית במרכז פיסת סיליקון P?", "opts": ["(1) דיפוזיה של שניהם לצדדים", "(2) חורים בלבד לצדדים", "(3) אלקטרונים בלבד לצדדים", "(4) חורים לצדדים ואלקטרונים למרכז", "(5) אלקטרונים לצדדים וחורים למרכז"], "ans": 0, "explain": "נוצר עודף של שני סוגי המטענים במרכז והם מפעפעים החוץ[cite: 495]."},
        {"topic": "Physics", "type": "decay", "q": "מה קורה כשמצמידים סיליקון P לגרמניום עם סימום זהה?", "opts": ["(1) חורים מגרמניום לסיליקון", "(2) אלקטרונים מגרמניום לסיליקון", "(3) חורים מסיליקון לגרמניום", "(4) אלקטרונים מסיליקון לגרמניום", "(5) שניהם מסיליקון לגרמניום"], "ans": 4, "explain": "לגרמניום ni גבוה בהרבה, לכן ריכוזי המטענים בו גבוהים יותר והם יפעפעו לסיליקון[cite: 501]."},
        {"topic": "PN Junction", "type": "iv", "q": "מה נכון לגבי זרם אחורי בדיודה קצרה מול ארוכה?", "opts": ["(1) גדול יותר כי מטענים מהמגע מגיעים", "(2) גדול יותר בגלל האצה", "(3) גדול יותר בגלל מעבר ישיר", "(4) גדול יותר כי W רחב", "(5) קטן יותר"], "ans": 0, "explain": "בדיודה קצרה המגע האוהמי 'שואב' מטענים ומגדיל את הגרדיאנט[cite: 503]."}
    ]

# --- לוגיקה של האפליקציה ---
st.title("🎓 סימולטור מל''מ אריאל - מאגר 20 שאלות")

tab_sim, tab_calc = st.tabs(["📝 סימולטור מבחן", "🧮 מחשבון ונתונים"])

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
            
        elif curr['type'] == "bjt":
            ax.add_patch(plt.Rectangle((0.1, 0.3), 0.2, 0.4, color='blue', alpha=0.3)); ax.text(0.15, 0.5, "E")
            ax.add_patch(plt.Rectangle((0.3, 0.3), 0.1, 0.4, color='red', alpha=0.3)); ax.text(0.32, 0.5, "B")
            ax.add_patch(plt.Rectangle((0.4, 0.3), 0.4, 0.4, color='green', alpha=0.3)); ax.text(0.55, 0.5, "C"); ax.axis('off')
            
        st.pyplot(fig)

with tab_calc:
    st.header("🧮 מחשבון ריכוזים ונתונים")
    st.subheader("📋 קבועים פיזיקליים")
    st.latex(r"q = 1.6 \cdot 10^{-19} \text{ C}, \quad k = 8.617 \cdot 10^{-5} \text{ eV/K}")
    st.latex(r"n \cdot p = n_i^2, \quad V_{bi} = \frac{kT}{q} \ln\left(\frac{N_a N_d}{n_i^2}\right)")
    
    st.divider()
    st.write("### מחשבון ריכוזים מהיר ($n, p$)")
    c_i1, c_i2, c_i3 = st.columns(3)
    with c_i1: na_v = st.number_input("$N_a$ [cm⁻³]", value=1.0e17, format="%.2e")
    with c_i2: nd_v = st.number_input("$N_d$ [cm⁻³]", value=9.0e16, format="%.2e")
    with c_i3: ni_v = st.number_input("$n_i$ [cm⁻³]", value=1.0e17, format="%.2e")
    
    diff = na_v - nd_v
    n_res = (-diff + np.sqrt(diff**2 + 4*ni_v**2)) / 2
    p_res = ni_v**2 / n_res
    st.metric("ריכוז אלקטרונים $n$", f"{n_res:.3e}")
    st.metric("ריכוז חורים $p$", f"{p_res:.3e}")
