
import React, { PropTypes,Component } from 'react';
import {FormGroup,Col,Button,DropdownButton,MenuItem,
  ButtonGroup,Dropdown,
} from 'react-bootstrap';
import Toggle from '../Toggle'
import HeadLine from '../HeadLine';
import ReactDOM from 'react-dom';
import {BREADCRUMB,INPUT_TIP} from "../../constants";

const DropdownToggle = Dropdown.Toggle,
  DropdownMenu = Dropdown.Menu;

const CodeStore = {
  "Default":(<span>选择代码仓库</span>),
  "Github":(<span><i className="icon-github"> </i><i>Github</i></span>),
  "Coding":(<span><i className="icon-refresh"> </i><i>Coding</i></span>)
};

class BuildingCreate extends React.Component{
  constructor(){
    super();
    this.state = {
      codeStoreKey: "Default",
      repoKey: null,
      repoId:null,
      isImageName:false,
      isAutoBuilding:1,
      isPublic:1
    }
  }
  static contextTypes = {
    setTitle: React.PropTypes.func,
    store: React.PropTypes.object,
    setBreadcrumb:React.PropTypes.func
  };
  static propTypes = {
    repos: React.PropTypes.array,
    githubAuthURL: React.PropTypes.string,
    onReposLoad: React.PropTypes.func,
    getGithubAuthURL: React.PropTypes.func,
    onBuilding:React.PropTypes.func,
    isBtnState:React.PropTypes.object
  };
  selectCodeStore(key,refresh){
    console.log(key,refresh);
    let tip = ReactDOM.findDOMNode(this.refs.btn_group_tip);
    tip.style.display = "none";
    this.setState({codeStoreKey:key});
    this.props.onReposLoad(key,refresh);
  }
  selectRepo(key,id){
    let tip = ReactDOM.findDOMNode(this.refs.btn_group_tip);
    tip.style.display = "none";
    this.setState({repoKey:key});
    this.setState({repoId:id});
  }
  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.BUILD_CREATE);
    if(this.state.codeStoreKey!='Default')
      this.props.onReposLoad(this.state.codeStoreKey);
    this.props.getGithubAuthURL();
  }
  onImageNameChange(){
    let imageName = ReactDOM.findDOMNode(this.refs.image_name),
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
    let imageName = ReactDOM.findDOMNode(this.refs.image_name),
      imageTip = ReactDOM.findDOMNode(this.refs.image_name_tip);
    if(imageName.value == ""){
      this.setState({
        isImageName:true
      });
      imageName.focus();
      imageTip.innerHTML = INPUT_TIP.image.Null;
      return false;
    }
    if(this.state.codeStoreKey == "Default"){
      let tip = ReactDOM.findDOMNode(this.refs.btn_group_tip);
      tip.style.display = "inline-block";
      tip.style.color = "red";
      tip.innerHTML = "代码仓库不能为空";
      return false;
    }
    if(!this.state.repoKey){
      let tip = ReactDOM.findDOMNode(this.refs.btn_group_tip);
      tip.style.display = "inline-block";
      tip.style.color = "red";
      tip.innerHTML = "项目不能为空";
      return false;
    }
    if(!this.state.isImageName) {
      let repository = ReactDOM.findDOMNode(this.refs.image_name).value,
        image_tag = ReactDOM.findDOMNode(this.refs.image_tag).value,
        repo_name = this.state.repoKey,
        repo_branch = "master",
        dockerfile_path = ReactDOM.findDOMNode(this.refs.dockerfile_name).value,
        dockerfile_name = ReactDOM.findDOMNode(this.refs.dockerfile_path).value,
        auto_build = String(this.state.isAutoBuilding),
        is_public = String(this.state.isPublic),
        detail = ReactDOM.findDOMNode(this.refs.detail).value,
        short_description = ReactDOM.findDOMNode(this.refs.short_description).value
      let data = {
        repository: repository,
        repo_name: repo_name,
        repo_branch: repo_branch,
        image_tag: image_tag,
        dockerfile_path:dockerfile_path,
        dockerfile_name: dockerfile_name,
        auto_build: auto_build,
        is_public: is_public,
        detail: detail,
        short_description: short_description,
        is_code: "1",
      };
      console.log(data);
      this.props.onBuilding(data)
    }
  }

  getToggleValue(){
    this.setState({
      isAutoBuilding:this.state.isAutoBuilding?0:1
    })
  }

  changePublicToggleValue(){
    this.setState({
      isPublic:this.state.isPublic?0:1
    })
  }

  render(){
    this.context.setTitle('代码构建');
    let user = this.context.store.getState().user_info;
    return (
      <div className="containerBgF">
        <div className="acBox">
          <h1>代码构建</h1>
          <p>镜像是服务运行的模板, 来源于代码, 基于 Dockerfile 构建, 默认目录在根'/'下, 文件名 Dockerfile .</p>
          <div className="assItem">
            <HeadLine
              title="镜像名称"
              titleEnglish="IMAGE NAME"
              titleInfo="默认会与您下方代码源的项目名称相同"
            />
            <div className={`assBox ${this.state.isImageName?"has-error":""}`}>
              <input
                type="text"
                placeholder=""
                className="form-control"
                ref = "image_name"
                onChange={this.onImageNameChange.bind(this)}
              />
              <span className="inputTip" ref = "image_name_tip">镜像名称不能为空</span>
            </div>
          </div>
          <div className="assItem">
            <HeadLine
              title="镜像标签"
              titleEnglish="IMAGE TAG"
              titleInfo="默认为latest"
            />
            <div className="assBox">
              <input
                type="text"
                placeholder=""
                className="form-control"
                ref = "image_tag"
                defaultValue="latest"
              />
            </div>
          </div>
          <div className="assItem">
            <HeadLine
              title="代码源"
              titleEnglish="CODE SOURCES"
              titleInfo="代码源的描述等"
            />
            <div className="assBox">
              {!user.github?<a className="btn btn-primary" href={this.props.githubAuthURL}>Github 授权</a>:
                <ButtonGroup>
                  <Dropdown bsStyle="default" ref = "repo_name"
                            onSelect={this.selectCodeStore.bind(this)}
                            id={`building-create-source-codestore`}>
                    <DropdownToggle>
                      {CodeStore[this.state.codeStoreKey]}
                    </DropdownToggle>
                    <DropdownMenu>
                      <MenuItem eventKey="Github">{CodeStore["Github"]}</MenuItem>
                      <MenuItem eventKey="Coding">{CodeStore["Coding"]}</MenuItem>
                    </DropdownMenu>
                  </Dropdown>
                  <DropdownButton bsStyle="default" title={this.state.repoKey||"选择项目"} onSelect={this.selectRepo.bind(this)} id={`building-create-source-repos`}>
                    {this.props.repos.length != 0?this.props.repos.map((item,i)=>{
                      return <MenuItem key={i} eventKey={item.repo_name}>{item.repo_name}</MenuItem>
                    }):<MenuItem key={0} eventKey={0}>加载中...</MenuItem>}
                  </DropdownButton>

                  <Button className="icon-refresh" onClick = {this.selectCodeStore.bind(this,this.state.codeStoreKey,true)}> </Button>
                </ButtonGroup>
              }
              <span className="inputTip" ref = "btn_group_tip">代码仓库和项目名称不能为空</span>
            </div>
          </div>
          <div className="assItem">
            <HeadLine
              title="构建位置"
              titleEnglish="CONSTRUCTION POSITION"
              titleInfo="Dockerfile是指导镜像构建的描述文件，系统会根据您设置的构建目录查找Dockerfile并在该目录下执行镜像构建命令。"
            />
            <div className="assBox assBoxW100">
              <div className="assPosition">
                <FormGroup controlId="form">
                  <Col sm={2}>
                    构建目录
                  </Col>
                  <Col sm={5}>
                    <input className="form-control" defaultValue="/" ref = "dockerfile_name" type="text" placeholder="/" />
                  </Col>
                </FormGroup>
              </div>
              <div className="assPosition">
                <FormGroup controlId="form">
                  <Col sm={2}>
                    Dockerfile 路径
                  </Col>
                  <Col sm={5}>
                    <input className="form-control" defaultValue="Dockerfile" ref = "dockerfile_path" type="text" placeholder="Dockerfile" />
                  </Col>
                </FormGroup>
              </div>
            </div>
          </div>
          <div className="assItem">
            <HeadLine
              title="是否自动构建"
              titleEnglish="AUTO BUILDING"
              titleInfo="当代码仓库中的项目有 push 操作的时候, 该镜像也会同步自动重新构建"
            />
            <div className="assBox">
              <Toggle
                defaultChecked = {this.state.isAutoBuilding==1}
                onChange = {this.getToggleValue.bind(this)}
              />
            </div>
          </div>
          <div className="assItem">
            <HeadLine
              title="是否公开"
              titleEnglish="IS PUBLIC"
              titleInfo="是否对外开放您的镜像"
            />
            <div className="assBox">
              <Toggle
                defaultChecked = {this.state.isPublic==1}
                onChange = {this.changePublicToggleValue.bind(this)}
              />
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
                defaultValue=""
                ref = 'detail'
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
                defaultValue=""
                ref = 'short_description'
              />
            </div>
          </div>
          <div className="assItem assItemNoborder">
            <div className="acBtn">
              <button className={`btn btn-primary ${!this.props.isBtnState.building?"btn-loading":""}`}
                      onClick = {this.building.bind(this)}
                      disabled={!this.props.isBtnState.building}>
                      {this.props.isBtnState.building?"开始构建":"构建中..."}
                </button>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default BuildingCreate;
