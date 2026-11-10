
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# PART 1: OOP Classes
class Product:
    def __init__(self, id, name, price, image):
        self.id = id
        self.name = name
        self.price = price
        self.image = image

class Calculator:
    def total(self, price, qty):
        return price * qty
    def discount(self, total, percent=10):
        return total - (total * percent / 100)
    def delivery(self, total):
        if total > 5000:
            return 0
        else:
            return 250

class Cart:
    def __init__(self):
        self.items = []
    def add_item(self, product, qty):
        self.items.append({"product": product, "qty": qty})
    def get_total(self):
        calc = Calculator()
        total = 0
        for item in self.items:
            total += calc.total(item["product"].price, item["qty"])
        return total

# PART 2: Products Data
products = [
    Product(1, "Wireless Headphones", 3500, "🎧"),
    Product(2, "Smart Watch", 5500, "⌚"),
    Product(3, "Laptop Stand", 1800, "💻"),
    Product(4, "Mobile Cover", 900, "📱"),
    Product(5, "Keyboard", 2800, "⌨️"),
    Product(6, "Mouse", 1500, "🖱️"),
]

cart = Cart()
calc = Calculator()

# PART 3: HTML Design
HTML = """
<!DOCTYPE html>
<html>
<head><title>My Shop</title>
<style>
body{font-family:Arial;background:#f2f2f2;text-align:center}
h1{color:#ff6b00}
.box{display:inline-block;background:white;padding:20px;margin:10px;border-radius:10px;width:200px}
button{background:#ff6b00;color:white;border:none;padding:8px 15px;border-radius:5px;cursor:pointer}
.bill{background:white;padding:20px;margin:20px auto;width:400px;border-radius:10px;text-align:left}
.clear{background:red}
</style>
</head>
<body>
<h1>My E-Commerce Shop</h1>
<p>OOP + Python + Calculator</p>
{% for p in products %}
<div class="box">
<h2>{{p.image}}</h2>
<h3>{{p.name}}</h3>
<p><b>Rs. {{p.price}}</b></p>
<form method="POST" action="/add">
<input type="hidden" name="id" value="{{p.id}}">
Qty: <input type="number" name="qty" value="1" style="width:40px">
<button>Add to Cart</button>
</form>
</div>
{% endfor %}

{% if cart_items %}
<div class="bill">
<h2>Bill - Calculator 🧾</h2>
{% for item in cart_items %}
<p>{{item.product.name}} x {{item.qty}} = Rs. {{item.product.price * item.qty}}</p>
{% endfor %}
<hr>
<p>Sub Total: Rs. {{total}}</p>
<p>Discount (10%): - Rs. {{discount_amount}}</p>
<p>Delivery: Rs. {{delivery}}</p>
<h3>Grand Total: Rs. {{grand_total}}</h3>
<form method="POST" action="/clear"><button class="clear">Clear Cart</button></form>
</div>
{% endif %}
</body>
</html>
"""

# PART 4: Routes
@app.route("/")
def home():
    total = cart.get_total()
    discounted = calc.discount(total)
    discount_amount = total - discounted
    delivery = calc.delivery(discounted) if total > 0 else 0
    grand_total = discounted + delivery
    return render_template_string(HTML, products=products, cart_items=cart.items, total=total, discount_amount=discount_amount, delivery=delivery, grand_total=grand_total)

@app.route("/add", methods=["POST"])
def add():
    pid = int(request.form["id"])
    qty = int(request.form["qty"])
    for p in products:
        if p.id == pid:
            cart.add_item(p, qty)
    return redirect("/")

@app.route("/clear", methods=["POST"])
def clear():
    cart.items = []
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)