# importing the libraries
import cv2
import numpy as np
import csv 
import requests


#UMID
UMID = ""
Name = ""
College = ""
Major = ""
#qprint(UMID.UMID)

def find_content_in_csv(file_path, content):
    """
    Searches for the given content in the CSV file specified by file_path.
    Returns True if the content is found, otherwise returns False.
    """
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if content in row:
                return True
    return False


# Setup camera
cap = cv2.VideoCapture(1)

#Converting cap resolution
cap.set(3, 1080)
cap.set(4, 720)

# Read logo and resize
logo = cv2.imread('C:/Users/palla/Desktop/namepron/From_Aditya/source_code/Banner.jpg')
#cv2.imshow("logo",logo)

#Setting logo resolution 
size_1 = 1280
size_2 = 175
logo = cv2.resize(logo, (size_1, size_2))
# cv2.imshow("sample", logo)

# Create a mask of logo
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    #Getting the data from cloud 
    msg=requests.get("https://api.thingspeak.com/channels/2059263/fields/1")
    msg=msg.json()['feeds'][-1]['field1']
    print("\nThe Message sent was: \n\n"+str(msg))
    
    UMID = str(msg)[1:]   #UMID.UMID
    print(UMID)
    # Region of Image (ROI), where we want to insert logo
    roi = frame[545:size_2+545, 0:size_1]
    roi = cv2.resize(roi, (mask.shape[1], mask.shape[0]))
    # Set an index of where the mask is
    roi[np.where(mask)] = 0
    roi += logo
    
    #extracting the student data
    with open('Students.csv') as file_obj:
          
        # Create reader object by passing the file 
        # object to reader method
        reader_obj = csv.reader(file_obj)
        
        if find_content_in_csv('Students.csv', UMID):
            
            # Iterate over each row in the csv 
            # file using reader object
           
            for row in reader_obj:
                if row[1] == UMID:
                    Name = row[2]
                    College = row[6]
                    Major = row[5]
                    
                    
                    #print("Name: {}".format(row[0]))
                    #("College:{}".format(row[4]))
                    #print("Major:{}".format(row[3]))
        else:
            Name = ''
            College = ''
            Major = ''
            

    #Setting text features
    name = Name             #"Abdul Kareem Shaik"
    name_org = (160, 605)

    col = College          #"College of Engineering and Computer Science"
    col_org = (160, 640)

    major = Major          #"MS in Robotics Engineering"
    major_org = (160, 675)

    font = cv2.FONT_HERSHEY_DUPLEX
    fontScale = 1
    color = (255, 255, 255)
    thickness = 2
    
    #Name
    cv2.putText(frame, name, name_org, font, fontScale,color, thickness, cv2.LINE_AA, False)
    #College
    cv2.putText(frame, col, col_org, font, fontScale,color, thickness, cv2.LINE_AA, False)
    #Major
    cv2.putText(frame, major, major_org, font, fontScale,color, thickness, cv2.LINE_AA, False)
    
    #Converting normal window size to full screen 
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) == ord('q'):
        cv2.imwrite('Frame.png', frame)
        break
cap.release()
cv2.destroyAllWindows()


# When everything done, release the capture

