# 打卡地点功能设计方案

## 项目概述

本文档描述了一个用户可以保存和查看"打卡地点"功能的设计方案。该功能允许用户记录、管理和可视化他们访问过的地点，并通过地图展示打卡路线。

## 功能特性

### 核心功能
1. **地点保存**: 用户可以添加新的打卡地点
2. **地点查看**: 用户可以浏览已保存的打卡地点列表
3. **地图可视化**: 在地图上显示打卡地点和路线
4. **路线规划**: 支持多条打卡路线的规划和展示

### 扩展功能
- 地点分类标签
- 打卡时间记录
- 照片上传
- 社交分享
- 统计分析

## 数据库设计

### 数据表结构

#### 1. checkin_locations 表
```sql
CREATE TABLE checkin_locations (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address TEXT,
    category VARCHAR(100),
    tags TEXT[],
    photos TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 2. checkin_routes 表
```sql
CREATE TABLE checkin_routes (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    location_ids INTEGER[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 3. checkin_records 表
```sql
CREATE TABLE checkin_records (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    location_id INTEGER REFERENCES checkin_locations(id),
    checkin_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    notes TEXT,
    photos TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## API 设计

### RESTful API 端点

#### 地点管理
- `GET /api/locations` - 获取用户的打卡地点列表
- `POST /api/locations` - 创建新的打卡地点
- `GET /api/locations/:id` - 获取特定地点详情
- `PUT /api/locations/:id` - 更新地点信息
- `DELETE /api/locations/:id` - 删除地点

#### 路线管理
- `GET /api/routes` - 获取用户的打卡路线列表
- `POST /api/routes` - 创建新的打卡路线
- `GET /api/routes/:id` - 获取特定路线详情
- `PUT /api/routes/:id` - 更新路线信息
- `DELETE /api/routes/:id` - 删除路线

#### 打卡记录
- `GET /api/checkins` - 获取用户的打卡记录
- `POST /api/checkins` - 创建新的打卡记录
- `GET /api/checkins/:id` - 获取特定打卡记录
- `DELETE /api/checkins/:id` - 删除打卡记录

## 前端设计

### 页面结构
1. **地点列表页**: 显示所有保存的打卡地点
2. **地点详情页**: 显示单个地点的详细信息
3. **地图页**: 在地图上显示所有地点和路线
4. **添加地点页**: 添加新的打卡地点表单
5. **路线管理页**: 管理打卡路线

### 组件设计
- `LocationCard`: 地点卡片组件
- `LocationMap`: 地图显示组件
- `LocationForm`: 地点表单组件
- `RouteManager`: 路线管理组件
- `CheckinHistory`: 打卡历史组件

## 技术栈

### 后端
- **框架**: Node.js + Express 或 Python + FastAPI
- **数据库**: PostgreSQL (Supabase)
- **认证**: Supabase Auth
- **文件存储**: Supabase Storage

### 前端
- **框架**: React.js 或 Vue.js
- **地图**: 高德地图 API 或 Google Maps API
- **UI库**: Ant Design 或 Material-UI
- **状态管理**: Redux 或 Vuex

### 部署
- **后端**: Vercel 或 Railway
- **前端**: Netlify 或 Vercel
- **数据库**: Supabase

## 示例数据

### 杭州景点打卡路线示例

基于生成的地图，以下是杭州景点的示例数据：

#### 路线1: 西湖经典游
- 杭州西湖断桥残雪
- 杭州西湖雷峰塔  
- 杭州西湖苏堤春晓

#### 路线2: 佛教文化游
- 杭州灵隐寺
- 杭州飞来峰
- 杭州三潭印月

#### 路线3: 休闲娱乐游
- 杭州宋城
- 杭州千岛湖
- 杭州西溪湿地

### 地图可视化

已生成的杭州打卡景点路线图：
- **静态预览**: https://mdn.alipayobjects.com/one_clip/afts/img/C93ZQ56UTbAAAAAAX6AAAAgAoEACAQFr/original
- **交互式地图**: https://render.alipay.com/p/yuyan/180020010001275218/travel-map.html?caprMode=sync&id=1c0358db7a7245ed9816a1f164af54ad&recordId=21829bbe17543855143051313e8198
- **移动端二维码**: https://mdn.alipayobjects.com/one_clip/afts/img/D_qCS6FquTkAAAAAQDAAAAgAoEACAQFr/original

## 实现计划

### 第一阶段 (MVP)
1. 基础数据库表创建
2. 基本的CRUD API实现
3. 简单的前端界面
4. 地图集成和地点显示

### 第二阶段
1. 路线功能实现
2. 照片上传功能
3. 用户界面优化
4. 移动端适配

### 第三阶段
1. 社交功能
2. 数据统计和分析
3. 性能优化
4. 高级地图功能

## 安全考虑

1. **用户认证**: 使用Supabase Auth进行用户认证
2. **数据权限**: 确保用户只能访问自己的数据
3. **输入验证**: 对所有用户输入进行验证和清理
4. **API限流**: 防止API滥用
5. **数据加密**: 敏感数据加密存储

## 性能优化

1. **数据库索引**: 为经常查询的字段添加索引
2. **缓存策略**: 使用Redis缓存热点数据
3. **图片优化**: 压缩和CDN加速
4. **懒加载**: 地图和图片懒加载
5. **分页**: 大数据集分页处理

## 监控和分析

1. **错误监控**: 使用Sentry进行错误追踪
2. **性能监控**: 监控API响应时间
3. **用户行为**: 分析用户使用模式
4. **业务指标**: 跟踪关键业务指标

---

*文档创建时间: 2024年*
*最后更新: 2024年*