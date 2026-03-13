with open('plugins/query.py', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if 'raw_text = set_msg.text.replace' in lines[i]:
        lines[i] = "                raw_text = set_msg.text.replace('\\n', ' | ')\n"

with open('plugins/query.py', 'w') as f:
    f.writelines(lines)
