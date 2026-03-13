import re

with open("plugins/query.py", "r") as f:
    content = f.read()

# Button settings callback handler
button_settings_handler = """    elif data == "button_settings":
        if await authoUser(query, query.from_user.id):
            try:
                buttons_data = await db.get_channel_button_links()

                button_preview = []
                for btn in buttons_data:
                    button_preview.append([InlineKeyboardButton(text=btn['name'], url=btn['link'])])

                button = [
                    [InlineKeyboardButton("🔲 Set/Change Buttons", callback_data="set_button_prompt")],
                    [InlineKeyboardButton("🗑 Delete Buttons", callback_data="delete_button_prompt")],
                    [InlineKeyboardButton("⬅️ Back", callback_data="main_settings")]
                ]
                await query.message.edit_text(
                    text="<b>🔲 Custom Button Settings:</b>\\n\\n<b>Current Buttons (Preview):</b>",
                    reply_markup=InlineKeyboardMarkup(button_preview + button),
                    disable_web_page_preview=True
                )
            except Exception as e:
                logging.error(f"Error loading button settings: {e}")
                await query.answer("❌ Error loading button settings.", show_alert=True)

    elif data == "set_button_prompt":
        id = query.from_user.id
        if await authoUser(query, id):
            await query.answer("♻️ Processing...")
            try:
                buttons_data = await db.get_channel_button_links()

                button_preview = []
                for btn in buttons_data:
                    button_preview.append([InlineKeyboardButton(text=btn['name'], url=btn['link'])])

                example_text = (
                    '<b>To set the button(s), Please send valid arguments within 1 minute. You can set up to 5 buttons.\\n\\n'
                    '<b>Separate buttons with | or newlines.</b>\\n'
                    '<blockquote><code>Join Channel - https://t.me/btth480p | Support - https://t.me/support</code></blockquote>\\n\\n'
                    '<i>Send /clear_buttons to remove all buttons.</i>\\n\\n'
                    '<i>Below is current button(s) Preview ⬇️</i></b>'
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
                    await set_msg.reply("<b>All buttons have been cleared.</b>")
                else:
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
                        return await set_msg.reply("<b>Please send valid arguments. Format: Name - Link</b>")

                    if len(new_buttons) > 5:
                        new_buttons = new_buttons[:5]

                    await db.set_channel_button_links(new_buttons)

                    button_preview = []
                    for btn in new_buttons:
                        button_preview.append([InlineKeyboardButton(text=btn['name'], url=btn['link'])])

                    await set_msg.reply(
                        "<b><i>Buttons Added Successfully ✅</i>\\n<blockquote>See below buttons as Preview ⬇️</blockquote></b>",
                        reply_markup=InlineKeyboardMarkup(button_preview)
                    )
            except Exception as e:
                try:
                    await client.send_message(id, text=f"<b>! Error Occurred..\\n<blockquote><i>Reason: Timeout or Error ..</i></b></blockquote>", disable_notification=True)
                except BaseException:
                    pass

    elif data == "delete_button_prompt":
        if await authoUser(query, query.from_user.id):
            await db.set_channel_button_links([])
            await query.answer("✅ Buttons deleted successfully.", show_alert=True)
            # Refresh button settings
            query.data = "button_settings"
            await cb_handler(client, query)

"""

# Insert these into cb_handler
insert_pos = content.find("    elif data == \"fsub_main\":")
content = content[:insert_pos] + button_settings_handler + content[insert_pos:]

with open("plugins/query.py", "w") as f:
    f.write(content)
