from flask import Blueprint, request, jsonify, Response
from src.models.device import Device
import subprocess
import threading
import time
import json
import os

stream_bp = Blueprint('stream', __name__)

# 存储活跃的流进程
active_streams = {}

class StreamManager:
    """视频流管理器"""
    
    @staticmethod
    def generate_rtsp_url(device):
        """根据设备信息生成RTSP URL"""
        if device.rtsp_url:
            return device.rtsp_url
        
        # 根据协议生成RTSP URL
        if device.protocol == 'RTSP':
            if device.username and device.password:
                return f"rtsp://{device.username}:{device.password}@{device.ip_address}:{device.port}/stream"
            else:
                return f"rtsp://{device.ip_address}:{device.port}/stream"
        
        elif device.protocol == 'GB28181':
            # GB28181协议需要通过SIP信令获取流地址，这里简化处理
            return f"rtsp://{device.ip_address}:{device.port}/{device.gb_channel_id}"
        
        elif device.protocol == 'ONVIF':
            # ONVIF协议通常使用标准RTSP路径
            if device.username and device.password:
                return f"rtsp://{device.username}:{device.password}@{device.ip_address}:{device.port}/onvif1"
            else:
                return f"rtsp://{device.ip_address}:{device.port}/onvif1"
        
        return None
    
    @staticmethod
    def start_stream_process(device_id, rtsp_url, output_format='hls'):
        """启动视频流处理进程"""
        try:
            # 创建输出目录
            output_dir = f"/tmp/streams/{device_id}"
            os.makedirs(output_dir, exist_ok=True)
            
            if output_format == 'hls':
                # HLS流输出
                output_path = f"{output_dir}/playlist.m3u8"
                cmd = [
                    'ffmpeg',
                    '-i', rtsp_url,
                    '-c:v', 'libx264',
                    '-preset', 'ultrafast',
                    '-tune', 'zerolatency',
                    '-c:a', 'aac',
                    '-f', 'hls',
                    '-hls_time', '2',
                    '-hls_list_size', '3',
                    '-hls_flags', 'delete_segments',
                    output_path
                ]
            else:
                # MJPEG流输出
                output_path = f"{output_dir}/stream.mjpg"
                cmd = [
                    'ffmpeg',
                    '-i', rtsp_url,
                    '-c:v', 'mjpeg',
                    '-q:v', '5',
                    '-r', '10',
                    '-f', 'mjpeg',
                    output_path
                ]
            
            # 启动FFmpeg进程
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            
            active_streams[device_id] = {
                'process': process,
                'output_path': output_path,
                'format': output_format,
                'start_time': time.time()
            }
            
            return True, output_path
            
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def stop_stream_process(device_id):
        """停止视频流处理进程"""
        if device_id in active_streams:
            try:
                process = active_streams[device_id]['process']
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception:
                pass
            
            del active_streams[device_id]
            return True
        return False

@stream_bp.route('/stream/start/<device_id>', methods=['POST'])
def start_stream(device_id):
    """启动设备视频流"""
    try:
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            return jsonify({
                'success': False,
                'message': '设备不存在'
            }), 404
        
        # 检查是否已有活跃流
        if device_id in active_streams:
            return jsonify({
                'success': True,
                'message': '流已经在运行',
                'stream_url': f'/api/stream/play/{device_id}'
            })
        
        # 生成RTSP URL
        rtsp_url = StreamManager.generate_rtsp_url(device)
        if not rtsp_url:
            return jsonify({
                'success': False,
                'message': '无法生成RTSP URL'
            }), 400
        
        # 获取输出格式
        data = request.get_json() or {}
        output_format = data.get('format', 'hls')
        
        # 启动流处理
        success, result = StreamManager.start_stream_process(device_id, rtsp_url, output_format)
        
        if success:
            return jsonify({
                'success': True,
                'message': '视频流启动成功',
                'stream_url': f'/api/stream/play/{device_id}',
                'rtsp_url': rtsp_url
            })
        else:
            return jsonify({
                'success': False,
                'message': f'启动视频流失败: {result}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@stream_bp.route('/stream/stop/<device_id>', methods=['POST'])
def stop_stream(device_id):
    """停止设备视频流"""
    try:
        success = StreamManager.stop_stream_process(device_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '视频流停止成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '没有找到活跃的视频流'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@stream_bp.route('/stream/play/<device_id>')
def play_stream(device_id):
    """播放设备视频流"""
    try:
        if device_id not in active_streams:
            return jsonify({
                'success': False,
                'message': '视频流未启动'
            }), 404
        
        stream_info = active_streams[device_id]
        output_path = stream_info['output_path']
        
        if stream_info['format'] == 'hls':
            # 返回HLS播放列表
            if os.path.exists(output_path):
                with open(output_path, 'r') as f:
                    content = f.read()
                return Response(content, mimetype='application/vnd.apple.mpegurl')
            else:
                return jsonify({
                    'success': False,
                    'message': 'HLS文件不存在'
                }), 404
        else:
            # 返回MJPEG流
            def generate_mjpeg():
                while device_id in active_streams:
                    if os.path.exists(output_path):
                        with open(output_path, 'rb') as f:
                            data = f.read()
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
                    time.sleep(0.1)
            
            return Response(generate_mjpeg(),
                          mimetype='multipart/x-mixed-replace; boundary=frame')
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@stream_bp.route('/stream/status', methods=['GET'])
def get_stream_status():
    """获取所有活跃流状态"""
    try:
        status = {}
        for device_id, stream_info in active_streams.items():
            process = stream_info['process']
            status[device_id] = {
                'running': process.poll() is None,
                'format': stream_info['format'],
                'start_time': stream_info['start_time'],
                'duration': time.time() - stream_info['start_time']
            }
        
        return jsonify({
            'success': True,
            'data': status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@stream_bp.route('/stream/snapshot/<device_id>', methods=['POST'])
def capture_snapshot(device_id):
    """捕获设备快照"""
    try:
        device = Device.query.filter_by(device_id=device_id).first()
        if not device:
            return jsonify({
                'success': False,
                'message': '设备不存在'
            }), 404
        
        # 生成RTSP URL
        rtsp_url = StreamManager.generate_rtsp_url(device)
        if not rtsp_url:
            return jsonify({
                'success': False,
                'message': '无法生成RTSP URL'
            }), 400
        
        # 创建快照目录
        snapshot_dir = f"/tmp/snapshots/{device_id}"
        os.makedirs(snapshot_dir, exist_ok=True)
        
        # 生成快照文件名
        timestamp = int(time.time())
        snapshot_path = f"{snapshot_dir}/snapshot_{timestamp}.jpg"
        
        # 使用FFmpeg捕获快照
        cmd = [
            'ffmpeg',
            '-i', rtsp_url,
            '-vframes', '1',
            '-q:v', '2',
            snapshot_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        
        if result.returncode == 0 and os.path.exists(snapshot_path):
            return jsonify({
                'success': True,
                'message': '快照捕获成功',
                'snapshot_path': snapshot_path,
                'snapshot_url': f'/api/stream/snapshot/{device_id}/{timestamp}'
            })
        else:
            return jsonify({
                'success': False,
                'message': '快照捕获失败'
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'message': '快照捕获超时'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
