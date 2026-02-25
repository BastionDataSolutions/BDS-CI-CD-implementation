from flask import jsonify, request
from models import products, cart

def register_routes(app):

    @app.route("/")
    def home():
        return {"message": "ECS app running 🚀"}, 200

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
