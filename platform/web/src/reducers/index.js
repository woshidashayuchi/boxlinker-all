import { combineReducers } from 'redux'
import runtime from './runtime';
import {
  TOGGLE_SIDEBAR,
  SIDEBAR_STATUS,
  SIDEBAR_ACTIVE,
  RECEIVE_VOLUMES_LIST,
  GET_ALL_SERVICES,
  GET_SERVICE_DETAIL,
  GET_REPO_LIST,
  IS_LOADING,
  GET_IMAGE_LIST,
  GET_IMAGE_DETAIL,
  RECEIVE_USER_INFO,
  RECEIVE_LOG,
  OPEN_LOG_XHR,
  ABORT_LOG_XHR,
  BREADCRUMB_LIST,
  GET_GITHUB_AUTH_URL,
  ADD_PORT,
  DEL_PORT,
  ADD_SAVE,
  DEL_SAVE,
  ADD_ENV,
  DEL_ENV,
  DEPLOY_SVC_IMAGE,
  DEPLOY_SVC_CONTAINER,
  DEPLOY_SVC_SENIOR,
  GET_BUILDING_IMAGE_LIST,
  RECEIVE_NOTIFICATION,
  CLEAR_NOTIFICATION,
  CLEAR_SERVICE_DETAIL,
  CLEAR_SERVICE_LIST,
  CLEAR_VOLUMES_LIST,
  CLEAR_IMAGE_LIST,
  GET_POD_LIST,
  IS_BTN_STATE
} from '../constants';

import * as Const from '../constants'

const serviceData = {
  policy:1,
  pods_num:1,
  service_name:"",
  containerDeploy:0,
  containerNum:1,
  isUpdate:1,
  container:[{at:new Date().getTime()}],
  env:[{at:new Date().getTime()}],
  volume:[{at:new Date().getTime(),readonly:0}],
  auto_startup:1
};

function isSidebarOpen(state = SIDEBAR_STATUS.OPEN, action){
  switch (action.type){
    case TOGGLE_SIDEBAR:
      return action.status;
    default:
      return state;
  }
}

function sidebarActive(state = "", action){
  switch (action.type){
    case SIDEBAR_ACTIVE:
      return action.payload;
    default:
      return state;
  }
}

function serviceList(state = [1],action){
  switch (action.type){
    case GET_ALL_SERVICES:
      return action.payload;
    case CLEAR_SERVICE_LIST:
      return [];
    case Const.REFRESH_LIST:
      return [0];
    default:
      return state;
  }
}

function podList(state = [1],action) {
  switch (action.type){
    case GET_POD_LIST:
      return action.payload;
    default:
      return state;
  }
}

function serviceDetail(state = serviceData ,action){
  switch(action.type){
    case GET_SERVICE_DETAIL :
      return action.payload;
    case ADD_PORT:
      let addPort = state.container;
      addPort.push({at:new Date().getTime()});
      return Object.assign({},state,{container:addPort});
    case DEL_PORT:
      let delPort = state.container;
      if(delPort.length == 1){}else {
        for (let j = 0; j < delPort.length; j++) {
          if (delPort[j].at == action.payload) {
            delPort.splice(j, 1)
          }
        }
      }
      return Object.assign({},state,{container:delPort});
    case ADD_SAVE:
      let addSave = state.volume;
      addSave.push({at:new Date().getTime(),readonly:1});
      return Object.assign({},state,{volume:addSave});
    case DEL_SAVE:
      let delSave = state.volume;
      if(delSave.length == 1){
        return Object.assign({},state,{volume:[{at:new Date().getTime(),readonly:1}],});
      }else {
        for(let m=0;m<delSave.length;m++){
          if(delSave[m].at == action.payload){
            delSave.splice(m,1)
          }
        }
        return Object.assign({},state,{volume:delSave});
      }
    case ADD_ENV:
      let addEnv = state.env;
      addEnv.push({at:new Date().getTime()});
      return Object.assign({},state,{env:addEnv});
    case DEL_ENV:
      let env = state.env;
      if(env.length == 1){
        return Object.assign({},state,{env:[{at:new Date().getTime()}]});
      }else {
        for (let i = 0; i < env.length; i++) {
          if (env[i].at == action.payload) {
            env.splice(i, 1)
          }
        }
        return Object.assign({},state,{env:env});
      }
    case Const.RECEIVE_ENDPOINTS:
      return Object.assign({},state,{endpoints: action.payload});
    case CLEAR_SERVICE_DETAIL:
      return serviceData;
    default :
      return state;
  }
}

