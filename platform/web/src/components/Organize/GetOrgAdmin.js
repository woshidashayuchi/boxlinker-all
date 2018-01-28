import React,{PropTypes,Component} from 'react';
import HeadLine from '../HeadLine';
import Loading from '../Loading';
import {DropdownButton,MenuItem} from 'react-bootstrap';
import Confirm from '../Confirm';
import {navigate} from '../../actions/route';
import {receiveNotification,clearNotification} from "../../actions/notification";

class GetOrgAdmin extends Component{
  static contextTypes = {
    store:React.PropTypes.object
  };
  static propTypes = {
    organizeUserList:React.PropTypes.array,
    getOrganizeUserList:React.PropTypes.func,
    getUserList:React.PropTypes.func,
    userList:React.PropTypes.array,
    inviteUser:React.PropTypes.func,
    changeUserRole:React.PropTypes.func,
    changeOrganizeOwner:React.PropTypes.func,
    deleteOrganize:React.PropTypes.func,
    leaveOrganize:React.PropTypes.func
  };

  constructor(props){
    super(props);
    this.state = {
      inviteBox:false,
      roleData:{},
      deleteData:{},
      leaveData:{}
    }
  }
  componentWillMount(){
    let is_user = this.context.store.getState().user_info.is_user;
    if(is_user == 1){
      this.context.store.dispatch(navigate("/"));
    }
  }
  componentDidMount(){
    let organizeId = this.context.store.getState().user_info.orga_uuid;
    this.props.getOrganizeUserList(organizeId);
  }
  getOrganizeUserBody(){
    let user_name = this.context.store.getState().user_info.user_name;
    let orgRole = Number(this.context.store.getState().user_info.role_uuid);
    let data = this.props.organizeUserList;
    if(data[0] == 1) return <tr><td colSpan = "3" style = {{textAlign:"center"}}><Loading /></td></tr>;
    if(!data.length) return <tr><td colSpan = "3" style = {{textAlign:"center"}}>暂无数据~</td></tr>;
    return data.map((item,i) =>{
      let role = "";
      let buttonGroup = "";
      switch (Number(item.role)){
        case 200:
          role = "组织创建者";
          buttonGroup =  <div className="roleBox">
            <button disabled = {orgRole != 200}
                    onClick={this.onDeleteOrganize.bind(this)}
                    className="btn btn-danger">解散组织</button>
          </div>;
          break;
        case 210 :
          role = "管理员";
          buttonGroup = <div className="roleBox">
            <DropdownButton
              onSelect = {this.onChangeUserRole.bind(this,item.uid)}
              bsStyle={"primary"}
              disabled = {orgRole != 200 && user_name != item.user_name}
              title={'更改权限'} id={`volumes-table-line-${i}`}>
              <MenuItem eventKey="400">用户</MenuItem>
              {orgRole == 200?<MenuItem eventKey="520">组织创建者</MenuItem>:""}
            </DropdownButton>
            {user_name == item.user_name?
              <button className="btn btn-danger"
                onClick={this.onLeaveOrganize.bind(this)}
              >离开组织</button>:
              <button className="btn btn-danger"
                      onClick={this.onDeleteUser.bind(this,item.uid)}
                      disabled={orgRole != 200}>移除组织</button>
            }

          </div>;
          break;
        case 400 :
          role = "成员";
          buttonGroup = <div className="roleBox">
             <DropdownButton
              onSelect = {this.onChangeUserRole.bind(this,item.uid)}
              bsStyle={"primary"}
              disabled = {orgRole != 200}
              title={'更改权限'} id={`volumes-table-line-${i}`}>
              {orgRole == 200?<MenuItem eventKey="210">管理员</MenuItem>:""}
              {orgRole == 200?<MenuItem eventKey="520">组织创建者</MenuItem>:""}
            </DropdownButton>
            {user_name == item.user_name?
              <button className="btn btn-danger"
                      onClick={this.onLeaveOrganize.bind(this)}
              >离开组织</button>:
              <button className="btn btn-danger"
                      disabled={orgRole == 400}
                      onClick={this.onDeleteUser.bind(this,item.uid)}
              >移除组织</button>
            }
          </div>;
          break;
        default :
          role = "成员";
          buttonGroup = <div className="roleBox">
            <DropdownButton
              onSelect = {this.onChangeUserRole.bind(this,item.uid)}
              bsStyle={"primary"}
              disabled = {orgRole == 400 && user_name != item.user_name}
              title={'更改权限'} id={`volumes-table-line-${i}`}>
              {orgRole == 200?<MenuItem eventKey="210">管理员</MenuItem>:""}
              {orgRole == 200?<MenuItem eventKey="520">组织创建者</MenuItem>:""}
            </DropdownButton>
            {user_name == item.user_name?<button className="btn btn-danger">离开组织</button>:""}
            {orgRole == 200 || orgRole ==210 ?<button className="btn btn-danger">移除组织</button>:""}
          </div>;

      }
      return (
        <tr key = {i}>
          <td>
            <div className="mediaItem">
              <img className="mediaImg" src = "/slImgJx.png" />
              <span className="mediaTxt">{item.user_name}</span>
            </div>
          </td>
          <td>{role}</td>
          <td>
            {buttonGroup}
          </td>
        </tr>
      )
    })
  }
  getTableDemo(){
    return (
      <table className="table table-hover table-bordered">
        <thead>
        <tr>
          <th width = "33%">用户名</th>
          <th width = "33%">权限信息</th>
          <th width = "34%">操作</th>
        </tr>
        </thead>
        <tbody>
        {this.getOrganizeUserBody()}
        </tbody>
      </table>
    )
  }
  getUserListFun(e){
    let name = e.target.value;
    if(name.length >=3) {
      this.setState({
        inviteBox:true
      });
      this.props.getUserList(name);
    }
  };
  getUserListBody(){
    let userList = this.props.userList;
    let my = this;
    if(userList && userList.length) {
      let body = userList.map((item, i) => {
        return (<li key = {i} onClick = {my.choseInviteName.bind(my,item.username)}>
                  <img width={40} height={40} src={item.logo||require('./imgHd.png')} />
                  <p>{item.username}</p>
                  <p>{item.email}</p>
        </li>)
      });
      return body;
    }else{
      return <li>暂无数据</li>
    }
  }
  inviteInputBlur(){
    let my = this;
    setTimeout(function(){
      my.setState({
        inviteBox:false
      })
    },200);
  }
  choseInviteName(name){
    console.log(name);
    this.refs.username.value = name;
  }
  onInviteUser(){
    let userList = this.props.userList;
    let userInfo = this.refs.username.value;
    let orga_id = this.context.store.getState().user_info.orga_uuid;
    let data = {};
    userList.map((item)=>{
      if(item.username == userInfo || item.email == userInfo){
        data = {
          user_id:item.user_id,
          orga_id:orga_id
        };
      }
    });
    if(data.user_id){
      this.props.inviteUser(data);
    }else{
      this.context.store.dispatch(receiveNotification({message:"没有找到此用户",level:"danger"}));
      let my = this;
      setTimeout(function(){
        my.context.store.dispatch(clearNotification());
      },3000);
    }
  }
  onChangeUserRole(user_uuid,key){
    let orga_uuid = this.context.store.getState().user_info.orga_uuid;
    let data = {
      orga_uuid:orga_uuid,
      user_uuid:user_uuid,
      role_uuid:key,
      method:"PUT"
    };
    console.log(key);
    if(key == 520){
      this.props.changeOrganizeOwner(data);
    }else {
      this.props.changeUserRole(data);
    }
  }
  onDeleteUser(user_uuid){
    let orga_uuid = this.context.store.getState().user_info.orga_uuid;
    this.setState({
      roleData: {
        orga_uuid: orga_uuid,
        user_uuid: user_uuid,
        role_uuid: "",
        method: "DELETE"
      }
    });
    this.refs.confirmModal.open();
  }
  onDeleteOrganize(){
    let orga_uuid = this.context.store.getState().user_info.orga_uuid;
    this.setState({
      orgData:{
        orgId:orga_uuid,
        keyList:"userList"
      }
    });
    this.refs.confirmModalDelete.open();
  }
  onLeaveOrganize(){
    let orgId = this.context.store.getState().user_info.orga_uuid;
    this.setState({
      leaveData:{
        orgId:orgId,
        keyList:"userList"
      }
    });
    this.refs.confirmModalLeave.open();
  }

