
import {createSelector} from 'reselect'

const getIsBtnState = (state) => state.isBtnState;

const makeIsBtnStateSelector = () => {
  return createSelector(
    [getIsBtnState],
    (isBtnState) => {
      return isBtnState
    }
  )
};

export default makeIsBtnStateSelector
