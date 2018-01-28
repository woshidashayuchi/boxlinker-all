import React,{PropsType,Component} from 'react';

import HeadLine from '../../components/HeadLine';

class GetCertificateMange extends Component{
  render(){
    return (
      <div className = "userTabBox">
        <div className="certificateMangeItem">
          <div className = "accountHd clearfix">
            <div className="left">
              <HeadLine
                title="我的礼券"
                titleEnglish=""
                titleInfo="MY CERTIFICATE"
              />
            </div>
            <div className = "right userHeadTip redTip">提示：礼券在激活后才可使用。</div>
          </div>
          <div className = "userInputItem">
            <input type = "text" className = "form-control" placeholder="请输入礼券八位码" /><br />
            <button className="btn btn-danger">激活</button>
          </div>
        </div>
      </div>
    )
  }
}

export default GetCertificateMange;
