// server

var app = require("express")();
var http = require("http");
var server = http.createServer(app);
var io = require("socket.io").listen(server);
var watch_event = require("./events");
var clients = {}

io.sockets.on("connection", function (socket) {
    console.log(socket.id + ": connected");
    socket.on("ok", function (data) {
        clients[data.id] = socket;
        console.log(clients);
        function start_push() {
            watch_event.emit("push", clients);
            setTimeout(function () {
                start_push();
            }, 1000);
        }
        start_push();
    });
    socket.on("disconnect", function () {
        for (var id in clients) {
            if (clients[id] === socket) {
                delete clients[id];
                break;
            }
        }
        console.log(clients);
    });
});




module.exports = server;


