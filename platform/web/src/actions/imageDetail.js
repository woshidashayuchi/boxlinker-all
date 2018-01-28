import * as Const from '../constants'

import fetch from 'isomorphic-fetch';
import {isLoadingAction} from './header'

function receiveImageDetail (data){
  return {
    type : Const.GET_IMAGE_DETAIL,
    payload : data
  }
}

export function fetchImageDetailAction(id){
  let myInit = {
      method : "GET",
      headers:{token:localStorage.getItem("_at")},
    },
    url = Const.FETCH_URL.IMAGE+"?only=true&repository_id="+id;
  return dispatch => {
    dispatch(isLoadingAction(true));
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json => {
        console.log(json);
        if(json.status == 0){
          dispatch(receiveImageDetail(json.result));
        }else{
          console.error(json);
        }
        dispatch(isLoadingAction(false));
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        console.error("imageDetail is error",e);
      })
  }
}
