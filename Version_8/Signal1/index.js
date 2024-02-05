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
const scanner_no = 1; 


// Read linestatus
linestatus.on("value", function(snapshot) {
    var data = snapshot.val();
    var linestatus_from = data.from;
    var linestatus_msg = data.message;

    if (linestatus_msg == "END" && linestatus_from == scanner_no) {
        window.location.href = 'End_page.html';
    }
});

// Read signal
Signal.on("value", function(snapshot) {
    var data = snapshot.val();
    var signal = data.signal1;
    if (signal == scanner_no){
        window.location.href = 'Normal.html';
    }
    else{
        var text = "Please Wait!!"; 
        var tempDiv = document.getElementById("start");
        tempDiv.innerHTML = text;
    }
});

