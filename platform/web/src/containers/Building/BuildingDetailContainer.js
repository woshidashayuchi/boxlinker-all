import BuildingDetail from '../../components/Building/BuildingDetail'
import {connect} from 'react-redux'
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'
import {
  fetchFastBuildingAction,
  fetchBuildDetail,
  onDeleteImageAction,
  fetchReviseBuilding
} from '../../actions/building';
import makeGetBuildingDetail from '../../selectors/buildingDetailSelector';
import makeIsBtnStateSelector from '../../selectors/isBtnStateSelector';

const mapStateToProps = (state) => {
  const buildingDetail = makeGetBuildingDetail();
  const isBtnStateSelector = makeIsBtnStateSelector();
  return {
    buildingDetail:buildingDetail(state),
    isBtnState:isBtnStateSelector(state),
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    onFastBuilding:(id) => {
      dispatch(fetchFastBuildingAction(id));
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    getBuildingDetail:(id) => {
      dispatch(fetchBuildDetail(id))
    },
    onDeleteImage:(name,keyList) =>{
      dispatch(onDeleteImageAction(name,keyList))
    },
    reviseBuilding:(data) => {
      dispatch(fetchReviseBuilding(data))
    }
  }
};

const BuildingDetailContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(BuildingDetail);

export default BuildingDetailContainer
