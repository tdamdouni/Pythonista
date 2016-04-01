from Cleanbar import cleanbar
import photos, console

screenshot = photos.pick_image()
console.clear()
cleanbar(screenshot, connection='lte').show()
