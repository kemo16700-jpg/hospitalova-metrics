import os
import json
import asyncio
from datetime import datetime, time
import pytz
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ─── CONFIG ───
TOKEN = os.environ.get("BOT_TOKEN", "8429196192:AAFzul-1ObLXZ4uJxkJ-CD3BhXQW2LtWBSg")
CHANNEL_ID = -1003826788764
EGYPT_TZ = pytz.timezone("Africa/Cairo")

# ─── CURRICULUM ───
TASKS = [
    {
        "id": 1,
        "phase": "المرحلة الأولى — الأساسيات",
        "title": "مقدمة في الإحصاء الطبي التطبيقي",
        "channel": "Dr. Mohamed Elsherif",
        "url": "https://www.youtube.com/playlist?list=PLnruVGowQilf3qPLK-Jhz2Suc06DBH5Cz",
        "desc": "ابدأ بالفيديو الأول من الكورس — مقدمة عن الإحصاء ولماذا يحتاجه الطبيب.",
        "question": "ما الفرق بين الإحصاء الوصفي والاستنتاجي؟",
        "options": ["الوصفي يلخص البيانات، الاستنتاجي يعمم النتائج", "الوصفي للأرقام فقط، الاستنتاجي للنصوص", "لا فرق بينهما", "الوصفي للمرضى، الاستنتاجي للأطباء"],
        "correct": 0
    },
    {
        "id": 2,
        "phase": "المرحلة الأولى — الأساسيات",
        "title": "أنواع البيانات",
        "channel": "Dr. Mohamed Elsherif",
        "url": "https://www.youtube.com/playlist?list=PLnruVGowQilf3qPLK-Jhz2Suc06DBH5Cz",
        "desc": "تعلّم الفرق بين Nominal وOrdinal وContinuous data — أساس أي تحليل.",
        "question": "درجة الألم من 1 لـ 10 — أي نوع بيانات هي؟",
        "options": ["Nominal", "Ordinal", "Continuous", "Binary"],
        "correct": 1
    },
    {
        "id": 3,
        "phase": "المرحلة الأولى — الأساسيات",
        "title": "المتوسط والوسيط والمنوال",
        "channel": "Dr. Mohamed Elsherif",
        "url": "https://www.youtube.com/playlist?list=PLnruVGowQilf3qPLK-Jhz2Suc06DBH5Cz",
        "desc": "Mean وMedian وMode — متى تستخدم كل واحدة في الأبحاث الطبية؟",
        "question": "في وجود outliers كثيرة — أي مقياس أفضل؟",
        "options": ["Mean", "Median", "Mode", "Range"],
        "correct": 1
    },
    {
        "id": 4,
        "phase": "المرحلة الأولى — الأساسيات",
        "title": "التوزيع الطبيعي",
        "channel": "Dr. Mohamed Elsherif",
        "url": "https://www.youtube.com/playlist?list=PLnruVGowQilf3qPLK-Jhz2Suc06DBH5Cz",
        "desc": "Normal Distribution — ليه مهم جداً في الإحصاء الطبي وكيف تتعرف عليه.",
        "question": "في التوزيع الطبيعي — كم نسبة البيانات داخل انحرافين معياريين؟",
        "options": ["68%", "90%", "95%", "99%"],
        "correct": 2
    },
    {
        "id": 5,
        "phase": "المرحلة الأولى — الأساسيات",
        "title": "الـ P-value",
        "channel": "Dr. Mohamed Elsherif",
        "url": "https://www.youtube.com/playlist?list=PLnruVGowQilf3qPLK-Jhz2Suc06DBH5Cz",
        "desc": "P-value — أكتر مصطلح بيتغلط فيه الناس. هنفهمه صح النهارده.",
        "question": "P-value = 0.03 معناها؟",
        "options": ["الفرق كبير جداً", "احتمال 3% إن النتيجة بالصدفة", "الدراسة مهمة", "النتيجة خاطئة بنسبة 3%"],
        "correct": 1
    },
    {
        "id": 6,
        "phase": "المرحلة الأولى — الأساسيات",
        "title": "Confidence Intervals",
        "channel": "Dr. Mohamed Elsherif",
        "url": "https://www.youtube.com/playlist?list=PLnruVGowQilf3qPLK-Jhz2Suc06DBH5Cz",
        "desc": "Confidence Intervals — ليه أهم من الـ P-value وحده في تفسير نتايج الأبحاث.",
        "question": "95% CI يعني؟",
        "options": ["النتيجة صح 95%", "لو كررنا الدراسة 100 مرة، 95 منهم هيطلع نفس الـ interval", "الخطأ 5% بس", "العينة كافية 95%"],
        "correct": 1
    },
    {
        "id": 7,
        "phase": "المرحلة الثانية — الإحصاء الحيوي",
        "title": "تصميم الدراسات",
        "channel": "Eighth Lab",
        "url": "https://www.youtube.com/playlist?list=PLt0thylmbOcnPXco89AvM6c1sN1pr0vZF",
        "desc": "RCT وCohort وCase-Control — متى تستخدم كل نوع وما هي قوة كل دراسة.",
        "question": "أقوى نوع دراسة لإثبات السببية؟",
        "options": ["Case Report", "Cohort Study", "RCT", "Cross-sectional"],
        "correct": 2
    },
    {
        "id": 8,
        "phase": "المرحلة الثانية — الإحصاء الحيوي",
        "title": "Bias وConfounding",
        "channel": "Eighth Lab",
        "url": "https://www.youtube.com/playlist?list=PLt0thylmbOcnPXco89AvM6c1sN1pr0vZF",
        "desc": "أكبر أسباب غلط الأبحاث — تعلّم تتعرف عليهم وتتجنبهم في بحثك.",
        "question": "Confounding variable هو؟",
        "options": ["متغير تم قياسه بغلط", "متغير مرتبط بالـ exposure والـ outcome معاً", "متغير غير مهم", "نوع من Bias"],
        "correct": 1
    },
    {
        "id": 9,
        "phase": "المرحلة الثانية — الإحصاء الحيوي",
        "title": "Sample Size وPower",
        "channel": "Eighth Lab",
        "url": "https://www.youtube.com/playlist?list=PLt0thylmbOcnPXco89AvM6c1sN1pr0vZF",
        "desc": "إزاي تحسب حجم العينة المناسب — سؤال لازم تعرف إجابته قبل أي بحث.",
        "question": "Power of a study = 80% معناها؟",
        "options": ["الدراسة دقيقة 80%", "80% احتمال نكتشف فرق حقيقي لو موجود", "العينة 80% كافية", "خطأ النوع الثاني 80%"],
        "correct": 1
    },
    {
        "id": 10,
        "phase": "المرحلة الثالثة — التطبيق",
        "title": "SPSS — المقدمة",
        "channel": "BioStat 101",
        "url": "https://www.youtube.com/watch?v=R2Ik-lLnaao&list=PLnruVGowQileyzRfxZbYQZzCasezy-d8s",
        "desc": "أول خطوة في SPSS — إزاي تدخل البيانات وتعمل analysis بسيطة.",
        "question": "SPSS بيُستخدم بشكل رئيسي في؟",
        "options": ["تصميم المواقع", "تحليل البيانات الإحصائية", "كتابة الأكواد", "رسم الجداول فقط"],
        "correct": 1
    },
    {
        "id": 11,
        "phase": "المرحلة الثالثة — التطبيق",
        "title": "BioStat 101 — Descriptive Statistics",
        "channel": "BioStat 101",
        "url": "https://www.youtube.com/watch?v=F7fcKHDnAz4&list=PL9GrBMsvivVWZ2Ztg5VXzKhxVF2F1q5Ld",
        "desc": "Descriptive Statistics في التطبيق الفعلي — تلخيص البيانات الطبية بشكل صح.",
        "question": "Descriptive Statistics تشمل؟",
        "options": ["Hypothesis Testing فقط", "Mean وSD وFrequencies", "Regression فقط", "P-value فقط"],
        "correct": 1
    },
    {
        "id": 12,
        "phase": "المرحلة الرابعة — R Programming",
        "title": "مقدمة في R",
        "channel": "محمد بشر زينه",
        "url": "https://youtube.com/playlist?list=PLiEE9iF6uemvnKoYt-tpU6npcEog4yEfM",
        "desc": "أول تاسك في R — تثبيت البرنامج وأول سطر كود. الجزء الأصعب هو البداية!",
        "question": "R مقارنةً بـ SPSS؟",
        "options": ["أصعب وأقل فائدة", "أسهل لكن أقل دقة", "أقوى وأكثر مرونة للأبحاث المتقدمة", "نفس الشيء تماماً"],
        "correct": 2
    },
]

