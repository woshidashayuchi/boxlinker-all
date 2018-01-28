import Organize from '../../components/Organize/Organize';
import {connect} from 'react-redux'
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb';
import * as fun from '../../actions/organize';
import makeGetOrganizeDetail  from '../../selectors/organizeDetailSelector';
import makeGetOrganizeUserList from '../../selectors/organizeUserListSelector';
import makeGetUserList from '../../selectors/userListSelector';
import makeIsBtnStateSelector from '../../selectors/isBtnStateSelector';
const mapStateToProps = (state) => {
  const getOrganizeDetail = makeGetOrganizeDetail();
  const getOrganizeUserList = makeGetOrganizeUserList();
  const getUserList = makeGetUserList();
  const isBtnStateSelector = makeIsBtnStateSelector();
  return {
    organizeDetail:getOrganizeDetail(state),
    organizeUserList:getOrganizeUserList(state),
    userList:getUserList(state),
    isBtnState:isBtnStateSelector(state),
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    getOrganizeDetail:(id) =>{
      dispatch(fun.fetchGetOrganizeDetailAction(id))
    },
    setOrganizeDetail:(data) => {
      dispatch(fun.fetchSetOrganizeDetailAction(data))
    },
    getOrganizeUserList:(id) =>{
      dispatch(fun.fetchGetOrganizeUserListAction(id))
    },
    getUserList:(name) =>{
      dispatch(fun.fetchGetUserListAction(name))
    },
    inviteUser:(data) =>{
      dispatch(fun.fetchInviteUser(data))
    },
    changeUserRole:(data) =>{
      dispatch(fun.fetchChangeUserRoleAction(data))
    },
    changeOrganizeOwner:(data) =>{
      dispatch(fun.fetchChangeOrganizeOwnerAction(data))
    },
    deleteOrganize:(data) =>{
      dispatch(fun.fetchDeleteOrganize(data))
    },
    leaveOrganize:(data) =>{
      dispatch(fun.fetchLeaveOrganize(data))
    }
  }
};

const OrganizeContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Organize);

export default OrganizeContainer
