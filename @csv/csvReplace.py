# https://omz-forums.appspot.com/pythonista/post/6425415090438144
import clipboard, csv
data = clipboard.get()  #.replace(' ', '')
with open('csv_data.csv', 'w') as out_file:
    w = csv.writer(out_file)
    for line in data.splitlines():
        w.writerow(line.split(','))
