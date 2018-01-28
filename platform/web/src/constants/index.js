export const TOGGLE_SIDEBAR = 'TOGGLE_SIDEBAR';

export const SIDEBAR_STATUS = {
  OPEN:true,
  CLOSE:false
};
export const SIDEBAR_ACTIVE = 'SIDEBAR_ACTIVE';
export const SET_RUNTIME_VARIABLE = 'SET_RUNTIME_VARIABLE';
export const RECEIVE_VOLUMES_LIST = 'RECEIVE_VOLUMES_LIST';
export const CLEAR_VOLUMES_LIST = 'CLEAR_VOLUMES_LIST';
// deploy service
export const DEPLOY_SVC_IMAGE = "DEPLOY_SVC_IMAGE";
export const DEPLOY_SVC_CONTAINER = 'DEPLOY_SVC_CONTAINER';
export const DEPLOY_SVC_SENIOR = 'DEPLOY_SVC_SENIOR';
export const CLEAR_DEPLOY_DATA = 'CLEAR_DEPLOY_DATA';
// service
export const GET_ALL_SERVICES = 'GET_ALL_SERVICES';
export const CLEAR_SERVICE_LIST = 'CLEAR_SERVICE_LIST';
export const REFRESH_LIST = 'REFRESH_LIST';
export const GET_SERVICE_DETAIL = 'GET_SERVICE_DETAIL';
export const ADD_PORT = 'ADD_PORT';
export const DEL_PORT = 'DEL_PORT';
export const ADD_SAVE = 'ADD_SAVE';
export const DEL_SAVE = 'DEL_SAVE';
export const ADD_ENV = 'ADD_ENV';
export const DEL_ENV = 'DEL_ENV';
export const CLEAR_SERVICE_DETAIL = 'CLEAR_SERVICE_DETAIL';
export const GET_POD_LIST = 'GET_POD_LIST';
export const SERVICE_STATE = {
  Running:'running',
  Pending:'pending',
  Stopping:'stopping'
};
export const GET_MONITOR_DATA = 'GET_MONITOR_DATA';
export const GET_DASHBOARD = 'GET_DASHBOARD';
//image
export const GET_IMAGE_LIST = 'GET_IMAGE_LIST';
export const CLEAR_IMAGE_LIST = 'CLEAR_IMAGE_LIST';
export const GET_IMAGE_DETAIL = 'GET_IMAGE_DETELE';
export const API_VOLUMES_URL = "http://storage.boxlinker.com/api/v1.0/storage/volumes";
export const API_SERVICE_URL = "http://api.boxlinker.com/api/v1/application/service";
export const API_DELETE_SERVICE_URL = "http://api.boxlinker.com/api/v1/application/remove/service";
export const API_IMAGE_URL = "http://auth.boxlinker.com/registry/v2";
// building
export const GET_REPO_LIST = "GET_REPO_LIST";
export const IS_LOADING = "IS_LOADING";
export const GET_GITHUB_AUTH_URL = "GET_GITHUB_AUTH_URL";
export const GET_CODING_AUTH_URL = 'GET_CODING_AUTH_URL';
export const GET_BUILDING_IMAGE_LIST = "GET_BUILDING_IMAGE_LIST";
export const GET_BUILDING_DETAIL = 'GET_BUILDING_DETAIL';
// userinfo
export const RECEIVE_USER_INFO = "RECEIVE_USER_INFO";
export const GET_USER_LIST = 'GET_USER_LIST';
//user
export const GET_BALANCE = 'GET_BALANCE';
// organize
export const GET_ORGANIZE_LIST = 'GET_ORGANIZE_LIST';
export const GET_ORGANIZE_DETAIL = 'GET_ORGANIZE_DETAIL';
export const GET_ORGANIZE_USER_LIST = 'GET_ORGANIZE_USER_LIST';
// breadcrumb
export const BREADCRUMB_LIST = "BREADCRUMB_LIST";
export const BREADCRUMB = {
  CONSOLE:{
    title:'控制台',
    link:'/'
  },
  CHOSE_IMAGE:{
    title:"选择镜像",
    link:'/choseImage'
  },
  CONFIG_CONTAINER:{
    title:"容器配置",
    link:'/configContainer'
  },
  ADD_SERVICE:{
    title:'新建服务',
    link:'javascript:;'
  },
  NEW_SERVICE:{
    title:'新建服务',
    link:'/addService'
  },
  SERVICE_LIST:{
    title:'服务列表',
    link:'/serviceList'
  },
  SERVICE_DETAIL:{
    title:'服务详情',
    link:'/serviceList'
  },
  VOLUMES:{
    title:'存储卷',
    link:'/volumes'
  },
  IMAGES_MY:{
    title:'我的镜像',
    link:'/imageForMy'
  },
  IMAGES_BOX_LINKER:{
    title:'平台镜像',
    link:'/imageForPlatform'
  },
  BUILD_IMAGE:{
    title:'构建镜像',
    link:'/building'
  },
  CREATE_IMAGE:{
    title:'新建镜像',
    link:'createImage'
  },
  BUILD_CREATE:{
    title:'代码构建',
    link:'/create'
  },
  IMAGE_DETAIL:{
    title:'镜像详情',
    link:'/imageDetail'
  },
  USER_CONTAINER:{
    title:'个人中心',
    link:'/user'
  },
  ORGANIZE:{
    title:'组织中心',
    link:'/organize'
  }
};

