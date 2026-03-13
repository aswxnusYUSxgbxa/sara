with open('plugins/query.py', 'r') as f:
    content = f.read()

import re

# Find buttonStatus def block
button_status_pattern = r'def buttonStatus.*?return button'
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

content = re.sub(button_status_pattern, new_button_status, content, flags=re.DOTALL)

# Fix invocations
content = re.sub(r'buttonStatus\(pc_data, hc_data, cb_data, m.from_user.id == Config.ADMIN\)', r'buttonStatus(pc_data, hc_data, cb_data, m.from_user.id == OWNER_ID)', content)
content = re.sub(r'buttonStatus\(pcd, hcd, cbd, query.from_user.id == Config.ADMIN\)', r'buttonStatus(pcd, hcd, cbd, query.from_user.id == OWNER_ID)', content)
content = re.sub(r'buttonStatus\(pcd,\s*hcd,\s*cbd\)', r'buttonStatus(pcd, hcd, cbd, query.from_user.id == OWNER_ID)', content)
content = re.sub(r'buttonStatus\(pc_data,\s*hc_data,\s*cb_data\)', r'buttonStatus(pc_data, hc_data, cb_data, m.from_user.id == OWNER_ID)', content)

# ensure import
if "OWNER_ID" not in content:
    content = content.replace("from config import START_PIC, FORCE_PIC, CUSTOM_CAPTION", "from config import START_PIC, FORCE_PIC, CUSTOM_CAPTION, OWNER_ID")
    content = content.replace("from config import FORCE_PIC, CUSTOM_CAPTION", "from config import FORCE_PIC, CUSTOM_CAPTION, OWNER_ID")

with open('plugins/query.py', 'w') as f:
    f.write(content)
