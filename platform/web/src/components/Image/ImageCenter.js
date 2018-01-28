
import React from 'react';
import {Panel,Grid,Row,Col,DropdownButton,MenuItem,Checkbox,Button} from 'react-bootstrap';
import {BREADCRUMB} from "../../constants";


class ImageCenter extends React.Component{
  static contextTypes = {
    setTitle: React.PropTypes.func
  };

  static propTypes = {
    imageList : React.PropTypes.array,
    onImageList : React.PropTypes.func,
    setBreadcrumb:React.PropTypes.func
  };
  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.SERVICE_LIST);
    this.props.onImageList();
  }
  getImageList(){
    let data = this.props.imageList;
    return data.map((item,i) => {
      return (
        <div className="imagesListItem" key = {i}>
          <div className="hd">
            <div className="imagesListHd">
              <Checkbox readOnly />
              <img width={40} height={40} src={require('./imgHd.png')} alt="img"/>
            </div>
            <div className="imagesListInfo">
              <h1>镜像名称</h1>
              <p><a href="javascript:;">{item}</a></p>
            </div>
          </div>
          <div className="bd clearfix">
            <span className="icon-collection">收藏</span>{/*icon-collectctd*/}
            <Button bsStyle="primary" bsSize="small">部署</Button>
          </div>
        </div>
      )
    })
  }
  getImageTopTen(n){
    let data = this.props.imageList;
    return data.map((item,i) => {
      if(i>=n){
        return false;
      }else {
        return (
          <div className="imagesListItem" key={i}>
            <div className="hd">
              <div className="imagesListHd">
                <img width={40} height={40} src={require('./imgHd.png')} alt="img"/>
              </div>
              <div className="imagesListInfo">
                <h1>镜像名称</h1>
                <p><a href="javascript:;">{item}</a></p>
              </div>
            </div>
          </div>
        )
      }
    })
  }
  render(){
    this.context.setTitle('镜像中心');
    const panelHd=(<div className="clearfix imgHd">
              <span>镜像仓库</span>
              <a href="javascript:;">什么是容器镜像？</a>
              <div className="imgDropBox">
                <DropdownButton bsSize="xs" title="操作" id="dropDown" className="dropDownForOpt">
                  <MenuItem eventKey="1">全选</MenuItem>
                  <MenuItem eventKey="2">删除</MenuItem>
                  <MenuItem eventKey="2">置顶</MenuItem>
                </DropdownButton>
              </div>
      </div>);
    return (
      <div className="images containerPadding">
        <Panel className="image-left" header={panelHd}>
          <div className="imagesListBox">
            {this.getImageList()}
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
      </div>
    )
  }
}

export default ImageCenter;
