var EventEmitter = require("events").EventEmitter;
var events = new EventEmitter();

events.on("push", function (data) {
	console.log(data);
});

events.emit("push", "test");
