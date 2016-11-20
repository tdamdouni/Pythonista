from collections import Counter
from console import hud_alert, input_alert
import dialogs

count_text = dialogs.text_dialog(title='Enter text to count', text='')
letter = input_alert('Counter', 'Enter a letter or number to count', '', 'Count', hide_cancel_button=False)

counter = Counter(count_text)
hud_alert(('There are %s total %s\'s') % (counter[letter], letter), 'success', 3)

