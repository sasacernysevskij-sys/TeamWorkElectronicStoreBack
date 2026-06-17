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