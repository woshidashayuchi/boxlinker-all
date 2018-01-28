
import {
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalTitle,
} from 'react-bootstrap'

import React,{Component} from 'react'

export default class extends Component {
  static propTypes = {
    title: React.PropTypes.string.isRequired,
    body: React.PropTypes.element,
    footer: React.PropTypes.element
  };
  constructor(){
    super();
    this.state = {
      show: false
    };
  }
  open(){
    this.setState({show:true})
  }
  close(){
    this.setState({show:false})
  }
  render(){
    return (
      <Modal onHide={this.close.bind(this)} show={this.state.show} bsStyle={"primary"}>
        <ModalHeader closeButton>
          <ModalTitle>{this.props.title}</ModalTitle>
        </ModalHeader>
        <ModalBody>{this.props.children || this.props.body}</ModalBody>
        <ModalFooter>{this.props.footer}</ModalFooter>
      </Modal>
    )
  }
  render1(){
    return (
      <div class="modal fade">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
              <h4 class="modal-title">{this.props.title}</h4>
            </div>
            <div class="modal-body">
              {this.props.children || this.props.body}
            </div>
            <div class="modal-footer">
              {this.props.footer}
            </div>
          </div>
        </div>
      </div>
    )
  }
}
