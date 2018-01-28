import * as Const from '../constants';

import fetch from 'isomorphic-fetch';
import {receiveNotification,clearNotification} from './notification';
import cookie from 'react-cookie';
import {navigate} from './route';

export function fetchCreateOrganize(org_name){
  let body = JSON.stringify({orga_name:org_name});
  let myInit = {
    method:"POST",
    headers:{token:localStorage.getItem("_at")},
    body:body
  };
  let url = Const.FETCH_URL.ORGANIZE;
  return (dispatch =>{
    return fetch(url,myInit)
        .then(response => response.json())
        .then(json =>{
          console.log(json,"新建组织返回值");
          if(json.status == 0){
            dispatch(receiveNotification({message:"创建成功",level:"success"}));
            dispatch(fetchGetOrganizeListAction());
            setTimeout(function(){
              dispatch(clearNotification());
            },3000);
          }else{
            dispatch(receiveNotification({message:"创建失败:"+json.msg,level:"danger"}));
            setTimeout(function(){
              dispatch(clearNotification());
            },3000);
          }
        })
  })
}

function receiveOrganizeList(data){
  return {
    type:Const.GET_ORGANIZE_LIST,
    payload:data

  }
}

export function fetchGetOrganizeListAction(){
  let myInit = {
    method:"GET",
    headers:{token:localStorage.getItem("_at")},
  };
  let url = Const.FETCH_URL.ORGANIZE;
  return (dispatch =>{
    return fetch(url,myInit)
      .then(response => response.json())
        .then(json =>{
          console.log(json,"组织列表");
          if(json.status == 0){
            dispatch(receiveOrganizeList(json.result));
          }else{
            dispatch(receiveNotification({message:"获取组织列表失败:"+json.msg,level:"danger"}));
            setTimeout(function(){
              dispatch(clearNotification());
            },3000);
          }
        })
  })
}

