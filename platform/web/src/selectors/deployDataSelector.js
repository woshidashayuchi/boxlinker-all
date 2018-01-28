
import {createSelector} from 'reselect';

//getServiceDetail
const getDeployData = (state) => {
  return state.deployData;
};

const makeGetDeployData = () => {
  return createSelector(
    [getDeployData],
    (deployData) => {
      return deployData
    },
  )
};

export default makeGetDeployData
