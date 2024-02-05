import requests
import base64
import os
import json
import io
from pydub import AudioSegment

class namecoachapi():
    def __init__(self):
        client_id = 'JON87hLdC5tQMvXgHlHSXR9o6A40JvRHIgmvbqN5XnjljZck'
        client_secret = '1EyHxADNB7KZjCu5XHSeAzrM5n2zCiCQtDOtWOhGzoGwh5AI6AL6F2TXXoBSHGu5'

        token_url = 'https://gw.api.it.umich.edu/um/oauth2/token'

        # Combine the client ID and client secret
        credentials = f"{client_id}:{client_secret}"

        # Base64 encode the credentials
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        # Construct the Authorization header
        authorization_header = f"Basic {encoded_credentials}"

        # Prepare the request parameters
        payload = {
            'grant_type': 'client_credentials',
            'scope': 'namecoach'
        }

        headers = {
            'Authorization': authorization_header,
            'Accept': 'application/json'
        }

        response = requests.post(token_url, data=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access_token')
            # print(self.access_token)
        else:
            print('Failed to retrieve access token')

    def access_audio_files(self, email):
      # id_or_email = ['adityabe@umich.edu','sweraka@umich.edu']
      requestUrl = "https://gw.api.it.umich.edu/um/inst/participants/{id_or_email}"
      url = requestUrl.format(id_or_email=email)
      # print(url)
      requestHeaders = {
          "Authorization": f"Bearer {self.access_token}",
          "Accept": "application/json"
      }

      response = requests.get(url, headers=requestHeaders)
      if response.status_code == 200:
        student_details = json.loads(response.text)
        recording_link = student_details["participant"]["recording_link"]
        return recording_link
    #   else:
    #       return None
    #   print(type(recording_link))

    #   if recording_link is None:
    #       return None    # Write something to handle return condition later

    #   # Send a GET request to download the audio file
    #   audio_link = requests.get(recording_link)

    #   if audio_link.status_code == 200:
    #       # Get the filename from the URL
    #       filename = recording_link.split("/")[-1].split("?")[0]

    #     ###### This part of code to save the namecoach audio files locally #####
    #     # # Directory to save the audio file
    #     #   save_directory = os.path.join(os.path.dirname(__file__), "../Temp_Namecoach_audio")
    #     # # Construct the file path
    #     #   file_path = os.path.join(save_directory, filename)
        
    #     # # Save the Namecoach audio files locally 
    #     #   with open(file_path, "wb") as file:
    #     #       file.write(audio_link.content)

    #     #   print(f"Audio file '{filename}' downloaded and saved at '{file_path}'.")
          
    #       audio_content = io.BytesIO(audio_link.content)
    #       sound = AudioSegment.from_file(audio_content)
    #       return sound
    #   else:
    #       print("Failed to download the audio file.")


