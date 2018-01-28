
import {connect} from 'react-redux'
import App from '../components/App'
import makeIsSidebarOpenSelector from '../selectors/isSidebarOpenSelector'
import makeGetNotificationsSelector from '../selectors/notificationsSelector'
import {init} from '../actions/notification'

const mapStateToProps = (state) => {
  const isSidebarOpenSelector = makeIsSidebarOpenSelector();
  const notificationsSelector = makeGetNotificationsSelector();
  return {
    isSidebarOpen: isSidebarOpenSelector(state),
    notifications: notificationsSelector(state)
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onInit: (username) => {
      dispatch(init(username))
    }

  }
}

const SidebarContainer = connect(
  mapStateToProps,
  mapDispatchToProps,
)(App)

export default SidebarContainer
