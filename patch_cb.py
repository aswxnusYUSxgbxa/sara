with open('plugins/query.py', 'r') as f:
    content = f.read()

import re

old_cb_block = """            try:
                protect_content, pcd = await fileSettings(db.get_protect_content)
                hide_caption, hcd = await fileSettings(db.get_hide_caption)
                pic, channel_button, cbd = await fileSettings(db.get_channel_button, db.set_channel_button)
                name, link, name2, link2 = await db.get_channel_button_links()
                if not name2:
                    name2 = "Not Set"
                if not link2:
                    link2 = "Not Set"

                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    FILES_CMD_TXT.format(
                                        protect_content=protect_content,
                                        hide_caption=hide_caption,
                                        channel_button=channel_button,
                                        name=name,
                                        link=link,
                                        name2=name2,
                                        link2=link2
                                    )
                                    ),
                    reply_markup=InlineKeyboardMarkup(
                        buttonStatus(pcd, hcd, cbd, query.from_user.id == OWNER_ID))
                )"""

new_cb_block = """            try:
                protect_content, pcd = await fileSettings(db.get_protect_content)
                hide_caption, hcd = await fileSettings(db.get_hide_caption)
                pic, channel_button, cbd = await fileSettings(db.get_channel_button, db.set_channel_button)
                buttons_data = await db.get_channel_button_links()

                buttons_text = ""
                for i in range(5):
                    if i < len(buttons_data):
                        btn = buttons_data[i]
                        buttons_text += f"◈ ʙᴜᴛᴛᴏɴ {i+1} Nᴀᴍᴇ: {btn['name']}\\n◈ ʙᴜᴛᴛᴏɴ {i+1} Lɪɴᴋ: {btn['link']}\\n"
                    else:
                        buttons_text += f"◈ ʙᴜᴛᴛᴏɴ {i+1} Nᴀᴍᴇ: Not Set\\n◈ ʙᴜᴛᴛᴏɴ {i+1} Lɪɴᴋ: Not Set\\n"

                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    FILES_CMD_TXT.format(
                                        protect_content=protect_content,
                                        hide_caption=hide_caption,
                                        channel_button=channel_button,
                                        buttons_text=buttons_text.strip()
                                    )
                                    ),
                    reply_markup=InlineKeyboardMarkup(
                        buttonStatus(pcd, hcd, cbd, query.from_user.id == OWNER_ID))
                )"""

content = content.replace(old_cb_block, new_cb_block)
with open('plugins/query.py', 'w') as f:
    f.write(content)
