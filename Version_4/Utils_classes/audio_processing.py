import requests
from pydub import AudioSegment
import io
from google.cloud import storage
import sys
import os

class Anonymized_audio:
    def simple_encrypt(self, number):
        number_str = str(number)
        encrypted = ''
        secret_key ='mySecretKey'

        for i in range(len(number_str)):
            char_code = ord(number_str[i])
            key_char_code = ord(secret_key[i % len(secret_key)])
            encrypted_char_code = char_code ^ key_char_code

            # Ensure the encrypted character is alphanumeric (0-9, A-Z, a-z)
            encrypted_char_code = (encrypted_char_code % 62) + 48
            if encrypted_char_code > 57:
                encrypted_char_code += 7
            if encrypted_char_code > 90:
                encrypted_char_code += 6

            encrypted += chr(encrypted_char_code)

        return encrypted
    
    def anonymize_umid(self, umid):
        dec_val = int(umid)

        def decimalToBinary(n):
            return bin(n).replace("0b", "")

        val2 = "1101" #13
        str1 = ""

        str1 = decimalToBinary(dec_val)
        val1 = str1
        #print(str1)

        if (len(sys.argv) > 1):
            val1 = str(sys.argv[1])

        if (len(sys.argv) > 2):
            val2 = str(sys.argv[2])

        def showpoly(a):
            str1 = ""
            nobits = len(a)

            for x in range(0, nobits - 2):
                if (a[x] == '1'):
                    if (len(str1) == 0):
                        str1 += "x**" + str(nobits - x - 1)
                    else:
                        str1 += "+x**" + str(nobits - x - 1)

            if (a[nobits - 2] == '1'):
                if (len(str1) == 0):
                    str1 += "x"
                else:
                    str1 += "+x"

            if (a[nobits - 1] == '1'):
                str1 += "+1"

            #print(str1)

        def toList(x):
            l = []
            for i in range(0, len(x)):
                l.append(int(x[i]))
            return (l)

        def toString(x):
            str1 = ""
            for i in range(0, len(x)):
                str1 += str(x[i])
            return (str1)

        def divide(val1, val2):
            a = toList(val1)
            b = toList(val2)
            working = toString(val1) + "\n"

            res = ""
            addspace = ""

            while len(b) <= len(a) and a:
                if a[0] == 1:
                    del a[0]
                    for j in range(len(b) - 1):
                        a[j] ^= b[j + 1]
                    if (len(a) > 0):
                        working += addspace + toString(b) + "\n"
                        working += addspace + "-" * (len(b)) + "\n"
                        addspace += " "
                        working += addspace + toString(a) + "\n"
                        res += "1"
                else:
                    del a[0]
                    working += addspace + "0" * (len(b)) + "\n"
                    working += addspace + "-" * (len(b)) + "\n"
                    addspace += " "
                    working += addspace + toString(a) + "\n"
                    res += "0"

            #print("Result is\t", res)
            #print("Remainder is\t", toString(a))

            #print("Working is\t\n\n", res.rjust(len(val1)), "\n", )
            #print("-" * (len(val1)), "\n", working)

            return toString(a)

        #print("Binary form:\t", val1, " divided by ", val2)
        #print("")

        showpoly(val1)
        showpoly(val2)

        strzeros = ""
        strzeros = strzeros.zfill(len(val2) - 1)
        val3 = val1 + strzeros

        # print("")
        # print("Binary form (added zeros):\t", val3, " divided by ", val2)

        res = divide(val3, val2)
        final_val = val1 + res
        # print("Transmitted value is:\t", final_val)
        return final_val
    
    def upload_audio_locally(self, output_file, sound, audio_folder):

        if not output_file.endswith('.mp3'):
            output_file = os.path.splitext(output_file)[0] + '.mp3'

        # Normalize the audio at specific loudness.
        def match_target_amplitude(sound, target_dBFS):
            change_in_dBFS = target_dBFS - sound.dBFS
            return sound.apply_gain(change_in_dBFS)

        # Normalize the audio
        normalized_sound = match_target_amplitude(sound, -20.0)

        # Save the audio file locally
        output_path = os.path.join(audio_folder, output_file)
        normalized_sound.export(output_path, format='mp3')

        print(f"Audio file {output_file} saved locally at {output_path}.")

