import {createSelector} from 'reselect'

//logs
const getLogs = (state) => state.logs;

const makeGetLogsSelector = () => {
  return createSelector(
    [getLogs],
    (logs) =>{
      return logs
    }
  )
};

export default makeGetLogsSelector