function monitorData(state = {memory:{},network:{},cpu:{}},action){
  switch (action.type){
    case Const.GET_MONITOR_DATA:
      switch (action.flag){
        case "memory":
          return Object.assign({},state,{memory: action.payload});
          break;
        case "network":
          return Object.assign({},state,{network: action.payload});
          break;
        case "cpu":
          return Object.assign({},state,{cpu: action.payload});
      }
      break;
    default:
      return state;
  }
}

function volumesList(state = [1],action){
  switch (action.type) {
    case RECEIVE_VOLUMES_LIST:
        return action.payload.map((item)=>{
          item.disk_used = item.disk_used == 'yes'?0:1;
          return item;
        });
    case CLEAR_VOLUMES_LIST:
      return [];
    case Const.REFRESH_LIST:
      return [0];
    default:
          return state
  }
}

function isBtnState(
  state = {deploy:true,building:true,volume:true,autoStateUp:true,reviseBuilding:true,
    port:true,storage:true,env:true,command:true,pods:true,setOrg:true}
  ,action){
  switch (action.type){
    case IS_BTN_STATE.deploy:
      state.deploy = action.payload;
      return Object.assign({},state);
    case IS_BTN_STATE.building:
      state.building = action.payload;
      return Object.assign({},state);
    case IS_BTN_STATE.createVolume:
      state.createVolume = action.payload;
      return Object.assign({},state);
    case Const.IS_BTN_STATE.autoStateUp:
      state.autoStateUp = action.payload;
          return Object.assign({},state);
    case Const.IS_BTN_STATE.reviseBuilding:
      state.reviseBuilding = action.payload;
          return Object.assign({},state);
    case Const.IS_BTN_STATE.port:
      state.port = action.payload;
      return Object.assign({},state);
    case Const.IS_BTN_STATE.storage:
      state.storage = action.payload;
      return Object.assign({},state);
    case Const.IS_BTN_STATE.env:
      state.env = action.payload;
      return Object.assign({},state);
    case Const.IS_BTN_STATE.command:
      state.command = action.payload;
      return Object.assign({},state);
    case Const.IS_BTN_STATE.pods:
      state.pods = action.payload;
      return Object.assign({},state);
    case Const.IS_BTN_STATE.setOrg:
      state.setOrg = action.payload;
      return Object.assign({},state);
    default:
      return state;
  }
}

function repos(state = [],action){
  switch (action.type) {
    case GET_REPO_LIST:
        return action.payload;
    default:
          return state
  }
}

function isLoading(state = false,action){
  switch (action.type) {
    case IS_LOADING:
        return action.payload;
    default:
          return state
  }
}

function imageList(state = [1],action){
  switch (action.type){
    case GET_IMAGE_LIST:
      return action.payload;
    default:
      return state;
  }
}

function imageDetail(state = {} ,action){
  switch(action.type){
    case GET_IMAGE_DETAIL :
      return action.payload;
    default :
      return state;
  }
}

function user_info(state = {},action){
  switch(action.type){
    case RECEIVE_USER_INFO:
          return action.payload;
    default:
          return state;
  }
}

function breadcrumbList(state = [],action){
  switch(action.type){
    case BREADCRUMB_LIST :
      return action.payload;
    default :
      return state;
  }
}

function authUrl(state = {github:"",coding:""},action){
  switch(action.type){
    case GET_GITHUB_AUTH_URL :
      state.github = action.payload;
      return Object.assign({},state);
      break;
    case Const.GET_CODING_AUTH_URL:
      state.coding = action.payload;
      return Object.assign({},state);
      break;
    default :
      return state;
  }
}

function buildingImageList(state = [1],action){
  switch (action.type){
    case GET_BUILDING_IMAGE_LIST:
      return action.payload;
    case CLEAR_IMAGE_LIST:
      return [];
    case Const.REFRESH_LIST:
      return [0];
    default :
      return state;
  }
}
function buildingDetail(state = {},action){
  switch (action.type){
    case Const.GET_BUILDING_DETAIL:
      return action.payload;
    default :
      return state;
  }
}

