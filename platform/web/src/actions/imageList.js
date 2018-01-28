import {
  GET_IMAGE_LIST,
  API_IMAGE_URL,
  FETCH_URL
} from '../constants';

import fetch from 'isomorphic-fetch';

import {isLoadingAction} from './header';

export function receiveImageList(data){
  return {
    type: GET_IMAGE_LIST,
    payload: data
  }
}

export function fetchImageListAction(flag){
  let myInit = {
    method:"GET",
    headers:{token:localStorage.getItem("_at")},
  };
  let url = flag ? FETCH_URL.IMAGE_LIST+"?is_public=true":FETCH_URL.IMAGE_LIST;
  return dispatch =>{
    dispatch(isLoadingAction(true));
    return fetch(url,myInit)
      .then(response => response.json())
      .then(json => {
        console.log('>>>>>images list',json);
        if(json.status==0){
          dispatch(receiveImageList(json.result));
        }else{
          console.error("images list error",json);
        }
        dispatch(isLoadingAction(false));
      })
      .catch (e => {
        dispatch(isLoadingAction(false));
        console.error("images list error" ,e);
      })
  }

}
