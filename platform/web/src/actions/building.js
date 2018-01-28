
import {GET_REPO_LIST,FETCH_URL,
  GET_GITHUB_AUTH_URL,
  GET_BUILDING_IMAGE_LIST,
  IS_BTN_STATE,
  REFRESH_LIST
} from '../constants'
import * as Const from "../constants";
import {isLoadingAction} from './header'
import fetch from 'isomorphic-fetch'
import {navigate} from './route';
import {receiveNotification,clearNotification} from './notification';
import {fetchImageListAction} from './imageList';

function receiveRepoListAction (data){
  return {
    type : GET_REPO_LIST,
    payload : data
  }
}

function isBuilding(state){
  return {
    type:IS_BTN_STATE.building,
    payload:state
  }
}

function receiveBuildingImageListAction (data){
  return {
    type : GET_BUILDING_IMAGE_LIST,
    payload : data
  }
}

function receiveAuthURLAction(type,url){
  let action_type ;
  switch (type){
    case "github":
      action_type = Const.GET_GITHUB_AUTH_URL;
      break;
    case "coding":
      action_type = Const.GET_CODING_AUTH_URL;
      break;
    default:
      action_type = Const.GET_GITHUB_AUTH_URL;
  }
  return {
    type: action_type,
    payload: url
  }
}

export function fetchGetAuthURLLAction(data){
  let body = JSON.stringify(data);
  console.log(body,"授权链接参数");
  return (dispatch) => {
    dispatch(isLoadingAction(true));
    return fetch(FETCH_URL.AUTH_URL,{
      method:'POST',
      headers:{
        token: localStorage.getItem('_at')
      },
      body:body
    }).then(response => response.json())
      .then(json => {
        console.log(json,"获取授权链接");
        if (json.status == 0){
          switch (data.src_type){
            case "github":
              dispatch(receiveAuthURLAction("github",json.result.msg));
              break;
            case "coding":
              dispatch(receiveAuthURLAction("coding",json.result.msg));
          }
        }else {
          console.error('fetchGithubAuthURLAction error: ',json)
        }
        dispatch(isLoadingAction(false));
      })
      .catch(e => {
        dispatch(isLoadingAction(false));
        console.error('fetchGithubAuthURLAction error:',e)
      })
  }
}

export function fetchRepoListAction (key,refresh){
  let parameter = refresh==true?"?refresh=true":"";
  return (dispatch) => {
    dispatch(isLoadingAction(true));
    return fetch(FETCH_URL.REPOS+parameter,{
      method: 'GET',
      headers:{
        token: localStorage.getItem('_at'),
        varbox:key
      }
      }
    ).then(response => response.json())
      .then(json => {
        if (json.status == 0){
          dispatch(receiveRepoListAction(json.result))
        }else {
          console.error('fetch repos error: ',json)
        }
        dispatch(isLoadingAction(false))
      })
      .catch(e => {
        console.error('fetch reopos error:',e);
        dispatch(isLoadingAction(false))
      })

  }
}

export function fetchBuildingImageListAction(){
  let myInit = {
    method:"GET",
    headers:{token:localStorage.getItem("_at")}
  };
  return(dispatch)=>{
    dispatch(isLoadingAction(true));
    return fetch(FETCH_URL.IMAGE+"?is_code=true",myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json);
        dispatch(isLoadingAction(false));
        if(json.status==0){
          dispatch(receiveBuildingImageListAction(json.result))
        }else{
          console.error("buildingImageList error",json);
        }
      })
      .catch (e => {
        dispatch(isLoadingAction(true));
        console.error("buildingImageList error" ,e);
      })
  }
}

export function fetchFastBuildingAction(obj){
  let myInit = {
    method:"PUT",
    headers:{
      token:localStorage.getItem("_at"),
      varbox:obj.id
    }

  };
  return(dispatch)=>{
    dispatch(isLoadingAction(true));
    return fetch(FETCH_URL.BUILDING,myInit)
      .then(response => response.json())
      .then(json =>{
        dispatch(isLoadingAction(false));
        console.log("快速构建返回值",json);
        if(json.status==0){
          if(obj.flag == "list"){
            dispatch(navigate(`/building/${obj.id}`));
          }else {
            dispatch(fetchBuildDetail(obj.id));
          }
        }else{
          console.error("fast building error",json);
        }
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        console.error("fast building error" ,e);
      })
  }
}

