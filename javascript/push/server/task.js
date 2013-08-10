//task queue

var bs = require("nodestalker");
var settings = require("./settings");


function process_job (clients, job, client, callback) {

    var data = JSON.parse(job.data);
    if (data.id in clients) {
        console.log("push noti");
        clients[data.id].emit("notification", data.msg);
        setTimeout(function() {
            callback(client, job);
        }, 1000);
    }
}

var del_cb = function (client, job) {
    client.deleteJob(job.id).onSuccess(function (del_msg) {
        console.log("deleted", job);
        console.log(del_msg);
        client.disconnect();
    });
    console.log("processed");
};

var watch_cb = function watch(clients) {
    var client = bs.Client(settings.config);
    client.watch(settings.watch_tube).onSuccess(function (data) {
        client.reserve().onSuccess(function (job) {
            process_job(clients, job, client, del_cb);
        });
    });
};


module.exports = watch_cb;

