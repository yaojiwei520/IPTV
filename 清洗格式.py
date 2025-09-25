import re


def clean_m3u_file(input_file, output_file):
    """
    清洗M3U文件：
    1. 仅保留以 #EXTINF 开头的行
    2. 移除重复的频道（基于 tvg-name 或频道名称）
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        seen_channels = set()  # 用于存储已处理的频道名称
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF"):
                # 提取 tvg-name 或频道名称（如 "CCTV-1"）
                match = re.search(r'tvg-name="([^"]+)"|,([^,\n]+)$', line)
                if match:
                    channel_name = match.group(1) or match.group(2)
                    if channel_name not in seen_channels:
                        seen_channels.add(channel_name)
                        cleaned_lines.append(line + '\n')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)

        print(f"文件清洗完成，已保存为 {output_file}")

    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")


# 使用示例
input_filename = 'tv.m3u'
output_filename = 'new.m3u'

clean_m3u_file(input_filename, output_filename)