from flask import Flask, request, redirect, render_template_string, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-later"
DB_NAME = "restaurant.db"



MENU = {
    "Phở Bò": {
        "price": 88,
        "desc": "Rich beef broth, rice noodles, herbs",
        "image": "/static/photos/pho_bo.jpg"
    },
    "Bánh Mì": {
        "price": 45,
        "desc": "Crispy baguette with grilled meat and pickles",
        "image": "/static/photos/banh_mi.jpeg"
    },
    "Bún Thịt Nướng": {
        "price": 78,
        "desc": "Grilled pork, vermicelli, fresh vegetables",
        "image": "/static/photos/bun_thit_nuong.jpeg"
    },
    "Gỏi Cuốn": {
        "price": 42,
        "desc": "Fresh rice paper rolls with herbs",
        "image": "/static/photos/goi_cuon.jpg"
    },
    "Cà Phê Sữa Đá": {
        "price": 32,
        "desc": "Vietnamese iced coffee with condensed milk",
        "image": "/static/photos/ca_phe_sua_da.jpeg"
    },
    "Trà Đá": {
        "price": 12,
        "desc": "Vietnamese iced tea",
        "image": "/static/photos/tra_da.jpeg"
    }
}

STYLE = """
<style>
body {
    font-family: Arial, sans-serif;
    background: #faf5ef;
    color: #2b1d0e;
    margin: 0;
}

/* Shared layout */
.container {
    max-width: 1200px;
    margin: 30px auto;
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.hero {
    text-align: center;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 10px;
    color: #b45309;
}

.subtitle {
    text-align: center;
    color: #666;
}

.card {
    border: 1px solid #f3d7b6;
    padding: 20px;
    border-radius: 16px;
    background: #fffaf3;
    margin-bottom: 15px;
}

/* Customer ordering page */
.mobile-page {
    width: min(100%, 1600px);
    margin: 0 auto;
    background: #fffaf3;
    min-height: 100vh;
    padding-bottom: 120px;
}

.top-hero {
    background: linear-gradient(135deg, #b45309, #dc2626);
    color: white;
    padding: 28px 20px;
    border-radius: 0 0 28px 28px;
    text-align: center;
}

.top-hero h1 {
    margin: 0;
    font-size: clamp(28px, 5vw, 48px);
}

.top-hero p {
    margin-top: 8px;
    opacity: 0.9;
}

.table-card {
    background: white;
    margin: 18px;
    padding: 16px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    text-align: center;
}

.table-card p {
    margin: 0;
    color: #777;
}

.table-card h2 {
    margin: 6px 0 0;
    color: #b45309;
}

.category-row {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    padding: 0 18px 16px;
}

.category-row span {
    background: white;
    padding: 10px 14px;
    border-radius: 999px;
    font-weight: bold;
    color: #b45309;
    white-space: nowrap;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}

.mobile-page {
    width: min(100%, 1600px);
    margin: 0 auto;
    background: #fffaf3;
    min-height: 100vh;
    padding-bottom: 120px;
}

.menu-grid {
    display: grid;
    gap: 16px;
    padding: 0 18px;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

.menu-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);

  
}

.menu-img {
    width: 100%;
    height: clamp(140px, 28vw, 220px);
    object-fit: cover;
}

.menu-info {
    padding: 14px 16px 6px;
}

.menu-info h3 {
    margin: 0;
    color: #b45309;
    font-size: 22px;
}

.menu-info p {
    color: #666;
    margin: 8px 0;
}

.menu-info strong {
    font-size: 20px;
}

.menu-qty {
    padding: 0 16px 16px;
}

.add-btn {
    display: inline-block;
    background: #2f6f3e;
    color: white;
    padding: 12px 18px;
    border-radius: 12px;
    text-decoration: none;
    font-weight: bold;
}

/* Cart page */
.cart-panel {
    padding: 18px;
}

.cart-header-card {
    background: white;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

.cart-header-card h3 {
    margin: 0 0 6px;
    color: #2f6f3e;
}

.cart-header-card p {
    margin: 0;
    color: #666;
}

.cart-item {
    background: white;
    border-radius: 18px;
    padding: 12px;
    margin-bottom: 14px;
    display: grid;
    grid-template-columns: 110px 1fr auto;
    gap: 14px;
    align-items: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

.cart-img {
    width: 110px;
    height: 90px;
    object-fit: cover;
    border-radius: 14px;
}

.cart-info h3 {
    margin: 0;
    color: #2b1d0e;
    font-size: 20px;
}

.cart-info p {
    margin: 6px 0;
    color: #666;
}

.cart-info strong {
    color: #2f6f3e;
    font-size: 20px;
}

.qty-box {
    display: flex;
    align-items: center;
    gap: 10px;
}

.qty-btn {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #f7f1e8;
    color: #2f6f3e;
    display: grid;
    place-items: center;
    text-decoration: none;
    font-size: 22px;
    font-weight: bold;
}

.qty-number {
    font-size: 20px;
    font-weight: bold;
}

.cart-summary {
    background: white;
    border-radius: 18px;
    padding: 16px;
    margin-top: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

.summary-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    color: #555;
}

.summary-total {
    display: flex;
    justify-content: space-between;
    font-size: 24px;
    font-weight: bold;
    color: #2f6f3e;
}

.note-box {
    width: 100%;
    min-height: 90px;
    border: 1px solid #ead8c0;
    border-radius: 16px;
    padding: 14px;
    font-size: 16px;
    box-sizing: border-box;
    resize: vertical;
    margin-top: 16px;
}

.cart-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 16px;
}

.secondary-btn {
    background: white;
    color: #2f6f3e;
    border: 2px solid #2f6f3e;
    text-align: center;
    padding: 14px;
    border-radius: 14px;
    text-decoration: none;
    font-weight: bold;
}

.place-btn {
    background: #2f6f3e;
    color: white;
    border: none;
    padding: 14px;
    border-radius: 14px;
    font-weight: bold;
    font-size: 16px;
}

/* Kitchen dashboard */
.kitchen-page {
    width: min(100% - 32px, 1500px);
    margin: 24px auto;
}

.kitchen-topbar {
    background: white;
    border-radius: 18px;
    padding: 20px 24px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

.kitchen-topbar h1 {
    margin: 0;
    color: #12351f;
}

.kitchen-topbar p {
    margin: 6px 0 0;
    color: #666;
}

.live-pill {
    background: #eef8ee;
    color: #2f6f3e;
    padding: 10px 14px;
    border-radius: 999px;
    font-weight: bold;
}

.kitchen-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 18px;
}

.stat-card {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

.stat-card p {
    margin: 0;
    color: #666;
}

.stat-card h2 {
    margin: 8px 0 0;
    font-size: 34px;
    color: #2f6f3e;
}

.kitchen-board {
    display: grid;
    grid-template-columns: repeat(3, minmax(280px, 1fr));
    gap: 18px;
}

.kitchen-column {
    background: #fffaf3;
    border: 1px solid #ead8c0;
    border-radius: 20px;
    padding: 14px;
    min-height: 500px;
}

.column-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}

.column-title h2 {
    margin: 0;
    color: #12351f;
}

.column-title span {
    background: #2f6f3e;
    color: white;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: bold;
}

.kitchen-order-card {
    background: white;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

.order-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.order-top h3 {
    margin: 0;
    color: #2f6f3e;
    font-size: 24px;
}

.table-pill {
    background: #f7f1e8;
    padding: 6px 10px;
    border-radius: 999px;
    font-weight: bold;
}

.order-time {
    color: #777;
    font-size: 14px;
    margin-bottom: 10px;
}

.kitchen-items {
    padding-left: 18px;
    margin: 10px 0;
}

.kitchen-items li {
    margin-bottom: 6px;
}

.order-note {
    background: #f7f1e8;
    border-radius: 12px;
    padding: 10px;
    color: #2b1d0e;
    margin: 12px 0;
}

.kitchen-action {
    width: 100%;
    border-radius: 12px;
    margin-top: 10px;
}

.accept-btn {
    background: #2f6f3e;
}

.start-btn {
    background: #f97316;
}

.ready-btn {
    background: #2f6f3e;
}

.served-btn {
    background: #12351f;
}

.empty-column {
    background: white;
    border-radius: 16px;
    padding: 20px;
    color: #777;
    text-align: center;
}

/* Sales dashboard */
.sales-page {
    width: min(100% - 32px, 1500px);
    margin: 24px auto;
}

.sales-topbar {
    background: white;
    border-radius: 18px;
    padding: 20px 24px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

.sales-topbar h1 {
    margin: 0;
    color: #12351f;
}

.sales-topbar p {
    margin: 6px 0 0;
    color: #666;
}

.sales-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 18px;
}

.sales-card {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

.sales-card p {
    margin: 0;
    color: #666;
}

.sales-card h2 {
    margin: 8px 0 0;
    font-size: 34px;
    color: #2f6f3e;
}

.sales-main {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 18px;
}

.sales-section {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
    margin-bottom: 18px;
}

.sales-section h2 {
    margin-top: 0;
    color: #12351f;
}

.top-item {
    margin-bottom: 16px;
}

.top-item-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    font-weight: bold;
}

.bar-bg {
    height: 12px;
    background: #f1eadf;
    border-radius: 999px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: #2f6f3e;
    border-radius: 999px;
}

.recent-order {
    border-bottom: 1px solid #eee0ce;
    padding: 12px 0;
}

.recent-order:last-child {
    border-bottom: none;
}

.recent-order-top {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
    color: #12351f;
}

.recent-order p {
    margin: 6px 0 0;
    color: #666;
}

.sales-table {
    width: 100%;
    border-collapse: collapse;
}

.sales-table th {
    background: #2f6f3e;
    color: white;
}

.sales-table td,
.sales-table th {
    padding: 12px;
    border: 1px solid #eee0ce;
    text-align: left;
}

.sales-table tr:nth-child(even) {
    background: #fffaf3;
}

/* Mini cart */
.mini-cart-bar {
    position: fixed;
    left: 50%;
    bottom: 18px;
    transform: translateX(-50%);
    width: calc(100% - 36px);
    max-width: 420px;
    background: white;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.20);
    padding: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 200;
}

.mini-cart-bar a {
    background: #2f6f3e;
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    text-decoration: none;
    font-weight: bold;
}

.mini-cart-bar span {
    color: #2f6f3e;
    font-weight: bold;
}

/* Order tracking page */
.order-page {
    width: min(100%, 900px);
    margin: 0 auto;
    background: #fffaf3;
    min-height: 100vh;
    padding-bottom: 40px;
}

.order-content {
    padding: 18px;
}

.order-success-card {
    background: white;
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
    margin-bottom: 22px;
}

.success-top {
    display: flex;
    gap: 16px;
    align-items: center;
    margin-bottom: 18px;
}

.success-icon {
    width: 58px;
    height: 58px;
    border-radius: 50%;
    background: #2f6f3e;
    color: white;
    display: grid;
    place-items: center;
    font-size: 30px;
    font-weight: bold;
}

.success-top h2 {
    margin: 0;
    color: #12351f;
}

.success-top p {
    margin: 6px 0 0;
    color: #666;
}

.order-meta {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    border-top: 1px solid #ead8c0;
    padding-top: 18px;
}

.meta-box {
    text-align: center;
}

.meta-box p {
    margin: 0;
    color: #666;
}

.meta-box strong {
    display: block;
    margin-top: 6px;
    color: #2f6f3e;
    font-size: 22px;
}

.order-progress {
    background: white;
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
    margin-bottom: 22px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}

.progress-step {
    text-align: center;
    color: #aaa;
}

.progress-circle {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: #f1eadf;
    display: grid;
    place-items: center;
    margin: 0 auto 10px;
    font-size: 24px;
}

.progress-step.active {
    color: #12351f;
}

.progress-step.active .progress-circle {
    background: #2f6f3e;
    color: white;
}

.progress-step strong {
    display: block;
}

.progress-step span {
    display: block;
    font-size: 14px;
    margin-top: 4px;
}

.order-summary-card {
    background: white;
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
    margin-bottom: 20px;
}

.order-summary-card h2 {
    margin-top: 0;
    color: #12351f;
}

.order-summary-item {
    display: grid;
    grid-template-columns: 75px 1fr auto;
    gap: 14px;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px dashed #ead8c0;
}

.order-summary-item:last-child {
    border-bottom: none;
}

.order-summary-img {
    width: 75px;
    height: 65px;
    object-fit: cover;
    border-radius: 12px;
}

.order-summary-info h3 {
    margin: 0;
    color: #2b1d0e;
}

.order-summary-info p {
    margin: 6px 0 0;
    color: #666;
}

.order-summary-price {
    text-align: right;
    font-weight: bold;
    color: #2f6f3e;
}

.order-total-box {
    margin-top: 16px;
    border-top: 1px solid #ead8c0;
    padding-top: 14px;
}

.order-note-card {
    background: #f7f1e8;
    border-radius: 16px;
    padding: 14px;
    margin-top: 14px;
}



/* Buttons and forms */
button {
    width: 100%;
    background: #c2410c;
    color: white;
    border: none;
    padding: 14px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    font-size: 16px;
}

button:hover {
    background: #9a3412;
}

.order-actions {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
}

.order-actions form {
    margin: 0;
    width: 100%;
}

.order-action-btn,
.order-actions .place-btn {
    height: 52px;
    width: 100%;
    box-sizing: border-box;
    padding: 0 14px;
    border-radius: 16px;
    font-size: 16px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
}

.order-action-btn {
    background: white;
    color: #2f6f3e;
    border: 2px solid #2f6f3e;
    text-decoration: none;
}

.order-actions .place-btn {
    background: #2f6f3e;
    color: white;
    border: 2px solid #2f6f3e;
}

input {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ddd;
    margin-top: 8px;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #f97316;
    color: white;
}

td, th {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: center;
}

tr:nth-child(even) {
    background: #fff7ed;
}

.nav {
    text-align: center;
    margin-top: 20px;
}

.nav a {
    color: #dc2626;
    font-weight: bold;
    text-decoration: none;
    margin: 0 10px;
}

.payment-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
}

.payment-grid.two {
    grid-template-columns: repeat(2, 1fr);
}

.payment-option {
    background: white;
    border: 2px solid #ead8c0;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    font-weight: bold;
    cursor: pointer;
}

.payment-option input {
    margin-bottom: 10px;
}

.payment-option:has(input:checked) {
    border-color: #2f6f3e;
    color: #2f6f3e;
    box-shadow: 0 4px 14px rgba(47,111,62,0.15);
}

@media (max-width: 768px) {
    .payment-grid {
        grid-template-columns: 1fr 1fr;
    }

    .payment-grid.two {
        grid-template-columns: 1fr;
    }
}

/* Mobile */
@media (max-width: 768px) {
    .container {
        margin: 0;
        border-radius: 0;
        padding: 18px;
        box-shadow: none;
        max-width: 100%;
    }

    .hero h1 {
        font-size: 30px;
    }

    .subtitle {
        font-size: 14px;
    }

    .mobile-page {
        max-width: 100%;
    }


    table {
        font-size: 13px;
    }
    .menu-grid {
        grid-template-columns: 1fr;
    }

    .cart-item {
        grid-template-columns: 95px 1fr;
    }

    .cart-img {
        width: 95px;
        height: 85px;
    }

    .qty-box {
        grid-column: 2;
        justify-content: flex-start;
    }

    .cart-actions {
        grid-template-columns: 1fr;
    }

    .sales-page {
        width: 100%;
        margin: 0;
    }

    .sales-topbar {
        border-radius: 0;
        flex-direction: column;
        text-align: center;
        gap: 12px;
    }

    .sales-main {
        grid-template-columns: 1fr;
    }

    .sales-section {
        border-radius: 0;
    }

    .order-actions {
        grid-template-columns: 1fr;
    }

    .kitchen-page {
        width: 100%;
        margin: 0;
    }

    .kitchen-topbar {
        border-radius: 0;
        flex-direction: column;
        gap: 12px;
        text-align: center;
    }

    .kitchen-board {
        grid-template-columns: 1fr;
    }

    .kitchen-column {
        border-radius: 0;
    }
}



</style>
"""

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("PRAGMA table_info(orders)")
    columns = cursor.fetchall()

    column_names = []
    for column in columns:
        column_names.append(column[1])

    if "note" not in column_names:
        cursor.execute("ALTER TABLE orders ADD COLUMN note TEXT")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bill_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER NOT NULL,
            order_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            payment_location TEXT NOT NULL,
            note TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        UPDATE bill_requests
        SET status = 'Paid'
        WHERE status = 'Completed'
    """)

    conn.commit()
    conn.close()

def get_active_table_bill(table_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, status
        FROM bill_requests
        WHERE table_number = ?
          AND status IN ('New', 'Accepted', 'Paid')
        ORDER BY id DESC
        LIMIT 1
    """, (table_number,))

    active_bill = cursor.fetchone()

    conn.close()

    return active_bill

