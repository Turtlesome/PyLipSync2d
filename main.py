
import datetime
import math
import pprint
import speech_recognition as sr
import eng_to_ipa as phonetic
import numpy as np

import sound_analyzer as soana


phonetic_alphabet = {
    "1": ["silenzio"],
    "2": ["a", "i"],
    "3": ["æ", "e", "ɛ", "ə"],
    "4": ["f", "v", "ð", "θ"],
    "5": ["k", "ɪ", "tʃ", "j"],
    "6": ["l", "s", "z", "x", "g"],    
    "7": ["m", "p", "b"],
    "8": ["n", "ŋ", "d"],
    "9": ["ʊ"],
    "10": ["ɔ"],
    "11": ["o"],
    "12": ["ʃ", "t"],
    "14": ["u"],    
}


current_timestamp = datetime.datetime.now()
print(current_timestamp)

r = sr.Recognizer()

audio_file = fr"C:\Users\kaspr\OneDrive\Programming\Python\PyLipSync\Archiwum PyLipSync\odo_1.wav"

text = soana.speechtext(audio_file)

with open('transcription.txt', 'w', encoding='utf-8') as f:
    duration = soana.get_audio_duration(audio_file)
    
    phonetic_text = phonetic.convert(text)
    print("phonetic_text = ", phonetic_text)
    phonetic_text = phonetic_text.encode('utf8')
    phonetic_text = phonetic_text.decode('utf8')
    phonetic_text = phonetic_text.replace("ˈ", '') 
    phonetic_text = phonetic_text.replace(" ", '')
    phonetic_text = phonetic_text.replace("*", '')
    print(phonetic_text)

    y, sr = soana.load_audio_file(audio_file)
    onset_frames = soana.get_onset_frames(y, sr)
    onset_times = soana.get_onset_times(onset_frames, sr)
    
    print(len (phonetic_text))
    pprint.pprint(onset_frames)
    pprint.pprint(onset_times)

    # detect silence
    silence_times = soana.detect_silence(audio_file)

    onsets = []
    length_of_onset_times = len(onset_times)-1
    i = 1
    
    while len(onsets) < length_of_onset_times:
        onsets.append(round(onset_times[i] - onset_times[i-1], 2))
        i+=1
    print("onsets = ", onsets)

    onsets.insert(0, round(silence_times[0][1], 2))
    onsets.append(round(silence_times[-1][-1] - silence_times[-1][0], 2))
    print("onsets with silenzio = ", onsets)



    silence_times_1d = np.array([val for tup in silence_times for val in tup])

    array3 = []
    for value in onset_times:
        for low, high in silence_times[1:-1]:
            if low < value < high:
                break
        else:
            array3.append(value)

    # Concatenate the two arrays
    array3 = np.concatenate((array3, silence_times_1d))            

    array3 = [round(num, 3) for num in array3]
    array3.sort()
    
    import copy
    onsets_with_silences = copy.copy(array3)
    
    for tup in silence_times:
        for num in tup:
            if num in array3:
                index = array3.index(num)
                array3[index] = str(num) + "s"

    new_array = []

    for x in array3:
        if isinstance(x, np.float64):
            new_x = float(x)
        else:
            new_x = x
        new_array.append(new_x)

    
    onsets = []
    for i in range(len(new_array) - 1):
        x = new_array[i]
        y = new_array[i + 1]

        x = float(x.strip('s')) if isinstance(x, str) else x
        y = float(y.strip('s')) if isinstance(y, str) else y

        diff = round(y - x, 3)

        if isinstance(new_array[i], str) and isinstance(new_array[i + 1], str):
            onsets.append(f"{diff}s")
        else:
            onsets.append(diff)

    print("ONSETS =", onsets)
    
    
    for i in range(len(onsets_with_silences)-1):
        onsets_with_silences[i] = round(onsets_with_silences[i+1] - onsets_with_silences[i], 3)
    print("onsets_with_silences =", onsets_with_silences)

    del onsets_with_silences[-1]
    print("onsets_with_silences =", onsets_with_silences, len(onsets_with_silences))
    
    print("BREAKPOINT\n\n")
    
    print("ONSETS =", onsets, len(onsets))
    print("onsets_with_silences =", onsets_with_silences, len(onsets_with_silences))
    

    durations_s = []

    for x in onsets:
        new_x = math.floor(x * 25) if isinstance(x,(int,float)) else f"{round(float(x.strip('s')) * 25)}s"
        new_x = new_x if new_x != 0 else 1
        durations_s.append(new_x)

    print("durations_s =", durations_s)
    
    # Check if the last element is a string that ends with 's'
    if isinstance(durations_s[-1], str) and durations_s[-1].endswith('s'):
        # Remove the 's' character and convert the element to an integer
        durations_s[-1] = int(durations_s[-1].strip('s'))

    print(durations_s)
    
    with open('transcription.txt', 'w', encoding='utf-8') as f:
        # Zapisywanie cyferek do fonemów
        h = 0
        while h < len(durations_s):
            for i in range(len(phonetic_text)):
                for key, sign in phonetic_alphabet.items():
                    duration_of_vowel = durations_s[h]

                    if isinstance(duration_of_vowel, str) and duration_of_vowel.endswith('s'):
                        x = int(duration_of_vowel.strip('s'))
                        k = 0
                        while k != x:
                            f.write("1\n")
                            k += 1
                        h += 1

                    elif phonetic_text[i] in phonetic_alphabet[key]:
                        k = 0
                        while k != duration_of_vowel:
                            f.write(key)
                            f.write("\n")
                            k += 1
                        h += 1
                        if h >= len(durations_s):
                            break  
                if h >= len(durations_s):
                    break  
            if h >= len(durations_s):
                break  

        print("h =", h)
        
        q = 0
        while q != 5:
            f.write("1")
            f.write("\n")
            q+=1
        
        f.close()
    
print(len(onsets_with_silences))
print(phonetic_text)

current_timestamp = datetime.datetime.now()
print(current_timestamp)


