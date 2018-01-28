

import React,{PropTypes,Component} from 'react';
import HeadLine from '../../components/HeadLine';
import ReactDOM from 'react-dom';

class GetPersonalInfo extends Component{
  static propTypes = {
    onRevisePassword:React.PropTypes.func
  };

  constructor(props){
    super(props);
    this.state = {
      oldP:false,
      newP:false,
      newAgain:false,
      notifications:{message:""}
    }
  }

  revisePassword(){
    let old_p = ReactDOM.findDOMNode(this.refs.old_p),
      oldTip = ReactDOM.findDOMNode(this.refs.oldTip),
      new_p = ReactDOM.findDOMNode(this.refs.new_p),
      newTip = ReactDOM.findDOMNode(this.refs.newTip),
      new_p_again = ReactDOM.findDOMNode(this.refs.new_p_again),
      newTipAgain = ReactDOM.findDOMNode(this.refs.newTipAgain);
    if(old_p.value ==""){
      this.setState({
        oldP:true
      });
      oldTip.innerHTML = "原始密码不能为空";
      return false;
    }
    if(new_p.value ==""){
      this.setState({
        newP:true
      });
      newTip.innerHTML = "新密码不能为空";
      return false;
    }
    if(new_p_again.value ==""){
      this.setState({
        newAgain:true
      });
      newTipAgain.innerHTML = "确认新密码不能为空";
      return false;
    }
    if(new_p_again.value !=new_p.value){
      this.setState({
        newAgain:true
      });
      newTipAgain.innerHTML = "两次新密码不一致";
      return false;
    }
    let passwordObj = {
      old_p:old_p.value,
      new_p:new_p.value
    };
    console.log(passwordObj);
    this.props.onRevisePassword(passwordObj)
  }
  changeOldPassword(){
    let old_p = ReactDOM.findDOMNode(this.refs.old_p);
    if(old_p.value.length > 0){
      this.setState({
        oldP:false
      })
    }
  }
  changeNewPassword(){
    let new_p = ReactDOM.findDOMNode(this.refs.new_p);
    let newTip = ReactDOM.findDOMNode(this.refs.newTip);
    if(new_p.value.length < 6 && new_p.value.length!=""){
      newTip.innerHTML = "密码不能少于6位";
      this.setState({
        newP:true
      })
    }else{
      this.setState({
        newP:false
      })
    }
  }
  changeNewAgainPassword(){
    let new_p_again = ReactDOM.findDOMNode(this.refs.new_p_again);
    let newTipAgain = ReactDOM.findDOMNode(this.refs.newTipAgain);
    if(new_p_again.value.length < 6 && new_p_again.value.length!=""){
      newTipAgain.innerHTML = "密码不能少于6位";
      this.setState({
        newAgain:true
      })
    }else{
      this.setState({
        newAgain:false
      })
    }
  }

  render(){
    return (
      <div className = "userTabBox">
        <div className = "userItem">
          <HeadLine
            title="个人头像"
            titleEnglish=""
            titleInfo="PERSONAL HEAD"
          />
          <div className = "userHead">
            <div className="userHeadBox">
              <img />
            </div>
            <div className = "choose icon-operation">
              <span>更改头像</span>
            </div>
          </div>
        </div>
        <div className = "userItem">
          <HeadLine
            title="绑定手机"
            titleEnglish=""
            titleInfo="BINDING CELLPHONE"
          />
          <div className = "userPhone">
            <div className = "userInputItem">
              <input type = "text" className = "form-control" />
              <i className="userTip">绑定手机号可接受系统重要通知</i>
            </div>
            <div className = "userInputItem">
              <input type = "text" className = "form-control userInputLittle" />
              <button className="userButtonLittle">短信验证码</button>
            </div>
            <div className = "userInputItem">
              <button className = "btn btn-warning">绑定</button>
            </div>
          </div>
        </div>
        <div className = "userItem">
          <HeadLine
            title="修改密码"
            titleEnglish=""
            titleInfo="MODIFY PASSWORD"
          />
          <div className = "userPhone">
            <div className ={`userInputItem ${this.state.oldP?"userInputItemError":""}`} >
              <input onChange = {this.changeOldPassword.bind(this)} type = "password" className = "form-control" ref = "old_p" placeholder = "原始密码" />
              <i className="userTip" ref = "oldTip"> </i>
            </div>
            <div className = {`userInputItem ${this.state.newP?"userInputItemError":""}`}>
              <input onChange = {this.changeNewPassword.bind(this)} type = "password" className = "form-control" ref = "new_p" placeholder = "新密码" />
              <i className="userTip" ref = "newTip"> </i>
            </div>
            <div className = {`userInputItem ${this.state.newAgain?"userInputItemError":""}`}>
              <input onChange={this.changeNewAgainPassword.bind(this)} type = "password" className = "form-control" ref = "new_p_again" placeholder = "确认新密码" />
              <i className="userTip" ref = "newTipAgain"> </i>
            </div>
            <div className = "userInputItem">
              <button className = "btn btn-warning" onClick={this.revisePassword.bind(this)}>确定</button>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default  GetPersonalInfo;
