
import React,{Component} from 'react';
import {SplitButton,MenuItem,
} from 'react-bootstrap';
import cx from 'classnames';
import Link from '../Link';
import Loading from '../Loading';
import Confirm from "../Confirm";
import {timeRange} from '../../core/utils';
import {BREADCRUMB} from "../../constants";

class Building extends Component {
  static contextTypes = {
    setTitle: React.PropTypes.func
  };
  constructor(){
    super();
    this.state = {
      githubModalShow: false,
      delData:{}
    }
  }
  static propTypes = {
    buildingImageList:React.PropTypes.array,
    onImageList:React.PropTypes.func,
    onFastBuilding:React.PropTypes.func,
    setBreadcrumb:React.PropTypes.func,
    onClearImageList:React.PropTypes.func,
    onDeleteImage:React.PropTypes.func
  };
  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.BUILD_IMAGE);
    this.props.onImageList();
    this.myTime = setInterval(this.props.onImageList,10000);
  }
  componentWillUnmount(){
    clearInterval(this.myTime);
  }

  getAddBtn() {
    return (
      <div className={cx("hbAdd", "left")}>
        <Link to={"/building/create"} className={cx("hbAddBtn", "clearfix")}>
          <div className={cx("hbPlus", "left")}></div>
          <div className={cx("hbPlusInfo", "left")}>
            <p className={"hbPName"}>代码构建</p>
            <p className={"hbPInfo"}>Code Build</p>
          </div>
        </Link>
      </div>
    )
  }
  deleteLine(name){
    this.setState({
      delData:{
        name:name,
        keyList:"buildingList"
      }
    });
    this.refs.confirmModal.open();
  }
  getSourceName(name){
    let _name;
    if(_name = /^https\:\/\/github.com\/([0-9a-zA-Z_-]+\/[0-9a-zA-Z_-]+)\.git$/.exec(name)){
      let style = {
        fontSize:'18px',
        verticalAlign:'middle',
        marginRight: '5px'
      };
      return <span><i className="icon-console" style={style}></i>{_name[1]}</span>
    }
    return null;
  }
  getLines(){
    let data = this.props.buildingImageList;
    if(!data.length) return <tr><td colSpan="6" style={{"textAlign":"center"}}>暂无数据~</td></tr>
    if(data.length == 1&&data[0] == 1) return <tr><td colSpan="6" style={{"textAlign":"center"}}><Loading /></td></tr>;
    if(data.length == 1&&data[0] == 0) return <tr><td colSpan="6" style={{"textAlign":"center"}}><Loading /></td></tr>
    let body = [];
    data.map((item,i)=>{
      let buildStatus = ["还未构建","构建成功","构建中","构建失败"][item.build_status];
      let buildUserTime = buildStatus =="还未构建"?"还未构建":Math.floor(item.use_time)+"秒";
      let prevUserTime = buildStatus =="还未构建"?"还未构建":timeRange(new Date(item.last_build));
      body.push(
        <tr key={i}>
          <td>
            <div className="mediaItem">
              <Link to={`/building/${item.uuid}`}>
                <img className="mediaImg" src = "/slImgJx.png" />
                <span className="mediaTxt">{item.repository}</span>
              </Link>
            </div>
          </td>
          <td>
            {item.src_url}
          </td>
          <td>{buildStatus}</td>
          <td>{buildUserTime}</td>
          <td>{prevUserTime}</td>
          <td>
            <SplitButton
              onClick={this.fastBuilding.bind(this,item.uuid)}
              onSelect={this.deleteLine.bind(this,item.repository)}
              bsStyle="primary" title="构建" id={`building-table-line-${i}`}>
              <MenuItem eventKey="1">删除</MenuItem>
            </SplitButton>
          </td>
        </tr>
      )
    });
    return body;
  }
  fastBuilding(id){
    let obj = {
      id:id,
      flag:"list"
    };
    this.props.onFastBuilding(obj)
  }
  refresh(){
    this.props.onClearImageList();
    this.props.onImageList();
  }
  render(){
    this.context.setTitle('构建镜像');
    return (
      <div className="containerBgF building-list">
        <div className={cx("hbHd","hbHdNoMb", "clearfix")}>
          {this.getAddBtn()}
          <div className="right slSearch">
            <button className="btn btn-default icon-refresh" onClick = {this.refresh.bind(this)} title="刷新"> </button>
          </div>
        </div>
        <div className="building-table TableTextLeft">
          <table className="table table-hover table-bordered">
            <thead>
            <tr>
              <th width = "30%">镜像名称</th>
              <th width = "30%">代码源</th>
              <th width = "10%">构建状态</th>
              <th width = "10%">上次构建用时</th>
              <th width = "10%">最近构建</th>
              <th width = "10%">操作</th>
            </tr>
            </thead>
            <tbody>
            {this.getLines()}
            </tbody>
          </table>
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

export default Building;
