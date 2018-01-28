
import React ,{PropTypes,Component}  from 'react';
import HeadLine from '../../components/HeadLine';

class GetMyAccount extends Component{
  static propTypes = {
    balance:React.PropTypes.number,
    getBalance:React.PropTypes.func,
  };
  componentDidMount(){

  }
  getTableBody(){
    let data = [
      {name:"服务名称",type:"数据卷扩容",time:"20160223",money:"200.00",way:"支付宝",pay:"已完成",odd:"123543"},
      {name:"服务名称",type:"数据卷扩容",time:"20160223",money:"200.00",way:"支付宝",pay:"已完成",odd:"123543"},
      {name:"服务名称",type:"数据卷扩容",time:"20160223",money:"200.00",way:"支付宝",pay:"已完成",odd:"123543"},
      {name:"服务名称",type:"数据卷扩容",time:"20160223",money:"200.00",way:"支付宝",pay:"已完成",odd:"123543"},
      {name:"服务名称",type:"数据卷扩容",time:"20160223",money:"200.00",way:"支付宝",pay:"已完成",odd:"123543"}
    ];
    return data.map((item,i) => {
      return (
        <tr key={i}>
          <td><div className="tablePaddingLeft">
            <div className="mediaItem">
                <img className="mediaImg" src = "/slImgJx.png" />
                <span className="mediaTxt">{item.name}</span>
            </div>
          </div></td>
          <td><div className="tablePaddingLeft"><span className="color333">{item.type}</span></div></td>
          <td><div className="tablePaddingLeft"><span className="color333">{item.time}</span></div></td>
          <td><div className="tablePaddingLeft"><span className="color333">{item.money}</span></div></td>
          <td><div className="tablePaddingLeft"><span className="color333">{item.way}</span></div></td>
          <td><div className="tablePaddingLeft"><span className="icon-right"></span></div></td>
          <td><div className="tablePaddingLeft"><span className="color333">{item.odd}</span></div></td>
        </tr>
      )
    })
  }
  getDemoTable(){
    return (
      <table className="table recordTable">
        <thead>
        <tr>
          <th width="15%">服务名称</th>
          <th width="15%">类型</th>
          <th width="15%">时间</th>
          <th width="15%">金额</th>
          <th width="15%">扣款方式</th>
          <th width="10%">是否完成</th>
          <th width="15%">单号</th>
        </tr>
        </thead>
        <tbody>
        {this.getTableBody()}
        </tbody>
      </table>
    )
  }

  render(){
    return (
      <div className = "userTabBox">
        <div className = "userItem accountBg">
          <div className = "accountHd clearfix">
            <div className="left">
              <HeadLine
                title="账户余额"
                titleEnglish=""
                titleInfo="ACCOUNT BALANCE"
              />
            </div>
            <div className = "right userHeadTip">  关注微信公众号，平台免费为您提供3个月的账户试用奖励。 </div>
          </div>
          <div className = "accountBd">
            <div className = "accountItem">
              <span className="aiName">账户余额 :</span>
              <span className="aiInfo">
                <i>-1550</i> 元
              </span>
            </div>
            <div className = "accountItem">
              <span className="aiName">支付金额 :</span>
              <span className="aiInfo">
                <input type="number" className="form-control" /> 元
              </span>
            </div>
            <div className = "accountItem">
              <span className="aiName">支付方式 :</span>
              <span className="aiInfo">
                <a href="javascript:;" className="accountPay accountPayZfb active"> </a>
                <a href="javascript:;" className="accountPay accountPayWx"> </a>
              </span>
            </div>
          </div>
          <div className = "accountFt clearfix">
            <button className="btn btn-danger">充值</button>
            <div className="accountFtTip right">
              <p> 提示：累计充值金额满<span>￥200</span>后可提交工单申请发票。</p>
              <a href="javascript:;"> </a>
            </div>
          </div>
        </div>
        <div className = "userItem">
          <div className = "accountHd clearfix">
            <div className="left">
              <HeadLine
                title="充值记录"
                titleEnglish=""
                titleInfo="RECHARGE RECORD"
              />
            </div>
            <div className = "right userHeadTip">提示：仅显示最近5笔交易，如需了解全部记录请提交 工单，我们会在24小时内发送您邮箱</div>
          </div>
          <div className = "userPayRecord">
            {this.getDemoTable()}
          </div>
        </div>
      </div>
    )
  }
}

export default GetMyAccount;
