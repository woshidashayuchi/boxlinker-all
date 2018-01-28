import ImageCenterList from '../../components/Image/ImageCenter';
import {connect} from 'react-redux';
import {
  fetchImageListAction
} from '../../actions/imageList';
import makeGetImageListSelector from '../../selectors/imageListSelector';

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
    }
  }
}

const ImageListContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(ImageCenterList);

export default ImageListContainer
