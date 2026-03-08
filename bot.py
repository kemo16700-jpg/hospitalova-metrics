import os
import asyncio
import pytz
from datetime import datetime
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8429196192:AAFzul-1ObLXZ4uJxkJ-CD3BhXQW2LtWBSg"
CHANNEL_ID = -1003826788764
EGYPT_TZ = pytz.timezone("Africa/Cairo")

TASKS = [
    {"id":1,"phase":"المرحلة الأولى","title":"مقدمة في الإحصاء الطبي","channel":"Dr. Mohamed Elsherif","url":"https://www.youtube.com/playlist?list=PLnruVGowQilf3qPLK-Jhz2Suc06DBH5Cz","desc":"ابدأ بالفيديو الأول — مقدمة عن الإحصاء ولماذا يحتاجه الطبيب.","question":"ما الفرق بين الإحصاء الوصفي والاستنتاجي؟","options":["الوصفي يلخص البيانات، الاستنتاجي يعمم النتائج","الوصفي للأرقام فقط","لا فرق بينهما","الوصفي للمرضى فقط"],"correct":0},
    {"id":2,"phase":"المرحلة الأولى","title":"أنواع البيانات","channel":"Dr. Mohamed Elsherif","url":"https://www.youtube.com/playlist?list=PLnruVGowQilf3qPLK-Jhz2Suc06DBH5Cz","desc":"Nominal وOrdinal وContinuous — أساس أي تحليل إحصائي.","question":"درجة الألم من 1 لـ 10 أي نوع بيانات؟","options":["Nominal","Ordinal","Continuous","Binary"],"correct":1},
    {"id":3,"phase":"المرحلة الأولى","title":"P-value","channel":"Dr. Mohamed Elsherif","url":"https://www.youtube.com/playlist?list=PLnruVGowQilf3qPLK-Jhz2Suc06DBH5Cz","desc":"P-value — أكتر مصطلح بيتغلط فيه الناس. هنفهمه صح.","question":"P-value = 0.03 معناها؟","options":["الفرق كبير جداً","احتمال 3% إن النتيجة بالصدفة","الدراسة مهمة جداً","النتيجة خاطئة 3%"],"correct":1},
    {"id":4,"phase":"المرحلة الأولى","title":"Confidence Intervals","channel":"Dr. Mohamed Elsherif","url":"https://www.youtube.com/playlist?list=PLnruVGowQilf3qPLK-Jhz2Suc06DBH5Cz","desc":"CI — ليه أهم من الـ P-value وحده في تفسير الأبحاث.","question":"95% CI يعني؟","options":["النتيجة صح 95%","لو كررنا 100 مرة 95 منهم نفس الـ interval","الخطأ 5% بس","العينة كافية 95%"],"correct":1},
    {"id":5,"phase":"المرحلة الثانية","title":"تصميم الدراسات","channel":"Eighth Lab","url":"https://www.youtube.com/playlist?list=PLt0thylmbOcnPXco89AvM6c1sN1pr0vZF","desc":"RCT وCohort وCase-Control — متى تستخدم كل نوع.","question":"أقوى نوع دراسة لإثبات السببية؟","options":["Case Report","Cohort Study","RCT","Cross-sectional"],"correct":2},
    {"id":6,"phase":"المرحلة الثانية","title":"Bias وConfounding","channel":"Eighth Lab","url":"https://www.youtube.com/playlist?list=PLt0thylmbOcnPXco89AvM6c1sN1pr0vZF","desc":"أكبر أسباب غلط الأبحاث — تعلّم تتعرف عليهم.","question":"Confounding variable هو؟","options":["متغير تم قياسه بغلط","متغير مرتبط بالـ exposure والـ outcome معاً","متغير غير مهم","نوع من Bias"],"correct":1},
    {"id":7,"phase":"المرحلة الثالثة","title":"SPSS — المقدمة","channel":"BioStat 101","url":"https://www.youtube.com/watch?v=R2Ik-lLnaao&list=PLnruVGowQileyzRfxZbYQZzCasezy-d8s","desc":"أول خطوة في SPSS — إزاي تدخل البيانات وتعمل analysis.","question":"SPSS بيستخدم بشكل رئيسي في؟","options":["تصميم المواقع","تحليل البيانات الإحصائية","كتابة الأكواد","رسم الجداول فقط"],"correct":1},
    {"id":8,"phase":"المرحلة الثالثة","title":"BioStat 101 — Descriptive Statistics","channel":"BioStat 101","url":"https://www.youtube.com/watch?v=F7fcKHDnAz4&list=PL9GrBMsvivVWZ2Ztg5VXzKhxVF2F1q5Ld","desc":"Descriptive Statistics في التطبيق الفعلي.","question":"Descriptive Statistics تشمل؟","options":["Hypothesis Testing فقط","Mean وSD وFrequencies","Regression فقط","P-value فقط"],"correct":1},
    {"id":9,"phase":"المرحلة الرابعة","title":"مقدمة في R","channel":"محمد بشر زينه","url":"https://youtube.com/playlist?list=PLiEE9iF6uemvnKoYt-tpU6npcEog4yEfM","desc":"أول تاسك في R — تثبيت البرنامج وأول سطر كود.","question":"R مقارنة بـ SPSS؟","options":["أصعب وأقل فائدة","أسهل لكن أقل دقة","أقوى وأكثر مرونة للأبحاث المتقدمة","نفس الشيء تماماً"],"correct":2},
]

user_data = {}
answered = {}

