
import React from 'react';

import BuildingCreateContainer from '../../containers/Building/BuildingCreateContainer'


export default {
  path: '/building/create',

  async action(){
    return <BuildingCreateContainer/>
  }
}
