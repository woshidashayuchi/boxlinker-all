import React from 'react';

class GetContainerTabs extends React.Component{
  static propTypes = {
    podList:React.PropTypes.array
  };
  componentDidMount(){
  }
  getTableLine(){
    let podList = this.props.podList;
    if (!podList||!podList.length) return <tr><td colSpan="4">暂无数据~</td></tr>;
    let body = [];
    podList.map((item,i) => {
      let n = item.containers.length;
      let port = item.containers.map((obj, j) => {
        let d = n == j + 1 ? "" : ",";
        return obj.container_port + "/" + obj.access_mode + d;
      });
      body.push(
        <tr key={i}>
          <td>{item.pod_name}</td>
          <td>{item.pod_ip}</td>
          <td>{port}</td>
          <td>
            <div
              className={`mirror-state ${item.pod_phase == "Running" ? "on" : "off"} tablePaddingLeft`}>
              {item.pod_phase == "Running" ? '运行中' : '已停止'}
            </div>
          </td>
        </tr>
      )
    });
    return body;
  }
  render(){
    return(
      <div style={{padding:"15px"}}>
        <table className="table table-hover table-bordered volumes-table">
          <thead>
          <tr>
            <th>名称</th>
            <th>IP</th>
            <th>端口</th>
            <th>状态</th>
          </tr>
          </thead>
          <tbody>
          {this.getTableLine()}
          </tbody>
        </table>
      </div>
    )

  }
}

export default GetContainerTabs;
