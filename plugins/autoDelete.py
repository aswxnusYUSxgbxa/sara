import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

#Time conversion for auto delete timer
def convert_time(duration_seconds: int) -> str:
    periods = [
        ('Year', 60 * 60 * 24 * 365),
        ('Month', 60 * 60 * 24 * 30),
        ('Day', 60 * 60 * 24),
        ('Hour', 60 * 60),
        ('Minute', 60),
        ('Second', 1)
    ]

    parts = []
    for period_name, period_seconds in periods:
        if duration_seconds >= period_seconds:
            num_periods = duration_seconds // period_seconds
            duration_seconds %= period_seconds
            parts.append(f"{num_periods} {period_name}{'s' if num_periods > 1 else ''}")

    if len(parts) == 0:
        return "0 Second"
    elif len(parts) == 1:
        return parts[0]
    else:
        return ', '.join(parts[:-1]) +' and '+ parts[-1]


#=====================================================================================##
#.........Auto Delete Functions.......#
#=====================================================================================##
DEL_MSG = """<b>⚠️ Due to Copyright issues....
<blockquote>Your files will be deleted within <a href="https://t.me/{username}">{time}</a>. So please forward them to any other place for future availability.</blockquote></b>"""

#Function for provide auto delete notification message
async def auto_del_notification(bot_username, msg, delay_time, transfer, is_batch=False, all_messages=None):
    # For batches, use the last message for notification
    notification_msg = msg
    if is_batch and all_messages and isinstance(all_messages, list) and len(all_messages) > 0:
        notification_msg = all_messages[-1]

    temp = await notification_msg.reply_text(DEL_MSG.format(username=bot_username, time=convert_time(delay_time)), disable_web_page_preview = True)

    await asyncio.sleep(delay_time)
    try:
        if transfer:
            try:
                name = "🔄 Get Again"
                button = [
                    [InlineKeyboardButton(text=name, callback_data=f"get_again_{transfer}"), InlineKeyboardButton(text="Close ✖️", callback_data="close")]
                ]
                await temp.edit_text(text=f"<b>Previous Message was Deleted \n<blockquote>If you want to get the files again, then click the button below else close this message.</blockquote></b>", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview = True)

            except Exception as e:
                await temp.edit_text(f"<b><blockquote>Previous Message was Deleted </blockquote></b>")
                print(f"Error occured while editing the Delete message: {e}")
        else:
            button = [[InlineKeyboardButton(text="Close ✖️", callback_data="close")]]
            await temp.edit_text(f"<b><blockquote>Previous Message was Deleted </blockquote></b>", reply_markup=InlineKeyboardMarkup(button))

    except Exception as e:
        print(f"Error occured while editing the Delete message: {e}")
        await temp.edit_text(f"<b><blockquote>Previous Message was Deleted </blockquote></b>")

    # Delete all messages in batch if it's a batch
    if is_batch and all_messages and isinstance(all_messages, list):
        for message in all_messages:
            try:
                await message.delete()
            except Exception as e:
                print(f"Error occurred deleting message in batch: {e}")
    else:
        # Delete single message
        try:
            await msg.delete()
        except Exception as e:
            print(f"Error occurred on auto_del_notification() : {e}")


#Function for deleteing files/Messages.....
async def delete_message(msg, delay_time):
    await asyncio.sleep(delay_time)

    try: await msg.delete()
    except Exception as e: print(f"Error occurred on delete_message() : {e}")
