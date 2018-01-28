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
import s from './ServiceStep.css';
import cx from 'classnames';


var ServiceStep = React.createClass({
  getDefaultProps:function(){
    return {
      dataActive:"first"
    }
  },
  render:function(){
    var activeFirst=[s.ssHdBox,s.ssHdFirst];
    var activeSecond=[s.ssHdBox,s.ssHdSecond];
    var activeThird=[s.ssHdBox,s.ssHdThird];
    switch(this.props.dataActive){
      case "first":activeFirst=activeFirst.concat([s.ssActive]);
            break
      case "second":activeSecond=activeSecond.concat([s.ssActive]);
            break
      case "third":activeThird=activeThird.concat([s.ssActive]);
            break
    }

    return (
      <div className={s.ssHd}>
        <div className={cx(activeFirst)}>
          <div className={cx(s.ssHdIcon,"icon-mirrorceer")}></div>
          <div className={s.ssHdName}>
            <p><span>1</span>镜像来源</p>
            <p>MIRRIR SOURCE</p>
          </div>
          <div className={s.ssActiveIcon}></div>
        </div>
        <div className={cx(activeSecond)}>
          <div className={cx(s.ssHdIcon,"icon-containerconfig")}></div>
          <div className={s.ssHdName}>
            <p><span>2</span>容器配置</p>
            <p>CONFIGURATION</p>
          </div>
          <div className={s.ssActiveIcon}></div>
        </div>
        <div className={cx(activeThird)}>
          <div className={cx(s.ssHdIcon,"icon-advancedset")}></div>
          <div className={s.ssHdName}>
            <p><span>3</span>高级设置</p>
            <p>ADVANCED SETUP</p>
          </div>
          <div className={s.ssActiveIcon}></div>
        </div>
      </div>)
  }
})

export default withStyles(s)(ServiceStep);
