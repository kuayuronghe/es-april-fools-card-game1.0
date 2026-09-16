import os

folder = "."  # 当前文件夹
prefix = "image"  # 图片相对于HTML的路径前缀
code_lines = ["const IMAGES = ["]

# 遍历文件夹中的图片
for filename in sorted(os.listdir(folder)):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        name_without_ext = os.path.splitext(filename)[0]
        # 生成代码行，默认label用文件名代替，你可以后续手动改
        code_lines.append(f'  {{ label: "🎲 {name_without_ext}", img: "{prefix}/{filename}" }},')

code_lines.append("];")

# 输出到控制台
print("\n".join(code_lines))