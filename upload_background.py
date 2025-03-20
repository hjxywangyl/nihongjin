from supabase import create_client, Client
import os

# Supabase配置
url = "https://rpvjqbmkqbovgrdagznp.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJwdmpxYm1rcWJvdmdyZGFnem5wIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIzNTU5NzgsImV4cCI6MjA1NzkzMTk3OH0.EQ_Isx98jNF9oO1_5Qeyys7_YyoReCQTY4JXHHYyx1M"
supabase: Client = create_client(url, key)

# 上传图片
try:
    with open("background.jpg", "rb") as f:
        supabase.storage.from_("drama-posters").upload(
            "background.jpg",
            f,
            {"content-type": "image/jpeg"}
        )
    print("背景图片上传成功！")
except Exception as e:
    print(f"上传失败：{str(e)}") 