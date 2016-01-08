# Standard Packages
import os
# PyPi packages
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

modeldir = "./data/model"

passiveconfig = Decoder.default_config()
passiveconfig.set_string('-hmm', os.path.join(modeldir, 'en-us'))
passiveconfig.set_string('-lm', os.path.join(modeldir, 'en-us/en-us.lm.bin'))
passiveconfig.set_string('-logfn', "/dev/null")
passiveconfig.set_string('-dict', os.path.join(modeldir, 'homebrain.dict'))
passivedecoder = Decoder(passiveconfig)

activeconfig = Decoder.default_config()
activeconfig.set_string('-hmm', os.path.join(modeldir, 'en-us'))
activeconfig.set_string('-lm', os.path.join(modeldir, 'en-us/en-us.lm.bin'))
passiveconfig.set_string('-logfn', "/dev/null")
activeconfig.set_string('-dict', os.path.join(modeldir, 'commandterms.dict'))
activedecoder = Decoder(activeconfig)

def passive_transcribe(filename):
    return transcribe(filename, passivedecoder)

def active_transcribe(filename):
    return transcribe(filename, activedecoder)

def transcribe(filename, decoder):
    fp = open(filename, 'rb')
    data = fp.read()
    decoder.start_utt()
    decoder.process_raw(data, False, True)
    decoder.end_utt()
    fp.close()

    result = decoder.hyp()
    if result:
        print(result)
        print(result.best_score)
        print(result.prob)
        print('Transcribed: '+result.hypstr)
        return result
    else:
        return None
