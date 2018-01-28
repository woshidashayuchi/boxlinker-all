/**
 * Created by zhangsai on 16/10/10.
 */
import ReviseImage from '../../components/Image/ReviseImage'
import {connect} from 'react-redux'
import makeIsBtnStateSelector from '../../selectors/isBtnStateSelector';
import makeImageDetailSelector from '../../selectors/imageDetailSelector';
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb';
import {
  fetchImageDetailAction
} from '../../actions/imageDetail';
import {
  fetchReviseImageAction
} from '../../actions/reviseImage';

const mapStateToProps = (state) => {
  const selector = makeImageDetailSelector();
  const isBtnStateSelector = makeIsBtnStateSelector();
  return {
    imageDetail:selector(state),
    isBtnState:isBtnStateSelector(state)
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    getImageDetail : (id)=>{
      dispatch(fetchImageDetailAction(id))
    },
    onReviseImage :(data) => {
      dispatch(fetchReviseImageAction(data))
    }
  }
};

const ReviseImageContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(ReviseImage);

export default ReviseImageContainer
