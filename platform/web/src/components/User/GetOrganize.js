import React,{PropTypes,Component,} from 'react';
import HeadLine from '../HeadLine';
import {Modal} from 'react-bootstrap';
import Loading from '../Loading';
import Confirm from '../Confirm';
import {navigate} from '../../actions/route';

class GetOrganize extends Component {
    static contextTypes = {
        store:React.PropTypes.object
    };
    static propTypes = {
        createOrganize:React.PropTypes.func,
        organizeList:React.PropTypes.array,
        getOrganizeList:React.PropTypes.func,
        leaveOrganize:React.PropTypes.func,
        deleteOrganize:React.PropTypes.func
    };
    constructor(){
        super();
        this.state = {
            orgData:{
                orgId:"",
                ketList:""
            }
        }
    }
    createOrganize(org_name){
        this.props.createOrganize(org_name);
        this.refs.createOrgModel.hide();

    }
    leaveOrganize(id){
        this.setState({
            orgData:{
                orgId:id,
                keyList:"orgList"
            }
        });
        this.refs.confirmModalLeave.open();
    }
    deleteOrganize(id){
        this.setState({
            orgData:{
                orgId:id,
                keyList:"orgList"
            }
        });
        this.refs.confirmModalDelete.open();
    }
    getOrganizeBody(){
        let data = this.props.organizeList;
        let user_name = this.context.store.getState().user_info.user_name;
        if(data[0] == 1) return <tr><td colSpan = "5" style = {{textAlign:"center"}}><Loading /></td></tr>;
        if(data.length == 1 && data[0].orga_name == user_name) return <tr><td colSpan = "5" style = {{textAlign:"center"}}>暂无数据~</td></tr>;
        if(data.length == 0) return <tr><td colSpan = "5" style = {{textAlign:"center"}}>暂无数据~</td></tr>;
        let role = "";
        return data.map((item,i) =>{
            if(item.orga_name == user_name) return false;
            let opt = <button className="btn btn-danger" onClick = {this.leaveOrganize.bind(this,item.org_id)}>退出组织</button>;
            switch (Number(item.role)){
                case 200 :
                    role = "组织拥有者";
                    opt = <button className="btn btn-danger" onClick = {this.deleteOrganize.bind(this,item.org_id)}>解散组织</button>;
                break;
                case 210 :
                    role = "管理员";
                break;
                case 400 :
                    role = "成员";
                break;
                default :
                    role = "成员";
            }
            return (
                <tr key = {i}>
                    <td>
                        <div className="mediaItem">
                            <img className="mediaImg" src = "/slImgJx.png" />
                            <span className="mediaTxt">{item.orga_name}</span>
                        </div>
                    </td>
                    <td>{item.org_detail||"暂无简介"}</td>
                    <td>{role}</td>
                    <td>
                        {opt}
                    </td>
                </tr>
            )
        })
    }
    getTableDemo(){
       return (
           <table className="table table-hover table-bordered">
               <thead>
               <tr>
                   <th width = "25%">组织名称</th>
                   <th width = "25%">组织简介</th>
                   <th width = "25%">组织权限</th>
                   <th width = "25%">操作</th>
               </tr>
               </thead>
               <tbody>
                {this.getOrganizeBody()}
               </tbody>
           </table>
       )
    }
    componentDidMount(){
        this.props.getOrganizeList();
    }
    componentWillMount(){
        let is_user = this.context.store.getState().user_info.is_user;
        if(is_user == 0){
            this.context.store.dispatch(navigate("/"));
        }
    }
    render(){
        return(
            <div className="organize">
                <div className="organizeHd hbHd clearfix">
                    <div className = "left">
                        <HeadLine
                            title = "我的组织"
                            titleEnglish = "MY ORGANIZE"
                            titleInfo = "所有我加入的组织的列表"
                        />
                    </div>
                    <div className="hbAdd right">
                        <div className="hbAddBtn clearfix" onClick = {() => {this.refs.createOrgModel.open()}}>
                            <div className="hbPlus left"></div>
                            <div className="hbPlusInfo left">
                                <p className="hbPName">新建组织</p>
                                <p className="hbPInfo">Create Organize</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="organizeBd sl-bd TableTextLeft">
                    {this.getTableDemo()}
                </div>
                <CreateOrganize onCreateOrganize = {this.createOrganize.bind(this)} ref = "createOrgModel" />
                <Confirm
                  title = "警告"
                  text = "您确定要离开此组织吗?"
                  ref = "confirmModalLeave"
                  func = {() => {this.props.leaveOrganize(this.state.orgData)}}
                />
                <Confirm
                  title = "警告"
                  text = "您确定要解散此组织吗?"
                  ref = "confirmModalDelete"
                  func = {() => {this.props.deleteOrganize(this.state.orgData)}}
                />
            </div>
        )
    }

}

class CreateOrganize extends Component{
    static propTypes = {
        onCreateOrganize:React.PropTypes.func
    };
    constructor(props){
        super(props);
        this.state = {
            show:false,
            orgName:false
        }
    }
    open(){
        this.setState({
            show:true,
        })
    }
    hide(){
        this.setState({
            show:false
        })
    }
    createOrganize(){
        let org_name = this.refs.org_name;
        let org_tip = this.refs.org_tip;
        if(!org_name.value){
            this.setState({
                orgName:true
            });
            org_tip.innerHTML = "组织名称不能为空";
            return false;
        }
        if(!this.state.orgName) {
            this.props.onCreateOrganize(org_name.value);
        }
    }
    organizeName(){
      let value = this.refs.org_name.value;
        let org_tip = this.refs.org_tip;
        if(value.length == 0){
            this.setState({
                orgName:false
            });
            return false;
        }else  if(value.length<6){
            this.setState({
                orgName:true
            });
            org_tip.innerHTML = "组织名称太短";
            return false;
        }else if (!/^[a-z]{1}[a-z0-9_]{5,}$/.test(value)){
            this.setState({
                orgName:true
            });
            org_tip.innerHTML = "组织名称格式不正确";
            return false;
        }else{
            this.setState({
                orgName:false
            });
        }
    }
    render(){
        return(
        <Modal {...this.props} show={this.state.show}
               onHide={this.hide.bind(this)}
               bsSize="sm" aria-labelledby="contained-modal-title-sm">
            <div className="modal-header">
                <button type="button" onClick={this.hide.bind(this)} className="close" aria-label="Close"><span aria-hidden="true">×</span></button>
                <h4 className="modal-title" id="contained-modal-title-sm">新建组织</h4>
            </div>
            <div className={this.state.orgName?"modal-body has-error":"modal-body"}>
                <div className="modalItem">
                    <label><span>组织名称</span></label>
                    <label>
                        <input  onInput = {this.organizeName.bind(this)}
                                className="form-control form-control-sm"
                               type="input" placeholder="请输入名称"
                               ref="org_name"/></label>
                </div>
                <div ref = "org_tip" className="volumeTip">组织名称不正确</div>
                <div className="modalItem modelItemLast">
                    <label><span>{this.state.orgName} </span></label>
                    <label>
                        <button className="btn btn-primary"
                                onClick={this.createOrganize.bind(this)}>创建组织</button>
                    </label>
                </div>
            </div>
        </Modal>
        )
    }
}

export default GetOrganize;