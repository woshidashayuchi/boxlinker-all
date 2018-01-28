/**
 * Created by zhangsai on 16/10/10.
 */
import CreateImage from '../../components/Image/CreateImage';
import {connect} from 'react-redux';
import makeIsBtnStateSelector from '../../selectors/isBtnStateSelector';
import {
  setBreadcrumbAction,
} from '../../actions/breadcumb';
import {fetchCreateImageAction} from '../../actions/createImage';

const mapStateToProps = (state) => {
  const isBtnStateSelector = makeIsBtnStateSelector();
  return {
    isBtnState:isBtnStateSelector(state),
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    setBreadcrumb:(...arr) => {
      dispatch(setBreadcrumbAction(...arr))
    },
    onCreateImage:(data) =>{
      dispatch(fetchCreateImageAction(data))
    }
  }
};

const CreateImageContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CreateImage);

export default CreateImageContainer
