/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import Root from '../components';

import React, {Component} from 'react'

// Child routes
import dashboard from './dashboard';
import imageCenter from './imageCenter';
import imageForPlatform from './imageForPlatform';
import imageForMy from './imageForMy';
import imageDetail from './imageDetail';
import createImage from './createImage';
import buildingDetail from './building-detail';
import building from './building';
import buildingCreate from './building-create';
import error from './error';
import serviceList from './serviceList';

import addService from './addService';
import choseImage from './choseImage';
import configContainer from './configContainer';
import serviceDetail from './serviceDetail';
import dataVolumeList from './dataVolumeList';
import login from './login';
import signUp from './signUp';
import user from './userCenter';
import reviseImage from './reviseImage';
import organize from './organize';
export default {

  path: '/',

  // keep in mind, routes are evaluated in order
  children: [
    dashboard,
    imageCenter,
    imageForPlatform,
    imageForMy,
    imageDetail,
    createImage,
    reviseImage,
    buildingCreate,
    buildingDetail,
    building,
    serviceList,
    serviceDetail,
    addService,
    dataVolumeList,
    login,
    signUp,
    user,
    choseImage,
    configContainer,
    organize,

    // place new routes before...
    error,
  ],

  async action({ next, render, context }) {
    const component = await next();
    if (component === undefined) return component;
    if (component === true) return component;
    return render(
      <Root context={context}>
        {component}
      </Root>
    );
  },

};
