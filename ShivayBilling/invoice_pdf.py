from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
import datetime
import os


# ============================================================
# INDIAN NUMBER SYSTEM (Lakh / Crore)
# ============================================================
def num_to_indian_words(num):
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
             "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
             "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen",
             "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty",
            "Sixty", "Seventy", "Eighty", "Ninety"]

    def two(n):
        if n < 20:
            return units[n]
        return tens[n // 10] + (" " + units[n % 10] if n % 10 else "")

    def three(n):
        h = n // 100
        r = n % 100
        if h and r: return units[h] + " Hundred " + two(r)
        if not h and r: return two(r)
        if h and not r: return units[h] + " Hundred"
        return ""

    out = ""
    crore = num // 10000000; num %= 10000000
    lakh = num // 100000; num %= 100000
    thousand = num // 1000; num %= 1000

    if crore: out += three(crore) + " Crore "
    if lakh: out += three(lakh) + " Lakh "
    if thousand: out += two(thousand) + " Thousand "
    if num: out += three(num)

    return out.strip()


# ============================================================
# LOGO PATH
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "logo.jpg")


# ============================================================
# MAIN INVOICE FUNCTION
# ============================================================
def generate_invoice_pdf(data, items):

    invoice_no = data["invoice_no"]
    invoice_date = data["date"]

    due_date = (
        datetime.datetime.strptime(invoice_date, "%d-%m-%Y")
        + datetime.timedelta(days=45)
    ).strftime("%d-%m-%Y")

    filename = f"invoices/INV-{invoice_no}-{data['customer_name']}.pdf"
    os.makedirs("invoices", exist_ok=True)

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # ============================================================
    # TOP HEADING
    # ============================================================
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(width / 2, height - 28, "!! SHREE GANESHAY NAMH !!")

    # ============================================================
    # HEADER (COMPACT)
    # ============================================================
    header_top = height - 35
    header_h = 80
    c.rect(15, header_top - header_h, width - 30, header_h)

    # Logo
    try:
        logo = Image.open(LOGO_PATH).convert("RGB")
        logo.thumbnail((110, 75))
        c.drawImage(ImageReader(logo), 22, header_top - 76, width=90, preserveAspectRatio=True)
    except:
        c.drawString(22, header_top - 50, "[LOGO ERROR]")

    # Company Info
    c.setFont("Helvetica-Bold", 16)
    c.drawString(130, header_top - 20, "SHIVAY TEXTILES")

    c.setFont("Helvetica", 8)
    c.drawString(130, header_top - 33, "Plot No. 2, Balaji Park, Sachin-Talangpor Road, Talangpor")
    c.drawString(130, header_top - 45, "Surat, Gujarat - 394230")
    c.drawString(130, header_top - 57, "Phone: +91-9725101375")
    c.drawString(130, header_top - 69, "GSTIN: 24AFQFS2672R1Z1")

    # ============================================================
    # DETAILS BLOCKS (VERY COMPACT)
    # ============================================================
    detail_top = header_top - header_h - 6
    detail_h = 95
    half = (width - 30) / 2

    c.rect(15, detail_top - detail_h, half, detail_h)
    c.rect(15 + half, detail_top - detail_h, half, detail_h)

    lx = 22
    rx = lx + half

    # LEFT BLOCK
    c.setFont("Helvetica-Bold", 9)
    c.drawString(lx, detail_top - 15, "FIRM DETAILS")

    c.setFont("Helvetica", 8)
    c.drawString(lx, detail_top - 30, "GSTIN: 24AFQFS2672R1Z1")
    c.drawString(lx, detail_top - 54, "PAN No: AFQFS2672R ")
    c.drawString(lx, detail_top - 42, "State: Gujarat (24)")
    c.drawString(lx, detail_top - 66, "MSME: UDYAM-GJ-22-0512040")
    c.drawString(lx, detail_top - 78, "Transport: ")
    c.drawString(lx, detail_top - 90, "Broker: ")

    # RIGHT BLOCK
    c.setFont("Helvetica-Bold", 9)
    c.drawString(rx, detail_top - 15, "INVOICE DETAILS")

    c.setFont("Helvetica", 8)
    c.drawString(rx, detail_top - 30, f"Invoice No: {invoice_no}")
    c.drawString(rx, detail_top - 42, f"Date: {invoice_date}")
    c.drawString(rx, detail_top - 54, f"Challan No: ")
    c.drawString(rx, detail_top - 66, "Credit: 45 Days")
    c.drawString(rx, detail_top - 78, f"Due Date: {due_date}")
    c.drawString(rx, detail_top - 90, f"Place of Supply: {data['customer_name']}")

    # ============================================================
    # BUYER DETAILS BLOCK (COMPACT)
    # ============================================================
    buyer_top = detail_top - detail_h - 8
    buyer_h = 65
    c.rect(15, buyer_top - buyer_h, width - 30, buyer_h)

    c.setFont("Helvetica-Bold", 9)
    c.drawString(22, buyer_top - 14, "BUYER DETAILS")

    c.setFont("Helvetica", 8)
    c.drawString(22, buyer_top - 27, f"Name: {data['customer_name']}")
    c.drawString(22, buyer_top - 38, f"Address: {data['customer_address']}")
    c.drawString(22, buyer_top - 49, f"GSTIN: {data['customer_gst']}")

    # ============================================================
    # ITEM TABLE (COMPACT)
    # ============================================================
    table_y = buyer_top - buyer_h - 8

    c.setFont("Helvetica-Bold", 8.5)
    c.line(15, table_y, width - 15, table_y)
    table_y -= 10

    c.drawString(20, table_y, "Sr")
    c.drawString(60, table_y, "Description")
    c.drawString(240, table_y, "HSN")
    c.drawString(300, table_y, "Qty")
    c.drawString(360, table_y, "Rate")
    c.drawString(460, table_y, "Amount")

    table_y -= 8
    c.line(15, table_y, width - 15, table_y)
    table_y -= 8

    # Rows (supporting 14 items)
    c.setFont("Helvetica", 8)
    row_gap = 14  # IMPORTANT FOR 14 ITEMS

    for i, (desc, hsn, qty, rate, amt) in enumerate(items, start=1):
        c.drawString(20, table_y, str(i))
        c.drawString(60, table_y, desc)
        c.drawString(240, table_y, hsn)
        c.drawString(300, table_y, str(qty))
        c.drawString(360, table_y, f"{rate:.2f}")
        c.drawString(460, table_y, f"{amt:.2f}")
        table_y -= row_gap

    # Bottom rule
    c.line(15, table_y + 6, width - 15, table_y + 6)

   # ============================================================
    # SUMMARY (RIGHT SIDE)
    # ============================================================
    summary_h = 110
    summary_w = 210
    summary_x = width - summary_w - 15

    # Push summary downward (Option C)
    MIN_GAP = 14
    summary_y = table_y - MIN_GAP
    if summary_y > 220:
        summary_y = 220

    # Draw summary box
    c.rect(summary_x, summary_y, summary_w, summary_h)

    c.setFillColorRGB(0.90, 0.90, 0.90)
    c.rect(summary_x, summary_y + summary_h - 18, summary_w, 18, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)

    c.setFont("Helvetica-Bold", 9)
    c.drawString(summary_x + 8, summary_y + summary_h - 12, "SUMMARY")

    c.setFont("Helvetica", 8)
    sy = summary_y + summary_h - 30
    sg = 14

    c.drawString(summary_x + 8, sy, "Taxable:")
    c.drawRightString(summary_x + summary_w - 10, sy, f"{data['taxable']:.2f}")

    c.drawString(summary_x + 8, sy - sg, "CGST 2.5%:")
    c.drawRightString(summary_x + summary_w - 10, sy - sg, f"{data['cgst']:.2f}")

    c.drawString(summary_x + 8, sy - sg*2, "SGST 2.5%:")
    c.drawRightString(summary_x + summary_w - 10, sy - sg*2, f"{data['sgst']:.2f}")

    c.drawString(summary_x + 8, sy - sg*3, "IGST 5%:")
    c.drawRightString(summary_x + summary_w - 10, sy - sg*3, f"{data['igst']:.2f}")

    c.setFont("Helvetica-Bold", 9)
    c.drawString(summary_x + 8, sy - sg*4, "Total:")
    c.drawRightString(summary_x + summary_w - 10, sy - sg*4, f"{data['total']:.2f}")


    # ============================================================
    # BANK DETAILS (LEFT SIDE, SAME HEIGHT AS SUMMARY)
    # ============================================================
    bank_h = summary_h
    bank_w = 260
    bank_x = 15
    bank_y = summary_y  # <<< CRITICAL FIX

    c.rect(bank_x, bank_y, bank_w, bank_h)

    c.setFillColorRGB(0.90, 0.90, 0.90)
    c.rect(bank_x, bank_y + bank_h - 18, bank_w, 18, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)

    c.setFont("Helvetica-Bold", 9)
    c.drawString(bank_x + 8, bank_y + bank_h - 12, "BANK DETAILS")

    c.setFont("Helvetica", 8)
    by = bank_y + bank_h - 32
    bg = 14

    c.drawString(bank_x + 12, by, "Bank: THE VARACHHA CO-OP BANK LTD")
    c.drawString(bank_x + 12, by - bg, "A/C No: 00830110040586")
    c.drawString(bank_x + 12, by - bg*2, "IFSC: VARA0289008")
    c.drawString(bank_x + 12, by - bg*3, "Branch: SACHIN GIDC")


    # ============================================================
    # AMOUNT IN WORDS — BELOW BOTH BOXES (NO OVERLAP)
    # ============================================================
    words_y = summary_y - 25  # <<< FIXED POSITION BELOW SUMMARY & BANK

    words = num_to_indian_words(int(data["total"]))

    c.setFont("Helvetica-Bold", 9)
    c.drawString(15, words_y, "Amount in Words:")

    c.setFont("Helvetica", 8)
    c.drawString(120, words_y, f"{words} Only")

    # ============================================================
    # FOOTER
    # ============================================================
    c.setFont("Helvetica-Bold", 9)
    c.drawString(15, 80, "Terms & Conditions:")

    c.setFont("Helvetica", 7)
    c.drawString(15, 65, "[1] Goods are dispatched at buyer's risk & responsibility.")
    c.drawString(15, 54, "[2] Complaints must be made within 24 hours.")
    c.drawString(15, 43, "[3] Goods once sold cannot be returned.")
    c.drawString(15, 32, "[4] Payment only by A/c Payee Cheque.")
    c.drawString(15, 21, "[5] Interest @ 2% per month on delayed payments.")
    c.drawString(15, 10, "[6] No dyeing guarantee.")

    # ============================================================
    # SIGNATURE SECTION (Receiver BETWEEN TERMS & AUTHORISED)
    # ============================================================

    sign_y = 70   # common baseline for signatures

    # Receiver's Signature (CENTER)
    receiver_x = width / 2 - 70
    c.setFont("Helvetica-Bold", 9)
    c.drawString(receiver_x, sign_y, "Receiver's Signature")
    c.line(receiver_x, sign_y - 20, receiver_x + 140, sign_y - 20)

    # Authorised Signature (RIGHT)
    auth_x = width - 180
    c.setFont("Helvetica-Bold", 9)
    c.drawString(auth_x, sign_y, "For SHIVAY TEXTILES")
    c.drawString(auth_x, sign_y - 35, "Authorised Signatory")
    c.line(auth_x, sign_y - 20, auth_x + 130, sign_y - 20)



    # ============================================================
    # SAVE
    # ============================================================
    c.save()
    return filename