  render(){
    let role = this.context.store.getState().user_info.role_uuid;
    return (
      <div className="organize">
        {role == 400 ? "" :
          <div className="organizeHd">
            <HeadLine
              title="邀请新成员"
              titleEnglish="INVITE USER"
              titleInfo="邀请新成员"
            />
            <div className="inviteUser">
              <input type="text" className="form-control inviteUserInput"
                     ref="username"
                     onInput={this.getUserListFun.bind(this)}
                     onBlur={this.inviteInputBlur.bind(this)}
              />
              <button className="btn btn-primary" onClick = {this.onInviteUser.bind(this)}>邀请</button>
              <ul className={this.state.inviteBox ? "inviteShow" : "inviteHide"}>
                {this.getUserListBody()}
              </ul>
            </div>
          </div>
        }
        <div className="organizeBd sl-bd TableTextLeft">
          <HeadLine
            title = "组织成员"
            titleEnglish = "ORGANIZE USER LIST"
            titleInfo = "组织成员列表"
          />
          <div className="organizeUserTab">
            {this.getTableDemo()}
          </div>
        </div>
        <Confirm
          title = "警告"
          text = "您确定要移除此用户吗?"
          ref = "confirmModal"
          func = {() => {this.props.changeUserRole(this.state.roleData)}}
        />
        <Confirm
          title = "警告"
          text = "您确定要离开此组织吗?"
          ref = "confirmModalLeave"
          func = {() => {this.props.leaveOrganize(this.state.leaveData)}}
        />
        <Confirm
          title = "警告"
          text = "您确定要解散此组织吗?"
          ref = "confirmModalDelete"
          func = {() => {this.props.deleteOrganize(this.state.orgData)}}
        />

      </div>
    )
  }
}

export default  GetOrgAdmin;
