on_pic = "https://telegra.ph/file/5593d624d11d92bceb48e.jpg"
off_pic = "https://telegra.ph/file/0d9e590f62b63b51d4bf9.jpg"
files_cmd_pic = "https://telegra.ph/file/d44f46054250a73053614.jpg"
autodel_cmd_pic = "https://telegra.ph/file/a64533814021b40057ccd.jpg"


SET_SHORTENER_CMD_TXT = "Shortener is {shortener_status}. Use button to configure the shortener."

#start message
START_MSG = """Hello {mention}

I can Download terabox files and having Advanced features 😎 ."""


#Force sub message
FORCE_MSG = """<b>Hello {mention},\n\nYou have to join this channel to access media in this bot.</b>"""




CMD_TXT = """<b>🤖 BASIC ADMIN COMMANDS :

<b>/broadcast :</b> broadcast message

<code>/broadcast silent</code> : silent broadcast message

<b>/status :</b> view bot statistics"""

BAN_TXT = "<b><blockquote>Sorry, you are banned 🚫</blockquote></b>"

HELP_TEXT = """<b>⁉️ Hello {mention} ~

<blockquote expandable>➪ I am a TeraBox Download Bot, created to help you download files from TeraBox and provide a direct download link.

➪ In order to use my services, you must follow all the mentioned channels that are required for access.

➪ Just send a valid TeraBox link, and you will receive a direct download link or file for easy access.

‣ /help -</b> Open this help message !</blockquote>
<b><i>◈ Still have questions? Contact the admins or join our group for more help !</i></b>"""

ABOUT_TXT = """<b>🤖 my name: {botname}
<blockquote expandable>◈ advance features: <a href='https://telegra.ph/BOT-FEATURES-11-09-28'>Click here</a>
◈ owner: {ownername}
◈ language: <a href='https://docs.python.org/3/'>Python 3</a>
◈ library: <a href='https://docs.pyrogram.org/'>Pyrogram v2</a>
◈ database: <a href='https://www.mongodb.com/docs/'>Mongo db</a>
🧑‍💻 developer: @rohit_1888</b></blockquote>"""

SETTING_TXT = """<b>⚙️ Configurations</b>
<blockquote expandable>◈ total force sub channel:  <b>{total_fsub}</b>
◈ total admins:  <b>{total_admin}</b>
◈ total banned users:  <b>{total_ban}</b>
◈ auto delete mode:  <b>{autodel_mode}</b>
◈ protect content:  <b>{protect_content}</b>
◈ hide caption:  <b>{hide_caption}</b>
◈ channel button:  <b>{chnl_butn}</b>
◈ request fsub mode: <b>{reqfsub}</b></blockquote>"""

on_txt, off_txt = "Enabled ✅", "Disabled ❌"

FILES_CMD_TXT ="""<b>🤖 FILES RELATED SETTINGS ⚙️

<blockquote expandable>🔒 protect content: {protect_content}
🫥 hide caption: {hide_caption}
🔘 channel button: {channel_button}</b>

{buttons_text}</blockquote>

<b>click below buttons to change settings</b>"""

AUTODEL_CMD_TXT = """<b>🤖 AUTO DELETE SETTINGS ⚙️

<blockquote>🗑️ auto delete mode: {autodel_mode}</blockquote>
<blockquote>⏱ delete timer: {timer}</blockquote>

click below buttons to change settings</b>"""

FSUB_CMD_TXT = """<b>🤖 FORCE SUB COMMANDS :</b>

<b>/fsub_chnl</b> : check current force-sub channels (admins)

<b>/add_fsub</b> : add one or multiple force sub channels (owner)

<b>/del_fsub</b> : delete one or multiple force sub channels (owner)"""


USER_CMD_TXT = """<b>🤖 USER SETTING COMMANDS :</b>

<b>/admin_list</b> : view the available admin list (owner)

<b>/add_admins</b> : add one or multiple user ids as admin (owner)

<b>/del_admins</b> : delete one or multiple user ids from admins (owner)

<b>/banuser_list</b> : view the available banned user list (admins)

<b>/add_banuser</b> : add one or multiple user ids in banned list (admins)

<b>/del_banuser</b> : delete one or multiple user ids from banned list (admins)"""



RFSUB_CMD_TXT = """<b>🤖 REQUEST FSUB SETTINGS 🚦

<blockquote><b>📢 request fsub mode: {req_mode}</b></blockquote>

click below buttons to change settings</b>"""


RFSUB_MS_TXT = """<b>🤖 REQUEST FSUB LIST 🚥

<blockquote expandable>{reqfsub_list}</blockquote>
click below buttons to change settings</b>"""

CLEAR_USERS_TXT = """<blockquote expandable><b>What is the use of Clear Users !?</b>

➪ Clear Users is used to clear the all user data of a specified Request forcesub channel id.

➪ Here only user data is deleted from specified channel.</blockquote>

<b><i>Choose the Channel id for deleting user data:</i></b>"""


CLEAR_CHNLS_TXT = """<blockquote expandable><b>What is the use of Clear Channels !?</b>

➪ Clear Channels used to Delete all user data along with Request forcesub channel id and link from database.

➪ Here all data realted to request forcesub channel id deleted Permanently...

<b>⚠️ WARNING:</b> Clear the channel data only when it is confirmed that the data will no longer be required for future operations.</blockquote>

<b><i>Choose the Channel id for deleting:</i></b>"""


CLEAR_LINKS_TXT = """<blockquote expandable><b>What is the use of Clear Links !?</b>

➪ Clear Stored Request Links used to Delete Links of a specified channel in database as well as revoke the link from that Channel.

➪ Even if clearing channel data the Request Link stored on database for future using of that channel,

➪ By deleting request link of specified channel the link will be revoked from that channel and not usable any more,

➪ So the bot will have to create again request link of that channel in future if that channel again added as request forcesub channel.

<b>⚠️ NOTE:</b>
‣ To perform this action the bot should have admin along with proper permission on that channel.

‣ if the bot not in that channel or don't have admin permission then this operation can't be performed.</blockquote>

<b><i>Choose the Channel id for deleting Request Link:</i></b>"""