with open('plugins/query.py', 'r') as f:
    content = f.read()

import re

# We need to replace buttonStatus calls
# In check_user
content = re.sub(
    r'reply_markup=InlineKeyboardMarkup\(buttonStatus\(pc_data, hc_data, cb_data\)\)',
    r'reply_markup=InlineKeyboardMarkup(buttonStatus(pc_data, hc_data, cb_data, m.from_user.id == OWNER_ID))',
    content
)

# In files_cmd and others
content = re.sub(
    r'reply_markup=InlineKeyboardMarkup\(\s*buttonStatus\(pcd, hcd, cbd\)\)',
    r'reply_markup=InlineKeyboardMarkup(buttonStatus(pcd, hcd, cbd, query.from_user.id == OWNER_ID))',
    content
)

# Need to ensure OWNER_ID is imported if not
if "from config import" in content and "OWNER_ID" not in content:
    content = re.sub(r'from config import ([^\n]+)', r'from config import \1, OWNER_ID', content, count=1)

with open('plugins/query.py', 'w') as f:
    f.write(content)
