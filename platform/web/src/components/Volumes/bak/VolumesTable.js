
import React,{Component} from 'react'
import MirrorIcon from '../../components/MirrorIcon';
import Checkbox from 'react-bootstrap/lib/Checkbox';
import cx from 'classnames';

class VolumesTable extends Component {
  static propTypes = {
    onVolumesListLoad: React.PropTypes.func,
    volumesList: React.PropTypes.array
  }
  componentDidMount(){
    this.props.onVolumesListLoad();
  }
  openScaleModal(imageName){
    this.props.onItemScale(imageName);
  }
  getTableLine(item,i){
    return (
      <tr key={i}>
        <td><div className="tablePaddingLeft"><Checkbox readOnly /><MirrorIcon text={item.disk_name} /></div></td>
        <td><div className="tablePaddingLeft"><span className="color333">{item.create_time}</span></div></td>
        <td><div className="tablePaddingLeft"><a href="javascript:;" className="color333">{item.fs_type}</a></div></td>
        <td><div className={cx("mirror-state",item.disk_used == 0?"on":"off","tablePaddingLeft")}>{item.disk_used == 0?'运行':'停止'}</div></td>
        <td><div className="tablePaddingLeft"><span className="color333">{item.disk_size}</span></div></td>
        <td><div className="tablePaddingLeft"><button onClick={this.openScaleModal.bind(this,item.image_name)} className="btn btn-primary">扩容</button></div></td>
      </tr>
    )
  }
  render(){
    let me = this;
    let data = this.props.volumesList.map(function(item,i){
      return me.getTableLine(item,i)
    });
    return (
      <div>
        <table className="table table-hover table-bordered volumes-table">
          <thead>
          <tr>
            <th>存储卷名称</th>
            <th>创建时间</th>
            <th>存储格式</th>
            <th>状态</th>
            <th>大小</th>
            <th>操作</th>
          </tr>
          </thead>
          <tbody>
          {data}
          </tbody>
        </table>
        <Modal {...this.props} show={this.state.show} onHide={this.hide.bind(this)}
                               bsSize="sm" aria-labelledby="contained-modal-title-sm">
          <div className="modal-header">
            <button type="button" onClick={this.hide.bind(this)} className="close" aria-label="Close"><span aria-hidden="true">×</span></button>
            <h4 className="modal-title" id="contained-modal-title-sm">扩容</h4>
          </div>
          <div className="modal-body">
            <div className="modalItem dilatationModalItem">
              <label><span>大小</span></label>
              <label>
                <div className="modelInputRange">
                  <InputRangesBox />
                  <span>充值用户可以创建更大存储卷</span>
                </div>
              </label>
            </div>
            <div className="modalItem modelItemLast dilatationModalItem">
              <label><span> </span></label>
              <label>
                <button className="btn btn-default">保存</button>
              </label>
            </div>
          </div>
        </Modal>
      </div>
    )
  }
}

export default VolumesTable
