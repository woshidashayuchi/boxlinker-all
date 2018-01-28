import {connect} from 'react-redux'
import BuildingCreate from '../../components/Building/BuildingCreate'
import {
  fetchRepoListAction,
  fetchGithubAuthURLAction,
  fetchBuildingAction
} from '../../actions/building'
import makeGetReposSelector,{makeGetGithubAuthURLSelector} from '../../selectors/BuildingCreateSelector'
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'
import makeIsBtnStateSelector from '../../selectors/isBtnStateSelector';

const mapStateToProps = (state) => {
  const selector = makeGetReposSelector();
  const s1 = makeGetGithubAuthURLSelector();
  const isBtnStateSelector = makeIsBtnStateSelector();
  return {
    repos: selector(state),
    githubAuthURL: s1(state),
    isBtnState:isBtnStateSelector(state),
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onReposLoad: (key,refresh) => {
      dispatch(fetchRepoListAction(key,refresh))
    },
    getGithubAuthURL: () => {
      dispatch(fetchGithubAuthURLAction())
    },
    onBuilding:(data) =>{
      dispatch(fetchBuildingAction(data))
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    }
  }
}

const BuildingCreateContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(BuildingCreate)

export default BuildingCreateContainer

