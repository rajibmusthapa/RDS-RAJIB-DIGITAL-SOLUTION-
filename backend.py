#!/usr/bin/env python3
"""
RDS ULTIMATE - Backend Server
Complete Business Solution for Rajib Digital Solution
"""

import json
import os
import hashlib
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime

# ============ KONFIGURASI ============
DATA_DIR = "data"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

# Konfigurasi WhatsApp (UltraMsg)
INSTANCE_ID = "instance175828"
TOKEN_ULTRAMSG = "r1gpq44ppe4ltp0n"
ADMIN_PHONE = "6281316885825"

# ============ Kupon Diskon ============
COUPONS = {
    "RDS10": {"discount": 10, "type": "percent", "desc": "Diskon 10%"},
    "RDS50": {"discount": 50000, "type": "fixed", "desc": "Potongan Rp50.000"},
    "WELCOME": {"discount": 15, "type": "percent", "desc": "Diskon 15% untuk member baru"}
}

# ============ Produk ============
PRODUCTS = {
    "1": {"id": "1", "name": "🏢 Company Profile Website", "price": 12000000, "description": "Website profesional 5 halaman + CMS", "category": "Website"},
    "2": {"id": "2", "name": "🛒 E-commerce Website", "price": 28000000, "description": "Toko online lengkap + payment gateway", "category": "Website"},
    "3": {"id": "3", "name": "🏪 Marketplace Platform", "price": 55000000, "description": "Multi-vendor marketplace", "category": "Website"},
    "4": {"id": "4", "name": "🔒 Cyber Security", "price": 5000000, "description": "Audit keamanan website + laporan", "category": "Security"},
    "5": {"id": "5", "name": "📱 Digital Marketing", "price": 7500000, "description": "SEO + Social Media + Ads", "category": "Marketing"},
    "6": {"id": "6", "name": "🔧 Website Maintenance", "price": 1000000, "description": "Per bulan: backup, update, monitoring", "category": "Service"}
}

# ============ Helper Functions ============
def load_data(filename):
    try:
        with open(f"{DATA_DIR}/{filename}", "r") as f:
            return json.load(f)
    except:
        return []

def save_data(filename, data):
    with open(f"{DATA_DIR}/{filename}", "w") as f:
        json.dump(data, f, indent=2)

def send_wa_notification(name, service, order_id=None):
    """Kirim WhatsApp notification via UltraMsg"""
    try:
        if order_id:
            message = f"🛒 ORDER BARU!\n\nNama: {name}\nLayanan: {service}\nOrder ID: {order_id}\n\nCek dashboard segera!"
        else:
            message = f"📅 BOOKING BARU!\n\nNama: {name}\nLayanan: {service}\n\nCek dashboard segera!"
        
        post_data = {"token": TOKEN_ULTRAMSG, "to": ADMIN_PHONE, "body": message}
        url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
        req = urllib.request.Request(url, data=json.dumps(post_data).encode(), method='POST')
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req, timeout=10)
        result = json.loads(response.read().decode())
        print(f"✅ WA sent: {result}")
        return True
    except Exception as e:
        print(f"⚠️ WA failed: {e}")
        with open(f"{DATA_DIR}/notifications.log", "a") as f:
            f.write(f"{datetime.now()}: Gagal WA - {message[:100]}...\n")
        return False

# ============ Inisialisasi Data ============
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

default_orders = [
    {"id": 1, "order_id": "RDS-20260516-1", "customer": {"name": "Muhammad RAJIB", "email": "rajibdigitalsolution@gmail.com", "phone": "081316885825"}, "items": [{"name": "E-commerce Website", "quantity": 1, "price": 28000000}], "total": 28000000, "status": "paid", "created_at": "2026-05-16"},
    {"id": 2, "order_id": "RDS-20260516-2", "customer": {"name": "Muhammad RAJIB", "email": "rajibdigitalsolution@gmail.com", "phone": "081316885825"}, "items": [{"name": "E-commerce Website", "quantity": 1, "price": 28000000}], "total": 28000000, "status": "paid", "created_at": "2026-05-16"},
    {"id": 3, "order_id": "RDS-20260516-3", "customer": {"name": "Muhammad RAJIB", "email": "rajibdigitalsolution@gmail.com", "phone": "081316885825"}, "items": [{"name": "Marketplace Platform", "quantity": 1, "price": 55000000}], "total": 55000000, "status": "paid", "created_at": "2026-05-16"},
    {"id": 4, "order_id": "RDS-20260516-4", "customer": {"name": "Muhammad RAJIB", "email": "rajibdigitalsolution@gmail.com", "phone": "081316885825"}, "items": [{"name": "Company Profile", "quantity": 1, "price": 12000000}], "total": 12000000, "status": "paid", "created_at": "2026-05-16"}
]

