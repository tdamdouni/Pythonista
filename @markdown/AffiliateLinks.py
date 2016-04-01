import console
import urllib
import clipboard

origURL = clipboard.get()

affID = "YOUR Affiliate URL"

affURL = origURL + "&" + affID

clipboard.set(affURL)

