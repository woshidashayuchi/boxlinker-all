/**
 * Created by zhangsai on 16/9/2.
 */
import React,{ PropTypes,Component } from 'react';
import HeadLine from '../../components/HeadLine';

class GetRealmNameTabs extends Component{
  getRealmNameTableBody(){
    return (
      <tr>
        <td>
          <div className="astTdBox sdDomain">
            <input type="text" placeholder="请输入新域名"/>
          </div>
        </td>
        <td>
          <div className="astTdBox"></div>
        </td>
        <td>
          <div className="astTdBox">
            <span className="color999">是</span>
          </div>
        </td>
        <td>
          <button className="btn btn-primary">添加</button>
        </td>
      </tr>
    )
  }
  getRealmNameTable(){
    return (
      <table className="table table-hover table-bordered">
        <thead>
        <tr>
          <th width="25%">自有域名</th>
          <th width="25%">CNAME地址</th>
          <th width="25%">域名验证</th>
          <th width="25%">操作</th>
        </tr>
        </thead>
        <tbody>
        {this.getRealmNameTableBody()}
        </tbody>
      </table>
    )
  }
  render(){
    return(
      <div>
        <div className="assItem">
          <HeadLine
            title="绑定自有域名"
            titleEnglish="BIND OWN DOMAIN"
            titleInfo="域名绑定说明"
          />
        </div>
        <div className="assItem">
          {this.getRealmNameTable()}
        </div>
      </div>
    )
  }
}

export default GetRealmNameTabs;
