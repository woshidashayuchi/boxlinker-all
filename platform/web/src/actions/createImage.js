/**
 * Created by zhangsai on 16/10/10.
 */
import {
  FETCH_URL,
  IS_BTN_STATE
} from '../constants';
import {isLoadingAction} from './header';
import fetch from 'isomorphic-fetch';
import {receiveNotification,clearNotification} from './notification';
import {navigate} from './route';

function isBuilding(state){
  return {
    type:IS_BTN_STATE.building,
    payload:state
  }
}

export function fetchCreateImageAction(data){
  let body = JSON.stringify(data);
  console.log(body,">>>>>>新建镜像  参数");
  let myInit = {
    method:"POST",
    headers:{
      token:localStorage.getItem("_at")
    },
    body:body
  };
  return(dispatch)=>{
    dispatch(isLoadingAction(true));
    dispatch(isBuilding(false));
    return fetch(FETCH_URL.IMAGE,myInit)
      .then(response => response.json())
      .then(json => {
        if(json.status==0){
          console.log(json,"新建镜像 返回值")
          dispatch(receiveNotification({message:"创建成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          dispatch(navigate(`/imageDetail/${json.result.uuid}`));
        }else{
          dispatch(receiveNotification({message:"创建失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
          console.error("createImage error",json);
        }
        dispatch(isLoadingAction(false));
        dispatch(isBuilding(true));
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        dispatch(isBuilding(true));
        console.error("createImage error" ,e);
      })
  }
}
