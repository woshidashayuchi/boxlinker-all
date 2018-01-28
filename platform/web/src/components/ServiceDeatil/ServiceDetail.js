/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */
import React, { PropTypes,Component } from 'react';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import s from './ServiceDetail.css';
import Tabs from 'react-bootstrap/lib/Tabs';
import Tab from 'react-bootstrap/lib/Tab';
import InputRange from 'react-input-range';
import GetDisposedTabs from './GetDisposedTabs.js';
import GetMonitorTabs from './GetMonitorTabs.js';
import GetReleaseTabs from './GetReleaseTabs.js';
import GetRealmNameTabs from './GetRealmNameTabs.js';
import GetContainerTabs from './GetContainerTabs.js';
import GetOptTabs from './GetOptTabs.js';
import Logs from '../Logs/Logs'
import {BREADCRUMB} from "../../constants";
import Link from "../Link";
import Loading from "../Loading";
import cx  from 'classnames';
import * as Const from "../../constants";

class InputRangesBox extends Component {//滑块组件
  static propTypes = {
    number: React.PropTypes.number,
    getContianerNum:React.PropTypes.func,
  };
  constructor(props) {
    super(props);
    this.state = {
      value: this.props.number
    };
  }
  handleValueChange(component, value) {
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
          value={this.state.value||this.props.number}
          onChange={this.handleValueChange.bind(this)}
        />
      </div>
    );
  }
}

const title = '服务详情';

