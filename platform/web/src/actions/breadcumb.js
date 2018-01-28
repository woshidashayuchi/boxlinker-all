
import {
  BREADCRUMB,
  BREADCRUMB_LIST,
} from '../constants'

export function setBreadcrumbAction(...names){
  return {
    type: BREADCRUMB_LIST,
    payload: names
  }
}

