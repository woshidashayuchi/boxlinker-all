import ChoseImage from '../../components/ChoseImage/ChoseImage';
import {connect} from 'react-redux';
import {
  goToConfigContainer,
} from '../../actions/deployService';
import {fetchImageListAction } from "../../actions/imageList";
import makeGetImageListSelector from '../../selectors/imageListSelector';
import makeGetDeployData from '../../selectors/deployDataSelector';
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb'

const mapStateToProps = (state) => {
  const selectorImage = makeGetImageListSelector();
  const deployData = makeGetDeployData();
  return {
    imageList :selectorImage(state),
    deployData: deployData(state),
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    onImageListLoad : (flag) => {
      dispatch(fetchImageListAction(flag));
    },
    goToConfigContainer:(obj) => {
      dispatch(goToConfigContainer(obj))
    },
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    }
  }
};

const ChoseImageContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(ChoseImage);

export default ChoseImageContainer
