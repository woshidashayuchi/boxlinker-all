
import React, {Component} from 'react'
import {Provider} from 'react-redux'
import AppContainer from '../containers/AppContainer'
import emptyFunction from 'fbjs/lib/emptyFunction';

class Root extends Component{
  static propTypes = {
    context: React.PropTypes.shape({
      createHref: React.PropTypes.func.isRequired,
      store: React.PropTypes.object.isRequired,
      insertCss: React.PropTypes.func,
      setTitle: React.PropTypes.func,
      setMeta: React.PropTypes.func,
      pathname: React.PropTypes.any,
    }),
    children: React.PropTypes.element.isRequired,
    error: React.PropTypes.object,
  };

  static childContextTypes = {
    createHref: React.PropTypes.func.isRequired,
    insertCss: React.PropTypes.func.isRequired,
    setTitle: React.PropTypes.func.isRequired,
    setMeta: React.PropTypes.func.isRequired,
    pathname: React.PropTypes.any,
  };

  getChildContext() {
    const context = this.props.context;
    return {
      createHref: context.createHref,
      insertCss: context.insertCss || emptyFunction,
      setTitle: context.setTitle || emptyFunction,
      setMeta: context.setMeta || emptyFunction,
      pathname: "",
    };
  }
  render(){
    if (this.props.error) {
      return this.props.children;
    }
    let pathname = this.props.context.pathname;
    if (
      pathname == '/login' ||
      pathname == '/signUp'
    ){
      return this.props.children;
    }

    if(typeof localStorage != 'undefined'&& !localStorage.getItem('_at')){
      location.href = '/login';
      return;
    }

    const store = this.props.context.store;
    return (
      <Provider store={store}>
        <AppContainer>
          {this.props.children}
        </AppContainer>
      </Provider>
    )
  }
}

export default Root
