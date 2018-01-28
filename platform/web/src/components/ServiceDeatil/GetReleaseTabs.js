/**
 * Created by zhangsai on 16/9/2.
 */
import React,{ PropTypes,Component } from 'react';
import HeadLine from '../../components/HeadLine';
import Toggle from 'react-toggle';
import ReactDOM from 'react-dom';

class UpdateStartToggle extends  Component{
  static propTypes={
    getToggle:React.PropTypes.func,
    state:React.PropTypes.bool,
  };
  constructor(props) {
    super(props);
    this.state = {
      autoStart:this.props.state
    };
  }
  handClick(component, value){
    this.setState({
      autoStart: !this.state.autoStart,
    });
    this.props.getToggle(this.state.autoStart);
  }
  render(){
    return(
        <Toggle
            defaultChecked={this.state.autoStart}
            onChange={this.handClick.bind(this)}
        />
    )
  }
}

class GetReleaseTabs extends Component{
  static propTypes = {
    serviceName:React.PropTypes.string,
    serviceDetail:React.PropTypes.object,
    buildingDetail:React.PropTypes.object,
    getBuildingDetail:React.PropTypes.func,
    onChangeRelease:React.PropTypes.func,
    isBtnState:React.PropTypes.object
  };
  constructor(props){
    super(props);
    this.state = {
      isUpdate:this.props.serviceDetail.policy
    }
  }
  getToggleValue(value){
    let flag = !value ? 1 : 0;//1 true  0 false
    this.setState({
      isUpdate:flag
    })
  }
  componentDidMount(){
    this.props.getBuildingDetail(this.props.serviceDetail.image_id);
  }
  changeRelease(){
    let image_name = this.props.serviceDetail.image_name,
        image_version = ReactDOM.findDOMNode(this.refs.imageVersion).value,
        policy = this.state.isUpdate;
    let data = {
      image_name:image_name,
      image_version:image_version,
      policy:String(policy),
      serviceName:this.props.serviceName
    };
    this.props.onChangeRelease(data);
  }

  render(){
    let data = this.props.serviceDetail;
    let tags = this.props.buildingDetail.tags;
    let option = [];
    if(!tags||!tags.length){
      option.push(<option key = "latest" value = "latest">latest</option>)
    }else {
      tags.map((item,i) => {
        option.push(<option value={item.tag} key = {i}>{item.tag}</option>)
      });
    }
    return(
      <div>
        <div className="assItem">
          <HeadLine
            title="自动发布"
            titleEnglish="AUTOMATIC SENDING"
            titleInfo="当镜像有更新时容器是否自动更新,开启自动更新时会覆盖手动选择的版本"
          />
          <div className="assBox">
            <UpdateStartToggle state = {this.state.isUpdate==1} getToggle = {this.getToggleValue.bind(this)} />
          </div>
        </div>
        <div className="assItem">
          <HeadLine
            title="手动发布"
            titleEnglish="MANUAL RELEASE"
            titleInfo="将服务更新到指定的镜像版本"
          />
          <div className="assBox">
            <select className="form-control" ref="imageVersion" defaultValue={data.image_version}>
              {option}
            </select>
          </div>
          <div className="assBox sdLastBtn">
            <button className={`btn btn-primary ${!this.props.isBtnState.deploy?"btn-loading":""}`}
                    disabled={!this.props.isBtnState.deploy}
                    onClick = {this.changeRelease.bind(this)}>更新发布</button>
          </div>
        </div>
      </div>
    )
  }
}

export default GetReleaseTabs;
