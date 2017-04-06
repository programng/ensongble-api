import os
import sys
import json
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from functools import partial
from multiprocessing import Pool

import librosa

pool = Pool()

def get_features(all_songs_for_movie, movie_name='unknown'):
    all_movie_names = [movie_name] * len(all_songs_for_movie)

    loaded_audio_for_movie = pool.map(librosa.load, all_songs_for_movie)
    audio_buffer_array = np.array([loaded_audio[0] for loaded_audio in loaded_audio_for_movie])
    X = audio_buffer_array
    df = pd.DataFrame(data={'movie': all_movie_names})

    spectral_rolloffs = pool.imap(librosa.feature.spectral_rolloff, X)
    spectral_rolloffs = list(spectral_rolloffs)
    df['spectral_rolloffs_mean'] = [spectral_rolloff.mean() for spectral_rolloff in spectral_rolloffs]
    df['spectral_rolloffs_std'] = [spectral_rolloff.std() for spectral_rolloff in spectral_rolloffs]


    spectral_centroids = pool.imap(librosa.feature.spectral_centroid, X)
    spectral_centroids = list(spectral_centroids)
    df['spectral_centroids_mean'] = [spectral_centroid.mean() for spectral_centroid in spectral_centroids]
    df['spectral_centroids_std'] = [spectral_centroid.std() for spectral_centroid in spectral_centroids]


    zero_crossing_rates = pool.imap(librosa.feature.zero_crossing_rate, X)
    zero_crossing_rates = list(zero_crossing_rates)
    df['zero_crossing_rates_mean'] = [zero_crossing_rate.mean() for zero_crossing_rate in zero_crossing_rates]
    df['zero_crossing_rates_std'] = [zero_crossing_rate.std() for zero_crossing_rate in zero_crossing_rates]

    partial_mfcc = partial(librosa.feature.mfcc, n_mfcc=5)
    mfccs = pool.imap(partial_mfcc, X)
    pool.close()
    pool.join()
    mfccs = list(mfccs)

    mfcc1s = [mfcc[0] for mfcc in mfccs]
    df['mfcc1_mean'] = [mfcc1.mean() for mfcc1 in mfcc1s]
    df['mfcc1_std'] = [mfcc1.std() for mfcc1 in mfcc1s]


    mfcc2s = [mfcc[1] for mfcc in mfccs]
    df['mfcc2_mean'] = [mfcc2.mean() for mfcc2 in mfcc2s]
    df['mfcc2_std'] = [mfcc2.std() for mfcc2 in mfcc2s]


    mfcc3s = [mfcc[2] for mfcc in mfccs]
    df['mfcc3_mean'] = [mfcc3.mean() for mfcc3 in mfcc3s]
    df['mfcc3_std'] = [mfcc3.std() for mfcc3 in mfcc3s]


    mfcc4s = [mfcc[3] for mfcc in mfccs]
    df['mfcc4_mean'] = [mfcc4.mean() for mfcc4 in mfcc4s]
    df['mfcc4_std'] = [mfcc4.std() for mfcc4 in mfcc4s]


    mfcc5s = [mfcc[4] for mfcc in mfccs]
    df['mfcc5_mean'] = [mfcc5.mean() for mfcc5 in mfcc5s]
    df['mfcc5_std'] = [mfcc5.std() for mfcc5 in mfcc5s]

    movies = df.pop('movie').values
    X = df.values

    return X

def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])

def main():
    lines = read_in()
    all_songs_for_movie = lines

    X = get_features(all_songs_for_movie)

    final_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'final_model.pkl')
    clf = joblib.load(final_model_path)
    predictions = clf.predict(X)

    print list(predictions)

if __name__ == '__main__':
    main()
