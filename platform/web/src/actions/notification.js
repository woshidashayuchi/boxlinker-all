
import {WS_MSG_TYPES,WS_URL,RECEIVE_NOTIFICATION,CLEAR_NOTIFICATION,RECEIVE_SERVICE_STATE} from '../constants'

import {fetchServiceDetailAction} from './serviceDetail'

import io from 'socket.io-client'

export const receiveNotification = (data) => {
  return {
    type: RECEIVE_NOTIFICATION,
    payload: data,
  }
}

export const clearNotification = ()=>{
  return {
    type: CLEAR_NOTIFICATION
  }
}

export const init = (username) => {
  const socket = io.connect(WS_URL)

  socket.emit('init',{namespace:username})

  return dispatch => {

    socket.on('notification',(message)=>{
      console.log(message,"oooooo")
      dispatch(receiveNotification(message));
      switch(message.type){
        case "service":
              dispatch(fetchServiceDetailAction(message.service_name));
              break;
        default:
          break;
      }

      setTimeout(function(){
        dispatch(clearNotification())
      },5000)
    })
  }
}

export const emit = (type,payload) =>{
  const socket = io.connect(WS_URL)
  return dispatch => {
    socket.emit(type, payload);
  }
}

