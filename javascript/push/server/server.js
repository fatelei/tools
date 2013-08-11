// server

var app = require("express")();
var http = require("http");
var server = http.createServer(app);
var io = require("socket.io").listen(server);
var watch_event = require("./events");
var clientsMap = {};
var socketsMap = {};

io.sockets.on("connection", function (socket) {
    console.log(socket.id + ": connected");
    socket.on("ok", function (data) {
        clientsMap[data.id] = socket;
        socketsMap[socket.id] = data.id;
        function start_push() {
            watch_event.emit("push", clientsMap);
            setTimeout(function () {
                start_push();
            }, 1000);
        }
        start_push();
    });
    socket.on("disconnect", function () {
        delete clientsMap[socketsMap[socket.id]];
        delete socketsMap[socket.id];
    });
});



server.listen(8000);

//module.exports = server;