def get_user(uid, name=""):
    if uid not in user_data:
        user_data[uid] = {"task_index": 0, "score": 0, "name": name}
    if uid not in answered:
        answered[uid] = set()
    return user_data[uid]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    name = update.effective_user.first_name or "صديقي"
    user = get_user(uid, name)
    idx = user["task_index"]
    if idx >= len(TASKS):
        await update.message.reply_text(f"مبروك يا {name}! خلصت المنهج!\nنقطك: {user['score']}/{len(TASKS)}")
        return
    task = TASKS[idx]
    await update.message.reply_text(
        f"أهلاً يا {name}!\nمرحباً بك في Hospitalova Metrics\n\n"
        f"هتبدأ من التاسك #{task['id']}:\n{task['phase']}\n{task['title']}\n\n"
        f"افتح الفيديو: {task['url']}\n\nبعد ما تخلص ابعت /done",
    )

async def done_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    idx = user["task_index"]
    if idx >= len(TASKS):
        await update.message.reply_text("خلصت المنهج كامل! مبروك!")
        return
    task = TASKS[idx]
    if task["id"] in answered[uid]:
        await update.message.reply_text("الفيديو ده خلصته بالفعل!")
        return
    keyboard = [[InlineKeyboardButton(f"{i+1}. {opt}", callback_data=f"pr_{task['id']}_{i}_{uid}")] for i, opt in enumerate(task["options"])]
    await update.message.reply_text(
        f"سؤال سريع:\n\n{task['question']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def score_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    name = update.effective_user.first_name or "انت"
    completed = user["task_index"]
    total = len(TASKS)
    pct = int((completed / total) * 100) if total > 0 else 0
    bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
    await update.message.reply_text(
        f"تقدمك في Hospitalova Metrics\n\n{name}\n{bar} {pct}%\n\n"
        f"تاسكات منجزة: {completed}/{total}\nنقاط: {user['score']}/{total}"
    )

async def leaderboard_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_data:
        await update.message.reply_text("لا يوجد اعضاء بعد!")
        return
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]["score"], reverse=True)[:10]
    medals = ["1","2","3","4","5","6","7","8","9","10"]
    msg = "Leaderboard - Hospitalova Metrics\n\n"
    for i, (uid, data) in enumerate(sorted_users):
        msg += f"{medals[i]}. {data.get('name','User')} - {data['score']} نقطة\n"
    await update.message.reply_text(msg)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_")

    if parts[0] == "pr":
        task_id, chosen, uid = int(parts[1]), int(parts[2]), int(parts[3])
        user = get_user(uid)
        task = next((t for t in TASKS if t["id"] == task_id), None)
        if not task:
            return
        if task_id in answered[uid]:
            await query.edit_message_text("سبق وجاوبت على السؤال ده!")
            return
        answered[uid].add(task_id)
        if chosen == task["correct"]:
            user["score"] += 1
            user["task_index"] += 1
            idx = user["task_index"]
            result = f"اجابة صح! نقطتك: {user['score']}\n\n"
            if idx < len(TASKS):
                nt = TASKS[idx]
                result += f"التاسك الجاي:\n{nt['title']}\n{nt['url']}\n\nابعت /done لما تخلص"
            else:
                result += "مبروك! خلصت المنهج كامل!"
        else:
            result = f"غلط!\nالصح: {task['options'][task['correct']]}\n\nراجع الفيديو وابعت /done تاني"
        await query.edit_message_text(result)

    elif parts[0] == "ch":
        task_id, chosen = int(parts[1]), int(parts[2])
        task = next((t for t in TASKS if t["id"] == task_id), None)
        if not task:
            return
        if chosen == task["correct"]:
            await query.answer("اجابة صح!", show_alert=True)
        else:
            await query.answer(f"غلط! الصح: {task['options'][task['correct']]}", show_alert=True)

async def scheduler(app: Application):
    task_index = [0]
    question_pending = [False]
    last_task_day = [None]

    while True:
        now = datetime.now(EGYPT_TZ)
        weekday = now.weekday()
        today = now.date()

        if weekday in [0, 4, 5] and now.hour == 0 and now.minute == 0 and last_task_day[0] != today:
            if task_index[0] < len(TASKS):
                task = TASKS[task_index[0]]
                msg = (f"Hospitalova Metrics - تاسك #{task['id']}\n\n"
                       f"{task['phase']}\n{task['title']}\n{task['channel']}\n\n"
                       f"{task['desc']}\n\n{task['url']}\n\nالسؤال هييجي بعد يومين!")
                await app.bot.send_message(chat_id=CHANNEL_ID, text=msg)
                last_task_day[0] = today
                question_pending[0] = True

        if question_pending[0] and weekday in [2, 0, 1] and now.hour == 0 and now.minute == 0:
            if task_index[0] < len(TASKS):
                task = TASKS[task_index[0]]
                keyboard = [[InlineKeyboardButton(f"{i+1}. {opt}", callback_data=f"ch_{task['id']}_{i}")] for i, opt in enumerate(task["options"])]
                await app.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=f"سؤال على التاسك #{task['id']}\n\n{task['question']}\n\nاختار الاجابة:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                task_index[0] += 1
                question_pending[0] = False

        await asyncio.sleep(30)

async def post_init(app: Application) -> None:
    asyncio.ensure_future(scheduler(app))

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("done", done_cmd))
    app.add_handler(CommandHandler("score", score_cmd))
    app.add_handler(CommandHandler("leaderboard", leaderboard_cmd))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
