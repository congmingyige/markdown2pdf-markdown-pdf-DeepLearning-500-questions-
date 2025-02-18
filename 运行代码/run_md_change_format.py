import os

def replace_strings_in_file(file_path, replacements):
    """替换文件中指定字符串并记录替换的位置"""
    modified = False
    occurrences = []
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 遍历每行进行替换
    new_lines = []
    for line_num, line in enumerate(lines, 1):
        new_line = line
        for search_string, replace_string in replacements.items():
            index = new_line.find(search_string)
            while index != -1:
                # 记录替换位置
                occurrences.append((line_num, index, search_string, replace_string))
                # 进行字符串替换
                new_line = new_line[:index] + replace_string + new_line[index + len(search_string):]
                # 查找后续出现的位置
                index = new_line.find(search_string, index + len(replace_string))
        # 保存修改后的行
        if new_line != line:
            modified = True
        new_lines.append(new_line)

    # 如果文件有修改，则重写文件
    if modified:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

    return occurrences

def replace_strings_in_directory(directory, replacements):
    """递归遍历文件夹，查找和替换所有 Markdown 文件中的指定字符串"""
    all_occurrences = {}

    # 遍历文件夹及子文件夹
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                occurrences = replace_strings_in_file(file_path, replacements)
                if occurrences:
                    all_occurrences[file_path] = occurrences

    return all_occurrences

def print_replacement_occurrences(occurrences):
    """输出所有修改的位置"""
    for file_path, positions in occurrences.items():
        print(f"\nFile: {file_path}")
        for line_num, col_num, old_string, new_string in positions:
            print(f"  Line {line_num}, Column {col_num}: '{old_string}' -> '{new_string}'")

if __name__ == "__main__":
    # 输入要搜索的文件夹路径
    directory = input("请输入要搜索的文件夹路径: ")

    # 替换规则
    replacements = {
        r'\begin{eqnarray}': r'\begin{equation}\begin{aligned}',
        r'\end{eqnarray}': r'\end{aligned}\end{equation}',
        '`$': '$',
        '$`': '$'
    }

    # 执行替换并记录修改位置
    occurrences = replace_strings_in_directory(directory, replacements)

    # 输出所有替换的地方
    if occurrences:
        print_replacement_occurrences(occurrences)
    else:
        print("No replacements made.")
