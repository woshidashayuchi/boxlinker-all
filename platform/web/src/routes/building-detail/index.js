
import React from 'react';

import BuildingDetail from '../../containers/Building/BuildingDetailContainer'


export default {
  path: '/building/:id',

  async action(c,params){
    return <BuildingDetail projectId={params.id}/>
  }
}
