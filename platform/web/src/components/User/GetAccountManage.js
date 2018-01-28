
import React,{PropTypes,Component} from 'react';
import HeadLine from '../../components/HeadLine';

class GetAccountManage extends Component{
  static contextTypes = {
    store: React.PropTypes.object,
  };
  static propTypes = {
    authUrl: React.PropTypes.object,
    getAuthURL:React.PropTypes.func
  };
  componentDidMount(){
    let git = this.context.store.getState().user_info.oauth.github;
    let cod = this.context.store.getState().user_info.oauth.coding;
    !git?this.props.getAuthURL({src_type:"github",redirect_url:window.location.href}):null;
    !cod?this.props.getAuthURL({src_type:"coding",redirect_url:window.location.href}):null;
  }
  render(){
    let user = this.context.store.getState().user_info;
    return(
      <div className = "userTabBox">
        <div className = "accountManageHd">
          <HeadLine
            title="账号管理"
            titleEnglish=""
            titleInfo="ACCOUNT MANAGEMENT"
          />
        </div>
        {/*<div className="accountManageItem">*/}
          {/*<div className="accountManageBox">*/}
            {/*<img width={60} height={60} src={require('./imgHd.png')} alt="img"/>*/}
            {/*<div className="ambInfo">*/}
              {/*<h1>微信公众名字</h1>*/}
              {/*<p>关注微信公众号，平台免费为您提供3个月的账户试用奖励。</p>*/}
            {/*</div>*/}
          {/*</div>*/}
          {/*<button className="btn btn-warning">绑定</button>*/}
        {/*</div>*/}
        <div className="accountManageItem">
          <div className="accountManageBox icon-github">
            <div className="ambInfo">
              <h1>Github</h1>
              <p>Github于2008年上线，用于Git代码仓库托管及基本的Web管理界面</p>
            </div>
          </div>
          <a href={user.oauth.github?"javascript:;":this.props.authUrl.github} target = "_blank"
             className="btn btn-warning">{user.oauth.github?"已绑定":"绑定"}</a>
        </div>
        {/*<div className="accountManageItem">*/}
          {/*<div className="accountManageBox">*/}
              {/*<img width={60} height={60} src={require('./imgHd.png')} alt="img"/>*/}
            {/*<div className="ambInfo">*/}
              {/*<h1>Bitbucket</h1>*/}
              {/*<p>Bitbucket 是一家源代码托管网站，采用Mercurial和Git作为分布式版本控制系统，同时提供商业计划和免费账户。</p>*/}
            {/*</div>*/}
          {/*</div>*/}
          {/*<button className="btn btn-warning">绑定</button>*/}
        {/*</div>*/}
        <div className="accountManageItem">
          <div className="accountManageBox icon-github">
            <div className="ambInfo">
              <h1>Coding</h1>
              <p>Coding.net 为软件开发者提供基于云计算技术的软件开发平台，包括项目管理，代码托管，运行空间和质量控制等等。</p>
            </div>
          </div>
          <a href={user.oauth.coding?"javascript:;":this.props.authUrl.coding} target = "_blank"
             className={`btn ${user.oauth.coding?"btn-default":"btn-warning"}`}>{user.oauth.coding?"解除绑定":"绑定"}</a>
        </div>
      </div>
    )
  }
}

export default  GetAccountManage
