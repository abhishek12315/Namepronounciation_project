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

// Reference to your Firebase Realtime Database
var database = firebase.database();

// Reference to the specific data you want to read from the database
var linestatus = database.ref("LineStatus");
var UMID = database.ref("UMID");
var Signal = database.ref("Signal");
const scanner_no = 2;

var text = "Line End - Please Wait.";
var text2 = "To start again scan 'START'"; 
var tempDiv = document.getElementById("end");
var tempDiv2 = document.getElementById("end2");
tempDiv.innerHTML = text;
tempDiv2.innerHTML = text2;


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
        if (inputData == "Start"){
            // Set Linestatus 
            message_data = {
                from: scanner_no, 
                message: "START"
            }
            linestatus.update(message_data).then(() => {console.log("message set linestatus")})
            window.location.href = 'index.html';
        }
    }
    }
}, 1000); // Adjust the interval as needed
