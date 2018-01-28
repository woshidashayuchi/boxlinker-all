
import React,{ PropTypes,Component } from 'react';
import ReactDOM from 'react-dom'
import * as Const from '../../constants';
import fetch from 'isomorphic-fetch';
import {timeFormat} from '../../core/utils';
import {isLoadingAction} from "../../actions/header";

class BtnGroup extends  Component{
  static propTypes = {
    prop:React.PropTypes.array,
    type:React.PropTypes.string,
    onSelect:React.PropTypes.func,
    activeKey:React.PropTypes.number
  };
  constructor(props){
    super(props);
    this.state = {
      active:this.props.activeKey
    }
  }
  handelSelect(i){
    this.setState({
      active:i
    });
    let time = "";
    switch (i){
      case 0:
        time = "60m";
        break;
      case 1:
        time = "360m";
        break;
      case 2:
        time = "1440m";
        break;
      default :
        time = "60m"
    }
    this.props.onSelect(time);
  }
  render(){
    let html = this.props.prop.map((item,i) => {
      return <button key = {i} className={`btn btn-default btn-xs ${this.state.active == i?"btn-primary":""}`}
                     onClick={this.handelSelect.bind(this,i)}
      >{item}</button>
    });
    return(
      <div className="btnGroup">
        {html}
      </div>
    )
  }

}

const ReactHighcharts = require('react-highcharts');

export default class extends React.Component {
  static contextTypes = {
    store:React.PropTypes.object
  };
  constructor(props){
    super(props);
    this.state = {
      data:{xAxis:[],series:[]},
      payload:this.props.payload,
      time:"60m"
    }
  }
  static propTypes = {
    payload:React.PropTypes.object,
    color:React.PropTypes.array,
    legend:React.PropTypes.bool,
    valueSuffix:React.PropTypes.string
  };
  fetchGetMonitorDataAction(data,time_long) {
    let myInit = {
      method : "GET",
      headers:{token:localStorage.getItem("_at")},
    };
    let my = this;
    this.context.store.dispatch(isLoadingAction(true));
    let url = Const.FETCH_URL.GET_SERVICE_MONITOR+"/"+data.userName+"/pods/"+data.pod_name+"/metrics/"+data.type+
      "?time_long="+time_long;
      fetch(url,myInit)
        .then(response => response.json())
        .then(json => {
          console.log(json,data.type);
          my.context.store.dispatch(isLoadingAction(false));
          if(json.status == 0){
            let monitor = {};
            let xAxis = [];
            let seriesName = [];
            let seriesValue = [];
            json.result.map((item,i) => {
              if(!item.name){return false}else {
                if (data.type == "memory") {
                  if (i == 2) {
                    seriesName.push(item.name.split("/")[1]);
                    seriesValue.push(item.value);
                  }
                } else if (data.type == "cpu") {
                  if (i == 1) {
                    seriesName.push(item.name.split("/")[1]);
                    seriesValue.push(item.value);
                  }
                } else {
                  seriesName.push(item.name.split("/")[1]);
                  seriesValue.push(item.value);
                }
              }
            });
            let series = seriesValue.map((item,i) => {
              let newSeries = {};
              let arr = [];
              seriesValue[i].map((obj,j) => {
                xAxis.push(timeFormat(obj[0], "hh:mm:ss"));
                if(j!=0) {
                  let number = obj[1] ? obj[1] / my.props.divisor : 0;
                  arr.push(Number(number.toFixed(2)));
                }
              });
              if(data.type == "network"){
                newSeries.name = seriesName[i]=="rx_rate"?"入网":"出网";
              }else{
                newSeries.name = seriesName[i]
              }

              newSeries.data = arr;
              return newSeries;
            });
            monitor.xAxis = xAxis;
            monitor.series = series;
            my.setState({
              data:monitor
            })
          }
        })
  }

  componentDidMount(){
    let data = this.props.payload ;
    this.fetchGetMonitorDataAction(data,this.state.time);
    let my = this;
    this.myTime = setInterval(function(){
      my.fetchGetMonitorDataAction(data,my.state.time);
    },60000)
  }
  componentWillUnmount(){
    clearInterval(this.myTime);
  }
  changeTime(time){
    let data = this.props.payload ;
    this.setState({
      time:time
    });
    let my = this;
    setTimeout(function(){
      my.fetchGetMonitorDataAction(data,my.state.time);
    },200);
  }
  render(){
    let my = this;
    const config = {
      chart: {
        type: 'area',
        animation: false
      },
      credits:{
        enable: false
      },
      xAxis: {
        categories: my.state.data.xAxis,
      },
      yAxis:{
        title: {//纵轴标题
          text: ''
        },
        labels: {
          formatter: function () {
            return this.value + my.props.valueSuffix;
          }
        }

      },
      legend: {
        enabled: my.props.legend
      },
      colors:my.props.color,
      title:{
        text:null
      },
      plotOptions: {
        series: {
          animation: false
        },
        area: {
          marker: {
            enabled: false,
            symbol: 'circle',
            radius: 2,
            states: {
              hover: {
                enabled: true
              }
            }
          },
          lineWidth: 1,
          states: {
            hover: {
              lineWidth: 1
            }
          },
        },
      },
      tooltip: {
        valueSuffix: my.props.valueSuffix
      },
      series: my.state.data.series

    };
    return (
      <div className="assBox">
        <div className="btnChoose">
          <BtnGroup
            activeKey={0}
            prop={["1小时","6小时","1天"]}
            type = "memory"
            onSelect={this.changeTime.bind(this)}
          >
          </BtnGroup>
        </div>
        <div className="monitorBox">
          {
            !this.state.data.xAxis.length?"监控信息传输中,请稍后再试":<ReactHighcharts config={config} />
          }
        </div>
      </div>
    )
  }
}
