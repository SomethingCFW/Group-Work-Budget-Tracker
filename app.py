import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Calculations/logic by Luis Valdes

def budget(): 
    try:
        income = float(income_entry.get()) 
        income_type = income_type_var.get() 
        budget_type = budget_type_var.get() 
        state = state_var.get() 

        if not income_type or not budget_type or not state or income_entry.get() == "": 
            messagebox.showwarning("Input Warning", "Please make sure to select Income Type, Budget Type, and State!") 
            return
    
        if income < 0 or float(expense_entries["housing"].get()) < 0 or float(expense_entries["food"].get()) < 0 or float(expense_entries["healthcare"].get()) < 0 or float(expense_entries["debt"].get()) < 0 or float(expense_entries["clothes"].get()) < 0 or float(expense_entries["going out"].get()) < 0 or float(expense_entries["activities"].get()) < 0:
            messagebox.showerror("Input Error", "Income and expenses must not be negative numbers!")
            return
#conversions and simple math plus error handling
        if income_type == "Weekly": 
            weekly_income = income 
        elif income_type == "Bi-Weekly": 
            weekly_income = income / 2 
        elif income_type == "Monthly": 
            weekly_income = income / 4 
        elif income_type == "Yearly": 
            weekly_income = income / 52 
        else:
            messagebox.showerror("Input Error", "Income type selected is invalid choose again!")
            return
    
        if budget_type == "Weekly":
            budget_income = weekly_income
        elif budget_type == "Bi-Weekly":
            budget_income = weekly_income * 2
        elif budget_type == "Monthly":
            budget_income = weekly_income * 4
        elif budget_type == "Yearly":
            budget_income = weekly_income * 52
        else:
            messagebox.showerror("Input Error", "Budget type selected is invalid choose again!")
            return
    
#tax rates by state, rounded to nearest hundrenth
        tax_rates = {
            "AL": 0.05,
            "AK": 0.00,
            "AZ": 0.05,
            "AR": 0.06,
            "CA": 0.09,
            "CO": 0.04,
            "CT": 0.06,
            "DE": 0.06,
            "FL": 0.00,
            "GA": 0.06,
            "HI": 0.11,
            "ID": 0.07,
            "IL": 0.05,
            "IN": 0.03,
            "IA": 0.09,
            "KS": 0.05,
            "KY": 0.06,
            "LA": 0.06,
            "ME": 0.07,
            "MD": 0.06,
            "MA": 0.05,
            "MI": 0.04,
            "MN": 0.10,
            "MS": 0.05,
            "MO": 0.05,
            "MT": 0.10,
            "NE": 0.07,
            "NV": 0.00,
            "NH": 0.00,
            "NJ": 0.11,
            "NM": 0.05,
            "NY": 0.08,
            "NC": 0.05,
            "ND": 0.03,
            "OH": 0.05,
            "OK": 0.05,
            "OR": 0.10,
            "PA": 0.03,
            "RI": 0.06,
            "SC": 0.07,
            "SD": 0.00,
            "TN": 0.00,
            "TX": 0.00,
            "UT": 0.05,
            "VT": 0.09,
            "VA": 0.06,
            "WA": 0.00,
            "WV": 0.07,
            "WI": 0.08,
            "WY": 0.00
        }
        tax_rate = tax_rates.get(state, 0.07)
        taxes = budget_income * tax_rate
#expenses with advice
        expenses_total = {
            "Housing": float(expense_entries["housing"].get() or 0),
            "Food": float(expense_entries["food"].get() or 0),
            "Healthcare": float(expense_entries["healthcare"].get() or 0),
            "Debt": float(expense_entries["debt"].get() or 0),
            "Clothes": float(expense_entries["clothes"].get() or 0),
            "Going Out": float(expense_entries["going out"].get() or 0),
            "Activities": float(expense_entries["activities"].get() or 0)
        }
        
        total_expenses = sum(expenses_total.values()) + taxes
        income_after_expenses = weekly_income - total_expenses

        if income_after_expenses < 0:
            messagebox.showwarning("Budget Warning", "Your expenses are too high, consider cutting down on non-essential things.")
        elif income_after_expenses > 0:
            messagebox.showinfo("Budget Info", "Good job keep it up and consider investment options.")
            
        budget_need = weekly_income * 0.5
        want_budget = weekly_income * 0.3
        savings_budget = weekly_income * 0.2
