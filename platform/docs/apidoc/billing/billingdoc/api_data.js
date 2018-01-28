define({ "api": [  {    "type": "put",    "url": "/api/v1.0/billing/resources",    "title": "1.5 资源核对",    "name": "check_resources_record",    "group": "1_resources",    "version": "1.0.0",    "description": "<p>核对需要计费的资源信息与资源提供端信息是否匹配</p>",    "permission": [      {        "name": "organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    add_list: [\n        {\n            \"resource_uuid\": \"string\",\n            \"resource_name\": \"string\",\n            \"resource_type\": \"string\",\n            \"resource_conf\": \"string\",\n            \"resource_status\": \"string\",\n            \"team_uuid\": \"string\",\n            \"project_uuid\": \"string\",\n            \"user_uuid\": \"string\"\n        }\n    ],\n    delete_list: [\n        {\n            \"resource_uuid\": \"string\",\n            \"resource_name\": \"string\",\n            \"resource_type\": \"string\",\n            \"resource_conf\": \"string\",\n            \"resource_status\": \"string\",\n            \"team_uuid\": \"string\",\n            \"project_uuid\": \"string\",\n            \"user_uuid\": \"string\"\n        }\n    ],\n    update_list: [\n        {\n            \"resource_uuid\": \"string\",\n            \"resource_name\": \"string\",\n            \"resource_type\": \"string\",\n            \"resource_conf\": \"string\",\n            \"resource_status\": \"string\",\n            \"team_uuid\": \"string\",\n            \"project_uuid\": \"string\",\n            \"user_uuid\": \"string\"\n        }\n    ]\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "1_resources",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {}\n}",          "type": "json"        }      ]    }  },  {    "type": "post",    "url": "/api/v1.0/billing/resources",    "title": "1.1 资源创建",    "name": "create_resources_record",    "group": "1_resources",    "version": "1.0.0",    "description": "<p>创建需要计费的资源信息</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    \"resource_uuid\": \"string\",\n    \"resource_name\": \"string\",\n    \"resource_type\": \"string\",\n    \"resource_conf\": \"string\",\n    \"resource_status\": \"string\"\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "1_resources",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"resource_uuid\": \"string\",\n        \"resource_name\": \"string\",\n        \"resource_type\": \"string\",\n        \"resource_conf\": \"string\",\n        \"resource_status\": \"string\",\n        \"team_uuid\": \"string\",\n        \"project_uuid\": \"string\",\n        \"user_uuid\": \"string\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "delete",    "url": "/api/v1.0/billing/resources/<resource_uuid>",    "title": "1.4 资源删除",    "name": "delete_resources_record",    "group": "1_resources",    "version": "1.0.0",    "description": "<p>删除需要计费的资源信息</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "1_resources",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {}\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/resources?page_size=<int>&page_num=<int>",    "title": "1.2 资源列表",    "name": "get_resources_record",    "group": "1_resources",    "version": "1.0.0",    "description": "<p>获取需要计费的资源列表</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "1_resources",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"count\": int,\n        \"resources_list\": [\n            {\n                \"resource_uuid\": \"string\",\n                \"resource_name\": \"string\",\n                \"resource_type\": \"string\",\n                \"resource_conf\": \"string\",\n                \"resource_status\": \"string\",\n                \"team_uuid\": \"string\",\n                \"project_uuid\": \"string\",\n                \"user_uuid\": \"string\",\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n            },\n            {\n                \"resource_uuid\": \"string\",\n                \"resource_name\": \"string\",\n                \"resource_type\": \"string\",\n                \"resource_conf\": \"string\",\n                \"resource_status\": \"string\",\n                \"team_uuid\": \"string\",\n                \"project_uuid\": \"string\",\n                \"user_uuid\": \"string\",\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n            },\n            {\n                \"resource_uuid\": \"string\",\n                \"resource_name\": \"string\",\n                \"resource_type\": \"string\",\n                \"resource_conf\": \"string\",\n                \"resource_status\": \"string\",\n                \"team_uuid\": \"string\",\n                \"project_uuid\": \"string\",\n                \"user_uuid\": \"string\",\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n            }\n        ]\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "put",    "url": "/api/v1.0/billing/resources/<resource_uuid>",    "title": "1.3 资源更新",    "name": "update_resources_record",    "group": "1_resources",    "version": "1.0.0",    "description": "<p>更新需要计费的资源信息</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    \"resource_conf\": \"string\",\n    \"resource_status\": \"string\",\n    \"team_uuid\": \"string\",\n    \"project_uuid\": \"string\",\n    \"user_uuid\": \"string\"\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "1_resources",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"resource_uuid\": \"string\",\n        \"resource_conf\": \"string\",\n        \"resource_status\": \"string\",\n        \"team_uuid\": \"string\",\n        \"project_uuid\": \"string\",\n        \"user_uuid\": \"string\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "post",    "url": "/api/v1.0/billing/vouchers/<voucher_uuid>",    "title": "2.4 礼券激活",    "name": "active_vouchers",    "group": "2_vouchers",    "version": "1.0.0",    "description": "<p>用户激活领用到的礼券</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "2_vouchers",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"vouchers_uuid\": \"string\",\n        \"team_uuid\": \"string\",\n        \"project_uuid\": \"string\",\n        \"user_uuid\": \"string\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "post",    "url": "/api/v1.0/billing/vouchers",    "title": "2.1 礼券生成",    "name": "create_vouchers",    "group": "2_vouchers",    "version": "1.0.0",    "description": "<p>系统管理员生成礼券</p>",    "permission": [      {        "name": "admin"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    \"denomination\": int,\n    \"invalid_time\": \"epoch_seconds\"\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "2_vouchers",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"voucher_uuid\": \"string\",\n        \"denomination\": int,\n        \"invalid_time\": \"YYYY-MM-DD HH:MM:SS\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "put",    "url": "/api/v1.0/billing/vouchers/<voucher_uuid>",    "title": "2.2 礼券分发",    "name": "distribute_vouchers",    "group": "2_vouchers",    "version": "1.0.0",    "description": "<p>系统管理员分发礼券给用户</p>",    "permission": [      {        "name": "admin"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    \"accepter\": \"string\"\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "2_vouchers",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"voucher_uuid\": \"string\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/vouchers?voucher_accept=<true>&page_size=<int>&page_num=<int>",    "title": "2.3 礼券查询",    "name": "get_accept_vouchers",    "group": "2_vouchers",    "version": "1.0.0",    "description": "<p>用户查询收到的礼券列表</p>",    "permission": [      {        "name": "admin"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "2_vouchers",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"count\": int,\n        \"vouchers_list\": [\n            {\n                \"vouchers_uuid\": \"string\",\n                \"denomination\": int,\n                \"status\": \"string\",\n                \"invalid_time\": \"YYYY-MM-DD HH:MM:SS\",\n            },\n            {\n                \"vouchers_uuid\": \"string\",\n                \"denomination\": int,\n                \"status\": \"string\",\n                \"invalid_time\": \"YYYY-MM-DD HH:MM:SS\",\n            },\n            {\n                \"vouchers_uuid\": \"string\",\n                \"denomination\": int,\n                \"status\": \"string\",\n                \"invalid_time\": \"YYYY-MM-DD HH:MM:SS\",\n            }\n        ]\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/vouchers?start_time=<epoch_seconds>&end_time=<epoch_seconds>&page_size=<int>&page_num=<int>",    "title": "2.5 礼券列表",    "name": "get_vouchers",    "group": "2_vouchers",    "version": "1.0.0",    "description": "<p>查询用户已激活的礼劵列表</p>",    "permission": [      {        "name": "user and organization and admin"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "2_vouchers",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"count\": int,\n        \"vouchers_list\": [\n            {\n                \"vouchers_uuid\": \"string\",\n                \"denomination\": int,\n                \"balance\": float,\n                \"status\": \"string\",\n                \"accepter\": \"string\",\n                \"activator\": \"string\",\n                \"active_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"invalid_time\": \"YYYY-MM-DD HH:MM:SS\",\n            },\n            {\n                \"vouchers_uuid\": \"string\",\n                \"denomination\": int,\n                \"balance\": float,\n                \"status\": \"string\",\n                \"accepter\": \"string\",\n                \"activator\": \"string\",\n                \"active_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"invalid_time\": \"YYYY-MM-DD HH:MM:SS\",\n            },\n            {\n                \"vouchers_uuid\": \"string\",\n                \"denomination\": int,\n                \"balance\": float,\n                \"status\": \"string\",\n                \"accepter\": \"string\",\n                \"activator\": \"string\",\n                \"active_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"invalid_time\": \"YYYY-MM-DD HH:MM:SS\",\n            }\n        ]\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "post",    "url": "/api/v1.0/billing/orders",    "title": "3.1 订单创建",    "name": "create_orders",    "group": "3_orders",    "version": "1.0.0",    "description": "<p>创建订单信息</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    \"resource_uuid\": \"string\",\n    \"cost\": float,\n    \"status\": \"string\"\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "3_orders",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"order_uuid\": \"string\",\n        \"resource_uuid\": \"string\",\n        \"cost\": float,\n        \"status\": \"string\",\n        \"team_uuid\": \"string\",\n        \"project_uuid\": \"string\",\n        \"user_uuid\": \"string\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/orders?start_time=<epoch_seconds>&end_time=<epoch_seconds>&page_size=<int>&page_num=<int>",    "title": "3.3 订单列表",    "name": "get_orders",    "group": "3_orders",    "version": "1.0.0",    "description": "<p>查询订单信息</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "3_orders",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"count\": int,\n        \"orders_list\": [\n            {\n                \"order_uuid\": \"string\",\n                \"resource_uuid\": \"string\",\n                \"cost\": float,\n                \"status\": \"string\",\n                \"team_uuid\": \"string\",\n                \"project_uuid\": \"string\",\n                \"user_uuid\": \"string\",\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n            },\n                \"order_uuid\": \"string\",\n                \"resource_uuid\": \"string\",\n                \"cost\": float,\n                \"status\": \"string\",\n                \"team_uuid\": \"string\",\n                \"project_uuid\": \"string\",\n                \"user_uuid\": \"string\",\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n            {\n            },\n            {\n                \"order_uuid\": \"string\",\n                \"resource_uuid\": \"string\",\n                \"cost\": float,\n                \"status\": \"string\",\n                \"team_uuid\": \"string\",\n                \"project_uuid\": \"string\",\n                \"user_uuid\": \"string\",\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n            }\n        ]\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "put",    "url": "/api/v1.0/billing/orders/<order_uuid>",    "title": "3.2 订单更新",    "name": "update_orders",    "group": "3_orders",    "version": "1.0.0",    "description": "<p>更新订单信息</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    \"cost\": float,\n    \"status\": \"string\"\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "3_orders",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"order_uuid\": \"string\",\n        \"cost\": float,\n        \"status\": \"string\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "post",    "url": "/api/v1.0/billing/limits",    "title": "4.1 限额检查",    "name": "limits_check",    "group": "4_limits",    "version": "1.0.0",    "description": "<p>检查限额值</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    \"resource_type\": \"string\",\n    \"cost\": float\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "4_limits",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"team_uuid\": \"string\",\n        \"resource_type\": \"string\",\n        \"balance_check\": 0/1,\n        \"limit_check\": 0/1\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/limits?page_size=<int>&page_num=<int>",    "title": "4.2 限额列表",    "name": "limits_list",    "group": "4_limits",    "version": "1.0.0",    "description": "<p>系统管理员查询限额列表</p>",    "permission": [      {        "name": "system admin"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "4_limits",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"count\": int,\n        \"limits_list\": [\n            {\n                \"team_level\": int,\n                \"teams\": int,\n                \"teamusers\": int,\n                \"projects\": int,\n                \"projectusers\": int,\n                \"roles\": int,\n                \"images\": int,\n                \"services\": int,\n                \"volumes\": int,\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n            },\n            {\n                \"team_level\": int,\n                \"teams\": int,\n                \"teamusers\": int,\n                \"projects\": int,\n                \"projectusers\": int,\n                \"roles\": int,\n                \"images\": int,\n                \"services\": int,\n                \"volumes\": int,\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n            },\n            {\n                \"team_level\": int,\n                \"teams\": int,\n                \"teamusers\": int,\n                \"projects\": int,\n                \"projectusers\": int,\n                \"roles\": int,\n                \"images\": int,\n                \"services\": int,\n                \"volumes\": int,\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n                \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n            }\n        ]\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "put",    "url": "/api/v1.0/billing/limits",    "title": "4.3 限额更新",    "name": "limits_update",    "group": "4_limits",    "version": "1.0.0",    "description": "<p>系统管理员更新限额信息</p>",    "permission": [      {        "name": "system admin"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    \"team_level\": \"string\",\n    \"resource_type\": \"string\",\n    \"limit\": int\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "4_limits",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"team_level\": int,\n        \"resource_type\": \"string\",\n        \"limit\": int\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/levels",    "title": "5.1 等级信息",    "name": "get_levels",    "group": "5_levels",    "version": "1.0.0",    "description": "<p>查询等级信息</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "5_levels",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"team_uuid\": \"string\",\n        \"level\": int,\n        \"experience\": int,\n        \"up_required\": int,\n        \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n        \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/balances?balance_check=<true>",    "title": "6.2 余额检查",    "name": "check_balances",    "group": "6_balances",    "version": "1.0.0",    "description": "<p>查询余额小于零的组织并进行资源回收</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "6_balances",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"teams_list\": [\n            {\n                \"team_uuid\": \"string\",\n                \"balance\": float\n            },\n            {\n                \"team_uuid\": \"string\",\n                \"balance\": float\n            },\n            {\n                \"team_uuid\": \"string\",\n                \"balance\": float\n            }\n        ]\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/balances",    "title": "6.1 余额信息",    "name": "get_balances",    "group": "6_balances",    "version": "1.0.0",    "description": "<p>查询余额信息</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "6_balances",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"team_uuid\": \"string\",\n        \"balance\": float,\n        \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "post",    "url": "/api/v1.0/billing/costs",    "title": "7.1 费用信息",    "name": "get_resource_cost",    "group": "7_costs",    "version": "1.0.0",    "description": "<p>计算资源费用</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    \"resource_type\": \"string\",\n    \"resource_conf\": \"string\",\n    \"resource_status\": \"string\",\n    \"hours\": int\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "7_costs",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"resource_type\": \"string\",\n        \"resource_conf\": \"string\",\n        \"resource_status\": \"string\",\n        \"hours\": int,\n        \"resource_cost\": float\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "post",    "url": "/api/v1.0/billing/recharges",    "title": "8.1 用户充值",    "name": "create_recharge_records",    "group": "8_recharges",    "version": "1.0.0",    "description": "<p>用户执行充值</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          },          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "body",            "description": ""          }        ]      },      "examples": [        {          "title": "body",          "content": "{\n    \"recharge_type\": \"zhifubao/weixin\",\n    \"recharge_amount\": int\n}",          "type": "json"        }      ]    },    "filename": "build/apidoc.py",    "groupTitle": "8_recharges",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"recharge_uuid\": int,\n        \"recharge_type\": \"string\",\n        \"recharge_amount\": int,\n        \"user_name\": \"string\",\n        \"qr_code\": \"url\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/recharges/<recharge_uuid>",    "title": "8.2 充值查询",    "name": "get_recharge_info_record",    "group": "8_recharges",    "version": "1.0.0",    "description": "<p>查询充值结果</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "8_recharges",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"recharge_uuid\": int,\n        \"recharge_amount\": int,\n        \"recharge_type\": \"string\",\n        \"team_uuid\": \"string\",\n        \"user_name\": \"string\",\n        \"create_time\": \"YYYY-MM-DD HH:MM:SS\"\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/recharges?start_time=<epoch_seconds>&end_time=<epoch_seconds>&page_size=<int>&page_num=<int>",    "title": "8.3 充值记录",    "name": "get_recharge_records",    "group": "8_recharges",    "version": "1.0.0",    "description": "<p>查询充值记录</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "8_recharges",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"count\": int,\n        \"recharge_list\": [\n            {\n                \"team_uuid\": \"string\",\n                \"recharge_uuid\": \"string\",\n                \"recharge_amount\": int,\n                \"recharge_type\": \"string\",\n                \"user_name\": \"string\",\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\"\n            },\n            {\n                \"team_uuid\": \"string\",\n                \"recharge_uuid\": \"string\",\n                \"recharge_amount\": int,\n                \"recharge_type\": \"string\",\n                \"user_name\": \"string\",\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\"\n            },\n            {\n                \"team_uuid\": \"string\",\n                \"recharge_uuid\": \"string\",\n                \"recharge_amount\": int,\n                \"recharge_type\": \"string\",\n                \"user_name\": \"string\",\n                \"create_time\": \"YYYY-MM-DD HH:MM:SS\"\n            }\n        ]\n    }\n}",          "type": "json"        }      ]    }  },  {    "type": "get",    "url": "/api/v1.0/billing/bills?start_time=<epoch_seconds>&end_time=<epoch_seconds>&page_size=<int>&page_num=<int>",    "title": "9.1 账单查询",    "name": "get_bills",    "group": "9_bills",    "version": "1.0.0",    "description": "<p>查询账单信息</p>",    "permission": [      {        "name": "user and organization"      }    ],    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "json",            "optional": false,            "field": "header",            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"          }        ]      }    },    "filename": "build/apidoc.py",    "groupTitle": "9_bills",    "success": {      "examples": [        {          "title": "返回",          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        \"count\": int,\n        \"bills_total\": {\n                           \"resource_cost\": float,\n                           \"voucher_cost\": float\n                       },\n        \"bills_list\": [\n            {\n                \"start_time\": \"YY-MM-DD\",\n                \"end_time\": \"YY-MM-DD\",\n                \"team_uuid\": \"string\",\n                \"project_uuid\": \"string\",\n                \"user_uuid\": \"string\",\n                \"resource_uuid\": \"string\",\n                \"resource_name\": \"string\",\n                \"resource_type\": \"string\",\n                \"resource_conf\": \"string\",\n                \"resource_status\": \"string\",\n                \"resource_cost\": float,\n                \"voucher_cost\": float\n            },\n            {\n                \"start_time\": \"YY-MM-DD\",\n                \"end_time\": \"YY-MM-DD\",\n                \"team_uuid\": \"string\",\n                \"project_uuid\": \"string\",\n                \"user_uuid\": \"string\",\n                \"resource_uuid\": \"string\",\n                \"resource_name\": \"string\",\n                \"resource_type\": \"string\",\n                \"resource_conf\": \"string\",\n                \"resource_status\": \"string\",\n                \"resource_cost\": float,\n                \"voucher_cost\": float\n            },\n            {\n                \"start_time\": \"YY-MM-DD\",\n                \"end_time\": \"YY-MM-DD\",\n                \"team_uuid\": \"string\",\n                \"project_uuid\": \"string\",\n                \"user_uuid\": \"string\",\n                \"resource_uuid\": \"string\",\n                \"resource_name\": \"string\",\n                \"resource_type\": \"string\",\n                \"resource_conf\": \"string\",\n                \"resource_status\": \"string\",\n                \"resource_cost\": float,\n                \"voucher_cost\": float\n            }\n        ]\n    }\n}",          "type": "json"        }      ]    }  }] });