function deployData(state = serviceData,action){
  switch (action.type){
    case DEPLOY_SVC_IMAGE:
      return Object.assign({},state,{
        image_name: action.payload.image_name,
        image_id:action.payload.image_id
      });
    case DEPLOY_SVC_CONTAINER:
      return Object.assign({},state,action.payload);
    case DEPLOY_SVC_SENIOR:
      return Object.assign({},state,action.payload);
    case ADD_PORT:
      let addPort = state.container;
      addPort.push({at:new Date().getTime()});
      return Object.assign({},state,{container:addPort});
    case DEL_PORT:
      let delPort = state.container;
      if(delPort.length<=1){
        return Object.assign({},state,{container:delPort});
      }else {
        for (let j = 0; j < delPort.length; j++) {
          if (delPort[j].at == action.payload) {
            delPort.splice(j, 1)
          }
        }
        return Object.assign({},state,{container:delPort});
      }
    case ADD_SAVE:
      let addSave = state.volume;
      addSave.push({at:new Date().getTime(),readonly:1});
      return Object.assign({},state,{volume:addSave});
    case DEL_SAVE:
      let delSave = state.volume;
      if(delSave.length<=1){
        return Object.assign({}, state, {volume: delSave});
      }else {
        for (let m = 0; m < delSave.length; m++) {
          if (delSave[m].at == action.payload) {
            delSave.splice(m, 1)
          }
        }
        return Object.assign({}, state, {volume: delSave});
      }
    case ADD_ENV:
      let addEnv = state.env;
      addEnv.push({at:new Date().getTime()});
      return Object.assign({},state,{env:addEnv});
    case DEL_ENV:
      let env = state.env;
      if(env.length<=1){
        return Object.assign({},state,{env:env});
      }else{
        for(let i=0;i<env.length;i++){
          if(env[i].at == action.payload){
            env.splice(i,1)
          }
        }
        return Object.assign({},state,{env:env});
      }
    case Const.CLEAR_DEPLOY_DATA:
      return serviceData;
    default:
      return state;
  }
}

function logs(state = [],action){
  switch (action.type){
    case RECEIVE_LOG:
          return [].concat(state).concat(action.payload);
    default:
          return state;
  }
}

function logs_xhr(state = {},action) {
  switch (action.type){
    case OPEN_LOG_XHR:
          return action.payload;
    case ABORT_LOG_XHR:
          state.abort();
          return {};
    default:
          return state;
  }
}

function notifications(state = {},action){
  switch (action.type){
    case RECEIVE_NOTIFICATION:
          return action.payload;
    case CLEAR_NOTIFICATION:
          return {};
    default:
          return state
  }
}
function organizeList(state = [1],action){
  switch (action.type){
    case Const.GET_ORGANIZE_LIST:
      return action.payload;
    break;
    default :
        return state
  }
}
function organizeDetail(state = {creation_time:""},action){
  switch (action.type){
    case Const.GET_ORGANIZE_DETAIL:
      return action.payload;
      break;
    default:
      return Object.assign({},state);
  }
}
function organizeUserList(state = [1],action){
  switch (action.type){
    case Const.GET_ORGANIZE_USER_LIST:
      return action.payload;
      break;
    default :
      return state
  }
}
function dashboard(state = {
  cpu_b:"0%",
  cpu_limit:0,
  cpu_usage:0,
  memory_b:"0%",
  memory_limit:0,
  memory_usage:0,
  flag:1
},action){
  switch (action.type){
    case Const.GET_DASHBOARD:
      return action.payload;
    default:
      return state;
  }

}
function userList(state = [],action){
  switch (action.type){
    case Const.GET_USER_LIST:
      return action.payload;
    break;
    default:
      return state;
  }
}

function balance(state = 0,action){
  switch(action.type){
    case Const.GET_BALANCE:
      return action.payload;
    default:
      return state
  }

}

const rootReducer = combineReducers({
  dashboard,
  isSidebarOpen,
  sidebarActive,
  volumesList,
  serviceList,
  serviceDetail,
  monitorData,
  podList,
  repos,
  isLoading,
  imageList,
  imageDetail,
  user_info,
  breadcrumbList,
  authUrl,
  buildingImageList,
  buildingDetail,
  deployData,
  logs,
  logs_xhr,
  notifications,
  runtime,
  isBtnState,
  organizeList,
  organizeDetail,
  organizeUserList,
  userList,
  balance
});


export default rootReducer
