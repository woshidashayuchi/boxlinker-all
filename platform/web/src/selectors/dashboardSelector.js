
import {createSelector} from 'reselect';

//getDashboard
const getDashboardData = (state) => {
  return state.dashboard;
};

const makeGetDashboardData = () => {
  return createSelector(
    [getDashboardData],
    (dashboard) => {
      return dashboard
    },
  )
};

export default makeGetDashboardData
