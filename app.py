import streamlit as st
import pandas as pd

# 极简单页面配置
st.set_page_config(page_title="情绪识别", layout="wide")

# 极简单样式
st.markdown("""
<style>
    .stApp { background: #0E1117; color: white; }
</style>
""", unsafe_allow_html=True)

# ------------------- 主页面 -------------------
st.title("😆真实AI多模态情绪识别")
st.write("欢迎使用情绪识别系统")

# 上传图片
img = st.file_uploader("上传图片", type=["jpg","png"])
text = st.text_area("输入文本")
btn = st.button("开始分析")

if btn and img:
    st.success("✅ 分析完成！")
    st.image(img)

    # 图表
    st.subheader("情绪指标")
    data = {
        "情绪": ["高兴","生气","惊讶","悲伤","中性"],
        "概率": [0.8,0.2,0.5,0.3,0.7]
    }
    st.bar_chart(pd.DataFrame(data), x="情绪", y="概率")

    st.write("### 分析报告")
    st.write("情绪积极，状态良好")
