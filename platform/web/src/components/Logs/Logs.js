
import React from 'react'
import ReactDOM from 'react-dom'
import * as Const from '../../constants'
import cookie from 'react-cookie'
import {timeFormat} from '../../core/utils';

export default class extends React.Component {
  constructor(){
    super();
    this.state = {
      items:[]
    }
  }
  shutByHand = false;
  xhr = null;
  start_time = "None";
  static propTypes = {
    logLabel: React.PropTypes.string,
  };
  fetchLogs(logLabel){
    let me = this;
    if (!logLabel) return console.info('fetch log with null label');
    var xhr = this.xhr;
    if (!xhr) return console.error('fetch log with null xhr!');
    xhr.open("post",`${Const.FETCH_URL.LOGS}/${logLabel}`,true)
    xhr.setRequestHeader("token", cookie.load("_at"))
    var offset = 0;
    xhr.onreadystatechange = function(){
      if (xhr.readyState == 2){

      }
      if (xhr.readyState == 3 && xhr.responseText) {
        var s = xhr.responseText.substring(offset);
        // console.log('log string :> ',s);
        if(s== "\n" || !s ) return
        try{
          var json = JSON.parse(s)
          console.log('log :> ',json);
          me.start_time = json.end_time;
          offset = xhr.responseText.length;
          if (json.status == 0){
            me.setState({
              items: [].concat(me.state.items).concat(json.result.logs_list)
            })
          } else {
            xhr.abort();
            console.info('fetch logs error: ',json)
          }
        } catch(e){
          // console.error('fetch logs error: ',e)
        }
      }
    };
    xhr.onabort = function(){
      console.info('fetch logs abort!!!!!!')
      if (!me.shutByHand){
        console.info('fetch logs reconnect .')
        setTimeout(function(){
          me.fetchLogs(logLabel)
        },100)
      } else {
        console.info('fetch logs abort by hand .')
      }
    };
    xhr.send(JSON.stringify({start_time:me.start_time}));
    return xhr
  }
  componentDidMount(){
    this.xhr = new XMLHttpRequest();
    this.fetchLogs(this.props.logLabel);
  }
  componentWillUnmount(){
    this.shutByHand = true;
    this.xhr.abort();
    this.xhr = null;
  }
  componentDidUpdate(){
    ReactDOM.findDOMNode(this.refs.list).scrollTop = 1000000
  }
  render(){
    this.state.items.sort(function(a,b){
      let t1 = a.time;//new Date(a.time).getTime();
      let t2 = b.time;//new Date(b.time).getTime();
      if (t1 < t2) return -1;
      if (t1 == t2) return 0;
      if (t1 > t2) return 1;
    })
    let _items = this.state.items;
    let items = _items.slice(_items.length-100).map((item,i)=>{
      return (
        <div key={i}>{timeFormat(item.log_time)} {item.log_info}</div>
      )
    })
    return (
      <pre ref="list" className="darken">
        {items}
      </pre>
    )
  }
}