// logs
export const RECEIVE_LOG = "RECEIVE_LOG"
export const STOP_RECEIVE_LOG = "STOP_RECEIVE_LOG"
export const OPEN_LOG_XHR = "OPEN_LOG_XHR"
export const ABORT_LOG_XHR = "ABORT_LOG_XHR"


// websocket
export const WS_MSG_TYPES = ["service"].reduce((accum, msg) => {
  accum[ msg ] = msg
  return accum
}, {})
export const WS_URL = "http://boxlinker.com:30003"
export const RECEIVE_NOTIFICATION = "RECEIVE_NOTIFICATION"
export const CLEAR_NOTIFICATION = "CLEAR_NOTIFICATION";
export const RECEIVE_SERVICE_STATE = "RECEIVE_SERVICE_STATE";


let URL = true;

if (URL){
  URL = 'http://192.168.1.6:8080'
}else {
  URL = 'http://auth.boxlinker.com'
}

export const FETCH_URL = {
  REPOS: URL+'/oauth/githubrepo',
  GITHUB_AUTH: URL+'/oauth/oauthurl',
  USER_INFO: URL+'/user/userinfo',
  REVISE_PASSWORD:URL+'/user/password',
  BUILDING:URL+'/oauth/githubbuild',
  USER:URL+'/api/v1.0/usercenter',
  IMAGE_LIST:URL+'/registry/image_repository',
  USER_INFO_INTERNAL: 'http://registry-api:8080/user/userinfo',
  LOGS: 'http://logs.boxlinker.com/api/v1.0/logs/polling/labels',
  SVC_ENDPOINTS: function(name) {
    return `http://ci-api.boxlinker.com/api/v1/endpoints/${name}`;
  },
  IMAGE:URL + '/registry/image_repository',
  BUILDING_REVISE:URL+'/api/v1.0/repository/repositorybuilds',
  GET_SERVICE_MONITOR: 'http://monitor.boxlinker.com/api/v1/model/namespaces',
  DASHBOARD:'http://controller.boxlinker.com/api/v1/broad',

  //new
  ORGANIZE:URL + '/api/v1.0/usercenter/orgs',
  TOKEN:URL + '/api/v1.0/usercenter/tokens',
  AUTH_URL:URL + '/api/v2.0/oauths/oauthurl'

};
// endpoints
export const RECEIVE_ENDPOINTS = 'RECEIVE_ENDPOINTS';

export const INPUT_TIP = {
  service :{
    Null:"服务名称不能为空",
    Format:"必须为小写字母数字下划线组合,开头必须为字母"
  },
  image :{
    Null:"镜像名称不能为空",
    Format:"必须为小写字母数字下划线组合,开头必须为字母"
  },
  port:{
    Null:"端口不能为空",
    Format:"端口格式不正确",
    Repeat:"端口不能重复"
  },
  volumes:{
    Null:"容器路径不能为空",
    Format:"必须以/开头,后可加字母数字下划线",
    Repeat:"数据卷名称不能重复"
  },
  env:{
    Null:"环境变量值不能为空",
    Format:"环境变量只能为字母数字中划线,并以字母开头",
    Repeat:"环境变量键值不能重复"
  }

};

export const CPU = [
    {x:1,m:"50M"},
    // {x:2,m:"256M"},
    // {x:4,m:"512M"},
    // {x:8,m:"1024M"},
    // {x:16,m:"2048M"}

];

export const IS_BTN_STATE = {
  deploy:'IS_DEPLOY',
  building:'IS_BUILDING',
  createVolume:'IS_CREATE_VOLUME',
  autoStateUp:'IS_AUTO_STATE_UP',
  reviseBuilding:"REVISE_BUILDING",
  port:'IS_PORT',
  storage:'STORAGE',
  env:'ENV',
  command:'COMMAND',
  pods:'PODS',
  setOrg:'SET_ORG'
};




