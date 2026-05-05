import streamlit as st
import random

# 1. ตั้งค่าหน้าเว็บให้รองรับมือถือ
st.set_page_config(page_title="เกมคณิตศาสตร์ผู้สูงวัย", page_icon="🧮", layout="centered")

# 2. ฉีด CSS เพื่อปรับขนาด UI ให้ใหญ่พิเศษ (Senior-Friendly UI)
st.markdown("""
    <style>
    /* ปรับขนาดตัวอักษรของโจทย์ */
    .big-font {
        font-size: 50px !important;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 20px;
    }
    /* ปรับขนาดตัวอักษรทั่วไป */
    div[data-testid="stMarkdownContainer"] > p {
        font-size: 24px !important;
    }
    /* ปรับขนาดช่องกรอกตัวเลข */
    input {
        font-size: 30px !important;
        height: 60px !important;
    }
    /* ปรับขนาดปุ่มให้ใหญ่และกว้างเต็มจอ */
    .stButton > button {
        width: 100%;
        height: 80px;
        font-size: 30px !important;
        font-weight: bold;
        background-color: #4CAF50;
        color: white;
        border-radius: 15px;
    }
    /* ปรับขนาดสถานะ Warning/Success/Error */
    .stAlert > div {
        font-size: 22px !important;
    }
    </style>
    """, unsafe_allow_html=True) # แก้ไขจาก stdio เป็น html

class MathEngineWeb:
    @staticmethod
    def generate_question(level):
        max_val = 10 + (level * 2) 
        ops = ['+', '-']
        if level > 5: ops.append('×') 
        
        while True:
            a = random.randint(1, max_val)
            b = random.randint(1, max_val)
            op = random.choice(ops)
            
            if op == '-':
                if a < b: a, b = b, a 
            
            display_op = op
            calc_op = op.replace('×', '*')
            
            question_str = f"{a} {display_op} {b}"
            ans = int(eval(f"{a} {calc_op} {b}"))
            return question_str, ans

# --- ส่วนจัดการ Session ---
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.q, st.session_state.ans = MathEngineWeb.generate_question(1)
    st.session_state.game_over = False

# --- หน้าจอหลัก ---
st.markdown("<h1 style='text-align: center;'>🧮 ฝึกสมองกันครับ</h1>", unsafe_allow_html=True)

if not st.session_state.game_over:
    st.write(f"### ระดับที่: {st.session_state.level}")
    st.markdown(f'<p class="big-font">{st.session_state.q} = ?</p>', unsafe_allow_html=True)

    # ใช้ Form เพื่อป้องกันโปรแกรมรีรันโดยไม่จำเป็น
    with st.form(key='math_form', clear_on_submit=True):
        user_input = st.number_input("แตะเพื่อใส่คำตอบ:", step=1, value=None, format="%d")
        submit_button = st.form_submit_button(label='ส่งคำตอบ')

        if submit_button:
            if user_input is None:
                st.warning("⚠️ โปรดใส่ตัวเลขก่อนครับ") # ป้องกัน Bug เกมจบเมื่อลืมใส่เลข[cite: 2]
            elif user_input == st.session_state.ans:
                st.balloons() 
                st.success("เก่งมากครับ! ถูกต้อง ✅")
                st.session_state.level += 1
                st.session_state.q, st.session_state.ans = MathEngineWeb.generate_question(st.session_state.level)
                st.rerun() # แสดงโจทย์ใหม่ทันที[cite: 2]
            else:
                st.session_state.game_over = True
                st.rerun()

else:
    st.error(f"❌ ตอบผิดนิดเดียวครับ")
    st.write(f"### เฉลยคือ {st.session_state.ans}")
    st.write(f"คุณทำคะแนนได้: {st.session_state.level - 1} ข้อ")
    
    if st.button("เริ่มเกมใหม่ 🔄"):
        st.session_state.level = 1
        st.session_state.game_over = False
        st.session_state.q, st.session_state.ans = MathEngineWeb.generate_question(1)
        st.rerun()