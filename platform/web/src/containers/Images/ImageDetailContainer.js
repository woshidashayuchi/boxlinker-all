import ImageDetail from "../../components/Image/ImageDetail";

import {connect} from 'react-redux';

import {
  fetchImageDetailAction,
} from '../../actions/imageDetail';
import makeImageDetailSelector from '../../selectors/imageDetailSelector';
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb';
import {
  goToConfigContainer,
} from '../../actions/deployService';
import {
  onDeleteImageAction
} from '../../actions/building';
import {fetchReviseImageAction}
from '../../actions/reviseImage';
import makeIsBtnStateSelector from '../../selectors/isBtnStateSelector';

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
    getImageDetail : (id)=>{
      dispatch(fetchImageDetailAction(id))
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    onDeleteImage:(name,keyList) =>{
      dispatch(onDeleteImageAction(name,keyList))
    },
    goToConfigContainer:(obj) =>{
      dispatch(goToConfigContainer(obj))
    },
    onReviseImage :(data) => {
      dispatch(fetchReviseImageAction(data))
    }
  }
};

const ImageDetailContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(ImageDetail);

export default ImageDetailContainer
