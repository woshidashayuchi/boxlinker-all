import ImageForMy from '../../components/Image/ImageForMy'
import {connect} from 'react-redux'
import {
  fetchImageListAction
} from '../../actions/imageList'
import makeGetImageListSelector from '../../selectors/imageListSelector'
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'
import {
  goToConfigContainer,
} from '../../actions/deployService';
import {
  onDeleteImageAction
} from '../../actions/building';


const mapStateToProps = (state) => {
  const selector = makeGetImageListSelector();
  return {
    imageList: selector(state)
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    onImageList : ()=>{
      dispatch(fetchImageListAction())
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    goToConfigContainer:(obj) =>{
      dispatch(goToConfigContainer(obj))
    },
    onDeleteImage:(name,keyList) =>{
      dispatch(onDeleteImageAction(name,keyList))
    }
  }
};

const ImageForMyContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(ImageForMy);

export default ImageForMyContainer
