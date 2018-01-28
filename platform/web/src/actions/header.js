
import {IS_LOADING} from '../constants'
import {navigate} from './route';

export function isLoadingAction (flag){
  return {
    type : IS_LOADING,
    payload : flag
  }
}
