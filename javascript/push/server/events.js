//事件处理

var EventEmitter = require("events").EventEmitter;
var events = new EventEmitter();

events.on("push", function (clientsMap) {
    var watch_cb = require("./task");
    watch_cb(clientsMap);
});

module.exports = events;
