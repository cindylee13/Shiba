var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');

var redis = require('redis');
var sub = redis.createClient();
var sub2 = redis.createClient();
//Subscribe to the Redis chat channel
sub.subscribe('price');
io.sockets.on('connection', function (socket) {
    //Grab message from Redis and send to client
    sub.on('message', function(channel, message){
    	//console.log(message.model);
        socket.send(message);
    });
});
