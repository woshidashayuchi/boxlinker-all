
import {createSelector} from 'reselect'

const getBreadcrumbList = (state) => state.breadcrumbList

const makeBreadcrumbSelector = () => {
  return createSelector(
    [getBreadcrumbList],
    (breadcrumbList) => {
      return breadcrumbList
    }
  )
}

export default makeBreadcrumbSelector
