import re

with open("plugins/start.py", "r") as f:
    content = f.read()

new_fsub = """@Bot.on_message(filters.command(['forcesub', 'fsub', 'config', 'settings']) & filters.private & is_admin)
async def fsub_commands(client: Client, message: Message):
    button = [
        [InlineKeyboardButton("🤖 Force Sub Settings", callback_data="fsub_main")],
        [InlineKeyboardButton("📝 Caption Settings", callback_data="caption_settings"), InlineKeyboardButton("🔲 Button Settings", callback_data="button_settings")],
        [InlineKeyboardButton("Cʟᴏsᴇ ✖️", callback_data="close")]
    ]
    await message.reply(
        text="<b>⚙️ Main Settings Panel:</b>\\n\\nManage your bot's configuration from here.",
        reply_markup=InlineKeyboardMarkup(button),
        quote=True
    )"""

content = re.sub(
    r"@Bot\.on_message\(filters\.command\(\['forcesub', 'fsub', 'config', 'settings'\]\) & filters\.private & is_admin\)\nasync def fsub_commands\(client: Client, message: Message\):\n    button = \[\n        \[InlineKeyboardButton\(\"➕ Add Channel\", callback_data=\"fsub_add\"\), InlineKeyboardButton\(\"➖ Remove Channel\", callback_data=\"fsub_remove\"\)\],\n        \[InlineKeyboardButton\(\"📋 List Channels\", callback_data=\"fsub_list\"\)\],\n        \[InlineKeyboardButton\(\"Cʟᴏsᴇ ✖️\", callback_data=\"close\"\)]\n    \]\n    await message\.reply\(text=\"<b>🤖 Force Subscription Settings:</b>\\n\\nManage your force sub channels below\. You can add up to 5 channels\.\", reply_markup=InlineKeyboardMarkup\(button\), quote=True\)",
    new_fsub,
    content
)

with open("plugins/start.py", "w") as f:
    f.write(content)
