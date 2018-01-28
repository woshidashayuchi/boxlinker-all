// import fetch from 'isomorphic-fetch'
import {TOGGLE_SIDEBAR,SIDEBAR_ACTIVE} from '../constants'

export function toggleSidebarAction(status){
  return {
    type: TOGGLE_SIDEBAR,
    status
  }
}


export function onChangeSidebarActiveAction(url){
  return {
    type:SIDEBAR_ACTIVE,
    payload:url
  }
}
