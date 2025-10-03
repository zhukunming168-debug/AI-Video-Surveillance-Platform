from flask import Blueprint, request, jsonify
from src.models.device import Device, AIEvent, db
from datetime import datetime, timedelta
import uuid

device_bp = Blueprint('device', __name__)

@device_bp.route('/devices', methods=['GET'])
def get_devices():
    """获取所有设备列表"""
    try:
        devices = Device.query.all()
        return jsonify({
            'success': True,
            'data': [device.to_dict() for device in devices]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@device_bp.route('/devices', methods=['POST'])
def add_device():
    """添加新设备"""
    try:
        data = request.get_json()
        
        # 生成设备ID
        device_id = data.get('device_id') or str(uuid.uuid4())
        
        # 检查设备ID是否已存在
        existing_device = Device.query.filter_by(device_id=device_id).first()
        if existing_device:
            return jsonify({
                'success': False,
                'message': '设备ID已存在'
            }), 400
        
        device = Device(
            device_id=device_id,
            name=data.get('name', ''),
            protocol=data.get('protocol', 'RTSP'),
            ip_address=data.get('ip_address', ''),
            port=data.get('port', 554),
            username=data.get('username'),
            password=data.get('password'),
            location=data.get('location'),
            description=data.get('description'),
            gb_device_id=data.get('gb_device_id'),
            gb_channel_id=data.get('gb_channel_id'),
            gb_manufacturer=data.get('gb_manufacturer'),
            gb_model=data.get('gb_model'),
            rtsp_url=data.get('rtsp_url')
        )
        
        db.session.add(device)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': device.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@device_bp.route('/devices/<device_id>', methods=['PUT'])
def update_device(device_id):
    """更新设备信息"""
    try:
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            return jsonify({
                'success': False,
                'message': '设备不存在'
            }), 404
        
        data = request.get_json()
        
        # 更新设备信息
        for key, value in data.items():
            if hasattr(device, key) and key != 'device_id':
                setattr(device, key, value)
        
        device.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': device.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@device_bp.route('/devices/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    """删除设备"""
    try:
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            return jsonify({
                'success': False,
                'message': '设备不存在'
            }), 404
        
        db.session.delete(device)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '设备删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@device_bp.route('/devices/<device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    """更新设备状态"""
    try:
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            return jsonify({
                'success': False,
                'message': '设备不存在'
            }), 404
        
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['online', 'offline', 'error']:
            return jsonify({
                'success': False,
                'message': '无效的设备状态'
            }), 400
        
        device.status = status
        device.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': device.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@device_bp.route('/events', methods=['GET'])
def get_events():
    """获取AI事件列表"""
    try:
        # 获取查询参数
        device_id = request.args.get('device_id')
        event_type = request.args.get('event_type')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # 构建查询
        query = AIEvent.query
        
        if device_id:
            query = query.filter(AIEvent.device_id == device_id)
        
        if event_type:
            query = query.filter(AIEvent.event_type == event_type)
        
        if start_time:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            query = query.filter(AIEvent.created_at >= start_dt)
        
        if end_time:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            query = query.filter(AIEvent.created_at <= end_dt)
        
        # 分页查询
        events = query.order_by(AIEvent.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [event.to_dict() for event in events.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': events.total,
                'pages': events.pages
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@device_bp.route('/events', methods=['POST'])
def create_event():
    """创建AI事件（通常由AI分析服务调用）"""
    try:
        data = request.get_json()
        
        event = AIEvent(
            device_id=data.get('device_id'),
            event_type=data.get('event_type'),
            confidence=data.get('confidence', 0.0),
            bbox_x=data.get('bbox_x'),
            bbox_y=data.get('bbox_y'),
            bbox_width=data.get('bbox_width'),
            bbox_height=data.get('bbox_height'),
            image_path=data.get('image_path'),
            metadata=data.get('metadata', {})
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': event.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@device_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """获取统计信息"""
    try:
        # 设备统计
        total_devices = Device.query.count()
        online_devices = Device.query.filter_by(status='online').count()
        offline_devices = Device.query.filter_by(status='offline').count()
        
        # 今日事件统计
        today = datetime.utcnow().date()
        today_events = AIEvent.query.filter(
            AIEvent.created_at >= today,
            AIEvent.created_at < today + timedelta(days=1)
        ).count()
        
        # 按事件类型统计（最近7天）
        week_ago = datetime.utcnow() - timedelta(days=7)
        event_types = db.session.query(
            AIEvent.event_type,
            db.func.count(AIEvent.id).label('count')
        ).filter(
            AIEvent.created_at >= week_ago
        ).group_by(AIEvent.event_type).all()
        
        return jsonify({
            'success': True,
            'data': {
                'devices': {
                    'total': total_devices,
                    'online': online_devices,
                    'offline': offline_devices
                },
                'events': {
                    'today': today_events,
                    'by_type': [{'type': et[0], 'count': et[1]} for et in event_types]
                }
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
