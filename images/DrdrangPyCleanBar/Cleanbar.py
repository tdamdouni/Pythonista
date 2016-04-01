#!/usr/bin/python

import Image
import base64, zlib

# Jay Parlar convinced me to turn this data structure
# from a dictionary into an object. 
class PackedImage(object):
  def __init__(self, mode, size, data):
    self.mode = mode
    self.size = size
    self.data = ''.join(data)
  
  def unpack(self):
    return Image.fromstring(self.mode,
                            self.size,
                            zlib.decompress(base64.b64decode(self.data)))

def cleanbar(screenshot, connection='wifi'):
  '''Clean up the statusbar in an iOS screenshot.

  Cover the signal strength, battery, location, and bluetooth
  graphics with full strength symbols.'''
  
  # This is for retina displays.
  height = 40

  # Statusbar image data for an iPhone 4, 4s, 5, 5c, or 5s portrait screenshot.
  # The data string is compressed and base64-encoded.
  if connection=='lte':
    limg = PackedImage('L',
                     (200, 40),
                     ['eJztl0toE0EYx6fGtvHVYlEiKGlMe/CiaEXTg4KotD56EqTY3k',
                      'RapBVEweBJBK0U0UPAJBVRKj4qiI+bQXxWsFaheGjTeig2hFCQ',
                      'trYlMTGyf/cxs9lkQynZXQw4v8N83zfzLfv/s5kZQgiHw+FwOB',
                      'zO/8Aqt3uJEjQsk5dKHSWZJt1qkXEfOCyGdmhpFGfcL34j7q+S',
                      'm/SrOUzdlINnWksDmWLpaattrP4Vx1Mx7n8kMYGwHLcQsnwcA7',
                      'd/oN9G8q3mIjyQw3qvxB30ybGGCENehXqrfXTiYjTtYNU9XGZp',
                      'C54QUvYdOzO9mtVcqA+FQ2jJN52DMzCRigSqDVaMIcF9Fd48Ss',
                      '/hjDj60GyRj8Y5+Tc6f8BQxajDe7IVY3mU7kFIHD9ikzU+XLN0',
                      's827DFQqfpwgZBi79UrLx3GEXEKfptlMH0H11AgaqBj2n4kKQs',
                      '7jbh6le4WZEN6ttMhHRNUTMVAxWvFQHF1ColKvdO0ocL1M++4C',
                      'fNDz6rjugaSqJ1VSeMV4i4NS6MdJndKjM8IInou9S20GfKSU6+',
                      'OD7gFTv0ctJmWR7fiSq7RNiNXbB9BF1uClAR+L2B89BipKF4S0',
                      'xB9gW7bSjYl4DSHroji2Dzes8OGao3KUU6jASsEWw+dBmSgVqy',
                      'o9qxwH2xOJkHhsWeDDzPujCYM0a8C0PUvpLZySYzMwqe51k+/z',
                      'YCQVCVYbrCSeoYNm4pdpzVLaDb+SvMa3Smt8mIYjnapi+TW8kY',
                      'KqdAeSHil2I4lXpbSpSH148VjN6yDUEq3SHqR7O31hhJ1f0Uvn',
                      'FvLxqU3BSbJ8sOldVhigjKIpUwzjSrbSjjEBmPVVkA0xXFCmFv',
                      'LBTkPpv4zGB5sOWKB/sazwbC7/h6/ncDgcDodThPwFVX6ICw=='])
  else:
    limg = PackedImage('L',
                     (200, 40),
                     ['eJztlltIFFEYx896v6SSKCaJ2uZDD22UUVtBJBWZaS9BSgnWQy',
                      'ShvSgk9hLdTMl8ENIVozCSCsTqKUW6qFCiYQaZ2oOrq4iUtKm4',
                      'OW7MvzOzM7Ozl3bE8RI0v4fzne+cb2f+/z1nzgwhGhoaGhoaGh',
                      'r/AxF6vZ8jyAjlpwLjdM4ij1kZgenlbSPTmBlpK08PXEXtchqB',
                      'TBryISedjuhbFjBXE80Xec7KSKyakk1OVSWtugfK+l9zeEbj4a',
                      'ccoxjg4zZCwobRdf87Ov2Jt1knEZUMXGEqo1bfRyGujtvjxOwR',
                      'bord02gmJGgEu521slmJvWZOetfltHg/4hd/oPQdl5r3LeLOib',
                      'WjjKU2SWUm8pHV30aJF6WXUETbauT49HF2gcpuNshGDE3ckuQp',
                      '2kif4Rdv9qiqTCQVHWQ7hrwoTUMrbd9ji08fGQymjrmPTYFxH/',
                      'MgeVrYhbPJKjKJGpwjpB/7PZUGD+MEuYEnsmJv+yq7V0/bgMz6',
                      'PiusffVZATTT92Yr2SAm6XEyqchEQn7aIgkpxUMvSg+y1la0r1',
                      'PwQeihrcszS1c3n9HxY0pYpF9YVGQiuXhM22TWFuWpNHYQqAqS',
                      '39urD3rkvYSclmhlF4TMS/WMbumZyFtkcKETFzyUnrSyX/CC1g',
                      'b4K/goohe1XjeGkhDjtW+0X7wYH8u6HimY5EXm44O70vPsxJ6Q',
                      'LpSRGLQp+KAP2YMYoRtuQqPOa5Ebzn1epyITKANr5/gN7HBVus',
                      'k2t5mQDeM4dQh3lXz4H5clmUFea9xJnhHkOE6hJWbC/SfQ080z',
                      'LoiVlBY7joOdNlsrPbYUfHBsbRhjxhoMf533YBnfH1noFnpH8C',
                      'PERek9XORjDjAp/cE+fGTZ+avbsxZvJNFkYSymJJUZx3MUCD26',
                      'MrkuSitQ4+i8xlfpa8mHj9B23kdH2OJ9LBtxdkY6Iu/gDRckpb',
                      'swb+RiBebxSvwU97WvInuojZ41+EAkpARNUj8VbAqRK62DvaGw',
                      'egADiZ/QIIz58kFiP6M/dqWk+mQQst3cj1vERWnBEAtMV0eShA',
                      'lccQz59EE2tiasjE61hBsNwWutQUNDQ0NDQ+Pf4g+RSY1o'])
  rimg = PackedImage('L',
                     (130, 40),
                     ['eJxjYBgFo2AUDFHwX3XAXfBfm462Ga+9j8UF//XpZv+KV//LsL',
                      'ngvzld7Pc6ALTqFaY4yAX/bdFF9/0nFhwgznq25Ktg5cVIYoy7',
                      'OSAusAFKuKCq3/k/hkiPRf7fSYQqvtJX38AOuGCMJLr9/38OsA',
                      'sY5YFSfig6/vsTHQb+/wnaLzvh80OoapT4/vP//z8OsAsYeIHs',
                      'cBQXMBHtAqb/TPjtN176B674AYoMx6//oFAAuwA9EKjnAte9n4',
                      'GK/kEVW6FKsnwCOQHoAsn/6GmRSi5gS7j0/zuS2tfoCpieg8WV',
                      '/2MUCaS54P9/a6wOMH6CpjYdQwnjDagUeslMqguwpsZL79GU/s',
                      'Gm6gRYShpdmCouQAbghFCPVQokY4wpSqoLCOQHiAsEsUiwvgKb',
                      'glE90iQM1mARF4QZo0cPF2BpBqgAhQ9D8oIpZS5wJMIFFzBFHY',
                      'H6J4FKJGEgw44CFxCyHuICSwzBTKD2NEipzA0sHr1o7AKM0oiB',
                      'AVgiOjEgXOBDYxdglkYMvJ/ASQPoAvH/6NUzdetGkIG/8Mj9V/',
                      '2P0UShdvuA4V8dPhf8x9JMo3Yb6SEeOZAptG+qFuF3gRbNHYAX',
                      'AEukgXUAw3+5AXbAKBgFwxUAAElqKPY='])

  # Calculate various dimensions based on the size of the screenshot.
  width = screenshot.size[0]
  lbox = (0, 0, limg.size[0], limg.size[1])
  rbox = (width - rimg.size[0], 0, width, rimg.size[1])
  
  # Decide whether the overlay text and graphics should be black or white.
  # The pixel at (width-13, 21) is in the button of the battery.
  p = screenshot.getpixel((width-13, 21))[:3]
  if sum(p) > 3*250:
    symbolcolor = 'white'
  else:
    symbolcolor = 'black'

  # Create the masks.
  lmask = limg.unpack()
  rmask = rimg.unpack()

  # Make the overlays.
  left = Image.new('RGBA', limg.size, symbolcolor)
  left.putalpha(lmask)
  right = Image.new('RGBA', rimg.size, symbolcolor)
  right.putalpha(rmask)

  # Paste the overlays and return.
  screenshot.paste(left, lbox, left)
  screenshot.paste(right, rbox, right)
  return screenshot

# And here we go.
if __name__ == '__main__':
  import photos, console
  screenshot = photos.pick_image()
  console.clear()
  cleanbar(screenshot).show()
