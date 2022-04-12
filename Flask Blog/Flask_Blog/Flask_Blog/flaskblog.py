from flask import Flask, render_template, url_for

app = Flask(__name__)
posts = [
{
"author":"Azaan",
"title":"Post 1",
"date_posted":"February 26, 2022",
"content" : "Post 1 Content"   
},
{
"author":"Ben Dover",
"title":"Post 2",
"date_posted":"February 25, 2022",
"content" : "Post 2 Content"   
}
]
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",posts=posts,title="Home/Posts")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)