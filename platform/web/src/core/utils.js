
const MIN = 60*1000;
const HOUR = 60*MIN;
const DAY = 24*HOUR;
const MONTH = 31*DAY;
const YEAR = 365*DAY;


export function timeRange(date){
  if (!date || !date.getTime) return "N/A"
  let _t = new Date().getTime() - date.getTime()
  if (!_t) return "N/A"
  if (_t < MIN) return "1分钟内"
  if (_t < HOUR) {
    return Math.ceil(_t/MIN)+"分钟前"
  }
  if (_t < DAY) return Math.ceil(_t/HOUR)+"小时前"
  if (_t < MONTH) return Math.ceil(_t/DAY)+"天前"
  if (_t < YEAR) return Math.ceil(_t/MONTH)+"月前"
  if (_t >= YEAR) return Math.ceil(_t/YEAR)+"年前"
}

export function timeFormat(times,flag){
  let date = new Date(times);
  if (!date) return "N/A";
  let year = date.getFullYear();
  let month = (date.getMonth()+1)>=10?(date.getMonth()+1):"0"+(date.getMonth()+1);
  let today = date.getDate()>=10?date.getDate():"0"+date.getDate();
  let hours = date.getHours()>=10?date.getHours():"0"+date.getHours();
  let minutes = date.getMinutes()>=10?date.getMinutes():"0"+date.getMinutes();
  let seconds = date.getSeconds()>=10?date.getSeconds():"0"+date.getSeconds();
  switch (flag){
    case "hh:mm:ss":
      return hours+":"+minutes+":"+seconds;
      break;
    default:
      return year+"-"+month+"-"+today+" "+hours+":"+minutes+":"+seconds
  }
}
