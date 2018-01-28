
import React from 'react'

import {Alert} from 'react-bootstrap';

export default class extends React.Component {
  static propTypes = {
    obj: React.PropTypes.object,
  };
  render(){
    let text = this.props.obj.message;
    return (
      <Alert bsStyle = {this.props.obj.level||"success"} className={!this.props.show?"notification":"notification notificationShow"}>
        {text}
      </Alert>
    )
  }
}
