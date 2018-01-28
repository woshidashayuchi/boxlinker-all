/**
 * Created by zhangsai on 16/9/2.
 */
import React, { PropTypes,Component } from 'react';
import HeadLine from '../HeadLine';
import ContainerBox from '../ContainerBox';
import ContainerItem from '../ContainerItem';
import Toggle from '../Toggle';
import {Button,Modal} from 'react-bootstrap/lib';
import ReactDOM from 'react-dom';
import {CPU,INPUT_TIP} from '../../constants';
import {clearDeployData} from '../../actions/deployService';

class AutoStartUpToggle extends  Component{
  static propTypes={
    getToggle:React.PropTypes.func,
    isState:React.PropTypes.bool,
    disabled:React.PropTypes.bool
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
        disabled = {this.props.disabled}
        defaultChecked={this.state.autoStart}
        onChange={this.handClick.bind(this)}
      />
    )
  }
}

class ChooseContainerBtn extends Component{//选择容器 按钮
  static propTypes = {
    onSaveContainerDeploy:React.PropTypes.func,
    serviceName:React.PropTypes.string
  };
  constructor(props) {
    super(props);
    this.state = {
      modalShow: false,
      containerDeploy:0,
    };
  }
  showModal() {
    this.setState({show: true});
  }
  hideModal() {
    this.setState({show: false});
  }
  getContainer(index){
    this.setState({
      containerDeploy:index
    });
  }
  saveContainerDeploy(){
    let data = {
      containerDeploy:this.state.containerDeploy,
      serviceName:this.props.serviceName
    };
    this.props.onSaveContainerDeploy(data);
    this.hideModal();
  }
  render(){
    return(<div className="chooseContainer icon-operation" onClick={this.showModal.bind(this)}>
        <span>更改</span>
        <Modal {...this.props} show={this.state.show} onHide={this.hideModal.bind(this)} bsSize="sm"
               aria-labelledby="contained-modal-title-sm">
          <div className="modal-header">
            <button type="button" onClick={this.hideModal.bind(this)} className="close" aria-label="Close">
              <span aria-hidden="true">×</span></button>
            <h4 className="modal-title" id="contained-modal-title-sm">容器配置</h4>
          </div>
          <div className="modal-body">
            <div className="modalItem">
              <ContainerBox
                getContainer = {this.getContainer.bind(this)}
              />
            </div>
            <div className="modalBtn">
              <Button bsStyle="primary" onClick = {this.saveContainerDeploy.bind(this)}>保存</Button>
              <Button bsStyle="default" onClick={this.hideModal.bind(this)}>取消</Button>
            </div>
          </div>
        </Modal>
      </div>
    )
  }
}