for f, default in [("orders.json", default_orders), ("bookings.json", []), ("messages.json", []), ("blog.json", []), ("portfolio.json", []), ("testimonials.json", []), ("chats.json", []), ("ratings.json", [])]:
    if not os.path.exists(f"{DATA_DIR}/{f}"):
        save_data(f, default)

# ============ HTTP Handler ============
class RDSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/api/orders":
            self.send_json(load_data("orders.json"))
        elif parsed.path == "/api/bookings":
            self.send_json(load_data("bookings.json"))
        elif parsed.path == "/api/messages":
            self.send_json(load_data("messages.json"))
        elif parsed.path == "/api/blog":
            self.send_json(load_data("blog.json"))
        elif parsed.path == "/api/portfolio":
            self.send_json(load_data("portfolio.json"))
        elif parsed.path == "/api/products":
            self.send_json(PRODUCTS)
        elif parsed.path == "/api/coupons":
            self.send_json(COUPONS)
        elif parsed.path == "/api/chats":
            self.send_json(load_data("chats.json"))
        elif parsed.path == "/api/ratings":
            self.send_json(load_data("ratings.json"))
        elif parsed.path == "/api/testimonials":
            self.send_json(load_data("testimonials.json"))
        elif parsed.path == "/api/stats":
            bookings = load_data("bookings.json")
            orders = load_data("orders.json")
            stats = {
                "total_bookings": len(bookings),
                "total_orders": len(orders),
                "total_revenue": sum(o.get('total', 0) for o in orders if o.get('status') == 'paid')
            }
            self.send_json(stats)
        elif parsed.path == "/api/export/csv":
            bookings = load_data("bookings.json")
            csv_data = "Nama,Email,Phone,Service,Tanggal,Status,Created At\n"
            for b in bookings:
                csv_data += f"{b.get('name','')},{b.get('email','')},{b.get('phone','')},{b.get('service','')},{b.get('date','')},{b.get('status','')},{b.get('created_at','')}\n"
            self.send_response(200)
            self.send_header("Content-type", "text/csv")
            self.send_header("Content-Disposition", "attachment; filename=bookings.csv")
            self.end_headers()
            self.wfile.write(csv_data.encode())
        else:
            if self.path == "/":
                self.path = "/index.html"
            try:
                with open("." + self.path, "rb") as f:
                    self.send_response(200)
                    if self.path.endswith(".css"):
                        self.send_header("Content-type", "text/css")
                    elif self.path.endswith(".js"):
                        self.send_header("Content-type", "application/javascript")
                    else:
                        self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        parsed = urlparse(self.path)

        if parsed.path == "/api/bookings":
            bookings = load_data("bookings.json")
            # Hapus field captcha jika ada
            if 'captcha' in data:
                del data['captcha']
            if 'g-recaptcha-response' in data:
                del data['g-recaptcha-response']
            
            data['id'] = len(bookings) + 1
            data['created_at'] = datetime.now().isoformat()
            data['status'] = 'pending'
            bookings.append(data)
            save_data("bookings.json", bookings)
            send_wa_notification(data.get('name'), data.get('service'))
            self.send_json({"status": "success", "message": "✅ Booking terkirim! Admin akan segera menghubungi Anda."})

        elif parsed.path == "/api/contact":
            messages = load_data("messages.json")
            data['id'] = len(messages) + 1
            data['created_at'] = datetime.now().isoformat()
            messages.append(data)
            save_data("messages.json", messages)
            self.send_json({"status": "success", "message": "✅ Pesan terkirim!"})

        elif parsed.path == "/api/checkout":
            orders = load_data("orders.json")
            order_id = f"RDS-{datetime.now().strftime('%Y%m%d')}-{len(orders)+1}"
            new_order = {
                'id': len(orders) + 1,
                'order_id': order_id,
                'customer': data.get('customer'),
                'items': data.get('items'),
                'total': data.get('total'),
                'status': 'pending',
                'created_at': datetime.now().isoformat()
            }
            orders.append(new_order)
            save_data("orders.json", orders)
            customer = data.get('customer', {})
            items = data.get('items', [])
            service = items[0].get('name', 'Jasa RDS') if items else 'Jasa RDS'
            send_wa_notification(customer.get('name'), service, order_id)
            self.send_json({"status": "success", "order_id": order_id, "amount": new_order['total']})

        elif parsed.path == "/api/validate-coupon":
            code = data.get('code', '').upper()
            if code in COUPONS:
                self.send_json({"valid": True, "coupon": COUPONS[code]})
            else:
                self.send_json({"valid": False})

        elif parsed.path == "/api/chats":
            chats = load_data("chats.json")
            data['time'] = datetime.now().isoformat()
            chats.append(data)
            save_data("chats.json", chats)
            self.send_json({"status": "success"})

        elif parsed.path == "/api/rating":
            ratings = load_data("ratings.json")
            data['id'] = len(ratings) + 1
            data['created_at'] = datetime.now().isoformat()
            ratings.append(data)
            save_data("ratings.json", ratings)
            self.send_json({"status": "success"})

        elif parsed.path == "/api/testimonials":
            testimonials = load_data("testimonials.json")
            data['id'] = len(testimonials) + 1
            data['created_at'] = datetime.now().isoformat()
            testimonials.append(data)
            save_data("testimonials.json", testimonials)
            self.send_json({"status": "success"})

        elif parsed.path == "/api/update-booking":
            booking_id = data.get('id')
            new_status = data.get('status')
            bookings = load_data("bookings.json")
            for b in bookings:
                if b.get('id') == booking_id:
                    b['status'] = new_status
                    break
            save_data("bookings.json", bookings)
            self.send_json({"status": "success"})

        elif parsed.path == "/api/update-order":
            order_id = data.get('id')
            new_status = data.get('status')
            orders = load_data("orders.json")
            for o in orders:
                if o.get('id') == order_id:
                    o['status'] = new_status
                    break
            save_data("orders.json", orders)
            self.send_json({"status": "success"})

        elif parsed.path == "/api/delete-booking":
            booking_id = data.get('id')
            bookings = load_data("bookings.json")
            bookings = [b for b in bookings if b.get('id') != booking_id]
            save_data("bookings.json", bookings)
            self.send_json({"status": "success"})

        elif parsed.path == "/api/delete-order":
            order_id = data.get('id')
            orders = load_data("orders.json")
            orders = [o for o in orders if o.get('id') != order_id]
            save_data("orders.json", orders)
            self.send_json({"status": "success"})

        elif parsed.path == "/api/login":
            password = data.get('password')
            if hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
                token = hashlib.sha256(f"{datetime.now()}{password}".encode()).hexdigest()
                self.send_json({"status": "success", "token": token})
            else:
                self.send_json({"status": "error", "message": "Password salah"}, 401)

        elif parsed.path == "/api/blog":
            action = data.get('action')
            blog_posts = load_data("blog.json")
            if action == 'create':
                new_post = {
                    'id': len(blog_posts) + 1,
                    'title': data.get('title'),
                    'content': data.get('content'),
                    'date': datetime.now().isoformat(),
                    'author': data.get('author', 'Admin')
                }
                blog_posts.append(new_post)
                save_data("blog.json", blog_posts)
                self.send_json({"status": "success"})
            elif action == 'delete':
                post_id = data.get('id')
                blog_posts = [p for p in blog_posts if p.get('id') != post_id]
                save_data("blog.json", blog_posts)
                self.send_json({"status": "success"})

        elif parsed.path == "/api/portfolio":
            action = data.get('action')
            portfolios = load_data("portfolio.json")
            if action == 'create':
                new_item = {
                    'id': len(portfolios) + 1,
                    'title': data.get('title'),
                    'category': data.get('category'),
                    'client': data.get('client'),
                    'description': data.get('description', '')
                }
                portfolios.append(new_item)
                save_data("portfolio.json", portfolios)
                self.send_json({"status": "success"})
            elif action == 'delete':
                item_id = data.get('id')
                portfolios = [p for p in portfolios if p.get('id') != item_id]
                save_data("portfolio.json", portfolios)
                self.send_json({"status": "success"})

        else:
            self.send_json({"status": "error", "message": "Endpoint not found"}, 404)

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == "__main__":
    port = 8080
    print(f"🚀 RDS ULTIMATE - Server Berjalan!")
    print(f"📱 WhatsApp: {ADMIN_PHONE}")
    print(f"🔐 Password Admin: admin123")
    print(f"📊 Dashboard: http://localhost:{port}/admin/dashboard.html")
    print(f"🛒 Toko: http://localhost:{port}/shop.html")
    print(f"💬 Live Chat: http://localhost:{port}/chat.html")
    HTTPServer(("0.0.0.0", port), RDSHandler).serve_forever()
