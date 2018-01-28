
import {createSelector} from 'reselect';

//getOrganizeDetail
const getOrganizeDetail = (state) => {
  return state.organizeDetail;
};

const makeGetOrganizeDetail = () => {
  return createSelector(
    [getOrganizeDetail],
    (organizeDetail) => {
      return organizeDetail
    },

  )
};

export default makeGetOrganizeDetail
