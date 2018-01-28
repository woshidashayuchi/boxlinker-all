import ImageForPlatform from '../../components/Image/ImageForPlatform'
import {connect} from 'react-redux'
import {
  fetchImageListAction
} from '../../actions/imageList'
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'
import {
  goToConfigContainer,
} from '../../actions/deployService';
import makeGetImageListSelector from '../../selectors/imageListSelector'

const mapStateToProps = (state) => {
  const selector = makeGetImageListSelector();
  return {
    imageList: selector(state)
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    onImageList : (flag)=>{
      dispatch(fetchImageListAction(flag))
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    goToConfigContainer:(obj) => {
      dispatch(goToConfigContainer(obj))
    },
  }
}

const ImageForPlatformContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(ImageForPlatform);

export default ImageForPlatformContainer
