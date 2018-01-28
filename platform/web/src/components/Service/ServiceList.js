/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React, { PropTypes,Component } from 'react';
import {SplitButton,MenuItem} from 'react-bootstrap';
import ReactDOM from 'react-dom';
import Link from '../Link';
import Loading from "../Loading";
import Confirm from "../Confirm";
import {BREADCRUMB} from "../../constants";
import * as Const from '../../constants';

const title = '服务列表';


class ServiceList extends Component{
  static contextTypes = {
    setTitle: PropTypes.func.isRequired,
    store:PropTypes.object
  };
  static propTypes = {
    serviceList: React.PropTypes.array,
    onServiceListLoad: React.PropTypes.func,
    onDeleteService: React.PropTypes.func,
    stepFunc: React.PropTypes.func,
    setBreadcrumb:React.PropTypes.func,
    onChangeState:React.PropTypes.func,
    onClearServiceList:React.PropTypes.func,
    isLoading:React.PropTypes.bool
  };
  constructor(){
    super();
    this.state = {
      isLoop: true,
      delData:{}
    }
  }
  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.SERVICE_LIST);
    this.props.onServiceListLoad();
    this.myTime = setInterval(this.props.onServiceListLoad,10000);
  }
  componentWillUnmount(){
    clearInterval(this.myTime)
  }

  deleteService(serviceName){
    let data = {serviceName:serviceName,type:"list"};
    this.setState({
      delData:data
    });
    this.refs.confirmModal.open();
  }
  changeState(serviceName,state){
    let data = {serviceName:serviceName,state:state};
    console.log(data);
    this.props.onChangeState(data)
  }
  getTableBody(){
    let data = this.props.serviceList;
    if(!data.length) return <tr><td colSpan="5" style={{"textAlign":"center"}}>暂无数据~</td></tr>;
    if(data.length == 1&&data[0] == 1) return <tr><td colSpan="5" style={{"textAlign":"center"}}><Loading /></td></tr>;
    if(data.length == 1&&data[0] == 0) return <tr><td colSpan="5" style={{"textAlign":"center"}}><Loading /></td></tr>;
    let body = [];
    data.map((item, i) => {
      let serviceState = "";
      let option = "";
      switch(item.fservice_status.toLowerCase()){
        case Const.SERVICE_STATE.Running:serviceState = "运行";
              option = <SplitButton
                onClick = {this.changeState.bind(this,item.fservice_name,"stop")}
                onSelect={this.deleteService.bind(this,item.fservice_name)}
                bsStyle={"default"}
                title='关闭' id={`volumes-table-line-${i}`}>
                <MenuItem eventKey="1">删除</MenuItem>
              </SplitButton>;
              break;
        case Const.SERVICE_STATE.Stopping:serviceState = "停止";
              option = <SplitButton
                onClick = {this.changeState.bind(this,item.fservice_name,"start")}
                onSelect={this.deleteService.bind(this,item.fservice_name)}
                bsStyle={"primary"}
                title={'启动'} id={`volumes-table-line-${i}`}>
                <MenuItem eventKey="1">删除</MenuItem>
              </SplitButton>;
              break;
        case Const.SERVICE_STATE.Pending :serviceState = "创建中";
              option = <SplitButton
                onClick={this.deleteService.bind(this,item.fservice_name)}
                bsStyle={"danger"}
                title={'删除'} id={`volumes-table-line-${i}`}>
              </SplitButton>;
              break;
        default:
          serviceState = "";
      }
      let domain = [];
      item.container.map((obj) =>{
        let url =  obj.http_domain == null ? obj.tcp_domain :obj.http_domain;
        domain.push(url)
      });
      body.push(
        <tr key={i}>
          <td>
            <div className="mediaItem">
                <Link to={`/serviceList/${item.fservice_name}/1`}>
                    <img className="mediaImg" src = "/slImgJx.png" />
                    <span className="mediaTxt">{item.fservice_name}</span>
                </Link>
            </div>
          </td>
          <td>
            <span className="color333">{item.ltime}</span>
          </td>
          <td>
            <div>
              {domain.map((url,j) =>{
                return <p key = {j}><a href={`http://${url}`} target = "_blank" className="clLink" >{url}</a></p>
              })}
            </div>
          </td>
          <td>
            <div
              className={`mirror-state ${serviceState == "运行" ? "on" : "off"} tablePaddingLeft`}>
              {serviceState}
            </div>
          </td>
          <td>
            <div className="btn-group">
              {option}
            </div>
          </td>
        </tr>
      )
    });
    return body;
  }
  getDemoTable(){
    return (
      <table className="table table-hover table-bordered services-table">
        <thead>
        <tr>
          <th width="20%">服务名称</th>
          <th width="10%">部署时间</th>
          <th width="45%">域名</th>
          <th width="10%">状态</th>
          <th width="15%">操作</th>
        </tr>
        </thead>
        <tbody ref = "tableBody">
        {this.getTableBody()}
        </tbody>
      </table>
    )
  }
  searchService(){
    let searchTxt = ReactDOM.findDOMNode(this.refs.searchInput).value;
    let my = this;
    my.props.onServiceListLoad(searchTxt);
    clearInterval(this.myTime);
    this.myTime = setInterval(function(){
      my.props.onServiceListLoad(searchTxt);
    },10000);
  }

  refresh(){// refresh
    this.props.onClearServiceList();
    this.props.onServiceListLoad();
  }
  render(){
    this.context.setTitle(title);
    return (
      <div className="containerBgF">
        <div className="hbHd clearfix">
          <div className="hbAdd left">
            <Link to={`/choseImage`}>
              <div className="hbAddBtn clearfix">
                <div className="hbPlus left"></div>
                <div className="hbPlusInfo left">
                  <p className="hbPName">新建服务</p>
                  <p className="hbPInfo">Create Service</p>
                </div>
              </div>
            </Link>
            <a href="javascript:;" className="hbAddExplain">什么是容器云服务？</a>
          </div>
          <div className="slSearch right">
            <button className="btn btn-default icon-refresh" onClick = {this.refresh.bind(this)} title = "刷新"> </button>
            <div className="search">
              <input type="text" placeholder='搜索服务' ref="searchInput" className={"slSearchInp"}/>
              <a type="button" className="slSearchBtn icon-select" onClick = {this.searchService.bind(this)}> </a>
            </div>
          </div>
        </div>
        <div className="sl-bd TableTextLeft">
          {this.getDemoTable()}
        </div>
        <Confirm
          title = "警告"
          text = "您确定要删除此服务吗?"
          ref = "confirmModal"
          func = {() => {this.props.onDeleteService(this.state.delData)}}
        />
      </div>
    );
  }
}

export default ServiceList;
