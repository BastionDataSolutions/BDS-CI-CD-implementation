from flask import jsonify, request
from models import products, cart

def register_routes(app):

    # ✅ NEW: Home page (HTML)
    @app.route("/")
    def home():
        return """
        <html>
            <head>
                <title>Flask App on AWS ECS</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f6f8;
                        padding: 40px;
                    }
                    h1 { color: #2c3e50; }
                    ul { font-size: 18px; }
                    code { background: #eaeaea; padding: 4px 6px; }
                </style>
            </head>
            <body>
                <h1>🚀 Flask Application Running on AWS ECS</h1>
                <p>This service is deployed using Docker, ECS (Fargate), and an Application Load Balancer.</p>

                <h3>Available Endpoints</h3>
                <ul>
                    <li><code>/health</code> – Health check</li>
                    <li><code>/products</code> – View products</li>
                    <li><code>/cart</code> – View cart</li>
                    <li><code>/checkout</code> – Checkout order</li>
                </ul>

                <p><b>Status:</b> Service is running successfully ✅</p>
            </body>
        </html>
        """

    # Existing routes (UNCHANGED)
    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    @app.route("/products", methods=["GET"])
    def get_products():
        return jsonify(products)

    @app.route("/cart", methods=["GET"])
    def view_cart():
        return jsonify(cart)

    @app.route("/cart", methods=["POST"])
    def add_to_cart():
        product_id = request.json.get("product_id")
        product = next((p for p in products if p["id"] == product_id), None)

        if not product:
            return {"error": "Product not found"}, 404

        cart.append(product)
        return {"message": "Added to cart", "cart": cart}, 201

    @app.route("/checkout", methods=["POST"])
    def checkout():
        total = sum(item["price"] for item in cart)
        cart.clear()
        return {"message": "Order placed", "total_amount": total}, 200
