import streamlit as st
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="EverProfit 报告中心",
    layout="wide",
    page_icon="📈"
)

st.title("📊 EverProfit 报告中心")
st.markdown("### 每日交易分析报告")

# reports 目录
report_dir = Path("reports")

if report_dir.exists() and any(report_dir.glob("*.md")):
    md_files = sorted(list(report_dir.glob("*.md")), 
                     key=lambda x: x.stat().st_mtime, 
                     reverse=True)
    
    file_names = [f.name for f in md_files]
    selected_file = st.selectbox("选择报告", file_names)
    
    file_path = report_dir / selected_file
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    st.markdown(content, unsafe_allow_html=True)
    
    st.download_button(
        label=f"📥 下载 {selected_file}",
        data=content,
        file_name=selected_file,
        mime="text/markdown"
    )
    
    st.caption(f"更新时间: {datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
else:
    st.info("📭 reports/ 目录暂无报告文件")
    st.markdown("服务器生成新报告并 push 后，刷新此页面即可看到最新内容。")

st.sidebar.info("EverProfit 系统 · 恒盈报告查看器")
