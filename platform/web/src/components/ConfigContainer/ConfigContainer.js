/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React, { PropTypes,Component } from 'react';
import ServiceStep from '../../components/ServiceStep';
import HeadLine from '../../components/HeadLine';
import ContainerBox from '../../components/ContainerBox';
import InputRange from 'react-input-range';
import Toggle from '../../components/Toggle';
import {DropdownButton,MenuItem} from 'react-bootstrap';
import ReactDOM from 'react-dom';
import {INPUT_TIP} from '../../constants/index';
import Link from '../Link';
import {BREADCRUMB} from "../../constants";
import {navigate} from '../../actions/route';
import {receiveNotification,clearNotification} from '../../actions/notification';
const title = '新建服务';


class InputRangesBox extends Component {//input滑块
  static propTypes={
    getContianerNum:React.PropTypes.func,
    number: React.PropTypes.number,

  };
  constructor(props) {
    super(props);
    this.state = {
      value: this.props.number
    };
  }
  handleValueChange(component,value) {
    this.setState({
      value: value,
    });
    this.props.getContianerNum(value);
  }
  render() {
    return (
      <div className="formField">
        <InputRange
          className="formField"
          maxValue={10}
          minValue={0}
          labelSuffix="个"
          value={this.state.value}
          onChange={this.handleValueChange.bind(this)}
        />
      </div>
    );
  }
}

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

class ConfigContainer extends Component{
  static contextTypes = {
    setTitle: PropTypes.func.isRequired,
    store:PropTypes.object
  };
  static propTypes = {
    deployData:React.PropTypes.object,
    deployContainer:React.PropTypes.func,
    setBreadcrumb:React.PropTypes.func,
    onGoToService:React.PropTypes.func,
    isSidebarOpen:React.PropTypes.bool,
    buildingDetail:React.PropTypes.object,
    getBuildingDetail:React.PropTypes.func,
  };
  constructor(){
    super();
    this.state = {
      containerDeploy:0,
      containerNum:1,
      isUpdate:1,//1 是   0   否
      isServiceName:false
    };
  }

  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.ADD_SERVICE,BREADCRUMB.CONFIG_CONTAINER);
    // let my = this;
    // if(!my.props.deployData.image_id){
    //   my.context.store.dispatch(receiveNotification({message:"请先选择要部署的镜像",level:"danger"}));
    //   my.context.store.dispatch(navigate("/choseImage"));
    //   setTimeout(function(){
    //     my.context.store.dispatch(clearNotification())
    //   },3000);
    // }else{
    //   this.props.getBuildingDetail(this.props.deployData.image_id);
    // }
  }

  onServiceNameChange(){
    let serviceName = ReactDOM.findDOMNode(this.refs.serviceName),
      serviceTip = ReactDOM.findDOMNode(this.refs.serviceNameTip),
      regExp = /^[a-z]+[a-z0-9_-]*$/;
    if(!regExp.test(serviceName.value) && serviceName.value != ""){
      this.setState({
        isServiceName:true
      });
      serviceTip.innerHTML = INPUT_TIP.service.Format
    }else{
      this.setState({
        isServiceName:false
      })
    }
  }
  onNextStep(){
    let serviceName = ReactDOM.findDOMNode(this.refs.serviceName),
        serviceTip = ReactDOM.findDOMNode(this.refs.serviceNameTip);
    if(serviceName.value == ""){
      this.setState({
        isServiceName:true
      });
      serviceName.focus();
      serviceTip.innerHTML = INPUT_TIP.service.Null;
      return false;
    }
    if(!this.state.isServiceName) {
      let data = {
        image_version:ReactDOM.findDOMNode(this.refs.imageVersion).value,
        service_name:serviceName.value,
        containerDeploy:this.state.containerDeploy,
        pods_num:this.state.containerNum,
        policy:this.state.isUpdate
      };
      console.log(data) ;
      this.props.deployContainer(data);
      this.props.onGoToService();
    }
  }

  getContainer(index){
    this.setState({
      containerDeploy:index
    });
  }

  getContainerNum(value){
    this.setState({
      containerNum:value
    })
  }

  getToggleValue(value){
    let flag = !value ? 1 : 0;//1 true  0 false
    this.setState({
      isUpdate:flag
    })
  }
  aaa(key,e){
    this.refs.aaa.title = key;
    console.log(this.refs.aaa.props);
    this.refs.aaa.props.title = "qqqqqq";
    console.log(e.target.innerHTML);
  }
  render(){
    let ttt =  "wwwww";
    this.context.setTitle(title);
    let data = this.props.deployData;
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
      <div className="containerBgF">
        <div className = "asTab">
          <ServiceStep dataActive = "second"/>
          <div className = "assHd">
            <div className="assItem">
              <HeadLine
                title="服务名称"
                titleEnglish="SERVICE NAME"
                titleInfo="规则后定"
              />
              <div className={`assBox ${this.state.isServiceName?"has-error":""}`}>
                <input
                  className = "form-control"
                  ref="serviceName"
                  type="text"
                  placeholder=""
                  defaultValue = {data.service_name}
                  onChange = {this.onServiceNameChange.bind(this)}
                />
                <span className = "inputTip" ref = "serviceNameTip" > </span>
              </div>
            </div>
            <div className = "assItem">
              <HeadLine
                title = "镜像名称"
                titleEnglish = "IMAGE NAME"
                titleInfo = "描述"
              />
              <div className = "assBox">
                <p>{data.image_name}</p>
              </div>
            </div>
            <div className = "assItem">
              <HeadLine
                title = "镜像版本"
                titleEnglish = "MIRROR VERSION"
                titleInfo = "更新于两个月前"
              />
              <div className="assBox">
                <select className="form-control" ref="imageVersion" defaultValue={data.image_version}>
                {option}
              </select>
                <DropdownButton title = {ttt} id = "1" ref = "aaa"
                                onSelect = {this.aaa.bind(this)}
                >
                  <MenuItem eventKey="1">Dropdown link1</MenuItem>
                  <MenuItem eventKey="2">Dropdown link2</MenuItem>
                </DropdownButton>
              </div>
            </div>
            <div className="assItem">
              <HeadLine
                title="容器配置"
                titleEnglish="CONTAINER CONFIGURATION"
                titleInfo="规则后定"
              />
              <div className="assBox assBoxAuto">
                <ContainerBox number = {data.containerDeploy} getContainer = {this.getContainer.bind(this)} />
              </div>
            </div>
            <div className="assItem">
              <HeadLine
                title="容器个数"
                titleEnglish="CONTAINER NUMBER"
                titleInfo="规则后定"
              />
              <div className="assBox formField">
                <InputRangesBox number = {data.pods_num} getContianerNum = {this.getContainerNum.bind(this)}  />
              </div>
            </div>
            <div className="assItem assItemNoborder">
              <HeadLine
                title="自动更新设置"
                titleEnglish="AUTO UPDATE SETTINGS"
                titleInfo="当镜像有更新时容器是否自动更新"
              />
              <div className="assBox">
                <UpdateStartToggle state = {data.policy==1} getToggle = {this.getToggleValue.bind(this)} />
              </div>
            </div>
            <div className="fixedBottom">
              <div style = {{"marginLeft":this.props.isSidebarOpen?"209px":"79px"}}>
                <Link className="btn btn-primary" to={`/choseImage`}>上一步</Link>
                <button className="btn btn-primary" onClick={this.onNextStep.bind(this)}>下一步</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
export default ConfigContainer;
