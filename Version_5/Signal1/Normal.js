// Initialize Firebase with your Firebase project configuration
var firebaseConfig = {
    apiKey: "AIzaSyBBMP0odqYWBhShPY7rdut5tzDw2m_zddY",
    authDomain: "name-pro-ad9ab.firebaseapp.com",
    databaseURL: "https://name-pro-ad9ab-default-rtdb.firebaseio.com",
    projectId: "name-pro-ad9ab",
    storageBucket: "name-pro-ad9ab.appspot.com",
    messagingSenderId: "1083966951154",
    appId: "1:1083966951154:web:8a3e857e50ecf486e9ca6b",
    measurementId: "G-S1HX60F3G9"
  };

firebase.initializeApp(firebaseConfig);

function simpleEncrypt(number) {
    const numberStr = number.toString();
    const alphanumericCharacters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    let encrypted = '';
    const secretKey = 'mySecretKey';
  
    for (let i = 0; i < numberStr.length; i++) {
      const charCode = numberStr.charCodeAt(i);
      const keyCharCode = secretKey.charCodeAt(i % secretKey.length);
      const encryptedCharCode = charCode ^ keyCharCode;
      
      // Ensure the encrypted character is alphanumeric
      const encryptedChar = alphanumericCharacters.charAt(encryptedCharCode % 62);
      
      encrypted += encryptedChar;
    }
    encrypted += ".mp3";
    return encrypted;
  }

function goahead(){
    var text = "Go ahead, scan QR code!!"; 
    var tempDiv = document.getElementById("start");
    tempDiv.innerHTML = text;
    // Show the GIF
    var gifImage = document.getElementById("gifImage");
    gifImage.src = "qrcode_scan.gif"; 
    gifImage.style.display = "block";
}
  
// Reference to your Firebase Realtime Database
var database = firebase.database();

// Reference to the specific data you want to read from the database
var linestatus = database.ref("LineStatus");
var UMID = database.ref("UMID");
var Signal = database.ref("Signal");
const scanner_no = 1; 

goahead();

const inputField = document.getElementById('inputField');
var scannedValues = '';
var inputData = "";
// Add an event listener for the 'input' event to detect changes in the input field
inputField.addEventListener('input', handleBarcodeScan);

function handleBarcodeScan(event) {
    const scannedValue = event.target.value.trim();

    if (scannedValue !== '') {
    scannedValues += scannedValue + ''; // Append the scanned value
    event.target.value = ''; // Clear the input field
    }
}

// Add an event listener for the 'keydown' event to prevent form submission on Enter
inputField.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
    event.preventDefault();
    }
});


// Log all scanned values to the console periodically (e.g., every 5 seconds)
setInterval(function () {
    if (scannedValues !== '') {
    console.log('Scanned Values:', scannedValues.trim());
    var inputData = scannedValues.trim()
    scannedValues = ''; // Clear the scanned values
    if (inputData.trim() !== ""){
        if (inputData.length == 8){
            // Set Linestatus 
            message_data = {
                from: scanner_no, 
                message: inputData,
                audio_file: simpleEncrypt(inputData)
            }
            UMID.update(message_data).then(() => {console.log("message set UMID")})
            signal_data = {
                signal1: 2
            }
            Signal.update(signal_data).then(() => {console.log("Signal Set to 2")})
            window.location.href = 'index.html';
        }
        else if (inputData == "End"){
            // Set Linestatus 
            message_data = {
                from: scanner_no, 
                message: "END"
            }
            linestatus.update(message_data).then(() => {console.log("message set linestatus")})
            message_data = {
                from: scanner_no, 
                message: 0,
                audio_file: 0
            }
            UMID.update(message_data).then(() => {console.log("END clear msg set UMID")});
            window.location.href = 'End_page.html';
        }
        else {
            var gifImage = document.getElementById("gifImage");
            gifImage.src = "try_again_GIF.gif"; 
            gifImage.style.display = "block";
            var text = "Invalid!!"; 
            var tempDiv = document.getElementById("start");
            tempDiv.innerHTML = text;
            message_data = {
                from: scanner_no, 
                message: 0,
                audio_file: 0
            }
            UMID.update(message_data).then(() => {console.log("Invalid clear message set UMID")});
            setTimeout(function() {
                goahead();
            }, 2000);
        }
    }
    }
}, 1000); // Adjust the interval as needed
