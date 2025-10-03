from flask import Blueprint, request, jsonify, current_app
from src.models.device import Device, AIEvent, db
import cv2
import numpy as np
import threading
import time
import os
import json
from datetime import datetime
import base64

ai_bp = Blueprint('ai', __name__)

class AIAnalysisEngine:
    """AI视频分析引擎"""
    
    def __init__(self):
        self.models = {}
        self.analysis_threads = {}
        self.load_models()
    
    def load_models(self):
        """加载AI模型"""
        try:
            # 加载人脸检测器（使用OpenCV内置的Haar级联分类器）
            face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.exists(face_cascade_path):
                self.models['face_detector'] = cv2.CascadeClassifier(face_cascade_path)
            
            # 加载人体检测器（使用HOG描述符）
            self.models['person_detector'] = cv2.HOGDescriptor()
            self.models['person_detector'].setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
            
            print("AI模型加载完成")
            
        except Exception as e:
            print(f"AI模型加载失败: {e}")
    
    def detect_faces(self, frame):
        """人脸检测"""
        try:
            if 'face_detector' not in self.models:
                return []
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.models['face_detector'].detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            
            results = []
            for (x, y, w, h) in faces:
                results.append({
                    'type': 'face_detection',
                    'confidence': 0.8,
                    'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
                })
            
            return results
            
        except Exception as e:
            print(f"人脸检测错误: {e}")
            return []
    
    def detect_persons(self, frame):
        """人员检测"""
        try:
            if 'person_detector' not in self.models:
                return []
            
            persons, weights = self.models['person_detector'].detectMultiScale(
                frame, winStride=(8, 8), padding=(32, 32), scale=1.05
            )
            
            results = []
            for i, (x, y, w, h) in enumerate(persons):
                if weights[i] > 0.5:
                    results.append({
                        'type': 'person_detection',
                        'confidence': float(weights[i]),
                        'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
                    })
            
            return results
            
        except Exception as e:
            print(f"人员检测错误: {e}")
            return []
    
    def analyze_frame(self, frame, device_id, analysis_types=['face_detection', 'person_detection']):
        """分析单帧图像"""
        results = []
        
        try:
            if 'face_detection' in analysis_types:
                face_results = self.detect_faces(frame)
                results.extend(face_results)
            
            if 'person_detection' in analysis_types:
                person_results = self.detect_persons(frame)
                results.extend(person_results)
            
            # 保存检测结果到数据库
            for result in results:
                self.save_detection_result(device_id, result, frame)
            
            return results
            
        except Exception as e:
            print(f"帧分析错误: {e}")
            return []
    
    def save_detection_result(self, device_id, result, frame):
        """保存检测结果到数据库"""
        try:
            timestamp = int(time.time())
            image_dir = f"/tmp/ai_detections/{device_id}"
            os.makedirs(image_dir, exist_ok=True)
            
            bbox = result['bbox']
            x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            roi = frame[y:y+h, x:x+w]
            
            image_path = f"{image_dir}/{result['type']}_{timestamp}.jpg"
            cv2.imwrite(image_path, roi)
            
            event = AIEvent(
                device_id=device_id,
                event_type=result['type'],
                confidence=result['confidence'],
                bbox_x=x,
                bbox_y=y,
                bbox_width=w,
                bbox_height=h,
                image_path=image_path,
                metadata={'detection_time': timestamp}
            )
            
            db.session.add(event)
            db.session.commit()
            
        except Exception as e:
            print(f"保存检测结果错误: {e}")
            db.session.rollback()

# 全局AI分析引擎实例
ai_engine = AIAnalysisEngine()

@ai_bp.route('/ai/start/<device_id>', methods=['POST'])
def start_ai_analysis(device_id):
    """启动设备AI分析"""
    try:
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            return jsonify({'success': False, 'message': '设备不存在'}), 404
        
        if device.status != 'online':
            return jsonify({'success': False, 'message': '设备不在线'}), 400
        
        data = request.get_json() or {}
        analysis_types = data.get('analysis_types', ['face_detection', 'person_detection'])
        
        return jsonify({
            'success': True,
            'message': 'AI分析已启动',
            'analysis_types': analysis_types
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@ai_bp.route('/ai/models', methods=['GET'])
def get_available_models():
    """获取可用的AI模型"""
    try:
        models_info = {}
        
        for model_name, model in ai_engine.models.items():
            models_info[model_name] = {
                'name': model_name,
                'status': 'loaded' if model is not None else 'failed',
                'type': 'opencv_cascade' if 'detector' in model_name else 'unknown'
            }
        
        return jsonify({
            'success': True,
            'data': {
                'models': models_info,
                'total_models': len(models_info)
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
