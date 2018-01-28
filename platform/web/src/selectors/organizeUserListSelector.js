
import {createSelector} from 'reselect'

const getOrganizeUserList = (state) => state.organizeUserList;

const makeGetOrganizeUserListSelector = () => {
  return createSelector(
    [getOrganizeUserList],
    (organizeUserList) => {
      return organizeUserList
    }
  )
};

export default makeGetOrganizeUserListSelector
