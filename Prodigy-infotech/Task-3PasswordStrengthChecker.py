import tkinter as tk
from tkinter import ttk
import string

# Toggle password visibility
def toggle_password():
    if show_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

# Check password logic
def assess_password():
    password = entry.get()
    lower = upper = digit = special = 0
    feedback = []

    for char in password:
        if char in string.ascii_lowercase:
            lower += 1
        elif char in string.ascii_uppercase:
            upper += 1
        elif char in string.digits:
            digit += 1
        elif char in string.punctuation:
            special += 1

    length = len(password)
    score = 0

    if lower: score += 1
    else: feedback.append("• Add lowercase letters")

    if upper: score += 1
    else: feedback.append("• Add uppercase letters")

    if digit: score += 1
    else: feedback.append("• Add numbers")

    if special: score += 1
    else: feedback.append("• Add special characters")

    if length >= 8: score += 1
    else: feedback.append("• Use at least 8 characters")

    # Strength feedback
    if score <= 2:
        result.set("❌ Weak Password")
        result_label.config(foreground="#ff4d4d")
    elif score in [3, 4]:
        result.set("⚠️ Moderate Password")
        result_label.config(foreground="#ffaa00")
    else:
        result.set("✅ Strong Password")
        result_label.config(foreground="#33cc33")

    if feedback:
        feedback_text.set("\n".join(feedback))
    else:
        feedback_text.set("✔ Your password is strong!")

# GUI Setup
root = tk.Tk()
root.title("🔐 Password Strength Checker")
root.geometry("550x420")
root.configure(bg="#161b2f")
root.resizable(False, False)

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#161b2f", foreground="white", font=("Segoe UI", 11))
style.configure("TEntry", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 11, "bold"), background="#3d4a72", foreground="white", padding=10)
style.map("TButton", background=[("active", "#4e5d8d")])

# Title
ttk.Label(root, text="🔐 Password Strength Checker", font=("Segoe UI", 15, "bold")).pack(pady=(30, 10))

# Entry
entry = ttk.Entry(root, show="*", width=35)
entry.pack(pady=10)

# Show Password Checkbox
show_var = tk.BooleanVar()
show_checkbox = ttk.Checkbutton(root, text="Show Password", variable=show_var, command=toggle_password)
show_checkbox.pack()

# Check Button
ttk.Button(root, text="Check Strength", command=assess_password).pack(pady=15)

# Strength Result
result = tk.StringVar()
result_label = ttk.Label(root, textvariable=result, font=("Segoe UI", 13, "bold"))
result_label.pack(pady=(10, 5))

# Feedback
feedback_text = tk.StringVar()
feedback_label = ttk.Label(root, textvariable=feedback_text, wraplength=460, justify="left", font=("Segoe UI", 10))
feedback_label.pack(pady=10)

# Footer
tk.Label(root, text="Made with ❤️ for learning purposes", bg="#161b2f", fg="#888888", font=("Segoe UI", 9)).pack(side="bottom", pady=10)

# Run app
root.mainloop()
