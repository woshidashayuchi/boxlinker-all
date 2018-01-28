
import React, { PropTypes,Component } from 'react';
import {BREADCRUMB} from "../../constants";
import {timeRange} from '../../core/utils';
import {Tabs,Tab,Button,Modal,FormControl,SplitButton,MenuItem} from 'react-bootstrap';
import Toggle from '../Toggle';
import Confirm from '../Confirm';
import Loading from '../Loading';
import {navigate} from '../../actions/route';

const title = '镜像详情';

class IsPublicToggle extends  Component{
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
        disabled = {this.props.disabled}
        defaultChecked={this.state.autoStart}
        onChange={this.handClick.bind(this)}
      />
    )
  }
}

class ImageDetail extends Component{
  static contextTypes = {
    setTitle: PropTypes.func.isRequired,
    store:PropTypes.object
  };

  static propTypes = {
    setBreadcrumb:React.PropTypes.func,
    imageDetail:React.PropTypes.object,
    getImageDetail:React.PropTypes.func,
    onDeleteImage:React.PropTypes.func,
    goToConfigContainer:React.PropTypes.func,
    isBtnState:React.PropTypes.object,
    onReviseImage:React.PropTypes.func,
  };
  constructor(props) {
    super(props);
    this.state = {
      show: false,
      isPublic:1,
      delData:{}
    };
  }
  showModal() {
    this.setState({show: true});
  }
  hideModal() {
    this.setState({show: false});
  }

  componentDidMount(){
    let uuid = this.props.uuid;
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.IMAGE_DETAIL);
    this.props.getImageDetail(uuid);
  }
  deployImage(ImageName){
    let obj = {
      image_name :`index.boxlinker.com/${ImageName}`,
      image_id:this.props.uuid
    };
    this.props.goToConfigContainer(obj);
  }
  selectImage(name,uuid,key){
    switch (key){
      case "1":
        this.context.store.dispatch(navigate(`/reviseImage/${this.props.uuid}`));
      break;
      case "2":
        this.setState({
          delData:{
            name:name,
            keyList:"myList"
          }
        });
        this.refs.confirmModal.open();
      break;
    }
  }
  getLines(){
    let data = this.props.imageDetail;
    let tags = data.tags ||[];
    if(!tags.length) return <tr><td colSpan = "3">暂无数据~</td></tr>;
    return tags.map((item,i) => {
      return (
        <tr key = {i}>
          <td>{data.repository}</td>
          <td>{item.tag}</td>
          <td>
            <SplitButton
              onClick = {this.deployImage.bind(this,data.repository)}
              bsStyle="primary" title="部署" id={`building-table-line-${i}`}>
              <MenuItem eventKey="1" onClick = {this.showModal.bind(this)}>拉取</MenuItem>
            </SplitButton>
          </td>
        </tr>
      )
    });
  }
  getVersion(){
    return (
      <div className="building-table">
        <table className="table table-hover table-bordered">
          <thead>
          <tr>
            <th width = "33%">镜像名称</th>
            <th width = "33%">版本</th>
            <th width = "34%">操作</th>
          </tr>
          </thead>
          <tbody>
          {this.getLines()}
          </tbody>
        </table>
      </div>
    )
  }
  getToggleValue(obj,value){
    console.log(value,obj);
    let flag = !value ? 1 : 0;//1 true  0 false
    this.setState({
      isPublic:flag
    });
    let repository = obj.repository,
      detail = obj.detail,
      short_description = obj.short_description,
      isPublic = String(flag);
    let data = {
      is_public:isPublic,
      short_description:short_description,
      detail:detail,
      repository:repository,
      is_code:"0",
      uuid:this.props.uuid
    };
    console.log(data);
    this.props.onReviseImage(data);
  }
  building(){
  }
  render(){
    this.context.setTitle(title);
    let data = this.props.imageDetail;
    if(!data.repository) return <div className="text-center"><Loading /></div>;
    let tag = data.image_tag?`:${data.image_tag}`:":latest";
    let userName = this.context.store.getState().user_info.user_name;
    let isMy = userName == data.user_name;
    return (
      <div className="containerBgF containerPadding" key = {data.is_public}>
        <div className="sdHd">
          <div className="sdImg">
            <img />
          </div>
          <div className="sdInfo">
            <div className="sdTitle">
              <div className="sdTitleItem">
                镜像名称:<span>{data.repository}</span>
              </div>
              <div className="sdTitleItem">
                最近部署时间:<span className="color999">{timeRange(new Date(data.update_time))}</span>
              </div>
              <div className="sdTitleItem imageDetail_lastItem">
                <SplitButton
                  onClick = {this.deployImage.bind(this,data.repository,data.uuid)}
                  onSelect={this.selectImage.bind(this,data.repository,data.uuid)}
                  bsStyle="primary" title="部署最新版本" id={`building-table-line`}>
                  <MenuItem eventKey = "1">编辑</MenuItem>
                  <MenuItem eventKey = "2">删除</MenuItem>
                </SplitButton>
              </div>
            </div>
            <div className="sdPBox">
              <div className="sdPItem">
                <span className="sdPItemName">镜像地址:</span>
                <a href={`http://index.boxlinker.com/${data.repository}`}
                   target = "_blank" className="aLink">{`http://index.boxlinker.com/${data.repository}`}</a>
              </div>
              <div className="sdPItem">
                <span className="sdPItemName">拉取命令:</span>
                <span className="aLink">{`docker pull index.boxlinker.com/${data.repository}${tag}`}</span>
              </div>
              <div className="sdPItem">
                <span className="sdPItemName">是否公开:</span>
                <span>
                  <IsPublicToggle
                    disabled={!this.props.isBtnState.building}
                    state = {data.is_public == 1}
                    getToggle = {this.getToggleValue.bind(this,data)}
                  />
                </span>
              </div>
            </div>
          </div>
        </div>
        <div className="sdBd">
          <Tabs defaultActiveKey={1} id="sdTabs">
            <Tab eventKey={1} title="概览">
              <div className="idTableBox">
                <div className="idOverview">
                  {data.detail}
                </div>
              </div>
            </Tab>
            <Tab eventKey={2} title="版本">
              <div className="idTableBox">
                {this.getVersion()}
                <Modal {...this.props} show={this.state.show} onHide={this.hideModal.bind(this)}  bsSize="sm" aria-labelledby="contained-modal-title-sm">
                  <div className="modal-header">
                    <button type="button" className="close" aria-label="Close" onClick={this.hideModal.bind(this)}><span aria-hidden="true">×</span></button>
                    <h4 className="modal-title" id="contained-modal-title-sm">拉取版本: latest扩容</h4>
                  </div>
                  <div className="modal-body">
                    <div className="idModalBox">
                      <p className="idModalFirst">拉取命令:</p>
                      <FormControl
                        type="text"
                        placeholder=""
                      />
                      <p className="idModalLast">拉取镜像前请先登录: docker login daocloud.io</p>
                      <div className="idModalBtnBox">
                        <Button bsStyle="primary">复制</Button>
                        <Button bsStyle="default" onClick={this.hideModal.bind(this)}>取消</Button>
                      </div>
                    </div>
                  </div>
                </Modal>
              </div>
            </Tab>
          </Tabs>
        </div>
        <Confirm
          title = "警告"
          text = "确定要删除此镜像吗?"
          func = {() =>{this.props.onDeleteImage(this.state.delData)}}
          ref = "confirmModal"
        />
      </div>
    )
  }
}



export default ImageDetail;


