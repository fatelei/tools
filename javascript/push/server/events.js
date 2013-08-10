//事件处理

var EventEmitter = require("events").EventEmitter;
var events = new EventEmitter();

events.on("push", function (socket) {
    var watch_cb = require("./task");
    watch_cb(socket);
});

module.exports = events;
