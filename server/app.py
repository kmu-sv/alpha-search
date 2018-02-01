from flask import Flask, render_template

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/<token>')
def index(token):
    print(token)
    return render_template("index.html", token=token)


if __name__ == '__main__':
    app.run(debug=True)
