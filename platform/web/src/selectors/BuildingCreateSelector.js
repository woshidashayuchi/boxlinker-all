
import {createSelector} from 'reselect'

const getRepos = (state) => state.repos

const authUrl = (state) => state.authUrl;

const makeGetReposSelector = () => {
  return createSelector(
    [getRepos],
    (repos) => {
      return repos
    }
  )
}

export const makeGetAuthURLSelector = () => {
  return createSelector(
    [authUrl],
    (url) => {
      return url;
    }
  )
}

export default makeGetReposSelector
