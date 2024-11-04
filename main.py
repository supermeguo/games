import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 设置日志记录
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = '7433167426:AAGhK-v2s7R9PDouK-lBXFa3ZIuzt6hFKDU'

# 维护游戏状态
game_state = {
    'players': [],  # 存储玩家用户名或 ID
    'current_turn': 0,  # 当前轮到的玩家索引
    'bullet_position': random.randint(0, 5)  # 随机生成子弹位置
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if update.effective_user.username not in game_state['players']:
        game_state['players'].append(update.effective_user.username)
        await update.message.reply_text(f"{update.effective_user.username} 已加入游戏！")

    if len(game_state['players']) == 1:
        await update.message.reply_text("等待更多玩家加入...")

async def play_round(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not game_state['players']:
        await update.message.reply_text("没有足够的玩家。请使用 /start 加入游戏。")
        return

    current_player = game_state['players'][game_state['current_turn']]
    if update.effective_user.username == current_player:
        trigger_pull = random.randint(0, 5)
        result_text = ""
        if trigger_pull == game_state['bullet_position']:
            result_text = f"糟糕，{current_player} 你中枪了！喝一杯！"
            # 重置子弹位置
            game_state['bullet_position'] = random.randint(0, 5)
        else:
            result_text = f"{current_player} 安全！轮到下一位玩家。"

        await update.message.reply_text(result_text)

        # 切换到下一个玩家
        game_state['current_turn'] = (game_state['current_turn'] + 1) % len(game_state['players'])
        next_player = game_state['players'][game_state['current_turn']]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"轮到 {next_player} 了！")

    else:
        await update.message.reply_text(f"还没轮到你呢，{update.effective_user.username}。请稍等！")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^拉动扳机$'), play_round))

    application.run_polling()

if __name__ == '__main__':
    main()