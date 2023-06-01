import struct
import sys
import os
import pandas as pd
import requests
import gdown
from pydub import AudioSegment
# Read CSV file into a pandas DataFrame
df = pd.read_excel('Students.xlsx')
print(df.columns)
# Specify the directory to save the downloaded files
download_dir = 'H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/Input_audio_files/UMID_audio'
temp_dir = 'H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/Input_audio_files/temp'
# Read Excel file into a pandas DataFrame
df = pd.read_excel('Students.xlsx')

# Loop through each row of the DataFrame
for index, row in df.iterrows():
    file_url = row['Link to audio file']  # Get the file URL from the 'File Link' column
    file_id = file_url.split('=')[1]
    modified_link = f'https://drive.google.com/uc?id={file_id}'
    #print(modified_link)# Extract the file ID from the URL
    output_file = f'{row["UM ID number"]}'  # Set the output file name
    output_path = os.path.join(temp_dir, output_file)
    final_output_path = os.path.join(download_dir, output_file)# Set the output file path
    gdown.download(modified_link, output_path, quiet=False)
    
    # Load the downloaded audio file
    sound = AudioSegment.from_file(output_path)
    # Convert the audio file to mp3 format
    if not final_output_path.endswith('.mp3'):
        final_output_path = os.path.splitext(final_output_path)[0] + '.mp3'
        sound.export(final_output_path, format='mp3')
    
    print(f'Downloaded and converted {row["UM ID number"]}')
    


#%%

#old_folder_path = 'H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/Input_audio_files'

#final_val = []

for filename in os.listdir(download_dir):
    if os.path.isfile(os.path.join(download_dir, filename)):
        name, extension = os.path.splitext(filename)
        print(name)
        dec_val = int((name))
        
    def decimalToBinary(n):
        return bin(n).replace("0b", "")
        
    
    val2="1101"
    str1 = ""
    
    str1 = decimalToBinary(dec_val)
    val1= str1
    print(str1)
    
    if (len(sys.argv)>1):
            val1=str(sys.argv[1])
    
    if (len(sys.argv)>2):
            val2=str(sys.argv[2])
    
    
    def showpoly(a):
    	str1 = ""
    	nobits = len(a)
    
    
    	for x in range (0,nobits-2):
    		if (a[x] == '1'):
    			if (len(str1)==0):
    				str1 +="x**"+str(nobits-x-1)	
    			else: 
    				str1 +="+x**"+str(nobits-x-1)
    
    	if (a[nobits-2] == '1'):
    		if (len(str1)==0):
    			str1 +="x"
    		else:
    			str1 +="+x"
    
    	if (a[nobits-1] == '1'):
    		str1 +="+1"
    
    	print (str1)
    	
    
    def toList(x):
    	l = []
    	for i in range (0,len(x)):
    		l.append(int(x[i]))
    	return (l)
    def toString(x):
    	str1 =""
    	for i in range (0,len(x)):
    		str1+=str(x[i])
    	return (str1)
    
    def divide(val1,val2):
    	a = toList(val1)
    	b = toList(val2)
    	working=toString(val1)+"\n"
    
    	res=""
    	addspace=""
    
    	while len(b) <= len(a) and a:
                if a[0] == 1:
                		del a[0]
                		for j in range(len(b)-1):
                    			a[j] ^= b[j+1]
                		if (len(a)>0):
                				working +=addspace+toString(b)+"\n"
                				working +=addspace+"-" * (len(b))+"\n"
                				addspace+=" "
                				working +=addspace+toString(a)+"\n"
                				res+= "1"
                else:
                    del a[0]
                    working +=addspace+"0" * (len(b))+"\n"
                    working +=addspace+"-" * (len(b))+"\n"
                    addspace+=" "
                    working +=addspace+toString(a)+"\n"
                    res+="0"
    
    
    	print ("Result is\t",res)
    	print ("Remainder is\t",toString(a))
    
    	print ("Working is\t\n\n",res.rjust(len(val1)),"\n",)
    	print ("-" * (len(val1)),"\n",working)
    
    	return toString(a)
    
    print ("Binary form:\t",val1," divided by ",val2)
    print ("")
    showpoly(val1)
    showpoly(val2)
    
    strzeros=""
    strzeros = strzeros.zfill(len(val2)-1)
    val3=val1+strzeros
    
    print ("")
    print ("Binary form (added zeros):\t",val3," divided by ",val2)
    
    res=divide(val3,val2)
    final_val = val1+res
    print ("Transmitted value is:\t",final_val)
    
    new_folder_path = 'H:/MS 2.0/UMDearborn/Lab_Projects/name_pronounciation/face recog/audio_files/'
    #new_prefix = final_val
    
    

    new_file_path = os.path.join(new_folder_path, final_val + extension)
    os.rename(os.path.join(download_dir, filename), new_file_path)
            
        
        
    
    
    