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
import s from './HeadLine.css';

var HeadLine = React.createClass({
  getDefaultProps:function(){
    return{
      title:"选择镜像",
      titleEnglish:"SELECT MIRROR",
      titleInfo:"这里里汇聚了构建产生的所有容器云镜像",
    }
  },
  render:function() {
    return (
      <div className={s.hlBox}>
        <h1 className={s.hlHd}>
          <span className={s.hlFirstTitle}>{this.props.title}</span>
          <span className={s.hlSecondTitle}>{this.props.titleEnglish}</span>
        </h1>
        <p className={s.hlPresent}>{this.props.titleInfo}</p>

      </div>
    );
  }
})

export default withStyles(s)(HeadLine);
