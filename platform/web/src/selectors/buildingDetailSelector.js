
import {createSelector} from 'reselect';

//getBuildingDetail
const getBuildingDetail = (state) => {
  return state.buildingDetail;
};

const makeGetBuildingDetail = () => {
  return createSelector(
    [getBuildingDetail],
    (buildingDetail) => {
      return buildingDetail
    },

  )
};

export default makeGetBuildingDetail
