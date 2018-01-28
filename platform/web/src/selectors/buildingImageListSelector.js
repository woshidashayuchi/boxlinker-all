import {createSelector} from 'reselect'

//getImageList
const getImageList = (state) => state.buildingImageList;

const buildingImageListSelector = () => {
  return createSelector(
    [getImageList],
    (buildingImageList) => {
      return buildingImageList
    }
  )
};

export default buildingImageListSelector
