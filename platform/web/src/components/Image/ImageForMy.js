
import React from 'react';

import {Panel,MenuItem,Tab,Tabs,SplitButton} from 'react-bootstrap';
import {BREADCRUMB} from "../../constants";
import Link from '../Link';
import Loading from '../Loading';
import Confirm from '../Confirm';
import {navigate} from '../../actions/route';

class ImageForMy extends React.Component{
  static contextTypes = {
    setTitle: React.PropTypes.func,
    store: React.PropTypes.object,
  };
  static propTypes = {
    imageList : React.PropTypes.array,
    onImageList : React.PropTypes.func,
    setBreadcrumb:React.PropTypes.func,
    goToConfigContainer:React.PropTypes.func,
    onDeleteImage:React.PropTypes.func
  };
  constructor(){
    super();
    this.state = {
      delData:{}
    }
  }
  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.IMAGES_MY);
    this.props.onImageList();
  }
  deployImage(ImageName,id){
    let obj = {
      image_name :`index.boxlinker.com/${ImageName}`,
      image_id:id
    };
    this.props.goToConfigContainer(obj);
  }
  onSelectBtn(name,uuid,key){
    switch (key){
      case "1":
        this.context.store.dispatch(navigate(`/reviseImage/${uuid}`));
        break;
      case "2":
        this.setState({
          delData:{
            name:name,
            keyList:"imageList"
          }
        });
        this.refs.confirmModal.open();
        break;
    }
  }
  getImageList(){
    let data = this.props.imageList;
    if(!data || !data.length) return <div>暂无数据~</div>;
    if(data.length == 1&&data[0] == 1) return <div className="text-center"><Loading /></div>;
    let body = [];
    data.map((item,i) => {
      body.push(
        <div className="imagesListItem" key = {i}>
          <div className="hd">
            <div className="imagesListHd">
              <img width={40} height={40} src={require('./imgHd.png')} alt="img"/>
            </div>
            <div className="imagesListInfo">
              <h1>镜像名称 : <Link  to={`/imageDetail/${item.uuid}`}>{item.repository}</Link></h1>
              <p>镜像简介 : {item.detail}</p>
            </div>
          </div>
          <div className="bd clearfix">
            <span className="icon-collection">收藏</span>{/*icon-collectctd*/}
            <SplitButton
              title = "部署"
              bsStyle = "primary"
              bsSize="small"
              onClick = {this.deployImage.bind(this,item.repository,item.uuid)}
              onSelect={this.onSelectBtn.bind(this,item.repository,item.uuid)}
              id = {`deploy-${i}`}
            >
              <MenuItem eventKey="1">编辑</MenuItem>
              <MenuItem eventKey="2">删除</MenuItem>
            </SplitButton>
          </div>
        </div>
      )
    });
    return body
  }
  getImageTopTen(n){
    let data = this.props.imageList;
    let body = [];
    data.map((item,i) => {
      body.push(<div className="imagesListItem" key={i}>
        <div className="hd">
          <div className="imagesListHd">
            <img width={40} height={40} src={require('./imgHd.png')} alt="img"/>
          </div>
          <div className="imagesListInfo">
            <h1>镜像名称</h1>
            <p><Link to={`/imageDetail/${item.uuid}`}>{item.repository}</Link></p>
          </div>
        </div>
      </div>)
    });
    return body.splice(0,n)
  }
  tabSelect(){

  }
  render(){
    this.context.setTitle('我的镜像');
    const panelHd=(<div className="clearfix imgHd">
      <span>镜像仓库</span>
      <a href="javascript:;">什么是容器镜像？</a>
      <div className="imgDropBox"></div>
    </div>);
    return (
      <div className="images containerPadding">
        <Panel className="image-left" header={panelHd}>
          <div className="imagesListBox asTabs">
            <Tabs defaultActiveKey = {1} onSelect={this.tabSelect.bind(this)} id="asTabs">
              <Tab eventKey = {1} title = "我的镜像">
                <div className = "asTableBox TableTextLeft">
                  {this.getImageList()}
                </div>
              </Tab>
              <Tab eventKey = {2} title = "我的收藏">
                <div className = "asTableBox TableTextLeft">
                  {this.getImageList()}
                </div>
              </Tab>
            </Tabs>
          </div>
        </Panel>
        <div className="image-right">
          <div className="imageSearch">
            <div className="search">
              <input type="text" placeholder='搜索镜像' ref="searchInput" className="slSearchInp"/>
              <a type="button" className="slSearchBtn icon-select" > </a>
            </div>
          </div>
          <Panel className="imagesRankingList" header="排行榜">
            {this.getImageTopTen(10)}
          </Panel>
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

export default ImageForMy;
