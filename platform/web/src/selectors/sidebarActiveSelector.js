
import { createSelector } from 'reselect';

const getSidebarActive = (state) => state.sidebarActive;

const makeSidebarActiveSelector = () =>{
  return createSelector(
    [getSidebarActive],
    (sidebarActive) => {
      return sidebarActive
    }
  )
};

export default makeSidebarActiveSelector