@app.route("/")
def admin():
    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{ style|safe }}
    <div class="container">
        <div class="hero">
            <h1>🍜 Phở Saigon Kitchen</h1>
            <p class="subtitle">Restaurant Admin Portal</p>
        </div>

        <div class="nav">
            <a href="/kitchen">Kitchen Dashboard</a>
            <a href="/sales">Sales Dashboard</a>
            <a href="/bills">Bill Requests</a>
        </div>
    </div>
    """
    return render_template_string(html, style=STYLE)


@app.route("/table/<int:table_number>")
def table_menu(table_number):

    current_table = session.get("table_number")

    if current_table != table_number:
        session["cart"] = {}
        session.pop("last_order_id", None)
        session["table_number"] = table_number

    cart = session.get("cart", {})

    last_order_id = session.get("last_order_id")

    active_bill = get_active_table_bill(table_number)

    cart_total = 0
    cart_count = 0

    for qty in cart.values():
        cart_count += qty

    for item, qty in cart.items():
        cart_total += MENU[item]["price"] * qty

    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{ style|safe }}

    <div class="mobile-page">
        <div class="top-hero">
            <h1>Phở Saigon Kitchen</h1>
            <p>Fresh Vietnamese food · Table {{ table_number }}</p>
        </div>

        <div class="table-card">
            <p>You are ordering at</p>
            <h2>Table {{ table_number }}</h2>
        </div>

        <div class="table-card">
            <a href="/table/{{ table_number }}" class="add-btn">
                Menu
            </a>

            <a href="/orders/{{ table_number }}" class="add-btn">
                Orders
            </a>
        </div>

        {% if last_order_id %}
        <div class="table-card">
            <p>You have an active/recent order</p>
            <h2>Order #{{ last_order_id }}</h2>
            <br>
            <a href="/order/{{ last_order_id }}" class="add-btn">
                View Current Order
            </a>
        </div>
        {% endif %}

       
        {% if active_bill %}
        <div class="table-card">
            <p>Ordering is locked</p>
            <h2>Bill status: {{ active_bill[1] }}</h2>
            <br>
            <a href="/bill_requested/{{ active_bill[0] }}" class="add-btn">
                View Bill Status
            </a>
        </div>
        {% endif %}


        <div class="category-row">
            <span>Phở</span>
            <span>Bánh Mì</span>
            <span>Bún</span>
            <span>Rolls</span>
            <span>Drinks</span>
        </div>

        <form action="/submit_order" method="POST">
            <input type="hidden" name="table_number" value="{{ table_number }}">

            <div class="menu-grid">

            {% for item, info in menu.items() %}
            <div class="menu-card">
                <img src="{{ info.image }}" class="menu-img">

                <div class="menu-info">
                    <h3>{{ item }}</h3>
                    <p>{{ info.desc }}</p>
                    <strong>${{ info.price }}</strong>
                </div>

                <div class="menu-qty">
                    {% if active_bill %}
                        <a href="/bill_requested/{{ active_bill[0] }}" class="add-btn">
                            View Bill Status
                        </a>
                    {% else %}
                        <a href="/add_to_cart/{{ item }}" class="add-btn">
                            + Add
                        </a>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
            </div>

            {% if cart_count > 0 %}
            <div class="mini-cart-bar">
                <div>
                    <strong>🛒 {{ cart_count }} items</strong>
                    <br>
                    <span>${{ cart_total }}</span>
                </div>

                <a href="/cart/{{ table_number }}">
                    View Cart
                </a>
            </div>
            {% endif %}
            
        </form>
    </div>
    """

    return render_template_string(
        html,
        table_number=table_number,
        menu=MENU,
        style=STYLE,
        cart=cart,
        cart_total=cart_total,
        cart_count=cart_count,
        last_order_id=last_order_id,
        active_bill=active_bill
    )