#display results
        result_text = (
            f"Budget Income ({budget_type}): ${budget_income:.2f}\n"
            f"Taxes: ${taxes:.2f}\n"
            f"Total Expenses: ${total_expenses:.2f}\n"
            f"Income After Expenses: ${income_after_expenses:.2f}\n\n"
            f"Recommended Budgets:\n"
            f"  Needs (50%): ${budget_need:.2f}\n"
            f"  Wants (30%): ${want_budget:.2f}\n"
            f"  Savings (20%): ${savings_budget:.2f}"
        )
        result_label.config(text=result_text, foreground="#FFD54F")

        customizable_pie_chart(chart_frame, expenses_total, total_income=budget_income)

    except ValueError:
        messagebox.showerror("Input Error", "Please make sure all things are filled out correctly!")

    except Exception as e:
        messagebox.showerror("Error", f"Something wrong occured {e}")




# Visualization by Lars Fahnemann
def customizable_pie_chart(parent, expenses_total, total_income=1000,
                           colors=None, title="Monthly Budget Breakdown",
                           show_percent=True, show_values=True,
                           explode=None, fig_bg="#1A1A1A", plot_bg="#000000"):
    # Clear previous chart
    for widget in parent.winfo_children():
        widget.destroy()

    labels, values = [], []
    for k, v in expenses_total.items():
        try:
            v = float(v or 0)
        except:
            v = 0
        if v > 0:
            labels.append(k)
            values.append(v)

    if not values:
        tk.Label(parent, text="No expenses to chart", fg="#777777",
                 bg=fig_bg, font=("Segoe UI", 11, "italic")).pack(expand=True)
        return

    if colors is None:
        base_colors = ["#FFD54F", "#4FC3F7", "#81C784", "#E57373",
                       "#BA68C8", "#FFB74D", "#64B5F6"]
        colors = [base_colors[i % len(base_colors)] for i in range(len(values))]

    if explode is None:
        explode = [0.04] * len(values)

    def make_autopct(values):
        def autopct(pct):
            total = sum(values)
            val = total * pct / 100.0
            if show_percent and show_values:
                return f"{pct:.1f}%\n${val:,.0f}"
            elif show_values:
                return f"${val:,.0f}"
            elif show_percent:
                return f"{pct:.1f}%"
            else:
                return ""
        return autopct

    
    fig = Figure(figsize=(4.2, 3.7), facecolor=fig_bg)
    ax = fig.add_subplot(111)
    ax.set_facecolor(plot_bg)

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct=make_autopct(values),
        startangle=90,
        explode=explode,
        shadow=False,
        pctdistance=0.8,
        labeldistance=1.1
    )

    for t in texts:
        t.set_color("#E0E0E0")
        t.set_fontsize(8)
    for t in autotexts:
        t.set_color("#000000")
        t.set_fontsize(7)
        t.set_fontweight("bold")

    
    ax.set_title(f"{title}\nTotal: ${total_income:,.0f}",
                 color="#FFD54F", fontsize=11, pad=25, loc="center")

    
    fig.tight_layout(pad=3)

    ax.axis("equal")

    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)


#  DATA STORAGE FUNCTIONS (by james)) 
DATA_FILE = "budget_data.json"

