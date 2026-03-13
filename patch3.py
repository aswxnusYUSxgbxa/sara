with open('plugins/query.py', 'r') as f:
    content = f.read()

import re
old_button_status = """def buttonStatus(pc_data: str, hc_data: str, cb_data: str) -> list:
    button = [
        [
            InlineKeyboardButton(
                f'Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ: {pc_data}', callback_data='pc'),
            InlineKeyboardButton(
                f'Hɪᴅᴇ Cᴀᴘᴛɪᴏɴ: {hc_data}', callback_data='hc')
        ],
        [
            InlineKeyboardButton(
                f'Cʜᴀɴɴᴇʟ Bᴜᴛᴛᴏɴ: {cb_data}', callback_data='cb'),
            InlineKeyboardButton(f'◈ Sᴇᴛ Bᴜᴛᴛᴏɴs ➪', callback_data='setcb')
        ],
        [
            InlineKeyboardButton('📝 Set Caption', callback_data='set_custom_caption'),
        ],
    ]
    return button"""

new_button_status = """def buttonStatus(pc_data: str, hc_data: str, cb_data: str, is_owner: bool = False) -> list:
    button = [
        [
            InlineKeyboardButton(
                f'Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ: {pc_data}', callback_data='pc'),
            InlineKeyboardButton(
                f'Hɪᴅᴇ Cᴀᴘᴛɪᴏɴ: {hc_data}', callback_data='hc')
        ],
        [
            InlineKeyboardButton(
                f'Cʜᴀɴɴᴇʟ Bᴜᴛᴛᴏɴ: {cb_data}', callback_data='cb'),
            InlineKeyboardButton(f'◈ Sᴇᴛ Bᴜᴛᴛᴏɴs ➪', callback_data='setcb')
        ],
        [
            InlineKeyboardButton('📝 Set Caption', callback_data='set_custom_caption'),
        ],
    ]
    if is_owner:
        button.append([InlineKeyboardButton('👥 Admins', callback_data='admins_menu')])
    return button"""

content = content.replace(old_button_status, new_button_status)

with open('plugins/query.py', 'w') as f:
    f.write(content)
