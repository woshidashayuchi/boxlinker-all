
import {Modal,Button} from 'react-bootstrap'
import React,{Component} from 'react'
import InputRange from 'react-input-range';

class InputRangesBox extends Component {//input滑块
  constructor(props) {
    super(props);
    this.state = {
      value: 2
    };
  }
  handleValueChange(component, value) {
    this.setState({
      value: value,
    });
  }
  getValue(){
    return this.state.value;
  }
  render() {
    return (
      <div className="formField">
        <InputRange
          className="formField"
          maxValue={2}
          minValue={1}
          step={1}
          labelPrefix=""
          labelSuffix="G"
          value={this.state.value}
          onChange={this.handleValueChange.bind(this)}
        />
      </div>
    );
  }
}

export default class extends Component {
  static propTypes = {
    onVolumeCreate: React.PropTypes.func,
    isBtnState:React.PropTypes.object
  };
  constructor(){
    super();
    this.state = {
      show: false
    }
  }
  open(){
    this.setState({
      show:true,
      isName:false
    })
  }
  hide(){
    this.setState({show:false})
  }
  createVolume(){
    let data = {
      disk_name: this.refs.disk_name.value,
      disk_size: (this.refs.disk_size.getValue()*1024)+"",
      fs_type: this.refs.fs_type.value
    };
    if (!/^[a-z]{1}[a-z0-9_]{5,}$/.test(data.disk_name)){
      this.setState({
        isName:true
      });
      this.refs.disk_name.focus();
      return false;
    }
    this.props.onVolumeCreate(data);
  }
  changeName(){
    this.setState({
      isName:false
    });
  }
  render(){
    return (
      <Modal {...this.props} show={this.state.show}
                             onHide={this.hide.bind(this)}
                             bsSize="sm" aria-labelledby="contained-modal-title-sm">
        <div className="modal-header">
          <button type="button" onClick={this.hide.bind(this)} className="close" aria-label="Close"><span aria-hidden="true">×</span></button>
          <h4 className="modal-title" id="contained-modal-title-sm">创建存储卷</h4>
        </div>
        <div className="modal-body">
          <div className="modalItem">
            <label><span>名称</span></label>
            <label><input onChange = {this.changeName.bind(this)} className="form-control form-control-sm" type="input" placeholder="请输入名称" ref="disk_name"/></label>
          </div>
          <div className="modalItem">
            <label><span>大小</span></label>
            <label>
              <div className="modelInputRange">
                <InputRangesBox ref="disk_size"/>
                <span>充值用户可以创建更大存储卷</span>
              </div>
            </label>
          </div>
          <div className="modalItem">
            <label><span>格式</span></label>
            <label>
              <select ref="fs_type" className="form-control">
                <option value="xfs">xfs</option>
                <option value="ext4">ext4</option>
              </select>
            </label>
          </div>
          <div className={this.state.isName?"volumeTip volumeTipShow":"volumeTip"}>数据卷名称格式不正确</div>
          <div className="modalItem modelItemLast">
            <label><span> </span></label>
            <label>
              <Button bsStyle="primary"
                      disabled={!this.props.isBtnState.volume}
                      onClick={this.createVolume.bind(this)}>创建存储卷</Button>
            </label>
          </div>
        </div>
      </Modal>
    )
  }
}
