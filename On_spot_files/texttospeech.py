from google.cloud import texttospeech
from google.oauth2 import service_account
from google.cloud import storage
import sys
#%%
class TTS:
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path
        
    def anonymize_umid(self, umid):
        dec_val = int(umid)
    
        def decimalToBinary(n):
            return bin(n).replace("0b", "")
    
        val2 = "1101"
        str1 = ""
    
        str1 = decimalToBinary(dec_val)
        val1 = str1
        # print(str1)
    
        if len(sys.argv) > 1:
            val1 = str(sys.argv[1])
    
        if len(sys.argv) > 2:
            val2 = str(sys.argv[2])
    
        def showpoly(a):
            str1 = ""
            nobits = len(a)
    
            for x in range(0, nobits - 2):
                if a[x] == '1':
                    if len(str1) == 0:
                        str1 += "x**" + str(nobits - x - 1)
                    else:
                        str1 += "+x**" + str(nobits - x - 1)
    
            if a[nobits - 2] == '1':
                if len(str1) == 0:
                    str1 += "x"
                else:
                    str1 += "+x"
    
            if a[nobits - 1] == '1':
                str1 += "+1"
    
            # print(str1)
    
        def toList(x):
            l = []
            for i in range(0, len(x)):
                l.append(int(x[i]))
            return l
    
        def toString(x):
            str1 = ""
            for i in range(0, len(x)):
                str1 += str(x[i])
            return str1
    
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
                    if len(a) > 0:
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
    
            # print("Result is\t", res)
            # print("Remainder is\t", toString(a))
    
            # print("Working is\t\n\n", res.rjust(len(val1)), "\n", )
            # print("-" * (len(val1)), "\n", working)
    
            return toString(a)
    
        # print("Binary form:\t", val1, " divided by ", val2)
        # print("")
    
        showpoly(val1)
        showpoly(val2)
    
        strzeros = ""
        strzeros = strzeros.zfill(len(val2) - 1)
        val3 = val1 + strzeros
    
        # print("")
        # print("Binary form (added zeros):\t", val3, " divided by ", val2)
    
        res = divide(val3, val2)
        final_val = val1 + res
        print("Transmitted value is:\t", final_val)
        return final_val
    
    def synthesize_text(self, name, lang_code):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        client = texttospeech.TextToSpeechClient(credentials=credentials)
    
        synthesis_input = texttospeech.SynthesisInput(text=name)
    
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang_code,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
    
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
    
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        return response
        
    def store_audio_in_gcs(self, bucket_name, folder_name, output_file, response):
        storage_client = storage.Client.from_service_account_json(self.credentials_path)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f'{folder_name}/{output_file}.mp3')
        blob.upload_from_string(response.audio_content, content_type='audio/mpeg')
        print(f"Audio file '{output_file}.mp3' uploaded to GCS under the folder '{folder_name}'.")
