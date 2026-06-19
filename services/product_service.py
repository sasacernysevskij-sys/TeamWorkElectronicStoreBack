from models.product import Product


class ProductService:
    def get_products(
        self,
        db,
        product_type=None,
        skip=0,
        limit=10
    ):
        query = db.query(Product)

        if product_type:
            query = query.filter(Product.product_type == product_type)

        products = query.offset(skip).limit(limit).all()

        return [
            {
                "id": product.id,
                "name": product.name,
                "article": product.article,
                "description": product.description,
                "price": product.price,
                "product_type": product.product_type,
                "stock": product.stock,
                "rating": product.rating,
                "image_url": product.image_url
            }
            for product in products
        ], 200

    def create_product(
        self,
        db,
        name,
        article,
        description,
        price,
        product_type,
        stock,
        rating,
        image_url
    ):
        existing_product = db.query(Product).filter(Product.article == article).first()

        if existing_product is not None:
            return {
                "detail": "Товар с таким article уже существует"
            }, 400

        product = Product(
            name=name,
            article=article,
            description=description,
            price=price,
            product_type=product_type,
            stock=stock,
            rating=rating,
            image_url=image_url
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return {
            "id": product.id,
            "name": product.name,
            "article": product.article,
            "description": product.description,
            "price": product.price,
            "product_type": product.product_type,
            "stock": product.stock,
            "rating": product.rating,
            "image_url": product.image_url
        }, 201

    def delete_product(self, db, product_id):
        product = db.query(Product).filter(Product.id == product_id).first()

        if product is None:
            return {
                "detail": "Товар не найден"
            }, 404

        db.delete(product)
        db.commit()

        return {
            "message": "Товар удалён",
            "product_id": product_id
        }, 200

    def update_product(
        self,
        db,
        product_id,
        name=None,
        article=None,
        description=None,
        price=None,
        product_type=None,
        stock=None,
        rating=None,
        image_url=None
    ):
        product = db.query(Product).filter(Product.id == product_id).first()

        if product is None:
            return {
                "detail": "Товар не найден"
            }, 404

        if article is not None and article != product.article:
            existing_product = db.query(Product).filter(Product.article == article).first()

            if existing_product is not None:
                return {
                    "detail": "Товар с таким article уже существует"
                }, 400

            product.article = article

        if name is not None:
            product.name = name

        if description is not None:
            product.description = description

        if price is not None:
            product.price = price

        if product_type is not None:
            product.product_type = product_type

        if stock is not None:
            product.stock = stock

        if rating is not None:
            product.rating = rating

        if image_url is not None:
            product.image_url = image_url

        db.commit()
        db.refresh(product)

        return {
            "id": product.id,
            "name": product.name,
            "article": product.article,
            "description": product.description,
            "price": product.price,
            "product_type": product.product_type,
            "stock": product.stock,
            "rating": product.rating,
            "image_url": product.image_url
        }, 200