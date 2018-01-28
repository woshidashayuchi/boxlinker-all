
import React, { PropTypes,Component } from 'react';
import {Media,Tabs,Tab,FormGroup,Col} from 'react-bootstrap';
import Logs from '../Logs';
import Loading from '../Loading';
import {BREADCRUMB} from "../../constants";
import Toggle from '../Toggle';
import ReactDOM from 'react-dom';

class IsAutoBuildToggle extends  Component{
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
  componentDidMount(){
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

class BuildingDetail extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      isAutoBuilding:1,
    }
  }
  static contextTypes = {
    setTitle: React.PropTypes.func,
    store: React.PropTypes.object,
  };
  static propTypes = {
    projectId: React.PropTypes.string.isRequired,
    buildingDetail:React.PropTypes.object,
    getBuildingDetail:React.PropTypes.func,
    onFastBuilding:React.PropTypes.func,
    setBreadcrumb:React.PropTypes.func,
    onDeleteImage:React.PropTypes.func,
    isBtnState:React.PropTypes.object,
    reviseBuilding:React.PropTypes.func
  };
  componentDidMount() {
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE, BREADCRUMB.BUILD_IMAGE, BREADCRUMB.IMAGE_DETAIL);
    this.props.getBuildingDetail(this.props.projectId);
    let build_status = this.props.buildingDetail.build_status;
    let my = this;
    this.myTime = setInterval(function () {
      if (my.props.buildingDetail.build_status != 2) {
        clearInterval(my.myTime)
      } else {
        my.props.getBuildingDetail(my.props.projectId);
      }
    }, 5000);
  }
  componentWillUnmount(){
    clearInterval(this.myTime);
  }
  fastBuilding(id){
    let obj = {
      id:id,
      flag:"detail"
    };
    this.props.onFastBuilding(obj);
    let my = this;
    this.myTime = setInterval(function () {
      if (my.props.buildingDetail.build_status != 2) {
        clearInterval(my.myTime)
      } else {
        my.props.getBuildingDetail(my.props.projectId);
      }
    }, 5000);
  }
  onReviseBuilding(){
    let dockerfile_path = ReactDOM.findDOMNode(this.refs.dockerfile_path).value,
        repo_branch = ReactDOM.findDOMNode(this.refs.repo_branch).value;
    let data = {
      dockerfile_path:dockerfile_path,
      repo_branch:repo_branch,
      auto_build:String(this.state.isAutoBuilding),
      uuid:this.props.projectId
    };
    console.log(data);
    this.props.reviseBuilding(data);
  }
  getToggleValue(value){
    let flag = !value ? 1 : 0;//1 true  0 false
    this.setState({
      isAutoBuilding:flag
    })
  }
  baseSeting(){//基本设置
    let data = [this.props.buildingDetail];
    let body = data.map((item) => {
      return (
        <div className="baseSet" key = {new Date(item.creation_time).getTime()}>
          <div className="baseItem">
            <FormGroup controlId="form">
              <Col sm={2}>
                镜像名称
              </Col>
              <Col sm={5}>
                <p>{item.repository}</p>
              </Col>
            </FormGroup>
          </div>
          <div className="baseItem">
            <FormGroup controlId="form">
              <Col sm={2}>
                Dockerfile位置
              </Col>
              <Col sm={5}>
                <input className="form-control" type="text" ref = "dockerfile_path" defaultValue={item.dockerfile_path}/>
              </Col>
            </FormGroup>
          </div>
          <div className="baseItem">
            <FormGroup controlId="form">
              <Col sm={2}>
                默认代码分支
              </Col>
              <Col sm={5}>
                <input className="form-control" type="text" ref = "repo_branch" defaultValue={item.repo_branch} />
              </Col>
            </FormGroup>
          </div>
          <div className="baseItem">
            <FormGroup controlId="form">
              <Col sm={2}>
                自动构建
              </Col>
              <Col sm={5}>
                <IsAutoBuildToggle state = {item.auto_build==1} getToggle = {this.getToggleValue.bind(this)} />
              </Col>
            </FormGroup>
          </div>
          <div className="baseItem">
            <FormGroup controlId="form">
              <Col sm={2}>

              </Col>
              <Col sm={5}>
                <button className={`btn btn-primary ${!this.props.isBtnState.reviseBuilding?"btn-loading":""}`}
                        onClick={this.onReviseBuilding.bind(this)}
                        disabled = {!this.props.isBtnState.reviseBuilding}
                >确认修改</button>
              </Col>
            </FormGroup>
          </div>
        </div>
      )
    });
    return body;
  };
  onDeleteBuilding(id){
    confirm("确定删除?")?this.props.onDeleteImage(id,"detail"):"";
  }
  handle(){//操作
    return(
      <div className="handleBox">
        <button className="btn btn-danger" onClick={this.onDeleteBuilding.bind(this,this.props.projectId)}>删除项目</button>
        <p>*删除项目将清除项目相关数据，请慎重选择！ </p>
      </div>
    )
  };
  render(){
    this.context.setTitle('构建镜像');
    const username = this.context.store.getState().user_info.user_name;
    let buildDetail = this.props.buildingDetail;
    let uuid = this.props.projectId;
    let build_status = buildDetail.build_status;
    if(buildDetail&&!build_status){
      return (
        <div style={{"textAlign":"center"}}><Loading /></div>
      )
    }
    return (
      <div className="containerBgF">
        <div className="cdBd">
          <div className="cbCodeInfo">
            <Media>
              <div className="media-left">
                <img width={65} height={65} src="/avatar.png" alt="Image"/>
              </div>
              <div className="media-body">
                <div className="media-heading">镜像名称 :
                  <a href="javascript:;" target = "_blank" className="aLink">{`index.boxlinker.com/${buildDetail.repository}:${buildDetail.image_tag}`}</a></div>
                <p><button className={`btn btn-primary ${buildDetail.build_status == 2?"btn-loading":""}`}
                           disabled={buildDetail.build_status == 2}
                           onClick = {this.fastBuilding.bind(this,uuid)}
                >
                  {buildDetail.build_status == 2?"构建中":"构建"}
                </button></p>
              </div>
            </Media>
          </div>
          <div className="cbTabs">
            <Tabs defaultActiveKey={1} id="cbTabs">
              <Tab eventKey={1} title="构建日志">
                <div className="asTableBox" style = {{"paddingTop":"30px"}}>
                  <Logs logLabel={`auto_build-${username}-${this.props.projectId}`}/>
                </div>
              </Tab>
              <Tab eventKey={2} title="基本设置">
                <div className="asTableBox">
                  {this.baseSeting()}
                </div>
              </Tab>
              <Tab eventKey={3} title="操作">
                <div className="asTableBox">
                  {this.handle()}
                </div>
              </Tab>
            </Tabs>
          </div>
        </div>
      </div>
    )
  }
}

export default BuildingDetail;
