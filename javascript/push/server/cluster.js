//cluster

var cluster = require("cluster");
var app = require("./server");
var os = require("os");

//获取cpu数量
var numCPUs = os.cpus().length;
var workers = {};

if (cluster.isMaster) {
    cluster.on("online", function (worker) {
        console.log(worker.id +":online");
    });
    cluster.on("exit", function (worker, code, signal) {
        var exitCode = worker.process.exitCode;
        console.log("worker " + worker.process.pid + " died (" + exitCode + "). restarting...");
        cluster.fork();
    });
    for (var i = 0; i < numCPUs; i++) {
        cluster.fork();
    }
} else {
    app.listen(8000);
}

process.on("SIGTERM", function () {
    for (var worker in cluster.workers) {
        process.kill(worker.pid);
    }
    process.exit(0);
});


