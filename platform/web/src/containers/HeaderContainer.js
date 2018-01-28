
import {connect} from 'react-redux'
import {toggleSidebarAction} from '../actions/toggleSidebar'
import Header from '../components/Header';
import * as funOrganize from  '../actions/organize';
import makeIsSidebarOpenSelector from '../selectors/isSidebarOpenSelector'
import makeIsLoadingSelector from '../selectors/isLoadingSelector';
import makeGetOrganizeListSelector from '../selectors/organizeListSelector';

const mapStateToProps = (state) => {
  const isSidebarOpenSelector = makeIsSidebarOpenSelector();
  const isLoadingSelector = makeIsLoadingSelector();
  const getOrganizeList = makeGetOrganizeListSelector();
  return {
    isSidebarOpen: isSidebarOpenSelector(state),
    isLoading: isLoadingSelector(state),
    organizeList:getOrganizeList(state)
  }
};


const mapDispatchToProps = (dispatch) => {
  return {
    onSidebarToggleClick: (flag) => {
      dispatch(toggleSidebarAction(flag))
    },
    getOrganizeList:() =>{
      dispatch(funOrganize.fetchGetOrganizeListAction())
    },
    changeAccount:(id) =>{
      dispatch(funOrganize.fetchChangeAccountAction(id))
    }
  }
};

const SidebarContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Header);

export default SidebarContainer
