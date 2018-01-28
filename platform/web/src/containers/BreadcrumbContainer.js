
import {connect} from 'react-redux'
import Breadcrumb from '../components/Breadcrumb/Breadcrumb'
import makeBreadcrumbSelector from '../selectors/breadcrumbSelector'
const mapStateToProps = (state) => {
  const isSidebarOpenSelector = makeBreadcrumbSelector();
  return {
    breadcrumbList: isSidebarOpenSelector(state)
  }
}


const BreadcrumbContainer = connect(
  mapStateToProps,
)(Breadcrumb)

export default BreadcrumbContainer
