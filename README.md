# はな胡哨背单词

一个帮助学习日语的在线工具，支持同音单词查找和剧本单词查询功能。

## 功能特点

1. 同音单词查找
   - 输入平假名，查找相同读音的单词
   - 显示单词的汉字写法、读音和含义

2. 剧本单词查询
   - 支持按剧集筛选
   - 显示单词在剧本中的具体出现场景
   - 包含JLPT等级信息（如果有）

## 技术栈

- Frontend: Streamlit
- Backend: Supabase
- Database: PostgreSQL
- Storage: Supabase Storage

## 本地开发

1. 克隆仓库
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用
```bash
streamlit run main.py
```

## 在线访问

访问 [Streamlit Cloud 链接] 即可使用在线版本。

## 维护说明

1. 数据库更新
   - 通过 Supabase 管理界面更新词库
   - 添加新的剧本内容

2. 功能改进
   - 提交 Issue 报告问题
   - 创建 Pull Request 贡献代码

## License

MIT License 