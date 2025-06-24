import tkinter as tk
from tracker import add_entry, calculate_summary, get_entries
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as tb

# --------------------- Functions ---------------------
def add_data(entry_type):
    category = entry_cat.get()
    amount = entry_amt.get()
    if category and amount:
        try:
            float(amount)
            add_entry(entry_type, category, amount)
            status_label.config(text="✅ Entry added!", foreground="green")
            entry_cat.delete(0, tk.END)
            entry_amt.delete(0, tk.END)
            show_summary()
            update_charts()
        except ValueError:
            status_label.config(text="❌ Invalid amount", foreground="red")

def show_summary():
    income, expense, balance = calculate_summary()
    summary_label.config(text=f"💰 Income: ₹{income}  🧾 Expense: ₹{expense}  🧮 Balance: ₹{balance}")

def update_charts():
    entries = get_entries()
    categories = {}
    for e in entries:
        if e.get('type') == 'Expense':
            cat = e.get('category', 'Other')
            amt = float(e.get('amount', 0))
            categories[cat] = categories.get(cat, 0) + amt

    fig.clear()
    ax = fig.add_subplot(111)

    if categories:
        colors = plt.get_cmap('Set3').colors
        ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', colors=colors)
        ax.set_title("🧾 Expense Breakdown", fontsize=12)
    else:
        ax.text(0.5, 0.5, 'No expenses yet', ha='center', va='center', fontsize=12)

    canvas.draw()

def switch_theme():
    current = style.theme.name
    new_theme = "solar" if current == "darkly" else "darkly"
    style.theme_use(new_theme)

# --------------------- UI Setup ---------------------
app = tb.Window(themename="solar")
app.title("💹 Budget Tracker App")
app.geometry("700x700")
app.minsize(700, 700)
style = tb.Style()

frame = tb.Frame(app, padding=20)
frame.pack(fill='x')

# Labels & Inputs
tb.Label(frame, text="Category:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w")
entry_cat = tb.Entry(frame, width=30, font=("Segoe UI", 12))
entry_cat.grid(row=0, column=1, padx=5, pady=5)

tb.Label(frame, text="Amount:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w")
entry_amt = tb.Entry(frame, width=30, font=("Segoe UI", 12))
entry_amt.grid(row=1, column=1, padx=5, pady=5)

# Buttons
tb.Button(frame, text="Add Income", bootstyle="success-outline", width=20, command=lambda: add_data("Income")).grid(row=2, column=0, pady=10)
tb.Button(frame, text="Add Expense", bootstyle="danger-outline", width=20, command=lambda: add_data("Expense")).grid(row=2, column=1, pady=10)
tb.Button(frame, text="🌓 Switch Theme", bootstyle="info-outline", width=20, command=switch_theme).grid(row=2, column=2, padx=5)

# Summary
summary_label = tb.Label(frame, text="", font=("Segoe UI", 12, "bold"))
summary_label.grid(row=3, column=0, columnspan=3, pady=10)

# Status
status_label = tb.Label(frame, text="", font=("Segoe UI", 10))
status_label.grid(row=4, column=0, columnspan=3)

# Chart Frame
chart_frame = tb.Frame(app)
chart_frame.pack(fill='both', expand=True, padx=20, pady=10)
fig = plt.Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack(expand=True)

# Load Initial Summary and Chart
show_summary()
update_charts()

app.mainloop()
