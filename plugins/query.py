import random
import logging
import asyncio
from bot import Bot
from pyrogram import __version__
from pyrogram.enums import ParseMode
from plugins.FORMATS import *
from config import *
from pyrogram.enums import ChatAction
from plugins.autoDelete import convert_time
from database.database import db
from datetime import timedelta
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, ReplyKeyboardMarkup, ReplyKeyboardRemove



logging.basicConfig(
    level=logging.INFO,  # Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

async def fileSettings(getfunc, setfunc=None, delfunc=False):
    btn_mode, txt_mode, pic_mode = '❌', off_txt, off_pic
    del_btn_mode = 'Eɴᴀʙʟᴇ Mᴏᴅᴇ ✅'
    try:
        if not setfunc:
            if await getfunc():
                txt_mode = on_txt
                btn_mode = '✅'
                del_btn_mode = 'Dɪsᴀʙʟᴇ Mᴏᴅᴇ ❌'

            return txt_mode, (del_btn_mode if delfunc else btn_mode)

        else:
            if await getfunc():
                await setfunc(False)
            else:
                await setfunc(True)
                pic_mode, txt_mode = on_pic, on_txt
                btn_mode = '✅'
                del_btn_mode = 'Dɪsᴀʙʟᴇ Mᴏᴅᴇ ❌'

            return pic_mode, txt_mode, (del_btn_mode if delfunc else btn_mode)

    except Exception as e:
        print(
            f"Error occured at [fileSettings(getfunc, setfunc=None, delfunc=False)] : {e}")

# Provide or Make Button by takiing required modes and data


def buttonStatus(pc_data: str, hc_data: str, cb_data: str, is_owner: bool = False) -> list:
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
    return button

# Verify user, if he/she is admin or owner before processing the query...


async def authoUser(query, id, owner_only=False):
    if not owner_only:
        if not any([id == OWNER_ID, await db.admin_exist(id)]):
            await query.answer("❌ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ Aᴅᴍɪɴ !", show_alert=True)
            return False
        return True
    else:
        if id != OWNER_ID:
            await query.answer("❌ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ Oᴡɴᴇʀ !", show_alert=True)
            return False
        return True


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except BaseException:
            pass

    elif data.startswith("get_again_"):
        # Handle get again callback
        try:
            action = data.replace("get_again_", "")
            user_id = query.from_user.id
            
            # Extract user_id from action (format: get_photo_123 or get_video_123 or get_batch_123)
            # Split and get the last part as user_id
            parts = action.split("_")
            if len(parts) >= 3:
                # Last part is always the user_id
                action_user_id = int(parts[-1])
                
                if action_user_id != user_id:
                    await query.answer("❌ Unauthorized access!", show_alert=True)
                    return
                
                # Extract action type (photo, video, or batch)
                action_type = parts[1]  # 'photo', 'video', or 'batch'
                
                await query.answer("🔄 Getting " + action_type + "...")
                
                # Use the query.message directly - it has all necessary attributes
                # We just need to ensure from_user is set correctly
                msg = query.message
                msg.from_user = query.from_user
                
                # Call the appropriate function
                from plugins.start import get_photo, get_video, get_batch
                try:
                    if action_type == "photo":
                        await get_photo(client, msg)
                    elif action_type == "video":
                        await get_video(client, msg)
                    elif action_type == "batch":
                        await get_batch(client, msg)
                    else:
                        await query.answer("❌ Invalid action type!", show_alert=True)
                        return
                finally:
                    # Delete the notification message after calling the function
                    try:
                        await query.message.delete()
                    except:
                        pass
            else:
                await query.answer("❌ Invalid format!", show_alert=True)
        except ValueError as e:
            logging.error(f"ValueError in get_again callback: {e}")
            await query.answer("❌ Invalid user ID format!", show_alert=True)
        except Exception as e:
            logging.error(f"Error handling get_again callback: {e}")
            import traceback
            logging.error(traceback.format_exc())
            await query.answer("❌ An error occurred!", show_alert=True)

    elif data == "about":
        await query.message.edit_text(
            text=(
                f"<b>○ Updates : <a href='https://t.me/rohit_1888'>Rohit</a>\n"
                f"○ Language : <code>Python3</code>\n"
                f"○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('⬅️ Bᴀᴄᴋ', callback_data='start'), InlineKeyboardButton(
                    'Cʟᴏsᴇ ✖️', callback_data='close')]
            ]),
        )

    elif data == "buy_prem":
        # Delete the current message and send a new one with the photo
        await query.message.delete()
        await client.send_photo(
            chat_id=query.message.chat.id,
            photo=QR_PIC,
            caption=(
                f"👋 {query.from_user.username}\n\n"
                f"🎖️ Available Plans :\n\n"
                f"● {PRICE1}  For 0 Days Prime Membership\n\n"
                f"● {PRICE2}  For 1 Month Prime Membership\n\n"
                f"● {PRICE3}  For 3 Months Prime Membership\n\n"
                f"● {PRICE4}  For 6 Months Prime Membership\n\n"
                f"● {PRICE5}  For 1 Year Prime Membership\n\n\n"
                f"💵 ASK UPI ID TO ADMIN AND PAY THERE -  <code>{UPI_ID}</code>\n\n\n"
                f"♻️ After Payment You Will Get Instant Membership \n\n\n"
                f"‼️ Must Send Screenshot after payment & If anyone want custom time membrship then ask admin"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "ADMIN 24/7", url=(SCREENSHOT_URL)
                        )
                    ],
                    [InlineKeyboardButton("🔒 Close", callback_data="close")],
                ]
            )
        )

    elif data == "setting":
        await query.edit_message_media(InputMediaPhoto(random.choice(PICS), "<b>Pʟᴇᴀsᴇ wᴀɪᴛ !\n\n<i>🔄 Rᴇᴛʀɪᴇᴠɪɴɢ ᴀʟʟ Sᴇᴛᴛɪɴɢs...</i></b>"))
        try:
            total_fsub = len(await db.get_all_channels())
            total_admin = len(await db.get_all_admins())
            total_ban = len(await db.get_ban_users())
            autodel_mode = 'Eɴᴀʙʟᴇᴅ' if await db.get_auto_delete() else 'Dɪsᴀʙʟᴇᴅ'
            protect_content = 'Eɴᴀʙʟᴇᴅ' if await db.get_protect_content() else 'Dɪsᴀʙʟᴇᴅ'
            hide_caption = 'Eɴᴀʙʟᴇᴅ' if await db.get_hide_caption() else 'Dɪsᴀʙʟᴇᴅ'
            chnl_butn = 'Eɴᴀʙʟᴇᴅ' if await db.get_channel_button() else 'Dɪsᴀʙʟᴇᴅ'
            reqfsub = 'Eɴᴀʙʟᴇᴅ' if await db.get_request_forcesub() else 'Dɪsᴀʙʟᴇᴅ'

            await query.edit_message_media(
                InputMediaPhoto(random.choice(PICS),
                                SETTING_TXT.format(
                                    total_fsub=total_fsub,
                                    total_admin=total_admin,
                                    total_ban=total_ban,
                                    autodel_mode=autodel_mode,
                                    protect_content=protect_content,
                                    hide_caption=hide_caption,
                                    chnl_butn=chnl_butn,
                                    reqfsub=reqfsub
                )
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('⬅️ Bᴀᴄᴋ', callback_data='start'), InlineKeyboardButton(
                        'Cʟᴏsᴇ ✖️', callback_data='close')]
                ]),
            )
        except Exception as e:
            print(f"! Error Occurred on callback data = 'setting' : {e}")

    elif data == "start":
        await query.edit_message_media(
            InputMediaPhoto(random.choice(PICS),
                            START_MSG.format(
                                first=query.from_user.first_name,
                                last=query.from_user.last_name,
                                username=None if not query.from_user.username else '@' + query.from_user.username,
                                mention=query.from_user.mention,
                                id=query.from_user.id
            )
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('🤖 Aʙᴏᴜᴛ ᴍᴇ', callback_data='about'), InlineKeyboardButton(
                    'Sᴇᴛᴛɪɴɢs ⚙️', callback_data='setting')]
            ]),
        )

    elif data == "files_cmd":
        if await authoUser(query, query.from_user.id):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                protect_content, pcd = await fileSettings(db.get_protect_content)
                hide_caption, hcd = await fileSettings(db.get_hide_caption)
                channel_button, cbd = await fileSettings(db.get_channel_button)
                buttons_data = await db.get_channel_button_links()
                
                buttons_text = ""
                for i in range(5):
                    if i < len(buttons_data):
                        btn = buttons_data[i]
                        buttons_text += f"◈ ʙᴜᴛᴛᴏɴ {i+1} Nᴀᴍᴇ: {btn['name']}\n◈ ʙᴜᴛᴛᴏɴ {i+1} Lɪɴᴋ: {btn['link']}\n"
                    else:
                        buttons_text += f"◈ ʙᴜᴛᴛᴏɴ {i+1} Nᴀᴍᴇ: Not Set\n◈ ʙᴜᴛᴛᴏɴ {i+1} Lɪɴᴋ: Not Set\n"

                await query.edit_message_media(
                    InputMediaPhoto(files_cmd_pic,
                                    FILES_CMD_TXT.format(
                                        protect_content=protect_content,
                                        hide_caption=hide_caption,
                                        channel_button=channel_button,
                                        buttons_text=buttons_text.strip()
                                    )
                                    ),
                    reply_markup=InlineKeyboardMarkup(
                        buttonStatus(pcd, hcd, cbd, query.from_user.id == OWNER_ID)),
                )
            except Exception as e:
                print(f"! Error Occurred on callback data = 'files_cmd' : {e}")

    elif data == "pc":
        if await authoUser(query, query.from_user.id):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                pic, protect_content, pcd = await fileSettings(db.get_protect_content, db.set_protect_content)
                hide_caption, hcd = await fileSettings(db.get_hide_caption)
                channel_button, cbd = await fileSettings(db.get_channel_button)
                buttons_data = await db.get_channel_button_links()
                
                buttons_text = ""
                for i in range(5):
                    if i < len(buttons_data):
                        btn = buttons_data[i]
                        buttons_text += f"◈ ʙᴜᴛᴛᴏɴ {i+1} Nᴀᴍᴇ: {btn['name']}\n◈ ʙᴜᴛᴛᴏɴ {i+1} Lɪɴᴋ: {btn['link']}\n"
                    else:
                        buttons_text += f"◈ ʙᴜᴛᴛᴏɴ {i+1} Nᴀᴍᴇ: Not Set\n◈ ʙᴜᴛᴛᴏɴ {i+1} Lɪɴᴋ: Not Set\n"

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
                )
            except Exception as e:
                print(f"! Error Occurred on callback data = 'pc' : {e}")

    elif data == "hc":
        if await authoUser(query, query.from_user.id):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                protect_content, pcd = await fileSettings(db.get_protect_content)
                pic, hide_caption, hcd = await fileSettings(db.get_hide_caption, db.set_hide_caption)
                channel_button, cbd = await fileSettings(db.get_channel_button)
                buttons_data = await db.get_channel_button_links()
                
                buttons_text = ""
                for i in range(5):
                    if i < len(buttons_data):
                        btn = buttons_data[i]
                        buttons_text += f"◈ ʙᴜᴛᴛᴏɴ {i+1} Nᴀᴍᴇ: {btn['name']}\n◈ ʙᴜᴛᴛᴏɴ {i+1} Lɪɴᴋ: {btn['link']}\n"
                    else:
                        buttons_text += f"◈ ʙᴜᴛᴛᴏɴ {i+1} Nᴀᴍᴇ: Not Set\n◈ ʙᴜᴛᴛᴏɴ {i+1} Lɪɴᴋ: Not Set\n"

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
                )
            except Exception as e:
                print(f"! Error Occurred on callback data = 'hc' : {e}")

    elif data == "cb":
        if await authoUser(query, query.from_user.id):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                protect_content, pcd = await fileSettings(db.get_protect_content)
                hide_caption, hcd = await fileSettings(db.get_hide_caption)
                pic, channel_button, cbd = await fileSettings(db.get_channel_button, db.set_channel_button)
                buttons_data = await db.get_channel_button_links()
                
                buttons_text = ""
                for i in range(5):
                    if i < len(buttons_data):
                        btn = buttons_data[i]
                        buttons_text += f"◈ ʙᴜᴛᴛᴏɴ {i+1} Nᴀᴍᴇ: {btn['name']}\n◈ ʙᴜᴛᴛᴏɴ {i+1} Lɪɴᴋ: {btn['link']}\n"
                    else:
                        buttons_text += f"◈ ʙᴜᴛᴛᴏɴ {i+1} Nᴀᴍᴇ: Not Set\n◈ ʙᴜᴛᴛᴏɴ {i+1} Lɪɴᴋ: Not Set\n"

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
                )
            except Exception as e:
                print(f"! Error Occurred on callback data = 'cb' : {e}")

    elif data == "setcb":
        id = query.from_user.id
        if await authoUser(query, id):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                buttons_data = await db.get_channel_button_links()
                
                # Create preview with existing buttons
                button_preview = []
                for btn in buttons_data:
                    button_preview.append([InlineKeyboardButton(text=btn['name'], url=btn['link'])])
                
                example_text = (
                    '<b>Tᴏ sᴇᴛ ᴛʜᴇ ʙᴜᴛᴛᴏɴ(s), Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛs ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ. Yᴏᴜ ᴄᴀɴ sᴇᴛ ᴜᴘ ᴛᴏ 5 ʙᴜᴛᴛᴏɴs.\n\n'
                    '<b>Sᴇᴘᴀʀᴀᴛᴇ ʙᴜᴛᴛᴏɴs ᴡɪᴛʜ | ᴏʀ ɴᴇᴡʟɪɴᴇs.</b>\n'
                    '<blockquote><code>Join Channel - https://t.me/btth480p | Support - https://t.me/support</code></blockquote>\n\n'
                    '<i>Sᴇɴᴅ /clear_buttons ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀʟʟ ʙᴜᴛᴛᴏɴs.</i>\n\n'
                    '<i>Bᴇʟᴏᴡ ɪs ᴄᴜʀʀᴇɴᴛ ʙᴜᴛᴛᴏɴ(s) Pʀᴇᴠɪᴇᴡ ⬇️</i></b>'
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
                    return await set_msg.reply("<b>All buttons have been cleared.</b>")

                # Parse up to 5 buttons
                raw_text = set_msg.text.replace('\n', ' | ')

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
                    markup = [[InlineKeyboardButton(f'◈ Sᴇᴛ Cʜᴀɴɴᴇʟ Bᴜᴛᴛᴏɴ ➪', callback_data='setcb')]]
                    return await set_msg.reply(
                        "<b>Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛs. Fᴏʀᴍᴀᴛ: Nᴀᴍᴇ - Lɪɴᴋ</b>", 
                        reply_markup=InlineKeyboardMarkup(markup)
                    )
                
                if len(new_buttons) > 5:
                    new_buttons = new_buttons[:5]

                button_preview = []
                for btn in new_buttons:
                    button_preview.append([InlineKeyboardButton(text=btn['name'], url=btn['link'])])
                
                await set_msg.reply(
                    "<b><i>Aᴅᴅᴇᴅ Sᴜᴄcᴇssғᴜʟʟʏ ✅</i>\n<blockquote>Sᴇᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴀs Pʀᴇᴠɪᴇᴡ ⬇️</blockquote></b>", 
                    reply_markup=InlineKeyboardMarkup(button_preview)
                )
                await db.set_channel_button_links(new_buttons)
                return
            except Exception as e:
                try:
                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                except BaseException:
                    pass


    elif data == 'set_custom_caption':
        id = query.from_user.id
        if await authoUser(query, id):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")
            try:
                caption = await db.get_custom_caption()
                msg = await client.ask(
                    chat_id=id,
                    text=f"<b>Sᴇɴᴅ Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ. Yᴏᴜ ᴄᴀɴ ᴜsᴇ HTML ᴛᴀɢs.\nSᴇɴᴅ <code>/clear_caption</code> ᴛᴏ ʀᴇᴍᴏᴠᴇ ɪᴛ.\n\n<blockquote>Cᴜʀʀᴇɴᴛ Cᴀᴘᴛɪᴏɴ:</blockquote></b> {caption}",
                    timeout=60
                )
                if msg.text.strip() == '/clear_caption':
                    await db.set_custom_caption("")
                    await msg.reply("<b>Cᴀᴘᴛɪᴏɴ ᴄʟᴇᴀʀᴇᴅ.</b>")
                else:
                    await db.set_custom_caption(msg.text.strip())
                    await msg.reply("<b>Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ Sᴇᴛ Sᴜᴄᴄᴇssғᴜʟʟʏ ✅</b>")
            except Exception as e:
                try:
                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                except BaseException:
                    pass

    elif data == 'admins_menu':
        id = query.from_user.id
        if await authoUser(query, id, owner_only=True):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")
            try:
                admins = await db.get_all_admins()
                text = "<b>👥 Bᴏᴛ Aᴅᴍɪɴs</b>\n\n"

                
                if admins:
                    for idx, admin in enumerate(admins, 1):
                        text += f"<b>{idx}.</b> <code>{admin['_id']}</code>\n"
                else:
                    text += "<i>Nᴏ ᴀᴅᴍɪɴs ᴀᴅᴅᴇᴅ ʏᴇᴛ.</i>\n"
                
                text += "\n<b>Tᴏ ᴀᴅᴅ ᴀɴ ᴀᴅᴍɪɴ, sᴇɴᴅ ᴛʜᴇ ᴜsᴇʀ ID ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ.</b>\n<b>Tᴏ ʀᴇᴍᴏᴠᴇ ᴀɴ ᴀᴅᴍɪɴ, sᴇɴᴅ <code>/del_admin &lt;user_id&gt;</code>.</b>" 
                
                msg = await client.ask(chat_id=id, text=text, timeout=60)
                
                if msg.text.startswith('/del_admin'):
                    parts = msg.text.split()
                    if len(parts) == 2 and parts[1].isdigit():
                        admin_id = int(parts[1])
                        await db.del_admin(admin_id)
                        await msg.reply(f"<b>Aᴅᴍɪɴ <code>{admin_id}</code> ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅</b>")
                    else:
                        await msg.reply("<b>❌ Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ. Tʀʏ: <code>/del_admin 12345678</code></b>")
                elif msg.text.isdigit():
                    new_admin = int(msg.text)
                    await db.add_admin(new_admin)
                    await msg.reply(f"<b>Aᴅᴍɪɴ <code>{new_admin}</code> ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅</b>")
                else:
                    await msg.reply("<b>❌ Iɴᴠᴀʟɪᴅ Iɴᴘᴜᴛ.</b>")
                    
            except Exception as e:
                try:
                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                except BaseException:
                    pass

    elif data == 'autodel_cmd':
        if await authoUser(query, query.from_user.id, owner_only=True):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                timer = convert_time(await db.get_del_timer())
                autodel_mode, mode = await fileSettings(db.get_auto_delete, delfunc=True)

                await query.edit_message_media(
                    InputMediaPhoto(autodel_cmd_pic,
                                    AUTODEL_CMD_TXT.format(
                                        autodel_mode=autodel_mode,
                                        timer=timer
                                    )
                                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(mode, callback_data='chng_autodel'), InlineKeyboardButton(
                            '◈ Sᴇᴛ Tɪᴍᴇʀ ⏱', callback_data='set_timer')],
                        [InlineKeyboardButton('🔄 Rᴇғʀᴇsʜ', callback_data='autodel_cmd'), InlineKeyboardButton(
                            'Cʟᴏsᴇ ✖️', callback_data='close')]
                    ])
                )
            except Exception as e:
                print(
                    f"! Error Occurred on callback data = 'autodel_cmd' : {e}")

    elif data == 'chng_autodel':
        if await authoUser(query, query.from_user.id, owner_only=True):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                timer = convert_time(await db.get_del_timer())
                pic, autodel_mode, mode = await fileSettings(db.get_auto_delete, db.set_auto_delete, delfunc=True)

                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    AUTODEL_CMD_TXT.format(
                                        autodel_mode=autodel_mode,
                                        timer=timer
                                    )
                                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(mode, callback_data='chng_autodel'), InlineKeyboardButton(
                            '◈ Sᴇᴛ Tɪᴍᴇʀ ⏱', callback_data='set_timer')],
                        [InlineKeyboardButton('🔄 Rᴇғʀᴇsʜ', callback_data='autodel_cmd'), InlineKeyboardButton(
                            'Cʟᴏsᴇ ✖️', callback_data='close')]
                    ])
                )
            except Exception as e:
                print(
                    f"! Error Occurred on callback data = 'chng_autodel' : {e}")

    elif data == 'set_timer':
        id = query.from_user.id
        if await authoUser(query, id, owner_only=True):
            try:

                timer = convert_time(await db.get_del_timer())
                set_msg = await client.ask(chat_id=id, text=f'<b><blockquote>⏱ Cᴜʀʀᴇɴᴛ Tɪᴍᴇʀ: {timer}</blockquote>\n\nTᴏ ᴄʜᴀɴɢᴇ ᴛɪᴍᴇʀ, Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ɪɴ sᴇᴄᴏɴᴅs ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ.\n<blockquote>Fᴏʀ ᴇxᴀᴍᴘʟᴇ: <code>300</code>, <code>600</code>, <code>900</code></b></blockquote>', timeout=60)
                del_timer = set_msg.text.split()

                if len(del_timer) == 1 and del_timer[0].isdigit():
                    DEL_TIMER = int(del_timer[0])
                    await db.set_del_timer(DEL_TIMER)
                    timer = convert_time(DEL_TIMER)
                    await set_msg.reply(f"<b><i>Aᴅᴅᴇᴅ Sᴜᴄcᴇssғᴜʟʟʏ ✅</i>\n<blockquote>⏱ Cᴜʀʀᴇɴᴛ Tɪᴍᴇʀ: {timer}</blockquote></b>")
                else:
                    markup = [[InlineKeyboardButton(
                        '◈ Sᴇᴛ Dᴇʟᴇᴛᴇ Tɪᴍᴇʀ ⏱', callback_data='set_timer')]]
                    return await set_msg.reply("<b>Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ɪɴ sᴇᴄᴏɴᴅs.\n<blockquote>Fᴏʀ ᴇxᴀᴍᴘʟᴇ: <code>300</code>, <code>600</code>, <code>900</code></blockquote>\n\n<i>Tʀʏ ᴀɢᴀɪɴ ʙʏ ᴄʟɪᴄᴋɪɴɢ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ..</i></b>", reply_markup=InlineKeyboardMarkup(markup))

            except Exception as e:
                try:
                    await set_msg.reply(f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")
                    print(
                        f"! Error Occurred on callback data = 'set_timer' : {e}")
                except BaseException:
                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                    print(
                        f"! Error Occurred on callback data = 'set_timer' -> Rᴇᴀsᴏɴ: 1 minute Time out ..")

    elif data == 'chng_req':
        if await authoUser(query, query.from_user.id, owner_only=True):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            try:
                on = off = ""
                if await db.get_request_forcesub():
                    await db.set_request_forcesub(False)
                    off = "🔴"
                    texting = off_txt
                else:
                    await db.set_request_forcesub(True)
                    on = "🟢"
                    texting = on_txt

                button = [
                    [InlineKeyboardButton(f"{on} ON", "chng_req"), InlineKeyboardButton(
                        f"{off} OFF", "chng_req")],
                    [InlineKeyboardButton(
                        "⚙️ Mᴏʀᴇ Sᴇᴛᴛɪɴɢs ⚙️", "more_settings")]
                ]
                # 🎉)
                await query.message.edit_text(text=RFSUB_CMD_TXT.format(req_mode=texting), reply_markup=InlineKeyboardMarkup(button))

            except Exception as e:
                print(f"! Error Occurred on callback data = 'chng_req' : {e}")

    elif data == 'more_settings':
        if await authoUser(query, query.from_user.id, owner_only=True):
            # await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")
            try:
                await query.message.edit_text("<b>Pʟᴇᴀsᴇ wᴀɪᴛ !\n\n<i>🔄 Rᴇᴛʀɪᴇᴠɪɴɢ ᴀʟʟ Sᴇᴛᴛɪɴɢs...</i></b>")
                LISTS = "Eᴍᴘᴛʏ Rᴇǫᴜᴇsᴛ FᴏʀᴄᴇSᴜʙ Cʜᴀɴɴᴇʟ Lɪsᴛ !?"

                REQFSUB_CHNLS = await db.get_reqChannel()
                if REQFSUB_CHNLS:
                    LISTS = ""
                    channel_name = "<i>Uɴᴀʙʟᴇ Lᴏᴀᴅ Nᴀᴍᴇ..</i>"
                    for CHNL in REQFSUB_CHNLS:
                        await query.message.reply_chat_action(ChatAction.TYPING)
                        try:
                            name = (await client.get_chat(CHNL)).title
                        except BaseException:
                            name = None
                        channel_name = name if name else channel_name

                        user = await db.get_reqSent_user(CHNL)
                        channel_users = len(user) if user else 0

                        link = await db.get_stored_reqLink(CHNL)
                        if link:
                            channel_name = f"<a href={link}>{channel_name}</a>"

                        LISTS += f"NAME: {channel_name}\n(ID: <code>{CHNL}</code>)\nUSERS: {channel_users}\n\n"

                buttons = [
                    [InlineKeyboardButton("ᴄʟᴇᴀʀ ᴜsᴇʀs", "clear_users"), InlineKeyboardButton(
                        "cʟᴇᴀʀ cʜᴀɴɴᴇʟs", "clear_chnls")],
                    [InlineKeyboardButton(
                        "♻️  Rᴇғʀᴇsʜ Sᴛᴀᴛᴜs  ♻️", "more_settings")],
                    [InlineKeyboardButton("⬅️ Bᴀᴄᴋ", "req_fsub"), InlineKeyboardButton(
                        "Cʟᴏsᴇ ✖️", "close")]
                ]
                await query.message.reply_chat_action(ChatAction.CANCEL)
                await query.message.edit_text(text=RFSUB_MS_TXT.format(reqfsub_list=LISTS.strip()), reply_markup=InlineKeyboardMarkup(buttons))

            except Exception as e:
                print(
                    f"! Error Occurred on callback data = 'more_settings' : {e}")

    elif data == 'clear_users':
        # if await authoUser(query, query.from_user.id, owner_only=True) :
        # await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")
        try:
            REQFSUB_CHNLS = await db.get_reqChannel()
            if not REQFSUB_CHNLS:
                return await query.answer("Eᴍᴘᴛʏ Rᴇǫᴜᴇsᴛ FᴏʀᴄᴇSᴜʙ Cʜᴀɴɴᴇʟ !?", show_alert=True)

            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            REQFSUB_CHNLS = list(map(str, REQFSUB_CHNLS))
            buttons = [REQFSUB_CHNLS[i:i + 2]
                       for i in range(0, len(REQFSUB_CHNLS), 2)]
            buttons.insert(0, ['CANCEL'])
            buttons.append(['DELETE ALL CHANNELS USER'])

            user_reply = await client.ask(query.from_user.id, text=CLEAR_USERS_TXT, reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))

            if user_reply.text == 'CANCEL':
                return await user_reply.reply("<b><i>🆑 Cᴀɴᴄᴇʟʟᴇᴅ...</i></b>", reply_markup=ReplyKeyboardRemove())

            elif user_reply.text in REQFSUB_CHNLS:
                try:
                    await db.clear_reqSent_user(int(user_reply.text))
                    return await user_reply.reply(f"<b><blockquote>✅ Usᴇʀ Dᴀᴛᴀ Sᴜᴄᴄᴇssғᴜʟʟʏ Cʟᴇᴀʀᴇᴅ ғʀᴏᴍ Cʜᴀɴɴᴇʟ ɪᴅ: <code>{user_reply.text}</code></blockquote></b>", reply_markup=ReplyKeyboardRemove())
                except Exception as e:
                    return await user_reply.reply(f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ...\n<blockquote>Rᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())

            elif user_reply.text == 'DELETE ALL CHANNELS USER':
                try:
                    for CHNL in REQFSUB_CHNLS:
                        await db.clear_reqSent_user(int(CHNL))
                    return await user_reply.reply(f"<b><blockquote>✅ Usᴇʀ Dᴀᴛᴀ Sᴜᴄᴄᴇssғᴜʟʟʏ Cʟᴇᴀʀᴇᴅ ғʀᴏᴍ Aʟʟ Cʜᴀɴɴᴇʟ ɪᴅs</blockquote></b>", reply_markup=ReplyKeyboardRemove())
                except Exception as e:
                    return await user_reply.reply(f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ...\n<blockquote>Rᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())

            else:
                return await user_reply.reply(f"<b><blockquote>INVALID SELECTIONS</blockquote></b>", reply_markup=ReplyKeyboardRemove())

        except Exception as e:
            print(f"! Error Occurred on callback data = 'clear_users' : {e}")

    elif data == 'clear_chnls':
        # if await authoUser(query, query.from_user.id, owner_only=True)

        try:
            REQFSUB_CHNLS = await db.get_reqChannel()
            if not REQFSUB_CHNLS:
                return await query.answer("Eᴍᴘᴛʏ Rᴇǫᴜᴇsᴛ FᴏʀᴄᴇSᴜʙ Cʜᴀɴɴᴇʟ !?", show_alert=True)

            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            REQFSUB_CHNLS = list(map(str, REQFSUB_CHNLS))
            buttons = [REQFSUB_CHNLS[i:i + 2]
                       for i in range(0, len(REQFSUB_CHNLS), 2)]
            buttons.insert(0, ['CANCEL'])
            buttons.append(['DELETE ALL CHANNEL IDS'])

            user_reply = await client.ask(query.from_user.id, text=CLEAR_CHNLS_TXT, reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))

            if user_reply.text == 'CANCEL':
                return await user_reply.reply("<b><i>🆑 Cᴀɴᴄᴇʟʟᴇᴅ...</i></b>", reply_markup=ReplyKeyboardRemove())

            elif user_reply.text in REQFSUB_CHNLS:
                try:
                    chnl_id = int(user_reply.text)

                    await db.del_reqChannel(chnl_id)

                    try:
                        await client.revoke_chat_invite_link(chnl_id, await db.get_stored_reqLink(chnl_id))
                    except BaseException:
                        pass

                    await db.del_stored_reqLink(chnl_id)

                    return await user_reply.reply(f"<b><blockquote><code>{user_reply.text}</code> Cʜᴀɴɴᴇʟ ɪᴅ ᴀʟᴏɴɢ ᴡɪᴛʜ ɪᴛs ᴅᴀᴛᴀ sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ ✅</blockquote></b>", reply_markup=ReplyKeyboardRemove())
                except Exception as e:
                    return await user_reply.reply(f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ...\n<blockquote>Rᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())

            elif user_reply.text == 'DELETE ALL CHANNEL IDS':
                try:
                    for CHNL in REQFSUB_CHNLS:
                        chnl = int(CHNL)

                        await db.del_reqChannel(chnl)

                        try:
                            await client.revoke_chat_invite_link(chnl, await db.get_stored_reqLink(chnl))
                        except BaseException:
                            pass

                        await db.del_stored_reqLink(chnl)

                    return await user_reply.reply(f"<b><blockquote>Aʟʟ Cʜᴀɴɴᴇʟ ɪᴅs ᴀʟᴏɴɢ ᴡɪᴛʜ ɪᴛs ᴅᴀᴛᴀ sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ ✅</blockquote></b>", reply_markup=ReplyKeyboardRemove())

                except Exception as e:
                    return await user_reply.reply(f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ...\n<blockquote>Rᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())

            else:
                return await user_reply.reply(f"<b><blockquote>INVALID SELECTIONS</blockquote></b>", reply_markup=ReplyKeyboardRemove())

        except Exception as e:
            print(f"! Error Occurred on callback data = 'more_settings' : {e}")

    elif data == 'clear_links':
        # if await authoUser(query, query.from_user.id, owner_only=True) :
        # await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

        try:
            REQFSUB_CHNLS = await db.get_reqLink_channels()
            if not REQFSUB_CHNLS:
                return await query.answer("Nᴏ Sᴛᴏʀᴇᴅ Rᴇǫᴜᴇsᴛ Lɪɴᴋ Aᴠᴀɪʟᴀʙʟᴇ !?", show_alert=True)

            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

            REQFSUB_CHNLS = list(map(str, REQFSUB_CHNLS))
            buttons = [REQFSUB_CHNLS[i:i + 2]
                       for i in range(0, len(REQFSUB_CHNLS), 2)]
            buttons.insert(0, ['CANCEL'])
            buttons.append(['DELETE ALL REQUEST LINKS'])

            user_reply = await client.ask(query.from_user.id, text=CLEAR_LINKS_TXT, reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))

            if user_reply.text == 'CANCEL':
                return await user_reply.reply("<b><i>🆑 Cᴀɴᴄᴇʟʟᴇᴅ...</i></b>", reply_markup=ReplyKeyboardRemove())

            elif user_reply.text in REQFSUB_CHNLS:
                channel_id = int(user_reply.text)
                try:
                    try:
                        await client.revoke_chat_invite_link(channel_id, await db.get_stored_reqLink(channel_id))
                    except BaseException:
                        text = """<b>❌ Uɴᴀʙʟᴇ ᴛᴏ Rᴇᴠᴏᴋᴇ ʟɪɴᴋ !
<blockquote expandable>ɪᴅ: <code>{}</code></b>
<i>Eɪᴛʜᴇʀ ᴛʜᴇ ʙᴏᴛ ɪs ɴᴏᴛ ɪɴ ᴀʙᴏᴠᴇ ᴄʜᴀɴɴᴇʟ Oʀ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘʀᴏᴘᴇʀ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs</i></blockquote>"""
                        return await user_reply.reply(text=text.format(channel_id), reply_markup=ReplyKeyboardRemove())

                    await db.del_stored_reqLink(channel_id)
                    return await user_reply.reply(f"<b><blockquote><code>{channel_id}</code> Cʜᴀɴɴᴇʟs Lɪɴᴋ Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ ✅</blockquote></b>", reply_markup=ReplyKeyboardRemove())

                except Exception as e:
                    return await user_reply.reply(f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ...\n<blockquote>Rᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())

            elif user_reply.text == 'DELETE ALL REQUEST LINKS':
                try:
                    result = ""
                    for CHNL in REQFSUB_CHNLS:
                        channel_id = int(CHNL)
                        try:
                            await client.revoke_chat_invite_link(channel_id, await db.get_stored_reqLink(channel_id))
                        except BaseException:
                            result += f"<blockquote expandable><b><code>{channel_id}</code> Uɴᴀʙʟᴇ ᴛᴏ Rᴇᴠᴏᴋᴇ ❌</b>\n<i>Eɪᴛʜᴇʀ ᴛʜᴇ ʙᴏᴛ ɪs ɴᴏᴛ ɪɴ ᴀʙᴏᴠᴇ ᴄʜᴀɴɴᴇʟ Oʀ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘʀᴏᴘᴇʀ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs.</i></blockquote>\n"
                            continue
                        await db.del_stored_reqLink(channel_id)
                        result += f"<blockquote><b><code>{channel_id}</code> IDs Lɪɴᴋ Dᴇʟᴇᴛᴇᴅ ✅</b></blockquote>\n"

                    return await user_reply.reply(f"<b>⁉️ Oᴘᴇʀᴀᴛɪᴏɴ Rᴇsᴜʟᴛ:</b>\n{result.strip()}", reply_markup=ReplyKeyboardRemove())

                except Exception as e:
                    return await user_reply.reply(f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ...\n<blockquote>Rᴇᴀsᴏɴ:</b> {e}</blockquote>", reply_markup=ReplyKeyboardRemove())

            else:
                return await user_reply.reply(f"<b><blockquote>INVALID SELECTIONS</blockquote></b>", reply_markup=ReplyKeyboardRemove())

        except Exception as e:
            print(f"! Error Occurred on callback data = 'more_settings' : {e}")

    elif data == 'req_fsub':
        # if await authoUser(query, query.from_user.id, owner_only=True) :
        await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")

        try:
            on = off = ""
            if await db.get_request_forcesub():
                on = "🟢"
                texting = on_txt
            else:
                off = "🔴"
                texting = off_txt

            button = [
                [InlineKeyboardButton(f"{on} ON", "chng_req"), InlineKeyboardButton(
                    f"{off} OFF", "chng_req")],
                [InlineKeyboardButton("⚙️ Mᴏʀᴇ Sᴇᴛᴛɪɴɢs ⚙️", "more_settings")]
            ]
            # 🎉)
            await query.message.edit_text(text=RFSUB_CMD_TXT.format(req_mode=texting), reply_markup=InlineKeyboardMarkup(button))

        except Exception as e:
            print(f"! Error Occurred on callback data = 'chng_req' : {e}")
    elif data == "fsub_main":
        if await authoUser(query, query.from_user.id):
            button = [
                [InlineKeyboardButton("➕ Add Channel", callback_data="fsub_add"), InlineKeyboardButton("➖ Remove Channel", callback_data="fsub_remove")],
                [InlineKeyboardButton("📋 List Channels", callback_data="fsub_list")],
                [InlineKeyboardButton("Cʟᴏsᴇ ✖️", callback_data="close")]
            ]
            await query.message.edit_text(text="<b>🤖 Force Subscription Settings:</b>\n\nManage your force sub channels below. You can add up to 5 channels.", reply_markup=InlineKeyboardMarkup(button))

    elif data == "fsub_add":
        if await authoUser(query, query.from_user.id):
            channels = await db.get_all_channels()
            if len(channels) >= 5:
                await query.answer("❌ You can only add up to 5 force sub channels.", show_alert=True)
                return

            try:
                user_id = query.from_user.id
                prompt_msg = await client.ask(
                    chat_id=user_id,
                    text="<b>Please send the Channel ID you want to add for force sub:</b>\n\n<i>Make sure the bot is an admin in that channel before sending the ID.</i>",
                    timeout=60
                )
                
                channel_id_str = prompt_msg.text.strip()
                try:
                    channel_id = int(channel_id_str)
                except ValueError:
                    await prompt_msg.reply("❌ Invalid Channel ID format. Please try again.")
                    return

                if channel_id in channels:
                    await prompt_msg.reply("❌ This channel is already added.")
                    return

                try:
                    from pyrogram.enums import ChatMemberStatus
                    chat = await client.get_chat(channel_id)
                    member = await client.get_chat_member(channel_id, client.me.id)
                    
                    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                         await prompt_msg.reply("❌ The bot is not an admin in the specified channel. Please promote the bot to admin and try again.")
                         return

                except Exception as e:
                    await prompt_msg.reply(f"❌ Error verifying channel: {e}\n\nPlease ensure the ID is correct and the bot is an admin in the channel.")
                    return

                button = [
                    [InlineKeyboardButton("Direct Force Sub", callback_data=f"fsub_set_{channel_id}_direct")],
                    [InlineKeyboardButton("Request Force Sub", callback_data=f"fsub_set_{channel_id}_request")],
                    [InlineKeyboardButton("Cancel", callback_data="fsub_main")]
                ]
                await prompt_msg.reply(
                    f"<b>Channel Verified: {chat.title}</b>\n\nChoose the type of force sub you want to set up:",
                    reply_markup=InlineKeyboardMarkup(button)
                )

            except asyncio.TimeoutError:
                await client.send_message(user_id, "⏳ Request timed out.")
            except Exception as e:
                logging.error(f"Error in fsub_add: {e}")
                await client.send_message(user_id, "❌ An error occurred.")

    elif data.startswith("fsub_set_"):
        if await authoUser(query, query.from_user.id):
            parts = data.split("_")
            channel_id = int(parts[2])
            mode = parts[3]

            await db.add_channel(channel_id)

            if mode == "request":
                await db.set_request_forcesub_channel(channel_id, True)
                await db.add_reqChannel(channel_id)
                try:
                    link = (await client.create_chat_invite_link(chat_id=channel_id, creates_join_request=True)).invite_link
                    await db.store_reqLink(channel_id, link)
                except Exception as e:
                    logging.error(f"Failed to create join request link for {channel_id}: {e}")
                    await query.answer("⚠️ Channel added, but failed to create join request link. Ensure the bot has correct permissions.", show_alert=True)
            else:
                await db.set_request_forcesub_channel(channel_id, False)

            mode_text = 'Request' if mode == 'request' else 'Direct'
            await query.message.edit_text(
                f"✅ <b>Channel {channel_id} successfully added as {mode_text} Force Sub!</b>",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="fsub_main")]])
            )

    elif data == "fsub_remove":
        if await authoUser(query, query.from_user.id):
            channels = await db.get_all_channels()
            if not channels:
                await query.answer("❌ No force sub channels found.", show_alert=True)
                return

            buttons = []
            for channel_id in channels:
                try:
                    chat = await client.get_chat(channel_id)
                    title = chat.title
                except:
                    title = str(channel_id)
                buttons.append([InlineKeyboardButton(f"❌ Remove {title}", callback_data=f"fsub_del_{channel_id}")])
            
            buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="fsub_main")])
            
            await query.message.edit_text(
                "<b>Select a channel to remove:</b>",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    elif data.startswith("fsub_del_"):
        if await authoUser(query, query.from_user.id):
            channel_id = int(data.split("_")[2])
            
            try:
                stored_link = await db.get_stored_reqLink(channel_id)
                if stored_link:
                    await client.revoke_chat_invite_link(channel_id, stored_link)
            except Exception:
                pass

            await db.del_channel(channel_id)
            await db.del_reqChannel(channel_id)
            await db.del_stored_reqLink(channel_id)

            await query.answer("✅ Channel removed successfully.", show_alert=True)
            
            query.data = "fsub_remove"
            await cb_handler(client, query)

    elif data == "fsub_list":
        if await authoUser(query, query.from_user.id):
            channels = await db.get_all_channels()
            if not channels:
                await query.message.edit_text(
                    "<b>📋 Force Sub Channels:</b>\n\nNo channels configured.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="fsub_main")]])
                )
                return

            text = "<b>📋 Force Sub Channels:</b>\n\n"
            for channel_id in channels:
                try:
                    chat = await client.get_chat(channel_id)
                    title = chat.title
                except:
                    title = "Unknown Channel"
                
                is_req = await db.get_request_forcesub_channel(channel_id)
                mode_str = "Request" if is_req else "Direct"
                text += f"◈ <b>{title}</b> (<code>{channel_id}</code>) - Mode: <i>{mode_str}</i>\n"

            await query.message.edit_text(
                text,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="fsub_main")]])
            )

    

    # Handle shortener settings
    elif data == "shortener_settings":
        if await authoUser(query, query.from_user.id, owner_only=True):
            try:
                await query.answer("💫 Fetching Shortener details...")

            # Fetch shortener details
                shortener_url = await db.get_shortener_url()
                shortener_api = await db.get_shortener_api()
                verified_time = await db.get_verified_time()
                tut_video = await db.get_tut_video()

            # Prepare the details for display
                shortener_url_display = shortener_url or "Not set"
                shortener_api_display = shortener_api or "Not set"
                status = "Active" if shortener_url and shortener_api else "Inactive"
                verified_time_display = (
                    f"{verified_time} seconds" if verified_time else "Not set"
                )
                tut_video_display = (
                    f"[Tutorial Video]({tut_video})" if tut_video else "Not set"
                )

            # Response message
                response_text = (
                    f"𝗦𝗵𝗼𝗿𝘁𝗲𝗻𝗲𝗿 𝗗𝗲𝘁𝗮𝗶𝗹𝘀\n\n"
                    f"Sɪᴛᴇ: {shortener_url_display}\n"
                    f"API Tᴏᴋᴇɴ:  {shortener_api_display}\n"
                    f"Sᴛᴀᴛᴜs: {status}\n\n"
                    f"Vᴇʀɪғɪᴇᴅ Tɪᴍᴇ:  {verified_time_display}\n"
                    f"Tᴜᴛᴏʀɪᴀʟ Vɪᴅᴇᴏ: {tut_video_display}"
                )

            # Update the message with the fetched details
                await query.message.edit_text(
                    text=response_text,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton('🔙', callback_data='set_shortener')]
                    ]),
                    disable_web_page_preview=True  # Disable preview for tutorial video link
                )

            except Exception as e:
                logging.error(f"Error fetching shortener settings: {e}")
                await query.message.reply(
                    "⚠️ An error occurred while fetching shortener settings. Please try again later.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton('Back', callback_data='set_shortener')]
                    ])
                )


    elif data == "chng_shortener": 
        user_id = query.from_user.id
        shortener_details = await db.get_shortener()

    # Toggle the shortener status in the database
        if shortener_details:
        # Disable shortener
            await db.set_shortener("", "")
            await query.answer("Shortener Disabled ❌", show_alert=True)
        else:
        # Enable shortener, prompt for URL and API Key
            await query.answer("Shortener Enabled ✅. Please provide the Shortener URL and API Key.", show_alert=True)
            await query.message.reply("Send the Shortener URL and API Key in the format:\n`<shortener_url> <api_key>`")

    


    elif data == 'set_shortener_details':
        if await authoUser(query, query.from_user.id, owner_only=True):
            try:
                await query.answer("Please send the shortener URL within 1 minute...")
                set_msg_url = await query.message.reply(
                    "⏳ Please provide the Shortener site URL (e.g., https://example.com) within 1 minute.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Back', callback_data='set_shortener')]])
                )
                site_msg = await client.ask(
                    chat_id=query.from_user.id,
                    text="⏳ Enter Shortener site URL:",
                    timeout=60
                )

                shortener_url = site_msg.text.strip()


            # Confirm the shortener site URL
                await site_msg.reply(f"Shortener site URL set to: {shortener_url}\nNow please send the API key.")

            # Step 3: Prompt for API key
                set_msg_api = await query.message.reply(
                    "⏳ Please provide the API key for the shortener within 1 minute.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Back', callback_data='set_shortener')]])
                )

                api_msg = await client.ask(
                    chat_id=query.from_user.id,
                    text="⏳ Enter API key for the shortener:",
                    timeout=60
                )

                api_key = api_msg.text.strip()

            # Step 4: Save the shortener details in the database
                await db.set_shortener_url(shortener_url)
                await db.set_shortener_api(api_key)
            
            # Confirmation message
                await api_msg.reply(
                    "✅ Shortener details have been successfully set!",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton('◈ Disable Shortener ❌', callback_data='disable_shortener')],
                        [InlineKeyboardButton('Back', callback_data='set_shortener')]
                    ])
                )
            except asyncio.TimeoutError:
                await query.message.reply(
                    "⚠️ You did not provide the details in time. Please try again.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Back', callback_data='set_shortener')]])
                )
            except Exception as e:
                logging.error(f"Error setting shortener details: {e}")  # This now works correctly
                await query.message.reply(
                    f"⚠️ Error occurred: {e}",
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Back', callback_data='set_shortener')]])
    )


    elif data == "set_shortener":
        if await authoUser(query, query.from_user.id, owner_only=True):
            try:
                message = query.message

                shortener_url = await db.get_shortener_url()
                shortener_api = await db.get_shortener_api()

                if shortener_url and shortener_api:
                    shortener_status = "Enabled ✅"
                    mode_button = InlineKeyboardButton('Disable Shortener ❌', callback_data='disable_shortener')
                else:
                    shortener_status = "Disabled ❌"
                    mode_button = InlineKeyboardButton('Enable Shortener ✅', callback_data='set_shortener_details')

            # Edit the same message instead of sending a new one
                await message.edit_media(
                    media=InputMediaPhoto(
                        media=START_PIC,
                        caption=SET_SHORTENER_CMD_TXT.format(shortener_status=shortener_status),
                        parse_mode=ParseMode.HTML
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [mode_button],
                        [
                            InlineKeyboardButton('Settings ⚙️', callback_data='shortener_settings'),
                            InlineKeyboardButton('🔄 Refresh', callback_data='set_shortener')
                        ],
                        [
                            InlineKeyboardButton('Set Verified Time ⏱', callback_data='set_verify_time'),
                            InlineKeyboardButton('Set Tutorial Video 🎥', callback_data='set_tut_video')
                        ],
                        [InlineKeyboardButton('Close ✖️', callback_data='close')]
                    ])
                )

            except Exception as e:
                await query.message.edit_text(
                    f"<b>! Error Occurred..\n<blockquote>Reason:</b> {e}</blockquote><b><i>Contact developer: @rohit_1888</i></b>",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Close ✖️", callback_data="close")]]
                    )
                )

    elif data == "set_tut_video":
        id = query.from_user.id

        if await authoUser(query, id, owner_only=True):
            await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....")
        
            try:
            # Fetch the current tutorial video URL from the database
                current_video_url = await db.get_tut_video()

            # Prompt the user to input the new tutorial video URL
                set_msg = await client.ask(
                    chat_id=id,
                    text=f'<b><blockquote>⏳ Cᴜʀʀᴇɴᴛ Tᴜᴛᴏʀɪᴀʟ Vɪᴅᴇᴏ URL: {current_video_url if current_video_url else "Not Set"}</blockquote>\n\nTᴏ ᴄʜᴀɴɢᴇ, Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴠɪᴅᴇᴏ URL.\n<blockquote>Fᴏʀ ᴇxᴀᴍᴘʟᴇ: <code>https://youtube.com/some_video</code></b></blockquote>',
                    timeout=60
                )

            # Validate the user input for a valid URL
                video_url = set_msg.text.strip()

                if video_url.startswith("http") and "://" in video_url:
                # Save the new tutorial video URL to the database
                    await db.set_tut_video(video_url)

                # Confirm the update to the user
                    await set_msg.reply(f"<b><i>Tᴜᴛᴏʀɪᴀʟ Vɪᴅᴇᴏ URL sᴇᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ✅</i>\n<blockquote>📹 Cᴜʀʀᴇɴᴛ Tᴜᴛᴏʀɪᴀʟ Vɪᴅᴇᴏ URL: {video_url}</blockquote></b>")
                else:
                # If the URL is invalid, prompt the user to try again
                    markup = [[InlineKeyboardButton(
                        '◈ Sᴇᴛ Tᴜᴛᴏʀɪᴀʟ Vɪᴅᴇᴏ URL 📹', callback_data='set_tut_video')]]
                    return await set_msg.reply(
                        "<b>Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ʟɪɴᴋ ᴛᴏ ᴀ ᴠᴀʟɪᴅ ᴠɪᴅᴇᴏ.\n<blockquote>Fᴏʀ ᴇxᴀᴍᴘʟᴇ: <code>https://youtube.com/some_video</code></blockquote>\n\n<i>Tʀʏ ᴀɢᴀɪɴ ʙʏ ᴄʟɪᴄᴋɪɴɢ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ..</i></b>", reply_markup=InlineKeyboardMarkup(markup))

            except Exception as e:
                try:
                # Handle any exceptions that occur during the process
                    await set_msg.reply(f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")
                    print(f"! Error Occurred on callback data = 'set_tut_video' : {e}")
                except BaseException:
                # If an error occurs while sending the error message, send a timeout message
                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                    print(f"! Error Occurred on callback data = 'set_tut_video' -> Reason: 1 minute Time out ..")


    elif data == 'set_verify_time':
        id = query.from_user.id

        if await authoUser(query, id, owner_only=True):
            await query.answer("♻️ Processing request...")

            try:
                # Fetch the current verified time from the database
                current_verify_time = await db.get_verified_time()
                time_display = f"{current_verify_time} seconds" if current_verify_time else "Not set"

                # Prompt the user to input a new verified time
                set_msg = await client.ask(
                    chat_id=id,
                    text=(
                        f"<b><blockquote>⏱ Current Timer: {time_display}</blockquote>\n\n"
                        f"To change the timer, please send a valid number in seconds within 1 minute.\n"
                        f"<blockquote>For example: <code>300</code>, <code>600</code>, <code>900</code></blockquote></b>"
                    ),
                    timeout=60
                )

                # Validate the user input
                verify_time_input = set_msg.text.strip()
                if verify_time_input.isdigit():
                    verify_time = int(verify_time_input)

                    # Save the new verified time to the database
                    await db.set_verified_time(verify_time)
                    formatted_time = f"{verify_time} seconds"
                    
                    # Confirm the update to the user
                    await set_msg.reply(
                        f"<b><i>Timer updated successfully ✅</i>\n"
                        f"<blockquote>⏱ Current Timer: {formatted_time}</blockquote></b>"
                    )
                else:
                    # Handle invalid input
                    markup = [[InlineKeyboardButton('◈ Set Verify Timer ⏱', callback_data='set_verify_time')]]
                    return await set_msg.reply(
                        "<b>Please send a valid number in seconds.\n"
                        "<blockquote>For example: <code>300</code>, <code>600</code>, <code>900</code></blockquote>\n\n"
                        "<i>Try again by clicking the button below.</i></b>",
                        reply_markup=InlineKeyboardMarkup(markup)
                    )

            except asyncio.TimeoutError:
                # Handle timeout if user doesn't respond in time
                await client.send_message(
                    id,
                    text="<b>⚠️ Timeout occurred. You did not respond within the time limit.</b>",
                    disable_notification=True
                )
            except Exception as e:
                # Handle any other exceptions
                await client.send_message(
                    id,
                    text=f"<b>⚠️ Error occurred:\n<blockquote>{e}</blockquote></b>",
                    disable_notification=True
                )
                print(f"! Error occurred on callback data = 'set_verify_time' : {e}")



    elif data == "enable_shortener":
        await query.answer()

        try:
            # Check if shortener details are already set
            shortener_url = await db.get_shortener_url()
            shortener_api = await db.get_shortener_api()

            if shortener_url and shortener_api:
                # Enable the shortener
                success_url = await db.set_shortener_url(shortener_url)
                success_api = await db.set_shortener_api(shortener_api)

                if success_url and success_api:
                    await query.edit_message_caption(
                        caption="Shortener has been enabled ✅",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton('Disable Shortener ❌', callback_data='disable_shortener')],
                            [InlineKeyboardButton('Close ✖️', callback_data='close')]
                        ])
                    )
                else:
                    await query.message.reply(
                        "Failed to enable the shortener. Please try again."
                    )
            else:
                # If no shortener details are found, prompt the user to set them
                await query.edit_message_caption(
                    caption="No shortener details found. Please set the shortener details first.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton('Set Shortener Details', callback_data='set_shortener_details')],
                        [InlineKeyboardButton('Close ✖️', callback_data='close')]
                    ])
                )
        except Exception as e:
            logging.error(f"Error enabling shortener: {e}")
            await query.message.reply(
                "An unexpected error occurred while enabling the shortener. Please try again later."
            )

    elif data == "disable_shortener":
        await query.answer()
    
    # Deactivate the shortener
        success = await db.deactivate_shortener()
        if success:
            await query.edit_message_caption(
                caption="Shortener has been disabled ❌",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('Enable Shortener ✅', callback_data='enable_shortener')],
                    [InlineKeyboardButton('Close ✖️', callback_data='close')]
                ])
            )
        else:
            await query.message.reply("Failed to disable the shortener. Please try again.")
    

    
    