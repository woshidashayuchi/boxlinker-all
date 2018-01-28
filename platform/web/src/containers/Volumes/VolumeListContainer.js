
import {connect} from 'react-redux'
import VolumeList from '../../components/Volumes/VolumeList'

import {
  fetchVolumesListAction,
  createVolume,
  deleteVolume,
  scaleVolume,
  refreshVolumeList,
} from '../../actions/volumes'
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'
import makeGetVolumesListSelector from '../../selectors/volumesListSelector'
import makeIsBtnStateSelector from '../../selectors/isBtnStateSelector';

const mapStateToProps = (state) => {
  const selector = makeGetVolumesListSelector();
  const isBtnStateSelector = makeIsBtnStateSelector();
  return {
    volumesList: selector(state),
    isBtnState:isBtnStateSelector(state),
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    setBreadcrumb: (...arr)=>{
      dispatch(setBreadcrumbAction(...arr))
    },
    onVolumesListLoad: () => {
      dispatch(fetchVolumesListAction())
    },
    onVolumeCreate: (data) => {
      dispatch(createVolume(data))
    },
    onVolumeDelete: (diskName) => {
      dispatch(deleteVolume(diskName))
    },
    onVolumeScale: (diskName,diskSize) => {
      dispatch(scaleVolume(diskName,diskSize))
    },
    onClearVolumesList:() => {
      dispatch(refreshVolumeList())
    }

  }
}

const VolumeTableContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(VolumeList)

export default VolumeTableContainer
