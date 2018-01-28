import {
  API_SERVICE_URL,
  CPU,
  DEPLOY_SVC_IMAGE,
  DEPLOY_SVC_CONTAINER,
  DEPLOY_SVC_SENIOR,
  ADD_PORT,
  DEL_PORT,
  ADD_SAVE,
  DEL_SAVE,
  DEL_ENV,
  ADD_ENV,
  IS_BTN_STATE,
  CLEAR_DEPLOY_DATA
} from '../constants';
import { navigate } from './route';
import {isLoadingAction} from "./header"
import fetch from 'isomorphic-fetch';
import {receiveNotification,clearNotification} from './notification';

export function deployImageNameAction(obj){
  return {
    type: DEPLOY_SVC_IMAGE,
    payload: obj,
  }
}

export function goToConfigContainer(obj){
  return dispatch =>{
    dispatch(deployImageNameAction(obj));
    dispatch(navigate("/configContainer"));
  }
}


export function deployContainerAction(data) {
  return{
    type:DEPLOY_SVC_CONTAINER,
    payload:data
  }
}

export function goToService(){
  return dispatch =>{
    dispatch(navigate(`/addService`));
  }
}

export function deploySeniorAction(data){
  return{
    type:DEPLOY_SVC_SENIOR,
    payload:data
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

export function isDeploy(state){
  return{
    type:IS_BTN_STATE.deploy,
    payload:state
  }
}

export function clearDeployData(){
  return{
    type:CLEAR_DEPLOY_DATA
  }
}

export function fetchDeployServiceAction(data){
  let container_cpu = CPU[data.containerDeploy].x,
      container_memory = CPU[data.containerDeploy].m;
  data.container_cpu = container_cpu;
  data.container_memory = container_memory;
  if(data.env[0].env_key == ""){
    data.env = "";
  }
  if(data.volume[0].disk_name == -1){
    data.volume = "";
  }
  delete data.containerDeploy;
  let myInit = {
    method:"POST",
    headers:{token:localStorage.getItem("_at")},
    body:JSON.stringify(data)
  };
  console.log(JSON.stringify(data));
  return dispatch =>{
    dispatch(isLoadingAction(true));
    dispatch(isDeploy(false));
    return fetch(`${API_SERVICE_URL}/`+data.service_name,myInit)
            .then(response => response.json())
            .then(json => {
              console.log('>>>>>',json);
              dispatch(isLoadingAction(false));
              dispatch(isDeploy(true));
              if(json.status==0){
                dispatch(clearDeployData());
                dispatch(navigate(`/serviceList/${data.service_name}/3`));
              }else if(json.status==301){
                dispatch(receiveNotification({message:"部署失败:服务名称已存在",level:"danger"}));
                setTimeout(function(){
                  dispatch(clearNotification())
                },5000);
              }else{
                dispatch(receiveNotification({message:"部署失败:"+json.msg,level:"danger"}));
                setTimeout(function(){
                  dispatch(clearNotification())
                },5000);
                console.error("部署失败",json);
              }
            })
            .catch (e => {
              dispatch(isLoadingAction(false));
              dispatch(isDeploy(true));
              console.error("部署失败" ,e)
            })
  }
}
