const video = document.querySelector('.player');
const canvas = document.querySelector('canvas');
const dummy = document.querySelector('.canvas-dummy');
const strip = document.querySelector('.strip');
//const snap = document.querySelector('.snap');
const newHeight = window.outerHeight
const newWidth = window.outerWidth


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
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const context = canvas.getContext('2d');
  
  return setInterval(() => {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
  }, 16);

}

function fullscreen() {
  canvas.width = newWidth;
  canvas.height = newHeight;
  if(dummy.webkitRequestFullScreen) {
    dummy.webkitRequestFullScreen();
  }
  else {
    dummy.mozRequestFullScreen();
  }         
}

getVideo();

video.addEventListener('canplay', paintToCanvas);
