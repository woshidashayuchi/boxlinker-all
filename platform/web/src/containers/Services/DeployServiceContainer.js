
import DeployService from '../../components/DeployService/DeployService';
import {connect} from 'react-redux';
import {
  fetchDeployServiceAction,
} from '../../actions/deployService';
import  {
  addPortAction,
  delPortAction,
  addSaveAction,
  delSaveAction,
  addEnvAction,
  delEnvAction,
  deploySeniorAction,
} from '../../actions/deployService'
import { fetchVolumesListAction } from '../../actions/volumes';
import makeVolumeListSelector from '../../selectors/volumesListSelector';
import makeGetDeployData from '../../selectors/deployDataSelector';
import makeIsSidebarOpenSelector from '../../selectors/isSidebarOpenSelector';
import makeIsBtnStateSelector from '../../selectors/isBtnStateSelector';
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'

const mapStateToProps = (state) => {
  const selectorVolume = makeVolumeListSelector();
  const deployData = makeGetDeployData();
  const isSidebarOpenSelector = makeIsSidebarOpenSelector();
  const isBtnStateSelector = makeIsBtnStateSelector();
  return {
    volumeList: selectorVolume(state),
    deployData: deployData(state),
    isSidebarOpen: isSidebarOpenSelector(state),
    isBtnState:isBtnStateSelector(state),
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    onDeployService : (data) => {
      dispatch(fetchDeployServiceAction(data));
    },
    onDeploySenior :(data) =>{
      dispatch(deploySeniorAction(data))
    },
    onVolumeListLoad:()=>{
      dispatch(fetchVolumesListAction())
    },
    onAddPort:() =>{
      dispatch(addPortAction())
    },
    onDelPort:(item)=>{
      dispatch(delPortAction(item))
    },
    onAddSave:() =>{
      dispatch(addSaveAction())
    },
    onDelSave:(item)=>{
      dispatch(delSaveAction(item))
    },
    onAddEnv:() =>{
      dispatch(addEnvAction())
    },
    onDelEnv:(item) => {
      dispatch(delEnvAction(item))
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    }


  }
};

const DeployServiceContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(DeployService);

export default DeployServiceContainer