class GetDisposedTabs extends Component{
  static contextTypes = {
    store:PropTypes.object
  };
  static propTypes = {
    serviceDetail : React.PropTypes.object,
    onServiceDetailLoad : React.PropTypes.func,
    onSavePort: React.PropTypes.func,
    onSaveVolume: React.PropTypes.func,
    onSaveEnvironment:React.PropTypes.func,
    getServiceFun : React.PropTypes.func,
    volumeList: React.PropTypes.array,
    onSaveContainerDeploy:React.PropTypes.func,
    onAddPort:React.PropTypes.func,
    onDelPort:React.PropTypes.func,
    onAddSave:React.PropTypes.func,
    onDelSave:React.PropTypes.func,
    onAddEnv:React.PropTypes.func,
    onDelEnv: React.PropTypes.func,
    onSaveCommand:React.PropTypes.func,
    onAutoStateUp:React.PropTypes.func,
    isBtnState:React.PropTypes.object
  };
  constructor(props){
    super(props);
    this.state = {
      isStateUp:1,
      port:false,
      volume:false,
      env:false
    }
  }
  delVal(index){
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
    container.map((item,i) => {
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
  isEnvKeyRepeat(index,e){
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
        this.refs.envTip.innerHTML = INPUT_TIP.volumes.Repeat;
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
    let regExp = /^\/[a-zA-Z0-9]+[a-zA-Z0-9_]*$/;
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
    let data = [],sd = this.props.serviceDetail;
    if(sd&&sd.container&&sd.container.length)
      data = this.props.serviceDetail.container;
    let tr = data.map((item , i) => {
      return(
        <tr key = {item.at}>
          <td>
            <div className="astTdBox">
              <div className={"iaBox"}>
                <input type="number" ref="container_port"  onBlur={this.isPortRepeat.bind(this,i)} className="form-control form-control-sm" defaultValue={item.container_port}/>
                <span className="iaOk icon-right" onClick = {this.focusVal.bind(this,i)}> </span>
                <span className="iaDel icon-delete" onClick = {this.delVal.bind(this,i)}> </span>
              </div>
            </div>
          </td>
          <td>
            <div className="astTdBox">
              <select className="form-control" ref = "protocol" defaultValue = {item.protocol}>
                <option value="TCP">TCP</option>
                <option value="UDP">UDP</option>
              </select>
            </div>
          </td>
          <td>
            <div className="astTdBox">
              <select className="form-control" ref = "access_mode" defaultValue = {item.access_mode}>
                <option value="HTTP">HTTP</option>
                <option value="TCP">TCP</option>
                <option value="no">不可访问</option>
              </select>
            </div>
          </td>
          <td>
            <div className="astTdBox">
              <select className="form-control" ref = "access_scope" defaultValue = {item.access_scope}>
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
  savePort(){
    let container = [];
    let containerTr = ReactDOM.findDOMNode(this.refs.tab_container_body).getElementsByTagName("tr");
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
    let data = {
      serviceName:this.props.serviceDetail.fservice_name,
      container:container
    };
    console.log(data,"+++++++")
    this.props.onSavePort(data);
  }
  getSaveTableBody(){//存储
    let data = [],sd = this.props.serviceDetail;
    let my = this;
    if(sd&&sd.volume&&sd.volume.length)
      data = this.props.serviceDetail.volume;
    let tr = data.map((item,i) => {
      let options = my.props.volumeList.map((obj,i) => {
        if(item.disk_name == obj.disk_name || obj.disk_status == "unused"  ) {
          return (
            <option key={i} value={obj.disk_name}>{obj.disk_name} </option>
          )
        }else{
          return false
        }
      });
      return (
        <tr key = {item.at}>
          <td>
            <div className="astTdBox">
              <select className="form-control" ref = "volumnName" defaultValue={item.disk_name}
                onChange={this.isSaveRepeat.bind(this,i)}
              >
                <option value = "-1">请选择数据卷</option>
                {options}
              </select>
            </div>
          </td>
          <td>
            <div className="astTdBox">
              <input type = "text" className = "form-control" ref = "container_path" defaultValue={item.disk_path}
                onBlur={this.isPathValidata.bind(this)}
              />
            </div>
          </td>
          <td>
            <div className="astTdBox">
              <label>
                <input type="checkbox" defaultChecked={item.readonly == "True"} /> 是否只读
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
  saveStorage(){
    let save = [];
    let saveTr = ReactDOM.findDOMNode(this.refs.tab_storage_body).children;
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
      if(disk_name.value ==-1){

      }else {
        saveObj.disk_name = disk_name.value;
        saveObj.disk_path = disk_path.value;
        saveObj.readonly = readonly;
        save.push(saveObj);
      }
    }
    let data = {
      serviceName:this.props.serviceDetail.fservice_name,
      volume :save,
    };
    console.log(data);
    if(!this.state.volume) {
      this.props.onSaveVolume(data);
    }
  }
  getEnvironment(){
    let data = [],sd = this.props.serviceDetail;
    if(sd&&sd.env&&sd.env.length)
      data = this.props.serviceDetail.env;
    let keyBox = data.map((item,i) => {
      return (
        <div key = {item.at} className = "astKeyItem">
          <div className="astInp">
            <input type = "text" className = "form-control" onBlur={this.isEnvKeyRepeat.bind(this,i)} placeholder = "键" defaultValue={item.env_key} />
          </div>
          <div className="astLine"></div>
          <div className="astInp">
            <input type = "text" className = "form-control" onBlur={this.isEnvValue.bind(this)} placeholder = "值" defaultValue={item.env_value} />
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
  saveEnvironment(){
    let env = [];
    let envTr = ReactDOM.findDOMNode(this.refs.tab_env_box).children;
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
    let data = {
      serviceName:this.props.serviceDetail.fservice_name,
      env :env,
    };
    this.props.onSaveEnvironment(data);
  }
  getContainerBox(n){
    if(!n){
      n=0;
    }
    let styleArr = [
        "containerBoxStyle_0 containerBoxStyle",
        "containerBoxStyle_1 containerBoxStyle",
        "containerBoxStyle_2 containerBoxStyle",
        "containerBoxStyle_3 containerBoxStyle",
        "containerBoxStyle_4 containerBoxStyle",
      ],
      newData = [],
      style = styleArr[n];
    newData.push(CPU[n]);
    let children = newData.map(function(item,i){
      return (
        <div className = {style} key = {i} >
          <ContainerItem key={i} classNumber = {i} active = {true}>
            <span>{item.x}</span>
            <span>x</span>
            <span>{item.m}<span>(公测)</span></span>
          </ContainerItem>
        </div>
      );
    });
    return (
      children
    )
  }
  getIsStartUp(value){
    this.setState({
      isStateUp:!value?1:0
    });
    let data = {
      serviceName:this.props.serviceDetail.fservice_name,
      auto_startup:!value?1:0
    };
    console.log(data);
    this.props.onAutoStateUp(data);
  }
  saveCommand(){
    let txt = this.refs.command.value;
    console.log(txt);
    let data = {
      command:txt,
      serviceName:this.props.serviceDetail.fservice_name,
    };
    this.props.onSaveCommand(data);
  }
  componentWillUnmount(){
    this.context.store.dispatch(clearDeployData());
  }

  render(){
    let data = this.props.serviceDetail;
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
      <div className="asTabThird">
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
            <button className="btn btn-primary"
                    onClick = {this.addPortTr.bind(this)}
            >添加</button>
            <button className={`btn btn-default ${!this.props.isBtnState.port?"btn-loading":""}`}
                    disabled={!this.props.isBtnState.port}
                    onClick = {this.savePort.bind(this)}>保存</button>
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
            <button className={`btn btn-default ${!this.props.isBtnState.storage?"btn-loading":""}`}
                    disabled={!this.props.isBtnState.storage}
                    onClick = {this.saveStorage.bind(this)}
            >保存</button>
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
            <button className={`btn btn-default ${!this.props.isBtnState.env?"btn-loading":""}`}
                    disabled={!this.props.isBtnState.env}
                    onClick = {this.saveEnvironment.bind(this)}
            >保存</button>
            <span className={this.state.env?"inputTip inputTipShow":"inputTip"} ref = "envTip">

            </span>
          </div>
        </div>
        <div className="assItem">
          <HeadLine
            title="容器配置"
            titleEnglish="CONTAINER CONFIGURATION"
            titleInfo="容器配置说明"
          />
          <div className="assBox">
            {this.getContainerBox(data.containerDeploy)}
            {/*<ChooseContainerBtn*/}
              {/*serviceName = {this.props.serviceDetail.fservice_name}*/}
              {/*onSaveContainerDeploy={(data) => {this.props.onSaveContainerDeploy(data)}}*/}
            {/*/>*/}
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
                   placeholder=""
                   ref = "command"
                   defaultValue={data.command}
            />
          </div>
          <div className="assBtnBox">
            <button className={`btn btn-default ${!this.props.isBtnState.command?"btn-loading":""}`}
                    disabled={!this.props.isBtnState.command}
                    onClick = {this.saveCommand.bind(this)}
            >保存</button>
          </div>
        </div>
        <div className="assItem assItemNoborder">
          <HeadLine
            title="自动启动"
            titleEnglish="AUTO UPDATE SETTING"
            titleInfo="自动启动设置"
          />
          <div className="assBox">
            <AutoStartUpToggle disabled ={!this.props.isBtnState.autoStateUp}
                               isState = {data.auto_startup==1}
                               getToggle = {this.getIsStartUp.bind(this)}  />
          </div>
        </div>
      </div>
    )
  }
}

export default GetDisposedTabs;

