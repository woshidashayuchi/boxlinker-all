/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React, { PropTypes,Component } from 'react';
import ServiceStep from '../ServiceStep';
import HeadLine from '../HeadLine';
import ReactDOM from 'react-dom';
import Link from '../Link';
import Toggle from '../Toggle';
import {INPUT_TIP,BREADCRUMB} from "../../constants";
import {navigate} from '../../actions/route';
import {receiveNotification,clearNotification} from '../../actions/notification';

const title = '新建服务';

class AutoStartUpToggle extends  Component{
  static propTypes={
    getToggle:React.PropTypes.func,
    isState:React.PropTypes.bool,
  };
  constructor(props) {
    super(props);
    this.state = {
      autoStart:true
    };
  }
  componentWillMount(){
    this.setState({
      autoStart:this.props.isState
    })
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

class AddService extends Component{
  static contextTypes = {
    setTitle: PropTypes.func.isRequired,
    store:PropTypes.object
  };
  static propTypes = {
    onDeployService : React.PropTypes.func,
    volumeList:React.PropTypes.array,
    onVolumeListLoad : React.PropTypes.func,
    deployData:React.PropTypes.object,
    onDeploySenior:React.PropTypes.func,
    onAddPort:React.PropTypes.func,
    onDelPort:React.PropTypes.func,
    onAddSave:React.PropTypes.func,
    onDelSave:React.PropTypes.func,
    onAddEnv:React.PropTypes.func,
    onDelEnv: React.PropTypes.func,
    setBreadcrumb:React.PropTypes.func,
    isSidebarOpen:React.PropTypes.bool,
    isBtnState:React.PropTypes.object
  };
  constructor(props) {
    super(props);
    this.state = {
      isPort:false,
      isPortShow:false,
      isStateUp:1,
      port:false,
      volume:false,
      env:false
    };
  }

  delVal (index){
    let containerTr = ReactDOM.findDOMNode(this.refs.tab_container_body).getElementsByTagName("tr");
    let input = containerTr[index].getElementsByTagName("input")[0];
    input.focus();
    input.value="";
  }
  focusVal(index){
    let containerTr = ReactDOM.findDOMNode(this.refs.tab_container_body).getElementsByTagName("tr");
    let input = containerTr[index].getElementsByTagName("input")[0];
    input.focus();
  }
  isPortRepeat(index,e){
    let container = [];
    let containerTr = ReactDOM.findDOMNode(this.refs.tab_container_body).getElementsByTagName("tr");
    let value = e.target.value;
    for(var i=0;i<containerTr.length;i++){
      let containerObj = {};
      containerObj.container_port = containerTr[i].getElementsByTagName("input")[0].value;
      container.push(containerObj);
    }
    this.setState({
      port:false
    });
    e.target.className = "form-control form-control-sm";
    if(value<=10 && value.length != 0){
      this.setState({
        port:true
      });
      e.target.className = "form-control form-control-sm inputError";
      this.refs.portTip.innerHTML = INPUT_TIP.port.Format;
      return false;
    }
    container.splice(index,1);
    container.map((item) => {
      if(item.container_port == value && value !=""){
        this.setState({
          port:true
        });
        e.target.className = "form-control form-control-sm inputError";
        this.refs.portTip.innerHTML = INPUT_TIP.port.Repeat;
        e.target.focus();
        return false;
      }
    });

  }
  isSaveRepeat(index,e){
    let save = [];
    let saveTr = ReactDOM.findDOMNode(this.refs.tab_save_box).children;
    let key = e.target.value;
    this.setState({
      volume:false
    });
    for(let i = 0;i<saveTr.length;i++){
      let saveObj = {};
      saveObj.value = saveTr[i].getElementsByTagName("select")[0].value;
      save.push(saveObj);
    }
    save.splice(index,1);
    save.map((item) => {
      if(item.value == key && key !=""){
        this.setState({
          volume:true
        });
        this.refs.volumeTip.innerHTML = INPUT_TIP.volumes.Repeat;
        e.target.value = "-1";
        e.target.focus();
        return false;
      }
    })

  }
  isEnvKey(index,e){
    let env = [];
    let regExp = /^[a-zA-Z]+[a-zA-Z0-9-]*$/;
    let envTr = ReactDOM.findDOMNode(this.refs.tab_env_box).children;
    let key = e.target.value;
    this.setState({
      env:false
    });
    e.target.className = "form-control";
    if(!regExp.test(key)){
      this.setState({
        env:true
      });
      this.refs.envTip.innerHTML = INPUT_TIP.env.Format;
      e.target.className = "form-control inputError";
      e.target.focus();
      return false;
    }
    for(let i = 0;i<envTr.length;i++){
      let envObj = {};
      envObj.env_key = envTr[i].getElementsByTagName("input")[0].value;
      env.push(envObj);
    }
    env.splice(index,1);
    env.map((item) => {
      if(item.env_key == key && key !=""){
        this.setState({
          env:true
        });
        this.refs.envTip.innerHTML = INPUT_TIP.env.Repeat;
        e.target.className = "form-control inputError";
        e.target.focus();
      }
    })
  }
  isEnvValue(e){
    this.setState({
      env:false
    });
    e.target.className = "form-control";
  }
  isPathValidata(e){
    let regExp = /^\/[a-zA-Z]+[a-zA-Z0-9_]*$/;
    let value = e.target.value;
    if(!regExp.test(value)&&value.length != 0){
      this.setState({
        volume:true
      });
      e.target.className = "form-control inputError";
      this.refs.volumeTip.innerHTML = INPUT_TIP.volumes.Format;
    }else{
      this.setState({
        volume:false
      });
      e.target.className = "form-control";
    }

  }
  getPortTableBody(){//端口
    let data = [],sd = this.props.deployData;
    if(sd&&sd.container&&sd.container.length)
      data = this.props.deployData.container;
    let tr = data.map((item , i) => {
      return(
        <tr key = {item.at}>
          <td>
            <div className="astTdBox">
              <div className="iaBox">
                  <input type="number" ref="container_port" onBlur={this.isPortRepeat.bind(this,i)} className="form-control form-control-sm" defaultValue={item.container_port}/>
                  <span className="iaOk icon-right" onClick = {this.focusVal.bind(this,i)}> </span>
                  <span className="iaDel icon-delete" onClick = {this.delVal.bind(this,i)}> </span>
              </div>
            </div>
          </td>
          <td>
            <div className="astTdBox">
              <select className="form-control" ref = "protocol" selected = {item.protocol}>
                <option value="TCP">TCP</option>
                <option value="UDP">UDP</option>
              </select>
            </div>
          </td>
          <td>
            <div className="astTdBox">
              <select className="form-control" ref = "access_mode" selected = {item.access_mode} >
                <option value="HTTP">HTTP</option>
                <option value="TCP">TCP</option>
                <option value="no">不可访问</option>
              </select>
            </div>
          </td>
          <td>
            <div className="astTdBox">
              <select className="form-control" ref = "access_scope" selected = {item.access_scope}>
                <option value="outsisde">外部范围</option>
                <option value="inside">内部范围</option>
              </select>
            </div>
          </td>
          <td>
            <a href="javascript:;" className="delBtn" onClick = {this.delPortTr.bind(this,item.at)}> </a>
          </td>
        </tr>
      )
    });
    return (
      tr
    )
  }
  getPortTable(){
    return (
      <table className="table table-bordered">
        <thead>
        <tr>
          <th width = "20%">容器端口</th>
          <th width = "20%">协议</th>
          <th width = "20%">访问方式</th>
          <th width = "20%">访问范围</th>
          <th width = "20%">操作</th>
        </tr>
        </thead>
        <tbody ref = "tab_container_body">
        {this.getPortTableBody()}
        </tbody>
      </table>
    )
  }
  addPortTr(){
    this.props.onAddPort();
  }
  delPortTr(item){
    this.props.onDelPort(item);
  }
  getSaveTableBody(){//存储
    let volumeList = this.props.volumeList;
    let options = volumeList.map((item,i) => {
      if(item.disk_status == "unused") {
        return (
          <option key={i} value={item.disk_name}>{item.disk_name} </option>
        )
      }else{
        return
      }
    });
    let data = [],sd = this.props.deployData;
    if(sd&&sd.volume&&sd.volume.length)
      data = this.props.deployData.volume;
    let tr = data.map((item , i) => {
      return (
        <tr key = {item.at}>
          <td>
            <div className="astTdBox">
              <select className="form-control" ref = "volumn_name" defaultValue={item.disk_name}
                      onChange={this.isSaveRepeat.bind(this,i)}
              >
                <option key = "-1" value = "-1">请选择数据卷</option>
                {options}
              </select>
            </div>
          </td>
          <td>
            <div className="astTdBox">
                <input type = "text" defaultValue={item.disk_path} className = "form-control"
                       onBlur={this.isPathValidata.bind(this)} ref = "container_path"/>
            </div>
          </td>
          <td>
            <div className="astTdBox">
              <label>
                <input type="checkbox" defaultChecked={item.readonly==1} /> 是否只读
              </label>
            </div>
          </td>
          <td>
            <a href="javascript:;" className="delBtn" onClick = {this.delSaveTr.bind(this,item.at)}> </a>
          </td>
        </tr>
      )
    });

    return (
      tr
    )
  }
  getSaveTable(){
    return (
      <table className="table table-bordered">
        <thead>
        <tr>
          <th width = "25%">数据卷名称</th>
          <th width = "25%">容器路径</th>
          <th width = "25%">是否只读</th>
          <th width = "25%">操作</th>
        </tr>
        </thead>
        <tbody ref = "tab_storage_body">
        {this.getSaveTableBody()}
        </tbody>
      </table>
    )
  }
  addSaveTr(){
    this.props.onAddSave();
  }
  delSaveTr(item){
    this.props.onDelSave(item)
  }
  getEnvironment(){
    let data = [],sd = this.props.deployData;
    if(sd&&sd.env&&sd.env.length)
      data = this.props.deployData.env;
    let keyBox = data.map((item,i) => {
      return (
        <div key = {item.at} className = "astKeyItem">
          <div className="astInp">
            <input type = "text" className = "form-control" onBlur={this.isEnvKey.bind(this,i)} ref = "env_key" placeholder = "键" defaultValue = {item.env_key} />
          </div>
          <div className="astLine"></div>
          <div className="astInp">
            <input type = "text" className = "form-control" onBlur={this.isEnvValue.bind(this)} ref = "env_value" placeholder = "值" defaultValue = {item.env_value} />
          </div>
          <div className = "astDel">
            <a href="javascript:;" className="delBtn" onClick = {this.delEnvironmentData.bind(this,item.at)}> </a>
          </div>
        </div>
      )
    });
    return (
      keyBox
    )
  }
  addEnvironmentData(){
    this.props.onAddEnv();
  }
  delEnvironmentData(item){
    this.props.onDelEnv(item);
  }
  onChangeStep(){
    let container = [],
      save = [],
      env = [];
    let containerTr = ReactDOM.findDOMNode(this.refs.tab_container_body).getElementsByTagName("tr"),
      saveTr = ReactDOM.findDOMNode(this.refs.tab_storage_body).getElementsByTagName("tr"),
      envTr = ReactDOM.findDOMNode(this.refs.tab_env_box).children;
    for(var i=0;i<containerTr.length;i++){
      let containerObj = {};
      containerObj.container_port = containerTr[i].getElementsByTagName("input")[0].value;
      containerObj.protocol = containerTr[i].getElementsByTagName("select")[0].value;
      containerObj.access_mode = containerTr[i].getElementsByTagName("select")[1].value;
      containerObj.access_scope = containerTr[i].getElementsByTagName("select")[2].value;
      containerObj.at = new Date().getTime()+i;
      container.push(containerObj);
    }
    for(let i = 0;i<saveTr.length;i++){
      let saveObj = {};
      saveObj.disk_name = saveTr[i].getElementsByTagName("select")[0].value;
      saveObj.disk_path = saveTr[i].getElementsByTagName("input")[0].value;
      saveObj.readonly = saveTr[i].getElementsByTagName("input")[1].checked;
      saveObj.at = new Date().getTime()+i;
      save.push(saveObj);
    }
    for(let i = 0;i<envTr.length;i++){
      let envObj = {};
      envObj.env_key = envTr[i].getElementsByTagName("input")[0].value;
      envObj.env_value = envTr[i].getElementsByTagName("input")[1].value;
      envObj.at = new Date().getTime()+i;
      env.push(envObj);
    }
    let data = {
      container:container,
      env:env,
      volume :save,
      auto_startup:this.state.isStateUp,
      command:this.refs.command.value
    };
    console.log(data);
    this.props.onDeploySenior(data);
  }
  deployService(){
    let container = [],
      save = [],
      env = [];
    let containerTr = ReactDOM.findDOMNode(this.refs.tab_container_body).getElementsByTagName("tr"),
      saveTr = ReactDOM.findDOMNode(this.refs.tab_storage_body).getElementsByTagName("tr"),
      envTr = ReactDOM.findDOMNode(this.refs.tab_env_box).children;
    for(var i=0;i<containerTr.length;i++){
      let containerObj = {};
      let container_port = containerTr[i].getElementsByTagName("input")[0];
      if(container_port.value == ""){
        this.setState({
          port:true
        });
        container_port.className = "form-control form-control-sm inputError";
        container_port.focus();
        this.refs.portTip.innerHTML = INPUT_TIP.port.Null;
        return false;
      }
      containerObj.container_port = container_port.value;
      containerObj.protocol = containerTr[i].getElementsByTagName("select")[0].value;
      containerObj.access_mode = containerTr[i].getElementsByTagName("select")[1].value;
      containerObj.access_scope = containerTr[i].getElementsByTagName("select")[2].value;
      container.push(containerObj);
    }
    for(let i = 0;i<saveTr.length;i++){
      let saveObj = {};
      let disk_name = saveTr[i].getElementsByTagName("select")[0];
      let disk_path = saveTr[i].getElementsByTagName("input")[0];
      let readonly = saveTr[i].getElementsByTagName("input")[1].checked ? "True" : "False";
      if(disk_name.value!=-1 && disk_path.value == ""){
        this.setState({
          volume:true
        });
        disk_path.className = "form-control inputError";
        this.refs.volumeTip.innerHTML = INPUT_TIP.volumes.Null;
        disk_path.focus();
        return false;
      }
      saveObj.disk_name = disk_name.value;
      saveObj.disk_path = disk_path.value;
      saveObj.readonly = readonly;
      save.push(saveObj);
    }
    for(let i = 0;i<envTr.length;i++){
      let envObj = {};
      let env_key = envTr[i].getElementsByTagName("input")[0];
      let env_value = envTr[i].getElementsByTagName("input")[1];
      if(env_key.value && env_value.value==""){
        this.setState({
          env:true
        });
        this.refs.envTip.innerHTML = INPUT_TIP.env.Null;
        env_value.className = "form-control inputError";
        env_value.focus();
        return false;
      }
      envObj.env_key = env_key.value;
      envObj.env_value = env_value.value;
      env.push(envObj);
    }
    let third = {
      container:container,
      env:env,
      volume :save,
      auto_startup:this.state.isStateUp,
      command:this.refs.command.value
    };
    if(this.state.env||this.state.port||this.state.volume){return false;}
    let data=Object.assign({},this.props.deployData,third);
    console.log(data);
    this.props.onDeployService(data);
  }
  getIsStartUp(value){
    this.setState({
      isStateUp:!value?1:0
    })
  }
  componentDidMount(){
    this.props.onVolumeListLoad();
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.NEW_SERVICE);
    let my = this;
    if(!my.props.deployData.image_id){
      my.context.store.dispatch(receiveNotification({message:"请先选择要部署的镜像",level:"danger"}));
      my.context.store.dispatch(navigate("/choseImage"));
      setTimeout(function(){
        my.context.store.dispatch(clearNotification())
      },3000);
    }else{
      this.props.onVolumeListLoad();
    }
  }
  render(){
    this.context.setTitle(title);
    let data = this.props.deployData;
    let n = 0;
    this.props.volumeList.map((item) => {
      if(item.disk_status == "unused"){
        n++
      }
    });
    let volumeLength = n == 0 ?
      "暂时没有数据卷":
      `目前有${n}个数据卷`;
    return(
      <div className="containerBgF">
       <div className="asTab">
        <ServiceStep dataActive="third"/>
        <div className="assItem">
          <HeadLine
            title="端口"
            titleEnglish="PORT"
            titleInfo="容器端口会映射到主机端口上"
          />
          <div className="astBox">
            {this.getPortTable()}
          </div>
          <div className="assBtnBox">
            <button className="btn btn-primary" onClick = {this.addPortTr.bind(this)}>添加</button>
            <span className={this.state.port?"inputTip inputTipShow":"inputTip"} ref = "portTip">

            </span>
          </div>
        </div>
        <div className="assItem">
          <HeadLine
            title="存储设置"
            titleEnglish="SAVE SETTING"
            titleInfo={volumeLength}
          />
          <div className="astBox" ref = "tab_save_box">
            {this.getSaveTable()}
          </div>
          <div className="assBtnBox">
            <button className="btn btn-primary" onClick = {this.addSaveTr.bind(this)}>添加</button>
            <span className={this.state.volume?"inputTip inputTipShow":"inputTip"} ref = "volumeTip">

            </span>
          </div>
        </div>
        <div className="assItem">
          <HeadLine
            title="环境变量"
            titleEnglish="ENVIRONMENT VARIABLE"
            titleInfo=""
          />
          <div className="astBox" ref = "tab_env_box">
            {this.getEnvironment()}
          </div>
          <div className="assBtnBox">
            <button className="btn btn-primary" onClick = {this.addEnvironmentData.bind(this)}>添加</button>
            <span className={this.state.env?"inputTip inputTipShow":"inputTip"} ref = "envTip">

            </span>
          </div>
        </div>
         <div className="assItem">
           <HeadLine
             title="启动命令"
             titleEnglish="JRE"
             titleInfo="启动命令解释说明 "
           />
           <div className="assBox">
             <input className = "form-control"
                    type="text"
                    ref = "command"
                    placeholder="如果输入，会覆盖镜像的默认启动命令"
             />
           </div>
         </div>
        <div className="assItem assItemNoborder">
          <HeadLine
            title="自动启动"
            titleEnglish="AUTO UPDATE SETTING"
            titleInfo="自动启动设置"
          />
          <div className="assBox">
            <AutoStartUpToggle isState = {data.auto_startup==1} getToggle = {this.getIsStartUp.bind(this)}  />
          </div>
        </div>

         <div className="fixedBottom">
           <div style = {{"marginLeft":this.props.isSidebarOpen?"209px":"79px"}}>
             <Link className = "btn btn-primary" to={`/configContainer`} onClick = {this.onChangeStep.bind(this)}>上一步</Link>
             <button className={`btn btn-primary ${!this.props.isBtnState.deploy?"btn-loading":""}`}
                     onClick={this.deployService.bind(this)}
                      disabled={!this.props.isBtnState.deploy}>
               {this.props.isBtnState.deploy?"部署":"部署中..."}
               </button>
           </div>
         </div>
      </div>
     </div>
    )
  }
}
export default AddService;
