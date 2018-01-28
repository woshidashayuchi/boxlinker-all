var socket = io.connect('http://boxlinker.com:30003');

socket.on('notification' , function(msg){
    console.log(msg)
})

function send(){
    socket.emit('init',{namespace:'boxlinker'})
}


var $list = $("#list")
function longPolling(){
    var xhr = new XMLHttpRequest()
    // xhr.overrideMimeType('multipart/x-mixed-replace;boundary=frame')
    xhr.open("get","http://logs.boxlinker.com/api/v1.0/logs/polling/labels/py_auto_build",true)
    xhr.setRequestHeader("token","eyJ1aWQiOiAxNiwgInVzZXJfb3JhZyI6ICJhZG1pbiIsICJ0b2tlbmlkIjogImVhNTU3YzdlODFjODdiYzU4MjQ3ZDEyNCIsICJ1c2VyX25hbWUiOiAiYWRtaW4iLCAiZXhwaXJlcyI6IDE0NzUzMTc3MzQuNzkwODY2LCAidXNlcl9yb2xlIjogIjAiLCAidXNlcl9pcCI6ICIxMjcuMC4wLjEiLCAic2FsdCI6ICI0NGZlYWNmMmUxYTg3MmM5MWI4YjYxNjUiLCAiZW1haWwiOiAiaXQtMTExQGFsbC1yZWFjaC5jb20ifYfV7lTt94TQr0ljcnTxAmE=")
    // xhr.setRequestHeader("Content-type","multipart/x-mixed-replace; boundary=frame")
    // xhr.multipart = true;
    var offset = 0;
    xhr.onreadystatechange = function(){
        console.log(xhr.readyState,xhr.status,xhr.statusText,xhr.timeout);
        if (xhr.readyState == 3 && xhr.responseText) {
            var s = xhr.responseText.substring(offset);
            try{
                JSON.parse(s)
                $list.append("<li>"+s+"</li>")
                offset = xhr.responseText.length;
            } catch(e){

            }
        }
    }
    xhr.onabort = function(){
        setTimeout(longPolling,100)
    }

    xhr.send(null);
}

longPolling();