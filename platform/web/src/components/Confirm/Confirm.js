
import React, { Component, PropTypes } from 'react';
import {Modal} from "react-bootstrap"
class Confirm extends Component{
  static propTypes = {
    func:React.PropTypes.func
  };
  constructor(props){
    super(props);
    this.state = {
      show:false
    }
  }
  open(){
    this.setState({
      show:true,
    })
  }
  hide(){
    this.setState({
      show:false
    })
  }
  isOk(){
    this.props.func();
    this.setState({
      show:false
    })
  }
  render(){
    return(
      <Modal {...this.props} show={this.state.show}
             onHide={this.hide.bind(this)}
             bsSize="sm" aria-labelledby="contained-modal-title-sm">
        <div className="modal-header">
          <button type="button" onClick={this.hide.bind(this)} className="close" aria-label="Close"><span aria-hidden="true">×</span></button>
          <h4 className="modal-title" id="contained-modal-title-sm">{this.props.title}</h4>
        </div>
        <div className="modal-body">
          <div className="modalItem">
            {this.props.text}
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn btn-default" onClick={this.hide.bind(this)}>取消</button>
          <button className="btn btn-primary" onClick={this.isOk.bind(this)}>确定</button>
        </div>
      </Modal>
    )
  }
}

export default Confirm;
