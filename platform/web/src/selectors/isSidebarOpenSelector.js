
import { createSelector } from 'reselect';

const getIsSidebarOpen = (state) => state.isSidebarOpen;

const makeIsSidebarOpenSelector = () =>{
  return createSelector(
    [getIsSidebarOpen],
    (isSidebarOpenFilter) => {
      return isSidebarOpenFilter
    }
  )
};

export default makeIsSidebarOpenSelector

