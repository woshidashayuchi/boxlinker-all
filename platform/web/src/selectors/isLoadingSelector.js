
import { createSelector } from 'reselect';

const getIsLoading = (state) => state.isLoading;

const makeIsLoadingSelector = () =>{
  return createSelector(
    [getIsLoading],
    (isLoading) => {
      return isLoading
    }
  )
};

export default makeIsLoadingSelector

