import streamlit as st
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="EverProfit 报告中心", layout="wide", page_icon="📈")

st.title("📊 EverProfit 报告中心")
st.markdown("### 历史交易分析报告")

report_dir = Path("reports")

if report_dir.exists() and any(report_dir.glob("*.md")):
    # 获取所有报告并按时间倒序排序
    md_files = sorted(list(report_dir.glob("*.md")), 
                     key=lambda x: x.stat().st_mtime, 
                     reverse=True)
    
    # 分组显示：最近7天 + 更早
    st.subheader("📅 最近报告")
    recent_files = md_files[:10]  # 前10个作为最近报告
    file_names = [f.name for f in recent_files]
    selected_file = st.selectbox("选择报告（最新在前）", file_names, key="recent")
    
    # 显示完整列表（可选展开）
    with st.expander("📚 查看全部历史报告"):
        all_file_names = [f.name for f in md_files]
        selected_all = st.selectbox("全部历史报告", all_file_names, key="all")
        if selected_all != selected_file:
            selected_file = selected_all
    
    # 显示选中的报告
    file_path = report_dir / selected_file
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    st.markdown("---")
    st.markdown(content, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            label=f"📥 下载 {selected_file}",
            data=content,
            file_name=selected_file,
            mime="text/markdown"
        )
    
    st.caption(f"文件更新时间: {datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    
else:
    st.info("📭 reports/ 目录暂无报告文件")
    st.markdown("当服务器生成新报告并 push 到 GitHub 后，刷新页面即可看到。")

st.sidebar.info("EverProfit 系统 · 恒盈报告查看器")
