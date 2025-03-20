from supabase import create_client, Client
import pandas as pd

# Supabase 连接信息
url = "https://rpvjqbmkqbovgrdagznp.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJwdmpxYm1rcWJvdmdyZGFnem5wIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIzNTU5NzgsImV4cCI6MjA1NzkzMTk3OH0.EQ_Isx98jNF9oO1_5Qeyys7_YyoReCQTY4JXHHYyx1M"
supabase: Client = create_client(url, key)

# 文件路径和对应的JLPT等级
files = {
    '/Users/qiao/Downloads/n1.csv': 1,
    '/Users/qiao/Downloads/n2.csv': 2,
    '/Users/qiao/Downloads/n3.csv': 3,
    '/Users/qiao/Downloads/n4.csv': 4,
    '/Users/qiao/Downloads/n5.csv': 5
}

# 清空现有数据
supabase.table('japanese_vocabulary').delete().neq('id', 0).execute()
print("已清空现有词汇数据")

# 导入所有文件
for file_path, level in files.items():
    try:
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 准备数据
        vocabulary_data = []
        for _, row in df.iterrows():
            vocabulary_data.append({
                'expression': row['expression'],
                'reading': row['reading'],
                'meaning': row['meaning'],
                'jlpt_level': level
            })
        
        # 批量插入数据
        if vocabulary_data:
            result = supabase.table('japanese_vocabulary').insert(vocabulary_data).execute()
            print(f"成功导入 {len(vocabulary_data)} 条 N{level} 词汇数据")
        else:
            print(f"没有找到要导入的 N{level} 词汇数据")
            
    except Exception as e:
        print(f"导入 N{level} 词汇时出错：{str(e)}")

print("\n✅ 所有词汇数据导入完成！") 