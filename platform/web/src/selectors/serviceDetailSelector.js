
import {createSelector} from 'reselect';

//getServiceDetail
const getServiceDetail = (state) => {
  return state.serviceDetail;
};

const makeGetServiceDetail = () => {
  return createSelector(
    [getServiceDetail],
    (serviceDetail) => {
      return serviceDetail
    },

  )
};

export default makeGetServiceDetail
