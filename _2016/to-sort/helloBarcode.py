# helloBarcode - ZBar delivers barcode data to Pythonista

# https://gist.github.com/cclauss/6708024

programName = sys.argv[0].rpartition('/')[2]
theBarcode  = sys.argv[1] if len(sys.argv) > 1 else None
fmt = '{} was launched with barcode: {}'
print(fmt.format(programName, theBarcode))

# Save this file in Pythonista as 'helloBarcode'.
# Download free app ZBar from the iTunes App Store.
# Launch ZBar on your device.
# Scan the barcode on a book, coke can, whatever.
# On the Barcode Detail screen, click Edit in the upper right.
# Scroll to the bottom fo the screen and Add New Link.
# Set the Name to Pythonista helloBarcode.
# Set the URL to pythonista://helloBarcode?action=run&argv=
# Click the plus (+) in the upper right of the screen.
# I selected GTIN-13 for everyday products.
# Click Edit Link URL in the upper left of the screen.
# This should complete the URL so it ends in &argv={GTIN-13}
# Click Done and then click Save and then click Done.
# Click the Pythonista helloBarcode line.
# Pythonista's helloBarcode should be launched...
# ... your barcode should appear!
