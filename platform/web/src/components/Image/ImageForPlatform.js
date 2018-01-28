
import React from 'react';
import {Panel} from 'react-bootstrap';
import {BREADCRUMB} from "../../constants";
import Link from '../Link';
import Loading from '../Loading';


class ImageForPlatform extends React.Component{
  static contextTypes = {
    setTitle: React.PropTypes.func
  };
  static propTypes = {
    imageList : React.PropTypes.array,
    onImageList : React.PropTypes.func,
    setBreadcrumb:React.PropTypes.func,
    deployImageName:React.PropTypes.func
  };
  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.IMAGES_BOX_LINKER);
    this.props.onImageList(true);
  }
  deployImage(ImageName,id){
    let obj = {
      image_name :`index.boxlinker.com/${ImageName}`,
      image_id:id
    };
    this.props.goToConfigContainer(obj);
  }
  getImageList(){
    let data = this.props.imageList;
    if(!data || !data.length) return <div>暂无数据~</div>;
    if(data.length == 1&&data[0] == 1) return <div className="text-center"><Loading /></div>;
    let body = [];
    data.map((item,i) => {
        body.push(<div className="imagesListItem" key={i}>
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
              <Link to={`/configContainer`} className="btn btn-sm btn-primary"
                    onClick={this.deployImage.bind(this,item.repository,item.uuid)}>部署</Link>
            </div>
          </div>
        )
    });
    return body;
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
  render(){
    this.context.setTitle('平台镜像');
    const panelHd=(<div className="clearfix imgHd">
      <span>镜像仓库</span>
      <a href="javascript:;">什么是容器镜像？</a>
      <div className="imgDropBox">
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

export default ImageForPlatform;
