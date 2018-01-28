##  角色权限控制

    @unique
    class Role(Enum):
        god   = '0'    # 上帝模式
        admin = '1'    # 管理员
        developer = '2'  # 开发者
        guest = '3'        # 观察者
    
    
    @unique
    class AccessCode(Enum):
        O = 0  # owners  拥有者
        M = 1  # Management 管理资源
        R = 2  # Read 读
        W = 3  # Write 写
        D = 4  # Delete 删除
        S = 5  # Search 搜索
 
##  用户中心组织关系数据表设计

  `orgs_base`: 组织基本信息
  
    id          组织 id
    org_name    组织名
    org_owner   组织拥有者,用户id --> user.user_id
    org_detail  组织描述
    is_public   是否公开
                1-> 公开,     允许非组织成员使用组织名进行搜索,主动提交加入申请(需要,群主或管理员同意)
                0-> 完全私有, 只能群主和管理员主动拉去成员加入,而且不允许非组织成员查看组织描述信息
                
    
  `orgs_user`: 组织用户关系表
    
    org_id         组织id --> orgs_base.id
    uid            用户id --> user.id
    user_name      用户名 --> user.user_name  (有该字段方便后期查询操作)
    role           权限角色 (只有两种角色, admin, developer, 同级别的不能降权, admin不能操作admin账号)
    confirm_url    确认加入组织的url链接
    is_confirm     用户已经确认加入该组织
    is_delete      成员是否被删除


    # 组织拥有者具有最高权限: OMRWDS  (只有组织拥有者才可以删除组织)
    # 组织一般管理员具有: MRWDS 权限
    # 组织开发者: RWS 权限
    
