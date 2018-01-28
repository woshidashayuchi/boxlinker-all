
import Config from '../../components/ConfigContainer/ConfigContainer';
import {connect} from 'react-redux';
import {
  deployContainerAction,
  goToService
} from '../../actions/deployService';
import makeGetDeployData from '../../selectors/deployDataSelector';
import makeIsSidebarOpenSelector from '../../selectors/isSidebarOpenSelector'
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb';
import {
  fetchBuildDetail
} from '../../actions/building';
import makeGetBuildingDetail from '../../selectors/buildingDetailSelector';

const mapStateToProps = (state) => {
  const deployData = makeGetDeployData();
  const isSidebarOpenSelector = makeIsSidebarOpenSelector();
  const buildingDetail = makeGetBuildingDetail();
  return {
    deployData: deployData(state),
    isSidebarOpen: isSidebarOpenSelector(state),
    buildingDetail:buildingDetail(state)
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    deployContainer:(data) =>{
      dispatch(deployContainerAction(data))
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    onGoToService:() =>{
      dispatch(goToService())
    },
    getBuildingDetail:(id) => {
      dispatch(fetchBuildDetail(id))
    }
  }
};

const ConfigContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Config);

export default ConfigContainer
