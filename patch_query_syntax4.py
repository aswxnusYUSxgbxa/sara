with open('plugins/query.py', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if 'text += f"<b>{idx}.</b> <code>{admin[\'_id\']}</code>' in lines[i]:
        lines[i] = '                        text += f"<b>{idx}.</b> <code>{admin[\'_id\']}</code>\\n"\n'
    if 'text += "<i>Nᴏ ᴀᴅᴍɪɴs ᴀᴅᴅᴇᴅ ʏᴇᴛ.</i>' in lines[i]:
        lines[i] = '                    text += "<i>Nᴏ ᴀᴅᴍɪɴs ᴀᴅᴅᴇᴅ ʏᴇᴛ.</i>\\n"\n'
    if 'text +=' in lines[i] and 'Tᴏ ᴀᴅᴅ ᴀɴ ᴀᴅᴍɪɴ' in lines[i+1]:
        lines[i] = '                text += "\\n<b>Tᴏ ᴀᴅᴅ ᴀɴ ᴀᴅᴍɪɴ, sᴇɴᴅ ᴛʜᴇ ᴜsᴇʀ ID ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ.</b>\\n<b>Tᴏ ʀᴇᴍᴏᴠᴇ ᴀɴ ᴀᴅᴍɪɴ, sᴇɴᴅ <code>/del_admin &lt;user_id&gt;</code>.</b>" \n'
        lines[i+1] = ""
        lines[i+2] = ""

with open('plugins/query.py', 'w') as f:
    f.writelines(lines)
