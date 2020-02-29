from __future__ import print_function
# https://gist.github.com/Dutcho/030e8cc7ecbcfd0a1e50

# Retrieved from https://gist.githubusercontent.com/omz/9882a00abf59c6009fa4/raw/139afad596c6d46f2f104b16120eefbb36e9960c/Audio%2520Recorder.py on Sat 26-Dec-2015 07:22:53
# Olaf, 26 Dec 2015, updated to use objc_util instead of ctypes; also removed seemingly superfluous AVAudioSession

import objc_util, os 

def main():
    NSMutableDictionary = objc_util.ObjCClass('NSMutableDictionary')
    settings = NSMutableDictionary.dictionary()
    kAudioFormatMPEG4AAC = 1633772320
    settings.setObject_forKey_(kAudioFormatMPEG4AAC, 'AVFormatIDKey')
    settings.setObject_forKey_(44100.0, 'AVSampleRateKey')
    settings.setObject_forKey_(2, 'AVNumberOfChannelsKey')

    AVAudioRecorder = objc_util.ObjCClass('AVAudioRecorder')
    recorder = AVAudioRecorder.alloc()
    output_path = os.path.abspath('Recording.m4a')
    out_url = objc_util.nsurl(output_path)
    recorder = recorder.initWithURL_settings_error_(out_url, settings, None)
    started_recording = recorder.record()

    if started_recording:
        print('Recording started, press the "stop script" button to end recording...')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Stopping...')
        recorder.stop()
        recorder.release()
        print('Stopped recording.')
        import console
        console.quicklook(os.path.abspath('Recording.m4a'))

if __name__ == '__main__':
    main()
