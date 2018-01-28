import {createSelector} from 'reselect'

//logs_xhr
const getLogs_xhr = (state) => state.logs_xhr;

const maleLogs_xhrSelector = () => {
  return createSelector(
    [getLogs_xhr],
    (logs_xhr) =>{
      return logs_xhr
    }
  )
};

export default maleLogs_xhrSelector
