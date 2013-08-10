//socket io server

module.exports = start

function start () {
    var io = require("socket.io").listen(8000);
    var TaskQueue = require("tasks-queue");

    q = new TaskQueue();
    q.setMinTime(500);

    function add_task_queue() {
        q.pushTask("sample task", {data: "test"});
    }

    setInterval(add_task_queue, 100);


    io.sockets.on('connection', function (socket) {
        console.log("join in " + socket.id);
        q.on("sample task", function (jinn, data) {
            var q = jinn.getQueue();
            if (q.length() > 0) {
                socket.send(data.data);
            }
            jinn.done();
        });
        q.execute();
        socket.on("close", function () {
            socket.disconnect();
        });
    });
}




