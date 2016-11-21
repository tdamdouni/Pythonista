import os, requests

def download_weather_icons():
    fmt = 'Downloading {} from {} ...'
    for i in (1,2,3,4,9,10,11,13,50):
        filenames = ('{:02}d.png'.format(i), '{:02}n.png'.format(i))
        for filename in filenames:
            if os.path.exists(filename):
                continue
            url = 'http://openweathermap.org/img/w/' + filename
            with open(filename, 'w') as out_file:
                try:
                    print(fmt.format(filename, url))
                    out_file.write(requests.get(url).content)
                except requests.ConnectionError as e:
                    print('ConnectionError on {}: {}'.format(i ,e))
    print('Done.')

download_weather_icons()
