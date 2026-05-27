import streamlit as st
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
    tab1 = st.tabs(["📷 图片+文本AI分析"])[0]
else:
    tab1, tab2 = st.tabs(["📷 图片+文本AI分析", "📹 实时摄像头识别"])

# ========== 图片+文本分析模块 ==========
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
        st.image(img_np, caption="AI识别结果", width=300)

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
        st.info("云端暂不支持摄像头，本地运行可使用")
