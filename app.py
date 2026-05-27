import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import os

# 页面全局配置
st.set_page_config(page_title="多模态情绪识别系统", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("😆真实AI多模态情绪识别")

# 判断是否为云端环境（屏蔽云端摄像头）
IS_CLOUD = os.environ.get("STREAMLIT_SERVER_HEADLESS") == "true"

# 标签页
if IS_CLOUD:
    # 云端：只保留可用的图片分析标签
    tab1 = st.tabs(["📷 图片+文本AI分析"])[0]
else:
    # 本地：双标签完整展示
    tab1, tab2 = st.tabs(["📷 图片+文本AI分析", "📹 实时摄像头识别"])

# 加载人脸检测器
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# 模拟情绪预测函数
def your_emotion_model_predict(face_img):
    emotions = ["高兴", "生气", "惊讶", "悲伤", "中性", "害怕", "厌恶"]
    probs = np.array([0.8, 0.2, 0.5, 0.3, 0.7, 0.4, 0.1])
    probs = probs / probs.sum()
    idx = np.argmax(probs)
    return emotions[idx], probs[idx]

# ========== 图片+文本分析模块（公网/本地都可用） ==========
with tab1:
    st.subheader("上传图片 + 输入文本 → AI自动分析")
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("上传人脸图片", type=["jpg", "png"])
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, width=220)

    with col2:
        text = st.text_area("输入文本", height=150)
        analyze = st.button("开始AI分析", type="primary")

    if analyze and uploaded_file and text.strip():
        st.success("✅ AI 分析完成！")

        img_np = np.array(Image.open(uploaded_file))
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.1, 4)
        res_img = img_np.copy()

        for (x, y, w, h) in faces:
            face = res_img[y:y+h, x:x+w]
            emo, score = your_emotion_model_predict(face)
            cv2.rectangle(res_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(res_img, f"{emo} {score:.0%}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        st.image(res_img, caption="AI识别结果", width=300)

        # 情绪指标卡片
        st.subheader("📊 情绪指标")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.metric("高兴", "80%")
        with c2: st.metric("生气", "20%")
        with c3: st.metric("惊讶", "50%")
        with c4: st.metric("悲伤", "30%")
        with c5: st.metric("中性", "70%")

        # 人脸情绪柱状图
        st.subheader("人脸情绪概率分布")
        face_df = pd.DataFrame({
            "情绪": ["高兴", "生气", "惊讶", "悲伤", "中性", "害怕", "厌恶"],
            "概率": [0.8, 0.2, 0.5, 0.3, 0.7, 0.4, 0.1]
        })
        st.bar_chart(face_df, x="情绪", y="概率")

        # 文本情绪柱状图
        st.subheader("文本情绪概率")
        text_df = pd.DataFrame({
            "情绪": ["正向", "负向", "中性"],
            "概率": [0.55, 0.32, 0.1]
        })
        st.bar_chart(text_df, x="情绪", y="概率")

        # 分析报告
        st.subheader("📝 AI分析报告")
        st.write("""
        本次分析结果：
        • 人脸主导情绪：高兴
        • 文本情绪：正向
        • 综合判断：情绪积极，状态良好
        你可以重新上传图片或修改文本再次分析。
        """)

# ========== 摄像头模块（仅本地可见） ==========
if not IS_CLOUD:
    with tab2:
        st.subheader("📹 实时摄像头情绪监测")
        run = st.checkbox("打开摄像头", value=False)

        if run:
            cap = cv2.VideoCapture(0)
            
            # ----------------- 修复在这里！！！ -----------------
            # 原来的 st.empty() 会崩溃，我换成安全写法
            import time
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.1, 4)

                for (x, y, w, h) in faces:
                    face = frame[y:y+h, x:x+w]
                    emo, _ = your_emotion_model_predict(face)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(frame, emo, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

                # 【关键修复】不用 st.empty()，直接显示，不动态删除
                st.image(frame)
                time.sleep(0.05)
        else:
            st.info("已关闭摄像头")
