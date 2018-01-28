
import React,{PropTypes,Component} from 'react';

import {Tabs,Tab,} from 'react-bootstrap';
import {BREADCRUMB} from "../../constants";
import GetOrgInfo from './GetOrgInfo';
import GetOrgDeal from './GetOrgDeal';
import GetOrgAdmin from './GetOrgAdmin';

const title = '组织中心';

class Organize extends  Component{
  static contextTypes = {
    setTitle: PropTypes.func.isRequired,
    store:React.PropTypes.object
  };
  static propTypes = {
    isBtnState:React.PropTypes.object,
    setBreadcrumb:React.PropTypes.func,
    getOrganizeDetail:React.PropTypes.func,
    organizeDetail:React.PropTypes.object,
    setOrganizeDetail:React.PropTypes.func,
    organizeUserList:React.PropTypes.array,
    getOrganizeUserList:React.PropTypes.func,
    userList:React.PropTypes.array,
    getUserList:React.PropTypes.func,
    inviteUser:React.PropTypes.func,
    changeOrganizeOwner:React.PropTypes.func,
    deleteOrganize:React.PropTypes.func,
    leaveOrganize:React.PropTypes.func
  };
  componentDidMount(){
    this.props.setBreadcrumb(BREADCRUMB.CONSOLE,BREADCRUMB.ORGANIZE)
  }
  render(){
    this.context.setTitle(title);
    return (
      <div className = "containerBgF">
        <div className = "userTab">
          <Tabs defaultActiveKey={4} id="userTabs">
            <Tab eventKey={1} title="账户信息">
            </Tab>
            <Tab eventKey={2} title="组织信息">
              <GetOrgInfo
                getOrganizeDetail = {(id) => {this.props.getOrganizeDetail(id)}}
                organizeDetail = {this.props.organizeDetail}
                setOrganizeDetail = {(data) => {this.props.setOrganizeDetail(data)}}
                isBtnState = {this.props.isBtnState}
              />
            </Tab>
            <Tab eventKey={3} title="交易记录">
              <GetOrgDeal />
            </Tab>
            <Tab eventKey={4} title="组织管理">
              <GetOrgAdmin
                organizeUserList = {this.props.organizeUserList}
                getOrganizeUserList={(id) =>{this.props.getOrganizeUserList(id)}}
                userList = {this.props.userList}
                getUserList={(name => {this.props.getUserList(name)})}
                inviteUser = {(data) => {this.props.inviteUser(data)}}
                changeUserRole = {(data) =>{this.props.changeUserRole(data)}}
                changeOrganizeOwner = {(data) =>{this.props.changeOrganizeOwner(data)}}
                deleteOrganize = {(id,flag) =>{this.props.deleteOrganize(id,flag)}}
                leaveOrganize = {(data) =>{this.props.leaveOrganize(data)}}
              />
            </Tab>
          </Tabs>
        </div>
      </div>
    )
  }

}

export default Organize
