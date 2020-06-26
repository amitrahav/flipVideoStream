var video = document.getElementById("normal");
var flip = document.getElementById("flipped");
var canvas = document.createElement("canvas");
    canvas.id = "canvas";
    document.body.appendChild(canvas);

    canvas.width  = 1078;
    canvas.height = 1508;

var can_con = canvas.getContext('2d');
let socket;

document.addEventListener("DOMContentLoaded", function(event) {


    socket = io.connect('http://' + document.domain + ':' + location.port + '/web', {
      reconnection: false
    });

    socket.on('connect', () => {
      console.log('Connected');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected');
    });

    socket.on('connect_error', (error) => {
      console.log('Connect error! ' + error);
    });

    socket.on('connect_timeout', (error) => {
      console.log('Connect timeout! ' + error);
    });

    socket.on('error', (error) => {
      console.log('Error! ' + error);
    });

    // Update image and text data based on incoming data messages
    socket.on('flipped', (flipped) => {
        var src = flipped.replace("b'", "").trim();
        document.getElementById("flipped").style.backgroundImage = 'url(' + encodeURI(src) + ')';
    });

});

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function (error) {
        console.error(error);
      console.log("Something went wrong!");
    }).finally(function(){
        setTimeout(function(){
        console.log(video.videoHeight)
        canvas.width  = video.offsetWidth;
        canvas.height = video.videoHeight;
    }, 100);
    });
}

function sendData(){
    var type = "image/png"
    var data = canvas.toDataURL(type);
    socket.emit('frame', data);
}

const FPS = 50;

setInterval(() => {
    can_con.drawImage(video, 0,0, video.offsetWidth, video.offsetHeight);
    sendData();
}, 10000/FPS)

