import os
import re

folder = "."  # 当前文件夹 (即 assets/audios)
prefix = "audio"  # 音频相对于HTML的根路径前缀

# 用于存储解析后的数据: { '1': {'cat': [1,2,3,4], 'dog': [1,2,3]} }
modules_data = {}

# 遍历 audios 下的子文件夹 (m1, m2, m3...)
for mod_folder in sorted(os.listdir(folder)):
    mod_path = os.path.join(folder, mod_folder)
    if os.path.isdir(mod_path) and mod_folder.startswith("m"):
        mod_num = mod_folder[1:]  # 提取数字，如 m1 -> 1
        
        # 遍历子文件夹里的音频文件
        for f in sorted(os.listdir(mod_path)):
            if f.lower().endswith('.mp3'):
                # 匹配文件名，例如 cat_1.mp3 -> cat, 1
                match = re.match(r"(\w+)_(\d+)\.mp3", f, re.IGNORECASE)
                if match:
                    label, audio_idx = match.groups()
                    if mod_num not in modules_data:
                        modules_data[mod_num] = {}
                    if label not in modules_data[mod_num]:
                        modules_data[mod_num][label] = []
                    modules_data[mod_num][label].append(int(audio_idx))

# 生成 JS 代码
js_code = "const GAME_MODULES = [\n"
for mod_num in sorted(modules_data.keys(), key=int):
    labels = modules_data[mod_num]
    total_audios = sum(len(v) for v in labels.values())
    avg_audios = total_audios // len(labels) if labels else 0
    js_code += f'  {{\n    name: "模块{mod_num} ({avg_audios}音频)",\n    audios: [\n'
    
    # 按照固定的图片顺序输出（保证和图片数组对齐）
    for label in sorted(labels.keys()):
        indexes = labels[label]
        paths = [f'"{prefix}/m{mod_num}/{label}_{idx}.mp3"' for idx in sorted(indexes)]
        js_code += f'      [{", ".join(paths)}],\n'
        
    js_code += '    ]\n  },\n'
js_code += "];"

print(js_code)