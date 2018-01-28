
import React from 'react';
import CreateImageContainer from '../../containers/Images/CreateImageContainer';
export default {
  path: '/createImage',
  async action(){
    return (
      <CreateImageContainer/>
    )
  }
}
