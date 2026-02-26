# Textile-billing-system
A lightweight, professional desktop billing application built using Python (Tkinter) for generating GST-compliant invoices with automatic PDF export.
Perfect 👍
Here is a **complete, clean, professional `README.md`** for your GitHub repository.

You can copy everything below and paste it into a file named:

```
README.md
```

---

# 🧾 Shivay Billing System

A professional desktop billing application built using **Python (Tkinter)** for generating GST-compliant invoices with automatic PDF export.

Designed for textile businesses like **Shivay Textiles**, this system supports multiple billing types with separate invoice series management and clean PDF generation.

---

## 🚀 Features

### 📌 Smart Invoice Series Management

* **Normal Billing** → `1, 2, 3...`
* **Yarn Billing** → `Y1, Y2, Y3...`
* **Jobwork Billing** → `J1, J2, J3...`
* Separate auto-increment counters
* Invoice numbers persist after restart

---

### 🧾 Automatic GST Calculation

* CGST + SGST (within Gujarat)
* IGST (outside Gujarat)
* Real-time taxable & total calculation

---

### 📄 Professional PDF Invoice Generation

* Clean invoice layout
* Company header with GST details
* Buyer details section
* Bank details section
* Amount in words (Indian number system)
* 45-day credit auto due-date
* Auto-created `invoices/` folder

---

### 👥 Customer Auto-Save & Suggestions

* Saves customer name, GSTIN, address, state
* Auto-suggestion while typing
* JSON-based lightweight storage

---

### 🖥 Cross-Platform Desktop Application

* Runs on **Windows & macOS**
* Can be converted to:

  * `.exe` (Windows)
  * `.app` (macOS)

---

## 🛠 Tech Stack

* Python 3.10+
* Tkinter (GUI)
* ReportLab (PDF generation)
* Pillow (Image handling)
* JSON (Local storage)

---

## 📂 Project Structure

```
ShivayBilling/
│
├── billing.py              # Main GUI application
├── invoice_pdf.py          # PDF generation logic
├── logo.jpg                # Company logo
├── invoice_counters.json   # Invoice number storage (auto-created)
├── customer_history.json   # Customer data storage (auto-created)
└── invoices/               # Generated PDF invoices
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/TirthThesiya/Textile-Billing-System.git
cd ShivayBilling
```

---

## 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### macOS

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If no `requirements.txt`:

```bash
pip install reportlab pillow
```

---

# ▶️ Run the Application

```bash
python billing.py
```

The billing type selection window will appear on startup.

---

# 📦 Build Executable

## 🪟 Windows (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "logo.jpg;." billing.py
```

Output:

```
dist/billing.exe
```

---

## 🍎 macOS (.app)

Install py2app:

```bash
pip install py2app
```

Then build:

```bash
python setup.py py2app
```

Output:

```
dist/Shivay Billing.app
```

---

# 📈 Ideal For

* Textile manufacturers
* Yarn suppliers
* Jobwork units
* Small & medium GST businesses
* Offline billing operations

---

# 🔮 Future Improvements

* Monthly GST report export
* Invoice search & reprint
* User login system
* Database integration
* Cloud backup support
* Installer package generation

---

# 📜 License

This project is developed for internal business use.
You are free to modify and customize it for your own business needs.

---

# 👨‍💻 Author
Tirth Jaswant Thesiya
Developed for **Shivay Textiles**
Built with Python & Tkinter.

---
