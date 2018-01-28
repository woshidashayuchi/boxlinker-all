
import {createSelector} from 'reselect'

//getServiceList
const getServiceList = (state) => state.serviceList;

const makeGetServiceListSelector = () => {
  return createSelector(
    [getServiceList],
    (serviceList) => {
      return serviceList
    }
  )
};

export default makeGetServiceListSelector


