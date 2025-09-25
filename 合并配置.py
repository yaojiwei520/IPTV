import re

def merge_m3u_files(new_file, update_file, output_file):
    """
    合并 new.m3u 和 update.m3u：
    1. 从 update.m3u 提取 tvg-name 和对应的 .m3u8 链接
    2. 根据 tvg-name 匹配 new.m3u 的行
    3. 仅保留匹配到的频道，并在其下方插入 .m3u8 链接
    """
    try:
        # 从 update.m3u 提取 (tvg-name, url) 对
        update_data = {}
        with open(update_file, 'r', encoding='utf-8') as f:
            current_name = None
            for line in f:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    # 提取 tvg-name（兼容带引号和不带引号）
                    match = re.search(r'tvg-name="([^"]+)"|,([^,\n]+)$', line)
                    if match:
                        current_name = match.group(1) or match.group(2)
                elif line.endswith('.m3u8') and current_name:
                    update_data[current_name] = line
                    current_name = None

        # 读取 new.m3u 并仅保留匹配到的频道
        merged_lines = []
        with open(new_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("#EXTINF"):
                # 提取当前行的 tvg-name
                match = re.search(r'tvg-name="([^"]+)"|,([^,\n]+)$', line)
                if match:
                    current_name = match.group(1) or match.group(2)
                    if current_name in update_data:
                        merged_lines.append(line + '\n')
                        merged_lines.append(update_data[current_name] + '\n')
                        i += 1  # 跳过可能的原链接行
            i += 1

        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(merged_lines)

        print(f"文件合并完成，已保存为 {output_file}")

    except FileNotFoundError as e:
        print(f"错误：找不到文件 {e.filename}")
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")

# 使用示例
new_filename = 'new.m3u'
update_filename = 'update.m3u'
output_filename = 'merged.m3u'

merge_m3u_files(new_filename, update_filename, output_filename)