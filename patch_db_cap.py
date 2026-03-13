with open('database/database.py', 'r') as f:
    content = f.read()

import re

# Add get/set custom caption methods
cap_methods = """
    # CUSTOM CAPTION
    async def get_custom_caption(self):
        doc = await self.configs.find_one({'_id': 'custom_caption'})
        if doc:
            return doc.get('caption', "")
        return ""

    async def set_custom_caption(self, caption: str):
        await self.configs.update_one({'_id': 'custom_caption'}, {'$set': {'caption': caption}}, upsert=True)
"""

if "async def get_custom_caption" not in content:
    content = content.replace("class Database:", "class Database:\n" + cap_methods)
    with open('database/database.py', 'w') as f:
        f.write(content)
