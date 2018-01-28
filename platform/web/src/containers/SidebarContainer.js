
import {connect} from 'react-redux'
import Sidebar from '../components/Sidebar'
import makeIsSidebarOpenSelector from '../selectors/isSidebarOpenSelector'
import makeSidebarActiveSelector from '../selectors/sidebarActiveSelector'
import {onChangeSidebarActiveAction} from '../actions/toggleSidebar'
const mapStateToProps = (state) => {
  const isSidebarOpenSelector = makeIsSidebarOpenSelector();
  const sidebarActive = makeSidebarActiveSelector()
  return {
    isSidebarOpen: isSidebarOpenSelector(state),
    sidebarActive : sidebarActive(state)
  }
}
const mapDispatchToProps = (dispatch) => {
  return {
    onChangeSidebarActive:(url) => {
      dispatch(onChangeSidebarActiveAction(url))
    }
  }
}


const SidebarContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Sidebar)

export default SidebarContainer
