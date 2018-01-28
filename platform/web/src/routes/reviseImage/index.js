
import React from 'react';

// import CodeBuildList from './CodeBuildList'
import ReviseImageContainer from '../../containers/Images/ReviseImageContainer';
export default {
  path: '/reviseImage/:uuid',
  async action(ctx,params){
    return (
      <ReviseImageContainer uuid = {params.uuid}  />
    )
  }
}
