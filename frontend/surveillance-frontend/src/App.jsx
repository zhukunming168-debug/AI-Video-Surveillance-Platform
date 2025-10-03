import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog.jsx'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table.jsx'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert.jsx'
import { 
  Camera, 
  Monitor, 
  Settings, 
  AlertTriangle, 
  Users, 
  Activity, 
  Plus, 
  Play, 
  Square, 
  Eye,
  Trash2,
  Edit,
  RefreshCw,
  MapPin,
  Clock,
  Wifi,
  WifiOff
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'
import './App.css'

// 模拟数据
const mockDevices = [
  {
    id: 1,
    device_id: 'CAM001',
    name: '大门入口摄像头',
    protocol: 'GB28181',
    ip_address: '192.168.1.101',
    port: 5060,
    status: 'online',
    location: '主楼大门',
    gb_device_id: '34020000001320000001',
    gb_manufacturer: '海康威视'
  },
  {
    id: 2,
    device_id: 'CAM002',
    name: '停车场监控',
    protocol: 'ONVIF',
    ip_address: '192.168.1.102',
    port: 80,
    status: 'online',
    location: '地下停车场',
    gb_manufacturer: '大华'
  },
  {
    id: 3,
    device_id: 'CAM003',
    name: '走廊监控',
    protocol: 'RTSP',
    ip_address: '192.168.1.103',
    port: 554,
    status: 'offline',
    location: '二楼走廊',
    gb_manufacturer: '宇视'
  }
]

const mockEvents = [
  {
    id: 1,
    device_id: 'CAM001',
    event_type: 'person_detection',
    confidence: 0.95,
    created_at: '2024-01-15T10:30:00Z'
  },
  {
    id: 2,
    device_id: 'CAM002',
    event_type: 'vehicle_detection',
    confidence: 0.88,
    created_at: '2024-01-15T10:25:00Z'
  }
]

const mockStatistics = {
  devices: { total: 3, online: 2, offline: 1 },
  events: { today: 15, by_type: [
    { type: 'person_detection', count: 8 },
    { type: 'vehicle_detection', count: 5 },
    { type: 'intrusion_detection', count: 2 }
  ]}
}

// 主仪表板组件
function Dashboard() {
  const [statistics, setStatistics] = useState(mockStatistics)
  
  const chartData = [
    { name: '00:00', events: 4 },
    { name: '04:00', events: 2 },
    { name: '08:00', events: 8 },
    { name: '12:00', events: 12 },
    { name: '16:00', events: 15 },
    { name: '20:00', events: 9 }
  ]

  const pieData = statistics.events.by_type.map((item, index) => ({
    name: item.type,
    value: item.count,
    color: ['#8884d8', '#82ca9d', '#ffc658'][index]
  }))

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">总设备数</CardTitle>
            <Camera className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{statistics.devices.total}</div>
            <p className="text-xs text-muted-foreground">
              在线: {statistics.devices.online} | 离线: {statistics.devices.offline}
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">今日事件</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{statistics.events.today}</div>
            <p className="text-xs text-muted-foreground">
              比昨日增长 +12%
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">在线率</CardTitle>
            <Wifi className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round((statistics.devices.online / statistics.devices.total) * 100)}%
            </div>
            <p className="text-xs text-muted-foreground">
              设备运行状态良好
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">告警数量</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2</div>
            <p className="text-xs text-muted-foreground">
              需要处理的告警
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>事件趋势</CardTitle>
            <CardDescription>过去24小时的事件统计</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="events" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>事件类型分布</CardTitle>
            <CardDescription>不同类型事件的占比</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

// 设备管理组件
function DeviceManagement() {
  const [devices, setDevices] = useState(mockDevices)
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false)
  const [newDevice, setNewDevice] = useState({
    name: '',
    protocol: 'RTSP',
    ip_address: '',
    port: 554,
    username: '',
    password: '',
    location: ''
  })

  const handleAddDevice = () => {
    const device = {
      ...newDevice,
      id: devices.length + 1,
      device_id: `CAM${String(devices.length + 1).padStart(3, '0')}`,
      status: 'offline'
    }
    setDevices([...devices, device])
    setIsAddDialogOpen(false)
    setNewDevice({
      name: '',
      protocol: 'RTSP',
      ip_address: '',
      port: 554,
      username: '',
      password: '',
      location: ''
    })
  }

  const getStatusBadge = (status) => {
    const variants = {
      online: 'default',
      offline: 'secondary',
      error: 'destructive'
    }
    const colors = {
      online: 'text-green-600',
      offline: 'text-gray-600',
      error: 'text-red-600'
    }
    return (
      <Badge variant={variants[status]} className={colors[status]}>
        {status === 'online' ? <Wifi className="w-3 h-3 mr-1" /> : <WifiOff className="w-3 h-3 mr-1" />}
        {status === 'online' ? '在线' : status === 'offline' ? '离线' : '错误'}
      </Badge>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">设备管理</h2>
        <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              添加设备
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>添加新设备</DialogTitle>
              <DialogDescription>
                配置新的摄像头设备信息
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="name" className="text-right">
                  设备名称
                </Label>
                <Input
                  id="name"
                  value={newDevice.name}
                  onChange={(e) => setNewDevice({...newDevice, name: e.target.value})}
                  className="col-span-3"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="protocol" className="text-right">
                  协议类型
                </Label>
                <Select value={newDevice.protocol} onValueChange={(value) => setNewDevice({...newDevice, protocol: value})}>
                  <SelectTrigger className="col-span-3">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="RTSP">RTSP</SelectItem>
                    <SelectItem value="GB28181">GB28181</SelectItem>
                    <SelectItem value="ONVIF">ONVIF</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="ip" className="text-right">
                  IP地址
                </Label>
                <Input
                  id="ip"
                  value={newDevice.ip_address}
                  onChange={(e) => setNewDevice({...newDevice, ip_address: e.target.value})}
                  className="col-span-3"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="port" className="text-right">
                  端口
                </Label>
                <Input
                  id="port"
                  type="number"
                  value={newDevice.port}
                  onChange={(e) => setNewDevice({...newDevice, port: parseInt(e.target.value)})}
                  className="col-span-3"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="location" className="text-right">
                  位置
                </Label>
                <Input
                  id="location"
                  value={newDevice.location}
                  onChange={(e) => setNewDevice({...newDevice, location: e.target.value})}
                  className="col-span-3"
                />
              </div>
            </div>
            <DialogFooter>
              <Button onClick={handleAddDevice}>添加设备</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>设备列表</CardTitle>
          <CardDescription>管理所有监控设备</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>设备ID</TableHead>
                <TableHead>设备名称</TableHead>
                <TableHead>协议</TableHead>
                <TableHead>IP地址</TableHead>
                <TableHead>状态</TableHead>
                <TableHead>位置</TableHead>
                <TableHead>操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {devices.map((device) => (
                <TableRow key={device.id}>
                  <TableCell className="font-medium">{device.device_id}</TableCell>
                  <TableCell>{device.name}</TableCell>
                  <TableCell>
                    <Badge variant="outline">{device.protocol}</Badge>
                  </TableCell>
                  <TableCell>{device.ip_address}:{device.port}</TableCell>
                  <TableCell>{getStatusBadge(device.status)}</TableCell>
                  <TableCell>
                    <div className="flex items-center">
                      <MapPin className="w-3 h-3 mr-1" />
                      {device.location}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm">
                        <Eye className="w-3 h-3" />
                      </Button>
                      <Button variant="outline" size="sm">
                        <Edit className="w-3 h-3" />
                      </Button>
                      <Button variant="outline" size="sm">
                        <Trash2 className="w-3 h-3" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

// 视频监控组件
function VideoMonitoring() {
  const [activeStreams, setActiveStreams] = useState({})

  const toggleStream = (deviceId) => {
    setActiveStreams(prev => ({
      ...prev,
      [deviceId]: !prev[deviceId]
    }))
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">视频监控</h2>
        <Button variant="outline">
          <RefreshCw className="w-4 h-4 mr-2" />
          刷新所有
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockDevices.map((device) => (
          <Card key={device.id}>
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle className="text-sm">{device.name}</CardTitle>
                {getStatusBadge(device.status)}
              </div>
              <CardDescription>{device.device_id} - {device.location}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                {activeStreams[device.device_id] ? (
                  <div className="text-center">
                    <Monitor className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                    <p className="text-sm text-gray-500">视频流播放中...</p>
                  </div>
                ) : (
                  <div className="text-center">
                    <Camera className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                    <p className="text-sm text-gray-500">点击播放视频流</p>
                  </div>
                )}
              </div>
              <div className="flex space-x-2">
                <Button 
                  size="sm" 
                  onClick={() => toggleStream(device.device_id)}
                  disabled={device.status !== 'online'}
                >
                  {activeStreams[device.device_id] ? (
                    <>
                      <Square className="w-3 h-3 mr-1" />
                      停止
                    </>
                  ) : (
                    <>
                      <Play className="w-3 h-3 mr-1" />
                      播放
                    </>
                  )}
                </Button>
                <Button variant="outline" size="sm" disabled={device.status !== 'online'}>
                  <Camera className="w-3 h-3 mr-1" />
                  截图
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )

  function getStatusBadge(status) {
    const variants = {
      online: 'default',
      offline: 'secondary',
      error: 'destructive'
    }
    const colors = {
      online: 'text-green-600',
      offline: 'text-gray-600',
      error: 'text-red-600'
    }
    return (
      <Badge variant={variants[status]} className={colors[status]}>
        {status === 'online' ? <Wifi className="w-3 h-3 mr-1" /> : <WifiOff className="w-3 h-3 mr-1" />}
        {status === 'online' ? '在线' : status === 'offline' ? '离线' : '错误'}
      </Badge>
    )
  }
}

// 事件管理组件
function EventManagement() {
  const [events, setEvents] = useState(mockEvents)

  const getEventTypeLabel = (type) => {
    const labels = {
      person_detection: '人员检测',
      vehicle_detection: '车辆检测',
      intrusion_detection: '入侵检测',
      face_recognition: '人脸识别'
    }
    return labels[type] || type
  }

  const getEventTypeBadge = (type) => {
    const colors = {
      person_detection: 'bg-blue-100 text-blue-800',
      vehicle_detection: 'bg-green-100 text-green-800',
      intrusion_detection: 'bg-red-100 text-red-800',
      face_recognition: 'bg-purple-100 text-purple-800'
    }
    return (
      <Badge className={colors[type] || 'bg-gray-100 text-gray-800'}>
        {getEventTypeLabel(type)}
      </Badge>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">事件管理</h2>
        <div className="flex space-x-2">
          <Select defaultValue="all">
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="事件类型" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">所有事件</SelectItem>
              <SelectItem value="person_detection">人员检测</SelectItem>
              <SelectItem value="vehicle_detection">车辆检测</SelectItem>
              <SelectItem value="intrusion_detection">入侵检测</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline">
            <RefreshCw className="w-4 h-4 mr-2" />
            刷新
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>最近事件</CardTitle>
          <CardDescription>AI分析检测到的事件列表</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>时间</TableHead>
                <TableHead>设备</TableHead>
                <TableHead>事件类型</TableHead>
                <TableHead>置信度</TableHead>
                <TableHead>操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {events.map((event) => (
                <TableRow key={event.id}>
                  <TableCell>
                    <div className="flex items-center">
                      <Clock className="w-3 h-3 mr-1" />
                      {new Date(event.created_at).toLocaleString()}
                    </div>
                  </TableCell>
                  <TableCell className="font-medium">{event.device_id}</TableCell>
                  <TableCell>{getEventTypeBadge(event.event_type)}</TableCell>
                  <TableCell>
                    <div className="flex items-center">
                      <div className="w-full bg-gray-200 rounded-full h-2 mr-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                          style={{ width: `${event.confidence * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm">{Math.round(event.confidence * 100)}%</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm">
                        <Eye className="w-3 h-3" />
                      </Button>
                      <Button variant="outline" size="sm">
                        <Camera className="w-3 h-3" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

// 主应用组件
function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="border-b bg-white">
        <div className="container mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center space-x-4">
              <Camera className="h-8 w-8 text-blue-600" />
              <h1 className="text-xl font-bold">AI视频监控平台</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4 mr-2" />
                设置
              </Button>
              <Button variant="outline" size="sm">
                <Users className="w-4 h-4 mr-2" />
                用户
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="dashboard" className="flex items-center space-x-2">
              <Activity className="w-4 h-4" />
              <span>仪表板</span>
            </TabsTrigger>
            <TabsTrigger value="devices" className="flex items-center space-x-2">
              <Camera className="w-4 h-4" />
              <span>设备管理</span>
            </TabsTrigger>
            <TabsTrigger value="monitoring" className="flex items-center space-x-2">
              <Monitor className="w-4 h-4" />
              <span>视频监控</span>
            </TabsTrigger>
            <TabsTrigger value="events" className="flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4" />
              <span>事件管理</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard">
            <Dashboard />
          </TabsContent>

          <TabsContent value="devices">
            <DeviceManagement />
          </TabsContent>

          <TabsContent value="monitoring">
            <VideoMonitoring />
          </TabsContent>

          <TabsContent value="events">
            <EventManagement />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App
