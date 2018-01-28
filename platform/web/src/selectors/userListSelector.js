import {createSelector} from 'reselect'

//getUserList
const getUserList = (state) => state.userList;

const makeGetUserListSelector = () => {
  return createSelector(
    [getUserList],
    (userList) => {
      return userList
    }
  )
};

export default makeGetUserListSelector
