# https://forum.omz-software.com/topic/2185/image-from-scene/10

from io import BytesIO
from PIL import Image

i = view.take_snapshot()
pil_image = Image.open(BytesIO(i.to_png()))
