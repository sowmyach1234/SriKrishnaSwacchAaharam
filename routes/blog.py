from flask import Blueprint, render_template


blog = Blueprint(
    "blog",
    __name__
)



blogs = [

    {
        "id":1,
        "title":"Benefits of Cold Pressed Oils",
        "image":"oil.jpg",
        "description":"Learn why traditionally extracted oils are healthier and preserve natural nutrients.",
        "content":
        """
        Cold pressed oils are prepared using traditional extraction methods
        that preserve natural nutrients, flavour and essential properties.

        They are a healthier choice compared to heavily processed oils.
        """
    },


    {
        "id":2,
        "title":"Why Millets Are The Future",
        "image":"millet.jpg",
        "description":"Discover the nutritional value of ancient grains like Foxtail Millet and Little Millet.",
        "content":
        """
        Millets are ancient grains rich in fibre, minerals and nutrients.

        Foxtail Millet and Little Millet are excellent choices for a healthy
        traditional lifestyle.
        """
    },


    {
        "id":3,
        "title":"Traditional Pickles And Their Heritage",
        "image":"pickle.jpg",
        "description":"Explore the traditional preparation methods behind authentic pickles.",
        "content":
        """
        Traditional pickles are prepared using natural ingredients,
        authentic spices and time-tested methods.
        """
    },


    {
        "id":4,
        "title":"The Purity Of A2 Cow Ghee",
        "image":"ghee.jpg",
        "description":"Understand the traditional process and benefits of pure A2 cow ghee.",
        "content":
        """
        A2 cow ghee prepared using traditional methods provides rich flavour
        and maintains the heritage of natural dairy preparation.
        """
    },


    {
        "id":5,
        "title":"Organic Farming Journey",
        "image":"farmer.jpg",
        "description":"A look into natural farming practices and farmer connections.",
        "content":
        """
        Organic farming focuses on natural cultivation methods while
        supporting farmers and protecting the environment.
        """
    },


    {
        "id":6,
        "title":"Healthy Traditional Sweets",
        "image":"sweets.jpg",
        "description":"Traditional sweets prepared using natural ingredients.",
        "content":
        """
        Traditional sweets made with natural ingredients bring together
        authentic taste and cultural heritage.
        """
    }

]





@blog.route("/blog")
def blog_page():


    return render_template(
        "blog/index.html",
        blogs=blogs
    )







@blog.route("/blog/<int:id>")
def blog_detail(id):


    selected_blog = None


    for item in blogs:

        if item["id"] == id:

            selected_blog = item



    return render_template(
        "blog/detail.html",
        blog=selected_blog
    )