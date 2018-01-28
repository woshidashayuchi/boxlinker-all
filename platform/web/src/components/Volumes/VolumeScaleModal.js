
import {Modal} from 'react-bootstrap'
import React,{Component} from 'react'
import InputRange from 'react-input-range';

class InputRangesBox extends Component {//input滑块
  static propTypes = {
    value: React.PropTypes.number
  };
  constructor(props) {
    super(props);
    this.state = {
      value: 2
    };
  }
  getValue(){
    return this.state.value
  }
  handleValueChange(component, value) {
    this.setState({
      value: value,
    });
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
    onSave: React.PropTypes.func
  };
  constructor(){
    super();
    this.state = {
      show: false,
      data:{}
    }
  }
  open(item){
    this.setState({
      show:true,
      data:item
    })
  }
  hide(){
    this.setState({show:false})
  }
  save(){
    this.props.onSave(this.state.data.disk_name,String(this.refs.diskSize.getValue()*1024))
  }
  render(){
    return (
      <Modal {...this.props} show={this.state.show} onHide={this.hide.bind(this)}
                             bsSize="sm" aria-labelledby="contained-modal-title-sm">
        <div className="modal-header">
          <button type="button" onClick={this.hide.bind(this)} className="close" aria-label="Close"><span aria-hidden="true">×</span></button>
          <h4 className="modal-title" id="contained-modal-title-sm">扩容</h4>
        </div>
        <div className="modal-body">
          <div className="modalItem dilatationModalItem">
            <label><span>大小</span></label>
            <label>
              <div className="modelInputRange">
                <InputRangesBox ref="diskSize" value={(this.state.data.disk_size/1024<<0)}/>
                <span>充值用户可以创建更大存储卷</span>
              </div>
            </label>
          </div>
          <div className="modalItem modelItemLast dilatationModalItem">
            <label><span> </span></label>
            <label>
              <button className="btn btn-primary" onClick={this.save.bind(this)}>保存</button>
            </label>
          </div>
        </div>
      </Modal>

    )
  }
}


