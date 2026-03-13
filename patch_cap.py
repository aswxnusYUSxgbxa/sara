with open('plugins/query.py', 'r') as f:
    content = f.read()

import re

# Add custom caption setting logic
set_cap_logic = """
    elif data == 'set_custom_caption':
        id = query.from_user.id
        if await authoUser(query, id):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")
            try:
                caption = await db.get_custom_caption()
                msg = await client.ask(
                    chat_id=id,
                    text=f"<b>Sᴇɴᴅ Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ. Yᴏᴜ ᴄᴀɴ ᴜsᴇ HTML ᴛᴀɢs.\nSᴇɴᴅ <code>/clear_caption</code> ᴛᴏ ʀᴇᴍᴏᴠᴇ ɪᴛ.\n\n<blockquote>Cᴜʀʀᴇɴᴛ Cᴀᴘᴛɪᴏɴ:</blockquote></b> {caption}",
                    timeout=60
                )
                if msg.text.strip() == '/clear_caption':
                    await db.set_custom_caption("")
                    await msg.reply("<b>Cᴀᴘᴛɪᴏɴ ᴄʟᴇᴀʀᴇᴅ.</b>")
                else:
                    await db.set_custom_caption(msg.text.strip())
                    await msg.reply("<b>Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ Sᴇᴛ Sᴜᴄᴄᴇssғᴜʟʟʏ ✅</b>")
            except Exception as e:
                try:
                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                except BaseException:
                    pass

    elif data == 'admins_menu':"""

content = content.replace("    elif data == 'autodel_cmd':", set_cap_logic + "\n    elif data == 'autodel_cmd':")
with open('plugins/query.py', 'w') as f:
    f.write(content)
