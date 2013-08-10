//client

var io = require("socket.io-client");

var socket = io.connect("http://localhost:8000");

socket.on("connect", function () {
    console.log("connect server successfully");
    socket.emit("ok", {id: 1});
});

socket.on("notification", function (message) {
    console.log(message);
});