# ─── USER DATA (in-memory) ───
user_data = {}  # {user_id: {"task_index": int, "score": int, "name": str}}
answered_questions = {}  # {user_id: set of task_ids answered}

def get_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"task_index": 0, "score": 0, "name": ""}
    if user_id not in answered_questions:
        answered_questions[user_id] = set()
    return user_data[user_id]

# ─── SEND TASK TO CHANNEL ───
async def send_task_to_channel(bot: Bot, task_index: int):
    if task_index >= len(TASKS):
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text="🎉 *مبروك! انتهى المنهج الكامل لـ Hospitalova Metrics*\n\nاتابعونا للمحتوى القادم! 🧪",
            parse_mode="Markdown"
        )
        return

    task = TASKS[task_index]
    msg = f"""🧪 *Hospitalova Metrics — تاسك #{task['id']}*

📚 *{task['phase']}*
━━━━━━━━━━━━━━━━
🎯 *{task['title']}*
👨‍🏫 {task['channel']}

{task['desc']}

🔗 [افتح الفيديو هنا]({task['url']})
━━━━━━━━━━━━━━━━
⏰ السؤال هييجي بعد يومين — استعد! 💪"""

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=msg,
        parse_mode="Markdown",
        disable_web_page_preview=False
    )

# ─── SEND QUESTION TO CHANNEL ───
async def send_question_to_channel(bot: Bot, task_index: int):
    if task_index >= len(TASKS):
        return
    task = TASKS[task_index]
    keyboard = [
        [InlineKeyboardButton(f"{i+1}. {opt}", callback_data=f"ch_{task['id']}_{i}")]
        for i, opt in enumerate(task['options'])
    ]
    msg = f"""❓ *سؤال على التاسك #{task['id']}*

*{task['question']}*

👇 اختار الإجابة الصح:"""
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=msg,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─── /start ───
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    name = update.effective_user.first_name or "صديقي"
    user = get_user(user_id)
    user["name"] = name

    task_index = user["task_index"]
    if task_index >= len(TASKS):
        await update.message.reply_text(
            f"🎉 مبروك يا {name}! خلصت المنهج كامل!\nنقطك: {user['score']} / {len(TASKS)}"
        )
        return

    task = TASKS[task_index]
    msg = f"""أهلاً يا {name}! 👋

مرحباً بك في *Hospitalova Metrics* 🧪

هتبدأ من *التاسك #{task['id']}*:
📚 {task['phase']}
🎯 {task['title']}

🔗 [افتح الفيديو]({task['url']})

بعد ما تخلص ابعت /done ✅"""

    await update.message.reply_text(msg, parse_mode="Markdown")

