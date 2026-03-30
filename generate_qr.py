import qrcode
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

ip  = get_local_ip()
url = f"http://{ip}:5000"

qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_10fix.png")

print(f"QR נוצר! הכתובת: {url}")
print("הקובץ נשמר: qr_10fix.png")
