
import React, { PropTypes,Component } from 'react';
import ReactDOM from 'react-dom'
import fetch from 'isomorphic-fetch'
import Notification from '../App/Notification';
import uuid from 'uuid';
import * as Const from '../../constants';


class SignUp extends React.Component{
  static contextTypes = {
    setTitle: React.PropTypes.func
  };
  constructor(props){
    super(props);
    this.state = {
      uName:false,
      uEmail:false,
      uPassword:false,
      uCode:false,
      isSignUp:true,
      notifications:{message:""}
    }
  }
  signUp(){
    let uName =  ReactDOM.findDOMNode(this.refs.username).value,
      userTip = ReactDOM.findDOMNode(this.refs.userTip),
      uEmail = ReactDOM.findDOMNode(this.refs.email).value,
      emailTip = ReactDOM.findDOMNode(this.refs.emailTip),
      uPassword =  ReactDOM.findDOMNode(this.refs.password).value,
      passwordTip = ReactDOM.findDOMNode(this.refs.passwordTip),
      uCode =  ReactDOM.findDOMNode(this.refs.code).value,
      codeTip =  ReactDOM.findDOMNode(this.refs.codeTip),
      codeId = ReactDOM.findDOMNode(this.refs.codeImg).src,
      myInit,
      my = this;
    codeId = codeId.split("?")[1].split("=")[1];
    console.log(codeId);
    if(uName == ""){
      userTip.innerHTML = "用户名不能为空";
      this.setState({
        uName:true,
      });
      return false
    }
    if(uEmail == ""){
      emailTip.innerHTML = "邮箱不能为空";
      this.setState({
        uEmail:true,
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
    if(uCode == ""){
      codeTip.innerHTML = "验证码不能为空";
      this.setState({
        uCode:true
      });
      return false
    }
    if(!this.state.uName&&!this.state.uEmail&&!this.state.uPassword) {
      my.setState({
        isSignUp:true
      });
      console.log("ok");
      let data = {
        user_name:uName,
        pass_word:uPassword,
        email:uEmail,
        code_str:uCode,
        code_id:codeId
      };
      console.log(data,"注册参数");
      myInit = {
        method: "POST",
        body: JSON.stringify(data)
      };
      fetch(Const.FETCH_URL.USER+"/users",myInit).then(function(res){
        if(res.ok) {
          return res.json().then(function (data) {
            my.setState({
              isSignUp:true
            });
            console.log(data);
            if(data.status==0){
              my.setState({
                notifications:{
                  message:"注册成功",
                  level:"success"
                }
              });
              setTimeout(function(){
                my.setState({
                  notifications:{
                    message:"",
                    level:""
                  },
                  //isSignUp:true
                });
                window.location.href = "/login"
              },2000);
            }else{
              my.changeImageSrc();
              my.setState({
                notifications:{
                  message:"注册失败:"+data.msg,
                  level:"danger"
                },
                isSignUp:true
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
            isSignUp:true
          });
          console.log("is xxx");
        }
      })
    }

  }
  changeUserName(){
    let uName =  ReactDOM.findDOMNode(this.refs.username).value,
        userTip = ReactDOM.findDOMNode(this.refs.userTip),
        nameRegExp = /^[a-zA-Z]+[a-zA-Z0-9_]*$/;
    if(uName.length<6&&uName!=""){
      userTip.innerHTML = "用户名必须6位以上";
      this.setState({
        uName:true,
      });
      return false
    }
    if(!nameRegExp.test(uName)&&uName!=""){
      userTip.innerHTML = "字母数字下划线组合,必须字母开头";
      this.setState({
        uName:true,
      });
      return false
    }else{
      this.setState({
        uName:false,
      });
    }
  }
  changeEmail(){
    let uEmail = ReactDOM.findDOMNode(this.refs.email).value,
        emailTip = ReactDOM.findDOMNode(this.refs.emailTip),
        emailRegExp = /^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/;
    if(!emailRegExp.test(uEmail) && uEmail!=""){
      emailTip.innerHTML = "邮箱格式不正确";
      this.setState({
        uEmail:true,
      });
      return false
    }else{
      this.setState({
        uEmail:false,
      });
    }

  }
  changePassword(){
    let uPassword =  ReactDOM.findDOMNode(this.refs.password).value,
      passwordTip = ReactDOM.findDOMNode(this.refs.passwordTip);
    if(uPassword.length<6 && uPassword!=""){
      passwordTip.innerHTML = "密码必须6位以上";
      this.setState({
        uPassword:true
      })
    }else{
      this.setState({
        uPassword:false,
      });
    }

  }
  changeCode(){
    let uCode =  ReactDOM.findDOMNode(this.refs.code).value,
      codeTip =  ReactDOM.findDOMNode(this.refs.codeTip);
    if(uCode.length!=4 && uCode!=""){
      codeTip.innerHTML = "请输入4位验证码";
      this.setState({
        uCode:true
      })
    }else{
      this.setState({
        uCode:false,
      });
    }

  }
  changeImageSrc(){
    let img = ReactDOM.findDOMNode(this.refs.codeImg);
    img.src = "http://verify-code.boxlinker.com/code?uuid="+uuid.v1();
  }
  componentDidMount(){
    ReactDOM.findDOMNode(this.refs.codeImg).src = "http://verify-code.boxlinker.com/code?uuid="+uuid.v1();
    let me = this;
    document.onkeydown = function(e){
      if(e.keyCode == 13){
        me.signUp();
      }
    }
  }
  render(){
    let notification = this.state.notifications.message?
      <Notification show = {true} obj={this.state.notifications}/>:<Notification show = {false} obj={this.state.notifications}/>;
    this.context.setTitle("注册");
    return (
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
        <div className="entryBd signUp">
          <div className="entryModel">
            <div className="entryModelBg">Make it simple   make it fast</div>
            <div className="entryFrom">
              <div className="title">用户注册</div>
              <div className="entryItemBox">
                <div className={`entryItem ${this.state.uName? "entryItemError" :""}`} >
                  <div className="entryInputBox icon-username">
                    <input onChange={this.changeUserName.bind(this)}
                           className="entryInput" ref = "username" type="text" placeholder="用户名"/>
                  </div>
                  <div className="entryTip">
                    <p ref = "userTip">用户名错误</p>
                  </div>
                </div>
                <div className={`entryItem ${this.state.uEmail? "entryItemError" :""}`} >
                  <div className="entryInputBox icon-email">
                    <input onChange={this.changeEmail.bind(this)}
                           className="entryInput" ref = "email" type="text" placeholder="邮箱"/>
                  </div>
                  <div className="entryTip">
                    <p ref = "emailTip">邮箱错误</p>
                  </div>
                </div>
                <div className={`entryItem ${this.state.uPassword? "entryItemError" :""}`} >
                  <div className="entryInputBox icon-mima">
                    <input onInput={this.changePassword.bind(this)}
                           className="entryInput" ref="password" type="password" placeholder="密码"/>
                  </div>
                  <div className="entryTip">
                    <p ref = "passwordTip">密码错误</p>
                  </div>
                </div>
                <div className={`entryItem entryItemCode ${this.state.uCode? "entryItemError" :""}`} >
                  <div className="entryInputBox  icon-mima">
                    <input onInput={this.changeCode.bind(this)}
                           className="entryInput" ref="code" type="text" placeholder="验证码"/>
                    <img ref = "codeImg" onClick = {this.changeImageSrc.bind(this)} src = "" />
                    <span className="icon-refresh" onClick = {this.changeImageSrc.bind(this)}> </span>
                  </div>
                  <div className="entryTip">
                    <p ref = "codeTip">验证码错误</p>
                  </div>
                </div>
                <div className="entryBtnBox">
                  <button className={`btn btn-primary entryBtn ${!this.state.isSignUp?"btn-loading":""}`}
                          disabled={!this.state.isSignUp}
                          onClick={this.signUp.bind(this)}>{this.state.isSignUp?"注册":"注册中..."}</button>
                </div>
                <div className="entryFromFt">
                  <a href="/login">已有账户   登录</a>
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
}

export default SignUp;
