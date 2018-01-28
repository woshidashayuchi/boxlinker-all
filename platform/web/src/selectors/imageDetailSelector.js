
import {createSelector} from 'reselect';

//getImageDetail
const getImageDetail = (state) => {
  return state.imageDetail;
};

const makeGetImageDetail = () => {
  return createSelector(
    [getImageDetail],
    (imageDetail) => {
      return imageDetail
    },

  )
};

export default makeGetImageDetail
