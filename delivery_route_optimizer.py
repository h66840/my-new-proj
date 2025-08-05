#!/usr/bin/env python3
"""
高优先级配送区域路线优化脚本
用于新增配送区域的路线规划和优化
"""

import math
from typing import List, Tuple, Dict
from dataclasses import dataclass

@dataclass
class DeliveryPoint:
    """配送点数据结构"""
    id: str
    name: str
    latitude: float
    longitude: float
    priority: int  # 1-5, 5为最高优先级
    estimated_delivery_time: int  # 预计配送时间（分钟）

class RouteOptimizer:
    """配送路线优化器"""
    
    def __init__(self):
        # 高优先级配送区域坐标点
        self.high_priority_zones = [
            DeliveryPoint("HP001", "市中心商务区", 39.9042, 116.4074, 5, 15),
            DeliveryPoint("HP002", "科技园区", 39.9889, 116.3058, 5, 20),
            DeliveryPoint("HP003", "大学城", 39.9526, 116.3017, 4, 25),
            DeliveryPoint("HP004", "医院区域", 39.9388, 116.3974, 5, 10),
            DeliveryPoint("HP005", "购物中心", 39.9170, 116.3971, 4, 30),
            DeliveryPoint("HP006", "住宅区A", 39.9280, 116.3889, 3, 35),
            DeliveryPoint("HP007", "住宅区B", 39.9350, 116.4200, 3, 40),
            DeliveryPoint("HP008", "工业园区", 39.8900, 116.4500, 2, 45),
        ]
        
        # 配送中心坐标（起点）
        self.distribution_center = DeliveryPoint("DC001", "配送中心", 39.9163, 116.3972, 5, 0)
        
        # 已知障碍物区域（施工区域、交通管制等）
        self.obstacles = [
            {"name": "施工区域1", "lat": 39.9200, "lng": 116.3900, "radius": 0.5},
            {"name": "交通管制区", "lat": 39.9400, "lng": 116.4100, "radius": 0.3},
            {"name": "临时封路", "lat": 39.9300, "lng": 116.4000, "radius": 0.2},
        ]
    
    def calculate_distance(self, point1: DeliveryPoint, point2: DeliveryPoint) -> float:
        """计算两点间的直线距离（公里）"""
        lat1, lng1 = math.radians(point1.latitude), math.radians(point1.longitude)
        lat2, lng2 = math.radians(point2.latitude), math.radians(point2.longitude)
        
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # 地球半径（公里）
        r = 6371
        return c * r
    
    def check_obstacle_interference(self, point: DeliveryPoint) -> List[str]:
        """检查配送点是否受到障碍物影响"""
        affected_obstacles = []
        
        for obstacle in self.obstacles:
            distance = self.calculate_distance(
                point,
                DeliveryPoint("temp", "temp", obstacle["lat"], obstacle["lng"], 1, 0)
            )
            
            if distance <= obstacle["radius"]:
                affected_obstacles.append(obstacle["name"])
        
        return affected_obstacles
    
    def optimize_route(self) -> Dict:
        """优化配送路线"""
        # 按优先级和配送时间排序
        sorted_points = sorted(
            self.high_priority_zones,
            key=lambda x: (-x.priority, x.estimated_delivery_time)
        )
        
        route_analysis = {
            "total_points": len(sorted_points),
            "total_distance": 0,
            "estimated_total_time": 0,
            "route_sequence": [],
            "obstacle_warnings": [],
            "coordinates_for_visualization": []
        }
        
        current_point = self.distribution_center
        route_analysis["coordinates_for_visualization"].append({
            "name": current_point.name,
            "lat": current_point.latitude,
            "lng": current_point.longitude,
            "type": "distribution_center"
        })
        
        for point in sorted_points:
            # 计算距离
            distance = self.calculate_distance(current_point, point)
            route_analysis["total_distance"] += distance
            route_analysis["estimated_total_time"] += point.estimated_delivery_time
            
            # 检查障碍物
            obstacles = self.check_obstacle_interference(point)
            if obstacles:
                route_analysis["obstacle_warnings"].append({
                    "point": point.name,
                    "obstacles": obstacles
                })
            
            # 添加到路线序列
            route_analysis["route_sequence"].append({
                "id": point.id,
                "name": point.name,
                "priority": point.priority,
                "distance_from_previous": round(distance, 2),
                "estimated_time": point.estimated_delivery_time,
                "obstacles": obstacles
            })
            
            # 添加坐标用于可视化
            route_analysis["coordinates_for_visualization"].append({
                "name": point.name,
                "lat": point.latitude,
                "lng": point.longitude,
                "type": "delivery_point",
                "priority": point.priority
            })
            
            current_point = point
        
        # 返回配送中心
        return_distance = self.calculate_distance(current_point, self.distribution_center)
        route_analysis["total_distance"] += return_distance
        route_analysis["total_distance"] = round(route_analysis["total_distance"], 2)
        
        return route_analysis

def main():
    """主函数"""
    optimizer = RouteOptimizer()
    result = optimizer.optimize_route()
    
    print("=== 高优先级配送区域路线优化报告 ===")
    print(f"总配送点数: {result['total_points']}")
    print(f"总距离: {result['total_distance']} 公里")
    print(f"预计总配送时间: {result['estimated_total_time']} 分钟")
    
    print("\n=== 优化后的配送路线 ===")
    for i, point in enumerate(result['route_sequence'], 1):
        print(f"{i}. {point['name']} (优先级: {point['priority']}, 距离: {point['distance_from_previous']}km)")
        if point['obstacles']:
            print(f"   ⚠️  障碍物警告: {', '.join(point['obstacles'])}")
    
    if result['obstacle_warnings']:
        print("\n=== 障碍物影响分析 ===")
        for warning in result['obstacle_warnings']:
            print(f"• {warning['point']}: 受到 {', '.join(warning['obstacles'])} 影响")
    
    print("\n=== 可视化坐标数据 ===")
    for coord in result['coordinates_for_visualization']:
        print(f"{coord['name']}: ({coord['lat']}, {coord['lng']})")

if __name__ == "__main__":
    main()