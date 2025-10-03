from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Device(db.Model):
    """摄像头设备模型"""
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(128), nullable=False)
    protocol = db.Column(db.String(32), nullable=False)  # GB28181, ONVIF, RTSP
    ip_address = db.Column(db.String(45), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(64))
    password = db.Column(db.String(128))
    status = db.Column(db.String(16), default='offline')  # online, offline, error
    location = db.Column(db.String(256))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # GB28181特有字段
    gb_device_id = db.Column(db.String(20))  # GB28181设备ID
    gb_channel_id = db.Column(db.String(20))  # GB28181通道ID
    gb_manufacturer = db.Column(db.String(64))  # 制造商
    gb_model = db.Column(db.String(64))  # 设备型号
    
    # RTSP流地址
    rtsp_url = db.Column(db.String(512))
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'name': self.name,
            'protocol': self.protocol,
            'ip_address': self.ip_address,
            'port': self.port,
            'username': self.username,
            'status': self.status,
            'location': self.location,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'gb_device_id': self.gb_device_id,
            'gb_channel_id': self.gb_channel_id,
            'gb_manufacturer': self.gb_manufacturer,
            'gb_model': self.gb_model,
            'rtsp_url': self.rtsp_url
        }

class AIEvent(db.Model):
    """AI分析事件模型"""
    __tablename__ = 'ai_events'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(64), db.ForeignKey('devices.device_id'), nullable=False)
    event_type = db.Column(db.String(64), nullable=False)  # person_detection, face_recognition, intrusion_detection
    confidence = db.Column(db.Float, nullable=False)
    bbox_x = db.Column(db.Integer)  # 检测框坐标
    bbox_y = db.Column(db.Integer)
    bbox_width = db.Column(db.Integer)
    bbox_height = db.Column(db.Integer)
    image_path = db.Column(db.String(512))  # 事件截图路径
    metadata = db.Column(db.JSON)  # 额外的事件元数据
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # 关联设备
    device = db.relationship('Device', backref=db.backref('events', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'event_type': self.event_type,
            'confidence': self.confidence,
            'bbox_x': self.bbox_x,
            'bbox_y': self.bbox_y,
            'bbox_width': self.bbox_width,
            'bbox_height': self.bbox_height,
            'image_path': self.image_path,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
