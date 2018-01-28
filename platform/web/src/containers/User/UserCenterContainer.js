import UserCenter from '../../components/User/UserCenter'
import {connect} from 'react-redux'
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'
import {
  fetchGetAuthURLLAction,
} from '../../actions/building';
import {makeGetAuthURLSelector} from '../../selectors/BuildingCreateSelector';
import * as funUser from '../../actions/users';
import * as funOrganize from  '../../actions/organize';
import makeGetOrganizeListSelector from '../../selectors/organizeListSelector';
import makeGetBalanceSelector from '../../selectors/balanceSelector';

const mapStateToProps = (state) => {
  const getAuthURL = makeGetAuthURLSelector();
  const getOrganizeList = makeGetOrganizeListSelector();
  const getBalance = makeGetBalanceSelector();
  return {
    authUrl: getAuthURL(state),
    organizeList:getOrganizeList(state),
    balance:getBalance(state)
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    getAuthURL: (data) => {
      dispatch(fetchGetAuthURLLAction(data))
    },
    onRevisePassword:(passwordObj) =>{
      dispatch(funUser.fetchRevisePasswordAction(passwordObj))
    },
    createOrganize:(org_name) =>{
      dispatch(funOrganize.fetchCreateOrganize(org_name))
    },
    getOrganizeList:() =>{
      dispatch(funOrganize.fetchGetOrganizeListAction())
    },
    leaveOrganize:(data) =>{
      dispatch(funOrganize.fetchLeaveOrganize(data))
    },
    deleteOrganize:(data) =>{
      dispatch(funOrganize.fetchDeleteOrganize(data))
    },
    getBalance:() =>{
      dispatch(funUser.fetchGetBalanceAction())
    }
  }
};

const UserCenterContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(UserCenter);

export default UserCenterContainer
