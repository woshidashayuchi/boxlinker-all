import {
  API_SERVICE_URL,
  GET_SERVICE_DETAIL,
  CPU,
  ADD_PORT,
  DEL_PORT,
  ADD_SAVE,
  DEL_SAVE,
  DEL_ENV,
  ADD_ENV,
  CLEAR_SERVICE_DETAIL,
  GET_POD_LIST
} from '../constants'
import * as Const from '../constants';
import fetch from 'isomorphic-fetch';
import {isLoadingAction} from './header';
import {receiveNotification,clearNotification} from './notification';

function receiveServiceDetail (data){
  return {
    type : GET_SERVICE_DETAIL,
    payload : data
  }
}

export function clearServiceDetail(){
  return {
    type :CLEAR_SERVICE_DETAIL,
    payload:{}
  }
}

export function fetchServiceDetailAction(serviceName){
  let myInit = {
        method : "GET",
        headers:{token:localStorage.getItem("_at")},
      },
      url = `${API_SERVICE_URL}`+"/"+serviceName+"/details";
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json,">>>>>>servicerDetail");
        if(json.status == 0){
          let containerDeploy = 0;
          let data = json.result[0];
          CPU.map((item , i) =>{
              if(item.x==data.limits_cpu){
                containerDeploy = i;
              }
          });
          data.containerDeploy = containerDeploy;
          if(data.env.length == 0){data.env.push({})}
          data.env.map((item,i) =>{
            item.at = new Date().getTime()+i;
          });
          data.container.map((item,i) =>{
            item.at = new Date().getTime()+i;
          });
          if(data.volume.length == 0){data.volume.push({})}
          data.volume.map((item,i) =>{
            item.at = new Date().getTime()+i;
          });
          dispatch(receiveServiceDetail(data));
        }else{
          console.error(json);
        }
        dispatch(isLoadingAction(false));
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        console.error("serviceDetail is error",e);
      })
  }
}

export function addPortAction() {
  return {
    type:ADD_PORT
  }
}
export function delPortAction(item){
  return{
    type:DEL_PORT,
    payload:item
  }
}
export function addSaveAction() {
  return {
    type:ADD_SAVE
  }
}
export function delSaveAction(item){
  return{
    type:DEL_SAVE,
    payload:item
  }
}
export function delEnvAction(item){
  return {
    type: DEL_ENV,
    payload: item
  }
}

export function addEnvAction() {
  return {
    type:ADD_ENV
  }
}
export function savePortAction(flag) {
  return {
    type:Const.IS_BTN_STATE.port,
    payload:flag
  }
}
export function saveStorageAction(flag) {
  return {
    type:Const.IS_BTN_STATE.storage,
    payload:flag
  }
}
export function saveEnvAction(flag) {
  return {
    type:Const.IS_BTN_STATE.env,
    payload:flag
  }
}
export function saveCommandAction(flag) {
  return {
    type:Const.IS_BTN_STATE.command,
    payload:flag
  }
}
export function savePodsAction(flag) {
  return {
    type:Const.IS_BTN_STATE.pods,
    payload:flag
  }
}


