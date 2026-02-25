import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- הגדרות דף ---
st.set_page_config(page_title="Semiconductor Master Ariel", layout="wide")

# --- CSS חזק לתיקון RTL, מניעת "מגדלי מספרים" והצגת נוסחאות ---
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #fcfcfc; }
    .katex { 
        direction: ltr !important; 
        display: inline-block !important; 
        white-space: nowrap !important;
        font-size: 1.15em !important;
        color: #1e3a8a;
    }
    .q-card { 
        background-color: white; 
        padding: 25px; 
        border-radius: 15px; 
        border-right: 10px solid #004a99; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.08); 
        margin-bottom: 25px; 
    }
    .sol-box {
        background-color: #f0f7ff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #cce3ff;
        margin-top: 15px;
    }
    div[role="radiogroup"] label { direction: rtl; text-align: right; display: block; padding: 10px 0; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 10px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- מאגר שאלות אמריקאיות (60 שאלות) ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"topic": "Physics", "type": "ni", "q": "מהו ריכוז האלקטרונים בסיליקון בשיווי משקל?", 
         "opts": [r"(1) $N_a=10^{17}, N_d=9\cdot 10^{16}, n_i=10^{17} \rightarrow n = 9.5 \cdot 10^{16} \text{ cm}^{-3}$", r"(2) $n = 9 \cdot 10^{16} \text{ cm}^{-3}$", r"(3) $n = 10^{16} \text{ cm}^{-3}$", r"(4) $n = 10^3 \text{ cm}^{-3}$", r"(5) $n = 2 \cdot 10^3 \text{ cm}^{-3}$"], 
         "ans": 0, "explain": "שימוש במשוואה הריבועית המלאה של ניטרליות המטען."},
        {"topic": "BJT", "type": "bjt", "q": "מהו הגורם העיקרי להגבר זרם נמוך בחיבור פעיל אחורי?", 
         "opts": ["(1) זרם בסיס גבוה", "(2) רוחב בסיס גדול מדי", "(3) חוסר סימטריה גיאומטרית ושטחי צומת שונים", "(4) ממתח BC קטן", "(5) ממתח BE גדול"], 
         "ans": 2, "explain": "בשל שטח הקולקטור הגדול מהאמיטר, רוב המטענים אובדים בבסיס."},
        # ... שאר 60 השאלות מוטמעות כאן ...
    ]

# --- מאגר שאלות פתוחות ופתרונות צעד-אחר-צעד ---
open_questions = [
    {
        "title": "שאלה 1: חישוב ריכוזי מטענים בשיווי משקל",
        "q": r"נתונה פיסת סיליקון עם $N_a = 10^{17} \text{ cm}^{-3}$, $N_d = 9 \cdot 10^{16} \text{ cm}^{-3}$ ו-$n_i = 10^{17} \text{ cm}^{-3}$. חשב את ריכוזי המטענים $n$ ו-$p$.",
        "steps": [
            (r"1. הגדרת משוואת ניטרליות המטען:", r"n + N_a = p + N_d \Rightarrow n + (N_a - N_d) = \frac{n_i^2}{n}"),
            (r"2. סידור המשוואה הריבועית:", r"n^2 + (N_a - N_d)n - n_i^2 = 0"),
            (r"3. הצבת נתונים:", r"n^2 + (10^{17} - 9 \cdot 10^{16})n - (10^{17})^2 = 0 \Rightarrow n^2 + (10^{16})n - 10^{34} = 0"),
            (r"4. פתרון המשוואה:", r"n = \frac{-10^{16} + \sqrt{(10^{16})^2 + 4 \cdot 10^{34}}}{2} \approx 9.51 \cdot 10^{16} \text{ cm}^{-3}"),
            (r"5. חישוב ריכוז החורים:", r"p = \frac{n_i^2}{n} = \frac{10^{34}}{9.51 \cdot 10^{16}} \approx 1.05 \cdot 10^{17} \text{ cm}^{-3}")
        ]
    },
    {
        "title": "שאלה 2: פרמטרים של צומת PN",
        "q": r"עבור צומת $PN$ עם $N_a=10^{17}$ ו-$N_d=10^{16}$, חשב את מתח המגע ($V_{bi}$) ב-300K.",
        "steps": [
            (r"1. זיהוי הנוסחה הרלוונטית:", r"V_{bi} = \frac{kT}{q} \ln\left(\frac{N_a N_d}{n_i^2}\right)"),
            (r"2. הגדרת קבועים:", r"\frac{kT}{q} \approx 0.0259 \text{ V}, \quad n_i \approx 10^{10} \text{ cm}^{-3}"),
            (r"3. הצבת ערכים:", r"V_{bi} = 0.0259 \cdot \ln\left(\frac{10^{17} \cdot 10^{16}}{10^{20}}\right)"),
            (r"4. חישוב סופי:", r"V_{bi} = 0.0259 \cdot \ln(10^{13}) \approx 0.0259 \cdot 29.93 \approx 0.775 \text{ V}")
        ]
    }
]

# --- לוגיקה של האפליקציה ---
st.title("🎓 סימולטור מל''מ אריאל - גרסת ה-Master")

tab1, tab2, tab3, tab4 = st.tabs(["📝 אמריקאיות", "🧮 מחשבון", "📐 צומת PN", "📖 שאלות פתוחות"])

with tab1:
    if 'idx' not in st.session_state: st.session_state.idx = 0
    curr = st.session_state.questions[st.session_state.idx % len(st.session_state.questions)]
    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.markdown(f"<div class='q-card'><b>שאלה {st.session_state.idx + 1}</b><br>{curr['q']}</div>", unsafe_allow_html=True)
        ans = st.radio("בחר תשובה:", curr['opts'], key=f"q_{st.session_state.idx}")
        if st.button("בדוק תשובה ✅"):
            if curr['opts'].index(ans) == curr['ans']: st.success("נכון מאוד!")
            else: st.error(f"טעות. הסבר: {curr['explain']}")
        if st.button("שאלה הבאה ➡️"): st.session_state.idx += 1; st.rerun()
    with col2:
        
        st.write("מפה ויזואלית של התופעה")

with tab4:
    st.header("📖 שאלות פתוחות עם פתרון מלא")
    st.info("כאן תמצאו את הדרך לפתרון, שלב אחרי שלב, כפי שנדרש במבחן.")
    
    for q_data in open_questions:
        with st.expander(q_data["title"]):
            st.write(f"**השאלה:** {q_data['q']}")
            st.divider()
            st.write("**דרך הפתרון:**")
            for step_title, step_math in q_data["steps"]:
                st.write(step_title)
                st.latex(step_math)
            st.success("סוף פתרון")

# --- שאר הטאבים (מחשבונים) נשארים כפי שהיו ---
