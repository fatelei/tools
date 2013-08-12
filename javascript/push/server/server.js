// server

var app = require("express")();
var http = require("http");
var server = http.createServer(app);
var io = require("socket.io").listen(server);
var watch_event = require("./events");
var clientsMap = {};
var socketsMap = {};

io.configure("production", function () {
    io.enable("browser client minification");
    io.enable("browser client etag");
    io.enable("browser client gzip");
    io.set("log level", 1);

    io.set("transport", [
        "websocket",
        "flashsocket",
        "htmlfile",
        "xhr-polling",
        "jsonp-polling"
    ]);
});

io.configure("development", function () {
    io.set("transport", [
        "websocket"
    ]);
});

app.get("/", function (req, res) {
    res.sendfile(__dirname + "/index.html");
});

io.sockets.on("connection", function (socket) {
    socket.on("push_service", function (data) {
        clientsMap[data.id] = socket;
        socketsMap[socket.id] = data.id;
        function push_service () {
            watch_event.emit("push", clientsMap);
            setTimeout(function () {
                push_service();  
            }, 1000);
        }
        push_service();
    });
    socket.on("disconnect", function () {
        delete clientsMap[socketsMap[socket.id]];
        delete socketsMap[socket.id];
    });
});

server.listen(8000);

//module.exports = server;