@app.route("/orders/<int:table_number>")
def customer_orders(table_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, table_number, status, created_at, note
        FROM orders
        WHERE table_number = ?
        ORDER BY id DESC
    """, (table_number,))

    orders = cursor.fetchall()

    order_list = []

    for order in orders:
        order_id = order[0]

        cursor.execute("""
            SELECT item, quantity, total_price
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))

        items = cursor.fetchall()

        cursor.execute("""
            SELECT id, status
            FROM bill_requests
            WHERE order_id = ?
              AND status IN ('New', 'Accepted', 'Paid')
            ORDER BY id DESC
            LIMIT 1
        """, (order_id,))

        bill = cursor.fetchone()

        total = 0
        item_count = 0

        for item in items:
            total += item[2]
            item_count += item[1]

        order_list.append({
            "id": order[0],
            "table_number": order[1],
            "status": order[2],
            "created_at": order[3],
            "note": order[4],
            "items": items,
            "total": total,
            "item_count": item_count,
            "bill": bill
        })

    conn.close()

    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{ style|safe }}

    <div class="order-page">
        <div class="top-hero">
            <h1>Your Orders</h1>
            <p>Table {{ table_number }}</p>
        </div>

        <div class="order-content">

            <div class="table-card">
                <a href="/table/{{ table_number }}" class="add-btn">
                    Menu
                </a>

                <a href="/orders/{{ table_number }}" class="add-btn">
                    Orders
                </a>
            </div>

            {% if orders|length == 0 %}
            <div class="order-success-card">
                <div class="success-top">
                    <div class="success-icon">🧾</div>

                    <div>
                        <h2>No orders yet</h2>
                        <p>Go to the menu and add food first.</p>
                    </div>
                </div>
            </div>
            {% endif %}

            {% for order in orders %}
            <div class="order-summary-card">
                <div class="recent-order-top">
                    <span>Order #{{ order.id }}</span>
                    <span>{{ order.status }}</span>
                </div>

                <p>Created: {{ order.created_at }}</p>

                {% for item in order["items"] %}
                <div class="summary-row">
                    <span>{{ item[1] }}x {{ item[0] }}</span>
                    <span>${{ item[2] }}</span>
                </div>
                {% endfor %}

                <div class="summary-total">
                    <span>Total</span>
                    <span>${{ order.total }}</span>
                </div>

                {% if order.bill %}
                <div class="order-note-card">
                    <strong>Bill status:</strong>
                    <p>{{ order.bill[1] }}</p>
                </div>
                {% endif %}

                <div class="order-actions">
                    <a href="/order/{{ order.id }}" class="order-action-btn">
                        View Order
                    </a>

                    {% if order.bill %}
                    <a href="/bill_requested/{{ order.bill[0] }}" class="place-btn">
                        View Bill
                    </a>
                    {% else %}
                    <a href="/request_bill/{{ order.id }}" class="place-btn">
                        Request Bill
                    </a>
                    {% endif %}
                </div>
            </div>
            {% endfor %}

        </div>
    </div>
    """

    return render_template_string(
        html,
        table_number=table_number,
        orders=order_list,
        style=STYLE
    )

@app.route("/cart/<int:table_number>")
def view_cart(table_number):
    cart = session.get("cart", {})

    last_order_id = session.get("last_order_id")

    cart_total = 0
    cart_count = 0

    for item, qty in cart.items():
        cart_total += MENU[item]["price"] * qty
        cart_count += qty

    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{ style|safe }}

    <div class="mobile-page">
        <div class="top-hero">
            <h1>Your Cart</h1>
            <p>Table {{ table_number }} · Dine-in order</p>
        </div>

        <div class="cart-panel">

            <div class="cart-header-card">
                <h3>Serving to Table {{ table_number }}</h3>
                <p>Please confirm your order before sending it to the kitchen.</p>
            </div>

            {% if cart|length == 0 %}
            <div class="cart-header-card">
                <h3>Your cart is empty</h3>
                <p>Add food from the menu first.</p>
            </div>
            {% endif %}

            {% for item, qty in cart.items() %}
            <div class="cart-item">
                <img src="{{ menu[item]['image'] }}" class="cart-img">

                <div class="cart-info">
                    <h3>{{ item }}</h3>
                    <p>{{ menu[item]["desc"] }}</p>
                    <strong>${{ menu[item]["price"] * qty }}</strong>

                </div>

                <div class="qty-box">
                    <a class="qty-btn" href="/remove_from_cart/{{ item }}">−</a>
                    <span class="qty-number">{{ qty }}</span>
                    <a class="qty-btn" href="/add_to_cart/{{ item }}">+</a>
                </div>
            </div>
            {% endfor %}

            <form action="/submit_order" method="POST">
                <input type="hidden" name="table_number" value="{{ table_number }}">

                <div class="cart-summary">
                    <div class="summary-row">
                        <span>Subtotal ({{ cart_count }} items)</span>
                        <span>${{ cart_total }}</span>
                    </div>

                    <div class="summary-total">
                        <span>Total</span>
                        <span>${{ cart_total }}</span>
                    </div>
                </div>

                <textarea
                    name="note"
                    class="note-box"
                    placeholder="Special requests? Example: no cilantro, less ice, extra chili..."
                    rows="4"
                ></textarea>

                <div class="cart-actions">
                    <a href="/table/{{ table_number }}" class="secondary-btn">
                        Continue Ordering
                    </a>

                    <button type="submit" class="place-btn">
                        Place Order
                    </button>
                </div>
            </form>

        </div>
    </div>
    """

    return render_template_string(
        html,
        table_number=table_number,
        menu=MENU,
        style=STYLE,
        cart=cart,
        cart_total=cart_total,
        cart_count=cart_count,
        last_order_id=last_order_id
    )


