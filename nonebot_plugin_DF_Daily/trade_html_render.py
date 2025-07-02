# delta_report/trade_html_render.py
from datetime import datetime

def generate_ammo_trade_html(ammo_data: list) -> str:
    """生成倒子弹HTML内容"""
    # 获取当前时间
    generate_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 生成子弹卡片HTML
    ammo_cards_html = ""
    for ammo in ammo_data:
        # 绘制折线图
        chart_html = generate_price_chart(ammo["timestamps"], ammo["prices"])
        
        ammo_cards_html += f"""
        <div class="ammo-card">
            <div class="ammo-header">
                <div class="ammo-image-container" style="background: {ammo['grade_color']}">
                    <img src="{ammo['image']}" alt="{ammo['name']}" class="ammo-image">
                </div>
                <div class="ammo-info">
                    <div class="ammo-name">{ammo['name']}</div>
                    <div class="ammo-stats">
                        <div class="stat-item">
                            <span class="stat-label">收益率:</span>
                            <span class="stat-value" style="color: #ffd166;">{ammo['bl']}%</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">单发收益:</span>
                            <span class="stat-value" style="color: #06d6a0;">{ammo['profit']}</span>
                        </div>
                    </div>
                    <div class="ammo-prices">
                        <div class="price-info">
                            <span class="price-label">最低</span>
                            <span class="price-value">{ammo['price_min']}</span>
                            <span class="price-time">({ammo['hour_min']}时)</span>                   
                            <span class="price-label">最高</span>
                            <span class="price-value">{ammo['price_max']}</span>
                            <span class="price-time">({ammo['hour_max']}时)</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="price-chart">
                {chart_html}
            </div>
        </div>
        """
    
    # 完整HTML模板
    return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>三角洲行动 - 子弹交易推荐</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Exo+2:wght@400;600&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}
        
        body {{
            background: #0c151f;
            color: #e0f0ff;
            font-family: 'Roboto Condensed', sans-serif;
            line-height: 1.5;
            padding: 12px;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .container {{
            max-width: 480px;
            width: 100%;
            background: 
                linear-gradient(rgba(13, 22, 41, 0.7), rgba(13, 22, 41, 0.7)),
                url('https://game.gtimg.cn/images/dfm/cp/a20240906main/medium/part1.jpg') no-repeat center center;
            background-size: cover;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #2c4762;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
            position: relative;
        }}
        
        /* 顶部标题区域 */
        .header {{
            background: linear-gradient(to right, #0d1e2e, #152b40);
            padding: 18px 15px;
            text-align: center;
            border-bottom: 3px solid #ff6b00;
            position: relative;
            overflow: hidden;
        }}
        
        .title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: #fff;
            letter-spacing: 1px;
            margin-bottom: 5px;
            text-shadow: 0 0 12px rgba(255, 106, 0, 0.6);
        }}
        
        .subtitle {{
            font-family: 'Exo 2', sans-serif;
            font-size: 1.1rem;
            color: #a9d6e5;
            opacity: 0.9;
        }}
        
        .date {{
            background: rgba(20, 45, 70, 0.85);
            padding: 8px;
            text-align: center;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.0rem;
            font-weight: bold;
            color: #ffd166;
            border-bottom: 1px solid #2a4d6e;
        }}
        
        /* 内容区域 */
        .content {{
            padding: 12px;
        }}
        
        .section {{
            margin-bottom: 20px;
            background: rgba(18, 33, 55, 0.6);
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #3a506b;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }}
        
        .section-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.4rem;
            color: #4cc9f0;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #3a506b;
            display: flex;
            align-items: center;
        }}
        
        .section-title::before {{
            content: "▸";
            color: #ff6b00;
            margin-right: 8px;
            font-size: 1.4rem;
        }}
        
        /* 子弹卡片样式 */
        .ammo-card {{
            background: rgba(22, 38, 66, 0.6);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid #3a506b;
        }}
        
        .ammo-header {{
            display: flex;
            margin-bottom: 15px;
        }}
        
        .ammo-image-container {{
            width: 80px;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            margin-right: 15px;
            border: 2px solid #5d7a9c;
            overflow: hidden;
            background: rgba(26, 42, 77, 0.5);
        }}
        
        .ammo-image {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}
        
        .ammo-info {{
            flex: 1;
        }}
        
        .ammo-name {{
            font-family: 'Exo 2', sans-serif;
            font-size: 1.2rem;
            color: #e0e7ff;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        
        .ammo-stats {{
            display: flex;
            margin-bottom: 10px;
        }}
        
        .stat-item {{
            margin-right: 20px;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #90e0ef;
            margin-right: 5px;
        }}
        
        .stat-value {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            font-weight: bold;
        }}
        
        .ammo-prices {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .price-info {{
            background: rgba(20, 45, 70, 0.7);
            padding: 6px 10px;
            border-radius: 5px;
            border: 1px solid #4a6580;
        }}
        
        .price-label {{
            font-size: 0.9rem;
            color: #90e0ef;
            margin-right: 5px;
        }}
        
        .price-value {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.0rem;
            font-weight: bold;
            color: #ffd166;
        }}
        
        .price-time {{
            font-size: 0.5rem;
            color: #a9d6e5;
            margin-left: 5px;
        }}
        
        /* 价格折线图 */
        .price-chart {{
            background: rgba(15, 30, 50, 0.7);
            border-radius: 8px;
            padding: 10px;
            height: 150px;
            position: relative;
            overflow: hidden;
        }}
        
        .chart-container {{
            position: relative;
            width: 100%;
            height: 100%;
        }}
        
        .chart-grid {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        
        .grid-line {{
            border-top: 1px dashed rgba(90, 120, 160, 0.3);
        }}
        
        .chart-labels {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 20px;
            display: flex;
            justify-content: space-between;
            font-size: 0.7rem;
            color: #90a4ae;
        }}
        
        .chart-label {{
            transform: translateX(-50%);
        }}
        
        .chart-line {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 20px;
        }}
        
        .line-path {{
            fill: none;
            stroke: #4cc9f0;
            stroke-width: 2px;
            stroke-linejoin: round;
        }}
        
        .data-point {{
            position: absolute;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #4cc9f0;
            transform: translate(-50%, -50%);
        }}
        
        .min-price, .max-price {{
            position: absolute;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9rem;
            padding: 2px 5px;
            border-radius: 3px;
            background: rgba(0, 0, 0, 0.5);
        }}
        
        .min-price {{
            left: 5px;
            bottom: 25px;
            color: #06d6a0;
        }}
        
        .max-price {{
            right: 5px;
            top: 5px;
            color: #ef476f;
        }}
        
        .current-price {{
            position: absolute;
            top: 5px;
            left: 5px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            color: #ffd166;
            background: rgba(0, 0, 0, 0.5);
            padding: 2px 5px;
            border-radius: 3px;
        }}
        
        /* 页脚样式 */
        .footer {{
            text-align: center;
            padding: 15px;
            font-family: 'Roboto Condensed', sans-serif;
            font-size: 0.7rem;
            color: #90a4ae;
            background: rgba(10, 20, 40, 0.6);
            border-top: 1px solid #2c4762;
        }}
        
        /* 空数据提示 */
        .empty-message {{
            text-align: center;
            padding: 15px;
            color: #ff6b6b;
            font-style: italic;
        }}
        
        /* 响应式调整 */
        @media (max-width: 380px) {{
            .title {{
                font-size: 1.8rem;
            }}
            
            .ammo-image-container {{
                width: 70px;
                height: 70px;
            }}
            
            .ammo-name {{
                font-size: 1.1rem;
            }}
            
            .stat-item {{
                margin-right: 10px;
            }}
            
            .stat-value {{
                font-size: 1.0rem;
            }}
            
            .price-info {{
                padding: 4px 8px;
            }}
            
            .price-value {{
                font-size: 1.0rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">三角洲子弹交易推荐</h1>
        </div>
        
        <div class="date">收益计算已扣除手续费和保证金</div>
        
        <div class="content">
            <div class="section">
                <h2 class="section-title">昨日倒子弹最高收益</h2>
                {ammo_cards_html if ammo_cards_html else '<div class="empty-message">获取子弹数据失败，请稍后再试</div>'}
            </div>
        </div>
        
        <div class="footer">
            数据来源：三角洲经济学教父 | GTI战术部门 | 生成时间: {generate_time}
        </div>
    </div>
</body>
</html>
    """

def generate_price_chart(timestamps, prices):
    """生成价格折线图HTML"""
    if not prices or not timestamps or len(prices) != len(timestamps):
        return '<div class="empty-message">暂无价格数据</div>'
    
    # 计算价格范围
    min_price = min(prices)
    max_price = max(prices)
    price_range = max_price - min_price
    
    # 获取当前价格
    current_price = prices[-1]
    
    # 生成网格线
    grid_lines = ""
    for i in range(5):
        grid_lines += f'<div class="grid-line" style="top: {i * 25}%"></div>'
    
    # 生成时间标签
    labels_html = ""
    num_labels = min(6, len(timestamps))  # 最多显示6个标签
    for i in range(num_labels):
        index = int(i * (len(timestamps) - 1) / (num_labels - 1)) if num_labels > 1 else 0
        label = timestamps[index].split(" ")[-1]  # 只取小时部分
        position = i * 100 / (num_labels - 1) if num_labels > 1 else 0
        labels_html += f'<div class="chart-label" style="left: {position}%">{label}</div>'
    
    # 生成折线路径点
    points = []
    for i, price in enumerate(prices):
        x = i * 100 / (len(prices) - 1) if len(prices) > 1 else 0
        y = 100 - ((price - min_price) / price_range * 100) if price_range > 0 else 50
        points.append(f"{x}% {y}%")
    
    # 生成折线路径
    path_data = "M" + " L".join(points)
    
    # 生成数据点
    points_html = ""
    for i, point in enumerate(points):
        points_html += f"<div class=\"data-point\" style=\"left: {point.split(' ')[0]}; top: {point.split(' ')[1]}\"></div>"
    
    return f"""
    <div class="chart-container">
        <div class="chart-grid">
            {grid_lines}
        </div>
        <div class="current-price">当前: {current_price}</div>
        <div class="chart-line">
            <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none">
                <path class="line-path" d="{path_data}" />
            </svg>
            {points_html}
        </div>
        <div class="chart-labels">
            {labels_html}
        </div>
    </div>
    """