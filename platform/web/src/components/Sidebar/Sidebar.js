import React, { Component } from "react";
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import cx from 'classnames';
import s from "./Sidebar.css"
import Link from "../Link"
import cookie from 'react-cookie'
import {Collapse,Tooltip,Overlay} from 'react-bootstrap';

function showIcon(className){
  return <i className={cx(s.listFA,className)}> </i>
}

class MenuListItem extends Component{
  static propTypes = {
    href: React.PropTypes.string.isRequired,
    icon: React.PropTypes.element.isRequired,
  };
  render(){
    return (
      <Link to={this.props.href} onClick={this.props.onClick}>
        {this.props.icon}
        {this.props.children}
        {this.props.rightIcon}
      </Link>
    )
  }
}
class MenuList extends Component{
  constructor(...args){
    super(...args);
    this.state = {
      open: true
    };
  }
  handleClick(){
    this.setState({
      open:!this.state.open
    });
  }
  render(){
    return <ul className={s.list}>
      <li><MenuListItem
        href="javascript:void(0)"
        icon={this.props.icon}
        rightIcon={<i className={cx(s.toggler,this.state.open?s.togglerOpen:'')}> </i>}
        onClick={this.handleClick.bind(this)}
      >
        {this.props.title}
      </MenuListItem></li>
      <li>
        <Collapse in={this.state.open}>
          {this.props.children}
        </Collapse>
      </li>
    </ul>
  }
}

class ThinItem extends Component {
  static propTypes = {
    icon: React.PropTypes.element.isRequired,
    tip: React.PropTypes.string.isRequired,
    href: React.PropTypes.string,
    onClick: React.PropTypes.func,
    open:React.PropTypes.bool,
    isOpen:React.PropTypes.bool,
    className:React.PropTypes.string
  };
  constructor(props){
    super(props)
    this.state = {
      tipShow: false
    }
    //menu-item
  }
  render(){
    return (
      <div>
        <Link to={this.props.href} onClick={this.props.onClick}
              className={this.props.href == "javascript:;" && this.props.open ? "menu-item menuItemAction" :`menu-item ${this.props.className}`}>
          {this.props.icon}
        </Link>
        <div className="thin-item-tip">{this.props.tip}</div>
        <Overlay placement="right">
          <Tooltip id="overload-right">Tooltip overload!</Tooltip>
        </Overlay>
      </div>
    )
  }
}

class ThinList extends Component{
  static propTypes = {
    href:React.PropTypes.string,
    className:React.PropTypes.string,
    onClick:React.PropTypes.func
  };
  constructor(props){
    super(props);
    this.state = {
      collapse: true
    };
  }
  handleClick(){
    this.props.onClick();
    this.setState({
      collapse: !this.state.collapse
    })
  }
  render(){
    return (
      <div>
        <ThinItem href={this.props.href != "javascript:;" ? this.props.href:"javascript:;"}
                  open={this.state.collapse}
                  isOpen={this.props.isOpen}
                  onClick={this.handleClick.bind(this)}
                  icon={this.props.icon}
                  tip={this.props.title}
                  className={this.props.className}

        />
        <Collapse in={this.state.collapse}>
          <div>
            {this.props.children}
          </div>
        </Collapse>
      </div>
    )
  }
}

