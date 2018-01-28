/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React from 'react';
import ServiceListContainer from '../../containers/Services/ServiceListContainer';

export default {

  path: '/serviceList',

  async action() {
    return <ServiceListContainer/>;
  },

};
