
import ServiceList from '../../components/Service/ServiceList'
import {connect} from 'react-redux'
import {
  fetchAllServicesAction,
  fetchDeleteServiceAction,
  fetchChangeStateAction,
  refreshServiceList,
} from '../../actions/services'
import makeGetServiceListSelector from '../../selectors/serviceListSelector'
import makeIsLoadingSelector from '../../selectors/isLoadingSelector'
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'

const mapStateToProps = (state) => {
  const selector = makeGetServiceListSelector();
  const isLoadingSelector = makeIsLoadingSelector();
  return {
    serviceList: selector(state),
    isLoading: isLoadingSelector(state)
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    onServiceListLoad : (txt)=>{
      dispatch(fetchAllServicesAction(txt))
    },
    onDeleteService : (data) => {
      dispatch(fetchDeleteServiceAction(data))
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    onChangeState:(data) => {
      dispatch(fetchChangeStateAction(data))
    },
    onClearServiceList:() => {
      dispatch(refreshServiceList())
    }
  }
}

const ServiceListContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(ServiceList);

export default ServiceListContainer
