
import React,{Component} from 'react'
import {DropdownButton,MenuItem} from 'react-bootstrap'

export default class extends Component {
  static propTypes = {
    onSelect: React.PropTypes.func,
    selectedKey: React.PropTypes.any
  };
  constructor(){
    super();
    this.state = {
      title: React.PropTypes.string
    }
  }
  onSelect(eventKey){
    // this.props.onSelect(this.state.data[eventKey]);
    this.setState({title:this.state.data[eventKey]})
  }
  componentDidMount(){
    this.onSelect(this.props.selectedKey)
  }
  render(){
    let data = this.props.data.map((item,i)=>{
      return (
        <MenuItem eventKey={i}>{item}</MenuItem>
      )
    });
    return (
      <DropdownButton title={this.state.title} onSelect={this.onSelect}>
        {data}
      </DropdownButton>
    )
  }
}
