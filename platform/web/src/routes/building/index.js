
import React from 'react';

// import CodeBuildList from './CodeBuildList'
import Building from '../../containers/Building/BuildingContainer';
export default {
  path: '/building',
  async action(){
    return (
      <Building/>
    )
  }
}