@app.route("/submit_order", methods=["POST"])
def submit_order():
    
    note = request.form.get("note", "")

    cart = session.get("cart", {})
    table_number = int(request.form["table_number"])
    created_at = datetime.now().isoformat()

    active_bill = get_active_table_bill(table_number)

    if active_bill:
        return redirect(f"/bill_requested/{active_bill[0]}")

    if len(cart) == 0:
        return redirect(f"/table/{table_number}")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO orders (table_number, status, created_at, note)
        VALUES (?, ?, ?, ?)
    """, (table_number, "New", created_at, note))

    order_id = cursor.lastrowid

    for item, quantity in cart.items():

        price = MENU[item]["price"]

        cursor.execute("""
            INSERT INTO order_items
            (order_id, item, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?)
        """, (
            order_id,
            item,
            quantity,
            price,
            price * quantity
        ))

    conn.commit()
    conn.close()

    session["cart"] = {}
    session["last_order_id"] = order_id

    return redirect(f"/order/{order_id}")


@app.route("/kitchen")
def kitchen():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, table_number, status, created_at, note
        FROM orders
        WHERE status != 'Served'
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    status_groups = {
        "New": [],
        "Preparing": [],
        "Ready": []
    }

    for order in orders:
        order_id = order[0]

        cursor.execute("""
            SELECT item, quantity
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))

        items = cursor.fetchall()

        order_data = {
            "id": order[0],
            "table_number": order[1],
            "status": order[2],
            "created_at": order[3],
            "note": order[4],
            "items": items
        }

        if order[2] in status_groups:
            status_groups[order[2]].append(order_data)



  
    conn.close()

    latest_order_id = orders[0][0] if orders else 0

    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{ style|safe }}

    <div class="kitchen-page">

        <div class="kitchen-topbar">
            <div>
                <h1>Kitchen Orders</h1>
                <p>Live order board · Auto-refreshing every 3 seconds</p>
            </div>

            <div class="live-pill">
                ● Live
            </div>
        </div>

        

        <div class="kitchen-stats">
            <div class="stat-card">
                <p>New Orders</p>
                <h2>{{ groups["New"]|length }}</h2>
            </div>

            <div class="stat-card">
                <p>Preparing</p>
                <h2>{{ groups["Preparing"]|length }}</h2>
            </div>

            <div class="stat-card">
                <p>Ready</p>
                <h2>{{ groups["Ready"]|length }}</h2>
            </div>
        </div>

        <div class="kitchen-board">

            <div class="kitchen-column">
                <div class="column-title">
                    <h2>New</h2>
                    <span>{{ groups["New"]|length }}</span>
                </div>

                {% for order in groups["New"] %}
                <div class="kitchen-order-card">
                    <div class="order-top">
                        <h3>#{{ order.id }}</h3>
                        <div class="table-pill">Table {{ order.table_number }}</div>
                    </div>

                    <div class="order-time">
                        {{ order.created_at }}
                    </div>

                    <ul class="kitchen-items">
                        {% for item in order["items"] %}
                        <li>{{ item[1] }}x {{ item[0] }}</li>
                        {% endfor %}
                    </ul>

                    {% if order.note %}
                    <div class="order-note">
                        <strong>Note:</strong> {{ order.note }}
                    </div>
                    {% endif %}

                    <form action="/update_status/{{ order.id }}/Preparing" method="POST">
                        <button class="kitchen-action accept-btn" type="submit">
                            Accept
                        </button>
                    </form>
                </div>
                {% else %}
                <div class="empty-column">No new orders</div>
                {% endfor %}
            </div>

            <div class="kitchen-column">
                <div class="column-title">
                    <h2>Preparing</h2>
                    <span>{{ groups["Preparing"]|length }}</span>
                </div>

                {% for order in groups["Preparing"] %}
                <div class="kitchen-order-card">
                    <div class="order-top">
                        <h3>#{{ order.id }}</h3>
                        <div class="table-pill">Table {{ order.table_number }}</div>
                    </div>

                    <div class="order-time">
                        {{ order.created_at }}
                    </div>

                    <ul class="kitchen-items">
                        {% for item in order["items"] %}
                        <li>{{ item[1] }}x {{ item[0] }}</li>
                        {% endfor %}
                    </ul>

                    {% if order.note %}
                    <div class="order-note">
                        <strong>Note:</strong> {{ order.note }}
                    </div>
                    {% endif %}

                    <form action="/update_status/{{ order.id }}/Ready" method="POST">
                        <button class="kitchen-action start-btn" type="submit">
                            Mark Ready
                        </button>
                    </form>
                </div>
                {% else %}
                <div class="empty-column">Nothing preparing</div>
                {% endfor %}
            </div>

            <div class="kitchen-column">
                <div class="column-title">
                    <h2>Ready</h2>
                    <span>{{ groups["Ready"]|length }}</span>
                </div>

                {% for order in groups["Ready"] %}
                <div class="kitchen-order-card">
                    <div class="order-top">
                        <h3>#{{ order.id }}</h3>
                        <div class="table-pill">Table {{ order.table_number }}</div>
                    </div>

                    <div class="order-time">
                        {{ order.created_at }}
                    </div>

                    <ul class="kitchen-items">
                        {% for item in order["items"] %}
                        <li>{{ item[1] }}x {{ item[0] }}</li>
                        {% endfor %}
                    </ul>

                    {% if order.note %}
                    <div class="order-note">
                        <strong>Note:</strong> {{ order.note }}
                    </div>
                    {% endif %}

                    <form action="/update_status/{{ order.id }}/Served" method="POST">
                        <button class="kitchen-action served-btn" type="submit">
                            Served
                        </button>
                    </form>
                </div>
                {% else %}
                <div class="empty-column">No ready orders</div>
                {% endfor %}
            </div>

        </div>

        <div class="nav">
            <a href="/">Admin</a>
            <a href="/sales">Sales Dashboard</a>
        </div>

    </div>

    <script>
        const latestOrderId = {{ latest_order_id }};
        const previousOrderId = localStorage.getItem("latestOrderId");

        if (previousOrderId !== null && Number(latestOrderId) > Number(previousOrderId)) {
            const audio = new Audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg");
            audio.play();
        }

        localStorage.setItem("latestOrderId", latestOrderId);

        setTimeout(function() {
            window.location.reload();
        }, 3000);
    </script>
    """

    return render_template_string(
        html,
        groups=status_groups,
        latest_order_id=latest_order_id,
        style=STYLE
    )


@app.route("/update_status/<int:order_id>/<new_status>", methods=["POST"])
def update_status(order_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?
    """, (new_status, order_id))

    conn.commit()
    conn.close()

    return redirect("/kitchen")


