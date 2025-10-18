import tkinter as tk
from tkinter import ttk
import pyautogui
from pynput import keyboard as pynput_keyboard

class AutoTyper:
    def __init__(self, root):
        self.root = root
        self.root.title("BasicBot 1.0")
        self.root.geometry("500x300")

        self.typing = False
        self.after_id = None

        # Metin Girişi
        tk.Label(root, text="Gönderilecek metin:").pack(pady=5)
        self.textbox_input = tk.Text(root, height=4, width=50)
        self.textbox_input.pack(pady=5)

        # Gecikme girişi
        tk.Label(root, text="Tuş arası süre (ms):").pack(pady=5)
        self.delay_entry = ttk.Entry(root)
        self.delay_entry.insert(0, "100")
        self.delay_entry.pack(pady=5)

        # Durum etiketi
        self.status_label = tk.Label(root, text="Hazır. Yazmaya başlamak için F8'e basın.", fg="green")
        self.status_label.pack(pady=10)

        # Bilgi
        tk.Label(root, text="⚠️ Tuş gönderilecek yere odaklanmayı unutma!", fg="red").pack(pady=5)

        # pynput ile klavye dinleyici başlat
        self.setup_pynput_listener()

        # Pencere kapanırken temizlik
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_pynput_listener(self):
        """pynput ile F8 tuşunu dinle"""
        try:
            self.listener = pynput_keyboard.Listener(on_press=self.on_key_press)
            self.listener.start()
            self.status_label.config(text="F8 tuşu bekleniyor... (Başlat/Durdur)", fg="blue")
        except Exception as e:
            self.status_label.config(text=f"pynput Hatası: {str(e)}", fg="red")

    def on_key_press(self, key):
        """Basılan tuşu kontrol et"""
        # F8 tuşu: pynput_keyboard.Key.f8
        if key == pynput_keyboard.Key.f8:
            # Tkinter ana iş parçacığından güvenli çağır
            self.root.after(0, self.toggle_typing)

    def toggle_typing(self):
        if self.typing:
            self.typing = False
            self.status_label.config(text="DURDU (F8: Başlat)", fg="red")
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
        else:
            self.typing = True
            self.status_label.config(text="YAZIYOR... (F8: Durdur)", fg="green")
            self.start_typing()

    def start_typing(self):
        text = self.textbox_input.get("1.0", tk.END).strip()
        try:
            delay_ms = int(self.delay_entry.get())
        except ValueError:
            delay_ms = 100

        if not text:
            self.status_label.config(text="HATA: Metin boş!", fg="orange")
            self.toggle_typing()
            return

        self.type_next_char(text, 0, delay_ms)

    def type_next_char(self, text, index, delay_ms):
        if not self.typing:
            return

        char = text[index % len(text)]
        pyautogui.typewrite(char)

        next_index = index + 1
        self.after_id = self.root.after(delay_ms, self.type_next_char, text, next_index, delay_ms)

    def on_closing(self):
        """Pencere kapatılırken dinleyiciyi durdur."""
        try:
            self.listener.stop()
        except:
            pass
        self.root.destroy()


# Ana uygulama
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyper(root)
    root.mainloop()