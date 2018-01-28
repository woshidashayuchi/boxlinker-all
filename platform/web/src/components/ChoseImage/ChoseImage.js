/**
 * Created by zhangsai on 16/9/18.
 */

import React, { PropTypes,Component } from 'react';
import ServiceStep from '../../components/ServiceStep';
import HeadLine from '../../components/HeadLine';
import Tabs from 'react-bootstrap/lib/Tabs';
import Tab from 'react-bootstrap/lib/Tab';
import Link from '../Link';
import Loading from '../Loading';
import {BREADCRUMB} from "../../constants";
import {timeRange} from '../../core/utils'
const title = '新建服务';

class ChooseImage extends Component{
  static contextTypes = {
    setTitle: PropTypes.func.isRequired,
    store: React.PropTypes.object
  };
  static propTypes = {
    imageList:React.PropTypes.array,
    onImageListLoad:React.PropTypes.func,
    deployData:React.PropTypes.object,
    goToConfigContainer:React.PropTypes.func,
    setBreadcrumb:React.PropTypes.func
  };

  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.ADD_SERVICE,BREADCRUMB.CHOSE_IMAGE);
    this.props.onImageListLoad(false);
  }

  deployImage(ImageName,id){
    let data = {
      image_name :`index.boxlinker.com/${ImageName}`,
      image_id:id
    };
    this.props.goToConfigContainer(data);
  }
  tabSelect(key){
    switch (key){
      case 1:
        this.props.onImageListLoad(false);
        break;
      case 3:
        this.props.onImageListLoad(true);
      default:
        break;
    }
  }
  getTableBody(){
    let data = this.props.imageList;
    if(!data.length){return <tr><td colSpan="5" style={{"textAlign":"center"}}>暂无数据~</td></tr>}
    if(data.length == 1&&data[0] == 1) return <tr><td colSpan="5" style={{"textAlign":"center"}}><Loading /></td></tr>;
    let body = [];
    data.map((item,i) => {
        body.push(  <tr key={i}>
            <td>
              <div className="mediaItem">
                <Link to={`/imageDetail/${item.uuid}`}>
                  <img className="mediaImg" src = "/slImgJx.png" />
                  <span className="mediaTxt">{item.repository}</span>
                </Link>
              </div>
            </td>
            <td>
              <span className="cl6">{timeRange(new Date(item.update_time))}</span>
            </td>
            <td>
              <span className="cl6">{`docker pull index.boxlinker.com/${item.repository}`}</span>
            </td>
            <td>
              <span className="cl3">{item.short_description}</span>
            </td>
            <td>
              <button className="btn btn-sm btn-primary"
                    onClick = {this.deployImage.bind(this,item.repository,item.uuid)}>部署</button>
            </td>
          </tr>)
    });
    return body;
  }

  getDemoTable(){
    return (
      <table className="table table-hover table-bordered">
        <thead>
        <tr>
          <th width="25%">镜像名称</th>
          <th width="10%">最近更新</th>
          <th width="35%">拉取命令</th>
          <th width="20%">镜像描述</th>
          <th width="10%">操作</th>
        </tr>
        </thead>
        <tbody>
        {this.getTableBody()}
        </tbody>
      </table>
    )
  }
  render(){
    this.context.setTitle(title);
    return (
      <div className="containerBgF">
        <div className = "asTab">
          <ServiceStep dataActive = "first"/>
          <div className = "asHd clearfix">
            <div className = "left">
              <HeadLine
                title = "选择镜像"
                titleEnglish = "SELECT MIRROR"
                titleInfo = "这里里汇聚了构建产生的所有容器云镜像"
              />
            </div>
            <div className = "right">
              <div className="search">
                <input type="text" placeholder='搜索镜像' ref="searchInput" className="slSearchInp"/>
                <a type="button" className="slSearchBtn icon-select" > </a>
              </div>
            </div>
          </div>
          <div className = "asTabs">
            <Tabs defaultActiveKey = {1} onSelect={this.tabSelect.bind(this)} id="asTabs">
              <Tab eventKey = {1} title = "我的镜像">
                <div className = "asTableBox TableTextLeft">
                  {this.getDemoTable()}
                </div>
              </Tab>
              {/*<Tab eventKey = {2} title = "镜像仓库">*/}
              {/*<div className = {cx(s.asTableBox,"TableTextLeft")}>*/}
              {/*{this.getDemoTable()}*/}
              {/*</div>*/}
              {/*</Tab>*/}
              <Tab eventKey = {3} title = "平台镜像">
                <div className = "asTableBox TableTextLeft">
                  {this.getDemoTable()}
                </div>
              </Tab>
            </Tabs>
          </div>
        </div>
      </div>
    );
  }
}
export default ChooseImage;
