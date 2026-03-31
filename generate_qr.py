import qrcode

BASE_URL = "https://one0fix-club.onrender.com"

# QR 1 - רישום למועדון (קיים)
qr1 = qrcode.QRCode(box_size=10, border=4)
qr1.add_data(BASE_URL)
qr1.make(fit=True)
img1 = qr1.make_image(fill_color="black", back_color="white")
img1.save("qr_10fix.png")
print(f"QR רישום נוצר: {BASE_URL}")
print("נשמר: qr_10fix.png")

# QR 2 - כניסה לעסק (חדש)
checkin_url = f"{BASE_URL}/checkin"
qr2 = qrcode.QRCode(box_size=10, border=4)
qr2.add_data(checkin_url)
qr2.make(fit=True)
img2 = qr2.make_image(fill_color="black", back_color="white")
img2.save("qr_checkin.png")
print(f"QR כניסה נוצר: {checkin_url}")
print("נשמר: qr_checkin.png")
