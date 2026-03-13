with open("plugins/start.py", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.strip() == 'text="<b>⚙️ Main Settings Panel:</b>':
        skip = True
        new_lines.append('        text="<b>⚙️ Main Settings Panel:</b>\\n\\nManage your bot\'s configuration from here.",\n')
    elif skip and line.strip() == "Manage your bot's configuration from here.\",":
        skip = False
    elif not skip:
        new_lines.append(line)

with open("plugins/start.py", "w") as f:
    f.writelines(new_lines)
