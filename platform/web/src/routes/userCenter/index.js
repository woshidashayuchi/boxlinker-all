
import React from 'react';

import User from '../../containers/User/UserCenterContainer';


export default {
  path: '/user',

  async action(){
    return <User/>
  }
}
