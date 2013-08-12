//client

var io = require("socket.io-client");

var socket = io.connect("http://api.notification.com");

socket.on("connect", function () {
    console.log("connect server successfully");
    socket.emit("push_service", {id: 1});
});

socket.on("notification", function (message) {
    console.log(message);
});

socket.on("disconnect", function () {
	console.log("server has gone away");
});