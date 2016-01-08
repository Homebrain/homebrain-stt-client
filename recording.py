# Standard libraries
import time
import wave
import audioop
# PyPi packages
import alsaaudio as alsa
# Local packages
import transcription



filename = '/tmp/homebrain-stt-recording-temp.wav'
volume_threshold = 13000

# Records audio to a file until two seconds of 'silence' have passed
# Silence is defined as any audio below volume_threshold
def record_audio(pcm_in, data, silencetime=2):
    print('Recording. {} seconds of silence will commit the command.'.format(silencetime))
    buf = open(filename, 'w+b')
    time_start = time.time()
    vol = volume_threshold + 1
    while ((time.time() - time_start) < silencetime) or (vol > volume_threshold):
        if vol > volume_threshold:
            time_start = time.time()
        buf.write(data)
        l, data = pcm_in.read()
        vol = audioop.max(data, 2)
        time.sleep(.001)
    buf.close()

def get_pcm():
    # Prepare the CAPTURE device. It must use 16k Hz,
    # little endian, 16 bit signed integer
    pcm_in = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NONBLOCK, 'default')
    pcm_in.setchannels(1)
    pcm_in.setrate(16000)
    pcm_in.setformat(alsa.PCM_FORMAT_S16_LE)
    # Size of block of each read
    pcm_in.setperiodsize(512)

    return pcm_in

def passive_listen():
    result = listen("passive")
    if  result == "home brain":
        return True
    else:
        return False

def active_listen():
    return listen("active")

def listen(mode):
    pcm_in = get_pcm()

    silencetime = 0
    transcriber = None

    if mode == "passive":
        silencetime = 1
        transcriber=transcription.passive_transcribe
        timeout = float("inf")
    elif mode == "active":
        silencetime = 2
        transcriber=transcription.active_transcribe
        timeout = 10
    else:
        print("Invalid listen mode, must be either passive or active")
        return

    print("Waiting for {} input...".format(mode))

    start_time = time.time()
    while start_time+timeout > time.time():
        l, data = pcm_in.read()
        vol = audioop.max(data, 2)
        # enter recording state
        if vol > volume_threshold:
            record_audio(pcm_in, data, silencetime)
            transcribed = transcriber(filename)
            if transcribed and any(transcribed.hypstr):
                return transcribed.hypstr
            else:
                return None
