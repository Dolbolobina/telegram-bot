import asyncio
from telethon import TelegramClient, events

# ============= ВАШИ ДАННЫЕ =============
API_ID = 34296359
API_HASH = '42dbf2bb76a144e5df51bd7e33f221d3'
BOT_TOKEN = '8644698019:AAHfro_jYA_0QN1ISgE08RiaLAbH-CdtFM4'


# =======================================

async def main():
    client = await TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
    print("✅ Бот запущен! Упоминает до 50 участников группы.")

    @client.on(events.NewMessage(pattern='(?i)@all'))
    async def mention_all(event):
        # Проверяем, что сообщение из группы
        if not event.is_group:
            await event.reply("❌ Эта команда работает только в группах!")
            return

        chat = await event.get_chat()
        print(f"📢 Обработка @all в чате: {chat.title}")

        # Отправляем сообщение о начале
        status_msg = await event.reply("🔄 Получаю список участников...")

        try:
            # Получаем ВСЕХ участников группы
            all_mentions = []
            async for user in client.iter_participants(chat):
                # Пропускаем ботов и удаленные аккаунты
                if not user.bot and not user.deleted:
                    if user.username:
                        all_mentions.append(f'@{user.username}')
                    else:
                        all_mentions.append(f'[{user.first_name}](tg://user?id={user.id})')

            # Удаляем сообщение о статусе
            await status_msg.delete()

            if not all_mentions:
                await event.reply("❌ Нет участников для упоминания")
                return

            # Ограничиваем первыми 50 участниками
            mentions = all_mentions[:50]
            total_users = len(all_mentions)
            mentioned_users = len(mentions)

            # Если в группе больше 50 человек, показываем предупреждение
            if total_users > 50:
                warning = f"⚠️ В группе {total_users} участников. Упомянуто только {mentioned_users} (максимум 50).\n\n"
            else:
                warning = ""

            # Отправляем упоминания (до 50 человек в одном сообщении)
            text = f"🔔Внимание пупсики🔔\n\n{warning}" + " ".join(mentions)
            await event.reply(text, parse_mode='markdown')

            print(f"✅ Упомянуто {mentioned_users} из {total_users} участников")

        except Exception as e:
            await status_msg.edit_text(f"❌ Ошибка: {str(e)}\n\nУбедитесь, что бот - администратор группы!")
            print(f"❌ Ошибка: {e}")

    # Держим бота запущенным
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())