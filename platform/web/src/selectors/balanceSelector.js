
import {createSelector} from 'reselect';

//getBalance
const getBalance = (state) => {
  return state.balance;
};

const makeGetBalance = () => {
  return createSelector(
    [getBalance],
    (balance) => {
      return balance
    }

  )
};

export default makeGetBalance
