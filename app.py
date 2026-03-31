from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "10fix_secret_2026"

EXCEL_FILE = "customers.xlsx"
ADMIN_PASSWORD = "10fix2026"

def init_excel():
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()
        ws = wb.active
        ws.title = "לקוחות"
        ws.append(["תאריך", "שם מלא", "עיר", "טלפון", "אימייל", "אישור שיווק"])
        for cell in ws[1]:
            cell.font = cell.font.copy(bold=True)
        wb.save(EXCEL_FILE)

def get_customers():
    init_excel()
    wb = load_workbook(EXCEL_FILE)
    ws = wb.active
    customers = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[1]:  # יש שם
            customers.append({
                "date": row[0] or "",
                "name": row[1] or "",
                "city": row[2] or "",
                "phone": row[3] or "",
                "email": row[4] or "",
                "consent": row[5] or ""
            })
    customers.sort(key=lambda x: x["name"])
    return customers

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
        full_name, city, phone, email, consent
    ])
    wb.save(EXCEL_FILE)

    print(f"[+] לקוח חדש: {full_name} | {city} | {phone}")
    return jsonify({"status": "ok"})

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        return render_template("admin_login.html", error="סיסמה שגויה")

    if not session.get("admin"):
        return render_template("admin_login.html", error=None)

    customers = get_customers()
    return render_template("admin.html", customers=customers, total=len(customers))

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin"))

if __name__ == "__main__":
    init_excel()
    print("=" * 40)
    print("10FIX מועדון לקוחות - שרת פעיל")
    print("כתובת: http://localhost:5000")
    print("=" * 40)
    app.run(host="0.0.0.0", port=5000, debug=False)
