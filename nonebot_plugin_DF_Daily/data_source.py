# delta_report/data_source.py
import asyncio
import httpx
from nonebot import logger
from datetime import datetime
from .config import API_URLS, HEADERS, MAP_NAMES, MAP_KEYS

# 品质颜色映射
GRADE_COLORS = {
    0: "transparent",    # 无背景
    1: "#cdd5d5",        # 灰色
    2: "#0c9507",        # 绿色
    3: "#317fd1",        # 蓝色
    4: "#9b61c8",        # 紫色
    5: "#e8a64e",        # 橙色
    6: "#cb464a",        # 红色
}

async def fetch_data():
    """从API获取数据"""
    try:
        async with httpx.AsyncClient() as client:
            # 并发请求所有API
            tasks = {name: client.get(url, headers=HEADERS, timeout=15.0) for name, url in API_URLS.items()}
            responses = await asyncio.gather(*tasks.values())
            
            # 将响应与名称关联
            results = {name: response for name, response in zip(tasks.keys(), responses)}
            
            map_codes, operation_date = parse_map_codes(results["map_pwd"].json())
            
            stations = {
                "技术中心": parse_workstation(results["tech_center"].json(), 2, sort_key="price"),
                "工作台": parse_workstation(results["workbench"].json(), 2, sort_key="price"),
                "制药台": parse_workstation(results["pharmacy"].json(), 2, sort_key="price"),
                "防具台": parse_workstation(results["armor"].json(), 2, sort_key="price")
            }
            
            bullet_changes = {
                "increase": parse_bullets(results["bullet_increase"].json(), 2),
                "decrease": parse_bullets(results["bullet_decrease"].json(), 2)
            }
            
            return {
                "map_codes": map_codes,
                "operation_date": operation_date,
                "stations": stations,
                "bullet_changes": bullet_changes
            }
            
    except Exception as e:
        return None
    
async def fetch_ammo_trade_data():
    """获取倒子弹数据"""
    try:
        async with httpx.AsyncClient() as client:
            # 获取子弹交易数据
            trade_url = API_URLS["ammo_trade"]
            trade_resp = await client.get(trade_url, headers=HEADERS, timeout=15.0)
            trade_data = trade_resp.json()
            
            if trade_data.get("code") != 0 or not isinstance(trade_data.get("data"), list):
                return []
            
            # 按收益率排序
            sorted_ammo = sorted(trade_data["data"], key=lambda x: x.get("bl", 0), reverse=True)[:3]
            
            # 获取每个子弹的历史价格数据
            ammo_details = []
            for ammo in sorted_ammo:
                history_url = API_URLS["ammo_history"].format(id=ammo["id"])
                history_resp = await client.get(history_url, headers=HEADERS, timeout=15.0)
                history_data = history_resp.json()
                
                if history_data.get("code") != 0:
                    continue
                
                # 获取历史价格数据
                timestamps = history_data.get("data", {}).get("a", [])
                prices = history_data.get("data", {}).get("b", [])
                
                # 72小时数据
                if len(timestamps) > 72:
                    timestamps = timestamps[-72:]
                    prices = prices[-72:]
                
                # 获取品质颜色
                grade = ammo.get("grade", 0)
                grade_color = GRADE_COLORS.get(grade, GRADE_COLORS[0])
                
                ammo_details.append({
                    "id": ammo["id"],
                    "name": ammo["name"],
                    "image": ammo["pic"],
                    "grade_color": grade_color,
                    "bl": ammo["bl"],  # 收益率
                    "profit": ammo["profit"],  # 单发收益
                    "price_min": ammo["price_min"],
                    "price_max": ammo["price_max"],
                    "hour_min": ammo["hour_min"],
                    "hour_max": ammo["hour_max"],
                    "timestamps": timestamps,
                    "prices": prices
                })
            
            return ammo_details
            
    except Exception as e:
        import traceback
        logger.error(f"获取子弹交易数据失败: {str(e)}\n{traceback.format_exc()}")
        return None
    
def parse_map_codes(data):
    """解析地图密码数据"""
    if data.get("code") != 0 or not data.get("data"):
        return {
            MAP_NAMES[0]: "暂无",
            MAP_NAMES[1]: "暂无",
            MAP_NAMES[2]: "暂无",
            MAP_NAMES[3]: "暂无"
        }, datetime.now().strftime("%Y-%m-%d")
    
    map_codes = {}
    operation_date = ""
    
    for i, key in enumerate(MAP_KEYS):
        map_data = data["data"].get(key, [])
        # 确保有密码数据且日期匹配
        if map_data and len(map_data) > 0:
            map_codes[MAP_NAMES[i]] = str(map_data[0])
            # 提取第一个有效日期
            if not operation_date and len(map_data) > 1:
                operation_date = map_data[1]
        else:
            map_codes[MAP_NAMES[i]] = "暂无"
    
    # 如果没有获取到日期，使用当前日期
    if not operation_date:
        operation_date = "ERROR"
    
    return map_codes, operation_date

def parse_workstation(data, count=2, sort_key="price"):
    """
    解析工作站数据
    :param data: API返回的原始数据
    :param count: 要返回的项目数量
    :param sort_key: 排序依据的键名
    :return: 排序后的项目列表
    """
    if data.get("code") != 0 or not isinstance(data.get("data"), list):
        return []
    
    # 过滤无效数据并确保价格是数值类型
    valid_items = []
    for item in data["data"]:
        # 确保排序键存在且是数值类型
        if sort_key in item and isinstance(item[sort_key], (int, float)):
            valid_items.append(item)
    
    # 按指定键降序排序
    sorted_items = sorted(valid_items, key=lambda x: x[sort_key], reverse=True)
    
    # 只取前count个项目
    top_items = sorted_items[:count]
    
    items = []
    for item in top_items:
        # 处理价格格式（添加千位分隔符）
        price = f"{item.get('price', 0):,}"
        
        # 处理利润文本
        profit = item.get("price_hour", 0)
        profit_text = f"时利润: {profit:,}" if profit != 0 else ""
        
        # 获取品质等级和对应颜色
        grade = item.get("grade", 0)
        grade_color = GRADE_COLORS.get(grade, GRADE_COLORS[0])
        
        items.append({
            "name": item.get("name", "未知物品"),
            "image": item.get("pic", "https://game.gtimg.cn/images/dfm/cp/a20250625she2/logo.png"),
            "value": price,
            "profit": profit_text,
            "grade_color": grade_color  # 添加品质颜色
        })
    
    return items

def parse_bullets(data, count=2):
    """解析子弹变动数据"""
    if data.get("code") != 0 or not isinstance(data.get("data"), list):
        return []
    
    bullets = []
    for bullet in data["data"][:count]:
        # 添加百分比符号和正负号
        change = bullet.get("bl", 0)
        sign = "+" if change >= 0 else ""
        value = f"{sign}{change}%"
        
        # 获取品质等级和对应颜色
        grade = bullet.get("grade", 0)
        grade_color = GRADE_COLORS.get(grade, GRADE_COLORS[0])
        
        bullets.append({
            "name": bullet.get("name", "未知子弹"),
            "image": bullet.get("pic", "https://game.gtimg.cn/images/dfm/cp/a20250625she2/logo.png"),
            "value": value,
            "grade_color": grade_color  # 添加品质颜色
        })
    
    return bullets