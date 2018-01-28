
import {createSelector} from 'reselect'

const getVolumesList = (state) => state.volumesList

const makeGetVolumesListSelector = () => {
  return createSelector(
    [getVolumesList],
    (volumesList) => {
      return volumesList
    }
  )
}

export default makeGetVolumesListSelector
