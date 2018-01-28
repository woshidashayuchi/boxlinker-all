
import React, { PropTypes,Component } from 'react';
import HeadLine from '../../components/HeadLine';
import ReactDOM from 'react-dom';
import Toggle from '../Toggle';
import {BREADCRUMB,INPUT_TIP} from "../../constants";

class IsPublicToggle extends  Component{
  static propTypes={
    getToggle:React.PropTypes.func,
    state:React.PropTypes.bool,
  };
  constructor(props) {
    super(props);
    this.state = {
      is_public:this.props.state
    };
  }
  handClick(component, value){
    this.setState({
      is_public: !this.state.is_public,
    });
    this.props.getToggle(this.state.is_public);
  }
  componentDidMount(){
  }
  render(){
    return(
      <Toggle
        defaultChecked={this.state.is_public}
        onChange={this.handClick.bind(this)}
      />
    )
  }
}

class ReviseImage extends React.Component{
  constructor(){
    super();
    this.state = {
      isImageName:false,
      isPublic:1
    }
  }
  static contextTypes = {
    setTitle: React.PropTypes.func,
    store: React.PropTypes.object,
  };
  static propTypes = {
    uuid:React.PropTypes.string,
    setBreadcrumb:React.PropTypes.func,
    isBtnState:React.PropTypes.object,
    imageDetail:React.PropTypes.object,
    getImageDetail:React.PropTypes.func,
    onReviseImage:React.PropTypes.func,
  };
  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.CREATE_IMAGE);
    this.props.getImageDetail(this.props.uuid);
  }
  onImageNameChange(){
    let imageName = ReactDOM.findDOMNode(this.refs.repository),
      imageTip = ReactDOM.findDOMNode(this.refs.image_name_tip),
      regExp = /^[a-z]+[a-z0-9_-]*$/;
    if(!regExp.test(imageName.value) && imageName.value != ""){
      this.setState({
        isImageName:true
      });
      imageTip.innerHTML = INPUT_TIP.image.Format
    }else{
      this.setState({
        isImageName:false
      })
    }
  }
  building(){
    let repository = ReactDOM.findDOMNode(this.refs.repository).innerHTML,
      detail = ReactDOM.findDOMNode(this.refs.image_detail).value,
      short_description = ReactDOM.findDOMNode(this.refs.short_description).value,
      isPublic = String(this.state.isPublic);
    let data = {
      is_public:isPublic,
      short_description:short_description,
      detail:detail,
      repository:repository,
      is_code:"0",
      uuid:this.props.uuid
    };
    this.props.onReviseImage(data);
  }
  getToggleValue(value){
    let flag = !value ? 1 : 0;//1 true  0 false
    this.setState({
      isPublic:flag
    })
  }
  getDate(){
    let arr = [this.props.imageDetail];
    let my = this;
    let name = arr[0].repository||"";
    name = name.split("/")[1];
    let dataBox = arr.map((item,i) => {
      return (
        <div className="acBox" key = {new Date(item.creation_time).getTime()}>
          <h1>修改镜像</h1>
          <p>镜像是服务运行的模板, 来源于代码, 基于 Dockerfile 构建, 默认目录在根'/'下, 文件名 Dockerfile .</p>
          <div className="assItem">
            <HeadLine
              title="镜像名称"
              titleEnglish="IMAGE NAME"
              titleInfo="默认会与您下方代码源的项目名称相同"
            />
            <div className={`assBox ${my.state.isImageName?"has-error":""}`}>
              <span ref = "repository">{name}</span>
            </div>
          </div>
          <div className="assItem">
            <HeadLine
              title="镜像简介"
              titleEnglish="IMAGE SUMMARY"
              titleInfo="简单介绍镜像的信息"
            />
            <div className="assBox">
                <textarea
                  placeholder="镜像简介"
                  className="form-control"
                  defaultValue={item.detail}
                  ref = 'image_detail'
                />
            </div>
          </div>
          <div className="assItem">
            <HeadLine
              title="详细描述"
              titleEnglish="IMAGE DETAIL"
              titleInfo="详细介绍镜像的信息"
            />
            <div className="assBox">
                <textarea
                  placeholder="详细描述"
                  className="form-control"
                  defaultValue={item.short_description}
                  ref = 'short_description'
                />
            </div>
          </div>
          <div className="assItem">
            <HeadLine
              title="是否公开"
              titleEnglish="IS PUBLIC"
              titleInfo="公开后都可以访问"
            />
            <div className="assBox">
              <IsPublicToggle state = {item.is_public == 1} getToggle = {my.getToggleValue.bind(this)} />
            </div>
          </div>
          <div className="assItem">
            <div className="acBtn">
              <button className="btn btn-primary"
                      onClick = {my.building.bind(this)}
                      disabled={!my.props.isBtnState.building}>
                {my.props.isBtnState.building?"修改":"修改中..."}
              </button>
            </div>
          </div>
        </div>
      )
    });
    return dataBox;
  }
  render(){
    this.context.setTitle('修改镜像');
    return (
      <div className="containerBgF">
        {this.getDate()}
      </div>
    )
  }
}

export default ReviseImage;
