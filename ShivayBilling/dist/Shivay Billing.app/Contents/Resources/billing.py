import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from invoice_pdf import generate_invoice_pdf

# ============================================================
# INVOICE COUNTERS
# ============================================================

INVOICE_COUNTER_FILE = "invoice_counters.json"

def load_counters():
    if not os.path.exists(INVOICE_COUNTER_FILE):
        return {"normal": 0, "yarn": 0, "jobwork": 0}
    with open(INVOICE_COUNTER_FILE, "r") as f:
        return json.load(f)

def save_counters(counters):
    with open(INVOICE_COUNTER_FILE, "w") as f:
        json.dump(counters, f, indent=4)

invoice_counters = load_counters()

# ============================================================
# CUSTOMER HISTORY
# ============================================================

HISTORY_FILE = "customer_history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

customer_history = load_history()

# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Shivay Textiles Billing System")
root.geometry("1050x750")

BG = "#F2F2F2"
FG = "#000000"
root.configure(bg=BG)

# ============================================================
# BILLING TYPE
# ============================================================

billing_type = None       # normal / yarn / jobwork
invoice_prefix = ""       # "", "Y", "J"

# ============================================================
# VARIABLES
# ============================================================

invoice_no_var = tk.StringVar()
invoice_date_var = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y"))

customer_name_var = tk.StringVar()
customer_address_var = tk.StringVar()
customer_gst_var = tk.StringVar()
customer_state_var = tk.StringVar()

taxable_var = tk.StringVar(value="0.00")
total_var = tk.StringVar(value="0.00")

description_var = tk.StringVar()
hsn_var = tk.StringVar()
qty_var = tk.StringVar()
rate_var = tk.StringVar()

# ============================================================
# BILLING TYPE SELECTION POPUP
# ============================================================

def choose_billing_type():
    global billing_type, invoice_prefix

    win = tk.Toplevel(root)
    win.title("Select Billing Type")
    win.geometry("300x200")
    win.grab_set()

    def select(option):
        global billing_type, invoice_prefix

        billing_type = option
        invoice_prefix = "" if option == "normal" else ("Y" if option == "yarn" else "J")

        next_no = invoice_counters[option] + 1
        invoice_no_var.set(f"{invoice_prefix}{next_no}")

        win.destroy()

    tk.Label(win, text="What are you billing for?",
             font=("Arial", 12, "bold")).pack(pady=15)

    tk.Button(win, text="Normal Billing", width=20,
              command=lambda: select("normal")).pack(pady=5)

    tk.Button(win, text="Yarn Billing", width=20,
              command=lambda: select("yarn")).pack(pady=5)

    tk.Button(win, text="Jobwork Billing", width=20,
              command=lambda: select("jobwork")).pack(pady=5)

# ============================================================
# CUSTOMER AUTOFILL
# ============================================================

def update_suggestions(*args):
    typed = customer_name_var.get().lower()
    suggestion_list.delete(0, tk.END)

    if not typed:
        return

    for name in customer_history:
        if name.lower().startswith(typed):
            suggestion_list.insert(tk.END, name)

def select_suggestion(event):
    try:
        name = suggestion_list.get(suggestion_list.curselection())
        customer_name_var.set(name)

        cust = customer_history[name]
        customer_address_var.set(cust["address"])
        customer_gst_var.set(cust["gst"])
        customer_state_var.set(cust["state"])
    except:
        pass

customer_name_var.trace("w", update_suggestions)

# ============================================================
# ITEM HANDLING
# ============================================================

def add_item():
    try:
        qty = float(qty_var.get())
        rate = float(rate_var.get())
        amount = qty * rate
    except:
        messagebox.showerror("Error", "Invalid Quantity or Rate")
        return

    item_tree.insert("", "end", values=(
        description_var.get(),
        hsn_var.get(),
        qty,
        rate,
        f"{amount:.2f}"
    ))

    description_var.set("")
    hsn_var.set("")
    qty_var.set("")
    rate_var.set("")

    update_totals()

def delete_selected_item():
    for row in item_tree.selection():
        item_tree.delete(row)
    update_totals()

def update_totals():
    taxable = sum(float(item_tree.item(r)["values"][-1])
                  for r in item_tree.get_children())

    taxable_var.set(f"{taxable:.2f}")

    if customer_state_var.get().strip().lower() == "gujarat":
        cgst = taxable * 0.025
        sgst = taxable * 0.025
        igst = 0
    else:
        cgst = sgst = 0
        igst = taxable * 0.05

    total_var.set(f"{taxable + cgst + sgst + igst:.2f}")

# ============================================================
# RESET FORM
# ============================================================

def reset_form():
    customer_name_var.set("")
    customer_address_var.set("")
    customer_gst_var.set("")
    customer_state_var.set("")

    for row in item_tree.get_children():
        item_tree.delete(row)

    taxable_var.set("0.00")
    total_var.set("0.00")
    invoice_date_var.set(datetime.now().strftime("%d-%m-%Y"))

# ============================================================
# GENERATE PDF
# ============================================================

