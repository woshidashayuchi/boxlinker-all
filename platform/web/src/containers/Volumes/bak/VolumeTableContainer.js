
import {connect} from 'react-redux'
import VolumesTable from '../../components/Volumes/VolumesTable'

import {fetchVolumesListAction} from '../../actions/volumes'

import makeGetVolumesListSelector from '../../selectors/volumesListSelector'

const mapStateToProps = (state) => {
  const selector = makeGetVolumesListSelector();
  return {
    volumesList: selector(state)
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onVolumesListLoad: () => {
      dispatch(fetchVolumesListAction())
    }
  }
}

const VolumeTableContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(VolumesTable)

export default VolumeTableContainer
