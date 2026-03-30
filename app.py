from flask import Flask, request, jsonify, render_template
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os

app = Flask(__name__)

EXCEL_FILE = "customers.xlsx"

def init_excel():
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()
        ws = wb.active
        ws.title = "לקוחות"
        ws.append(["תאריך", "שם מלא", "עיר", "טלפון", "אימייל", "אישור שיווק"])
        # עיצוב כותרות
        for cell in ws[1]:
            cell.font = cell.font.copy(bold=True)
        wb.save(EXCEL_FILE)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    if not data:
        return jsonify({"error": "no data"}), 400

    full_name = data.get("full_name", "").strip()
    city      = data.get("city", "").strip()
    phone     = data.get("phone", "").strip()
    email     = data.get("email", "").strip()
    consent   = "כן" if data.get("marketing_consent") else "לא"

    if not full_name or not city or not phone:
        return jsonify({"error": "missing fields"}), 400

    init_excel()

    wb = load_workbook(EXCEL_FILE)
    ws = wb.active
    ws.append([
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        full_name,
        city,
        phone,
        email,
        consent
    ])
    wb.save(EXCEL_FILE)

    print(f"[+] לקוח חדש: {full_name} | {city} | {phone}")
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    init_excel()
    print("=" * 40)
    print("10FIX מועדון לקוחות - שרת פעיל")
    print("כתובת: http://localhost:5000")
    print("=" * 40)
    app.run(host="0.0.0.0", port=5000, debug=False)