export function fetchLeaveOrganize(data){
  let myInit = {
    method:"PUT",
    headers:{token:localStorage.getItem("_at")}
  };
  let url = Const.FETCH_URL.ORGANIZE+"/"+data.orgId;
  return (dispatch =>{
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json =>{
        console.log(json);
        if(json.status == 0){
          switch (data.keyList){
            case "orgList":
              dispatch(receiveNotification({message:"退出成功",level:"success"}));
              dispatch(fetchGetOrganizeListAction());
              setTimeout(function(){
                dispatch(clearNotification());
              },3000);
              break;
            case "userList":
              dispatch(receiveNotification({message:"退出成功",level:"success"}));
              var exp = new Date();
              exp.setTime(exp.getTime()+1000*60*60*24*7);
              cookie.save('_at',json.result.token,{path:'/',expires: exp});
              localStorage.setItem("_at",json.result.token);
              location.href = '/';
              setTimeout(function(){
                dispatch(clearNotification());
              },3000);
              break;

          }
        }else{
          dispatch(receiveNotification({message:"退出失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }
      })
  })
}

export function fetchDeleteOrganize(data){
  let myInit = {
    method:"DELETE",
    headers:{token:localStorage.getItem("_at")}
  };
  let url = Const.FETCH_URL.ORGANIZE+"/"+data.orgId;
  return (dispatch =>{
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json =>{
        console.log(json);
        if(json.status == 0){
          dispatch(receiveNotification({message:"解散成功",level:"success"}));
          switch (data.keyList){
            case "orgList":
              dispatch(fetchGetOrganizeListAction());
              break;
            case "userList":
              dispatch(receiveNotification({message:"解散成功",level:"success"}));
              var exp = new Date();
              exp.setTime(exp.getTime()+1000*60*60*24*7);
              cookie.save('_at',json.result.token,{path:'/',expires: exp});
              localStorage.setItem("_at",json.result.token);
              location.href = '/';
              setTimeout(function(){
                dispatch(clearNotification());
              },3000);
              break;
          }
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }else{
          dispatch(receiveNotification({message:"解散失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }
      })
  })
}

function receiveOrganizeDetail(data){
  return{
    type:Const.GET_ORGANIZE_DETAIL,
    payload:data
  }
}

export function fetchGetOrganizeDetailAction(id){
  let myInit = {
    method:"GET",
    headers:{token:localStorage.getItem("_at")}
  };
  let url = Const.FETCH_URL.ORGANIZE+"/"+id;
  return (dispatch =>{
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json =>{
        console.log(json);
        if(json.status == 0){
          dispatch(receiveOrganizeDetail(json.result));
        }else{
          dispatch(receiveNotification({message:"获取组织详情失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }
      })
  })
}

function isLoading(state){
  return {
    type:Const.IS_BTN_STATE.setOrg,
    payload:state
  }
}

export function fetchSetOrganizeDetailAction(data){
  let body = JSON.stringify({
    orga_detail:data.orga_detail,
    is_public:String(data.is_public)
  });
  console.log(body,"修改组织参数");
  let myInit = {
    method:"PUT",
    headers:{token:localStorage.getItem("_at")},
    body:body
  };
  let url = Const.FETCH_URL.ORGANIZE;
  return (dispatch =>{
    dispatch(isLoading(false));
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json =>{
        console.log(json,"修改组织返回值");
        dispatch(isLoading(true));
        if(json.status == 0){
          dispatch(receiveNotification({message:"修改成功",level:"success"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }else{
          dispatch(receiveNotification({message:"修改失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }
      })
  })
}

function receiveOrganizeUserList(data){
  return{
    type:Const.GET_ORGANIZE_USER_LIST,
    payload:data
  }
}
export function fetchGetOrganizeUserListAction(id){
  let myInit = {
    method:"GET",
    headers:{token:localStorage.getItem("_at")},
  };
  let url = Const.FETCH_URL.ORGANIZE+"/"+id+"/users";
  return (dispatch =>{
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json =>{
        console.log(json,"组织用户列表");
        if(json.status == 0){
          dispatch(receiveOrganizeUserList(json.result));
        }else{
          dispatch(receiveNotification({message:"获取组织用户列表失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }
      })
  })
}

export function fetchChangeAccountAction(id){
  let body = JSON.stringify({
    orga_uuid:id
  });
  console.log(body);
  let myInit = {
    method:"PUT",
    headers:{token:localStorage.getItem("_at")},
    body:body
  };
  let url = Const.FETCH_URL.TOKEN;
  return (dispatch =>{
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json =>{
        console.log(json,"切换组织");
        if(json.status == 0){
          var exp = new Date();
          exp.setTime(exp.getTime()+1000*60*60*24*7);
          cookie.save('_at',json.result.token,{path:'/',expires: exp});
          localStorage.setItem("_at",json.result.token);
          location.href = '/';
        }else{
          dispatch(receiveNotification({message:"切换失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }
      })
  })
}

function receiveUserList(data){
  return{
    type:Const.GET_USER_LIST,
    payload:data
  }
}

export function fetchGetUserListAction(name){
  let myInit = {
    method:"GET",
    headers:{token:localStorage.getItem("_at")}
  };
  let url = Const.FETCH_URL.USER+"/users/list/"+name;
  return (dispatch =>{
    return fetch(url,myInit)
      .then(response =>response.json())
      .then(json =>{
        console.log(json,"用户列表");
        if(json.status == 0){
          dispatch(receiveUserList(json.result));
        }else{
          dispatch(receiveNotification({message:"获取用户列表失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }
      })
  })
}

export function fetchInviteUser(data){
  let body = JSON.stringify({
    user_uuid:data.user_id
  });
  console.log(data);
  let myInit = {
    method:"POST",
    headers:{token:localStorage.getItem("_at")},
    body:body
  };
  let url = Const.FETCH_URL.ORGANIZE+"/"+data.orga_id+"/users";
  return (dispatch =>{
    return fetch(url,myInit)
      .then(response =>response.json())
      .then(json =>{
        console.log(json,"邀请用户");
        if(json.status == 0){
          dispatch(receiveNotification({message:"邀请成功",level:"success"}));
          dispatch(fetchGetOrganizeUserListAction(data.orga_id));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }else{
          dispatch(receiveNotification({message:"邀请失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }
      })
  })
}

export function fetchChangeUserRoleAction(data){
  console.log(data,"设置用户权限参数");
  let body = JSON.stringify({
    role_uuid:data.role_uuid
  });
  let myInit = {
    method:data.method,
    headers:{token:localStorage.getItem("_at")},
    body:body
  };
  let url = Const.FETCH_URL.ORGANIZE+"/"+data.orga_uuid+"/users/"+data.user_uuid;
  return(dispatch =>{
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json =>{
        console.log(json,"设置用户权限");
        if(json.status == 0){
          dispatch(receiveNotification({message:"设置成功",level:"success"}));
          dispatch(fetchGetOrganizeUserListAction(data.orga_uuid));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }else{
          dispatch(receiveNotification({message:"操作失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }
      })
  })
}

export function fetchChangeOrganizeOwnerAction(data){
  let myInit = {
    method:'PUT',
    headers:{token:localStorage.getItem("_at")},
  };
  let url = Const.FETCH_URL.ORGANIZE+"/"+data.orga_uuid+"/owner/"+data.user_uuid;
  return(dispatch =>{
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json =>{
        console.log(json,"委托组织创建者");
        if(json.status == 0){
          dispatch(receiveNotification({message:"设置成功",level:"success"}));
          dispatch(fetchGetOrganizeUserListAction(data.orga_uuid));
          var exp = new Date();
          exp.setTime(exp.getTime()+1000*60*60*24*7);
          cookie.save('_at',json.result.token,{path:'/',expires: exp});
          localStorage.setItem("_at",json.result.token);
          location.href = '/';
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }else{
          dispatch(receiveNotification({message:"操作失败:"+json.msg,level:"danger"}));
          setTimeout(function(){
            dispatch(clearNotification());
          },3000);
        }
      })
  })
}