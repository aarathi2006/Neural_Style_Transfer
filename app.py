from flask import Flask, render_template, request
from nst_model import apply_style
import os

app = Flask(__name__)

UPLOAD_DIR = "static/uploads"
OUTPUT_DIR = "static/output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    content_img = None
    style_img = None
    result_img = None

    if request.method == "POST":
        content = request.files["content"]
        style = request.files["style"]

        content_path = os.path.join(UPLOAD_DIR, "content.jpg")
        style_path = os.path.join(UPLOAD_DIR, "style.jpg")
        output_path = os.path.join(OUTPUT_DIR, "result.jpg")

        content.save(content_path)
        style.save(style_path)

        apply_style(content_path, style_path, output_path)

        content_img = content_path
        style_img = style_path
        result_img = output_path

    return render_template(
        "index.html",
        content_img=content_img,
        style_img=style_img,
        result_img=result_img
    )

if __name__ == "__main__":
    app.run(debug = True)
