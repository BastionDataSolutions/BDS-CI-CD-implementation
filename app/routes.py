from flask import jsonify, request
from models import products, cart

def register_routes(app):

    @app.route("/")
    def home():
        return """
        <html>
            <head>
                <title>Flask App on ECS</title>
                <style>
                    body {
                        font-family: Arial;
                        text-align: center;
                        margin-top: 60px;
                        background-color: #f4f6f8;
                    }
                    h1 {
                        color: #2c3e50;
                    }
                    ul {
                        list-style: none;
                        padding: 0;
                    }
                    li {
                        margin: 10px 0;
                        font-size: 18px;
                    }
                </style>
            </head>
            <body>
                <h1>🚀 Flask Application Running on AWS ECS</h1>
                <p>This service is deployed using Docker and ECS (Fargate)</p>

                <h3>Available Endpoints</h3>
                <ul>
                    <li>/health – Health check</li>
                    <li>/products – View products</li>
                    <li>/cart – View cart</li>
                    <li>/checkout – Checkout order</li>
                </ul>

                <p><b>Status:</b> Service is running successfully ✅</p>
            </body>
        </html>
        """

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
