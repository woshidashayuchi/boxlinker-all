/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React, { PropTypes,Component } from 'react';
import cx from 'classnames';
import VolumeCreateModal from './VolumeCreateModal'
import VolumeScaleModal from './VolumeScaleModal'
import {SplitButton,MenuItem} from 'react-bootstrap'
import { BREADCRUMB } from '../../constants';
import Loading from "../Loading";
import Confirm from '../Confirm';
const title = '数据卷列表';



class VolumeList extends Component{
  static contextTypes = {setTitle: PropTypes.func.isRequired};
  static propTypes = {
    onVolumeDelete: React.PropTypes.func,
    onVolumeCreate: React.PropTypes.func,
    onVolumeScale: React.PropTypes.func,
    onVolumesListLoad: React.PropTypes.func,
    setBreadcrumb: React.PropTypes.func,
    volumesList: React.PropTypes.array,
    onClearVolumesList:React.PropTypes.func,
    isBtnState:React.PropTypes.object
  };
  constructor(){
    super();
    this.state = {
      diskName:""
    }
  }
  getCreateBtn(){
     return (
       <div className={cx("hbAddBtn", "clearfix")} onClick={()=>{this.refs.createModal.open()}}>
         <div className={cx("hbPlus", "left")}></div>
         <div className={cx("hbPlusInfo", "left")}>
           <p className={"hbPName"}>创建存储卷</p>
           <p className={"hbPInfo"}>Create a volume</p>
         </div>
       </div>
     )
  }
  deleteLine(diskName){
    this.setState({
      diskName:diskName
    });
    this.refs.confirmModal.open();
  }
  createVolume(data){
    this.props.onVolumeCreate(data);
    this.refs.createModal.hide();
  }
  scaleVolume(diskName,diskSize){
    this.props.onVolumeScale(diskName,diskSize)
    this.refs.scaleModal.hide();
  }
  getDiskSize(size){
    return (parseInt(size)/1024) + 'G'
  }
  getTableLine(){
    let data = this.props.volumesList;
    if(!data.length) return <tr><td colSpan="6" style={{"textAlign":"center"}}>暂无数据~</td></tr>
    if(data.length == 1&&data[0] == 1) return <tr><td colSpan="6" style={{"textAlign":"center"}}><Loading /></td></tr>
    if(data.length == 1&&data[0] == 0) return <tr><td colSpan="6" style={{"textAlign":"center"}}><Loading /></td></tr>
    let body = [];
    data.map((item,i)=>{
      body.push(<tr key={i}>
        <td>
          <div className="mediaItem">
              <img className="mediaImg" src = "/slImgJx.png" />
              <span className="mediaTxt">{item.disk_name}</span>
          </div>
        </td>
        <td><span className="cl3">{item.create_time}</span></td>
        <td>{item.fs_type}</td>
        <td><div
          className={cx("mirror-state",item.disk_status == "unused"?"off":"on")}>
          {item.disk_status == "unused"?'未使用':'使用中'}
        </div></td>
        <td>
          <span className="cl3">{this.getDiskSize(item.disk_size)}</span>
        </td>
        <td>
          <div className="btn-group">
            <SplitButton
              onClick={()=>{this.refs.scaleModal.open(item)}}
              onSelect={this.deleteLine.bind(this,item.disk_name)}
              bsStyle="primary" title="扩容" id={`volumes-table-line-${i}`}>
              <MenuItem eventKey="1">删除</MenuItem>
            </SplitButton>

          </div>
        </td>
      </tr>)
      })
    return body
  }
  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.VOLUMES);
    this.props.onVolumesListLoad();
    this.myTime = setInterval(this.props.onVolumesListLoad,10000);
  }
  componentWillUnmount(){
    clearInterval(this.myTime);
  }
  refresh(){
    this.props.onClearVolumesList();
    this.props.onVolumesListLoad();
  }
  render(){
    this.context.setTitle(title)
    return (
      <div className="containerBgF">
        <div className={cx("hbHd", "clearfix")}>
          <div className={cx("hbAdd", "left")}>
            {this.getCreateBtn()}
            <a href="javascript:;" className={"hbAddExplain"}>什么是存储卷？</a>
          </div>
          <div className="right slSearch">
            <button className="btn btn-default icon-refresh" onClick = {this.refresh.bind(this)} title="刷新"> </button>
          </div>
        </div>
        <div className="TableTextLeft" style={{padding:"15px"}}>
          <table className="table table-hover table-bordered volumes-table">
            <thead>
            <tr>
              <th width = "20%">存储卷名称</th>
              <th width = "20%">创建时间</th>
              <th width = "15%">存储格式</th>
              <th width = "15%">状态</th>
              <th width = "15%">容量</th>
              <th width = "15%">操作</th>
            </tr>
            </thead>
            <tbody>
            {this.getTableLine()}
            </tbody>
          </table>
        </div>
        <VolumeScaleModal ref="scaleModal" onSave={this.scaleVolume.bind(this)}/>
        <VolumeCreateModal ref="createModal" isBtnState = {this.props.isBtnState} onVolumeCreate={this.createVolume.bind(this)}/>
        <Confirm
          title = "警告"
          text = "您确定要删除此数据卷吗?"
          ref = "confirmModal"
          func = {() => {this.props.onVolumeDelete(this.state.diskName)}}
        />
      </div>
    );
  }
}

export default VolumeList;
