import React, { Component, PropTypes } from 'react';
import BreadcrumbContainer from '../../containers/BreadcrumbContainer'
import SidebarContainer from '../../containers/SidebarContainer';
import HeaderContainer from '../../containers/HeaderContainer';
import Notification from './Notification';

class App extends Component {
  static contextTypes = {
    store: React.PropTypes.object,
  };
  static propTypes = {
    isSidebarOpen: React.PropTypes.bool,
    notifications: React.PropTypes.object,
    onInit: React.PropTypes.func,
  };

  componentWillMount() {
    // const { insertCss } = this.props.context;
    // this.removeCss = insertCss(s);
  }

  componentWillUnmount() {
    // this.removeCss();
  }

  componentDidMount(){
    // let username = this.context.store.getState().user_info.user_name;
    // this.props.onInit(username)
  }

  render() {
    let notification = this.props.notifications.message?
      <Notification show = {true} obj={this.props.notifications}/>:<Notification show = {false} obj={this.props.notifications}/>;
    return (
      <div className={`app ${this.props.isSidebarOpen?"":"sidebar-close"}`}>
        <HeaderContainer/>
        <SidebarContainer/>
        <div className="containerPack">
          <div className="containerInner">
            <BreadcrumbContainer />
            <div className="containerBody">
              {this.props.children}
            </div>
          </div>
        </div>
        {notification}
      </div>
    )
  }

}

export default App;
