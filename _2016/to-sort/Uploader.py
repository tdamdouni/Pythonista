from __future__ import print_function
# https://gist.github.com/jefflovejapan/5076080

import requests
import console
import clipboard
import Image

console.clear()

thisImage = clipboard.get_image(0)
thisImage.show()
user = 'jeffblagdon'
passw = 'du7rte9ghil7ce8phi7theg5spul'

#derp = console.login_alert('Welcome to The Verge')

s = requests.Session()
r = s.get('http://www.theverge.com/admin/assets/new?community_id=372', auth=(user, passw))
print(r.url)
print(r.text)

payload = {'title':'test', 'uploaded_data':thisImage, 'tags':'testing1, testing2', 'disable_resize_on_save':'false'}

final = s.get('', params=payload)

print(s.content)
print(s.cookies)
