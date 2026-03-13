import re

with open('plugins/query.py', 'r') as f:
    content = f.read()

# Fix unterminated string block due to unexpected newlines instead of \n
bad_block = """                example_text = (
                    '<b>Tᴏ sᴇᴛ ᴛʜᴇ ʙᴜᴛᴛᴏɴ(s), Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛs ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ. Yᴏᴜ ᴄᴀɴ sᴇᴛ ᴜᴘ ᴛᴏ 5 ʙᴜᴛᴛᴏɴs.

'
                    '<b>Sᴇᴘᴀʀᴀᴛᴇ ʙᴜᴛᴛᴏɴs ᴡɪᴛʜ | ᴏʀ ɴᴇᴡʟɪɴᴇs.</b>
'
                    '<blockquote><code>Join Channel - https://t.me/btth480p | Support - https://t.me/support</code></blockquote>

'
                    '<i>Sᴇɴᴅ /clear_buttons ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀʟʟ ʙᴜᴛᴛᴏɴs.</i>

'
                    '<i>Bᴇʟᴏᴡ ɪs ᴄᴜʀʀᴇɴᴛ ʙᴜᴛᴛᴏɴ(s) Pʀᴇᴠɪᴇᴡ ⬇️</i></b>'
                )"""

good_block = """                example_text = (
                    '<b>Tᴏ sᴇᴛ ᴛʜᴇ ʙᴜᴛᴛᴏɴ(s), Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛs ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ. Yᴏᴜ ᴄᴀɴ sᴇᴛ ᴜᴘ ᴛᴏ 5 ʙᴜᴛᴛᴏɴs.\\n\\n'
                    '<b>Sᴇᴘᴀʀᴀᴛᴇ ʙᴜᴛᴛᴏɴs ᴡɪᴛʜ | ᴏʀ ɴᴇᴡʟɪɴᴇs.</b>\\n'
                    '<blockquote><code>Join Channel - https://t.me/btth480p | Support - https://t.me/support</code></blockquote>\\n\\n'
                    '<i>Sᴇɴᴅ /clear_buttons ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀʟʟ ʙᴜᴛᴛᴏɴs.</i>\\n\\n'
                    '<i>Bᴇʟᴏᴡ ɪs ᴄᴜʀʀᴇɴᴛ ʙᴜᴛᴛᴏɴ(s) Pʀᴇᴠɪᴇᴡ ⬇️</i></b>'
                )"""

if bad_block in content:
    content = content.replace(bad_block, good_block)

bad_text = """raw_text = set_msg.text.replace('
"""
good_text = "                raw_text = set_msg.text.replace('\\n', ' | ')\n"
if bad_text in content:
    content = content.replace(bad_text, good_text)

content = content.replace("', ' | ')", "")

content = content.replace('                    "<b><i>Aᴅᴅᴇᴅ Sᴜᴄcᴇssғᴜʟʟʏ ✅</i>\n<blockquote>Sᴇᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴀs Pʀᴇᴠɪᴇᴡ ⬇️</blockquote></b>", \n', '                    "<b><i>Aᴅᴅᴇᴅ Sᴜᴄcᴇssғᴜʟʟʏ ✅</i>\\n<blockquote>Sᴇᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴀs Pʀᴇᴠɪᴇᴡ ⬇️</blockquote></b>", \n')

content = content.replace('                    text=f"<b>Sᴇɴᴅ Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ. Yᴏᴜ ᴄᴀɴ ᴜsᴇ HTML ᴛᴀɢs.\n', '                    text=f"<b>Sᴇɴᴅ Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ. Yᴏᴜ ᴄᴀɴ ᴜsᴇ HTML ᴛᴀɢs.\\n')
content = content.replace('Sᴇɴᴅ <code>/clear_caption</code> ᴛᴏ ʀᴇᴍᴏᴠᴇ ɪᴛ.\n\n<blockquote>Cᴜʀʀᴇɴᴛ Cᴀᴘᴛɪᴏɴ:</blockquote></b> {caption}",\n', 'Sᴇɴᴅ <code>/clear_caption</code> ᴛᴏ ʀᴇᴍᴏᴠᴇ ɪᴛ.\\n\\n<blockquote>Cᴜʀʀᴇɴᴛ Cᴀᴘᴛɪᴏɴ:</blockquote></b> {caption}",\n')


with open('plugins/query.py', 'w') as f:
    f.write(content)
