'use strict';

// Put variables in global scope to make them available to the browser console.
const video = document.querySelector('video');
//const fullscreenDummy = $(".fullscreen-dummy")
const canvas = window.canvas = document.querySelector('canvas');
canvas.width = 480;
canvas.height = 360;
const button = document.querySelector('button');
var timeleft = 5;
var numPhotos = 4;

//Socket Stuff
console.log(window.location)
var loc = window.location
var wsStart = 'ws://'
if (loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + loc.host + loc.pathname
var socket = new ReconnectingWebSocket(endpoint);
var newStrip = true;
var flash = document.getElementById("flash");


const constraints = {
  audio: false,
  video: {
      width: { min: 1024, ideal: 1280, max: 1920 },
      height: { min: 576, ideal: 720, max: 1080 },
  }
};
socket.onmessage = function(event){
    console.log("message", event)
    var msg = JSON.parse(event.data)
    if ("newURL" in msg){
        var myRedirect = msg["newURL"]
        window.location = myRedirect
    }
}

socket.onopen = function(e){
    console.log("open", e)
    $('.server-status').css({ 'color': 'green', });
    
}

socket.onerror = function(e){
    console.log("error", e)
}

socket.onclose = function(e){
    console.log("close", e)
    $('.server-status').css({ 'color': 'red', });
}

function flasher(){
  console.log("Flashy flashy!")
  $(".flash").hide().fadeIn(100);
  flash.style.opacity = "1";
  $(".flash").fadeOut(100);
}

function handleSuccess(stream) {
  window.stream = stream; // make stream available to browser console
  video.srcObject = stream;
}
    
function handleError(error) {
  console.log('navigator.MediaDevices.getUserMedia error: ', error.message, error.name);
}

function startCountdown() {
    if (newStrip === true) {
        createStrip();
    }
    //if(video.requestFullscreen) {
    //    video.requestFullscreen();
    //}
    //if(fullscreenDummy.requestFullscreen) {
    //    fullscreenDummy.requestFullscreen();
    //}
    document.getElementById("start").style.display= "none";
    document.getElementsByClassName("countdown")[0].style.display= "none";
    document.getElementsByClassName("countdown")[0].style.display= "block";
    document.getElementById("remaining").style.display= "block";
    timer();
};

function loadCamera(){ 
  navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);
  document.getElementById("vid").style.width= "100%";
  document.getElementById("start").style.display= "block";
  document.getElementById("booth").style.display= "grid";
  document.getElementById("camerabutt").style.display= "block";
  document.getElementById("camerabutt").style.display= "none";
  $(".top").hide()
}

function sendPhoto(dataURL) {
    var postDetails = {
        'imgBase64': dataURL,
    };
    socket.send(JSON.stringify(postDetails))
}

function createStrip() {
    console.log("Creating new strip.")
    console.log(newStrip)
    var postDetails = {
        'new_strip': newStrip,
    };
    newStrip = false;
    console.log(newStrip)
    socket.send(JSON.stringify(postDetails))
}

function snapPhoto() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    var dataURL = canvas.toDataURL();
    var postDetails = {
        'imgBase64': dataURL,
    };
    socket.send(JSON.stringify(postDetails))
}

function timer() {
    console.log("numPhotos", numPhotos);
    document.getElementById("remaining").innerHTML = "Photos Remaining: " + numPhotos;
    if (numPhotos > 0) {
        numPhotos -= 1
        photoTimer(() => timer())
    } else {
        stripComplete();
    }
}

function photoTimer() {
    document.getElementById("countdown").innerHTML = "Next photo in " + timeleft;
    timeleft -= 1;
    if(timeleft <= -1){
        document.getElementById("countdown").innerHTML = ""
        flasher(); 
        snapPhoto();
        timeleft = 5;
        timer()
    } else {
        var countAgain = setTimeout(function(){ photoTimer()}, 1000)
    }
}


function stripComplete() {
    var stripDone= true;
    var postDetails = {
        'strip_done': stripDone,
    };
    socket.send(JSON.stringify(postDetails))
}