@app.route("/sales")
def sales():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(total_amount)
        FROM bill_requests
        WHERE status IN ('Paid', 'Closed')
    """)
    total_revenue = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT COUNT(DISTINCT order_id)
        FROM bill_requests
        WHERE status IN ('Paid', 'Closed')
    """)
    total_orders = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(order_items.quantity)
        FROM order_items
        JOIN bill_requests ON bill_requests.order_id = order_items.order_id
        WHERE bill_requests.status IN ('Paid', 'Closed')
    """)

    total_items_sold = cursor.fetchone()[0] or 0

    if total_orders > 0:
        average_order_value = round(total_revenue / total_orders, 2)
    else:
        average_order_value = 0

    cursor.execute("""
        SELECT 
            order_items.item,
            SUM(order_items.quantity) AS quantity_sold,
            SUM(order_items.total_price) AS revenue
        FROM order_items
        JOIN bill_requests ON bill_requests.order_id = order_items.order_id
        WHERE bill_requests.status IN ('Paid', 'Closed')
        GROUP BY order_items.item
        ORDER BY quantity_sold DESC
    """)
    item_sales_raw = cursor.fetchall()

    max_quantity = 1
    for item in item_sales_raw:
        if item[1] > max_quantity:
            max_quantity = item[1]

    item_sales = []
    for item in item_sales_raw:
        percent = round((item[1] / max_quantity) * 100)
        item_sales.append({
            "name": item[0],
            "quantity": item[1],
            "revenue": item[2],
            "percent": percent
        })

    cursor.execute("""
        SELECT 
            orders.id,
            orders.table_number,
            bill_requests.created_at,
            bill_requests.total_amount AS order_total,
            GROUP_CONCAT(order_items.quantity || 'x ' || order_items.item, ', ') AS items
        FROM bill_requests
        JOIN orders ON bill_requests.order_id = orders.id
        JOIN order_items ON order_items.order_id = orders.id
        WHERE bill_requests.status IN ('Paid', 'Closed')
        GROUP BY orders.id, orders.table_number, bill_requests.created_at, bill_requests.total_amount
        ORDER BY bill_requests.id DESC
        LIMIT 8
    """)
    recent_orders = cursor.fetchall()

    conn.close()

    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{ style|safe }}

    <div class="sales-page">

        <div class="sales-topbar">
            <div>
                <h1>Sales Dashboard</h1>
                <p>Paid bills only · Real restaurant revenue</p>
            </div>

            <div class="live-pill">
                ● Live
            </div>
        </div>

        <div class="sales-grid">
            <div class="sales-card">
                <p>Total Revenue</p>
                <h2>${{ total_revenue }}</h2>
            </div>

            <div class="sales-card">
                <p>Paid Orders</p>
                <h2>{{ total_orders }}</h2>
            </div>

            <div class="sales-card">
                <p>Average Order Value</p>
                <h2>${{ average_order_value }}</h2>
            </div>

            <div class="sales-card">
                <p>Items Sold</p>
                <h2>{{ total_items_sold }}</h2>
            </div>
        </div>

        <div class="sales-main">

            <div>
                <div class="sales-section">
                    <h2>Recent Paid Orders</h2>

                    {% if recent_orders|length == 0 %}
                        <p>No paid orders yet.</p>
                    {% endif %}

                    {% for order in recent_orders %}
                    <div class="recent-order">
                        <div class="recent-order-top">
                            <span>Order #{{ order[0] }} · Table {{ order[1] }}</span>
                            <span>${{ order[3] }}</span>
                        </div>
                        <p>{{ order[4] }}</p>
                        <p>{{ order[2] }}</p>
                    </div>
                    {% endfor %}
                </div>

                <div class="sales-section">
                    <h2>Sales by Item</h2>

                    <table class="sales-table">
                        <tr>
                            <th>Item</th>
                            <th>Quantity Sold</th>
                            <th>Revenue</th>
                        </tr>

                        {% for item in item_sales %}
                        <tr>
                            <td>{{ item.name }}</td>
                            <td>{{ item.quantity }}</td>
                            <td>${{ item.revenue }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>

            <div>
                <div class="sales-section">
                    <h2>Top Selling Items</h2>

                    {% if item_sales|length == 0 %}
                        <p>No item sales yet.</p>
                    {% endif %}

                    {% for item in item_sales[:6] %}
                    <div class="top-item">
                        <div class="top-item-row">
                            <span>{{ item.name }}</span>
                            <span>{{ item.quantity }} sold</span>
                        </div>

                        <div class="bar-bg">
                            <div class="bar-fill" style="width: {{ item.percent }}%;"></div>
                        </div>
                    </div>
                    {% endfor %}
                </div>

                <div class="sales-section">
                    <h2>Insights</h2>

                    {% if item_sales|length > 0 %}
                        <p><strong>Best selling item:</strong> {{ item_sales[0].name }}</p>
                        <p><strong>Units sold:</strong> {{ item_sales[0].quantity }}</p>
                        <p><strong>Revenue from this item:</strong> ${{ item_sales[0].revenue }}</p>
                    {% else %}
                        <p>No insights yet. Serve some orders first.</p>
                    {% endif %}
                </div>
            </div>

        </div>

        <div class="nav">
            <a href="/">Admin</a>
            <a href="/kitchen">Kitchen</a>
        </div>

    </div>
    """

    return render_template_string(
        html,
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_items_sold=total_items_sold,
        average_order_value=average_order_value,
        item_sales=item_sales,
        recent_orders=recent_orders,
        style=STYLE
    )


