
import {createSelector} from 'reselect';

//stepNumber
const getStepNumber = (state) => {
  return state.stepNumber;
};

const makeGetStepNumber = () => {
  return createSelector(
    [getStepNumber],
    (stepNumber) => {
      return stepNumber
    },
  )
};

export default makeGetStepNumber
