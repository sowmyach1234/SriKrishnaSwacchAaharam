from app import app

from models import db

from models.product import Product



products = [

# ==========================
# COLD PRESSED OILS
# ==========================


{
"name":"Groundnut Oil",
"category":"Cold Pressed Oils",
"description":"Traditional wooden pressed groundnut oil with natural nutrients.",
"price":450,
"stock":50,
"image":"groundnut_oil.jpg"
},


{
"name":"Sesame Oil",
"category":"Cold Pressed Oils",
"description":"Pure cold pressed sesame oil prepared naturally.",
"price":520,
"stock":40,
"image":"sesame_oil.jpg"
},


{
"name":"Coconut Oil",
"category":"Cold Pressed Oils",
"description":"Fresh coconut oil extracted using traditional methods.",
"price":600,
"stock":30,
"image":"coconut_oil.jpg"
},



# ==========================
# PICKLES
# ==========================


{
"name":"Mango Pickle",
"category":"Traditional Pickles",
"description":"Authentic Andhra style mango pickle.",
"price":250,
"stock":60,
"image":"mango_pickle.jpg"
},


{
"name":"Gongura Pickle",
"category":"Traditional Pickles",
"description":"Traditional homemade gongura pickle.",
"price":280,
"stock":45,
"image":"gongura_pickle.jpg"
},



# ==========================
# MILLETS
# ==========================

{
"name":"Foxtail Millet",
"category":"Organic Millets",
"description":"Healthy organic foxtail millet rich in nutrition.",
"price":180,
"stock":70,
"image":"foxtail_millet.jpg"
},


{
"name":"Little Millet",
"category":"Organic Millets",
"description":"Natural little millet for healthy lifestyle.",
"price":200,
"stock":50,
"image":"little_millet.jpg"
},


# ==========================
# GHEE
# ==========================


{
"name":"A2 Cow Ghee",
"category":"A2 Cow Ghee",
"description":"Pure A2 cow ghee prepared traditionally.",
"price":900,
"stock":25,
"image":"a2_ghee.jpg"
},



# ==========================
# DRY FRUITS
# ==========================


{
"name":"California Almonds",
"category":"Dry Fruits",
"description":"Premium quality almonds.",
"price":750,
"stock":35,
"image":"almonds.jpg"
},



# ==========================
# ORGANIC SWEETS
# ==========================


{
"name":"Millet Chikki",
"category":"Organic Sweets",
"description":"Healthy millet sweet made with jaggery.",
"price":150,
"stock":80,
"image":"millet_chikki.jpg"
}

]



with app.app_context():


    db.create_all()


    for item in products:


        product = Product(

            product_name=item["name"],

            category=item["category"],

            description=item["description"],

            price=item["price"],

            stock=item["stock"],

            image=item["image"],

            organic=True

        )


        db.session.add(product)



    db.session.commit()



    print("Products inserted successfully")