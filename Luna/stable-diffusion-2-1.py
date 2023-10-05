import os
import sys
from torch import autocast
from diffusers import DiffusionPipeline

SAVE_PATH = os.path.join(os.environ["USERPROFILE"], "PycharmProjects", "Luna", "images")


def uniquify(path):
    filename, extension = os.path.splitext(path)
    x = 1
    while os.path.exists(path):
        path = filename + f"({x})" + extension
        x += 1
    return path

sys.argv.append("a gray cat")

if len(sys.argv) != 2:
    raise SyntaxError(f"Expected 1 argument, got {len(sys.argv)}.")
else:
    prompt = sys.argv[1]
    if len(prompt) > 200:
        raise ValueError(f"Prompt exceeds 200 characters.")

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1")
pipe = pipe.to("cpu")


with autocast("cpu"):
    image = pipe(prompt).images[0]

    img_path = uniquify(os.path.join(SAVE_PATH, (prompt[:25] + "...") if len(prompt) > 25 else prompt) + ".png")
    image.save(img_path)

    print(img_path)
