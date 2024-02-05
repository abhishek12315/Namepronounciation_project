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

