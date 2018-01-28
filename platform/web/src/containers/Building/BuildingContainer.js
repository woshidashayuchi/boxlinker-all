import Building from '../../components/Building/Building'
import {connect} from 'react-redux'
import {
  fetchBuildingImageListAction,
  fetchFastBuildingAction,
  refreshBuildingList,
  onDeleteImageAction
} from '../../actions/building'
import makeGetBuildingImageListSelector from '../../selectors/buildingImageListSelector'
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'

const mapStateToProps = (state) => {
  const selector = makeGetBuildingImageListSelector();
  return {
    buildingImageList: selector(state)
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    onImageList : ()=>{
      dispatch(fetchBuildingImageListAction())
    },
    onFastBuilding:(obj) => {
      dispatch(fetchFastBuildingAction(obj));
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    onClearImageList:() => {
      dispatch(refreshBuildingList())
    },
    onDeleteImage:(data) =>{
      dispatch(onDeleteImageAction(data))
    }
  }
}

const BuildingContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Building);

export default BuildingContainer
