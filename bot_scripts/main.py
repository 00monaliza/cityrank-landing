import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ParseMode

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Константы
TOKEN = "8580895159:AAFJ5feGwE0tan9UIw3_9I87UmuAIVL2_j0"
INITIAL_CODE = "ВЕБИНАР"
BONUS_WORDS = ["ВЫБИРАЮ", "ПУТЬ", "РАЗВИТИЯ"]

# Состояния для ConversationHandler
WAITING_INITIAL_CODE, WAITING_BONUS_WORDS = range(2)

# Подсостояния для сбора бонусных слов (0, 1, 2)
BONUS_STAGE_1, BONUS_STAGE_2, BONUS_STAGE_3 = 0, 1, 2

BONUSES = [
    {
        "title": "🎁 Гид по промптам",
        "description": "Готовые формулы и шаблоны для работы с ИИ"
    },
    {
        "title": "📊 Шаблон маркетингового плана",
        "description": "Структура для автоматизации маркетинга"
    },
    {
        "title": "💰 Калькулятор ROI",
        "description": "Считаем доходность рекламных кампаний"
    },
    {
        "title": "🎯 Стратегия продаж на год",
        "description": "План развития бизнеса с ИИ"
    },
    {
        "title": "📝 Чек-лист контент-менеджера",
        "description": "Все, что нужно для создания контента"
    },
    {
        "title": "🤖 Архив промптов 2024",
        "description": "500+ готовых промптов для разных задач"
    },
    {
        "title": "💡 Мини-курс 'ИИ для предпринимателя'",
        "description": "Краткое руководство по автоматизации"
    },
    {
        "title": "🎓 Видео-уроки по ChatGPT",
        "description": "7 видео для начинающих"
    },
    {
        "title": "📚 E-book 'Нейросети в бизнесе'",
        "description": "Практическое пособие с примерами"
    },
    {
        "title": "🔐 Аккаунт в базе данных с ресурсами",
        "description": "Доступ к закрытой библиотеке материалов"
    }
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик команды /start"""
    user = update.effective_user
    
    welcome_message = """🎁 Держи свой бонус — гид по промптам, который я обещала!

Внутри всё, что нужно для работы с нейросетями:

📖 Часть 1. Основы
Готовые формулы и шаблоны для повседневных задач — от написания текстов до генерации идей

🚀 Часть 2. Для бизнеса
Промпты для маркетинга, продаж и автоматизации — то, что реально приносит деньги

📥 Забирай здесь: https://drive.google.com/file/d/11U920n3qqoLvjanZdyVwtbk_EksjHceA/view?usp=sharing

💎 Но это только начало.
На вебинаре покажу, как превратить эти знания в конкретные результаты — больше клиентов, меньше рутины, выше доход.

Научу работать с ИИ так, чтобы он экономил твоё время и делал работу за тебя.
Увидимся на эфире! ⚡"""
    
    await update.message.reply_text(welcome_message)
    
    # Задержка перед следующим сообщением
    await asyncio.sleep(3)
    
    # Кнопка для подтверждения участия
    keyboard = [
        [InlineKeyboardButton("Забрать 10 бонусов", callback_data="get_bonuses")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    bonus_request = """✨ Для подтверждения, что ты с вебинара, введи кодовое слово из эфира и получи 10 бонусов!"""
    
    await update.message.reply_text(bonus_request, reply_markup=reply_markup)
    
    # Сохраняем состояние: пользователь ожидает подтверждения
    context.user_data['state'] = WAITING_INITIAL_CODE
    
    return WAITING_INITIAL_CODE


async def handle_initial_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик ввода начального кодового слова"""
    user_input = update.message.text.strip().upper()
    
    if user_input == INITIAL_CODE:
        # Успешно введено кодовое слово
        success_message = """🔓 Готово, всё верно!
Ты успешно подтвердил(а) участие и уже получил(а) бонус — гид по промптам."""
        
        await update.message.reply_text(success_message)
        
        # Задержка перед мотивирующим сообщением
        await asyncio.sleep(3)
        
        # Мотивирующее сообщение
        motivation_message = """💥 Это ещё не всё, досмотрите все 3 дня вебинара, соберите кодовые слова и получите 10 бонусов бесплатно, общая стоимость которых составляет 250 000 тг. Для вас они бесплатны — нужно собрать кодовые слова."""
        
        keyboard = [
            [InlineKeyboardButton("Старт", callback_data="start_bonus_words")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            motivation_message,
            reply_markup=reply_markup
        )
        
        # Переходим в состояние ожидания нажатия кнопки/сбора бонусов
        context.user_data['state'] = WAITING_BONUS_WORDS
        context.user_data['bonus_stage'] = -1  # Ещё не начали собирать слова
        
        return WAITING_BONUS_WORDS
    else:
        # Неправильное кодовое слово
        error_message = """😔 Похоже, кодовое слово введено неверно.
Попробуй ещё раз позже.
Если что — всегда можешь вернуться командой /start.
До встречи!"""
        
        await update.message.reply_text(error_message)
        
        # Завершаем диалог
        return ConversationHandler.END


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    
    if query.data == "get_bonuses":
        await query.answer()
        
        # Запрашиваем кодовое слово для подтверждения
        await query.edit_message_text(text="Введите кодовое слово из эфира для подтверждения участия.")
        
        # Переходим в состояние ввода начального кодового слова
        context.user_data['state'] = WAITING_INITIAL_CODE
        return WAITING_INITIAL_CODE
    
    elif query.data == "start_bonus_words":
        await query.answer()
        
        # Начинаем с первого слова
        context.user_data['bonus_stage'] = BONUS_STAGE_1
        context.user_data['collected_words'] = []
        
        message = "Введите 1 кодовое слово."
        await query.edit_message_text(text=message)
        
        return WAITING_BONUS_WORDS
    
    elif query.data == "start_over":
        await query.answer()
        await query.delete_message()
        
        # Перезапускаем /start
        await start(update, context)
        return WAITING_INITIAL_CODE
    
    elif query.data == "support":
        await query.answer()
        await query.message.reply_text(
            "📧 Свяжись с нами для вопросов и поддержки!"
        )
        return WAITING_BONUS_WORDS


async def handle_bonus_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик ввода бонусных слов"""
    user_input = update.message.text.strip().upper()
    
    # Получаем текущий этап
    stage = context.user_data.get('bonus_stage', -1)
    collected_words = context.user_data.get('collected_words', [])
    
    if stage == -1:
        # Пользователь еще не нажал кнопку "Старт", просто ждем
        return WAITING_BONUS_WORDS
    
    if stage == BONUS_STAGE_1:
        if user_input == BONUS_WORDS[0]:
            collected_words.append(BONUS_WORDS[0])
            context.user_data['collected_words'] = collected_words
            context.user_data['bonus_stage'] = BONUS_STAGE_2
            
            await update.message.reply_text("Отлично! ✅ Теперь введите 2 кодовое слово.")
            return WAITING_BONUS_WORDS
        else:
            await update.message.reply_text(
                "Это не то кодовое слово. Проверьте правильность и попробуйте ещё раз."
            )
            return WAITING_BONUS_WORDS
    
    elif stage == BONUS_STAGE_2:
        if user_input == BONUS_WORDS[1]:
            collected_words.append(BONUS_WORDS[1])
            context.user_data['collected_words'] = collected_words
            context.user_data['bonus_stage'] = BONUS_STAGE_3
            
            await update.message.reply_text("Супер! ✅ Теперь введите 3 кодовое слово.")
            return WAITING_BONUS_WORDS
        else:
            await update.message.reply_text(
                "Это не то кодовое слово. Проверьте правильность и попробуйте ещё раз."
            )
            return WAITING_BONUS_WORDS
    
    elif stage == BONUS_STAGE_3:
        if user_input == BONUS_WORDS[2]:
            collected_words.append(BONUS_WORDS[2])
            context.user_data['collected_words'] = collected_words
            
            # Формируем финальное сообщение с бонусами
            words_str = " ".join(collected_words)
            
            final_message = f"""🔥 Ты собрал(а) все 3 кодовых слова: {words_str}.

Как и обещала, вот твои бонусы 👇

🎁 Поздравляю! Ты прошёл(ла) весь путь до конца.

Как и обещала, вот 10 бонусов общей стоимостью 250 000 тг, которые ты получаешь бесплатно.

"""
            
            # Добавляем список бонусов
            for idx, bonus in enumerate(BONUSES, 1):
                final_message += f"{idx}. {bonus['title']}\n   {bonus['description']}\n\n"
            
            final_message += "Сохрани это сообщение — доступ к материалам может пригодиться в любой момент."
            
            # Кнопки для финального сообщения
            keyboard = [
                [InlineKeyboardButton("Вернуться в начало", callback_data="start_over")],
                [InlineKeyboardButton("Задать вопрос", callback_data="support")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Задержка перед финальным сообщением
            await asyncio.sleep(3)
            
            await update.message.reply_text(
                final_message,
                reply_markup=reply_markup
            )
            
            # Завершаем диалог
            return ConversationHandler.END
        else:
            await update.message.reply_text(
                "Похоже, последнее кодовое слово введено неверно. Пересмотри нужный фрагмент вебинара и попробуй ещё раз."
            )
            return WAITING_BONUS_WORDS
    
    return WAITING_BONUS_WORDS


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена текущего диалога"""
    await update.message.reply_text(
        "Диалог отменён. Используй /start для начала с начала."
    )
    return ConversationHandler.END


def main() -> None:
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Создаем ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_INITIAL_CODE: [
                CallbackQueryHandler(button_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_initial_code),
            ],
            WAITING_BONUS_WORDS: [
                CallbackQueryHandler(button_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bonus_words),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
    )
    
    # Добавляем обработчики
    application.add_handler(conv_handler)
    
    # Запускаем бота
    print("✅ Бот запущен!")
    print("🤖 Ожидание входящих сообщений...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