export function fetchBuildingAction(data){
  let body = JSON.stringify(data);
  console.log(body,">>>>>>>>构建镜像  参数")
  let myInit = {
    method:"POST",
    headers:{token:localStorage.getItem("_at")},
    body:body
  };
  return(dispatch)=>{
    dispatch(isLoadingAction(true));
    dispatch(isBuilding(false));
    return fetch(FETCH_URL.IMAGE,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json,">>>>>>>>>构建镜像接口");
        if(json.status==0){
          dispatch(navigate(`/building/${json.result.uuid}`));
        }else if(json.status==706){
          dispatch(receiveNotification({message:"创建失败:镜像名称已存在",level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
        }else{
          dispatch(receiveNotification({message:"创建失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },5000);
          console.error("building error",json);
        }
        dispatch(isLoadingAction(false));
        dispatch(isBuilding(true));
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        dispatch(isBuilding(true));
        console.error("building error" ,e);
      })
  }
}

export function refreshBuildingList(){
  return {
    type: REFRESH_LIST,
  }
}

export function onDeleteImageAction(data){
  let myInit = {
    method:"DELETE",
    headers:{
      token:localStorage.getItem("_at"),
      imagename:data.name
    }
  };
  let url = FETCH_URL.IMAGE_LIST+"?imagename="+data.name;
  return(dispatch)=>{
    dispatch(isLoadingAction(true));
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json =>{
        console.log("删除镜像返回值",json);
        dispatch(isLoadingAction(false));
        if(json.status==0){
          switch (data.keyList){
            case "myList":
              dispatch(navigate("/imageForMy"));
                  break;
            case "imageList" :
              dispatch(fetchImageListAction(false));
                  break;
            case "buildingList" :
              dispatch(fetchBuildingImageListAction());
                  break;
            case "detail":
              dispatch(navigate("/building"));
                  break;
          }
          dispatch(receiveNotification({message:"删除成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
        }else{
          dispatch(receiveNotification({message:"删除失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
          console.error("fast building error",json);
        }
      })
      .catch (e => {
        dispatch(receiveNotification({message:"程序错误",level:"danger"}));
        setTimeout(function(){
          dispatch(clearNotification())
        },3000);
        dispatch(isLoadingAction(false));
        console.error("fast building error" ,e);
      })
  }
}

function receiveBuildingDetail(data){
  return{
    type:Const.GET_BUILDING_DETAIL,
    payload:data
  }
}

export function fetchBuildDetail(id) {
  let myInit = {
    method:"GET",
    headers:{
      token:localStorage.getItem("_at"),
    }
  };
  let url = FETCH_URL.IMAGE+"?only=true&repository_id="+id;
  return(dispatch) =>{
    dispatch(isLoadingAction(true));
    return fetch(url,myInit)
      .then(response =>response.json())
      .then(json=>{
        dispatch(isLoadingAction(false));
        console.log(json,">>>>>构建镜像详情");
        if(json.status == 0){
          dispatch(receiveBuildingDetail(json.result));
        }else{
          console.error("获取构建详情失败",json)
        }
      })
      .catch(e =>{
        dispatch(isLoadingAction(false));
        console.error("获取构建详情失败",e);
      })
  }
}

function isReviseBuilding(state){
  return{
    type:IS_BTN_STATE.reviseBuilding,
    payload:state
  }
}

export function fetchReviseBuilding(data){
  let body = JSON.stringify({
    dockerfile_path:data.dockerfile_path,
    repo_branch:data.repo_branch,
    auto_build:data.auto_build,
  });
  let myInit = {
    method:"PUT",
    headers:{
      token:localStorage.getItem("_at"),
    },
    body:body
  };
  let url = FETCH_URL.BUILDING_REVISE+"/"+data.uuid;
  return(dispatch) => {
    dispatch(isLoadingAction(true));
    dispatch(isReviseBuilding(false));
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json => {
        console.log("修改镜像返回值",json);
        dispatch(isLoadingAction(false));
        dispatch(isReviseBuilding(true));
        if(json.status == 0){
          dispatch(receiveNotification({message:"修改成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
        }else{
          dispatch(receiveNotification({message:"修改失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification())
          },3000);
        }
      })
      .catch(e=>{
        dispatch(isLoadingAction(false));
        console.error("修改失败",e);
      })
  }
}
