from models.cart_item import CartItem
from models.product import Product
from models.order import Order
from models.order_item import OrderItem


class OrderService:
    def create_order(self, db, user_id):
        cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

        if len(cart_items) == 0:
            return {
                "detail": "Корзина пустая"
            }, 400

        try:
            total_price = 0
            products_data = []

            for cart_item in cart_items:
                product = db.query(Product).filter(Product.id == cart_item.product_id).first()

                if product is None:
                    return {
                        "detail": f"Товар с id {cart_item.product_id} не найден"
                    }, 404

                if product.stock < cart_item.quantity:
                    return {
                        "detail": f"Недостаточно товара на складе: {product.name}"
                    }, 400

                subtotal = product.price * cart_item.quantity
                total_price += subtotal

                products_data.append({
                    "cart_item": cart_item,
                    "product": product,
                    "price": product.price,
                    "quantity": cart_item.quantity,
                    "subtotal": subtotal
                })

            order = Order(
                user_id=user_id,
                status="new",
                total_price=total_price
            )

            db.add(order)
            db.flush()

            order_items_response = []

            for item in products_data:
                product = item["product"]
                cart_item = item["cart_item"]

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item["quantity"],
                    price=item["price"]
                )

                db.add(order_item)

                product.stock -= item["quantity"]

                db.delete(cart_item)

                order_items_response.append({
                    "product_id": product.id,
                    "name": product.name,
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "subtotal": item["subtotal"]
                })

            db.commit()
            db.refresh(order)

            return {
                "message": "Заказ успешно создан",
                "order": {
                    "id": order.id,
                    "user_id": order.user_id,
                    "status": order.status,
                    "total_price": order.total_price,
                    "created_at": str(order.created_at),
                    "items": order_items_response
                }
            }, 201

        except Exception:
            db.rollback()
            return {
                "detail": "Ошибка при создании заказа"
            }, 500

    def get_my_orders(self, db, user_id):
        orders = db.query(Order).filter(Order.user_id == user_id).all()

        result = []

        for order in orders:
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

            items = []

            for order_item in order_items:
                product = db.query(Product).filter(Product.id == order_item.product_id).first()

                product_name = None

                if product is not None:
                    product_name = product.name

                items.append({
                    "product_id": order_item.product_id,
                    "name": product_name,
                    "quantity": order_item.quantity,
                    "price": order_item.price,
                    "subtotal": order_item.price * order_item.quantity
                })

            result.append({
                "id": order.id,
                "status": order.status,
                "total_price": order.total_price,
                "created_at": str(order.created_at),
                "items": items
            })

        return result, 200