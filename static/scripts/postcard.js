const video = document.querySelector('.player');
const canvas = document.querySelector('canvas');
const dummy = document.querySelector('.canvas-dummy');
const strip = document.querySelector('.strip');
//const snap = document.querySelector('.snap');
var newHeight = window.outerHeight
var newWidth = window.outerWidth
dummy.style.width = newWidth;
dummy.style.height = newHeight;

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
  console.log("Video width: " + video.videoWidth);
  console.log("Video height: " + video.videoHeight);
  console.log("screen width: " + newWidth);
  console.log("screen height: " + newHeight);
  console.log("canvas width: " + canvas.width);
  console.log("canvas height: " + canvas.height);
  console.log("dummy width: " + dummy.offsetWidth);
  console.log("dummy height: " + dummy.offsetHeight);
  //var vRatio = (canvas.height / video.videoHeight) * video.videoWidth;
  //console.log(vRatio);
  const context = canvas.getContext('2d');
  
  return setInterval(() => {
    //context.drawImage(video, 0, 0, canvas.width, canvas.height);
    //context.drawImage(video, 0, 0, newWidth, newHeight);
    context.drawImage(video, 0, 0, dummy.offsetWidth, dummy.offsetHeight);
    //context.drawImage(video, 0, 0,);
    //context.drawImage(video, 0, 0, vRatio, newHeight);
    //context.drawImage(video, 0, 0, 0, 0, 0, 0, newWidth, newHeight);
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

function exitFull() {
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

function startCamera() {
  getVideo();
  var newHeight = window.outerHeight
  var newWidth = window.outerWidth
  canvas.width = newWidth;
  canvas.height = newHeight;
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
