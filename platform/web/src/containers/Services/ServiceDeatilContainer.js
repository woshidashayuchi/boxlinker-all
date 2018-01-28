
import ServiceDetail from '../../components/ServiceDeatil/ServiceDetail';
import {connect} from 'react-redux';
import {
  fetchServiceDetailAction,
  fetchSavePortAction,
  fetchSaveVolumeAction,
  fetchSaveEnvironmentAction,
  fetchSaveContainerDeployAction,
  addPortAction,
  delPortAction,
  addSaveAction,
  delSaveAction,
  addEnvAction,
  delEnvAction,
  clearServiceDetail,
  onSavePodsAction,
  fetchOnPodListLoadAction,
  fetchAutoStateUp,
  fetchGetMonitorDataAction
} from '../../actions/serviceDetail';
import {fetchChangeStateAction,fetchDeleteServiceAction} from '../../actions/services'
import * as actions from '../../actions/serviceDetail'
import { fetchVolumesListAction } from '../../actions/volumes';
import makeServiceDetailSelector from '../../selectors/serviceDetailSelector';
import makeVolumeListSelector from '../../selectors/volumesListSelector';
import makeLogsSelector from '../../selectors/logsSelector';
import maleLogs_xhrSelector from '../../selectors/logs_shrSelector';
import makeGetNotificationsSelector from '../../selectors/notificationsSelector';
import makePodListSelector from '../../selectors/podListSelector';
import makeGetBuildingDetail from '../../selectors/buildingDetailSelector';
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'
import makeIsBtnStateSelector from '../../selectors/isBtnStateSelector';
import makeGetMonitorDataSelector from '../../selectors/monitorDataSelector';
import {
    fetchBuildDetail
} from '../../actions/building';

const makeMapStateToProps = () => {
  const selector = makeServiceDetailSelector();
  const selectorVolume = makeVolumeListSelector();
  const selectorLogs = makeLogsSelector();
  const selectorLogs_xhrSelector = maleLogs_xhrSelector();
  const notificationsSelector = makeGetNotificationsSelector();
  const selectorPodList = makePodListSelector();
  const isBtnStateSelector = makeIsBtnStateSelector();
  const getMonitorData = makeGetMonitorDataSelector();
  const buildingDetail = makeGetBuildingDetail();
  const mapStateToProps = (state) => {
    return {
      serviceDetail : selector(state),
      volumeList: selectorVolume(state),
      logs:selectorLogs(state),
      logs_xhr:selectorLogs_xhrSelector(state),
      notifications: notificationsSelector(state),
      podList:selectorPodList(state),
      isBtnState:isBtnStateSelector(state),
      monitorData:getMonitorData(state),
      buildingDetail:buildingDetail(state)
    }
  };
  return mapStateToProps;
};

const mapDispatchToProps = (dispatch) => {
  return {
    onServiceDetailLoad : (serviceName) => {
      dispatch(fetchServiceDetailAction(serviceName));
    },
    onSavePort: (data) => {
      dispatch(fetchSavePortAction(data))
    },
    onSaveVolume:(data) => {
      dispatch(fetchSaveVolumeAction(data))
    },
    onSaveEnvironment:(data) => {
      dispatch(fetchSaveEnvironmentAction(data))
    },
    onVolumeListLoad:()=>{
      dispatch(fetchVolumesListAction())
    },
    onSaveContainerDeploy:(data) =>{
      dispatch(fetchSaveContainerDeployAction(data))
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
    },
    onClearServiceDetail:() => {
      dispatch(clearServiceDetail())
    },
    onSavePods:(data) => {
      dispatch(onSavePodsAction(data))
    },
    onPodListLoad:(name) =>{
      dispatch(fetchOnPodListLoadAction(name))
    },
    onChangeState:(data) => {
      dispatch(fetchChangeStateAction(data))
    },
    onAutoStateUp:(data) => {
      dispatch(fetchAutoStateUp(data))
    },
    getMonitorData:(data) => {
      dispatch(fetchGetMonitorDataAction(data))
    },
    getBuildingDetail:(id) => {
      dispatch(fetchBuildDetail(id))
    },
    onChangeRelease:(data) =>{
      dispatch(actions.fetchChangeReleaseAction(data))
    },
    onSaveCommand:(data) =>{
      dispatch(actions.fetchSaveCommand(data))
    },
    onDeleteService : (data) => {
      dispatch(fetchDeleteServiceAction(data))
    },
  }
};

const ServiceDetailContainer = connect(
  makeMapStateToProps,
  mapDispatchToProps
)(ServiceDetail);

export default ServiceDetailContainer
