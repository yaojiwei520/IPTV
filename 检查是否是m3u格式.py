import re

def is_valid_m3u(file_path):
    """
    检查 M3U 文件是否符合标准格式：
    1. 必须以 #EXTM3U 开头（可选，但推荐）
    2. 每个 #EXTINF 行必须包含 duration 和可选的额外属性
    3. 每个 #EXTINF 行后必须跟一个媒体链接（URL 或文件路径）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        if not lines:
            print("错误：文件为空")
            return False

        # 检查文件头（可选）
        if not lines[0].startswith("#EXTM3U"):
            print("警告：建议以 #EXTM3U 开头")

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("#EXTINF"):
                # 检查 EXTINF 格式（至少包含 duration）
                if not re.match(r'^#EXTINF:-?\d+', line):
                    print(f"错误：第 {i+1} 行 #EXTINF 格式无效（缺少 duration）")
                    return False

                # 检查下一行是否是媒体链接
                if i + 1 >= len(lines) or lines[i+1].startswith('#'):
                    print(f"错误：第 {i+1} 行 #EXTINF 后缺少媒体链接")
                    return False
                i += 1  # 跳过链接行
            elif not line.startswith("#"):
                print(f"错误：第 {i+1} 行出现未标记的媒体链接（缺少 #EXTINF）")
                return False
            i += 1

        print("文件符合 M3U 标准格式")
        return True

    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return False
    except Exception as e:
        print(f"检查文件时出错: {str(e)}")
        return False

# 使用示例
file_to_check = 'merged.m3u'
is_valid_m3u(file_to_check)