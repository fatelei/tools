//task queue

var bs = require("nodestalker");
var settings = require("./settings");


function process_job (clientsMap, job, client, callback) {
    var data = JSON.parse(job.data);
    console.log(data);
    if (data.id in clientsMap) {
        clientsMap[data.id].emit("notification", data.msg);
        callback(client, job);
        return;
    } else {
        if (data.id) {
            client.release(job.id).onSuccess(function (data) {
                client.disconnect();
                return;
            });
        } else {
            callback(client, job);
            return;
        }
    }
    client.disconnect();
}

var del_cb = function (client, job) {
    client.deleteJob(job.id).onSuccess(function (del_msg) {
        console.log("deleted", job);
        console.log(del_msg);
        client.disconnect();
    });
    console.log("processed");
};

var watch_cb = function watch(clientsMap) {
    var client = bs.Client(settings.config);
    client.watch(settings.watch_tube).onSuccess(function (data) {
        client.reserve().onSuccess(function (job) {
            process_job(clientsMap, job, client, del_cb);
        });
    });
};


module.exports = watch_cb;

