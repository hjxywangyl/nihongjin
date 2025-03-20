import os
from supabase import create_client, Client
import re
from datetime import datetime

# === 初始化 Supabase ===
url = "https://rpvjqbmkqbovgrdagznp.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJwdmpxYm1rcWJvdmdyZGFnem5wIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIzNTU5NzgsImV4cCI6MjA1NzkzMTk3OH0.EQ_Isx98jNF9oO1_5Qeyys7_YyoReCQTY4JXHHYyx1M"
supabase: Client = create_client(url, key)

def parse_srt_file(file_path):
    """解析SRT文件，返回字幕列表"""
    print(f"\n开始解析文件: {file_path}")
    subtitles = []
    current_subtitle = {}
    line_number = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print(f"成功读取文件，共 {len(lines)} 行")
            
        for line in lines:
            line_number += 1
            line = line.strip()
            
            # 跳过空行
            if not line:
                if current_subtitle:
                    # 检查字幕条目是否完整
                    required_fields = ['index', 'start_time', 'end_time', 'content']
                    missing_fields = [field for field in required_fields if field not in current_subtitle]
                    if missing_fields:
                        print(f"警告：第 {line_number} 行附近发现不完整的字幕条目，缺少字段：{missing_fields}")
                        print(f"当前字幕内容：{current_subtitle}")
                    else:
                        subtitles.append(current_subtitle)
                    current_subtitle = {}
                continue
                
            # 如果是数字（字幕序号）
            if line.isdigit():
                if current_subtitle:
                    # 检查字幕条目是否完整
                    required_fields = ['index', 'start_time', 'end_time', 'content']
                    missing_fields = [field for field in required_fields if field not in current_subtitle]
                    if missing_fields:
                        print(f"警告：第 {line_number} 行附近发现不完整的字幕条目，缺少字段：{missing_fields}")
                        print(f"当前字幕内容：{current_subtitle}")
                    else:
                        subtitles.append(current_subtitle)
                current_subtitle = {'index': int(line)}
                continue
                
            # 如果是时间戳
            if '-->' in line:
                start_time, end_time = line.split(' --> ')
                current_subtitle['start_time'] = start_time
                current_subtitle['end_time'] = end_time
                continue
                
            # 如果是角色和台词
            if line.startswith('('):
                # 提取角色名
                character_match = re.match(r'\((.*?)\)', line)
                if character_match:
                    current_subtitle['character'] = character_match.group(1)
                    # 提取台词（去掉角色名部分）
                    current_subtitle['content'] = line[line.find(')')+1:].strip()
            else:
                # 如果是纯台词
                if 'content' in current_subtitle:
                    current_subtitle['content'] += ' ' + line
                else:
                    current_subtitle['content'] = line
        
        # 添加最后一个字幕
        if current_subtitle:
            # 检查字幕条目是否完整
            required_fields = ['index', 'start_time', 'end_time', 'content']
            missing_fields = [field for field in required_fields if field not in current_subtitle]
            if missing_fields:
                print(f"警告：文件末尾发现不完整的字幕条目，缺少字段：{missing_fields}")
                print(f"当前字幕内容：{current_subtitle}")
            else:
                subtitles.append(current_subtitle)
        
        print(f"成功解析 {len(subtitles)} 条字幕")
        return subtitles
    except Exception as e:
        print(f"解析文件时出错: {str(e)}")
        print(f"错误发生在第 {line_number} 行")
        raise

def import_srt_to_supabase(drama_title, episode_number, subtitles):
    """将字幕数据导入到Supabase"""
    try:
        print(f"\n开始导入第{episode_number}集到Supabase...")
        
        # 清除该集数的现有数据
        print("清除现有数据...")
        delete_response = supabase.table("drama_subtitles").delete().eq("drama_title", drama_title).eq("episode", episode_number).execute()
        print(f"删除响应: {delete_response}")
        
        # 准备要插入的数据
        data = []
        for subtitle in subtitles:
            # 确保所有必需字段都存在
            if not all(key in subtitle for key in ['index', 'start_time', 'end_time', 'content']):
                print(f"警告：跳过不完整的字幕条目：{subtitle}")
                continue
                
            data.append({
                "drama_title": drama_title,
                "episode": episode_number,
                "subtitle_index": subtitle['index'],
                "start_time": subtitle['start_time'],
                "end_time": subtitle['end_time'],
                "character": subtitle.get('character', ''),
                "content": subtitle['content']
            })
        
        if not data:
            print("错误：没有有效的字幕数据可以导入")
            return False
            
        print(f"准备插入 {len(data)} 条数据...")
        
        # 批量插入数据
        response = supabase.table("drama_subtitles").insert(data).execute()
        print(f"插入响应: {response}")
        
        # 验证插入是否成功
        verify_response = supabase.table("drama_subtitles").select("*").eq("drama_title", drama_title).eq("episode", episode_number).execute()
        print(f"验证查询结果: {len(verify_response.data)} 条记录")
        
        print(f"成功导入第{episode_number}集，共{len(data)}条字幕")
        return True
    except Exception as e:
        print(f"导入失败：{str(e)}")
        print("详细错误信息：")
        import traceback
        print(traceback.format_exc())
        return False

def extract_episode_number(filename):
    """从文件名中提取集数"""
    # 匹配 EP01 或 EP1 格式
    episode_match = re.search(r'EP(\d+)', filename, re.IGNORECASE)
    if episode_match:
        return int(episode_match.group(1))
    return None

def main():
    print("=== 字幕导入程序 ===")
    
    # 获取用户输入的剧集名称
    drama_title = input("请输入剧集名称（例如：重启人生）：").strip()
    if not drama_title:
        print("错误：剧集名称不能为空")
        return

    # 获取SRT文件目录
    srt_dir = input("请输入SRT文件所在目录路径（例如：/Users/qiao/Downloads/chongqirensheng）：").strip()
    if not os.path.exists(srt_dir):
        print(f"错误：目录 '{srt_dir}' 不存在")
        return
    
    print(f"\n正在扫描目录: {srt_dir}")
    
    # 遍历目录中的所有srt文件
    srt_files = [f for f in os.listdir(srt_dir) if f.endswith('.srt')]
    if not srt_files:
        print(f"错误：在目录 '{srt_dir}' 中没有找到SRT文件")
        return

    print(f"\n找到以下SRT文件：")
    for i, filename in enumerate(srt_files, 1):
        episode = extract_episode_number(filename)
        episode_info = f" (第{episode}集)" if episode else " (无法识别集数)"
        print(f"{i}. {filename}{episode_info}")
    
    # 确认是否继续
    confirm = input("\n是否继续导入？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消导入")
        return

    # 处理每个SRT文件
    for filename in srt_files:
        episode_number = extract_episode_number(filename)
        if episode_number:
            file_path = os.path.join(srt_dir, filename)
            
            print(f"\n正在处理第{episode_number}集...")
            try:
                subtitles = parse_srt_file(file_path)
                if import_srt_to_supabase(drama_title, episode_number, subtitles):
                    print(f"第{episode_number}集导入成功！")
                else:
                    print(f"第{episode_number}集导入失败！")
            except Exception as e:
                print(f"处理第{episode_number}集时出错: {str(e)}")
        else:
            print(f"警告：无法从文件名 '{filename}' 中提取集数，已跳过")

if __name__ == "__main__":
    main() 