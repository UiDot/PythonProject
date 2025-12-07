import logging
import sqlite3
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# --- Настройка логирования ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Настройки бота ---
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_CHAT_ID = 123456789  # Ваш Telegram ID для получения уведомлений
ADMIN_USER_ID = 123456789  # Ваш Telegram ID для админ-панели

# --- Товары и цены ---
PRODUCTS = {
    "sugar_regular": {"name": "🍬 Сахар обычный", "price": 5},
    "sugar_brown": {"name": "🟫 Коричневый сахар", "price": 8},
    "sugar_cubes": {"name": "🧊 Сахар в кубиках", "price": 12},
    "caramel": {"name": "🍮 Карамель", "price": 15},
}

# --- База данных ---
def init_db():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            product TEXT,
            price INTEGER,
            coordinates TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_order(user_id, username, first_name, last_name, product, coords):
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO orders (user_id, username, first_name, last_name, product, price, coordinates) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, username, first_name, last_name, product, PRODUCTS[product]["price"], coords)
    )
    conn.commit()
    order_id = c.lastrowid
    conn.close()
    return order_id


def get_all_orders():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = c.fetchall()
    conn.close()
    return orders


def update_order_status(order_id, status):
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()


# --- Хэндлеры ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(p["name"])] for p in PRODUCTS.values()]
    await update.message.reply_text(
        "Выберите товар для заказа:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


async def handle_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    for key, value in PRODUCTS.items():
        if value["name"] == text:
            context.user_data["product"] = key
            keyboard = [
                [InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm_{key}")],
                [InlineKeyboardButton("❌ Отменить", callback_data="cancel")]
            ]
            await update.message.reply_text(
                f"{value['name']}\nЦена: {value['price']} алмазов\nПодтвердите заказ:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
    await update.message.reply_text("Выберите товар из меню")


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("confirm_"):
        product = query.data.split("_", 1)[1]
        context.user_data["product"] = product
        await query.edit_message_text("Отправьте координаты сундука (X Y Z):")

    elif query.data == "cancel":
        context.user_data.clear()
        await query.edit_message_text("Заказ отменен")

    elif query.data.startswith("admin_"):
        action, order_id = query.data.split("_")[1], query.data.split("_")[2]
        update_order_status(order_id, "completed" if action == "confirm" else "cancelled")
        await query.edit_message_text(
            f"Заказ #{order_id} {'выполнен' if action == 'confirm' else 'отменен'}!"
        )


async def handle_coords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "product" not in context.user_data:
        await update.message.reply_text("Сначала выберите товар")
        return

    coords = update.message.text.strip()
    if not re.match(r"^-?\d+\s+-?\d+\s+-?\d+$", coords):
        await update.message.reply_text("Неверный формат координат. Используйте: X Y Z")
        return

    user = update.effective_user
    order_id = save_order(user.id, user.username, user.first_name, user.last_name, context.user_data["product"], coords)

    # Уведомление админу
    try:
        await context.bot.send_message(
            ADMIN_CHAT_ID,
            f"Новый заказ #{order_id}\nТовар: {PRODUCTS[context.user_data['product']]['name']}\n"
            f"Цена: {PRODUCTS[context.user_data['product']]['price']} алмазов\nКоординаты: {coords}\n"
            f"Пользователь: {user.first_name} (@{user.username or 'нет'})",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ Выполнить", callback_data=f"admin_confirm_{order_id}"),
                InlineKeyboardButton("❌ Отменить", callback_data=f"admin_cancel_{order_id}")
            ]])
        )
    except Exception as e:
        logger.error(f"Ошибка уведомления админу: {e}")

    await update.message.reply_text(f"Заказ #{order_id} принят! Ожидайте доставки.")
    context.user_data.clear()


async def admin_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("Доступ запрещен")
        return

    orders = get_all_orders()
    if not orders:
        await update.message.reply_text("Заказов нет")
        return

    message = "Все заказы:\n\n"
    for order in orders:
        message += f"#{order[0]} - {PRODUCTS[order[5]]['name']} - {order[7]} - {order[8]}\n"
    await update.message.reply_text(message[:4000])


# --- Запуск бота ---
def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("orders", admin_orders))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_product))
    app.add_handler(MessageHandler(filters.Regex(r"^-?\d+\s+-?\d+\s+-?\d+$"), handle_coords))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
