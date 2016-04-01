# https://gist.github.com/lukf/8982799

# -*- coding: utf-8 -*-
import console, datetime, json, os, sys, urllib, webbrowser
selected = "no"
console.clear()
# I moved 'dropboxlogin' into a sub folder so it doesn't clutter my main folder
sys.path += [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')]
import dropboxlogin # this code can be found here https://gist.github.com/4034526
# API app needs to be set up as root; set access_type to "dropbox".
dropbox_client = dropboxlogin.get_client() # auth
todayString=datetime.date.today().strftime('%Y-%m-%d')
# todayString = '2014-02-22'
path='/Apps/Reporter-App/' + todayString + '-reporter-export.json'

fmt = '''
|{}||
|:---|:---|
|Location|{}, {}|
|Battery|{}|
|Audio|{}|
|**QUESTIONS**||
{}
'''

outp = ''
for i in json.loads(dropbox_client.get_file(path).read())['snapshots']:
    # formatting responses
    responses=''
    for r in i['responses']:
        # formatting answeredOptions
        answered = '; '.join(r.get('answeredOptions', ''))
        if answered:
            answered += '; '
        answered += ''.join(r.get('numericResponse', ''))
        tokens = '; '.join(r.get('tokens', ''))
        if tokens:
            tokens += '; '
        # responses_strings
        qP = r.get('questionPrompt', '')
        locResp = r.get('locationResponse')
        l_t = locResp.get('text', '') if locResp else ''
        tR = r.get('textResponse', '')
        responses += '|{}|{}{}{}{}|\n'.format(qP, answered, tokens, l_t, tR)
    # extracted_strings
    battery   = i.get('battery', '')
    audio     = i.get('audio')
    audio_avg = audio.get('avg', '') if audio else ''
    l_time    = lp_name = lp_country = ''
    location  = i.get('location')
    if location:
        l_time = location.get('timestamp', '')
        if l_time:
            l_time = l_time.lstrip(todayString).lstrip('T')[:-5]
        placemark = location.get('placemark')
        if placemark:
            lp_name    = placemark.get('name', '')
            lp_country = placemark.get('country', '')

    # final formatting
    outp += fmt.format(l_time, lp_name, lp_country,
                       battery, audio_avg, responses)

dayone_entry = '# reporter entries\n{}\n***\n#reporter'.format(outp)
# User confirmation
print(dayone_entry)
if "preselect" in sys.argv:
	selected = "yes"
elif not raw_input('-- Press enter to import'):
	selected = "yes"
    # encode final entry
if selected == "yes":
	dayone_entry = urllib.quote(dayone_entry.encode('utf-8'))
	webbrowser.open('dayone://post?entry=' + dayone_entry)
sys.exit()
