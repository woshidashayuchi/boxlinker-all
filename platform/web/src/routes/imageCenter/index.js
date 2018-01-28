
import React from 'react';

import ImageListContainer from '../../containers/Images/ImageCenterContainer'


export default {
  path: '/imageCenter',

  async action(){
    return <ImageListContainer/>
  }
}
