
import React from 'react';

import Organize from '../../containers/Organize/OrganizeContainer';


export default {
  path: '/organize',

  async action(){
    return <Organize/>
  }
}