class ServiceDetail extends Component{
  static contextTypes = {
    setTitle: PropTypes.func.isRequired,
    store: React.PropTypes.object,
  };
  static propTypes = {
    serviceName: React.PropTypes.string,
    tabs:React.PropTypes.string,
    volumeList: React.PropTypes.array,
    serviceDetail : React.PropTypes.object,
    onSavePort: React.PropTypes.func,
    onSaveVolume:React.PropTypes.func,
    onSaveEnvironment:React.PropTypes.func,
    onServiceDetailLoad : React.PropTypes.func,
    onVolumeListLoad : React.PropTypes.func,
    onSaveContainerDeploy:React.PropTypes.func,
    onAddPort:React.PropTypes.func,
    onDelPort:React.PropTypes.func,
    onAddSave:React.PropTypes.func,
    onDelSave:React.PropTypes.func,
    onAddEnv:React.PropTypes.func,
    onDelEnv: React.PropTypes.func,
    notifications:React.PropTypes.object,
    serviceState :React.PropTypes.string,
    setBreadcrumb:React.PropTypes.func,
    loadEndpoints: React.PropTypes.func,
    onClearServiceDetail:React.PropTypes.func,
    onPodListLoad:React.PropTypes.func,
    podList :React.PropTypes.array,
    onChangeState:React.PropTypes.func,
    onAutoStateUp:React.PropTypes.func,
    onSaveCommand:React.PropTypes.func,
    isBtnState:React.PropTypes.object,
    getMonitorData:React.PropTypes.func,
    monitorData:React.PropTypes.object,
    buildingDetail:React.PropTypes.object,
    getBuildingDetail:React.PropTypes.func,
    onChangeRelease:React.PropTypes.func,
    onDeleteService: React.PropTypes.func,
  };
  constructor(props){
    super(props);
    this.state = {
      containerNum:1,
      tabSelect:this.props.tabs
    }
  }
  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.SERVICE_LIST,BREADCRUMB.SERVICE_DETAIL);
    this.props.onServiceDetailLoad(this.props.serviceName);
    this.props.onVolumeListLoad();
    this.props.onPodListLoad(this.props.serviceName);
  }
  componentWillUnmount(){
    this.props.onClearServiceDetail();
  }
  tabSelect(key){
    switch (Number(key)){
      case 1:
        this.setState({
          tabSelect:1
        });
        break;
      case 2:
        this.setState({
          tabSelect:2
        });
        break;
      case 3:
        this.setState({
          tabSelect:3
        });
        break;
      case 4:
        this.setState({
          tabSelect:4
        });
        break;
      case 5:
        this.setState({
          tabSelect:5
        });
        break;
      case 6:
        this.props.onPodListLoad(this.props.serviceName);
        this.setState({
          tabSelect:6
        });
            break;
      case 7:
        this.setState({
          tabSelect:7
        });
        break;
      default:
            break;
    }
  }
  getContainerNum(value){
    this.setState({
      containerNum:value
    })
  }
  onSavePods(){
    let data = {
      serviceName : this.props.serviceDetail.service_name,
      n : this.state.containerNum

    };
    this.props.onSavePods(data);
  }
  changeState(serviceName,state){
    let data = {serviceName:serviceName,state:state?"stop":"start"};
    this.props.onChangeState(data)
  }
  render(){
    this.context.setTitle(title);
    let data = this.props.serviceDetail;
    if (data&&!data.uuid){
      return (
        <div style={{"textAlign":"center"}}><Loading /></div>
      )
    }
    let serviceState = data.fservice_status.toLowerCase();
    let serviceStateTxt = "";
    let domain = [];
    switch (serviceState) {
      case Const.SERVICE_STATE.Running : serviceStateTxt = <span className="text-success">运行</span>;
        break;
      case Const.SERVICE_STATE.Pending : serviceStateTxt = <span className="text-info">创建中</span>;
        break;
      case Const.SERVICE_STATE.Stopping : serviceStateTxt = <span className="text-danger">关闭</span>;
        break;
      default : serviceStateTxt = <span className="text-danger">运行失败</span>;
        break;
    }
    data.container.map((item) =>{
      let txt =  item.http_domain == null ? item.tcp_domain :item.http_domain;
      domain.push(txt)
    });
    let tab = null;
    switch (Number(this.state.tabSelect)){
      case 1 :
        tab = <GetDisposedTabs
          volumeList={this.props.volumeList}
          serviceDetail={this.props.serviceDetail}
          onSavePort={data => this.props.onSavePort(data)}
          onSaveVolume={data => this.props.onSaveVolume(data)}
          onSaveEnvironment={data => this.props.onSaveEnvironment(data)}
          onSaveContainerDeploy={data => this.props.onSaveContainerDeploy(data)}
          onAddPort={() => this.props.onAddPort()}
          onDelPort={(item) =>this.props.onDelPort(item)}
          onAddSave={() => this.props.onAddSave()}
          onDelSave={(item) =>this.props.onDelSave(item)}
          onAddEnv={()=> this.props.onAddEnv()}
          onDelEnv={(item) => this.props.onDelEnv(item)}
          onSaveCommand = {(txt) => this.props.onSaveCommand(txt)}
          onAutoStateUp = {(data) => this.props.onAutoStateUp(data)}
          isBtnState = {this.props.isBtnState}
        />;
            break;
      case 2:
        tab = this.props.podList.length == 0?<div className="assItem">该服务因没有启动，尚未占用资源，暂无容器实例。</div>:<GetMonitorTabs
          serviceDetail = {this.props.serviceDetail}
          podList = {this.props.podList}
          getMonitorData = {(data) => this.props.getMonitorData(data)}
          monitorData = {this.props.monitorData}
        />;
            break;
      case 3:
        tab = <div className="log" style={{paddingBottom:"100px"}}>
          <Logs logLabel={data.logs_labels}/>
        </div>;
            break;
      case 4:
        tab =  <GetReleaseTabs
                serviceName = {this.props.serviceName}
                serviceDetail = {this.props.serviceDetail}
                buildingDetail = {this.props.buildingDetail}
                getBuildingDetail = {(id) => this.props.getBuildingDetail(id)}
                isBtnState = {this.props.isBtnState}
                onChangeRelease = {(data) => this.props.onChangeRelease(data)}
        />;
        break;
      case 5:
        tab = <GetRealmNameTabs
                serviceDetail = {this.props.serviceDetail}
        />;
        break;
      case 6:
        tab = this.props.podList.length == 0?<div className="assItem">该服务因没有启动，尚未占用资源，暂无容器实例。</div>:<GetContainerTabs
            podList = {this.props.podList}
        />;
        break;
      case 7:
        tab = <GetOptTabs
            serviceName = {this.props.serviceName}
            onDeleteService = {(name) =>{this.props.onDeleteService(name)}}
        />;
        break;

    }
    return(
      <div className="containerBgF containerPadding">
        <div className={s.sdHd}>
          <div className={s.sdImg}>
            <img />
            <a href="javascript:;">置于首页</a>
          </div>
          <div className={s.sdInfo}>
            <div className={s.sdTitle}>
              <div className={s.sdTitleItem}>
                服务名称:<span>{data.service_name}</span>
              </div>
              <div className={s.sdTitleItem}>
                部署时间:<span className="cl9">{data.ltime}</span>
              </div>
              <div className={s.sdTitleItem}>
                状态:{serviceStateTxt}
              </div>
              <div className={s.sdTitleItem}>
                <Link to={"/"} className="btn btn-default">进入控制台</Link>
                <button
                  onClick = {this.changeState.bind(this,data.fservice_name,serviceState == Const.SERVICE_STATE.Running)}
                  className={serviceState == Const.SERVICE_STATE.Running ?"btn btn-default":"btn btn-primary"} ref = "startUpBtn"
                  disabled = {serviceState == Const.SERVICE_STATE.Pending}
                >
                  {serviceState == Const.SERVICE_STATE.Running ?"关闭":"启动"}</button>
              </div>
            </div>
            <div className={s.sdPBox}>
              <div className={cx(s.sdPItem,s.sdDomain)}>
                <span className={s.sdPItemName}>域名:</span>
                {domain.map((item,i) =>{
                  return <a key = {i} href={`http://${item}`} target="_blank" className="clLink">{item}</a>
                })}
              </div>
              <div className={s.sdPItem}>
                <span className={s.sdPItemName}>所属镜像:</span>
                <a href="javascript:;" className="clLink">{data.image_name}</a>
              </div>
              <div className={s.sdPItem}>
                <span className={s.sdPItemName}>容器个数:</span>
                <div className={s.sdInputRanges}>
                  <InputRangesBox number={data.spec_replicas} getContianerNum = {this.getContainerNum.bind(this)} />
                </div>
                <button className={`btn btn-default ${!this.props.isBtnState.pods?"btn-loading":""}`}
                        disabled={!this.props.isBtnState.pods}
                        onClick = {this.onSavePods.bind(this)}>保存</button>
              </div>
            </div>
          </div>
        </div>
        <div className="sdDetail">
          <Tabs defaultActiveKey={Number(this.props.tabs)} onSelect={this.tabSelect.bind(this)} id="sdTabs">
            <Tab eventKey={1} title="配置">
                {this.state.tabSelect==1?tab:null}
            </Tab>
            <Tab eventKey={2} title="监控">
                {this.state.tabSelect==2?tab:null}
            </Tab>
            <Tab eventKey={3} title="日志">
              {this.state.tabSelect==3?tab:null}
            </Tab>
            <Tab eventKey={4} title="发布">
              {this.state.tabSelect==4?tab:null}
            </Tab>
            <Tab eventKey={5} title="域名">
              {this.state.tabSelect==5?tab:null}
            </Tab>
            <Tab eventKey={6} title="容器实例">
              {this.state.tabSelect==6?tab:null}
            </Tab>
            <Tab eventKey={7} title="操作">
              {this.state.tabSelect==7?tab:null}
            </Tab>
          </Tabs>
        </div>
      </div>
    )
  }
}

export default withStyles(s)(ServiceDetail);
