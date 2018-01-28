var express = require('express');
var app = express();
var server = require('http').Server(app);

var rabbitmq_url = process.env.RABBITMQ_URL;
var rabbitmq_port = process.env.RABBITMQ_PORT;

if (!rabbitmq_url || !rabbitmq_port){
    console.error('need env RABBITMQ_URL and RABBITMQ_PORT');
    return;
}

var cookieParser = require('cookie-parser');
server.listen(8080,function(){
    console.log('listen for :8080');
})

app.use(express.static('static'))
app.use(cookieParser());

var Server = require('socket.io');
var io = new Server(8081);

var usersMap = {};

io.on('connection', function(socket){
    console.log('on connection');
    socket.on('init',function(data){
        if(!data.namespace) return;
        console.log(`user ${data.namespace} connected`);
        usersMap[data.namespace] = socket.id;
    });

    socket.on('disconnect', function(){
        delete usersMap[socket.id];
        console.log(`user ${usersMap[socket.id]} disconnected`);
        console.log('on disconnect');
    })
})

io.on('error',function(){
    console.error('on error');
})


var amqp = require('amqp')
console.log('==>>>',rabbitmq_url,rabbitmq_port);
var connection = amqp.createConnection({
    host:rabbitmq_url,
    port:rabbitmq_port
})

connection.on('error',function(e){
    console.error('Error from amqp: ',e)
})
var queue_name = 'build_code_exchang_debug'
connection.on('ready',function(){
    console.log('amq ready.');
    var src = connection.exchange('build_code_debug',function (exchange) {
        console.log('Exchange ' + exchange.name + ' is open');
    });

    // connection.queue(queue_name,{
    //     autoDelete: false,
    //     passive: false,
    //     durable: false
    // },function(q){
    //     console.log(queue_name+' ready.');
    //     q.bind(exc)
    //     q.subscribe(function(message){
    //         message = message.data.toString('utf-8')
    //         try{
    //             message = JSON.parse(message)
    //         }catch(e){
    //             console.log("parse error :> ", message);
    //             return
    //         }
    //         console.log('message -> ',message);
    //         var namespace = message.user_name;
    //         if (!usersMap[namespace]) {
    //             console.log('namespace not found in ws sockets');
    //             return;
    //         }
    //         var socket = io.sockets.sockets[usersMap[namespace]]
    //         if (!socket) {
    //             console.log('socket not found in ws sockets');
    //             return;
    //         }
    //         socket.emit('notification',message);
    //     })
    // })
})