def generate_pdf():
    if not customer_name_var.get():
        messagebox.showerror("Error", "Enter Customer Name")
        return

    items = []
    for row in item_tree.get_children():
        desc, hsn, qty, rate, amt = item_tree.item(row)["values"]
        items.append((desc, str(hsn), float(qty), float(rate), float(amt)))

    if not items:
        messagebox.showerror("Error", "No items added")
        return

    taxable = float(taxable_var.get())

    if customer_state_var.get().strip().lower() == "gujarat":
        cgst = taxable * 0.025
        sgst = taxable * 0.025
        igst = 0
    else:
        cgst = sgst = 0
        igst = taxable * 0.05

    data = {
        "invoice_no": invoice_no_var.get(),
        "date": invoice_date_var.get(),
        "customer_name": customer_name_var.get(),
        "customer_address": customer_address_var.get(),
        "customer_gst": customer_gst_var.get(),
        "customer_state": customer_state_var.get(),
        "taxable": taxable,
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "total": taxable + cgst + sgst + igst
    }

    customer_history[data["customer_name"]] = {
        "address": data["customer_address"],
        "gst": data["customer_gst"],
        "state": data["customer_state"]
    }
    save_history(customer_history)

    generate_invoice_pdf(data, items)

    invoice_counters[billing_type] += 1
    save_counters(invoice_counters)

    next_no = invoice_counters[billing_type] + 1
    invoice_no_var.set(f"{invoice_prefix}{next_no}")

    messagebox.showinfo("Success", "Invoice Generated Successfully!")
    reset_form()

# ============================================================
# UI LAYOUT
# ============================================================

frame0 = tk.LabelFrame(root, text="Invoice Info", bg=BG, fg=FG, font=("Arial", 12, "bold"))
frame0.pack(fill="x", padx=10, pady=5)

tk.Label(frame0, text="Invoice No:", bg=BG).grid(row=0, column=0)
tk.Entry(frame0, textvariable=invoice_no_var, width=20).grid(row=0, column=1)

tk.Label(frame0, text="Invoice Date:", bg=BG).grid(row=0, column=2)
tk.Entry(frame0, textvariable=invoice_date_var, width=20).grid(row=0, column=3)

frame1 = tk.LabelFrame(root, text="Customer Details", bg=BG, fg=FG, font=("Arial", 12, "bold"))
frame1.pack(fill="x", padx=10, pady=5)

tk.Label(frame1, text="Name:", bg=BG).grid(row=0, column=0)
tk.Entry(frame1, textvariable=customer_name_var, width=30).grid(row=0, column=1)

tk.Label(frame1, text="Address:", bg=BG).grid(row=1, column=0)
tk.Entry(frame1, textvariable=customer_address_var, width=60).grid(row=1, column=1)

tk.Label(frame1, text="GSTIN:", bg=BG).grid(row=2, column=0)
tk.Entry(frame1, textvariable=customer_gst_var, width=30).grid(row=2, column=1)

tk.Label(frame1, text="State:", bg=BG).grid(row=3, column=0)
tk.Entry(frame1, textvariable=customer_state_var, width=30).grid(row=3, column=1)

suggestion_list = tk.Listbox(frame1, height=4)
suggestion_list.grid(row=0, column=2, rowspan=4, padx=10)
suggestion_list.bind("<<ListboxSelect>>", select_suggestion)

frame2 = tk.LabelFrame(root, text="Add Item", bg=BG, fg=FG, font=("Arial", 12, "bold"))
frame2.pack(fill="x", padx=10, pady=5)

tk.Label(frame2, text="Description:", bg=BG).grid(row=0, column=0)
tk.Entry(frame2, textvariable=description_var, width=22).grid(row=0, column=1)

tk.Label(frame2, text="HSN:", bg=BG).grid(row=0, column=2)
tk.Entry(frame2, textvariable=hsn_var, width=10).grid(row=0, column=3)

tk.Label(frame2, text="Qty:", bg=BG).grid(row=0, column=4)
tk.Entry(frame2, textvariable=qty_var, width=8).grid(row=0, column=5)

tk.Label(frame2, text="Rate:", bg=BG).grid(row=0, column=6)
tk.Entry(frame2, textvariable=rate_var, width=10).grid(row=0, column=7)

tk.Button(frame2, text="Add Item", command=add_item, bg="#8AE68A").grid(row=0, column=8, padx=10)

frame3 = tk.Frame(root, bg=BG)
frame3.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("Description", "HSN", "Qty", "Rate", "Amount")
item_tree = ttk.Treeview(frame3, columns=columns, show="headings", height=14)

for col in columns:
    item_tree.heading(col, text=col)
    item_tree.column(col, width=160)

item_tree.pack(fill="both", expand=True)

tk.Button(root, text="Delete Selected Item", command=delete_selected_item,
          bg="#FF6666").pack(pady=5)

frame4 = tk.LabelFrame(root, text="Totals", bg=BG, fg=FG, font=("Arial", 12, "bold"))
frame4.pack(fill="x", padx=10, pady=5)

tk.Label(frame4, text="Taxable:", bg=BG).grid(row=0, column=0)
tk.Entry(frame4, textvariable=taxable_var, width=15).grid(row=0, column=1)

tk.Label(frame4, text="Total:", bg=BG).grid(row=0, column=2)
tk.Entry(frame4, textvariable=total_var, width=15).grid(row=0, column=3)

tk.Button(root, text="Generate Invoice PDF", command=generate_pdf,
          bg="#4A90E2", font=("Arial", 12, "bold")).pack(pady=15)

# ============================================================
# START APP
# ============================================================

choose_billing_type()
root.mainloop()