def save_data():
    """Save all input fields and settings to a JSON file."""
    data = {
        "income": income_entry.get(),
        "income_type": income_type_var.get(),
        "budget_type": budget_type_var.get(),
        "state": state_var.get(),
        "expenses": {label: entry.get() for label, entry in expense_entries.items()},
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        result_label.config(text="✅ Data saved successfully!", foreground="#4CAF50")
    except Exception as e:
        result_label.config(text=f"Error saving data: {e}", foreground="#FF5555")


def load_data():
    """Load data from the JSON file and update GUI fields."""
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        income_entry.delete(0, tk.END)
        income_entry.insert(0, data.get("income", ""))

        income_type_var.set(data.get("income_type", ""))
        budget_type_var.set(data.get("budget_type", ""))
        state_var.set(data.get("state", ""))

        for label, entry in expense_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, data["expenses"].get(label, ""))

        result_label.config(text=" Data loaded successfully!", foreground="#4FC3F7")
    except FileNotFoundError:
        result_label.config(text=" No saved data found.", foreground="#FFB74D")
    except Exception as e:
        result_label.config(text=f"Error loading data: {e}", foreground="#FF5555")




#Source For Tkinter Layout and Styling by ChatGPT and tweaked by all team members
# ----------------------------
#  APP SETUP
# ----------------------------
root = tk.Tk()
root.title("Budget Tracker")
root.state("zoomed")  # Start maximized
root.configure(bg="#000000")

# ----------------------------
#  STYLE
# ----------------------------
style = ttk.Style()
style.theme_use("clam")

# Color palette
BACKGROUND = "#000000"
CARD_BG = "#0D0D0D"
TEXT_MAIN = "#E0E0E0"
TEXT_ACCENT = "#FFD54F"
TEXT_HEADER = "#FFD54F"      
ENTRY_BG = "#1A1A1A"
BORDER = "#333333"
BUTTON_BG = "#FFD54F"
BUTTON_ACTIVE = "#FFD54F"

# Configure ttk elements
style.configure("TFrame", background=BACKGROUND)
style.configure("Card.TFrame", background=CARD_BG, relief="flat")
style.configure("TLabel", background=BACKGROUND, foreground=TEXT_MAIN, font=("Segoe UI", 10))
style.configure("Header.TLabel", foreground=TEXT_HEADER, background=BACKGROUND, font=("Segoe UI", 12, "bold"))
style.configure("Title.TLabel", foreground=TEXT_HEADER, background=BACKGROUND, font=("Segoe UI", 20, "bold"))
style.configure("TEntry", fieldbackground=ENTRY_BG, foreground=TEXT_MAIN, insertcolor=TEXT_MAIN)
style.configure("TButton", background=BUTTON_BG, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0)
style.map("TButton", background=[("active", BUTTON_ACTIVE)])
style.configure("TCombobox",
                fieldbackground=ENTRY_BG,
                background=ENTRY_BG,
                foreground=TEXT_MAIN,
                arrowcolor=TEXT_MAIN)

# ----------------------------
#  MAIN FRAME
# ----------------------------
main = ttk.Frame(root, padding=20)
main.pack(fill="both", expand=True)

# Layout proportions
main.rowconfigure(0, weight=0)   # title
main.rowconfigure(1, weight=1)   # income
main.rowconfigure(2, weight=3)   # expenses
main.rowconfigure(3, weight=0)   # buttons
main.rowconfigure(4, weight=0)   # bottom
main.columnconfigure(0, weight=1, uniform="equal")
main.columnconfigure(1, weight=1, uniform="equal")

# ----------------------------
#  TITLE
# ----------------------------
ttk.Label(main, text="Personal Budget Tracker", style="Title.TLabel").grid(
    row=0, column=0, columnspan=2, pady=(0, 15)
)

# ----------------------------
#  INCOME SECTION (Compact)
# ----------------------------
income_frame = ttk.Frame(main, style="Card.TFrame", padding=10)
income_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 5))

ttk.Label(income_frame, text="Income", style="Header.TLabel").grid(
    row=0, column=0, columnspan=2, pady=(0, 8), sticky="n"
)

ttk.Label(income_frame, text="Income Amount:").grid(row=1, column=0, sticky="w", pady=3)
income_entry = ttk.Entry(income_frame, font=("Segoe UI", 10))
income_entry.grid(row=1, column=1, sticky="ew", pady=3)

