//GUI and Camera Variables
const video = document.querySelector('.player');
const canvas = document.querySelector('canvas');
const dummy = document.querySelector('.canvas-dummy');
const strip = document.querySelector('.strip');
const gui = document.getElementsByClassName('.gui');
var newHeight = window.outerHeight
var newWidth = window.outerWidth
dummy.style.width = newWidth;
dummy.style.height = newHeight;


//Booth Variables
var timeleft = 5;
var numPhotos = 1;
var newStrip = true;
var flash = document.getElementById("#flash");


//Socket Stuff
console.log(window.location)
var loc = window.location
var wsStart = 'ws://'
if (loc.protocol == 'https:'){
    wsStart = 'wss://'
}
var endpoint = wsStart + loc.host + loc.pathname
var socket = new ReconnectingWebSocket(endpoint);

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




const constraints = {
  audio: false,
  video: {
      width: { min: 1024, ideal: newWidth, max: 1920 },
      height: { min: 576, ideal: newHeight, max: 1080 },
  }
};

function handleSuccess(stream) {
  window.stream = stream; // make stream available to browser console
  video.srcObject = stream;
  video.play();
}

function handleError(error) {
  console.log('navigator.MediaDevices.getUserMedia error: ', error.message, error.name);
}


function getVideo() {
  navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);
}

function paintToCanvas() {
  //const width = video.videoWidth;
  //const height = video.videoHeight;
  //canvas.width = video.videoWidth;
  //canvas.height = video.videoHeight;
  canvas.width = dummy.offsetWidth;
  canvas.height = dummy.offsetHeight;
  //console.log("Video width: " + video.videoWidth);
  //console.log("Video height: " + video.videoHeight);
  //console.log("screen width: " + newWidth);
  //console.log("screen height: " + newHeight);
  //console.log("canvas width: " + canvas.width);
  //console.log("canvas height: " + canvas.height);
  //console.log("dummy width: " + dummy.offsetWidth);
  //console.log("dummy height: " + dummy.offsetHeight);
  //var vRatio = (canvas.height / video.videoHeight) * video.videoWidth;
  //console.log(vRatio);
  const context = canvas.getContext('2d');
  
  return setInterval(() => {
    //context.drawImage(video, 0, 0, canvas.width, canvas.height);
    //context.drawImage(video, 0, 0, newWidth, newHeight);
    //context.drawImage(video, 0, 0,);
    //context.drawImage(video, 0, 0, vRatio, newHeight);
    //context.drawImage(video, 0, 0, 0, 0, 0, 0, newWidth, newHeight);
    context.drawImage(video, 0, 0, dummy.offsetWidth, dummy.offsetHeight);
    let pixels = context.getImageData(0, 0, dummy.offsetWidth, dummy.offsetHeight);
    //pixels = redEffect(pixels);
    pixels = rgbSplit(pixels);
    context.globalAlpha = 0.3;
    context.putImageData(pixels, 0, 0)
  }, 16);

}

function fullscreen() {
  if(dummy.webkitRequestFullScreen) {
    dummy.webkitRequestFullScreen();
  }
  else {
    dummy.mozRequestFullScreen();
  }
  setTimeout(paintToCanvas, 500);
}


function toggleFullScreen() {
  if (!document.fullscreenElement) {
      fullscreen();
  } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.mozCancelFullScreen) { /* Firefox */
        document.mozCancelFullScreen();
      } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) { /* IE/Edge */
        document.msExitFullscreen();
      }
      paintToCanvas();
  }
}

function startCamera() {
  getVideo();
  var newHeight = window.outerHeight
  var newWidth = window.outerWidth
  canvas.width = newWidth;
  canvas.height = newHeight;
  var elements = document.getElementsByClassName('gui');
  for(var i=0; i<elements.length; i++) { 
    elements[i].style.visibility='visible';
  }
  document.querySelector('#camera-butt').style.visibility='hidden'; 
  setTimeout(fullscreen(), 500);
  //canvas.style.objectFit = "contain";
}

function queryDummy() {
  console.log("Dummy size: " + dummy.offsetWidth, dummy.offsetHeight);
}

function queryCanvas() {
  console.log("Canvas size: " + canvas.width, canvas.height);
}
video.addEventListener('canplay', paintToCanvas);

window.addEventListener("orientationchange", function() {
        var newHeight = window.outerHeight
        var newWidth = window.outerWidth
        fullscreen();
}, false);

//Booth Functions

function flasher(){
  console.log("Flashy flashy!")
  $(".flash").hide().fadeIn(100);
  $(".flash").fadeOut(100);
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

function startCountdown() {
    if (newStrip === true) {
        createStrip();
    }
    timer();
};

//Filters

function redEffect(pixels) {
  for(let i = 0; i < pixels.data.length; i+=4) {
    pixels.data[i + 0] = pixels.data[i + 0] - 100;
    pixels.data[i + 1] = pixels.data[i + 1] - 50;
    pixels.data[i + 2] = pixels.data[i + 2] * 0.5;
  }
  return pixels;
}

function rgbSplit(pixels) {
  for(let i = 0; i < pixels.data.length; i+=4) {
    pixels.data[i + 50] = pixels.data[i + 0];
    pixels.data[i + 100] = pixels.data[i + 1];
    pixels.data[i - 50] = pixels.data[i + 2];
  }
  return pixels;
}
