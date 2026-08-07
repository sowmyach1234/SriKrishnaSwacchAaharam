from flask import Blueprint, render_template

from models.product import Product


categories = Blueprint(
    "categories",
    __name__
)



@categories.route("/categories")
def category_page():


    category_data = [

        {
            "name": "Cold Pressed Oils",
            "image": "oil.jpg",
            "description": "Pure traditional oils prepared using natural extraction methods.",
            "filter": "Cold Pressed Oils"
        },


        {
            "name": "Traditional Pickles",
            "image": "pickle.jpg",
            "description": "Authentic homemade pickles with traditional flavours.",
            "filter": "Traditional Pickles"
        },


        {
            "name": "Organic Millets",
            "image": "millet.jpg",
            "description": "Healthy ancient grains sourced naturally from farmers.",
            "filter": "Millets"
        },


        {
            "name": "A2 Cow Ghee",
            "image": "ghee.jpg",
            "description": "Pure A2 cow ghee made using traditional methods.",
            "filter": "A2 Cow Ghee"
        },


        {
            "name": "Dry Fruits",
            "image": "dryfruits.jpg",
            "description": "Premium quality naturally selected dry fruits.",
            "filter": "Dry Fruits"
        },


        {
            "name": "Organic Sweets",
            "image": "sweets.jpg",
            "description": "Traditional sweets prepared with natural ingredients.",
            "filter": "Organic Sweets"
        }

    ]



    for category in category_data:


        category["products"] = Product.query.filter_by(
            category=category["filter"]
        ).limit(4).all()



    return render_template(

        "categories/index.html",

        categories=category_data

    )