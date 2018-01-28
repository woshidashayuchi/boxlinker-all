
import {createSelector} from 'reselect';

//getMonitorData
const getMonitorData = (state) => {
  return state.monitorData;
};

const makeGetMonitorDataSelector = () => {
  return createSelector(
    [getMonitorData],
    (monitorData) => {
      return monitorData
    },

  )
};

export default makeGetMonitorDataSelector
