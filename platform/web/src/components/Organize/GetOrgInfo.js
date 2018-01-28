
import React,{PropTypes,Component} from 'react';
import HeadLine from '../../components/HeadLine';
import Toggle from '../Toggle';
import Loading from '../Loading';

class IsPublicToggle extends  Component{
  static propTypes={
    getToggle:React.PropTypes.func,
    state:React.PropTypes.bool,
    disabled:React.PropTypes.bool
  };
  constructor(props) {
    super(props);
    this.state = {
      is_public:this.props.state
    };
  }
  handClick(component, value){
    this.setState({
      is_public: !this.state.is_public,
    });
    this.props.getToggle(this.state.is_public);
  }
  componentDidMount(){
  }
  render(){
    return(
      <Toggle
        defaultChecked={this.state.is_public}
        onChange={this.handClick.bind(this)}
        disabled = {this.props.disabled}
      />
    )
  }
}

class GetOrgInfo extends Component{
  static contextTypes = {
    store:React.PropTypes.object
  };
  static propTypes = {
    getOrganizeDetail:React.PropTypes.func,
    organizeDetail:React.PropTypes.object,
    setOrganizeDetail:React.PropTypes.func,
    isBtnState:React.PropTypes.object
  };

  constructor(props){
    super(props);
    this.state = {
      is_public:0
    }
  }
  componentDidMount(){
    let organizeId = this.context.store.getState().user_info.orga_uuid;
    this.props.getOrganizeDetail(organizeId);
  }
  getToggleValue(value){
    let flag = !value ? 1 : 0;//1 true  0 false
    this.setState({
      is_public:flag
    })
  }

  setOrganizeDetail(){
    let data = {
      orga_detail:this.refs.orga_detail.value,
      is_public:this.state.is_public
    };
    this.props.setOrganizeDetail(data);
  }
  render(){
    let data = this.props.organizeDetail;
    let role_uuid = this.context.store.getState().user_info.role_uuid;
    let role = role_uuid == 200;
    if(data.creation_time == "") return <div style={{textAlign:"center"}}><Loading /></div>;
    return (
      <div className = "userTabBox" key = {new Date(data.creation_time).getTime()}>
        <div className = "userItem organizeBox">
          <HeadLine
            title="组织头像"
            titleEnglish=""
            titleInfo="ORGANIZE HEAD"
          />
          <div className = "userHead organizeItem">
            <div className="userHeadBox">
              <img />
            </div>
            <div className = "choose icon-operation">
              <span>更改头像</span>
            </div>
          </div>
          <HeadLine
            title="组织描述"
            titleEnglish=""
            titleInfo="ORGANIZE "
          />
          <div className = "organizeItem">
            {role?
              <textarea type = "text" className = "form-control" ref = "orga_detail" defaultValue={data.orga_detail} />
            :
              <p>{data.orga_detail}</p>
            }
          </div>
          <HeadLine
            title="是否公开"
            titleEnglish=""
            titleInfo="IS PUBLIC"
          />
          <div className = "organizeItem">
            <IsPublicToggle
              state = {data.is_public == 1}
              getToggle={this.getToggleValue.bind(this)}
              disabled={!role}
            />
          </div>
          <div className = "organizeItem organizeItemBtn ">
            <button className={`btn btn-primary ${!this.props.isBtnState.setOrg?"btn-loading":""}`}
                    disabled = {!this.props.isBtnState.setOrg}
                    onClick={this.setOrganizeDetail.bind(this)}>
              {this.props.isBtnState.setOrg?"保存":"保存中..."}
            </button>
          </div>
        </div>
      </div>
    )
  }
}

export default  GetOrgInfo;
