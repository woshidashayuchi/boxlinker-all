import React, { Component } from 'react';
import Loading from 'react-loading'
import cookie from 'react-cookie'
import {Navbar,Nav,NavItem,NavDropdown,MenuItem,
} from 'react-bootstrap';

class Header extends Component {
  static propTypes = {
    isLoading: React.PropTypes.bool,
    isSidebarOpen: React.PropTypes.bool.isRequired,
    onSidebarToggleClick: React.PropTypes.func,
    organizeList:React.PropTypes.array,
    getOrganizeList:React.PropTypes.func,
    changeAccount:React.PropTypes.func
  };
  static contextTypes = {
    store: React.PropTypes.object
  };
  handleSelect(key){
    console.log(key);
    switch (key) {
      case 0.1:
        let orga_uuid = this.context.store.getState().user_info.orga_uuid;
        this.props.changeAccount(orga_uuid);
        break;
      case 1.1:
        this.props.onSidebarToggleClick(!this.props.isSidebarOpen);
        var exp = new Date();
        exp.setTime(exp.getTime()+1000*60*60*24*7);
        cookie.save('isSidebarOpen',!this.props.isSidebarOpen,{path:'/',expires: exp});
        break;
      case 4.1:
        cookie.remove('_at');
        cookie.remove('30589');
        localStorage.removeItem('_at');
        localStorage.removeItem('sidebarActive');
        location.href = '/login';
        break;
      default:
        let organizeList = this.props.organizeList;
        let org_id = organizeList[key].org_id;
        this.props.changeAccount(org_id);
    }
  }
  handleClick(e){
    if(e.target.innerText.trim() =="退出"){
      cookie.remove('_at');
      cookie.remove('30589');
      localStorage.removeItem('_at');
      localStorage.removeItem('sidebarActive');
      location.href = '/login';
    }
  }
  componentDidMount(){
    this.props.getOrganizeList();
  }
  render(){
    const username = this.context.store.getState().user_info.user_name;
    const is_user = this.context.store.getState().user_info.is_user;
    const user_orga =  this.context.store.getState().user_info.user_orga;
    let menuItem = this.props.organizeList.map((item,i) =>{
      if(item.orga_name == username && is_user == 0){
        return <MenuItem eventKey={i} key = {i}><div className="headerOrgList">
          <p>{item.orga_name}</p>
          <p>切换到个人</p>
        </div></MenuItem>;
      }else if(item.orga_name == user_orga){

      }else{
        return <MenuItem eventKey={i} key = {i}><div className="headerOrgList">
          <p>{item.orga_name}</p>
          <p>切换到该组织</p>
        </div></MenuItem>;
      }
    });
    let dropdown = null;
    if(is_user == 0){
      dropdown = user_orga?
        <NavDropdown eventKey={4} title={user_orga} id="header-nav-item-userinfo">
          {menuItem}
          <MenuItem eventKey={4.1}>退出</MenuItem>
        </NavDropdown>
        :
        <NavDropdown eventKey={4.1} title="退出" id="header-nav-item-userinfo"> </NavDropdown>;
    }else{
      dropdown = username?
        <NavDropdown eventKey={4} title={username} id="header-nav-item-userinfo">
          {menuItem}
          <MenuItem eventKey={4.1}>退出</MenuItem>
        </NavDropdown>
        :
        <NavDropdown eventKey={4.1} title="退出" id="header-nav-item-userinfo"> </NavDropdown>;
    }
    return (
      <Navbar fixedTop={true} className="app-navbar" style={{left:"180px"}} onClick = {this.handleClick.bind(this)}>
        <Nav onSelect={this.handleSelect.bind(this)}>
          <NavItem eventKey={1.1} href="javascript:void(0)"><i className={this.props.isSidebarOpen?"icon-withdraw":"icon-back"} aria-hidden="true"></i></NavItem>
        </Nav>
        <Nav pullRight onSelect={this.handleSelect.bind(this)} style={{marginRight:"0"}}>
          <NavItem className="loading-animation">{this.props.isLoading?<Loading type="bubbles" color="#fff" height="50px" width="50px"/>:null}</NavItem>
          {dropdown}
        </Nav>

      </Navbar>
    )
  }

}

export default Header;
