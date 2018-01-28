import {createSelector} from 'reselect'

//logs
const getLogs = (state) => state.notifications;

const makeGetNotificationsSelector = () => {
  return createSelector(
    [getLogs],
    (notifications) =>{
      return notifications
    }
  )
};

export default makeGetNotificationsSelector
