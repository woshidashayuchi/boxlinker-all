var express = require('express')
var nodemailer = require('nodemailer')
var smtpPool = require('nodemailer-smtp-pool');
var isemail = require('isemail')
var messages = [];
// var transporter = nodemailer.createTransport(
//     smtpPool('smtps://service%40boxlinker.com:3xt-Tfe-cMa-Rrt@smtp.exmail.qq.com/?pool=true')
// );
var transporter = nodemailer.createTransport(smtpPool({
    host: 'smtp.exmail.qq.com',
    port: 25,
    auth: {
        user: 'service@boxlinker.com',
        pass: 'boxlinker'
    },
    // use up to 5 parallel connections
    maxConnections: 5,
    // do not send more than 10 messages per connection
    maxMessages: 10,
    // no not send more than 5 messages in a second
    rateLimit: 5
}));
transporter.verify(function(error, success) {
    if (error) {
        console.log(error);
    } else {
        console.log('Server is ready to take our messages');
    }
});
transporter.on('idle',function(){
    // send next messages from the pending queue
    console.log('email transporter idle.')
    sendLoop();
})
function sendLoop(){
    while(transporter.isIdle() && messages.length){
        // transporter.send(messages.shift());
        var msg = messages.shift();
        console.log("send to: %s", msg.to)
        transporter.sendMail(msg, function(error, info){
            if(error){
                return console.error(error)
            }
            console.log('Message sent: ' + info.response);
        });
    }
    setTimeout(sendLoop,500)
}
var app = express();
var bodyParser = require('body-parser');
app.use(bodyParser.json())

/**
 * @api {post} /v1/email/send 发送邮件
 * @apiName 发送邮件
 * @apiGroup Send Email
 *
 * @apiParam {String} to 接收方邮箱
 * @apiParam {String} title 标题
 * @apiParam {String} text 发送文本内容,html存在则覆盖
 * @apiParam {String} html 发送 html 内容
 *
 * @apiSuccess {String} status 0 OK
 *
 */
app.post('/v1/email/send',function(req,res){
    var to = req.body.to,
        title = req.body.title,
        text = req.body.text,
        html = req.body.html
        ;
    if (!isemail.validate(to)) return res.json({status:2,msg:"error receiver email format"})
    if (!(text||html)||!title) return res.json({status:1,msg:"no text/html/title provided"})
    var from = 'service@boxlinker.com';
    // setup e-mail data with unicode symbols
    var mailOptions = {
        from: from, // sender address
        to: to, // list of receivers
        subject: title, // Subject line
        text: text, // plaintext body
        html: html // html body
    };
    console.log('receive send: from %s - to %s', from,to)
    messages.push(mailOptions)
    res.json({status:0,msg:"messages length "+messages.length})
// send mail with defined transport object
})

var server = app.listen(3000, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Email app listening at http://%s:%s', host, port);
});


