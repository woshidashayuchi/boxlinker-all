/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React from 'react';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import s from './ContainerItem.css';
import cx from 'classnames';

var ContainerItem = React.createClass({
  getDefaultProps(){
    return {
      index: 0,
      onClick: function(){},
      classNumber:0
    };
  },
  handleClick(){
    this.props.onClick(this.props.index);
  },
  render:function() {
    var sp1=this.props.children[0].props.children;
    var sp2=this.props.children[1].props.children;
    var sp3=this.props.children[2].props.children;
    var style=this.props.active?[s.csItem,s.csActive]:[s.csItem];
    return (
        <div className={cx(style)} onClick={this.handleClick}>
          <p className={s.csSize} >{sp1}<span>{sp2}</span></p>
          <p className={s.csUnit}>{sp3}</p>
        </div>
    )
  }
})

export default withStyles(s)(ContainerItem);
