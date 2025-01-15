from os.path import join

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    CallbackContext,
)
from telegram.error import TimedOut, NetworkError
import logging
import asyncio

from telegram.request import HTTPXRequest

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Welcome message and buttons
async def start(update: Update, context: CallbackContext) -> None:
    # Check if the update is from a callback query (e.g., "Back" button)
    if update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat.id
        await query.answer()  # Acknowledge the callback query
    else:
        chat_id = update.message.chat.id

    # Get the user's first and last name
    user = update.effective_user  # Works for both message and callback_query
    first_name = user.first_name
    last_name = user.last_name or ""  # Handle case where last_name is None
    full_name = f"{first_name} {last_name}".strip()  # Combine first and last name

    # Store the full name in context.user_data for later use
    context.user_data["full_name"] = full_name
    welcome_text = (f"👋 {full_name} <b>እንኳን ደህና መጡ!\n</b>\n ይህ ኦላይን ስራ ብዙ ሰዎችን የቀየረና ብዙ ሰዎች እየተቀየሩበት ያለ ቢዝነስ ሲሆን እናንተም "
                    f"አምናችሁበት ወደ ስራ የምትገቡ ከሆነ ነገ ከነገ ወዲያ እንደምታመሰግኑን ምንም አንጠራጠርም። ከናንተ የሚጠበቀው እዚህ ቦት ላይ የተቀመጡትን "
                    f"ቅደም ተከተሎች ብትክክል ተከትላቹ "
                    f"ሙሉ ምዝገባ ማድረግና ስለ ሙሉ ስራው መረጃ ማግኘት ነው። \n\n"
                    f"‼️ <b>ልብ ይበሉ ይህንን የኦንላይን ስራ ለመሥራት ይህንን ቦት ብቻ ይጠቀሙ!</b>"
                    f"\n\n እባክዎ የሚፈልጉትን በመምረጥ ይቀጥሉ:")
    buttons = [
        ['አዲስ ከሆኑ እዚህ ይጫኑ'],
        ['💰 ፖይንት/ኮይን መስራት'],
        ['level ማሳደግ', 'ኤጀንሲ ለመመዝገብ'],
        ['ኤጀንሲ', "live ለመግባት", 'other/ሌሎች']
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    await context.bot.send_message(chat_id=chat_id, text=welcome_text, reply_markup=reply_markup, parse_mode="HTML")


# Show buttons without welcome text
async def show_buttons(update: Update, context: CallbackContext) -> None:
    buttons = [
        ['አዲስ ከሆኑ እዚህ ይጫኑ'],
        ['💰 ፖይንት/ኮይን መስራት'],
        ['level ማሳደግ', 'ኤጀንሲ ለመመዝገብ'],
        ['ኤጀንሲ', "live ለመግባት", 'other/ሌሎች']
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("❌ የተሳሳተ አማራጭ አስገብተዋል.\n\nእባክዎ ደግመው ምርጫዎን በትክክል ያስገቡ:", reply_markup=reply_markup)


# Handle button responses
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_choice = update.message.text
    full_name = context.user_data.get("full_name", "User")

    if user_choice == 'አዲስ ከሆኑ እዚህ ይጫኑ':
        app_link = """
    (a) https://aaaonline.info/WDDYkC
    (b) https://aaaonline.info/6AMfj2
    (c) https://aaaonline.info/JmCeEN
    (d) https://aaaonline.info/xan8NM

<b>ከላይ የተዘረዘሩት ሊንኮች ካልሰሩ</b> <a href="https://play.google.com/store/apps/details?id=com.baitu.qingshu"><ins>እዚህ 
ያውርዱ</ins> ⬅️⬅️</a>"""

        keyboard = [
            [InlineKeyboardButton("Register ለማድረግ", callback_data="register")],
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_text = (f"🎉 እንኳን ደህና መጡ {full_name}!\n\n"
                        f"1, ቀጥለው ከተዘረዘሩት ሊንኮች አንዱን በመንካት አፑን ወደ ስልክዎ ይጫኑ (አንዱ ሊንክ ካልሰራ በሌላኛው ይሞክሩት) ⬇️⬇️\n {app_link}\n\n"
                        "2. አፑን ወደ ስልክዎ ከጫኑ ብዋላ ከዚህ በታች ከ ቪደዎው ቀጥሎ ያለውን Register ለማድረግ የሚለውን ጠቅ ያድርጉ ⬇️⬇️")

        await update.message.reply_text(message_text,
                                        parse_mode="HTML",
                                        disable_web_page_preview=True
                                        )
        await update.message.reply_text("3. ተጨማሪ ማብራሪያ ካስፈለግዎ ቀጥሎ የተቀመጠዉን ቪዲዎ ይመልከቱ\n"
                                        "    https://youtu.be/DQK4E6-vwKU?si=UL_h6X5rYHfOmtBB",
                                        reply_markup=reply_markup,
                                        disable_web_page_preview=False,
                                        )

    elif user_choice == '💰 ፖይንት/ኮይን መስራት':
        keyboard = [
            [InlineKeyboardButton("የፊት አሻራ ለመስጠት", callback_data="face_authentication")],
            [InlineKeyboardButton("ወደ ታስክ/To tasks", callback_data='to_tasks')],
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        coin_instructions = (
            "የፊት አሻራ/Face Authentication ጨርሰዋል❓❓\n"
            "‼️ <b>ልብ ይበሉ የፊት አሻራ ካልሰጡ አፑ ላይ ታስክ መስራት/ገንዘብ ማግኘት አይችሉም</>\n\n"
            "   ➡️ የፊት አሻራ ካልሰጡ <b>የፊት አሻራ ለመስጠት</b> የሚለዉን ጠቅ ያድርጉ\n"
            "   ➡️ የፊት አሻራ ሰተው ጨርሰዉ ከሆነ <b>ወደ ታስክ/To tasks</b> የሚለዉን ጠቅ ያድርጉ\n"
        )
        await update.message.reply_text(coin_instructions, reply_markup=reply_markup, parse_mode="HTML")

    else:
        await show_buttons(update, context)


# Handle callback query for inline buttons
async def handle_callback_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    if query.data == "register":
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        app_icon_img = join("images", "app_icon.jpg")
        await query.message.reply_text("✅ እባክዎ Register ለማድረግ የሚከተሉትን መመሪያዎች በአግባቡ ይከተሉ:\n\n")

        with open(app_icon_img, "rb") as app_icon:
            await query.message.reply_photo(photo=InputFile(app_icon), caption="1. አፑን ወደ ስልክዎ ከጫኑ ብዋላ ይክፈቱት")

        open_app_img = join("images", "open_app.jpg")
        with open(open_app_img, "rb") as open_app:
            await query.message.reply_photo(photo=InputFile(open_app), caption="2. አፑን ከከፈቱት ብዋላ የሚመጣው ስክሪን ላይ "
                                                                               "google ወይም Facebook ከሚሉት በተኖች አንዱን "
                                                                               "በመምረጥ እና ተያያዥ የሆነ ጂሜል ወይም ፌስቡክ አካዉንት "
                                                                               "በማስገባት ከዚያም መጨረሻ ላይ በመሄድ ☑️ I agree "
                                                                               "የምትለውን ቦክስ ጠቅ ያድርጉ")

        register_img = join("images", "register.jpg")
        with open(register_img, "rb") as reg_img:
            await query.message.reply_photo(photo=InputFile(reg_img), caption="3. ከዚያም ቀጥሎ የሚመጣው ፎርም ላይ የግል መረጃዎችን ("
                                                                              "ሙሉ ስም, የትውልድ ዘመን, ሀገር እና ፆታ) በትክክል "
                                                                              "ካስገቡ ብዋላ submit የሚለውን ጠቅ ያድርጉ።")
        await query.message.reply_text(
            "4. submit ሲሉት ካስቸገርዎ ያስገቧቸዉን መረጃዎች "
            "ትክክለኛነት ያረጋግጡ (ማብራሪያ ካስፈለግዎ የሚከተለውን "
            "ቪዲዎ ይመልከቱ) ⬇️⬇️\n"
            "https://youtu.be/3JsEA4r_YbI?si"
            "=QR2jL4B8L9E0xQgi",
            disable_web_page_preview=False,
            reply_markup=reply_markup
        )

    elif query.data == "face_authentication":
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        auth_start_pg = join("images/face_auth", "auth_start_pg.jpg")
        await query.message.reply_text("✅ እባክዎ የፊት አሻራ ለመጨረስ አፑን ከከፈቱት ብዋላ የሚከተሉትን መመሪያዎች በአግባቡ ይከተሉ:\n\n")

        with open(auth_start_pg, "rb") as auth_start:
            await query.message.reply_photo(photo=InputFile(auth_start), caption="1. ልክ ምስሉ ላይ እንዳለው በቁጥሮቹ መሰረት ቁልፎቹን "
                                                                                 "ይጫኑ")

        face_auth_btn = join("images/face_auth", "face_auth_btn.jpg")
        with open(face_auth_btn, "rb") as face_auth:
            await query.message.reply_photo(photo=InputFile(face_auth), caption="2. ልክ ምስሉ ላይ እንዳለው face "
                                                                                "authentication ላይ go የሚለውን ቁልፍ ጠቅ "
                                                                                "ያድርጉ")

        upload_pro_btn = join("images/face_auth", "upload_pro_btn.jpg")
        with open(upload_pro_btn, "rb") as upl_pro:
            await query.message.reply_photo(photo=InputFile(upl_pro), caption="3. ከዚያም ምስሉ ላይ እንደሚታየው 'upload photo "
                                                                              "of your self' የሚለውን ቁልፍ ጠቅ ያድርጉ")

        auth_photo = join("images/face_auth", "auth_photo.jpg")
        with open(auth_photo, "rb") as auth_pic:
            await query.message.reply_photo(photo=InputFile(auth_pic), caption="4. ከዚያም ምስሉ ላይ እንደሚታየው የራስዎን ምስል "
                                                                               "አስታካክለው ያስገቡ"
                                            )

        start_cert = join("images/face_auth", "start_certificate.jpg")
        with open(start_cert, "rb") as str_cert:
            await query.message.reply_photo(photo=InputFile(str_cert), caption="5. ምስልዎን በትክክል ካስገቡ ብዋላ ከላይ ያለው ምስል "
                                                                               "ላይ እንደሚታየው 'start certificate' የሚለውን "
                                                                               "ቁልፍ ይጫኑ"
                                            )

        face_cert = join("images/face_auth", "face_certificate.jpg")
        with open(face_cert, "rb") as fc_id:
            await query.message.reply_photo(photo=InputFile(fc_id), caption="6. ከዚያም ልክ ከላይ ምስሉ ላይ እንዳለው ፊትዎን አፑ "
                                                                            "በሚነግርዎ መሰረት ስካን ያድርጉ\n ተጨማሪ ማብራሪያ "
                                                                            "ካስፈልግዎ ቀጥሎ ያለዉን ቪዲዮ ይመልከቱ "
                                                                            "⬇️⬇️\nhttps://youtu.be/3JsEA4r_YbI?si"
                                                                            "=QR2jL4B8L9E0xQgi",
                                            reply_markup=reply_markup
                                            )

    elif query.data == 'to_tasks':
        keyboard = [
            [InlineKeyboardButton("ሴት", callback_data="female_task")],
            [InlineKeyboardButton("ወንድ", callback_data='male_tasks')],
            [InlineKeyboardButton("የጋራ (ለሴትም ለወንድም)", callback_data='common_task')],
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        coin_instructions = (
            "✅ <b>እዚህ አፕ ላይ ታስኮች የሴት የወንድ እና የጋራ ተብለው የተከፈሉ ናቸዉ</b>\n\n"
            "   ስለዚህ ከዚህ በታች ካሉት አማራጮች ከርስዎ ጋር የሚሄደዉን ይምረጡ ⬇️⬇️"
        )
        await query.message.reply_text(coin_instructions, reply_markup=reply_markup,
                                       parse_mode="HTML")

    elif query.data == 'female_task':
        # Create two buttons for female tasks
        keyboard = [
            [InlineKeyboardButton("አዲስ (ሴት)", callback_data="new_female_task")],
            [InlineKeyboardButton("ነባር (ሴት)", callback_data="existed_female_task")],
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send a message with the buttons
        await query.message.reply_text(
            "<b> መልካም ዜና ‼️ ይህ አፕ ሴቶችን በተለዬ መንገድ ያበረታታል።\n\n✅ለሴቶች የተዘጋጁ ታስኮች ለአዲሶች እና ለነባሮች ተብለው የተከፈሉ ናቸዉ። "
            "ስለዚህ፡</b>\n\n"
            "አዲስ ከሆኑ <b>አዲስ</b> የሚለውን ነባር ከሆኑ (እዚህ አፕ ላይ ተመዝግበው 7 ቀን እና ከዛ በላይ ከሆንዎ) <b>ነባር</b> የሚለውን ይንኩ⬇️⬇️",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

    elif query.data == 'new_female_task':
        keyboard = [
            [InlineKeyboardButton("ላይቭ (ለአዲስ ሴት)", callback_data="live_new_female")],
            [InlineKeyboardButton("ፓርቲ (ለአዲስ ሴት)", callback_data="party_new_female")],
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text("✅  <b>ቀጥሎ ከተዘረዘሩት ታስክ ይምረጡ (ለአዲስ ሴት)</b>",
                                       parse_mode="HTML",
                                       reply_markup=reply_markup
                                       )

    elif query.data == 'live_new_female':
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("✅ <b>ይህ አፕ ሴቶችን በተለይም ጀማሪ ሴቶችን ተጨማሪ ነጥቦችን/points በመስጠት በተለዬ መንገድ "
                                       "ያበረታታል። ይህም የሚቆየው ኦፑ ላይ ከተመዘገቡበት ጊዜ አንስቶ ከ3 እስከ 7 ቀን ነው።\n\n"
                                       "✅ አፑ ላይ በሚገባ አክቲቨ ሆነው የሚሰሩ ከሆን(በቀን ዉስጥ ከ2 ሰአት በላይ ላይቭ የሚቆዩ ከሆነ) ይህ እድል እስከ 7 "
                                       "ቀን የሚቆይ"
                                       " ይሆናል። ካልሆነ ግን እስከ 3 ቀን ብቻ የሚቆይ ይሆናል። ከዛ ብኋላ ባሉት ጊዜያት እንደ ነባር ሰቶች ሆና ነጥብ የምታገኝ "
                                       "ይሆናል።\n\n"
                                       "✅ ነጥብ/point የምንላቸው ወደ <ins>ዶላር/ብር</ins> የሚቀየሩ አፑ የሚሰጠን ክፍያዎች ናቸው።\n\n"
                                       "✅ ስለዚህ እዚህ አፕ ላይ ስኬታማ ለመሆን (ብዙ ገንዘብ ለመስራት) የሚከተሉትን ቅደም ተከተሎች በአግባቡ "
                                       "ይተግብሩ።</b>\n\n", parse_mode="HTML")

        reward_entry = join("images/new_female_task", "reward_entry.jpg")
        with open(reward_entry, "rb") as reward_entry:
            await query.message.reply_photo(photo=InputFile(reward_entry), caption="(1) አፑን ከከፈቱት ብዋላ ከላይ ምስሉ ላይ "
                                                                                   "እንደተመለከተው በተፃፉት ቁጥሮች መሰረት ቁልፎቹን "
                                                                                   "ጠቅ ጠቅ ያድርጉ"
                                            )

        coin_hourly = join("images/new_female_task", "coin_hourly.jpg")
        with open(coin_hourly, "rb") as coin_hourly:
            await query.message.reply_photo(photo=InputFile(coin_hourly), caption="(2) ቀጥሎ ከላይ በምስሉ ላይ የተመለከተው አዲስ "
                                                                                  "ሴት በ1 ቀን/24hr ዉስጥ ላይቭ ስትገባ የምታገኛችው "
                                                                                  "ነጥቦች ናቸው፡\n\n"
                                                                                  "✔️ 1 ሰአት ላይቭ ከቆየች 5000 ነጥቦች/points\n"
                                                                                  "✔️ 2 ሰአት/120 ደቂቃ እና ከዛ በላይ ላይቭ "
                                                                                  "ከቆየች 10,000 ነጥቦች/ponits ታገኛልለች ማለት "
                                                                                  "ነው።\n\n"
                                                                                  "(3) ከዚያም <b>GO</b> የሚለውን ቁልፍ "
                                                                                  "ይጫኑ\n\n "
                                                                                  "‼️ <b>ልብ ይበሉ በ1ቀን/24ሰአት ከ 10 "
                                                                                  "ሰአታት በላይ ላይቭ ተጨማሪ ኮይን አያስገኝዎትም። (ላይቭ ላይ ለላ የሚሰሩት ነገር ከሌለ)</b>"
                                            , parse_mode='HTML',
                                            )

        live_btn = join("images/common_images", "live_btn.jpg")
        with open(live_btn, "rb") as live_btn:
            await query.message.reply_photo(photo=InputFile(live_btn), caption="(4) ከላይ ምስሉ ላይ እንደሚታየው <b>LIVE</b> "
                                                                               "የሚለውን"
                                                                               "ቁልፍ ጠቅ ያድርጉ", parse_mode="HTML"
                                            )

        live_splash = join("images/common_images", "live_entry_splash.jpg")
        with open(live_splash, "rb") as live_splash:
            await query.message.reply_photo(photo=InputFile(live_splash), caption="(5) ከዚያም ከላይ በምስሉ ላይ የሚታዩትን ቅደም "
                                                                                  "ተከተሎች በትክክል ይተግብሩ። ከዚያም ላይቭ ምስራት "
                                                                                  "ይጀምሩ"
                                            )

        live_entry_last = join("images/common_images", "live_entry_last.jpg")
        with open(live_entry_last, "rb") as live_entry_last:
            await query.message.reply_photo(photo=InputFile(live_entry_last),
                                            caption="(6) 👏🏽👏🏽 አሁን live/ላይቭ ገብተዋል\n"
                                                    "ስለዚህ ለሰዎች ከላይ በምስሉ ላይ እንደሚታየው "
                                                    "ሆነው ይታያሉ ማለት ነው።\n\n"
                                                    "😆😍<b>መልካም ቆይታ!</b>",
                                            parse_mode="HTML",
                                            )
        reward_entry = join("images/new_female_task", "reward_entry.jpg")
        with open(reward_entry, "rb") as reward_entry:
            await query.message.reply_photo(photo=InputFile(reward_entry),
                                            caption="(7) ከዚያም ላይቩን ከጨረሱ ብዋላ በላይቩ ያገኙትን ነጥብ/point ለመቀበል(receive ለማድረግ) "
                                                    "ልክ ከላይ በምስሉ ላይ በሚታየው መልኩ ቁልፎቹን ጠቅ ጠቅ ያድርጉ",
                                            )

        live_coin_recieve = join("images/new_female_task", "live_coin_recieve.jpg")
        with open(live_coin_recieve, "rb") as live_coin_recieve:
            await query.message.reply_photo(photo=InputFile(live_coin_recieve),
                                            caption="(8) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው <b>Receive</b> የሚለውን ቁልፍ ጠቅ ያድርጉ",
                                            parse_mode="HTML",
                                            )

        point_store = join("images/common_images", "point_store.jpg")
        with open(point_store, "rb") as point_store:
            await query.message.reply_photo(photo=InputFile(point_store),
                                            caption="(9) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው ወደ ፕሮፋይላችሁ ስትገቡ ያገኛችሁት point ከዚህ "
                                                    "በፊት የነበራችሁ point "
                                                    "ጋር ተደምሮ የሚቀመጥ ይሆናል።\n\n"
                                                    "‼️ <b>ልብ ይበሉ ያገኙትን ነጥብ/point በአፑ ቀን አቆጣጠር መሰረት 24 ሰአት ሳይሞላዉ ("
                                                    "በእትዮጵያ አቆጣጠር በየ "
                                                    "ቀኑ ከ ምሽቱ 1ሰአት በፊት) 'Recieve' ማድረግ (መቀበል) ይጠበቅብዎታል።</b>\n\n"
                                                    " <b>✅ እነዚህ ነጥቦች/points አፑ የሚከፍለን ክፍያዎች ናቸው።</b>\n"
                                                    " ስለዚህ እነዚህን ነጥቦች ወደ ገንዘብ ቀይረን ወደ አካዉንታችን ማስገባት እንችላለን። "
                                                    "<b>ለምሳሌ፡ </b>100,000 points ቢኖረን ወደ ገንዘብ ሲቀየር $10 አለን ማለት ነው።",
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

    elif query.data == 'party_new_female':
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("✅ <b>ይህ አፕ ሴቶችን በተለይም ጀማሪ ሴቶችን ተጨማሪ ነጥቦችን/points በመስጠት በተለዬ መንገድ "
                                       "ያበረታታል። ይህም የሚቆየው ኦፑ ላይ ከተመዘገቡበት ጊዜ አንስቶ ከ3 እስከ 7 ቀን ነው።\n\n"
                                       "✅ አፑ ላይ በሚገባ አክቲቨ ሆነው የሚሰሩ ከሆን(በቀን ዉስጥ ከ2 ሰአት በላይ ላይቭ የሚቆዩ ከሆነ) ይህ እድል እስከ 7 "
                                       "ቀን የሚቆይ"
                                       " ይሆናል። ካልሆነ ግን እስከ 3 ቀን ብቻ የሚቆይ ይሆናል። ከዛ ብኋላ ባሉት ጊዜያት እንደ ነባር ሰቶች ሆና ነጥብ የምታገኝ "
                                       "ይሆናል።\n\n"
                                       "✅ ነጥብ/point የምንላቸው ወደ <ins>ዶላር/ብር</ins> የሚቀየሩ አፑ የሚሰጠን ክፍያዎች ናቸው።\n\n"
                                       "✅ ስለዚህ እዚህ አፕ ላይ ስኬታማ ለመሆን (ብዙ ገንዘብ ለመስራት) የሚከተሉትን ቅደም ተከተሎች በአግባቡ "
                                       "ይተግብሩ።</b>\n\n", parse_mode="HTML")

        new_female_party_entry = join("images/new_female_task", "reward_entry.jpg")
        with open(new_female_party_entry, "rb") as new_female_party_entry:
            await query.message.reply_photo(photo=InputFile(new_female_party_entry),
                                            caption="(1) አፑን ከከፈቱት ብዋላ ከላይ ምስሉ ላይ "
                                                    "የተመለከቱትን ቁልፎች ጠቅ ጠቅ ያድርጉ"
                                            )

        party_hourly = join("images/new_female_task", "party_hourly.jpg")
        with open(party_hourly, "rb") as party_hourly:
            await query.message.reply_photo(photo=InputFile(party_hourly), caption="(2) ከዚያም ቀጥሎ ከላይ በምስሉ ላይ የተመለከተው "
                                                                                   "አዲስ "
                                                                                   "ሴት ፓርቲ ላይ ስትቀመጥ የምታገኛችው "
                                                                                   "ነጥቦች ናቸው፡\n\n"
                                                                                   "✔️ ለአንድ ሰአት/60ደቂቃ ያክል ሰዎች በሚከፍቷቸዉ "
                                                                                   "ፓርቲዎች"
                                                                                   "ላይ ከቆየች "
                                                                                   "800 ነጥቦች/points የምታገኝ ይሆናል።\n"
                                                                                   "✔️ ከአንድ ሰአት እና ከዛ በላይ ሰዎች በሚከፍቷቸው "
                                                                                   "ፓርቲዎች"
                                                                                   "ላይ ከቆየች የቆየችበት ሰአት በ800 ተባዝቶ "
                                                                                   "ነጥብ/point"
                                                                                   "የምታገኝ ይሆናል።\n\n"
                                                                                   "<b>ለምሳሌ፡</b> አንድ ሴት የሆነ ፓርቲ ላይ ለ3 "
                                                                                   "ሰአታት ብትቆይ ወይም ሶስት የተለያዩ ፓርቲዎች ላይ "
                                                                                   "ለ አንድ አንድ ሰአት ብትቆይ <b>3 * 800 = "
                                                                                   "2400</b> ነጥቦች/ponits የታምገኝ "
                                                                                   "ይሆናል።\n\n"
                                                                                   "‼️ <b>ልብ ይበሉ አንድ ሴት በአንድ ቀን/24ሰአት "
                                                                                   "ዉስጥ አንድ ፓርቲ ላይ ወይም የተለያዩ ፓርቲዎች ላይ "
                                                                                   "ከአስር ሰአት በላይ ብትቀመጥ የምታገኘው 10 * "
                                                                                   "800 = 8000 ነጥቦች ብቻ ነው።\n"
                                                                                   "ያማለት በቀን ዉስጥ ከ10 ሰአት በላይ ፓርቲ ላይ "
                                                                                   "መቆየት"
                                                                                   " የሚያገኙት ነጥብ ላይ የሚጨምረው ነገር የለም ማለት "
                                                                                   "ነው።</b>\n\n"
                                                                                   "(3) ቀጥሎ <b>GO</b> የሚለውን ቁልፍ "
                                                                                   "ጠቅ ያድርጉ\n\n"
                                            , parse_mode='HTML',
                                            )

        party_selection = join("images/new_female_task", "party_selection.jpg")
        with open(party_selection, "rb") as party_select:
            await query.message.reply_photo(photo=InputFile(party_select), caption="4. ከላይ ምስሉ ላይ በሚታየው መልኩ በአሁኑ ሰአት "
                                                                                   "ክፍት የሆኑ ፓርቲዎች የሚመጡ ይሆናል። \n"
                                                                                   "ከተዘረዘሩት ፓርዎች መካከል አንዱን በመምረጥ ወደ "
                                                                                   "ፓርቲው ይግቡ።"
                                            )

        party_sit = join("images/new_female_task", "party_sit.jpg")
        with open(party_sit, "rb") as party_sit:
            await query.message.reply_photo(photo=InputFile(party_sit), caption="5. ከዚያም ልክ ከላይ በምስሉ ላይ እንደሚታየው ፓርቲው "
                                                                                "ላይ ክፍት ወርቃማ ወንበሮች መኖራቸዉን ያረጋግጡ።\n"
                                                                                "እነዚህ ወርቃማ ወንበሮች ለሴቶች የተዘጋጁ ናቸው።\n\n"
                                                                                "ከዚያም ካሉት ወርቃማ ወንበሮች አንዱን ይንኩት።\n"
                                                                                "የመረጡት ፓርቲ ላይ ሁሉም ወርቃማ ወንበሮች ከተያዙ ወደ "
                                                                                "ታች ወይም ወደ ላይ በማንሽራተት ያልተያዘ ወርቃማ ወንበር "
                                                                                "ያለበትን ፓርቲ መፈለግ ይችላሉ።\n\n"
                                                                                "‼️ <b>ልብ ይበሉ ሴቶች "
                                                                                "ፓርቲ ላይ ሲገቡ እነዚህ ወርቃማ ወንበሮች ላይ "
                                                                                "እስካልተቀመጡ ድረስ ነጥብ የሚያገኙ አይሆንም።</b>"
                                            , parse_mode="HTML"
                                            )

        party_sit_last = join("images/new_female_task", "party_sit_last.jpg")
        with open(party_sit_last, "rb") as party_sit_last:
            await query.message.reply_photo(photo=InputFile(party_sit_last),
                                            caption="6. 👏🏽👏🏽 አሁን party/ፓርቲ ላይ ተቀምጠዋል\n"
                                                    "😆😍<b>መልካም ቆይታ!</b>\n\n"
                                                    "‼️ <b>ልብ ይበሉ አንዳንድ ጊዜ የፓርቲው "
                                                    "ባለቤቶች ፓርቲያችው ላይ ሰዎች ሲቀመጡ "
                                                    "እንዲያስፈቅዷቸው ወይም ኮይን እንዲከፍሉ "
                                                    "ሊያደርጉ ይችላሉ።</b>"
                                            ,
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

        reward_entry = join("images/new_female_task", "reward_entry.jpg")
        with open(reward_entry, "rb") as reward_entry:
            await query.message.reply_photo(photo=InputFile(reward_entry),
                                            caption="(7) ከዚያም ከፓርቲው ከወጡ ብዋላ ከፓሪቲው ያገኙትን ነጥብ/point ለመቀበል(receive ለማድረግ) "
                                                    "ልክ ከላይ በምስሉ ላይ በሚታየው መልኩ ቁልፎቹን ጠቅ ጠቅ ያድርጉ",
                                            )

        party_point_recieve = join("images/common_images", "party_point_recieve.jpg")
        with open(party_point_recieve, "rb") as party_point_recieve:
            await query.message.reply_photo(photo=InputFile(party_point_recieve),
                                            caption="(8) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው <b>Receive</b> የሚለውን ቁልፍ ጠቅ ያድርጉ",
                                            parse_mode="HTML",
                                            )

        point_store = join("images/common_images", "point_store.jpg")
        with open(point_store, "rb") as point_store:
            await query.message.reply_photo(photo=InputFile(point_store),
                                            caption="(9) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው ወደ ፕሮፋይላችሁ ስትገቡ ያገኛችሁት point ከዚህ "
                                                    "በፊት የነበራችሁ point "
                                                    "ጋር ተደምሮ የሚቀመጥ ይሆናል።\n\n"
                                                    "‼️ <b>ልብ ይበሉ ያገኙትን ነጥብ/point በአፑ ቀን አቆጣጠር መሰረት 24 ሰአት ሳይሞላዉ ("
                                                    "በእትዮጵያ አቆጣጠር በየ "
                                                    "ቀኑ ከ ምሽቱ 1ሰአት በፊት) 'Recieve' ማድረግ (መቀበል) ይጠበቅብዎታል።</b>\n\n"
                                                    " <b>✅ እነዚህ ነጥቦች/points አፑ የሚከፍለን ክፍያዎች ናቸው።</b>\n"
                                                    " ስለዚህ እነዚህን ነጥቦች ወደ ገንዘብ ቀይረን ወደ አካዉንታችን ማስገባት እንችላለን። "
                                                    "<b>ለምሳሌ፡ </b>100,000 points ቢኖረን ወደ ገንዘብ ሲቀየር $10 አለን ማለት ነው።",
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

    elif query.data == 'existed_female_task':
        keyboard = [
            [InlineKeyboardButton("የፊት አሻራ ለመስጠት", callback_data="face_authentication")],
            [InlineKeyboardButton("ላይቭ (ለነባር ሴት)", callback_data="live_existed_female")],
            [InlineKeyboardButton("ፓርቲ (ለነባር ሴት)", callback_data="party_existed_female")],
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        coin_instructions = (
            "የፊት አሻራ/Face Authentication ጨርሰዋል❓❓\n"
            "‼️ <b>ልብ ይበሉ የፊት አሻራ ካልሰጡ አፑ ላይ ታስክ መስራት/ገንዘብ ማግኘት አይችሉም</>\n\n"
            "   ➡️ የፊት አሻራ ካልሰጡ <b>የፊት አሻራ ለመስጠት</b> የሚለዉን ጠቅ ያድርጉ\n"
        )
        await query.message.reply_text(coin_instructions, reply_markup=reply_markup, parse_mode="HTML")

    elif query.data == 'live_existed_female':
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("✅ <b>ይህ አፕ ሴቶችን ከወንዶች በተለየ ተጨማሪ ነጥቦችን/points በመስጠት ያበረታታል።\n\n"
                                       "✅ ነጥብ/point የምንላቸው ወደ <ins>ዶላር/ብር</ins> የሚቀየሩ አፑ የሚሰጠን ክፍያዎች ናቸው።\n\n"
                                       "✅ ስለዚህ እዚህ አፕ ላይ ስኬታማ ለመሆን (ብዙ ገንዘብ ለመስራት) የሚከተሉትን ቅደም ተከተሎች በአግባቡ "
                                       "ይተግብሩ።</b>\n\n", parse_mode="HTML")

        reward_entry = join("images/new_female_task", "reward_entry.jpg")
        with open(reward_entry, "rb") as reward_entry:
            await query.message.reply_photo(photo=InputFile(reward_entry), caption="(1) አፑን ከከፈቱት ብዋላ ከላይ ምስሉ ላይ "
                                                                                   "እንደተመለከተው በተፃፉት ቁጥሮች መሰረት ቁልፎቹን "
                                                                                   "ጠቅ ጠቅ ያድርጉ"
                                            )

        live_hour_existed_female = join("images/existed_female_task", "live_hour_existed_female.jpg")
        with open(live_hour_existed_female, "rb") as live_hour_existed_female:
            await query.message.reply_photo(photo=InputFile(live_hour_existed_female),
                                            caption="(2) ከላይ በምስሉ ላይ የተመለከተው አንድ "
                                                    "ሴት በ1 ቀን/24hr ዉስጥ በራሷ ላይቭ ከፍታ ስትገባ የምታገኛችው "
                                                    "ነጥቦች ናቸው፡\n\n"
                                                    "✔️ 1 ሰአት ላይቭ ከቆየች 1000 ነጥቦች/points\n\n"
                                                    "(3) ከዚያም <b>GO</b> የሚለውን ቁልፍ "
                                                    "ይጫኑ\n\n‼️ <b>ልብ ይበሉ በ1ቀን/24ሰአት ዉስጥ ቢበዛ 10 "
                                                    "ጊዜ ብቻ ነው ሰዎች የከፈቷቸው ፓርቲዎች ላይ "
                                                    "በመቀመጥ ነጥብ/ፖይንት ማግኘት የሚቻለው።</b>"
                                            , parse_mode='HTML',
                                            )

        live_btn = join("images/common_images", "live_btn.jpg")
        with open(live_btn, "rb") as live_btn:
            await query.message.reply_photo(photo=InputFile(live_btn), caption="(4) ከዚያም ከላይ ምስሉ ላይ እንደሚታየው <b>LIVE</b>"
                                                                               "የሚለውን"
                                                                               "ቁልፍ ጠቅ ያድርጉ", parse_mode="HTML"
                                            )

        live_splash = join("images/common_images", "live_entry_splash.jpg")
        with open(live_splash, "rb") as live_splash:
            await query.message.reply_photo(photo=InputFile(live_splash), caption="(5) ከዚያም ከላይ በምስሉ ላይ የሚታዩትን ቅደም "
                                                                                  "ተከተሎች በትክክል ይተግብሩ። ከዚያም ላይቭ ምስራት "
                                                                                  "ይጀምሩ"
                                            )

        live_entry_last = join("images/common_images", "live_entry_last.jpg")
        with open(live_entry_last, "rb") as live_entry_last:
            await query.message.reply_photo(photo=InputFile(live_entry_last),
                                            caption="(6) 👏🏽👏🏽 አሁን live/ላይቭ ገብተዋል\n"
                                                    "ስለዚህ ለሰዎች ከላይ በምስሉ ላይ እንደሚታየው "
                                                    "ሆነው ይታያሉ ማለት ነው።\n\n"
                                                    "😆😍<b>መልካም ቆይታ!</b>",
                                            parse_mode="HTML",
                                            )
        reward_entry = join("images/new_female_task", "reward_entry.jpg")
        with open(reward_entry, "rb") as reward_entry:
            await query.message.reply_photo(photo=InputFile(reward_entry),
                                            caption="(7) ከዚያም ላይቩን ከጨረሱ ብዋላ በላይቩ ያገኙትን ነጥብ/point ለመቀበል(receive ለማድረግ) "
                                                    "ልክ ከላይ በምስሉ ላይ በሚታየው መልኩ ቁልፎቹን ጠቅ ጠቅ ያድርጉ",
                                            )

        live_existed_female_coin = join("images/existed_female_task", "live_existed_female_coin.jpg")
        with open(live_existed_female_coin, "rb") as live_existed_female_coin:
            await query.message.reply_photo(photo=InputFile(live_existed_female_coin),
                                            caption="(8) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው <b>Receive</b> የሚለውን ቁልፍ ጠቅ ያድርጉ",
                                            parse_mode="HTML",
                                            )

        point_store = join("images/common_images", "point_store.jpg")
        with open(point_store, "rb") as point_store:
            await query.message.reply_photo(photo=InputFile(point_store),
                                            caption="(9) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው ወደ ፕሮፋይላችሁ ስትገቡ ያገኛችሁት point ከዚህ "
                                                    "በፊት የነበራችሁ point "
                                                    "ጋር ተደምሮ የሚቀመጥ ይሆናል።\n\n"
                                                    "‼️ <b>ልብ ይበሉ ያገኙትን ነጥብ/point በአፑ ቀን አቆጣጠር መሰረት 24 ሰአት ሳይሞላዉ ("
                                                    "በእትዮጵያ አቆጣጠር በየ "
                                                    "ቀኑ ከ ምሽቱ 1ሰአት በፊት) 'Recieve' ማድረግ (መቀበል) ይጠበቅብዎታል።</b>\n\n"
                                                    " <b>✅ እነዚህ ነጥቦች/points አፑ የሚከፍለን ክፍያዎች ናቸው።</b>\n"
                                                    " ስለዚህ እነዚህን ነጥቦች ወደ ገንዘብ ቀይረን ወደ አካዉንታችን ማስገባት እንችላለን። "
                                                    "<b>ለምሳሌ፡ </b>100,000 points ቢኖረን ወደ ገንዘብ ሲቀየር $10 አለን ማለት ነው።",
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

    elif query.data == 'party_existed_female':
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text("✅ <b>ይህ አፕ ሴቶችን ከወንዶች በተለየ ተጨማሪ ነጥቦችን/points በመስጠት ያበረታታል።\n\n"
                                       "✅ ነጥብ/point የምንላቸው ወደ <ins>ዶላር/ብር</ins> የሚቀየሩ አፑ የሚሰጠን ክፍያዎች ናቸው።\n\n"
                                       "✅ ስለዚህ እዚህ አፕ ላይ ስኬታማ ለመሆን (ብዙ ገንዘብ ለመስራት) የሚከተሉትን ቅደም ተከተሎች በአግባቡ "
                                       "ይተግብሩ።</b>\n\n", parse_mode="HTML")
        existed_female_party_entry = join("images/new_female_task", "reward_entry.jpg")
        with open(existed_female_party_entry, "rb") as existed_female_party_entry:
            await query.message.reply_photo(photo=InputFile(existed_female_party_entry),
                                            caption="(1) አፑን ከከፈቱት ብዋላ ከላይ ምስሉ ላይ "
                                                    "የተመለከተቱን ቁልፎች ጠቅ ጠቅ ያድርጉ"
                                            )

        party_hourly = join("images/new_female_task", "party_hourly.jpg")
        with open(party_hourly, "rb") as party_hourly:
            await query.message.reply_photo(photo=InputFile(party_hourly), caption="(2) ከዚያም ቀጥሎ ከላይ በምስሉ ላይ የተመለከተው "
                                                                                   "አዲስ"
                                                                                   "ሴት ፓርቲ ላይ ስትቀመጥ የምታገኛችው "
                                                                                   "ነጥቦች ናቸው፡\n\n"
                                                                                   "✔️ ለአንድ ሰአት/60ደቂቃ ያክል ሰዎች በሚከፍቷቸዉ "
                                                                                   "ፓርቲዎች"
                                                                                   "ላይ ከቆየች "
                                                                                   "800 ነጥቦች/points የምታገኝ ይሆናል።\n"
                                                                                   "✔️ ከአንድ ሰአት እና ከዛ በላይ ሰዎች በሚከፍቷቸው "
                                                                                   "ፓርቲዎች"
                                                                                   "ላይ ከቆየች የቆየችበት ሰአት በ800 ተባዝቶ "
                                                                                   "ነጥብ/point"
                                                                                   "የምታገኝ ይሆናል።\n\n"
                                                                                   "<b>ለምሳሌ፡</b> አንድ ሴት የሆነ ፓርቲ ላይ ለ3 "
                                                                                   "ሰአታት ብትቆይ ወይም ሶስት የተለያዩ ፓርቲዎች ላይ "
                                                                                   "ለ አንድ አንድ ሰአት ብትቆይ <b>3 * 800 = "
                                                                                   "2400</b> ነጥቦች/ponits የታምገኝ "
                                                                                   "ይሆናል።\n\n"
                                                                                   "‼️ <b>ልብ ይበሉ አንድ ሴት በአንድ ቀን/24ሰአት "
                                                                                   "ዉስጥ አንድ ፓርቲ ላይ ወይም የተለያዩ ፓርቲዎች ላይ "
                                                                                   "ከአስር ሰአት በላይ ብትቀመጥ የምታገኘው 10 * "
                                                                                   "800 = 8000 ነጥቦች ብቻ ነው።\n"
                                                                                   "ያማለት በቀን ዉስጥ ከ10 ሰአት በላይ ፓርቲ ላይ "
                                                                                   "መቆየት"
                                                                                   " የሚያገኙት ነጥብ ላይ የሚጨምረው ነገር የለም ማለት "
                                                                                   "ነው።</b>\n\n"
                                                                                   "(3) ቀጥሎ <b>GO</b> የሚለውን ቁልፍ "
                                                                                   "ጠቅ ያድርጉ\n\n"
                                            , parse_mode='HTML',
                                            )

        party_selection = join("images/new_female_task", "party_selection.jpg")
        with open(party_selection, "rb") as party_select:
            await query.message.reply_photo(photo=InputFile(party_select), caption="4. ከላይ ምስሉ ላይ በሚታየው መልኩ በአሁኑ ሰአት "
                                                                                   "ክፍት የሆኑ ፓርቲዎች የሚመጡ ይሆናል። \n"
                                                                                   "ከተዘረዘሩት ፓርዎች መካከል አንዱን በመምረጥ ወደ "
                                                                                   "ፓርቲው ይግቡ።"
                                            )

        party_sit = join("images/new_female_task", "party_sit.jpg")
        with open(party_sit, "rb") as party_sit:
            await query.message.reply_photo(photo=InputFile(party_sit), caption="5. ከዚያም ልክ ከላይ በምስሉ ላይ እንደሚታየው ፓርቲው "
                                                                                "ላይ ክፍት ወርቃማ ወንበሮች መኖራቸዉን ያረጋግጡ።\n"
                                                                                "እነዚህ ወርቃማ ወንበሮች ለሴቶች የተዘጋጁ ናቸው።\n\n"
                                                                                "ከዚያም ካሉት ወርቃማ ወንበሮች አንዱን ይንኩት።\n"
                                                                                "የመረጡት ፓርቲ ላይ ሁሉም ወርቃማ ወንበሮች ከተያዙ ወደ "
                                                                                "ታች ወይም ወደ ላይ በማንሽራተት ያልተያዘ ወርቃማ ወንበር "
                                                                                "ያለበትን ፓርቲ መፈለግ ይችላሉ።\n\n"
                                                                                "‼️ <b>ልብ ይበሉ ሴቶች "
                                                                                "ፓርቲ ላይ ሲገቡ እነዚህ ወርቃማ ወንበሮች ላይ "
                                                                                "እስካልተቀመጡ ድረስ ነጥብ የሚያገኙ አይሆንም።</b>"
                                            , parse_mode="HTML"
                                            )

        party_sit_last = join("images/new_female_task", "party_sit_last.jpg")
        with open(party_sit_last, "rb") as party_sit_last:
            await query.message.reply_photo(photo=InputFile(party_sit_last),
                                            caption="6. 👏🏽👏🏽 አሁን party/ፓርቲ ላይ ተቀምጠዋል\n"
                                                    "😆😍<b>መልካም ቆይታ!</b>\n\n"
                                                    "‼️ <b>ልብ ይበሉ አንዳንድ ጊዜ የፓርቲው "
                                                    "ባለቤቶች ፓርቲያችው ላይ ሰዎች ሲቀመጡ "
                                                    "እንዲያስፈቅዷቸው ወይም ኮይን እንዲከፍሉ "
                                                    "ሊያደርጉ ይችላሉ።</b>"
                                            ,
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

        reward_entry = join("images/new_female_task", "reward_entry.jpg")
        with open(reward_entry, "rb") as reward_entry:
            await query.message.reply_photo(photo=InputFile(reward_entry),
                                            caption="(7) ከዚያም ከፓርቲው ከወጡ ብዋላ ከፓሪቲው ያገኙትን ነጥብ/point ለመቀበል(receive ለማድረግ) "
                                                    "ልክ ከላይ በምስሉ ላይ በሚታየው መልኩ ቁልፎቹን ጠቅ ጠቅ ያድርጉ",
                                            )

        party_point_recieve = join("images/common_images", "party_point_recieve.jpg")
        with open(party_point_recieve, "rb") as party_point_recieve:
            await query.message.reply_photo(photo=InputFile(party_point_recieve),
                                            caption="(8) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው <b>Receive</b> የሚለውን ቁልፍ ጠቅ ያድርጉ",
                                            parse_mode="HTML",
                                            )

        point_store = join("images/common_images", "point_store.jpg")
        with open(point_store, "rb") as point_store:
            await query.message.reply_photo(photo=InputFile(point_store),
                                            caption="(9) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው ወደ ፕሮፋይላችሁ ስትገቡ ያገኛችሁት point ከዚህ "
                                                    "በፊት የነበራችሁ point "
                                                    "ጋር ተደምሮ የሚቀመጥ ይሆናል።\n\n"
                                                    "‼️ <b>ልብ ይበሉ ያገኙትን ነጥብ/point በአፑ ቀን አቆጣጠር መሰረት 24 ሰአት ሳይሞላዉ ("
                                                    "በእትዮጵያ አቆጣጠር በየ "
                                                    "ቀኑ ከ ምሽቱ 1ሰአት በፊት) 'Recieve' ማድረግ (መቀበል) ይጠበቅብዎታል።</b>\n\n"
                                                    " <b>✅ እነዚህ ነጥቦች/points አፑ የሚከፍለን ክፍያዎች ናቸው።</b>\n"
                                                    " ስለዚህ እነዚህን ነጥቦች ወደ ገንዘብ ቀይረን ወደ አካዉንታችን ማስገባት እንችላለን። "
                                                    "<b>ለምሳሌ፡ </b>100,000 points ቢኖረን ወደ ገንዘብ ሲቀየር $10 አለን ማለት ነው።",
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

    elif query.data == 'male_tasks':
        keyboard = [
            [InlineKeyboardButton("የፊት አሻራ ለመስጠት", callback_data="face_authentication")],
            [InlineKeyboardButton("ላይቭ (ለወንድ)", callback_data="live_male")],
            [InlineKeyboardButton("ፓርቲ (ለወንድ)", callback_data="party_male")],
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        coin_instructions = (
            "የፊት አሻራ/Face Authentication ጨርሰዋል❓❓\n"
            "‼️ <b>ልብ ይበሉ የፊት አሻራ ካልሰጡ አፑ ላይ ታስክ መስራት/ገንዘብ ማግኘት አይችሉም</>\n\n"
            "   ➡️ የፊት አሻራ ካልሰጡ <b>የፊት አሻራ ለመስጠት</b> የሚለዉን ጠቅ ያድርጉ\n"
        )
        await query.message.reply_text(coin_instructions, reply_markup=reply_markup, parse_mode="HTML")

    elif query.data == 'live_male':
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("ቀጥሎ በተዘረዘሩት ቅደም ተከተሎች መሰረት ወንዶች እዚህ አፕ ላይ ሌሎች ሰዎች የከፈቷቸው ላይቮች ላይ ገብተው እንዴት "
                                       "ኮይን/coin እንደሚሰሩ እናያለን።\n\n"
                                       "✅ <b>ኮይን/coin የምንላቸው ወደ ነጥብ/point ኢክስቼንጅ/exchange የሚደረጉ እና ወደ ባንክ አካዉንታችን ወይም "
                                       "ወደ"
                                       "ቴሌ ብር ዊዝድሮው/withdraw ስናደርግ ወደ <ins>ዶላር/ብር</ins> የሚቀየሩ አፑ የሚሰጠን ክፍያዎች ናቸው።\n\n"
                                       "✅ ስለዚህ እዚህ አፕ ላይ ስኬታማ ለመሆን (ብዙ ገንዘብ ለመስራት) የሚከተሉትን ቅደም ተከተሎች በአግባቡ "
                                       "ይተግብሩ።</b>\n\n", parse_mode="HTML")

        live_entry_select = join("images/common_images", "live_entry_select.jpg")
        with open(live_entry_select, "rb") as live_entry_select:
            await query.message.reply_photo(photo=InputFile(live_entry_select), caption="(1) አፑን ከከፈቱት ብዋላ ከላይ ምስሉ ላይ "
                                                                                        "እንደተመለከተው መጀመሪያ ቁልፉን ጠቅ ያድርጉ "
                                                                                        "ከዚይም በአሁኑ"
                                                                                        "ሰአት ላይቭ ላይ "
                                                                                        "ያሉ ሰዎች ከላይ ምስሉ ላይ እንደተከበቡት "
                                                                                        "ሆነው የሚመጡ ይሆናል።"
                                                                                        " ከዚያም የሚፈልጉትን ላይቭ በመንካት ይግቡ።"
                                            )

        treasure_box_live = join("images/common_images", "treasure_box_live.jpg")
        with open(treasure_box_live, "rb") as treasure_box_live:
            await query.message.reply_photo(photo=InputFile(treasure_box_live),
                                            caption="(2) በመቀጠል ላይቩ ላይ ከገቡ ብዋላ ከላይ ምስሉ "
                                                    "ላይ እንደተመለከተው ሳጥኑን(treasure box) በዬ "
                                                    "5 ደቂቃው (ያ ማለት ከ5 ደቂቃ ጀምሮ ወደ ኋላ ቆጥሮ "
                                                    "ዜሮ እስኪደረስ በመጠበቅ) "
                                                    "ጠቅ ማድረግ፡\n\n"
                                                    "✔️ 1 የኢንተርኔት ፍጥነትዎ ጥሩ ከሆነ 40 "
                                                    "ኮይን/coin ያገኛሉ\n"
                                                    "✔️ 2 የኢንተርኔት ፍጥነትዎ ደከም ያለ ከሆነ 5 "
                                                    "ኮይን/coin የሚያገኙ ይሆናል\n\n"
                                                    "‼️ <b>ልብ ይበሉ ይህንን ማድረግ የሚችሉት "
                                                    "በቀን/24ሰአት ዉስጥ ቢበዛ አስር ጊዜ ብቻ ነው።\n"
                                                    "በስዎች ላይቭ ላይ በመግባት ከአስር ጊዜ በላይ ሳጥኑን "
                                                    "ቢነኩ ተጨማሪ ኮይን የሚያገኙ አይሆንም።</b>"
                                            , parse_mode='HTML',
                                            )

        coin_store = join("images/common_images", "coin_store.jpg")
        with open(coin_store, "rb") as coin_store:
            await query.message.reply_photo(photo=InputFile(coin_store),
                                            caption="(3) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው ወደ ፕሮፋይልዎ ሲገቡ ከላይቩ ያገኙት coin ከዚህ "
                                                    "በፊት ከነበረው coin "
                                                    "ጋር ተደምሮ የሚቀመጥ ይሆናል።\n\n"
                                                    " <b>‼️ ልብ ይበሉ እነዚህ ኮይኖች/coins አፑ የሚከፍለን ክፍያዎች ናቸው።</b>\n\n"
                                                    "ስለዚህ እነዚህን ነጥቦች exchange አድርገን ወደ ነጥብ/point ከዚያም ወደ ገንዘብ ቀይረን ወደ "
                                                    "አካዉንታችን ወይም ወደ ቴሌ ብር ማስገባት እንችላለን።"
                                                    "<b>ለምሳሌ፡ </b>100,000 coins ቢኖረን ወደ point exchange ሲደረግ 70,"
                                                    "000 point ይሆናል።\n"
                                                    "70,000 point ደግሞ ወደ ገንዘብ ሲቀየር $7 አለን ማለት ነው።",
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

    elif query.data == 'party_male':
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text("ቀጥሎ በተዘረዘሩት ቅደም ተከተሎች መሰረት ወንዶች እዚህ አፕ ላይ ሌሎች ሰዎች የከፈቷቸው ፓርቲዎች ላይ ገብተው እንዴት "
                                       "ኮይን/coin እንደሚሰሩ እናያለን።\n\n"
                                       "✅ <b>ኮይን/coin የምንላቸው ወደ ነጥብ/point ኢክስቼንጅ/exchange የሚደረጉ እና ወደ ባንክ አካዉንታችን ወይም "
                                       "ወደ"
                                       "ቴሌ ብር ዊዝድሮው/withdraw ስናደርግ ወደ <ins>ዶላር/ብር</ins> የሚቀየሩ አፑ የሚሰጠን ክፍያዎች ናቸው።\n\n"
                                       "✅ ስለዚህ እዚህ አፕ ላይ ስኬታማ ለመሆን (ብዙ ገንዘብ ለመስራት) የሚከተሉትን ቅደም ተከተሎች በአግባቡ "
                                       "ይተግብሩ።</b>\n\n", parse_mode="HTML")

        live_coin_entry = join("images/common_images", "live_coin_entry.jpg")
        with open(live_coin_entry, "rb") as live_coin_entry:
            await query.message.reply_photo(photo=InputFile(live_coin_entry), caption="(1) ከላይ ምስሉ እንደሚያመለክተው አንድ "
                                                                                      "ሰው/ወንድ ሰዎች የከፈቷቸው ፓርቲዎች ላይ "
                                                                                      "ሲቀመጥ በየ 15 ደቂቃው 200 coin የሚያገኝ "
                                                                                      "ይሆናል።"
                                                                                      "(1.1) ቀጥሎ 'GO' የሚለውን ቁልፍ ይንኩት።\n"
                                                                                      "<b>ወይም ቀጥሎ የተቀመጠውን አማራጭ ይጠቀሙ ⬇️⬇️</b>"
                                            )

        party_selection = join("images/common_images", "party_selection_short.jpg")
        with open(party_selection, "rb") as party_select:
            await query.message.reply_photo(photo=InputFile(party_select), caption="2. ወይም ከላይ በምስሉ ላይ በሚታየው መልኩ ቁልፉን "
                                                                                   "በመንካት በአሁኑ ሰአት "
                                                                                   "ክፍት የሆኑ ፓርቲዎች የሚመጡላቸው ይሆናል። \n"
                                                                                   "ከተዘረዘሩት ፓርዎች መካከል አንዱን በመምረጥ ወደ "
                                                                                   "ፓርቲው ይግቡ።"
                                            )

        party_sit = join("images/new_female_task", "party_sit.jpg")
        with open(party_sit, "rb") as party_sit:
            await query.message.reply_photo(photo=InputFile(party_sit), caption="3. ከዚያም ልክ ከላይ በምስሉ ላይ እንደሚታየው ፓርቲው "
                                                                                "ላይ ክፍት ወንበሮች መኖራቸዉን ያረጋግጡ።\n"
                                                                                "<b>ወርቃማ ወንበሮች ለሴቶች የተዘጋጁ ናቸው። ስለዚህ ሌላ "
                                                                                "ክፍት ወንበር ካላጡ ወርቃማ ወንበሮች ላይ "
                                                                                "ባይቀመጡ የተሻለ ይሆናል።</b>\n\n"
                                                                                "ከዚያም ካሉት ክፍት ወንበሮች አንዱን ይንኩት።\n"
                                                                                "የመረጡት ፓርቲ ላይ ሁሉም ወንበሮች ከተያዙ ወደ "
                                                                                "ታች ወይም ወደ ላይ በማንሽራተት "
                                                                                "ክፍት ወንበር ያለበትን ፓርቲ መፈለግ ይችላሉ።\n\n"
                                                                                "‼️ <b>ልብ ይበሉ በ1ቀን/24ሰአት ዉስጥ ቢበዛ 10 "
                                                                                "ጊዜ ብቻ ነው ሰዎች የከፈቷቸው ፓርቲዎች ላይ "
                                                                                "በመቀመጥ ኮይን ማግኘት የሚችሉት።</b>"
                                            , parse_mode="HTML"
                                            )

        party_sit_last_m = join("images/male_task", "party_sit_last.jpg")
        with open(party_sit_last_m, "rb") as party_sit_m:
            await query.message.reply_photo(photo=InputFile(party_sit_m),
                                            caption="4. 👏🏽👏🏽 አሁን party/ፓርቲ ላይ ተቀምጠዋል\n"
                                                    "ከላይ ምስሉ ላይ በቀስት እንደተመልከተው ሳ"
                                                    "ጥኑን በየ 5 ደቂቃው በመንካት ፓርቲው ላይ ተቀምተው "
                                                    "ከሚያገኙት ኮይን ዉጭ ተጨማሪ ኮይን ማግኘት ይችላሉ።\n\n"
                                                    "😆😍<b>መልካም ቆይታ!</b>\n\n"
                                                    "‼️ <b>ልብ ይበሉ አንዳንድ ጊዜ የፓርቲው "
                                                    "ባለቤቶች ፓርቲያችው ላይ ሰዎች ሲቀመጡ "
                                                    "ፍቃድ እንዲጠይቋቸዉ ወይም ኮይን እንዲከፍሉ "
                                                    "ሊያደርጉ ይችላሉ።</b>"
                                            ,
                                            parse_mode="HTML",
                                            )

        reward_entry = join("images/new_female_task", "reward_entry.jpg")
        with open(reward_entry, "rb") as reward_entry:
            await query.message.reply_photo(photo=InputFile(reward_entry),
                                            caption="(5) ከዚያም ከፓርቲው ከወጡ ብዋላ ከፓሪቲው ያገኙትን ነጥብ/point ለመቀበል(receive ለማድረግ) "
                                                    "ልክ ከላይ በምስሉ ላይ በሚታየው መልኩ ቁልፎቹን ጠቅ ጠቅ ያድርጉ",
                                            )

        party_common_recieve = join("images/common_images", "party_common_recieve.jpg")
        with open(party_common_recieve, "rb") as party_common_recieve:
            await query.message.reply_photo(photo=InputFile(party_common_recieve),
                                            caption="(6) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው <b>Receive</b> የሚለውን ቁልፍ ጠቅ ያድርጉ",
                                            parse_mode="HTML",
                                            )

        point_store = join("images/common_images", "point_store.jpg")
        with open(point_store, "rb") as point_store:
            await query.message.reply_photo(photo=InputFile(point_store),
                                            caption="(7) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው ወደ ፕሮፋይላችሁ ስትገቡ ያገኛችሁት point ከዚህ "
                                                    "በፊት የነበራችሁ point "
                                                    "ጋር ተደምሮ የሚቀመጥ ይሆናል።\n\n"
                                                    "‼️ <b>ልብ ይበሉ ያገኙትን ነጥብ/point በአፑ ቀን አቆጣጠር መሰረት 24 ሰአት ሳይሞላዉ ("
                                                    "በእትዮጵያ አቆጣጠር በየ "
                                                    "ቀኑ ከ ምሽቱ 1ሰአት በፊት) 'Recieve' ማድረግ (መቀበል) ይጠበቅብዎታል።</b>\n\n"
                                                    " <b>✅ እነዚህ ነጥቦች/points አፑ የሚከፍለን ክፍያዎች ናቸው።</b>\n"
                                                    " ስለዚህ እነዚህን ነጥቦች ወደ ገንዘብ ቀይረን ወደ አካዉንታችን ማስገባት እንችላለን።\n"
                                                    "<b>ለምሳሌ፡ </b>100,000 points ቢኖረን ወደ ገንዘብ ሲቀየር $10 አለን ማለት ነው።",
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

    elif query.data == 'common_task':
        keyboard = [
            [InlineKeyboardButton("ላኪ ቦክስ", callback_data="lucky_box")],
            [InlineKeyboardButton("ፋየር ዎርክ", callback_data="fire_work")],
            [InlineKeyboardButton("ትሬዠር ቦክስ", callback_data="treasure_box")],
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        coin_instructions = (
            "<b>ከዚህ በታች የተዘረዘሩት ፖይንት/ኮይን መሰብሰቢያ መንገዶች ለሁሉም ፆታዎች(ለሴትም ለወንድም) በአንድ አይነት መንገድ የሚሰሩ ናቸው።</b>"
        )
        await query.message.reply_text(coin_instructions, parse_mode="HTML", reply_markup=reply_markup)

    elif query.data == 'lucky_box':
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("<b>ቀጥሎ በተዘረዘሩት ቅደም ተከተሎች መሰረት እዚህ አፕ ላይ ሌሎች ሰዎች የከፈቷቸው ላይቮች ላይ ገብተው እንዴት "
                                       "ከላኪ ቦክስ/lucky box ኮይን/coin እንደምናገኝ እናያለን።</b>\n\n"
                                       "✅ <b>ኮይን/coin የምንላቸው ወደ ነጥብ/point ኢክስቼንጅ/exchange የሚደረጉ እና ወደ ባንክ አካዉንታችን ወይም "
                                       "ወደ"
                                       "ቴሌ ብር ዊዝድሮው/withdraw ስናደርግ ወደ <ins>ዶላር/ብር</ins> የሚቀየሩ አፑ የሚሰጠን ክፍያዎች ናቸው።\n\n"
                                       "✅ ስለዚህ እዚህ አፕ ላይ ስኬታማ ለመሆን (ብዙ ገንዘብ ለመስራት) የሚከተሉትን ቅደም ተከተሎች በአግባቡ "
                                       "ይተግብሩ።</b>\n\n", parse_mode="HTML")

        live_entry_select = join("images/common_images", "live_entry_select.jpg")
        with open(live_entry_select, "rb") as live_entry_select:
            await query.message.reply_photo(photo=InputFile(live_entry_select), caption="(1) አፑን ከከፈቱት ብዋላ ከላይ ምስሉ ላይ "
                                                                                        "እንደተመለከተው መጀመሪያ በቀስት የተመለከተውን ቁልፍ ጠቅ ያድርጉ። "
                                                                                        "ከዚይም በአሁኑ "
                                                                                        "ሰአት ላይቭ ላይ "
                                                                                        "ያሉ ሰዎች ከላይ ምስሉ ላይ እንደተከበበው "
                                                                                        "ሆነው የሚመጡ ይሆናል።"
                                                                                        " ከዚያም የሚፈልጉትን ላይቭ በመንካት ይግቡ።"
                                            )

        lucky_box_entry = join("images/lucky_box", "lucky_box_entry.jpg")
        with open(lucky_box_entry, "rb") as lucky_box_entry:
            await query.message.reply_photo(photo=InputFile(lucky_box_entry),
                                            caption="(2) በመቀጠል ላይቩ ላይ ከገቡ ብዋላ ከላይ ምስሉ "
                                                    "ላይ በቀስት እንደተመለከተው አይነት ሳጥን/ላኪ ቦክስ መኖሩን ያረጋግጡ።\n\n"
                                                    "✔️ የገቡበት ላይቭ ላይ ሳጥኑ/ላኪ ቦክስ ካለ ሳጥኑን ጠቅ ያድርጉት።\n"
                                                    "✔️ ከሌለ ደግሞ የስልክዎን ስክሪን ወደ ላይ ወይም ወደታች በማንሸራተት ሳጥኑ/ላኪ ቦክስ"
                                                    " ያለበትን ላይቭ በመፈለግ ሳጥኑን ጠቅ ያድርጉት።\n\n"
                                                    "‼️ <b>ላኪ ቦክስ በላይቩ ባለቤቶች አማካኝነት የተቀመጠ እና እነሱ ባስቀመጧቸው ህጎች "
                                                    "መሰረት የሚሰራ ኮይን መሰብሰቢያ መንገድ ነው።</b>"
                                            , parse_mode='HTML',
                                            )

        lucky_box_last = join("images/lucky_box", "lucky_box_last.jpg")
        with open(lucky_box_last, "rb") as lucky_box_last:
            await query.message.reply_photo(photo=InputFile(lucky_box_last),
                                            caption="(3) በመቀጠል ሳጥኑን ከነኩት ብዋላ ከላይ ምስሉ "
                                                    "ላይ እንደተከበበው ሆኖ ላኪ ቦክሱ ይከፈታል።\n\n"
                                                    "✅ <b>ላኪ ቦክሱ ዉስጥ የኮይን ብዛት፣ ለስንት ሰው እንደሚደርስ እና ለሎችም ህጎች ሊቀመጡ "
                                                    "ይችላሉ።</b>\n"
                                                    "✅ ስለዚህ ላኪ ቦክሱ ዉስጥ በተቀመጡት ህጎች መሰረት ኮይን የሚያገኙ ይሆናል።\n\n"
                                            # "‼️ <b>ላኪ ቦክስ በላይቩ ባለቤቶች አማካኝነት የተቀመጠ እና እነሱ ባስቀመጧቸው ክሪይቴሪያዎች "
                                            # "መሰረት ብቻ የሚሰራ ነው።</b>"
                                                    "(3.1) ከዚያም <b>Open the box</b> የሚለውን ቁልፍ ጠቅ ያድርጉ።"
                                            , parse_mode='HTML',
                                            )

        coin_store = join("images/common_images", "coin_store.jpg")
        with open(coin_store, "rb") as coin_store:
            await query.message.reply_photo(photo=InputFile(coin_store),
                                            caption="(4) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው ወደ ፕሮፋይልዎ ሲገቡ ከላኪ ቦክሱ ያገኙት coin ከዚህ"
                                                    "በፊት ከነበረው coin "
                                                    "ጋር ተደምሮ የሚቀመጥ ይሆናል።\n\n"
                                                    " <b>‼️ ልብ ይበሉ እነዚህ ኮይኖች/coins አፑ የሚከፍለን ክፍያዎች ናቸው።</b>\n\n"
                                                    "ስለዚህ እነዚህን ነጥቦች exchange አድርገን ወደ ነጥብ/point ከዚያም ወደ ገንዘብ ቀይረን ወደ "
                                                    "አካዉንታችን ወይም ወደ ቴሌ ብር ማስገባት እንችላለን።"
                                                    "<b>ለምሳሌ፡ </b>100,000 coins ቢኖረን ወደ point exchange ሲደረግ 70,"
                                                    "000 point ይሆናል።\n"
                                                    "70,000 point ደግሞ ወደ ገንዘብ ሲቀየር $7 አለን ማለት ነው።",
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

    elif query.data == 'fire_work':
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("<b>ቀጥሎ በተዘረዘሩት ቅደም ተከተሎች መሰረት እዚህ አፕ ላይ ሌሎች ሰዎች የከፈቷቸው ላይቮች ላይ ገብተው እንዴት "
                                       "ከፋየር ዎርክ(fire work) ኮይን/coin እንደምናገኝ እናያለን።</b>\n\n"
                                       "✅ <b>ኮይን/coin የምንላቸው ወደ ነጥብ/point ኢክስቼንጅ/exchange የሚደረጉ እና ወደ ባንክ አካዉንታችን ወይም "
                                       "ወደ"
                                       "ቴሌ ብር ዊዝድሮው/withdraw ስናደርግ ወደ <ins>ዶላር/ብር</ins> የሚቀየሩ አፑ የሚሰጠን ክፍያዎች ናቸው።\n\n"
                                       "✅ ስለዚህ እዚህ አፕ ላይ ስኬታማ ለመሆን (ብዙ ገንዘብ ለመስራት) የሚከተሉትን ቅደም ተከተሎች በአግባቡ "
                                       "ይተግብሩ።</b>\n\n", parse_mode="HTML")

        live_entry_select = join("images/common_images", "live_entry_select.jpg")
        with open(live_entry_select, "rb") as live_entry_select:
            await query.message.reply_photo(photo=InputFile(live_entry_select), caption="(1) አፑን ከከፈቱት ብዋላ ከላይ ምስሉ ላይ "
                                                                                        "እንደተመለከተው መጀመሪያ በቀስት "
                                                                                        "የተመለከተውን ቁልፍ ጠቅ ያድርጉ።"
                                                                                        "ከዚይም በአሁኑ "
                                                                                        "ሰአት ላይቭ ላይ "
                                                                                        "ያሉ ሰዎች ከላይ ምስሉ ላይ እንደተከበበው "
                                                                                        "ሆነው የሚመጡ ይሆናል።"
                                                                                        " ከዚያም የሚፈልጉትን ላይቭ በመንካት ይግቡ።"
                                            )

        fire_work_entry = join("images/fire_work", "fire_work_result.jpg")
        with open(fire_work_entry, "rb") as fire_work_entry:
            await query.message.reply_photo(photo=InputFile(fire_work_entry),
                                            caption="(2) በመቀጠል ላይቩ ላይ ከገቡ ብዋላ ከላይ ምስሉ "
                                                    "ላይ እንደተከበበው አይነት <b>fire work</b> የሚል ፅሁፍ ሲመጣልዎ ፈጠን ብለው ጠቅ "
                                                    "ያድርጉት።\n\n"
                                                    "✔️ ፋየር ዎርክ(fire work) ማለት አንድ ሰው በራሱ ላይቭ ሲገባ ሌሎች ሰዎች ወደሱ ላይቭ "
                                                    "እንዲመጡ ለማድረግ ለአፑ በመክፈል ወደ ሌሎች ላይቭ በማስታወቂያ መልክ እንዲታይ የሚደረግበት መንገድ "
                                                    "ነው።\n"
                                                    "✔️ ታዲያ ይህንን ማስታወቂያ እኛ በምንነካበት ሰአት ወደ ላይቩ ባለቤት የሚወስደን ይሆናል።\n\n"
                                            , parse_mode='HTML',
                                            )

        fire_work_result = join("images/fire_work", "fire_work_entry.jpg")
        with open(fire_work_result, "rb") as fire_work_result:
            await query.message.reply_photo(photo=InputFile(fire_work_result),
                                            caption="(3) በመቀጠል fire work የሚለውን ፅሁፍ ከነኩት ብዋላ ከላይ ምስሉ እንደሚታየው "
                                                    "ወደ ላይቩ (ወደ ፋየር ዎርኩ ባለቤት) ይወስደናል።\n\n"
                                                    "✅ <b>ከዚያም ወደ ላይቩ ከወሰደን ብዋላ ለ1 ደቂቃ/60ሰከንድ መጠበቅ።\n\n"
                                                    "✅ ከ 1 ደቂቃ ብዋላ ከላይ ምስሉ ላይ እንደተከበበው ቁጥሮች በተከታታይ ይፈነዳሉ/ፋየር ይደረጋሉ። ያ "
                                                    "ማለት እዚህ ፋየር ዎርክ ላይ የተቀመጠውን ኮይን አገኘን ማለት ነው።</b>\n\n"
                                                    "‼️ <b>ልብ ይበሉ እዚህ ፋየር ዎርክ ላይ የተቀመጡት ኮይኖች ሁልጊዜም ላይደርሱን ይችላሉ። ይህ "
                                                    "የሚሆነው "
                                                    "ከኛ በፊት የገቡ ሰዎች ካሉ እና እንዲሁም VIP ስዎች ካሉ ለእነሱ ቅድሚያ ስልሚሰጥ ፋየር ዎርኩ ላይ "
                                                    "ያሉት ኮይኖች ለኛ ከመድረሳቸው በፊት ለእነሱ ተከፋፍለው ስለሚያልቁ ነው።</b>"
                                            , parse_mode='HTML',
                                            )

        coin_store = join("images/common_images", "coin_store.jpg")
        with open(coin_store, "rb") as coin_store:
            await query.message.reply_photo(photo=InputFile(coin_store),
                                            caption="(4) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው ወደ ፕሮፋይልዎ ሲገቡ ከፋየር ዎርኩ ያገኙት(አግኝተው "
                                                    "ከሆነ) ኮይን/coin ከዚህ በፊት ከነበረው coin "
                                                    "ጋር ተደምሮ የሚቀመጥ ይሆናል።\n\n"
                                                    " <b>‼️ ልብ ይበሉ እነዚህ ኮይኖች/coins አፑ የሚከፍለን ክፍያዎች ናቸው።</b>\n\n"
                                                    "ስለዚህ እነዚህን ነጥቦች exchange አድርገን ወደ ነጥብ/point ከዚያም ወደ ገንዘብ ቀይረን ወደ "
                                                    "አካዉንታችን ወይም ወደ ቴሌ ብር ማስገባት እንችላለን።"
                                                    "<b>ለምሳሌ፡ </b>100,000 coins ቢኖረን ወደ point exchange ሲደረግ 70,"
                                                    "000 point ይሆናል።\n"
                                                    "70,000 point ደግሞ ወደ ገንዘብ ሲቀየር $7 አለን ማለት ነው።",
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

    elif query.data == 'treasure_box':
        keyboard = [
            [InlineKeyboardButton("ወደ ዋናው ማዉጫ ለመመለስ", callback_data="back_to_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("ቀጥሎ በተዘረዘሩት ቅደም ተከተሎች መሰረት እዚህ አፕ ላይ ሌሎች ሰዎች የከፈቷቸው ላይቮች እና ፓርቲዎች ላይ ገብተው እንዴት "
                                       "ኮይን/coin እንደሚሰሩ እናያለን።\n\n"
                                       "✅ <b>ኮይን/coin የምንላቸው ወደ ነጥብ/point ኢክስቼንጅ/exchange የሚደረጉ እና ወደ ባንክ አካዉንታችን ወይም "
                                       "ወደ"
                                       "ቴሌ ብር ዊዝድሮው/withdraw ስናደርግ ወደ <ins>ዶላር/ብር</ins> የሚቀየሩ አፑ የሚሰጠን ክፍያዎች ናቸው።\n\n"
                                       "✅ ስለዚህ እዚህ አፕ ላይ ስኬታማ ለመሆን (ብዙ ገንዘብ ለመስራት) የሚከተሉትን ቅደም ተከተሎች በአግባቡ "
                                       "ይተግብሩ።</b>\n\n", parse_mode="HTML")

        live_entry_select = join("images/common_images", "live_entry_select.jpg")
        with open(live_entry_select, "rb") as live_entry_select:
            await query.message.reply_photo(photo=InputFile(live_entry_select),
                                            caption="(1) \n(a) አፑን ከከፈቱት ብዋላ ከላይ ምስሉ ላይ "
                                                    "እንደተመለከተው መጀመሪያ ቁልፉን ጠቅ ያድርጉ "
                                                    "ከዚይም በአሁኑ"
                                                    "ሰአት ላይቭ ላይ "
                                                    "ያሉ ሰዎች ከላይ ምስሉ ላይ እንደተከበቡት "
                                                    "ሆነው የሚመጡ ይሆናል።"
                                                    " ከዚያም የሚፈልጉትን ላይቭ በመንካት ይግቡ።\n\n"
                                                    "<b>ወይም (ፓርቲ ላይ መስራት ከፈለጉ) ቀጥሎ የተቀመጠውን አማራጭ ይጠቀሙ ⬇️⬇️</b>"
                                            )
        party_selection_short = join("images/common_images", "party_selection_short.jpg")
        with open(party_selection_short, "rb") as party_selection_short:
            await query.message.reply_photo(photo=InputFile(party_selection_short),
                                            caption="b. ወይም ከላይ በ ምስሉ ላይ በሚታየው መልኩ ቁልፉን በመንካት  በአሁኑ ሰአት "
                                                    "ክፍት የሆኑ ፓርቲዎች የሚመጡላቸው ይሆናል። \n"
                                                    "ከተዘረዘሩት ፓርዎች መካከል አንዱን በመምረጥ ወደ "
                                                    "ፓርቲው ይግቡ።"
                                            )

        treasure_box_live = join("images/common_images", "treasure_box_live.jpg")
        with open(treasure_box_live, "rb") as treasure_box_live:
            await query.message.reply_photo(photo=InputFile(treasure_box_live),
                                            caption="2.\n"
                                                    "(a) በመቀጠል ላይቩ ላይ ከገቡ ብዋላ ከላይ ምስሉ "
                                                    "ላይ እንደተመለከተው ሳጥኑን(treasure box) በዬ "
                                                    "5 ደቂቃው (ያ ማለት ከ5 ደቂቃ ጀምሮ ወደ ኋላ ቆጥሮ "
                                                    "ዜሮ እስኪደረስ በመጠበቅ) "
                                                    "ጠቅ ማድረግ፡\n\n"
                                                    "✔️ 1 የኢንተርኔት ፍጥነትዎ ጥሩ ከሆነ 40 "
                                                    "ኮይን/coin ያገኛሉ\n"
                                                    "✔️ 2 የኢንተርኔት ፍጥነትዎ ደከም ያለ ከሆነ 5 "
                                                    "ኮይን/coin የሚያገኙ ይሆናል\n\n"
                                                    "‼️ <b>ልብ ይበሉ ይህንን ማድረግ የሚችሉት "
                                                    "በቀን/24ሰአት ዉስጥ ቢበዛ አስር ጊዜ ብቻ ነው።\n"
                                                    "በስዎች ላይቭ ላይ በመግባት ከአስር ጊዜ በላይ ሳጥኑን "
                                                    "ቢነኩ ተጨማሪ ኮይን የሚያገኙ አይሆንም።</b>"
                                            , parse_mode='HTML',
                                            )

        party_sit = join("images/new_female_task", "party_sit.jpg")
        with open(party_sit, "rb") as party_sit:
            await query.message.reply_photo(photo=InputFile(party_sit), caption="(b). ከዚያም ልክ ከላይ በምስሉ ላይ እንደሚታየው ፓርቲው "
                                                                                "ላይ ክፍት ወንበሮች መኖራቸዉን ያረጋግጡ።\n"
                                                                                "<b>ወርቃማ ወንበሮች ለሴቶች የተዘጋጁ ናቸው። ስለዚህ ሌላ "
                                                                                "ክፍት ወንበር ካላጡ ወርቃማ ወንበሮች ላይ "
                                                                                "ባይቀመጡ የተሻለ ይሆናል።</b>\n\n"
                                                                                "ከዚያም ካሉት ክፍት ወንበሮች አንዱን ይንኩት።\n"
                                                                                "የመረጡት ፓርቲ ላይ ሁሉም ወንበሮች ከተያዙ ወደ "
                                                                                "ታች ወይም ወደ ላይ በማንሽራተት "
                                                                                "ክፍት ወንበር ያለበትን ፓርቲ መፈለግ ይችላሉ።\n\n"
                                                                                "‼️ <b>ልብ ይበሉ በ1ቀን/24ሰአት ዉስጥ ቢበዛ 10 "
                                                                                "ጊዜ ብቻ ነው ሰዎች የከፈቷቸው ፓርቲዎች ላይ "
                                                                                "በመቀመጥ ኮይን ማግኘት የሚችለው።</b>"
                                            , parse_mode="HTML"
                                            )

        party_sit_last_m = join("images/male_task", "party_sit_last.jpg")
        with open(party_sit_last_m, "rb") as party_sit_m:
            await query.message.reply_photo(photo=InputFile(party_sit_m),
                                            caption="3. 👏🏽👏🏽 አሁን party/ፓርቲ ላይ ተቀምጠዋል\n"
                                                    "ከላይ በምስሉ ላይ በቀስት እንደተመልከተው ሳ"
                                                    "ጥኑን በየ 5 ደቂቃው በመንካት ፓርቲው ላይ ተቀምጠው "
                                                    "ኮይን ማግኘት ይችላሉ።\n\n"
                                                    "✅ <b>ልብ ይበሉ በ1ቀን/24ሰአት ዉስጥ ቢበዛ 10 "
                                                    "ጊዜ ብቻ ነው ሰዎች የከፈቷቸው ፓርቲዎች ላይ "
                                                    "በመቀመጥ ኮይን ማግኘት የሚችለው።</b>\n\n"
                                                    "‼️ <b>ልብ ይበሉ አንዳንድ ጊዜ የፓርቲው "
                                                    "ባለቤቶች ፓርቲያችው ላይ ሰዎች ሲቀመጡ "
                                                    "ፍቃድ እንዲጠይቋቸዉ ወይም ኮይን እንዲከፍሉ "
                                                    "ሊያደርጉ ይችላሉ።</b>"
                                            ,
                                            parse_mode="HTML",
                                            )
        coin_store = join("images/common_images", "coin_store.jpg")
        with open(coin_store, "rb") as coin_store:
            await query.message.reply_photo(photo=InputFile(coin_store),
                                            caption="(3) ከዚያም ከላይ ምስሉ ላይ እንደተመለከተው ወደ ፕሮፋይልዎ ሲገቡ ከላይቩ ወይም ከፓርቲው ትሬዠር ቦክስ ያገኙት coin ከዚህ "
                                                    "በፊት ከነበረው coin "
                                                    "ጋር ተደምሮ የሚቀመጥ ይሆናል።\n\n"
                                                    " <b>‼️ ልብ ይበሉ እነዚህ ኮይኖች/coins አፑ የሚከፍለን ክፍያዎች ናቸው።</b>\n\n"
                                                    "ስለዚህ እነዚህን ነጥቦች exchange አድርገን ወደ ነጥብ/point ከዚያም ወደ ገንዘብ ቀይረን ወደ "
                                                    "አካዉንታችን ወይም ወደ ቴሌ ብር ማስገባት እንችላለን።"
                                                    "<b>ለምሳሌ፡ </b>100,000 coins ቢኖረን ወደ point exchange ሲደረግ 70,"
                                                    "000 point ይሆናል።\n"
                                                    "70,000 point ደግሞ ወደ ገንዘብ ሲቀየር $7 አለን ማለት ነው።",
                                            parse_mode="HTML",
                                            reply_markup=reply_markup
                                            )

    elif query.data == "back_to_main":
        # Return to the main menu
        await start(update, context)


# Global error handler
async def error_handler(update: Update, context: CallbackContext) -> None:
    """Log errors and send a user-friendly message."""
    logger.error(f"Update {update} caused error: {context.error}")

    # Handle specific errors
    if isinstance(context.error, (TimedOut, NetworkError)):
        logger.warning("Network error occurred. Retrying...")
        await asyncio.sleep(3)  # Wait before retrying
        try:
            await context.bot.get_me()  # Retry the request
        except Exception as e:
            logger.error(f"Retry failed: {e}")
            if update and update.message:
                await update.message.reply_text(
                    "❌ አልተሳካም! እባክዎ ትንሽ ቆይተው እንደገና ይሞክሩ።\n\n"
                    "የበለጠ ድጋፍ ከፈለጉ እባክዎ አስተያየትዎን ያሳውቁን።"
                )
    else:
        # Send a generic error message
        if update and update.message:
            await update.message.reply_text(
                "❌ አልተሳካም! እባክዎ ትንሽ ቆይተው እንደገና ይሞክሩ።\n\n"
                "የበለጠ ድጋፍ ከፈለጉ እባክዎ አስተያየትዎን ያሳውቁን።"
            )


# Main function to start the bot
def main() -> None:
    custom_request = HTTPXRequest(
        connect_timeout=20.0,  # Increase the connection timeout
        read_timeout=40.0,  # Increase the read timeout
    )
    application = Application.builder().token("7898073903:AAGp4hDifYI61gWWpth1P8TGYdLmYBzPFb8").request(
        custom_request).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
