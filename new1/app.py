import string
import random
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
shortened_urls = {}

# function to generate a random short URL
def generate_short_urls(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_urls()
        # generate a new short URL if the generated one already exists in the dictionary
        while short_url in shortened_urls:
            short_url = generate_short_urls()
        shortened_urls[short_url] = long_url
        # display the shortened URL to the user
        return f"Shortened URL: {request.url_root}{short_url}"
    return render_template("demo.html")

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        # return a 404 error message if the shortened URL is not found
        return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)
