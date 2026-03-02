from flask import Flask, send_file, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import io
import math

app = Flask(__name__)

# Prime check
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

# Spiral matrix
def create_spiral(n):
    matrix = [[0]*n for _ in range(n)]
    num = 1
    top, bottom = 0, n-1
    left, right = 0, n-1

    while top <= bottom and left <= right:
        for i in range(left, right+1):
            matrix[top][i] = num; num += 1
        top += 1

        for i in range(top, bottom+1):
            matrix[i][right] = num; num += 1
        right -= 1

        for i in range(right, left-1, -1):
            matrix[bottom][i] = num; num += 1
        bottom -= 1

        for i in range(bottom, top-1, -1):
            matrix[i][left] = num; num += 1
        left += 1

    return matrix

# Generate image
def generate_ulam_image(n):
    spiral = create_spiral(n)
    img_array = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if is_prime(spiral[i][j]):
                img_array[i][j] = 1

    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(img_array, cmap='binary')
    ax.axis('off')

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    img.seek(0)
    plt.close(fig)
    return img

@app.route("/")
def index():
    n = request.args.get("n", default=100, type=int)
    return render_template("index.html", n=n)

@app.route("/ulam")
def ulam():
    n = request.args.get("n", default=100, type=int)
    img = generate_ulam_image(n)
    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)