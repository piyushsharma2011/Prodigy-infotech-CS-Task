import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

class FuturisticEncryptorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Quantum Image Encryptor")
        self.root.geometry("1200x750")
        self.root.configure(bg="#121212")

        self.image_path = None
        self.encrypted_image = None
        self.key = None
        self.original_img = None

        self.setup_style()
        self.build_ui()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("TFrame", background="#121212")
        style.configure("TLabel", background="#121212", foreground="#e0e0e0", font=("Segoe UI", 12))
        style.configure("Title.TLabel", font=("Orbitron", 28, "bold"), foreground="#00ffe0")
        style.configure("Card.TLabelframe", background="#1f1f1f", foreground="#00ffe0", font=("Segoe UI", 14, "bold"))
        style.configure("TButton", font=("Segoe UI", 12), background="#00ffe0", foreground="#000000")
        style.map("TButton", background=[("active", "#00cccc")])

    def build_ui(self):
        title = ttk.Label(self.root, text="🧠 Quantum Image Encryptor", style="Title.TLabel")
        title.pack(pady=25)

        # Image Panels
        image_frame = ttk.Frame(self.root)
        image_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.original_card = ttk.Labelframe(image_frame, text="Original Image", style="Card.TLabelframe")
        self.original_card.grid(row=0, column=0, padx=30, ipadx=10, ipady=10)

        self.processed_card = ttk.Labelframe(image_frame, text="Encrypted / Decrypted Image", style="Card.TLabelframe")
        self.processed_card.grid(row=0, column=1, padx=30, ipadx=10, ipady=10)

        self.left_label = ttk.Label(self.original_card)
        self.left_label.pack()

        self.right_label = ttk.Label(self.processed_card)
        self.right_label.pack()

        # Buttons Frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=30)

        self.add_button(control_frame, "🖼️ Choose Image", self.load_image, 0)
        self.add_button(control_frame, "🔐 Encrypt", self.encrypt_image, 1)
        self.add_button(control_frame, "🔓 Decrypt", self.decrypt_image, 2)
        self.add_button(control_frame, "♻️ Reset", self.reset_image, 3)
        self.add_button(control_frame, "💾 Save Original", self.save_original, 4)
        self.add_button(control_frame, "📤 Download Encrypted", self.download_encrypted, 5)
        self.add_button(control_frame, "📥 Download Decrypted", self.download_decrypted, 6)
        self.add_button(control_frame, "❌ Exit", self.root.quit, 7)

        # Status Bar
        self.status = ttk.Label(self.root, text="Ready", anchor=tk.W, relief=tk.SUNKEN, style="TLabel")
        self.status.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

    def add_button(self, parent, text, command, col):
        btn = ttk.Button(parent, text=text, command=command)
        btn.grid(row=0, column=col, padx=6, pady=10)

    def set_status(self, msg):
        self.status.config(text=msg)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            img = Image.open(self.image_path)
            self.original_img = img
            img.thumbnail((300, 300))
            tk_img = ImageTk.PhotoImage(img)
            self.left_label.configure(image=tk_img)
            self.left_label.image = tk_img
            self.right_label.configure(image=tk_img)
            self.right_label.image = tk_img
            self.set_status("✅ Image loaded successfully.")
        else:
            self.set_status("⚠️ No image selected.")

    def encrypt_image(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "No image selected.")
            return

        img_gray = cv2.imread(self.image_path, 0).astype(float) / 255.0
        self.key = np.random.normal(0, 0.1, img_gray.shape) + np.finfo(float).eps
        self.encrypted_image = img_gray / self.key
        encrypted_img = (self.encrypted_image * 255).astype(np.uint8)
        cv2.imwrite("temp_encrypted.jpg", encrypted_img)

        img = Image.open("temp_encrypted.jpg")
        img.thumbnail((300, 300))
        tk_img = ImageTk.PhotoImage(img)
        self.right_label.configure(image=tk_img)
        self.right_label.image = tk_img
        self.set_status("🔐 Image encrypted.")

    def decrypt_image(self):
        if self.encrypted_image is None or self.key is None:
            messagebox.showwarning("Warning", "No encrypted image.")
            return

        decrypted = self.encrypted_image * self.key
        decrypted *= 255.0
        cv2.imwrite("temp_decrypted.jpg", decrypted.astype(np.uint8))

        img = Image.open("temp_decrypted.jpg")
        img.thumbnail((300, 300))
        tk_img = ImageTk.PhotoImage(img)
        self.right_label.configure(image=tk_img)
        self.right_label.image = tk_img
        self.set_status("🔓 Image decrypted.")

    def reset_image(self):
        if self.original_img:
            img = self.original_img.copy()
            img.thumbnail((300, 300))
            tk_img = ImageTk.PhotoImage(img)
            self.right_label.configure(image=tk_img)
            self.right_label.image = tk_img
            self.set_status("♻️ Reset to original.")
        else:
            self.set_status("⚠️ Nothing to reset.")

    def save_original(self):
        if self.original_img:
            file = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file:
                self.original_img.save(file)
                self.set_status("💾 Original saved.")
        else:
            self.set_status("⚠️ No image to save.")

    def download_encrypted(self):
        if self.encrypted_image is not None:
            file = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file:
                cv2.imwrite(file, (self.encrypted_image * 255).astype(np.uint8))
                self.set_status("📤 Encrypted image saved.")
        else:
            self.set_status("⚠️ Nothing encrypted.")

    def download_decrypted(self):
        if self.encrypted_image is not None and self.key is not None:
            file = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file:
                decrypted = self.encrypted_image * self.key
                decrypted *= 255.0
                cv2.imwrite(file, decrypted.astype(np.uint8))
                self.set_status("📥 Decrypted image saved.")
        else:
            self.set_status("⚠️ Nothing decrypted.")

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = FuturisticEncryptorUI(root)
    root.mainloop()


