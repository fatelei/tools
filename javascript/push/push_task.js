//push task

var bs = require("nodestalker");
var client = bs.Client();

var id = parseInt(process.argv[2]);

console.log(id);

function push_task() {
	client.use("notification").onSuccess(function (data) {
		client.put(JSON.stringify({id: 1, msg: "hello world"})).onSuccess(function (data) {
			console.log(data);
			client.disconnect();
		});
	});
}

push_task();

