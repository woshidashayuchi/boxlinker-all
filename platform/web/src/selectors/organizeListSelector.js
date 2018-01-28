
import {createSelector} from 'reselect'

const getOrganizeList = (state) => state.organizeList;

const makeGetOrganizeListSelector = () => {
  return createSelector(
    [getOrganizeList],
    (organizeList) => {
      return organizeList
    }
  )
};

export default makeGetOrganizeListSelector
