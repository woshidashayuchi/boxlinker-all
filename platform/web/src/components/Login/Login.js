
import React, { PropTypes,Component } from 'react';
import cookie from 'react-cookie';
import {FETCH_URL} from '../../constants'
import ReactDOM from 'react-dom';
import Notification from '../App/Notification';


class Login extends React.Component{
  static contextTypes = {
    setTitle: React.PropTypes.func
  };
  constructor(props){
    super(props);
    this.state={
      uName:false,
      uPassword:false,
      isLogin:true,
      notifications:{message:""}
    }
  }
  login(){
    let data = {},
      uName =  ReactDOM.findDOMNode(this.refs.username).value,
      uPassword = ReactDOM.findDOMNode(this.refs.password).value,
      userTip = ReactDOM.findDOMNode(this.refs.userTip),
      passwordTip = ReactDOM.findDOMNode(this.refs.passwordTip),
      my = this,
      myInit;
    if(uName == ""){
      userTip.innerHTML = "用户名不能为空";
      this.setState({
        uName:true,
      });
      return false
    }
    if(uPassword == ""){
      passwordTip.innerHTML = "密码不能为空";
      this.setState({
        uPassword:true
      });
      return false
    }
    my.setState({
      isLogin:false
    });
    data = {
      user_name:uName,
      pass_word:uPassword
    };
    console.log(data,"登录参数isok");
    myInit = {
      method: "POST",
      body: JSON.stringify(data)
    };
    fetch(FETCH_URL.USER+"/tokens",myInit).then(function(res){
      if(res.ok) {
        return res.json().then(function (data) {
          console.log(data);
          if(data.status == 0){
            localStorage.setItem('_at',data.result.token);
            var exp = new Date();
            exp.setTime(exp.getTime()+1000*60*60*24*7);
            cookie.save('_at',data.result.token,{path:'/',expires: exp});
            cookie.save('sidebarActive',"/",{path:'/',expires: exp});
            cookie.save('isSidebarOpen',true,{path:'/',expires:exp});
            my.setState({
              notifications:{
                message:"登录成功",
                level:"success"
              },
            });
            setTimeout(function(){
              my.setState({
                notifications:{
                  message:"",
                  level:""
                },
                //isLogin:true
              });
              window.location.href = "/"
            },2000);
          }else if(data.status == 705){
            userTip.innerHTML = "用户名或者密码错误";
            my.setState({
              uName:true,
              isLogin:true
            });
          }else{
            my.setState({
              notifications:{
                message:"登录失败:"+data.msg,
                level:"danger"
              },
              isLogin:true
            });
            setTimeout(function(){
              my.setState({
                notifications:{
                  message:"",
                  level:""
                }
              });
            },5000);
          }
        })
      }else{
        my.setState({
          isLogin:true
        });
        console.log("is xxx");
      }
    })

  }
  changeUserName(e){
    if(e.target.value){
      this.setState({
        uName:false
      })
    }
  }
  changePassword(e){
    if(e.target.value){
      this.setState({
        uPassword:false
      })
    }
  }
  componentDidMount(){
    let me = this;
    document.onkeydown = function(e){
      if(e.keyCode == 13){
        me.login();
      }
    }
  }
  render(){
    let notification = this.state.notifications.message?
      <Notification show = {true} obj={this.state.notifications}/>:<Notification show = {false} obj={this.state.notifications}/>;
    this.context.setTitle("登录");
    return(
      <div className="entryBox">
        <div className="entryHd">
          <div className="w1200 clearfix">
            <div className="entryHdLogo">
              <a href="javascript:;" className="entryLogo"><image src="/logo.png" /></a>
              {/*<a href="javascript:;" className="entryNews icon-buildlog">新闻</a>*/}
              {/*<a href="javascript:;" className="entryDoc icon-mirrorceer">文档</a>*/}
            </div>
            <div className="entryHdBtn">
              <a href="/signUp">注册</a>
              <a href="/login">登录</a>
            </div>
          </div>
        </div>
        <div className="entryBd">
            <div className="entryModel">
              <div className="entryModelBg">Make it simple   make it fast</div>
              <div className="entryFrom">
                <div className="title">用户登录</div>
                <div className="entryItemBox">
                  <div className={`entryItem ${this.state.uName? "entryItemError" :""}`} >
                    <div className="entryInputBox icon-username">
                      <input onInput={this.changeUserName.bind(this)} className="entryInput" ref = "username" type="text" placeholder="用户名或邮箱"/>
                    </div>
                    <div className="entryTip">
                      <p ref = "userTip">用户名错误</p>
                    </div>
                  </div>
                  <div className={`entryItem ${this.state.uPassword? "entryItemError" : ""}`}>
                    <div className="entryInputBox icon-mima">
                      <input onInput={this.changePassword.bind(this)} className="entryInput" ref="password" type="password" placeholder="密码"/>
                    </div>
                    <div className="entryTip">
                      <p ref = "passwordTip">密码错误</p>
                    </div>
                  </div>
                  <div className="entryBtnBox">
                    <button className={`btn btn-primary entryBtn ${!this.state.isLogin?"btn-loading":""}`}
                            disabled={!this.state.isLogin}
                            onClick={this.login.bind(this)}>{this.state.isLogin?"登录":"登录中"}</button>
                  </div>
                  <div className="entryFromFt">
                    <a href="/signUp">立即注册</a>
                    <a href="javascript:;">忘记密码</a>
                  </div>
                </div>
              </div>
            </div>
        </div>
        <div className="entryBg"></div>
        {notification}
      </div>
    )
  }
  render1(){
    let notification = this.state.notifications.message?
        <Notification obj={this.state.notifications}/>:null;
    this.context.setTitle("登录");
    return(
        <div className="entryBox">
          <div className="entryHd">
            <div className="w1200 clearfix">
              <div className="entryHdLogo">
                <a href="javascript:;" className="entryLogo"><image src="/logo.png" /></a>
                {/*<a href="javascript:;" className="entryNews icon-buildlog">新闻</a>*/}
                {/*<a href="javascript:;" className="entryDoc icon-mirrorceer">文档</a>*/}
              </div>
              <div className="entryHdBtn">
                <a href="/signUp">注册</a>
                <a href="/login">登录</a>
              </div>
            </div>
          </div>
          <div className="entryBd">
            <div className="entryModel">
              <div className="title">用户登录</div>
              <div className="entryFrom">
                <div className={`entryItem ${this.state.uName? "entryItemError" :""}`} >
                  <div className="entryInputBox icon-username">
                    <input onInput={this.changeUserName.bind(this)} className="entryInput" ref = "username" type="text" placeholder="用户名或邮箱"/>
                  </div>
                  <div className="entryTip">
                    <p ref = "userTip">用户名错误</p>
                  </div>
                </div>
                <div className={`entryItem ${this.state.uPassword? "entryItemError" : ""}`}>
                  <div className="entryInputBox icon-mima">
                    <input onInput={this.changePassword.bind(this)} className="entryInput" ref="password" type="password" placeholder="密码"/>
                  </div>
                  <div className="entryTip">
                    <p ref = "passwordTip">密码错误</p>
                  </div>
                </div>
                <div className="entryBtnBox">
                  <button className="btn btn-primary entryBtn" disabled={!this.state.isLogin}
                          onClick={this.login.bind(this)}>{this.state.isLogin?"登录":"登录中..."}</button>
                </div>
                <div className="entryFromFt">
                  没有账户? <a href="/signUp">注册</a>
                  <a href="javascript:;">忘记密码</a>
                </div>
              </div>
            </div>
          </div>
          <div className="entryBg"></div>
          {notification}
        </div>
    )
  }
}

export default Login;
