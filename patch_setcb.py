with open('plugins/query.py', 'r') as f:
    content = f.read()

import re

old_setcb_start = """    elif data == "setcb":
        id = query.from_user.id
        if await authoUser(query, id):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                button_name, button_link, button_name2, button_link2 = await db.get_channel_button_links()"""

new_setcb_start = """    elif data == "setcb":
        id = query.from_user.id
        if await authoUser(query, id):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                buttons_data = await db.get_channel_button_links()"""

content = content.replace(old_setcb_start, new_setcb_start)

# We need to rewrite the entire setcb block until autodel_cmd
setcb_pattern = r'elif data == "setcb":.*?elif data == \'autodel_cmd\':'

new_setcb_block = """elif data == "setcb":
        id = query.from_user.id
        if await authoUser(query, id):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                buttons_data = await db.get_channel_button_links()

                # Create preview with existing buttons
                button_preview = []
                for btn in buttons_data:
                    button_preview.append([InlineKeyboardButton(text=btn['name'], url=btn['link'])])

                example_text = (
                    '<b>Tᴏ sᴇᴛ ᴛʜᴇ ʙᴜᴛᴛᴏɴ(s), Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛs ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ. Yᴏᴜ ᴄᴀɴ sᴇᴛ ᴜᴘ ᴛᴏ 5 ʙᴜᴛᴛᴏɴs.\n\n'
                    '<b>Sᴇᴘᴀʀᴀᴛᴇ ʙᴜᴛᴛᴏɴs ᴡɪᴛʜ | ᴏʀ ɴᴇᴡʟɪɴᴇs.</b>\n'
                    '<blockquote><code>Join Channel - https://t.me/btth480p | Support - https://t.me/support</code></blockquote>\n\n'
                    '<i>Sᴇɴᴅ /clear_buttons ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀʟʟ ʙᴜᴛᴛᴏɴs.</i>\n\n'
                    '<i>Bᴇʟᴏᴡ ɪs ᴄᴜʀʀᴇɴᴛ ʙᴜᴛᴛᴏɴ(s) Pʀᴇᴠɪᴇᴡ ⬇️</i></b>'
                )

                set_msg = await client.ask(
                    chat_id=id,
                    text=example_text,
                    timeout=60,
                    reply_markup=InlineKeyboardMarkup(button_preview) if button_preview else None,
                    disable_web_page_preview=True
                )

                if set_msg.text.strip() == '/clear_buttons':
                    await db.set_channel_button_links([])
                    return await set_msg.reply("<b>All buttons have been cleared.</b>")

                # Parse up to 5 buttons
                raw_text = set_msg.text.replace('\\n', ' | ')
                parts = raw_text.split('|')

                new_buttons = []
                for p in parts:
                    p = p.strip()
                    if not p:
                        continue
                    if ' - ' in p:
                        name, link = p.split(' - ', 1)
                        new_buttons.append({'name': name.strip(), 'link': link.strip()})

                if not new_buttons:
                    markup = [[InlineKeyboardButton(f'◈ Sᴇᴛ Cʜᴀɴɴᴇʟ Bᴜᴛᴛᴏɴ ➪', callback_data='setcb')]]
                    return await set_msg.reply(
                        "<b>Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛs. Fᴏʀᴍᴀᴛ: Nᴀᴍᴇ - Lɪɴᴋ</b>",
                        reply_markup=InlineKeyboardMarkup(markup)
                    )

                if len(new_buttons) > 5:
                    new_buttons = new_buttons[:5]

                button_preview = []
                for btn in new_buttons:
                    button_preview.append([InlineKeyboardButton(text=btn['name'], url=btn['link'])])

                await set_msg.reply(
                    "<b><i>Aᴅᴅᴇᴅ Sᴜᴄcᴇssғᴜʟʟʏ ✅</i>\n<blockquote>Sᴇᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴀs Pʀᴇᴠɪᴇᴡ ⬇️</blockquote></b>",
                    reply_markup=InlineKeyboardMarkup(button_preview)
                )
                await db.set_channel_button_links(new_buttons)
                return
            except Exception as e:
                try:
                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                except BaseException:
                    pass

    elif data == 'autodel_cmd':"""

content = re.sub(setcb_pattern, new_setcb_block, content, flags=re.DOTALL)
with open('plugins/query.py', 'w') as f:
    f.write(content)
