import re

with open("plugins/query.py", "r") as f:
    content = f.read()

# Add a callback handler for back to main settings
main_settings_handler = """    elif data == "main_settings":
        if await authoUser(query, query.from_user.id):
            button = [
                [InlineKeyboardButton("🤖 Force Sub Settings", callback_data="fsub_main")],
                [InlineKeyboardButton("📝 Caption Settings", callback_data="caption_settings"), InlineKeyboardButton("🔲 Button Settings", callback_data="button_settings")],
                [InlineKeyboardButton("Cʟᴏsᴇ ✖️", callback_data="close")]
            ]
            await query.message.edit_text(
                text="<b>⚙️ Main Settings Panel:</b>\\n\\nManage your bot's configuration from here.",
                reply_markup=InlineKeyboardMarkup(button)
            )

"""

# Caption settings callback handler
caption_settings_handler = """    elif data == "caption_settings":
        if await authoUser(query, query.from_user.id):
            try:
                caption = await db.get_custom_caption()
                caption_text = caption if caption else "Not set"

                button = [
                    [InlineKeyboardButton("📝 Set/Change Caption", callback_data="set_caption_prompt")],
                    [InlineKeyboardButton("🗑 Delete Caption", callback_data="delete_caption_prompt")],
                    [InlineKeyboardButton("⬅️ Back", callback_data="main_settings")]
                ]
                await query.message.edit_text(
                    text=f"<b>📝 Custom Caption Settings:</b>\\n\\n<b>Current Caption:</b>\\n<code>{caption_text}</code>",
                    reply_markup=InlineKeyboardMarkup(button)
                )
            except Exception as e:
                logging.error(f"Error loading caption settings: {e}")
                await query.answer("❌ Error loading caption settings.", show_alert=True)

    elif data == "set_caption_prompt":
        id = query.from_user.id
        if await authoUser(query, id):
            await query.answer("♻️ Processing...")
            try:
                caption = await db.get_custom_caption()
                msg = await client.ask(
                    chat_id=id,
                    text=f"<b>Send Custom Caption within 1 minute. You can use HTML tags.\\nSend <code>/clear_caption</code> to remove it.\\n\\n<blockquote>Current Caption:</blockquote></b> {caption}",
                    timeout=60
                )
                if msg.text.strip() == '/clear_caption':
                    await db.set_custom_caption("")
                    await msg.reply("<b>Caption cleared.</b>")
                else:
                    await db.set_custom_caption(msg.text.strip())
                    await msg.reply("<b>Custom Caption Set Successfully ✅</b>")
            except Exception as e:
                try:
                    await client.send_message(id, text=f"<b>! Error Occurred..\\n<blockquote><i>Reason: Timeout or Error ..</i></b></blockquote>", disable_notification=True)
                except BaseException:
                    pass

    elif data == "delete_caption_prompt":
        if await authoUser(query, query.from_user.id):
            await db.set_custom_caption("")
            await query.answer("✅ Caption deleted successfully.", show_alert=True)
            # Refresh caption settings
            query.data = "caption_settings"
            await cb_handler(client, query)

"""

# Insert these into cb_handler
# We can find elif data == "fsub_main": and put it right before
insert_pos = content.find("elif data == \"fsub_main\":")
content = content[:insert_pos] + main_settings_handler + caption_settings_handler + content[insert_pos:]

# Wait, we need to change fsub_main back button to go to main_settings instead of fsub_main?
# Wait, fsub_main IS a settings panel now.
# In original fsub_main, it says "Close". But the back buttons in fsub_add, fsub_remove, etc., go to fsub_main.
# We should change fsub_main to have a back button to main_settings instead of close.
content = content.replace(
    '        if await authoUser(query, query.from_user.id):\n            button = [\n                [InlineKeyboardButton("➕ Add Channel", callback_data="fsub_add"), InlineKeyboardButton("➖ Remove Channel", callback_data="fsub_remove")],\n                [InlineKeyboardButton("📋 List Channels", callback_data="fsub_list")],\n                [InlineKeyboardButton("Cʟᴏsᴇ ✖️", callback_data="close")]\n            ]',
    '        if await authoUser(query, query.from_user.id):\n            button = [\n                [InlineKeyboardButton("➕ Add Channel", callback_data="fsub_add"), InlineKeyboardButton("➖ Remove Channel", callback_data="fsub_remove")],\n                [InlineKeyboardButton("📋 List Channels", callback_data="fsub_list")],\n                [InlineKeyboardButton("⬅️ Back", callback_data="main_settings")]\n            ]'
)

with open("plugins/query.py", "w") as f:
    f.write(content)