export function fetchSavePortAction(data){
  let json = JSON.stringify({container:data.container});
  console.log(json);
  let myInit = {
    method : "PUT",
    headers:{token:localStorage.getItem("_at")},
    body :json
  };
  return dispatch => {
    dispatch(isLoadingAction(true));
    dispatch(savePortAction(false));
    return fetch(`${API_SERVICE_URL}/`+data.serviceName+`/container`,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json,">>>>>>更新端口");
        if(json.status == 0){
          dispatch(receiveNotification({message:"更新成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(fetchServiceDetailAction(data.serviceName));
        }else{
          dispatch(receiveNotification({message:"更新失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
          console.error(json);
        }
        dispatch(isLoadingAction(false));
        dispatch(savePortAction(true));
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        dispatch(savePortAction(true));
        console.error("SavePort is error",e);
      })
  }
}

export function fetchSaveVolumeAction(data){
  let json = JSON.stringify({volume:data.volume});
  console.log(json);
  let myInit = {
    method : "PUT",
    headers:{token:localStorage.getItem("_at")},
    body :json
  };
  return dispatch => {
    dispatch(isLoadingAction(true));
    dispatch(saveStorageAction(false));
    return fetch(`${API_SERVICE_URL}/`+data.serviceName+`/volume`,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json,">>>>>>更新端口");
        if(json.status == 0){
          dispatch(receiveNotification({message:"更新成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(fetchServiceDetailAction(data.serviceName));
        }else{
          dispatch(receiveNotification({message:"更新失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
          console.error(json);
        }
        dispatch(isLoadingAction(false));
        dispatch(saveStorageAction(true));
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        dispatch(saveStorageAction(true));
        console.error("SaveVolume is error",e);
      })
  }
}

export function fetchSaveEnvironmentAction(data){
  if(data.env[0].env_key==""){
    data.env = "";
  }
  let json = JSON.stringify({env:data.env});
  console.log(json);
  let myInit = {
    method : "PUT",
    headers:{token:localStorage.getItem("_at")},
    body :json
  };
  return dispatch => {
    dispatch(isLoadingAction(true));
    dispatch(saveEnvAction(false));
    return fetch(`${API_SERVICE_URL}/`+data.serviceName+`/env`,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json, " >>>>>>>更新环境变量")
        if(json.status == 0){
          dispatch(receiveNotification({message:"更新成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(fetchServiceDetailAction(data.serviceName));
        }else{
          dispatch(receiveNotification({message:"更新失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
          console.error(json);
        }
        dispatch(isLoadingAction(false));
        dispatch(saveEnvAction(true));
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        dispatch(saveEnvAction(true));
        console.error("serviceDetail is error",e);
      })
  }
}

export function fetchSaveContainerDeployAction(data){
  console.log(data);
  let container_cpu = CPU[data.containerDeploy].x,
    container_memory = CPU[data.containerDeploy].m;
  let json = JSON.stringify({
    container_cpu:container_cpu,
    container_memory:container_memory
  });
  console.log(json);
  let myInit = {
    method : "PUT",
    headers:{token:localStorage.getItem("_at")},
    body :json
  };
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch(`${API_SERVICE_URL}/`+data.serviceName+`/cm`,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json, " >>>>>>>更新容器配置")
        if(json.status == 0){
          dispatch(receiveNotification({message:"更新成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(fetchServiceDetailAction(data.serviceName));
        }else{
          dispatch(receiveNotification({message:"更新失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
          console.error(json);
        }
        dispatch(isLoadingAction(false));
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        console.error("serviceDetail is error",e);
      })
  }
}

export function onSavePodsAction(data) {
  let json = JSON.stringify({pods_num:data.n});
  let myInit = {
    method : "PUT",
    headers:{token:localStorage.getItem("_at")},
    body :json
  };
  return dispatch => {
    dispatch(isLoadingAction(true));
    dispatch(savePodsAction(false));
    return fetch(`${API_SERVICE_URL}/`+data.serviceName+`/telescopic`,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json,">>>>>>更新容器个数");
        if(json.status == 0){
          dispatch(receiveNotification({message:"更新成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(fetchServiceDetailAction(data.serviceName));
        }else{
          dispatch(receiveNotification({message:"更新失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
          console.error(json);
        }
        dispatch(isLoadingAction(false));
        dispatch(savePodsAction(true));
      })
      .catch (e => {
        dispatch(savePodsAction(true));
        dispatch(isLoadingAction(false));
        console.error("pods_num is error",e);
      })
  }
}

export function receivePodList(data){
  return {
    type:GET_POD_LIST,
    payload:data
  }
}

export function fetchOnPodListLoadAction(name) {
  let myInit = {
      method : "GET",
      headers:{token:localStorage.getItem("_at")},
    },
    url = `${API_SERVICE_URL}`+"/"+name+"/pod/message";
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch(url, myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json, ">>>>>>pod");
        if (json.status == 0) {
          dispatch(receivePodList(json.result))
        }
        dispatch(isLoadingAction(false));
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        console.error("pod is error",e);
      })
  }
}

export function isAutoStateUp(flag) {
  return{
    type:Const.IS_BTN_STATE.autoStateUp,
    payload:flag
  }

}

export function fetchAutoStateUp(data) {
  let obj = {auto_startup:data.auto_startup};
  let myInit = {
      method : "PUT",
      headers:{token:localStorage.getItem("_at")},
      body:JSON.stringify(obj)
    },
    url = `${API_SERVICE_URL}`+"/"+data.serviceName+"/autostartup";
  return dispatch => {
    dispatch(isLoadingAction(true));
    dispatch(isAutoStateUp(false));
    return fetch(url, myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json, ">>>>>>autostartup");
        dispatch(isLoadingAction(false));
        dispatch(isAutoStateUp(true));
        if (json.status == 0) {
          dispatch(receiveNotification({message:"更新成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(fetchServiceDetailAction(data.serviceName));
        }else {
          dispatch(receiveNotification({message: "更新失败:" + json.msg, level: "danger"}));
          setTimeout(function () {
            dispatch(clearNotification())
          }, 5000);
        }
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        console.error("pod is error",e);
      })
  }
}

function receiveMonitorData(data,flag){
  return {
    type:Const.GET_MONITOR_DATA,
    payload:data,
    flag:flag
  }
}
export function fetchGetMonitorDataAction(data) {
  let myInit = {
    method : "GET",
    headers:{token:localStorage.getItem("_at")},
  };
  let url = Const.FETCH_URL.GET_SERVICE_MONITOR+"/"+data.userName+"/pods/"+data.pod_name+"/metrics/"+data.type+
    "?time_long="+data.time_long//+"&time_span="+data.time_span;
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json);
        dispatch(isLoadingAction(false));
        if(json.status == 0){
          dispatch(receiveMonitorData(json.result,data.type));
        }
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        console.error("monitor is error",e);
      })
  }
}

function isChange(flag){
  return {
    type:Const.IS_BTN_STATE.deploy,
    payload:flag
  }
}

export function fetchChangeReleaseAction(data){
  let obj = JSON.stringify({
    image_name:data.image_name,
    image_version:data.image_version,
    policy:data.policy,
  });
  console.log(obj,"publish 参数");
  let myInit = {
    method : "PUT",
    headers:{token:localStorage.getItem("_at")},
    body:obj
  };
  let url = Const.API_SERVICE_URL+"/"+data.serviceName+"/publish";
  return dispatch => {
    dispatch(isLoadingAction(true));
    dispatch(isChange(false));
    return fetch(url,myInit)
        .then(response => response.json())
        .then(json => {
          console.log(json);
          dispatch(isLoadingAction(false));
          dispatch(isChange(true));
          if(json.status == 0){
            dispatch(receiveNotification({message:"更新成功",level:"success"}));
            setTimeout(function(){
              dispatch(clearNotification())
            },3000);
          }else{
            dispatch(receiveNotification({message: "更新失败:" + json.msg, level: "danger"}));
            setTimeout(function () {
              dispatch(clearNotification())
            }, 5000);
          }
        })
        .catch (e => {
          dispatch(isLoadingAction(false));
          dispatch(isChange(true));
          console.error("publish is error",e);
        })
  }
}
export function fetchSaveCommand(data){
  let obj = JSON.stringify({
    command:data.command
  });
  let myInit = {
    method : "PUT",
    headers:{token:localStorage.getItem("_at")},
    body:obj
  };
  let url = Const.API_SERVICE_URL+"/"+data.serviceName+"/command";
  return dispatch => {
    dispatch(isLoadingAction(true));
    dispatch(saveCommandAction(false));
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json);
        dispatch(isLoadingAction(false));
        dispatch(saveCommandAction(true));
        if(json.status == 0){
          dispatch(receiveNotification({message:"更新成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
        }else{
          dispatch(receiveNotification({message: "更新失败:" + json.msg, level: "danger"}));
          setTimeout(function () {
            dispatch(clearNotification())
          }, 5000);
        }
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        dispatch(saveCommandAction(true));
        console.error("publish is error",e);
      })
  }
}
