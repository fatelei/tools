// socket io client

var io = require("socket.io-client");

var socket = io.connect("http://localhost:8000");



socket.on("connect", function () {
    console.log("connect server successfully");
});

socket.on("message", function (message) {
    var start = new Date();
    console.log(message);
    var end = new Date();
    console.log((end - start)/1000);
});