class Sidebar extends Component {
  static contextTypes = {
    store: React.PropTypes.object
  };
  static propTypes = {
    isSidebarOpen: React.PropTypes.bool,
    sidebarActive:React.PropTypes.string,
    onChangeSidebarActive:React.PropTypes.func
  };
  onChangeAction(url){
    var exp = new Date();
    exp.setTime(exp.getTime()+1000*60*60*24*7);
    cookie.save('sidebarActive',url,{path:'/',expires: exp});
    this.props.onChangeSidebarActive(url);
  }
  getLogo(){
    let open = this.props.isSidebarOpen;
    return (
      open?
        <div className={s.logo}>
          <a href="/"><img src="/logo.png"/></a>
        </div>:
        <div className={cx(s.logo,s.logoSmall)}>
          <a href="/"><img src="/logo-small.png"/></a>
        </div>
    )
  }
  getList(){
    let open = this.props.isSidebarOpen;
    let is_user = this.context.store.getState().user_info.is_user;
    return (
      open?
        <div className={s.listPack}>
          <div className={s.menuList}>
            <ul className={cx(s.list,"sidebar-menu-list")}>
              <li onClick = {this.onChangeAction.bind(this,"/")}
                  className={this.props.sidebarActive =="/"?"subListAction":""}><MenuListItem href="/" icon={showIcon("icon-console")}>控制台</MenuListItem></li>
            </ul>
            <MenuList title="服务中心" icon={showIcon("icon-servicecenter")}>
              <ul className={s.subList}>
                <li onClick = {this.onChangeAction.bind(this,"/choseImage")}
                    className={this.props.sidebarActive =="/choseImage"?"subListAction":""}>
                  <MenuListItem href="/choseImage" icon={showIcon("icon-New-service")}>新建服务</MenuListItem>
                </li>
                <li onClick = {this.onChangeAction.bind(this,"/serviceList")}
                    className={this.props.sidebarActive =="/serviceList"?"subListAction":""}>
                  <MenuListItem href="/serviceList" icon={showIcon("icon-servicelist")}>服务列表</MenuListItem>
                </li>
                <li onClick = {this.onChangeAction.bind(this,"/volumes")}
                    className={this.props.sidebarActive =="/volumes"?"subListAction":""}>
                  <MenuListItem href="/volumes" icon={showIcon("icon-storagemanag")}>存储卷管理</MenuListItem></li>
              </ul>
            </MenuList>
            <MenuList title="镜像中心" icon={showIcon("icon-mirrorceer")}>
              <ul className={s.subList}>
                <li onClick = {this.onChangeAction.bind(this,"/createImage")}
                    className={this.props.sidebarActive =="/createImage"?"subListAction":""}>
                  <MenuListItem href="/createImage" icon={showIcon("icon-mirrorhouse")}>新建镜像</MenuListItem></li>
                <li onClick = {this.onChangeAction.bind(this,"/imageForMy")}
                    className={this.props.sidebarActive =="/imageForMy"?"subListAction":""}>
                  <MenuListItem href="/imageForMy" icon={showIcon("icon-mymirror")}>我的镜像</MenuListItem></li>
                <li onClick = {this.onChangeAction.bind(this,"/imageForPlatform")}
                    className={this.props.sidebarActive =="/imageForPlatform"?"subListAction":""}>
                  <MenuListItem href="/imageForPlatform" icon={showIcon("icon-formmirror")}>平台镜像</MenuListItem></li>
                <li onClick = {this.onChangeAction.bind(this,"/building")}
                    className={this.props.sidebarActive =="/building"?"subListAction":""}>
                  <MenuListItem href="/building" icon={showIcon("icon-codeconstruct")}>代码构建</MenuListItem></li>
              </ul>
            </MenuList>
            {is_user == 1?<ul className={cx(s.list,"sidebar-menu-list")}>
              <li onClick = {this.onChangeAction.bind(this,"/user")}
                  className={this.props.sidebarActive =="/user"?"subListAction":""}>
                <MenuListItem href="/user" icon={showIcon("icon-login")}>用户中心</MenuListItem></li>
            </ul>:
              <ul className={cx(s.list,"sidebar-menu-list")}>
                <li onClick = {this.onChangeAction.bind(this,"/organize")}
                    className={this.props.sidebarActive =="/organize"?"subListAction":""}>
                  <MenuListItem href="/organize" icon={showIcon("icon-login")}>组织中心</MenuListItem></li>
              </ul>
            }
          </div>
        </div>
        :
        <div className="sidebar-menu-thin">
          <ThinList
            href = "/"
            title="控制台"
            isOpen={false}
            icon={<i className="icon-console"> </i>}
            onClick = {this.onChangeAction.bind(this,"/")}
            className={this.props.sidebarActive =="/"?"menuListAction":""}
          >
          </ThinList>
          <ThinList
            href="javascript:;"
            title="服务中心"
            isOpen={true}
            icon={<i className="icon-sanjiaoright"> </i>}
            onClick = {function(){}}
            className=""
          >
            <ThinItem href="/choseImage" icon={<i className="icon-New-service"> </i>} tip="新建服务"
                      onClick = {this.onChangeAction.bind(this,"/choseImage")}
                      className={this.props.sidebarActive =="/choseImage"?"menuListAction":""}
            />
            <ThinItem href="/serviceList" icon={<i className="icon-servicelist"> </i>} tip="服务列表"
                      onClick = {this.onChangeAction.bind(this,"/serviceList")}
                      className={this.props.sidebarActive =="/serviceList"?"menuListAction":""}
            />
            <ThinItem href="/volumes" icon={<i className="icon-storagemanag"> </i>} tip="存储卷管理"
                      onClick = {this.onChangeAction.bind(this,"/volumes")}
                      className={this.props.sidebarActive =="/volumes"?"menuListAction":""}
            />
          </ThinList>
          <ThinList
            href="javascript:;"
            title="镜像中心"
            isOpen={true}
            icon={<i className="icon-sanjiaoright"> </i>}
            onClick = {function(){}}
            className=""
          >
            <ThinItem href="/imageForMy" icon={<i className="icon-mymirror"> </i>} tip="我的镜像"
                      onClick = {this.onChangeAction.bind(this,"/imageForMy")}
                      className={this.props.sidebarActive =="/imageForMy"?"menuListAction":""}
            />
            <ThinItem href="/imageForPlatform" icon={<i className="icon-formmirror"> </i>} tip="平台镜像"
                      onClick = {this.onChangeAction.bind(this,"/imageForPlatform")}
                      className={this.props.sidebarActive =="/imageForPlatform"?"menuListAction":""}
            />
            <ThinItem href="/building" icon={<i className="icon-codeconstruct"> </i>} tip="构建镜像"
                      onClick = {this.onChangeAction.bind(this,"/building")}
                      className={this.props.sidebarActive =="/building"?"menuListAction":""}
            />
          </ThinList>
          {is_user==1?
            <ThinList
              href = "/user"
              isOpen={false}
              title="用户中心"
              icon={<i className="icon-login"> </i>}
              onClick = {this.onChangeAction.bind(this,"/user")}
              className={this.props.sidebarActive =="/user"?"menuListAction":""}
            >
            </ThinList>:
            <ThinList
              href = "/organize"
              isOpen={false}
              title="组织中心"
              icon={<i className="icon-login"> </i>}
              onClick = {this.onChangeAction.bind(this,"/organize")}
              className={this.props.sidebarActive =="/organize"?"menuListAction":""}
            >
            </ThinList>
            }
        </div>
    )
  }
  render(){
    return (
      <div className={cx(s.root,"app-sidebar")}>
        {this.getLogo()}
        {this.getList()}
      </div>
    )
  }

}

// <li><a href="/">新建服务</a></li>
// <li><a href="/serviceList">服务列表</a></li>
//   <li><a href="/">存储卷管理</a></li>

export default withStyles(s)(Sidebar);
