import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

tf.get_logger().setLevel("ERROR")

# Load model once
model = hub.load(
    "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
)

def load_image(path):
    img = Image.open(path).convert("RGB")

    # Better clarity, still RAM-safe
    max_size = 330   # ⭐ increase from 128 → 256
    img.thumbnail((max_size, max_size))

    img = np.array(img).astype(np.float32) / 255.0
    img = tf.convert_to_tensor(img, dtype=tf.float32)

    return tf.expand_dims(img, axis=0)


def apply_style(content_path, style_path, output_path):
    content = load_image(content_path)
    style = load_image(style_path)

    output = model(content, style)   # DO NOT use [0]
    output = tf.squeeze(output)

    output = tf.clip_by_value(output, 0.0, 1.0)
    output = (output * 255).numpy().astype("uint8")

    Image.fromarray(output).save(output_path)
