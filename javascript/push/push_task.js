//push task

var bs = require("nodestalker");
var client = bs.Client();

function push_task() {
	client.use("notification").onSuccess(function (data) {
		client.put(JSON.stringify({id: 3, msg: "hello world"})).onSuccess(function (data) {
			console.log(data);
			client.disconnect();
		});
	});
}

push_task();

