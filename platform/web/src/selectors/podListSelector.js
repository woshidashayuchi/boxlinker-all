
import {createSelector} from 'reselect'

const getPodList = (state) => state.podList;

const makeGetPodListSelector = () => {
  return createSelector(
    [getPodList],
    (podList) => {
      return podList
    }
  )
}

export default makeGetPodListSelector
