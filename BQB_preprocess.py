import os
import re
from pathlib import Path

def rename_images_in_folder(folder_path):
    """
    重命名指定文件夹下的图片，删除文件名中第一个出现的连续四位或以上数字
    """
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    
    folder = Path(folder_path)
    if not folder.exists():
        print(f"文件夹不存在: {folder_path}")
        return
    
    # 正则表达式：匹配第一个连续四位或以上数字
    pattern = r'\d{4,}'
    
    renamed_count = 0
    
    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            old_name = file_path.name
            name_without_ext = file_path.stem
            extension = file_path.suffix
            
            # 检查是否匹配模式
            if re.search(pattern, name_without_ext):
                # 删除第一个连续四位或以上的数字
                new_name_without_ext = re.sub(pattern, '', name_without_ext, count=1)
                new_name = new_name_without_ext + extension
                new_path = file_path.parent / new_name
                
                # 避免文件名冲突
                counter = 1
                while new_path.exists():
                    new_name = f"{new_name_without_ext}_{counter}{extension}"
                    new_path = file_path.parent / new_name
                    counter += 1
                
                try:
                    file_path.rename(new_path)
                    print(f"重命名: {old_name} -> {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"重命名失败 {old_name}: {e}")
    
    print(f"完成！共重命名了 {renamed_count} 个文件")

def main():
    """
    主函数，处理多个文件夹
    """
    # 在这里指定要处理的文件夹路径
    folders = [
        r"./原神_BQB",
        r"./那年那兔那些事_BQB"
        # 添加更多文件夹路径
        # r"C:\path\to\another\folder",
    ]
    
    for folder in folders:
        print(f"\n处理文件夹: {folder}")
        rename_images_in_folder(folder)

if __name__ == "__main__":
    main()
