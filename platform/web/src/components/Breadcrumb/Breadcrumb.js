
import React, { Component } from 'react';
import Link from '../Link'
import s from './Breadcrumb.css';
import withStyles from 'isomorphic-style-loader/lib/withStyles';

class Breadcrumb extends Component {
  static propTypes = {
    breadcrumbList: React.PropTypes.array
  };
  render () {
    // console.log('breadcrumbList>>',this.props.breadcrumbList);
    let list = this.props.breadcrumbList,
      len = list.length;
    if (len <= 0) return <ol className={s.root}></ol>;
    if (len == 1) return <li>
      <a className={s.selected}>{list[0].title}</a>
    </li>;
    let data = [];
    for(let i=0;i<len-1;i++){
      let item = list[i];
      data.push (
        <li key={i}>
          <Link to={item.link} >{i==0?<span className="icon-console" style={{marginRight:"5px"}}> </span>:""}{item.title}</Link>
        </li>
      )
      data.push(<li key={i+"1"} className={s.split}>/</li>)
    }
    data.push((
      <li key={len-1}>
        <a className={s.selected}>{list[len-1].title}</a>
      </li>
    ))
    return (
      <ol className={s.root}>
        {data}
      </ol>
    )
  }
}

export default withStyles(s)(Breadcrumb)
