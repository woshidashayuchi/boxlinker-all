var express = require('express');
var ccap = require('ccap')

var http = require('http')
var uuid = require('uuid')
var randomstring = require("randomstring");
var redis_port = process.env.REDIS_PORT||6379;
var redis_host = process.env.REDIS_HOST||'127.0.0.1';
var redis = require("redis"),
    client = redis.createClient(redis_port,redis_host);

console.log('connect to redis: %s:%s',redis_host,redis_port);
client.on('error',function(){
    console.error('connect to redis %s:%s failed, retry...',redis_host,redis_port)
})
client.on('ready',function(){
    console.info('connect to redis %s:%s successfully.',redis_host,redis_port)
})

var captcha = ccap({

    width:170,//set width,default is 256

    height:60,//set height,default is 60

    offset:40,//set text spacing,default is 40

    quality:50,//set pic quality,default is 50

    generate:function(){//Custom the function to generate captcha text

        //generate captcha text here

        return randomstring.generate(4);//return the captcha text

    }

});

var app = express();

/**
 * @api {get} /v1/verify-code/check_code/:id?code={code} 验证用户输入的验证码
 * @apiName 验证验证码
 * @apiGroup verify code
 *
 * @apiParam {String} id 由前端生成的 uuid 用来标识验证码
 * @apiParam {String} code 用户输入的验证码字符串
 *
 * @apiSuccess {String} status 0 OK
 * @apiError {Number} status 1-no code provided, 2-wrong code
 *
 */
app.get('/v1/verify-code/check_code/:id',function(req,res){
    var code = req.query.code || "";
    if (!code || typeof code != 'string') {
        res.json({
            status:1,
            err:'no code'
        });
        return
    }
    client.get(req.params.id,function(err,value){
        if (typeof value != 'string' ||
            value.toLowerCase() !== code.toLowerCase()) {
            res.json({status:2,err:'wrong code'})
            return
        }
        res.json({status:0,err:null})
    })
})

/**
 * @api {get} /v1/verify-code/code?uuid={uuid} 获取验证码图片
 * @apiName 获取验证码图片
 * @apiGroup verify code
 *
 * @apiParam {String} uuid 由前端生成的 uuid 用来标识验证码
 *
 * @apiSuccessExample Success-Response:
 *     HTTP/1.1 200 OK
 *     base64 string ...
 *
 * @apiErrorExample Error-Response:
 *     HTTP/1.1 404 Not Found
 */
app.get('/v1/verify-code/code', function (req, res) {
    var ary = captcha.get();
    var txt = ary[0];

    var buf = ary[1];
    var id = req.query.uuid;
    if(!id) {
        res.sendStatus(404)
        return
    }
    client.set(id,txt,function(err, reply){
        if(reply == 'OK'){
            res.end(buf);
        }
        else
            res.sendStatus(404)
    })
    client.expire(id,60)
});

var server = app.listen(3000, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('Verify code app listening at http://%s:%s', host, port);
});
