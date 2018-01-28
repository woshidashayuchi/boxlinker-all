import Dashboard from '../components/Dashboard/Dashboard'
import {connect} from 'react-redux'
import {
  setBreadcrumbAction,
} from '../actions/breadcumb'
import {
  fetchAllServicesAction,
} from '../actions/services'
import makeGetServiceListSelector from '../selectors/serviceListSelector'
import {fetchImageListAction } from "../actions/imageList";
import makeGetImageListSelector from '../selectors/imageListSelector';
import {
  fetchVolumesListAction,
} from '../actions/volumes'
import makeGetVolumesListSelector from '../selectors/volumesListSelector';
import makeGetDashboardData from '../selectors/dashboardSelector';
import {fetchGetDashboardAction} from "../actions/dashboard";

const mapStateToProps = (state) => {
  const selectorServiceList = makeGetServiceListSelector();
  const selectorImage = makeGetImageListSelector();
  const selectorVolumesList = makeGetVolumesListSelector();
  const selectorDashboard = makeGetDashboardData()
  return {
    serviceList: selectorServiceList(state),
    imageList :selectorImage(state),
    volumesList: selectorVolumesList(state),
    dashboard:selectorDashboard(state)
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    onServiceListLoad : (txt)=>{
      dispatch(fetchAllServicesAction(txt))
    },
    onImageListLoad : () => {
      dispatch(fetchImageListAction());
    },
    onVolumesListLoad: () => {
      dispatch(fetchVolumesListAction())
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    onDashboardLoad:() =>{
      dispatch(fetchGetDashboardAction())
    }
  }
}

const DashboardContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Dashboard);

export default DashboardContainer