ttk.Label(income_frame, text="Income Time Frame:").grid(row=2, column=0, sticky="w", pady=3)
income_type_var = tk.StringVar()
income_box = ttk.Combobox(
    income_frame, textvariable=income_type_var,
    values=["Weekly", "Bi-Weekly", "Monthly", "Yearly"], font=("Segoe UI", 10)
)
income_box.grid(row=2, column=1, sticky="ew", pady=3)

ttk.Label(income_frame, text="Budget Time Frame:").grid(row=3, column=0, sticky="w", pady=3)
budget_type_var = tk.StringVar()
budget_box = ttk.Combobox(
    income_frame, textvariable=budget_type_var,
    values=["Weekly", "Bi-Weekly", "Monthly", "Yearly"], font=("Segoe UI", 10)
)
budget_box.grid(row=3, column=1, sticky="ew", pady=3)

ttk.Label(income_frame, text="State:").grid(row=4, column=0, sticky="w", pady=3)
state_var = tk.StringVar()
state_box = ttk.Combobox(
    income_frame, textvariable=state_var,
    values=[
        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID",
        "IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS",
        "MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK",
        "OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV",
        "WI","WY"
    ], font=("Segoe UI", 10)
)
state_box.grid(row=4, column=1, sticky="ew", pady=3)

income_frame.columnconfigure(1, weight=1)

# ----------------------------
#  EXPENSES SECTION
# ----------------------------
expense_frame = ttk.Frame(main, style="Card.TFrame", padding=15)
expense_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 10))

ttk.Label(expense_frame, text="Expenses", style="Header.TLabel").grid(
    row=0, column=0, columnspan=2, pady=(0, 10), sticky="n"
)

expenses = ["Housing", "Food", "Healthcare", "Debt", "Clothes", "Going Out", "Activities"]
expense_entries = {}

for i, label in enumerate(expenses, start=1):
    ttk.Label(expense_frame, text=f"{label}:").grid(row=i, column=0, sticky="e", pady=5, padx=(0, 10))
    entry = ttk.Entry(expense_frame, font=("Segoe UI", 10))
    entry.grid(row=i, column=1, sticky="ew", pady=5)
    expense_entries[label.lower()] = entry

expense_frame.columnconfigure(1, weight=1)

# ----------------------------
#  RIGHT PANEL (Chart + Results)
# ----------------------------
right_panel = ttk.Frame(main, style="Card.TFrame", padding=20)
right_panel.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=20, pady=10)
right_panel.rowconfigure(0, weight=2)  # chart area
right_panel.rowconfigure(1, weight=1)  # results area
right_panel.columnconfigure(0, weight=1)

# Chart placeholder
chart_frame = ttk.Frame(right_panel, style="Card.TFrame")
chart_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
ttk.Label(chart_frame, text="Budget Chart", style="Header.TLabel").pack(pady=(0, 10))
chart_canvas = tk.Canvas(chart_frame, width=400, height=250,
                         bg="#111111", highlightthickness=1, highlightbackground=BORDER)
chart_canvas.create_text(200, 125, text="(Chart will appear here)", fill="#666666", font=("Segoe UI", 11, "italic"))
chart_canvas.pack(fill="both", expand=True)

# Results placeholder
result_frame = ttk.Frame(right_panel, style="Card.TFrame", padding=10)
result_frame.grid(row=1, column=0, sticky="nsew")
ttk.Label(result_frame, text="Results", style="Header.TLabel").pack(pady=(0, 8))
result_label = tk.Label(
    result_frame,
    text="Budget summary will appear here...",
    font=("Segoe UI", 10),
    fg="#FFD54F",
    bg=CARD_BG,
    justify="left",
    wraplength=350, 
    anchor="nw"
)
result_label.pack(fill="both", expand=True, padx=5, pady=5)

# ----------------------------
#  BUTTONS
# ----------------------------
button_frame = ttk.Frame(main, style="TFrame")
button_frame.grid(row=3, column=0, columnspan=2, pady=15)

ttk.Button(button_frame, text="Save Data", command=save_data).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Load Data", command=load_data).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="Calculate Budget", command=budget).grid(row=0, column=2, padx=10)

# ----------------------------
#  RUN
# ----------------------------
root.mainloop()