import streamlit as st
from supabase import create_client, Client
import traceback
import os
import requests
from io import BytesIO

# Supabase 配置
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    
    if not supabase_url or not supabase_key:
        st.error("错误：未找到 Supabase 配置。")
        st.stop()
        
    # 初始化 Supabase 客户端
    supabase = create_client(supabase_url, supabase_key)
    
    # 测试连接
    test = supabase.table('japanese_vocabulary').select("*").limit(1).execute()
    
except Exception as e:
    st.error("数据库连接错误")
    st.error(f"错误详情：{str(e)}")
    st.stop()

# 检查数据库连接
try:
    # 测试字典连接
    data = supabase.table('japanese_vocabulary').select("*").limit(5).execute()
    print("✅ 字典连接成功！")
except Exception as e:
    print(f"❌ 字典连接失败：{str(e)}")
    print("详细错误信息：")
    print(traceback.format_exc())

try:
    # 测试剧本表连接
    drama_check = supabase.table("drama_subtitles").select("*").limit(1).execute()
    print(f"✅ 剧本表连接成功！({'有' if drama_check.data else '无'}数据)")
except Exception as e:
    print(f"❌ 剧本表连接失败：{str(e)}")
    print("详细错误信息：")
    print(traceback.format_exc())

# 设置页面主题
st.set_page_config(
    page_title="はな胡哨背单词",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# 自定义CSS样式
st.markdown("""
    <style>
    /* 全局样式 */
    .stApp {
        background-color: #000000;
        background-image: url('https://rpvjqbmkqbovgrdagznp.supabase.co/storage/v1/object/public/drama-posters/chongqirensheng/6a7346a1e0398c34cf462091b1383024.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #1a1f36;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* 页面内容居中 */
    .main > div {
        max-width: 1000px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        margin: 0 auto !important;
    }
    
    /* 主标题样式 */
    .big-font {
        font-size: 3em !important;
        color: #1d1d21;
        font-weight: 700;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    /* 副标题样式 */
    .medium-font {
        font-size: 1.1em !important;
        color: #1d1d21;
        font-weight: 500;
        letter-spacing: -0.01em;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        padding: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #232323;
        font-weight: 300;
        font-size: 0.95em;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 4px;
        min-width: 150px;
        text-align: center;
    }
    
    .stTabs [aria-selected="true"] {
        color: #232323 !important;
        font-weight: 700 !important;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 4px;
        padding: 0.5rem 1rem;
        min-width: 150px;
    }
    
    /* 移除标签页容器的边框 */
    .stTabs > div {
        border: none !important;
    }
    
    /* 移除标签页内容区域的边框 */
    .stTabs [role="tabpanel"] {
        border: none !important;
    }
    
    /* 按钮样式 */
    .stButton>button {
        background-color: #635bff;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 0.95em;
        transition: all 0.2s ease;
        text-transform: none;
        letter-spacing: 0;
    }
    
    .stButton>button:hover {
        background-color: #4f46e5;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 91, 255, 0.2);
    }
    
    /* 输入框样式 */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(83, 108, 204, 0.2);
        color: #232323;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        font-size: 0.95em;
        transition: all 0.2s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: rgba(255, 255, 255, 0.4);
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
    }
    
    /* 输入框标签样式 */
    .stTextInput>label {
        color: #232323 !important;
    }
    
    /* 表格样式 */
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 6px !important;
        padding: 1rem !important;
        color: #ffffff !important;
    }
    
    /* 表格容器样式 */
    .stDataFrame > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 6px !important;
        padding: 1rem !important;
    }
    
    /* 表格内容样式 */
    .stDataFrame > div > div {
        background-color: transparent !important;
    }
    
    /* 表格行样式 */
    .stDataFrame > div > div > div > div {
        border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* 表格最后一行样式 */
    .stDataFrame > div > div > div > div:last-child {
        border-bottom: none !important;
    }
    
    /* 表格单元格样式 */
    .stDataFrame > div > div > div > div > div {
        padding: 0.75rem 1rem !important;
        color: #ffffff !important;
        border: none !important;
    }
    
    /* 表格头部样式 */
    .stDataFrame > div > div > div:first-child > div > div {
        background-color: rgba(255, 39, 92, 0.9) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 0.75rem 1rem !important;
        border: none !important;
    }
    
    /* 隐藏序号列 */
    .stDataFrame > div > div > div > div > div:first-child {
        display: none !important;
    }
    
    /* 表格行悬停效果 */
    .stDataFrame > div > div > div > div:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* 强制移除所有竖线 */
    .stDataFrame * {
        border-right: none !important;
    }
    
    /* 强制移除表格边框 */
    .stDataFrame > div > div > div > div > div {
        border: none !important;
    }
    
    /* 强制移除表格容器边框 */
    .stDataFrame > div {
        border: none !important;
    }
    
    /* 强制移除表格内容边框 */
    .stDataFrame > div > div {
        border: none !important;
    }
    
    /* 成功消息样式 */
    .stSuccess {
        background-color: rgba(95, 98, 202, 0.1);
        color: #1f2747;
        padding: 1rem;
        border-radius: 6px;
    }
    
    /* 警告消息样式 */
    .stWarning {
        background-color: rgba(95, 98, 202, 0.1);
        color: #1f2747;
        padding: 1rem;
        border-radius: 6px;
    }
    
    /* 错误消息样式 */
    .stError {
        background-color: rgba(95, 98, 202, 0.1);
        color: #1f2747;
        padding: 1rem;
        border-radius: 6px;
    }
    
    /* 卡片样式 */
    .stContainer {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 6px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e6e8eb;
        transition: all 0.2s ease;
    }
    
    .stContainer:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* 分隔线样式 */
    hr {
        border: none;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1.5rem 0;
    }
    
    /* 链接样式 */
    a {
        color: #635bff;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: #4f46e5;
        text-decoration: none;
    }
    
    /* 选择框样式 */
    .stSelectbox>div>div>select {
        background-color: rgba(255, 255, 255, 0.9);
        color: #1a1f36;
        border: 1px solid #e6e8eb;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        font-size: 0.95em;
        transition: all 0.2s ease;
    }
    
    .stSelectbox>div>div>select:focus {
        border-color: #635bff;
        box-shadow: 0 0 0 3px rgba(99, 91, 255, 0.1);
    }
    
    /* 展开面板样式 */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.9);
        color: #1a1f36;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e6e8eb;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #ffffff;
    }
    
    /* 代码块样式 */
    .stCodeBlock {
        background-color: rgba(248, 250, 252, 0.9);
        border-radius: 6px;
        padding: 1rem;
        color: #1a1f36;
        border: 1px solid #e6e8eb;
    }
    
    /* 图片容器样式 */
    .stImage {
        border-radius: 6px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* 移动端优化 */
    @media (max-width: 768px) {
        .big-font {
            font-size: 2em !important;
        }
        .medium-font {
            font-size: 1em !important;
        }
        .stButton>button {
            width: 100%;
            margin: 0.5rem 0;
        }
        .sttable {
            font-size: 0.9em;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        .stTabs [aria-selected="true"] {
            padding: 0.3rem 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 设置海报路径
POSTER_DIR = "/Users/qiao/Downloads/chongqirensheng"
POSTER_FILENAME = "BRUSH_UP_LIFE_POSTER.JPG"
POSTER_BUCKET = "drama-posters"

# === 界面模块 ===
def main():
    st.markdown('<p class="big-font">🌸はな胡哨背单词</p>', unsafe_allow_html=True)
    
    # 创建两个标签页
    tab1, tab2 = st.tabs(["🎴 同音单词查找", "🎬 剧本单词查询"])
    
    # === 1. 同音汉字查找功能 ===
    with tab1:
        search_kana = st.text_input("🔍 输入平假名查找同音单词：", key="kana_search").strip()

        if search_kana:
            st.write(f"搜索词：'{search_kana}'")
            
            try:
                # 先尝试精确匹配
                response = supabase.table("japanese_vocabulary").select("expression", "reading", "meaning").eq("reading", search_kana).execute()
                results = response.data
                
                # 如果精确匹配没结果，尝试模糊匹配
                if not results:
                    response = supabase.table("japanese_vocabulary").select("expression", "reading", "meaning").ilike("reading", f"%{search_kana}%").execute()
                    results = response.data
                
            except Exception as e:
                st.error(f"查询失败：{str(e)}")
                st.error("详细错误信息：")
                st.code(traceback.format_exc())
                results = []

            if results:
                st.markdown(f"""
                    <div class="stSuccess">
                        找到 {len(results)} 条同音词：
                    </div>
                """, unsafe_allow_html=True)
                
                # 使用卡片式布局显示结果
                for result in results:
                    st.markdown("""
                        <style>
                        .word-card {
                            background-color: rgba(255, 255, 255, 0.3);
                            border-radius: 6px;
                            padding: 1rem;
                            margin: 0.5rem 0;
                            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                        }
                        .word-card-header {
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            margin-bottom: 0.5rem;
                            color: #232323;
                        }
                        .word-card-content {
                            color: #232323;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="word-card">
                            <div class="word-card-header">
                                <strong>{result['expression']}</strong>
                                <span>{result['reading']}</span>
                            </div>
                            <div class="word-card-content">
                                {result['meaning']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                # 同音汉字查找功能中的警告
                st.markdown("""
                    <div class="stWarning">
                        ⚠️ 未找到相关同音单词
                    </div>
                """, unsafe_allow_html=True)
    
    # === 2. 剧本单词查询功能 ===
    with tab2:
        # 获取所有可用的剧集
        drama_titles = ["所有剧集"]
        try:
            dramas_response = supabase.table("drama_subtitles").select("drama_title").execute()
            if dramas_response.data:
                unique_dramas = list(set([drama['drama_title'] for drama in dramas_response.data]))
                drama_titles.extend(unique_dramas)
        except Exception as e:
            st.error(f"获取剧集列表失败：{str(e)}")
            st.error("详细错误信息：")
            st.code(traceback.format_exc())
        
        selected_drama = st.selectbox("选择剧集", drama_titles)
        
        search_word = st.text_input("🔍 输入日语单词进行查询：", key="script_search").strip()
        
        if search_word:
            st.write(f"搜索词：'{search_word}'")
            
            try:
                # 查询单词释义
                vocab_response = supabase.table("japanese_vocabulary").select("*").ilike("expression", f"%{search_word}%").execute()
                vocab_results = vocab_response.data
                
                # 如果按表达式没找到，再尝试按读音查找
                if not vocab_results:
                    vocab_response = supabase.table("japanese_vocabulary").select("*").ilike("reading", f"%{search_word}%").execute()
                    vocab_results = vocab_response.data
                
                # 查询剧本中的出现情况
                if selected_drama == "所有剧集":
                    script_response = supabase.table("drama_subtitles").select("*").ilike("content", f"%{search_word}%").execute()
                else:
                    script_response = supabase.table("drama_subtitles").select("*").eq("drama_title", selected_drama).ilike("content", f"%{search_word}%").execute()
                
                script_results = script_response.data
                
                # 显示单词释义
                if vocab_results:
                    st.subheader("📚 单词释义")
                    for result in vocab_results:
                        with st.expander(f"{result.get('expression', '')} 「{result.get('reading', '')}」"):
                            st.write(f"**意思**：{result.get('meaning', '未提供')}")
                            if 'jlpt_level' in result and result['jlpt_level']:
                                st.write(f"**JLPT等级**：N{result.get('jlpt_level', '')}")
                else:
                    # 单词释义未找到的警告
                    st.markdown("""
                        <div class="stWarning">
                            ⚠️ 未找到该单词的释义
                        </div>
                    """, unsafe_allow_html=True)
                
                # 显示剧本中的出现情况
                if script_results:
                    st.subheader("🎬 剧本中的出现")
                    st.markdown(f"""
                        <div class="stSuccess">
                            在剧本中找到 {len(script_results)} 处相关内容
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # 按剧集和集数排序
                    script_results.sort(key=lambda x: (x.get('drama_title', ''), x.get('episode', 0)))
                    
                    # 按剧集分组显示结果
                    current_drama = None
                    for result in script_results:
                        drama = result.get('drama_title', '未知剧集')
                        episode = result.get('episode', '未知集数')
                        character = result.get('character', '未知角色')
                        content = result.get('content', '')
                        start_time = result.get('start_time', '')
                        end_time = result.get('end_time', '')
                        
                        # 如果是新剧集，显示剧集信息
                        if drama != current_drama:
                            st.markdown(f"### {drama}")
                            # 显示剧集海报
                            poster_data = get_poster_from_storage(drama)
                            if poster_data:
                                st.image(poster_data, width=200)
                            else:
                                st.warning("⚠️ 无法加载海报图片")
                            current_drama = drama
                        
                        # 高亮显示搜索词
                        highlighted_content = content.replace(search_word, f"**{search_word}**")
                        
                        # 创建卡片式布局
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.markdown(f"**第{episode}集**")
                                st.markdown(f"*{start_time} → {end_time}*")
                                st.markdown(f"*{character}*")
                            with col2:
                                st.markdown(highlighted_content)
                            st.markdown("---")
                else:
                    # 剧本中未找到的警告
                    st.markdown("""
                        <div class="stWarning">
                            ⚠️ 在剧本中未找到该单词
                        </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"查询失败：{str(e)}")
                st.error("详细错误信息：")
                st.code(traceback.format_exc())

def get_poster_from_storage(drama_title):
    """从 Supabase Storage 获取海报"""
    try:
        # 构建海报文件名，使用英文文件夹名
        folder_name = "chongqirensheng"  # 使用英文文件夹名
        poster_path = f"{folder_name}/{POSTER_FILENAME}"
        
        print(f"尝试获取海报: {poster_path}")  # 调试信息
        
        # 获取海报文件的公共URL
        poster_url = supabase.storage.from_(POSTER_BUCKET).get_public_url(poster_path)
        print(f"海报URL: {poster_url}")  # 调试信息
        
        # 下载海报图片
        response = requests.get(poster_url)
        print(f"下载状态码: {response.status_code}")  # 调试信息
        
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            print(f"下载失败: {response.text}")  # 调试信息
            return None
    except Exception as e:
        print(f"获取海报时出错: {str(e)}")  # 调试信息
        print("详细错误信息：")
        print(traceback.format_exc())  # 打印完整的错误堆栈
        return None

if __name__ == "__main__":
    main()