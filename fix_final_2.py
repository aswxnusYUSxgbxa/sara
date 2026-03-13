with open('plugins/query.py', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if 'text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..' in lines[i] and 'disable_notification=True' not in lines[i]:
        lines[i] = '                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)\n'
        if i+1 < len(lines) and '<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)' in lines[i+1]:
            lines[i+1] = ""

with open('plugins/query.py', 'w') as f:
    f.writelines(lines)
