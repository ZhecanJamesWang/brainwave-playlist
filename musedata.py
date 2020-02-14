import numpy as np
from pylsl import StreamInlet, resolve_byprop
import utils
import time
import socket

host = '192.168.your.IP'
port = 13

class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3


BUFFER_LENGTH = 5
EPOCH_LENGTH = 1
OVERLAP_LENGTH = 0.8
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH
INDEX_CHANNEL = [0]

if __name__ == "__main__":

    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()

    info = inlet.info()
    description = info.desc()

    fs = int(info.nominal_srate())
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
    filter_state = None  
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                              SHIFT_LENGTH + 1))

    band_buffer = np.zeros((n_win_test, 4))

    bwaves = [0 for i in range(10)]
    

    try:
        while True:

            eeg_data, timestamp = inlet.pull_chunk(
                timeout=0.1, max_samples=int(SHIFT_LENGTH * fs))

            ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]

            eeg_buffer, filter_state = utils.update_buffer(
                eeg_buffer, ch_data, notch=True,
                filter_state=filter_state)


            data_epoch = utils.get_last_data(eeg_buffer,
                                             EPOCH_LENGTH * fs)


            band_powers = utils.compute_band_powers(data_epoch, fs)
            band_buffer, _ = utils.update_buffer(band_buffer,
                                                 np.asarray([band_powers]))
            
            smooth_band_powers = np.mean(band_buffer, axis=0)
            beta_metric = smooth_band_powers[Band.Beta]

            print(beta_metric)
            bwaves.append(beta_metric)
            del bwaves[0]
            if bwaves[0]<bwaves[1]<bwaves[2]<bwaves[3]<bwaves[4]<bwaves[5]<bwaves[6]<bwaves[7]<bwaves[8]<bwaves[9] and sum(bwaves)>1:
                print(1)
                for i in range(1,9,1):
                    bwaves[i]=0
                winsound.PlaySound(music[musicnum], winsound.SND_ASYNC)
                musicnum+=1

                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((host,port))
                    msg = str(beta_metric)
                    client.send(msg.encode())
                    client.close()
                except:
                    pass
                
                if musicnum>len(music)-1:
                    musicnum=0     

    except KeyboardInterrupt:
        print('Program is closing')
