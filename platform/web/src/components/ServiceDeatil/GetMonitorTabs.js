/**
 * Created by zhangsai on 16/9/2.
 */
import React,{ PropTypes,Component } from 'react';
import HeadLine from '../HeadLine';
import Monitor from '../Monitor';
import Loading from '../Loading';

class GetMonitorTabs extends Component{
  static contextTypes = {
    store:PropTypes.object
  };
  static propTypes = {
    serviceDetail:React.PropTypes.object,
    podList :React.PropTypes.array,
    getMonitorData:React.PropTypes.func,
    monitorData:React.PropTypes.object
  };
  constructor(props){
    super(props);
    this.state = {
      pod_name:this.props.podList[0].pod_name,
    }
  }
  componentDidMount(){}

  changePods(e){
    this.setState({
      pod_name:e.target.value
    });
    let my = this;
    setTimeout(function(){
      my.refs.cpu.componentDidMount();
      my.refs.memory.componentDidMount();
      my.refs.network.componentDidMount()
    },200)
  }

  render(){
    if(!this.state.pod_name || !this.props.serviceDetail) return(<div className="text-center"><Loading> </Loading></div>);
    let limits_cpu = this.props.serviceDetail.limits_cpu;
    switch (Number(limits_cpu)){
      case 8 :
        limits_cpu = 1000;
      break;
      case 16 :
        limits_cpu = 2000;
      break;
      default :
        limits_cpu = 200;
      break;
    }
    let userName = this.context.store.getState().user_info.user_name;
    let pod_name = this.state.pod_name;
    let cpu = {
      userName: userName,
      pod_name: pod_name,
      type: "cpu",
      time_span: "1m"
    };
    let memory = {
      userName: userName,
      pod_name: pod_name,
      type: "memory",
      time_span: "1m"
    };
    let network = {
      userName: userName,
      pod_name: pod_name,
      type: "network",
      time_span: "1m"
    };
    let option = this.props.podList.map((item,i) => {
      return (
        <option value = {item.pod_name} key = {i}>{item.pod_name}</option>
      )
    });
    return(
      <div>
        <div className="choosePods">
          <label>
            请选择容器实例:
          </label>
          <select className="form-control" onChange={this.changePods.bind(this)}>
            {option}
          </select>
        </div>
        <div className="assItem">
          <HeadLine
            title="CPU监控"
            titleEnglish="CPU MONITOR"
            titleInfo="24小时"
          />
          <div className="assBox">
            <Monitor
              ref = "cpu"
              payload = {cpu}
              color = {["#7ed9fc"]}
              legend = {false}
              divisor = {limits_cpu}
              valueSuffix = "%"
            >
            </Monitor>
          </div>
        </div>
        <div className="assItem">
          <HeadLine
            title="内存监控"
            titleEnglish="MEMORY MONITOR"
            titleInfo="24小时"
          />
          <div className="assBox">
            <Monitor
              ref = "memory"
              payload = {memory}
              color = {["#b7e769"]}
              legend = {false}
              divisor = "1000000"
              valueSuffix = "M"
            >
            </Monitor>
          </div>
        </div>
        <div className="assItem">
          <HeadLine
            title="网络监控"
            titleEnglish="NETWORK MONITOR"
            titleInfo="24小时"
          />
          <div className="assBox">
            <Monitor
              ref = "network"
              payload = {network}
              color = {["#f7a397","#b7e769"]}
              legend = {true}
              divisor = "1000"
              valueSuffix = "kBps"
            >
            </Monitor>
          </div>
        </div>
      </div>
    )
  }
}

export default GetMonitorTabs;
