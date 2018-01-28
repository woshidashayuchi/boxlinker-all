
import {
  GET_ALL_SERVICES,
  API_SERVICE_URL,
  API_DELETE_SERVICE_URL,
  REFRESH_LIST,
} from '../constants'
import {isLoadingAction} from './header';
import fetch from 'isomorphic-fetch';
import {receiveNotification,clearNotification} from './notification';
import {fetchServiceDetailAction} from './serviceDetail';
import {navigate} from "./route";

function receiveServices(data){
  return {
    type: GET_ALL_SERVICES,
    payload: data
  }
}

export function fetchAllServicesAction(txt){
  let url =  txt ? `${API_SERVICE_URL}?&service_name=`+txt : `${API_SERVICE_URL}`;
  let myInit = {
    method:"GET",
    headers:{token:localStorage.getItem("_at")},
  };
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch(url , myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json);
        if (json.status == 0) {
          dispatch(receiveServices(json.result))
        } else {
          dispatch(receiveNotification({message:"获取列表失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(receiveServices([]))
        }
        dispatch(isLoadingAction(false));
      })
      .catch(e => {
        dispatch(isLoadingAction(false));
        console.error('get all services error:',e)
      })
  }
}

export  function fetchDeleteServiceAction(data){
  let url =`${API_DELETE_SERVICE_URL}`+"/"+data.serviceName,
      myInit = {
        method:"DELETE",
        headers:{token:localStorage.getItem("_at")},
      };
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch (url,myInit)
            .then(response => response.json())
            .then(json => {
              console.log(json);
              if(json.status == 0){
                dispatch(receiveNotification({message:"删除成功",level:"success"}));
                setTimeout(function(){
                  dispatch(clearNotification())
                },3000);
                  if(data.type == "list"){
                      dispatch(fetchAllServicesAction());
                  }else{
                      dispatch(navigate("/serviceList"));
                  }
              }else{
                dispatch(receiveNotification({message:"删除失败",level:"danger"}));
                setTimeout(function(){
                  dispatch(clearNotification())
                },3000);
                console.error(json);
              }
              dispatch(isLoadingAction(false));
            })
            .catch(e => {
              dispatch(receiveNotification({message:"程序错误",level:"danger"}));
              setTimeout(function(){
                dispatch(clearNotification())
              },3000);
              dispatch(isLoadingAction(false));
              console.error('delete service error',e)
            })
  }
}

export function fetchChangeStateAction(data){
  console.log({"operate":data.state});
  let url =`${API_SERVICE_URL}`+"/"+data.serviceName+"/status",
    myInit = {
      method:"PUT",
      headers:{token:localStorage.getItem("_at")},
      body:JSON.stringify({operate:data.state})
    };
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch (url,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json);
        if(json.status == 0){
          dispatch(receiveNotification({message:"修改成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(fetchAllServicesAction());
          dispatch(fetchServiceDetailAction(data.serviceName));
        }else{
          dispatch(receiveNotification({message:"修改失败:"+json.msg,level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
          console.error(json);
        }
        dispatch(isLoadingAction(false));
      })
      .catch(e => {
        dispatch(isLoadingAction(false));
        console.error('status service error',e)
      })
  }
}

export function refreshServiceList(){
  return {
    type: REFRESH_LIST,
  }
}

