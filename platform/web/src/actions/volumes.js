
import {
  RECEIVE_VOLUMES_LIST,
  API_VOLUMES_URL,
  REFRESH_LIST,
  IS_BTN_STATE
} from '../constants'

import fetch from 'isomorphic-fetch'
import {isLoadingAction} from './header'
import {receiveNotification,clearNotification} from './notification';

export function receiveVolumes(volumes) {
  return {
    type: RECEIVE_VOLUMES_LIST,
    payload: volumes
  }
}

export function refreshVolumeList(){
  return {
    type:REFRESH_LIST
  }
}

function isCreateVolume(state){
  return {
    type:IS_BTN_STATE.createVolume,
    payload:state
  }
}

export function createVolume(data){
  console.log(data,">>>>>>");
  return dispatch => {
    dispatch(isLoadingAction(true));
    dispatch(isCreateVolume(false));
    return fetch(`${API_VOLUMES_URL}`,{
      method: 'POST',
      headers: {
        token: localStorage.getItem('_at')
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(json => {
        if (json.status == 0){
          let d = json.result;
          console.log(`create volume ${d.pool_name}/${d.disk_name} success!`,d);
          dispatch(receiveNotification({message:"创建成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(fetchVolumesListAction())
        } else {
          console.error('create volume error: ', json)
        }
        dispatch(isLoadingAction(false));
        dispatch(isCreateVolume(true));
      })
      .catch(e => {
        dispatch(isLoadingAction(false));
        dispatch(isCreateVolume(true));
        console.error('create volume error: ',e)
      })
  }
}

export function scaleVolume(diskName,diskSize){
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch(`${API_VOLUMES_URL}/${diskName}`,{
      method: 'PUT',
      headers:{
        token: localStorage.getItem('_at')
      },
      body: JSON.stringify({disk_size:diskSize})
    }).then(response => response.json())
      .then(json => {
        if ( json.status == 0 ){
          dispatch(receiveNotification({message:"扩容成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(fetchVolumesListAction())
        }else {
          dispatch(receiveNotification({message:"扩容失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
          console.error(`scale volume ${diskName} failed!`,json)
        }
        dispatch(isLoadingAction(false));
      })
      .catch(e => {
        dispatch(isLoadingAction(false));
        console.error(`scale volume ${diskName} error!`,e)
      })
  }
}

export function deleteVolume(diskName){
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch(`${API_VOLUMES_URL}/${diskName}`,{
      method: 'DELETE',
      headers: {
        token: localStorage.getItem('_at')
      }
    }).then(response => response.json())
      .then(json => {
        if ( json.status == 0 ){
          dispatch(receiveNotification({message:"删除成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(fetchVolumesListAction())
        }else {
          dispatch(receiveNotification({message:"删除失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
          console.error(`delete volume ${diskName} failed!`,json)
        }
        dispatch(isLoadingAction(false));
      })
      .catch(e => {
        dispatch(receiveNotification({message:"程序错误",level:"danger"}));
        setTimeout(function(){
          dispatch(clearNotification())
        },5000);
        dispatch(isLoadingAction(false));
        console.error(`delete volume ${diskName} error!`,e)
      })
  }
}

export function fetchVolumesListAction(){
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch(`${API_VOLUMES_URL}`,{
      headers:{
        token:localStorage.getItem("_at")
      }
    })
      .then(response => {
        return response.json()
      })
      .then(json => {
        if (json.status == 0) {
          dispatch(receiveVolumes(json.result.volume_list))
        } else {
          dispatch(receiveNotification({message:"获取列表失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(receiveVolumes([]))
          console.error('get all volumes failed:',json);
        }
        dispatch(isLoadingAction(false));
      })
      .catch((e)=>{
        dispatch(isLoadingAction(false));
        console.error('get all volumes error:',e);
      })
  }
}
