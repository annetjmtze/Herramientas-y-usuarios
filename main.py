import argparse
import threading

def main():
    parser = argparse.ArgumentParser(description="Dr. Ahorro Bot")
    parser.add_argument("--channel", choices=["telegram", "whatsapp", "all"],
                        default="all", help="Canal a ejecutar")
    parser.add_argument("--port", type=int, default=5000,
                        help="Puerto para WhatsApp (Flask)")
    args = parser.parse_args()

    if args.channel == "telegram":
        from bot.telegram_handler import run_telegram_bot
        run_telegram_bot()
    elif args.channel == "whatsapp":
        from bot.whatsapp_handler import run_whatsapp_bot
        run_whatsapp_bot(port=args.port)
    else:  # "all"
        from bot.whatsapp_handler import run_whatsapp_bot
        from bot.telegram_handler import run_telegram_bot
        t = threading.Thread(target=run_whatsapp_bot, args=(args.port,), daemon=True)
        t.start()
        run_telegram_bot()

if __name__ == "__main__":
    main()