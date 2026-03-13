with open('plugins/query.py', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if 'text = "<b>👥 Bᴏᴛ Aᴅᴍɪɴs</b>' in lines[i]:
        lines[i] = '                text = "<b>👥 Bᴏᴛ Aᴅᴍɪɴs</b>\\n\\n"\n'
    elif '"\n' == lines[i] or '"\n' == lines[i].strip():
        lines[i] = ""

with open('plugins/query.py', 'w') as f:
    f.writelines(lines)
