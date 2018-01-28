import {createSelector} from 'reselect'

//getImageList
const getImageList = (state) => state.imageList;

const makeGetImageListSelector = () => {
  return createSelector(
    [getImageList],
    (imageList) => {
      return imageList
    }
  )
};

export default makeGetImageListSelector
