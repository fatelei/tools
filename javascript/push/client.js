//client

var io = require("socket.io-client");

var socket = io.connect("http://127.0.0.1:8000");

socket.on("connect", function () {
    console.log("connect server successfully");
    socket.emit("ok", {id: 3});
});

socket.on("notification", function (message) {
    console.log(message);
});