@app.route("/order/<int:order_id>")
def track_order(order_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, table_number, status, created_at, note
        FROM orders
        WHERE id = ?
    """, (order_id,))

    order = cursor.fetchone()

    if not order:
        conn.close()
        return "Order not found"

    cursor.execute("""
        SELECT item, quantity, total_price
        FROM order_items
        WHERE order_id = ?
    """, (order_id,))

    items = cursor.fetchall()

    active_bill = get_active_table_bill(order[1])
    
    conn.close()

    cart_total = 0
    item_count = 0

    for item in items:
        cart_total += item[2]
        item_count += item[1]

    status = order[2]

    status_order = ["New", "Preparing", "Ready", "Served"]

    if status in status_order:
        active_index = status_order.index(status)
    else:
        active_index = 0

    steps = [
        {
            "name": "New",
            "title": "Received",
            "subtitle": "Order received",
            "icon": "✓"
        },
        {
            "name": "Preparing",
            "title": "Preparing",
            "subtitle": "Cooking now",
            "icon": "🍳"
        },
        {
            "name": "Ready",
            "title": "Ready",
            "subtitle": "Ready to serve",
            "icon": "🔔"
        },
        {
            "name": "Served",
            "title": "Served",
            "subtitle": "Enjoy your meal",
            "icon": "✅"
        }
    ]

    status_message = {
        "New": "Your order has been sent to the kitchen.",
        "Preparing": "The kitchen is preparing your food.",
        "Ready": "Your food is ready to serve.",
        "Served": "Your order has been served."
    }.get(status, "Your order is being processed.")

    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{ style|safe }}

    <div class="order-page">

        <div class="top-hero">
            <h1>Your Order</h1>
            <p>Table {{ order[1] }} · Dine-in order</p>
        </div>

        <div class="order-content">

            <div class="order-success-card">
                <div class="success-top">
                    <div class="success-icon">✓</div>

                    <div>
                        <h2>{{ status_message }}</h2>
                        <p>Thank you. We are working on your order.</p>
                    </div>
                </div>

                <div class="order-meta">
                    <div class="meta-box">
                        <p>Order #</p>
                        <strong>#{{ order[0] }}</strong>
                    </div>

                    <div class="meta-box">
                        <p>Table</p>
                        <strong>{{ order[1] }}</strong>
                    </div>

                    <div class="meta-box">
                        <p>Status</p>
                        <strong>{{ order[2] }}</strong>
                    </div>
                </div>
            </div>

            <div class="order-progress">
                {% for step in steps %}
                <div class="progress-step {% if loop.index0 <= active_index %}active{% endif %}">
                    <div class="progress-circle">
                        {{ step.icon }}
                    </div>

                    <strong>{{ step.title }}</strong>
                    <span>{{ step.subtitle }}</span>
                </div>
                {% endfor %}
            </div>

            <div class="order-summary-card">
                <h2>Order Summary</h2>

                {% for item in items %}
                <div class="order-summary-item">
                    <img src="{{ menu[item[0]]['image'] }}" class="order-summary-img">

                    <div class="order-summary-info">
                        <h3>{{ item[0] }}</h3>
                        <p>x{{ item[1] }}</p>
                    </div>

                    <div class="order-summary-price">
                        ${{ item[2] }}
                    </div>
                </div>
                {% endfor %}

                {% if order[4] %}
                <div class="order-note-card">
                    <strong>Special request:</strong>
                    <p>{{ order[4] }}</p>
                </div>
                {% endif %}

                <div class="order-total-box">
                    <div class="summary-row">
                        <span>Subtotal ({{ item_count }} items)</span>
                        <span>${{ cart_total }}</span>
                    </div>

                    <div class="summary-total">
                        <span>Total</span>
                        <span>${{ cart_total }}</span>
                    </div>
                </div>
            </div>

           {% if active_bill %}
            <div class="order-success-card">
                <div class="success-top">
                    <div class="success-icon">🧾</div>

                    <div>
                        <h2>Bill already requested</h2>
                        <p>To add more food, please cancel the bill request first.</p>
                    </div>
                </div>
            </div>

            <div class="order-actions">
                <a href="/bill_requested/{{ active_bill[0] }}" class="order-action-btn">
                    View Bill Status
                </a>

                <a href="/bill_requested/{{ active_bill[0] }}" class="place-btn">
                    Manage Bill
                </a>
            </div>
            {% else %}
            <div class="order-actions">
                <a href="/table/{{ order[1] }}" class="order-action-btn">
                    Add More Items
                </a>

                <a href="/request_bill/{{ order[0] }}" class="place-btn">
                    Request Bill
                </a>
            </div>
            {% endif %}
        </div>
    </div>

    <script>
        setTimeout(function() {
            window.location.reload();
        }, 5000);
    </script>
    """

    return render_template_string(
        html,
        order=order,
        items=items,
        cart_total=cart_total,
        item_count=item_count,
        steps=steps,
        active_index=active_index,
        status_message=status_message,
        menu=MENU,
        style=STYLE,
        active_bill=active_bill
    )

@app.route("/add_to_cart/<item>")
def add_to_cart(item):
    if item not in MENU:
        return redirect("/")

    cart = session.get("cart", {})

    table_number = session.get("table_number")

    if table_number:
        active_bill = get_active_table_bill(table_number)

        if active_bill:
            return redirect(f"/bill_requested/{active_bill[0]}")
    
    if item not in cart:
        cart[item] = 0

    cart[item] += 1

    session["cart"] = cart

    return redirect(request.referrer or "/")


@app.route("/remove_from_cart/<item>")
def remove_from_cart(item):
    cart = session.get("cart", {})

    if item in cart:
        cart[item] -= 1

        if cart[item] <= 0:
            del cart[item]

    session["cart"] = cart

    return redirect(request.referrer or "/")



@app.route("/bills")
def bills():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            table_number,
            status,
            created_at,
            order_id,
            total_amount,
            payment_method,
            payment_location,
            note
        FROM bill_requests
        ORDER BY id DESC
    """)

    requests = cursor.fetchall()
    conn.close()

    bill_groups = {
        "New": [],
        "Accepted": [],
        "Paid": []
    }

    for req in requests:
        request_data = {
            "id": req[0],
            "table_number": req[1],
            "status": req[2],
            "created_at": req[3],
            "order_id": req[4],
            "total": req[5],
            "payment_method": req[6],
            "payment_location": req[7],
            "note": req[8]
        }

        if req[2] in bill_groups:
            bill_groups[req[2]].append(request_data)

    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{ style|safe }}

    <div class="sales-page">

        <div class="sales-topbar">
            <div>
                <h1>Bill Requests</h1>
                <p>Manage customer bill requests from dine-in tables.</p>
            </div>

            <div class="live-pill">
                ● Live
            </div>
        </div>

        <div class="sales-grid">
            <div class="sales-card">
                <p>New Requests</p>
                <h2>{{ groups["New"]|length }}</h2>
            </div>

            <div class="sales-card">
                <p>Accepted</p>
                <h2>{{ groups["Accepted"]|length }}</h2>
            </div>

            <div class="sales-card">
                <p>Paid</p>
                <h2>{{ groups["Paid"]|length }}</h2>
            </div>
        </div>

        <div class="kitchen-board">

            <div class="kitchen-column">
                <div class="column-title">
                    <h2>New</h2>
                    <span>{{ groups["New"]|length }}</span>
                </div>

                {% for bill in groups["New"] %}
                <div class="kitchen-order-card">
                    <div class="order-top">
                        <h3>Table {{ bill.table_number }}</h3>
                        <div class="table-pill">Bill</div>
                    </div>

                    <div class="order-time">
                        {{ bill.created_at }}
                    </div>

                    <p>Customer is requesting the bill.</p>

                    <p><strong>Payment:</strong> {{ bill.payment_method }}</p>
                    <p><strong>Location:</strong> {{ bill.payment_location }}</p>

                    {% if bill.note %}
                    <div class="order-note">
                        <strong>Note:</strong> {{ bill.note }}
                    </div>
                    {% endif %}

                    <div class="summary-total">
                        <span>Total</span>
                        <span>${{ bill.total }}</span>
                    </div>

                    <form action="/reset_table/{{ bill.table_number }}" method="POST">
                        <button class="kitchen-action served-btn" type="submit">
                            Reset Table
                        </button>
                    </form>

                    <form action="/update_bill_status/{{ bill.id }}/Accepted" method="POST">
                        <button class="kitchen-action accept-btn" type="submit">
                            Accept
                        </button>
                    </form>
                </div>
                {% else %}
                <div class="empty-column">No new bill requests</div>
                {% endfor %}
            </div>

            <div class="kitchen-column">
                <div class="column-title">
                    <h2>Accepted</h2>
                    <span>{{ groups["Accepted"]|length }}</span>
                </div>

                {% for bill in groups["Accepted"] %}
                <div class="kitchen-order-card">
                    <div class="order-top">
                        <h3>Table {{ bill.table_number }}</h3>
                        <div class="table-pill">Accepted</div>
                    </div>

                    <div class="order-time">
                        {{ bill.created_at }}
                    </div>

                    <p>Bring the bill to the table.</p>

                    <p><strong>Payment:</strong> {{ bill.payment_method }}</p>
                    <p><strong>Location:</strong> {{ bill.payment_location }}</p>

                    {% if bill.note %}
                    <div class="order-note">
                        <strong>Note:</strong> {{ bill.note }}
                    </div>
                    {% endif %}

                    <div class="summary-total">
                        <span>Total</span>
                        <span>${{ bill.total }}</span>
                    </div>

                    <form action="/update_bill_status/{{ bill.id }}/Paid" method="POST">
                        <button class="kitchen-action served-btn" type="submit">
                            Mark Paid
                        </button>
                    </form>
                </div>
                {% else %}
                <div class="empty-column">No accepted bills</div>
                {% endfor %}
            </div>

            <div class="kitchen-column">
                <div class="column-title">
                    <h2>Paid</h2>
                    <span>{{ groups["Paid"]|length }}</span>
                </div>

                {% for bill in groups["Paid"][:8] %}
                <div class="kitchen-order-card">
                    <div class="order-top">
                        <h3>Table {{ bill.table_number }}</h3>
                        <div class="table-pill">Paid</div>
                    </div>

                    <div class="order-time">
                        {{ bill.created_at }}
                    </div>

                    <div class="summary-total">
                        <span>Total</span>
                        <span>${{ bill.total }}</span>
                    </div>
                </div>
                {% else %}
                <div class="empty-column">No paid bills</div>
                {% endfor %}
            </div>

        </div>

        <div class="nav">
            <a href="/">Admin</a>
            <a href="/kitchen">Kitchen</a>
            <a href="/sales">Sales Dashboard</a>
        </div>

    </div>

    <script>
        setTimeout(function() {
            window.location.reload();
        }, 3000);
    </script>
    """

    return render_template_string(
        html,
        groups=bill_groups,
        style=STYLE
    )

@app.route("/update_bill_status/<int:request_id>/<new_status>", methods=["POST"])
def update_bill_status(request_id, new_status):
    allowed_statuses = ["Accepted", "Paid"]

    if new_status not in allowed_statuses:
        return redirect("/bills")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE bill_requests
        SET status = ?
        WHERE id = ?
    """, (new_status, request_id))

    conn.commit()
    conn.close()

    return redirect("/bills")

@app.route("/request_bill/<int:order_id>")
def request_bill_page(order_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

   
    cursor.execute("""
        SELECT id, table_number
        FROM orders
        WHERE id = ?
    """, (order_id,))

    order = cursor.fetchone()

    if not order:
        conn.close()
        return "Order not found"
    
    active_bill = get_active_table_bill(order[1])

    if active_bill:
        conn.close()
        return redirect(f"/bill_requested/{active_bill[0]}")

    cursor.execute("""
        SELECT item, quantity, total_price
        FROM order_items
        WHERE order_id = ?
    """, (order_id,))

    items = cursor.fetchall()

    conn.close()

    total_amount = 0
    item_count = 0

    for item in items:
        total_amount += item[2]
        item_count += item[1]

    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{ style|safe }}

    <div class="order-page">

        <div class="top-hero">
            <h1>Request Bill</h1>
            <p>Table {{ order[1] }} · Dine-in order</p>
        </div>

        <div class="order-content">

            <div class="order-summary-card">
                <h2>Bill Summary</h2>

                <div class="summary-row">
                    <span>{{ item_count }} items</span>
                    <span>HK${{ total_amount }}</span>
                </div>

                <div class="summary-total">
                    <span>Total</span>
                    <span>HK${{ total_amount }}</span>
                </div>
            </div>

            <form action="/submit_bill_request" method="POST">
                <input type="hidden" name="order_id" value="{{ order[0] }}">
                <input type="hidden" name="table_number" value="{{ order[1] }}">
                <input type="hidden" name="total_amount" value="{{ total_amount }}">

                <div class="order-summary-card">
                    <h2>Payment Method</h2>

                    <div class="payment-grid">
                        <label class="payment-option">
                            <input type="radio" name="payment_method" value="Octopus" checked>
                            <span>Octopus</span>
                        </label>

                        <label class="payment-option">
                            <input type="radio" name="payment_method" value="AlipayHK">
                            <span>AlipayHK</span>
                        </label>

                        <label class="payment-option">
                            <input type="radio" name="payment_method" value="WeChat Pay HK">
                            <span>WeChat Pay HK</span>
                        </label>

                        <label class="payment-option">
                            <input type="radio" name="payment_method" value="FPS">
                            <span>FPS</span>
                        </label>

                        <label class="payment-option">
                            <input type="radio" name="payment_method" value="Credit Card">
                            <span>Credit Card</span>
                        </label>

                        <label class="payment-option">
                            <input type="radio" name="payment_method" value="Cash">
                            <span>Cash</span>
                        </label>
                    </div>
                </div>

                <div class="order-summary-card">
                    <h2>Payment Location</h2>

                    <div class="payment-grid two">
                        <label class="payment-option">
                            <input type="radio" name="payment_location" value="Pay at table" checked>
                            <span>Pay at table</span>
                        </label>

                        <label class="payment-option">
                            <input type="radio" name="payment_location" value="Pay at counter">
                            <span>Pay at counter</span>
                        </label>
                    </div>

                    <textarea
                        name="note"
                        class="note-box"
                        placeholder="Optional note. Example: Please bring Octopus machine."
                        rows="3"
                    ></textarea>
                </div>

                <div class="order-actions">
                    <a href="/order/{{ order[0] }}" class="order-action-btn">
                        Cancel
                    </a>

                    <button type="submit" class="place-btn">
                        Request Bill
                    </button>
                </div>
            </form>

        </div>
    </div>
    """

    return render_template_string(
        html,
        order=order,
        items=items,
        total_amount=total_amount,
        item_count=item_count,
        style=STYLE
    )

@app.route("/submit_bill_request", methods=["POST"])
def submit_bill_request():
    order_id = int(request.form["order_id"])
    table_number = int(request.form["table_number"])
    total_amount = float(request.form["total_amount"])
    payment_method = request.form["payment_method"]
    payment_location = request.form["payment_location"]
    note = request.form.get("note", "")
    created_at = datetime.now().isoformat()

    active_bill = get_active_table_bill(table_number)

    if active_bill:
        return redirect(f"/bill_requested/{active_bill[0]}")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

   

    cursor.execute("""
        INSERT INTO bill_requests
        (table_number, order_id, total_amount, payment_method, payment_location, note, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        table_number,
        order_id,
        total_amount,
        payment_method,
        payment_location,
        note,
        "New",
        created_at
    ))

    bill_request_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return redirect(f"/bill_requested/{bill_request_id}")

@app.route("/bill_requested/<int:bill_request_id>")
def bill_requested(bill_request_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            table_number,
            order_id,
            total_amount,
            payment_method,
            payment_location,
            note,
            status
        FROM bill_requests
        WHERE id = ?
    """, (bill_request_id,))

    bill = cursor.fetchone()
    conn.close()

    if not bill:
        return "Bill request not found"

    status = bill[7]

    if status == "New":
        page_title = "Bill requested"
        page_message = "A staff member will bring your payment device shortly."
        icon = "🧾"
    elif status == "Accepted":
        page_title = "Bill request accepted"
        page_message = "Staff is on the way to your table."
        icon = "🔔"
    elif status == "Paid":
        page_title = "Payment completed"
        page_message = "Thank you! Your bill has been paid."
        icon = "✅"
    else:
        page_title = "Bill requested"
        page_message = "Your bill request is being processed."
        icon = "🧾"

    html = """
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{ style|safe }}

    <div class="order-page">
        <div class="top-hero">
            <h1>{{ page_title }}</h1>
            <p>Table {{ bill[1] }}</p>
        </div>

        <div class="order-content">

            <div class="order-success-card">
                <div class="success-top">
                    <div class="success-icon">{{ icon }}</div>

                    <div>
                        <h2>{{ page_title }}</h2>
                        <p>{{ page_message }}</p>
                    </div>
                </div>

                <div class="order-meta">
                    <div class="meta-box">
                        <p>Payment</p>
                        <strong>{{ bill[4] }}</strong>
                    </div>

                    <div class="meta-box">
                        <p>Location</p>
                        <strong>{{ bill[5] }}</strong>
                    </div>

                    <div class="meta-box">
                        <p>Total</p>
                        <strong>HK${{ bill[3] }}</strong>
                    </div>
                </div>

                {% if bill[6] %}
                <div class="order-note-card">
                    <strong>Note:</strong>
                    <p>{{ bill[6] }}</p>
                </div>
                {% endif %}
            </div>

            <div class="order-actions">
                <a href="/order/{{ bill[2] }}" class="order-action-btn">
                    View Order
                </a>

                {% if bill[7] in ["New", "Accepted"] %}
                <form action="/cancel_bill_request/{{ bill[0] }}" method="POST">
                    <button type="submit" class="place-btn">
                        Cancel Bill
                    </button>
                </form>
                {% else %}
                <a href="/table/{{ bill[1] }}" class="place-btn">
                    Back to Menu
                </a>
                {% endif %}
            </div>

        </div>
    </div>

    {% if bill[7] != "Paid" %}
    <script>
        setTimeout(function() {
            window.location.reload();
        }, 3000);
    </script>
    {% endif %}
    """

    return render_template_string(
        html,
        bill=bill,
        page_title=page_title,
        page_message=page_message,
        icon=icon,
        style=STYLE
    )

@app.route("/cancel_bill_request/<int:bill_request_id>", methods=["POST"])
def cancel_bill_request(bill_request_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT order_id, status
        FROM bill_requests
        WHERE id = ?
    """, (bill_request_id,))

    bill = cursor.fetchone()

    if not bill:
        conn.close()
        return "Bill request not found"

    order_id = bill[0]
    status = bill[1]

    if status in ["New", "Accepted"]:
        cursor.execute("""
            UPDATE bill_requests
            SET status = 'Cancelled'
            WHERE id = ?
        """, (bill_request_id,))

    conn.commit()
    conn.close()

    return redirect(f"/order/{order_id}")

@app.route("/reset_table/<int:table_number>", methods=["POST"])
def reset_table(table_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE bill_requests
        SET status = 'Closed'
        WHERE table_number = ?
          AND status IN ('Paid', 'Closed')
    """, (table_number,))

    conn.commit()
    conn.close()

    return redirect("/bills")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)