# ─── /done ───
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    task_index = user["task_index"]

    if task_index >= len(TASKS):
        await update.message.reply_text("🎉 خلصت المنهج كامل! مبروك!")
        return

    task = TASKS[task_index]
    if task["id"] in answered_questions[user_id]:
        await update.message.reply_text("✅ الفيديو ده خلصته بالفعل!")
        return

    keyboard = [
        [InlineKeyboardButton(f"{i+1}. {opt}", callback_data=f"pr_{task['id']}_{i}_{user_id}")]
        for i, opt in enumerate(task['options'])
    ]
    await update.message.reply_text(
        f"ممتاز! 🎯 سؤال سريع على التاسك:\n\n*{task['question']}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─── CALLBACK ───
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("_")

    if data[0] == "pr":  # private answer
        task_id = int(data[1])
        chosen = int(data[2])
        user_id = int(data[3])
        user = get_user(user_id)

        task = next((t for t in TASKS if t["id"] == task_id), None)
        if not task:
            return

        if task_id in answered_questions[user_id]:
            await query.edit_message_text("سبق وجاوبت على السؤال ده! ✅")
            return

        answered_questions[user_id].add(task_id)
        correct = task["correct"]

        if chosen == correct:
            user["score"] += 1
            user["task_index"] += 1
            next_task_index = user["task_index"]
            result = f"✅ *إجابة صح!* نقطتك: {user['score']}\n\n"
            if next_task_index < len(TASKS):
                next_task = TASKS[next_task_index]
                result += f"🎯 التاسك الجاي:\n*{next_task['title']}*\n🔗 [افتح الفيديو]({next_task['url']})\n\nبعد ما تخلص ابعت /done"
            else:
                result += "🎉 مبروك! خلصت المنهج كامل!"
        else:
            result = f"❌ *إجابة غلط!*\nالإجابة الصح: *{task['options'][correct]}*\n\nراجع الفيديو وحاول تاني مع /done"

        await query.edit_message_text(result, parse_mode="Markdown")

    elif data[0] == "ch":  # channel answer
        task_id = int(data[1])
        chosen = int(data[2])
        task = next((t for t in TASKS if t["id"] == task_id), None)
        if not task:
            return
        correct = task["correct"]
        if chosen == correct:
            await query.answer("✅ إجابة صح! 🎉", show_alert=True)
        else:
            await query.answer(f"❌ غلط! الصح: {task['options'][correct]}", show_alert=True)

# ─── /score ───
async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    name = update.effective_user.first_name or "أنت"
    completed = user["task_index"]
    total = len(TASKS)
    sc = user["score"]
    pct = int((completed / total) * 100) if total > 0 else 0
    bar = "█" * (pct // 10) + "░" * (10 - pct // 10)

    msg = f"""📊 *تقدمك في Hospitalova Metrics*

👤 {name}
{bar} {pct}%

✅ تاسكات منجزة: {completed}/{total}
⭐ نقاط: {sc}/{total}

{'🎉 خلصت المنهج كامل!' if completed >= total else f'🎯 التاسك الجاي: #{completed + 1}'}"""
    await update.message.reply_text(msg, parse_mode="Markdown")

# ─── /leaderboard ───
async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_data:
        await update.message.reply_text("لا يوجد أعضاء بعد!")
        return
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]["score"], reverse=True)[:10]
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    msg = "🏆 *Leaderboard — Hospitalova Metrics*\n\n"
    for i, (uid, data) in enumerate(sorted_users):
        name = data.get("name") or f"User {uid}"
        msg += f"{medals[i]} {name} — {data['score']} نقطة\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

# ─── SCHEDULER ───
async def scheduler(app):
    bot = app.bot
    task_index = [0]  # مؤشر التاسك الحالي للقناة
    question_pending = [False]

    while True:
        now = datetime.now(EGYPT_TZ)
        weekday = now.weekday()  # 0=Mon, 4=Fri, 5=Sat
        hour, minute = now.hour, now.minute

        # أيام التاسك: اتنين(0), جمعة(4), سبت(5) — الساعة 00:00
        if weekday in [0, 4, 5] and hour == 0 and minute == 0:
            if not question_pending[0]:
                await send_task_to_channel(bot, task_index[0])
                question_pending[0] = True
                await asyncio.sleep(61)
                continue

        # بعد يومين من التاسك — نبعت السؤال
        # (هنا بنبعت السؤال في نفس اليوم بعد 48 ساعة)
        if weekday in [2, 0, 1] and hour == 0 and minute == 0 and question_pending[0]:
            await send_question_to_channel(bot, task_index[0])
            task_index[0] += 1
            question_pending[0] = False
            await asyncio.sleep(61)
            continue

        await asyncio.sleep(30)

# ─── MAIN ───
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CallbackQueryHandler(callback))

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler(app))
    app.run_polling()

if __name__ == "__main__":
    main()
