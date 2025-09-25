import re
from collections import defaultdict
from datetime import datetime


def process_m3u_files(new_file, update_file):
    """
    严格按指定格式输出的处理流程：
    1. 保留原始#EXTINF行的完整属性
    2. 精确匹配tvg-name并添加对应.m3u8链接
    3. 确保输出格式完全符合要求
    """
    try:
        # 生成带时间戳的输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"iptv_{timestamp}.m3u"

        # 从update.m3u提取有效数据（以tvg-name为键）
        update_urls = {}
        with open(update_file, 'r', encoding='utf-8') as f:
            current_name = None
            for line in f:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    # 精确提取tvg-name
                    match = re.search(r'tvg-name="([^"]+)"', line)
                    if match:
                        current_name = match.group(1)
                elif line.endswith('.m3u8') and current_name:
                    update_urls[current_name] = line
                    current_name = None

        # 处理new.m3u并生成输出文件
        matched_count = 0
        with open(new_file, 'r', encoding='utf-8') as f_in, \
                open(output_file, 'w', encoding='utf-8') as f_out:

            # 写入标准M3U文件头
            f_out.write("#EXTM3U\n")

            for line in f_in:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    # 提取当前行的tvg-name
                    match = re.search(r'tvg-name="([^"]+)"', line)
                    if match and match.group(1) in update_urls:
                        # 保留原始EXTINF行（包含所有属性）
                        f_out.write(f"{line}\n")
                        # 添加对应的.m3u8链接
                        f_out.write(f"{update_urls[match.group(1)]}\n")
                        matched_count += 1

        # 输出统计信息
        print(f"处理完成！文件已保存为: {output_file}")
        print(f"成功匹配并输出: {matched_count} 个频道")
        print("\n示例输出格式验证:")
        print("#EXTINF:-1 tvg-name=\"CCTV3\" tvg-logo=\"...\" group-title=\"📺央视频道\",CCTV-3")
        print("http://example.com/cctv3.m3u8")

    except FileNotFoundError as e:
        print(f"错误：找不到文件 {e.filename}")
    except Exception as e:
        print(f"处理出错: {str(e)}")


# 使用示例
process_m3u_files(
    new_file='new.m3u',
    update_file='update2.m3u'
)