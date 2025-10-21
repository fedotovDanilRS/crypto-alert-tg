
try:
    from distutils.version import StrictVersion
except ImportError:
    import fix_distutils

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time
import json
from datetime import datetime
import os


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CryptoDetector:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🔍 Crypto Price Detector")
        self.root.geometry("800x600")
        self.root.resizable(True, True)


        self.telegram_token = tk.StringVar()
        self.chat_id = tk.StringVar()
        self.crypto_symbol = tk.StringVar()
        self.target_price = tk.StringVar()
        self.message_text = tk.StringVar()
        self.condition = tk.StringVar(value="below")


        self.is_monitoring = False
        self.monitor_thread = None


        self.load_settings()

        self.create_widgets()

    def create_widgets(self):

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)


        title_label = ctk.CTkLabel(
            main_frame,
            text="🔍 Crypto Price Detector",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))


        self.tabview = ctk.CTkTabview(main_frame, width=700, height=450)
        self.tabview.pack(pady=10)


        self.tabview.add("⚙️ Настройки")
        self.create_settings_tab()


        self.tabview.add("📊 Мониторинг")
        self.create_monitoring_tab()


        self.tabview.add("📝 Логи")
        self.create_logs_tab()

    def create_settings_tab(self):
        settings_frame = self.tabview.tab("⚙️ Настройки")


        telegram_frame = ctk.CTkFrame(settings_frame)
        telegram_frame.pack(fill="x", padx=20, pady=10)

        telegram_title = ctk.CTkLabel(
            telegram_frame,
            text="📱 Telegram Bot Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        telegram_title.pack(pady=10)


        ctk.CTkLabel(telegram_frame, text="Bot Token:").pack(anchor="w", padx=20)
        token_entry = ctk.CTkEntry(
            telegram_frame,
            textvariable=self.telegram_token,
            placeholder_text="Введите токен вашего Telegram бота",
            width=400
        )
        token_entry.pack(pady=(5, 10), padx=20)


        ctk.CTkLabel(telegram_frame, text="Chat ID:").pack(anchor="w", padx=20)
        chat_entry = ctk.CTkEntry(
            telegram_frame,
            textvariable=self.chat_id,
            placeholder_text="Введите ID чата (например: @username или 123456789)",
            width=400
        )
        chat_entry.pack(pady=(5, 10), padx=20)


        get_chat_id_btn = ctk.CTkButton(
            telegram_frame,
            text="Получить Chat ID",
            command=self.get_chat_id,
            width=150
        )
        get_chat_id_btn.pack(pady=(0, 10))


        crypto_frame = ctk.CTkFrame(settings_frame)
        crypto_frame.pack(fill="x", padx=20, pady=10)

        crypto_title = ctk.CTkLabel(
            crypto_frame,
            text="💰 Crypto Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        crypto_title.pack(pady=10)


        ctk.CTkLabel(crypto_frame, text="Криптовалюта:").pack(anchor="w", padx=20)
        crypto_entry = ctk.CTkEntry(
            crypto_frame,
            textvariable=self.crypto_symbol,
            placeholder_text="Например: bitcoin, ethereum, cardano",
            width=400
        )
        crypto_entry.pack(pady=(5, 10), padx=20)


        condition_frame = ctk.CTkFrame(crypto_frame)
        condition_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(condition_frame, text="Уведомить когда цена:").pack(side="left", padx=10)

        condition_menu = ctk.CTkOptionMenu(
            condition_frame,
            values=["below", "above"],
            variable=self.condition,
            width=100
        )
        condition_menu.pack(side="left", padx=10)

        ctk.CTkLabel(condition_frame, text="$").pack(side="left", padx=5)

        price_entry = ctk.CTkEntry(
            condition_frame,
            textvariable=self.target_price,
            placeholder_text="0.00",
            width=150
        )
        price_entry.pack(side="left", padx=5)


        ctk.CTkLabel(crypto_frame, text="Сообщение для отправки:").pack(anchor="w", padx=20, pady=(10, 0))
        message_entry = ctk.CTkTextbox(
            crypto_frame,
            height=80,
            width=400
        )
        message_entry.pack(pady=(5, 10), padx=20)
        message_entry.insert("1.0", "🚨 Алерт! {crypto} достиг цены ${price}")
        self.message_text.set("🚨 Алерт! {crypto} достиг цены ${price}")


        button_frame = ctk.CTkFrame(settings_frame)
        button_frame.pack(fill="x", padx=20, pady=20)

        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Сохранить настройки",
            command=self.save_settings,
            width=200
        )
        save_btn.pack(side="left", padx=10)

        test_btn = ctk.CTkButton(
            button_frame,
            text="🧪 Тест уведомления",
            command=self.test_notification,
            width=200
        )
        test_btn.pack(side="left", padx=10)

    def create_monitoring_tab(self):
        monitoring_frame = self.tabview.tab("📊 Мониторинг")


        status_frame = ctk.CTkFrame(monitoring_frame)
        status_frame.pack(fill="x", padx=20, pady=10)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="⏹️ Мониторинг остановлен",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.status_label.pack(pady=10)


        price_frame = ctk.CTkFrame(monitoring_frame)
        price_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(price_frame, text="Текущая цена:", font=ctk.CTkFont(size=14)).pack(pady=5)
        self.current_price_label = ctk.CTkLabel(
            price_frame,
            text="$0.00",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.current_price_label.pack(pady=5)



        control_frame = ctk.CTkFrame(monitoring_frame)
        control_frame.pack(fill="x", padx=20, pady=20)

        self.start_btn = ctk.CTkButton(
            control_frame,
            text="▶️ Начать мониторинг",
            command=self.start_monitoring,
            width=200,
            height=40
        )
        self.start_btn.pack(side="left", padx=10)

        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="⏹️ Остановить",
            command=self.stop_monitoring,
            width=200,
            height=40,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=10)



        settings_frame = ctk.CTkFrame(monitoring_frame)
        settings_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(settings_frame, text="Интервал проверки (секунды):").pack(side="left", padx=10)
        self.interval_var = tk.StringVar(value="60")
        interval_entry = ctk.CTkEntry(settings_frame, textvariable=self.interval_var, width=100)
        interval_entry.pack(side="left", padx=10)

    def create_logs_tab(self):
        logs_frame = self.tabview.tab("📝 Логи")


        self.log_text = ctk.CTkTextbox(logs_frame, height=350)
        self.log_text.pack(fill="both", expand=True, padx=20, pady=20)


        log_button_frame = ctk.CTkFrame(logs_frame)
        log_button_frame.pack(fill="x", padx=20, pady=(0, 20))

        clear_logs_btn = ctk.CTkButton(
            log_button_frame,
            text="🗑️ Очистить логи",
            command=self.clear_logs,
            width=150
        )
        clear_logs_btn.pack(side="left", padx=10)

        export_logs_btn = ctk.CTkButton(
            log_button_frame,
            text="📤 Экспорт логов",
            command=self.export_logs,
            width=150
        )
        export_logs_btn.pack(side="left", padx=10)

    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        self.log_text.insert("end", log_entry)
        self.log_text.see("end")

    def get_crypto_price(self, symbol):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": symbol.lower(),
                "vs_currencies": "usd"
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if symbol.lower() in data:
                return data[symbol.lower()]["usd"]
            else:
                return None

        except Exception as e:
            self.log_message(f"❌ Ошибка получения цены: {str(e)}")
            return None

    def send_telegram_message(self, message):
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token.get()}/sendMessage"

            data = {
                "chat_id": self.chat_id.get(),
                "text": message,
                "parse_mode": "HTML"
            }

            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()

            return True

        except Exception as e:
            self.log_message(f"❌ Ошибка отправки в Telegram: {str(e)}")
            return False

    def get_chat_id(self):
        if not self.telegram_token.get():
            messagebox.showerror("Ошибка", "Сначала введите токен бота!")
            return

        try:
            url = f"https://api.telegram.org/bot{self.telegram_token.get()}/getUpdates"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data["ok"] and data["result"]:
                chat_id = data["result"][-1]["message"]["chat"]["id"]
                self.chat_id.set(str(chat_id))
                messagebox.showinfo("Успех", f"Chat ID найден: {chat_id}")
            else:
                messagebox.showwarning("Предупреждение",
                                       "Не найдено сообщений. Отправьте любое сообщение боту и попробуйте снова.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить Chat ID: {str(e)}")

    def test_notification(self):
        if not all([self.telegram_token.get(), self.chat_id.get()]):
            messagebox.showerror("Ошибка", "Заполните все поля Telegram настроек!")
            return

        test_message = "🧪 Тестовое сообщение от Crypto Detector!"
        if self.send_telegram_message(test_message):
            messagebox.showinfo("Успех", "Тестовое сообщение отправлено!")
            self.log_message("✅ Тестовое сообщение отправлено успешно")
        else:
            messagebox.showerror("Ошибка", "Не удалось отправить тестовое сообщение!")

    def start_monitoring(self):
        if not all([self.telegram_token.get(), self.chat_id.get(),
                    self.crypto_symbol.get(), self.target_price.get()]):
            messagebox.showerror("Ошибка", "Заполните все необходимые поля!")
            return

        try:
            target_price = float(self.target_price.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную цену!")
            return

        self.is_monitoring = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text="▶️ Мониторинг активен")

        self.log_message("🚀 Мониторинг запущен")

        self.monitor_thread = threading.Thread(target=self.monitor_price, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.is_monitoring = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="⏹️ Мониторинг остановлен")

        self.log_message("⏹️ Мониторинг остановлен")

    def monitor_price(self):
        target_price = float(self.target_price.get())
        condition = self.condition.get()
        crypto_symbol = self.crypto_symbol.get()

        while self.is_monitoring:
            try:
                current_price = self.get_crypto_price(crypto_symbol)

                if current_price is not None:

                    self.root.after(0, lambda: self.current_price_label.configure(
                        text=f"${current_price:.2f}"
                    ))


                    condition_met = False
                    if condition == "below" and current_price <= target_price:
                        condition_met = True
                    elif condition == "above" and current_price >= target_price:
                        condition_met = True

                    if condition_met:
                        message = self.message_text.get().format(
                            crypto=crypto_symbol.upper(),
                            price=f"{current_price:.2f}"
                        )

                        if self.send_telegram_message(message):
                            self.root.after(0, lambda: self.log_message(
                                f"🚨 Уведомление отправлено! {crypto_symbol.upper()} = ${current_price:.2f}"
                            ))

                            self.root.after(0, self.stop_monitoring)
                        else:
                            self.root.after(0, lambda: self.log_message(
                                "❌ Не удалось отправить уведомление"
                            ))
                    else:
                        self.root.after(0, lambda: self.log_message(
                            f"📊 {crypto_symbol.upper()}: ${current_price:.2f} (цель: {condition} ${target_price})"
                        ))
                else:
                    self.root.after(0, lambda: self.log_message(
                        "❌ Не удалось получить цену"
                    ))


                interval = int(self.interval_var.get())
                time.sleep(interval)

            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Ошибка мониторинга: {str(e)}"))
                time.sleep(60)

    def save_settings(self):

        settings = {
            "telegram_token": self.telegram_token.get(),
            "chat_id": self.chat_id.get(),
            "crypto_symbol": self.crypto_symbol.get(),
            "target_price": self.target_price.get(),
            "message_text": self.message_text.get(),
            "condition": self.condition.get()
        }

        try:
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("Успех", "Настройки сохранены!")
            self.log_message("💾 Настройки сохранены")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {str(e)}")

    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)

                self.telegram_token.set(settings.get("telegram_token", ""))
                self.chat_id.set(settings.get("chat_id", ""))
                self.crypto_symbol.set(settings.get("crypto_symbol", ""))
                self.target_price.set(settings.get("target_price", ""))
                self.message_text.set(settings.get("message_text", "🚨 Алерт! {crypto} достиг цены ${price}"))
                self.condition.set(settings.get("condition", "below"))

        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")

    def clear_logs(self):
        self.log_text.delete("1.0", "end")
        self.log_message("🗑️ Логи очищены")

    def export_logs(self):
        try:
            logs = self.log_text.get("1.0", "end")
            filename = f"crypto_detector_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(logs)

            messagebox.showinfo("Успех", f"Логи экспортированы в файл: {filename}")
            self.log_message(f"📤 Логи экспортированы: {filename}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать логи: {str(e)}")

    def run(self):
        self.log_message("🚀 Crypto Price Detector запущен")
        self.root.mainloop()


if __name__ == "__main__":
    app = CryptoDetector()
    app.run()
