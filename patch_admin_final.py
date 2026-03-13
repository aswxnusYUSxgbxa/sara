with open('plugins/query.py', 'r') as f:
    content = f.read()

import re

admin_logic = """    elif data == 'admins_menu':
        id = query.from_user.id
        if await authoUser(query, id, owner_only=True):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")
            try:
                admins = await db.get_all_admins()
                text = "<b>👥 Bᴏᴛ Aᴅᴍɪɴs</b>\\n\\n"

                if admins:
                    for idx, admin in enumerate(admins, 1):
                        text += f"<b>{idx}.</b> <code>{admin['_id']}</code>\\n"
                else:
                    text += "<i>Nᴏ ᴀᴅᴍɪɴs ᴀᴅᴅᴇᴅ ʏᴇᴛ.</i>\\n"

                text += "\\n<b>Tᴏ ᴀᴅᴅ ᴀɴ ᴀᴅᴍɪɴ, sᴇɴᴅ ᴛʜᴇ ᴜsᴇʀ ID ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ.</b>\\n<b>Tᴏ ʀᴇᴍᴏᴠᴇ ᴀɴ ᴀᴅᴍɪɴ, sᴇɴᴅ <code>/del_admin &lt;user_id&gt;</code>.</b>"

                msg = await client.ask(chat_id=id, text=text, timeout=60)

                if msg.text.startswith('/del_admin'):
                    parts = msg.text.split()
                    if len(parts) == 2 and parts[1].isdigit():
                        admin_id = int(parts[1])
                        await db.del_admin(admin_id)
                        await msg.reply(f"<b>Aᴅᴍɪɴ <code>{admin_id}</code> ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅</b>")
                    else:
                        await msg.reply("<b>❌ Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ. Tʀʏ: <code>/del_admin 12345678</code></b>")
                elif msg.text.isdigit():
                    new_admin = int(msg.text)
                    await db.add_admin(new_admin)
                    await msg.reply(f"<b>Aᴅᴍɪɴ <code>{new_admin}</code> ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅</b>")
                else:
                    await msg.reply("<b>❌ Iɴᴠᴀʟɪᴅ Iɴᴘᴜᴛ.</b>")

            except Exception as e:
                try:
                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                except BaseException:
                    pass

    elif data == 'autodel_cmd':"""

content = re.sub(r'    elif data == \'admins_menu\':\n    elif data == \'autodel_cmd\':', admin_logic, content)

with open('plugins/query.py', 'w') as f:
    f.write(content)
