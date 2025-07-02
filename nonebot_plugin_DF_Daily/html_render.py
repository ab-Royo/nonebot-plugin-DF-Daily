# delta_report/html_render.py
from datetime import datetime
from .data_source import fetch_data  # 用于类型提示

def generate_html(data: dict) -> str:
    """根据数据生成HTML内容"""
    # 获取当前时间作为生成时间
    generate_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 生成密码房HTML
    password_rooms_html = ""
    for name, code in data["map_codes"].items():
        password_rooms_html += f"""
        <div class="room-card">
            <div class="room-name">{name}</div>
            <div class="room-code">{code}</div>
        </div>
        """
    
    # 生成工作台HTML
    workstations_html = ""
    for station_name, items in data["stations"].items():
        items_html = ""
        for item in items:
            # 添加品质背景色样式
            items_html += f"""
            <div class="item-row">
                <div class="item-image-container" style="background: {item['grade_color']}">
                    <img src="{item['image']}" alt="{item['name']}" class="item-image">
                </div>
                <div class="item-info">
                    <div class="item-name">{item['name']}</div>
                    <div class="item-details">
                        <div class="item-value">{item['value']}</div>
                        <div class="item-profit">{item['profit']}</div>
                    </div>
                </div>
            </div>
            """
        
        workstations_html += f"""
        <div class="workstation-card">
            <h3 class="workstation-title">{station_name}</h3>
            {items_html}
        </div>
        """
    
    # 生成子弹变动HTML
    increase_html = ""
    for bullet in data["bullet_changes"]["increase"]:
        # 添加品质背景色样式
        increase_html += f"""
        <div class="bullet-item">
            <div class="bullet-image-container" style="background: {bullet['grade_color']}">
                <img src="{bullet['image']}" alt="{bullet['name']}" class="bullet-image">
            </div>
            <div class="bullet-info">
                <div class="bullet-name">{bullet['name']}</div>
                <div class="bullet-value">{bullet['value']}</div>
            </div>
        </div>
        """
    
    decrease_html = ""
    for bullet in data["bullet_changes"]["decrease"]:
        # 添加品质背景色样式
        decrease_html += f"""
        <div class="bullet-item">
            <div class="bullet-image-container" style="background: {bullet['grade_color']}">
                <img src="{bullet['image']}" alt="{bullet['name']}" class="bullet-image">
            </div>
            <div class="bullet-info">
                <div class="bullet-name">{bullet['name']}</div>
                <div class="bullet-value">{bullet['value']}</div>
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
    <title>三角洲行动 - 每日战报</title>
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
                url('https://game.gtimg.cn/images/dfm/cp/a20240906main/small/p4_img1.jpg') no-repeat center center;
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
        
        /* 密码房样式 */
        .password-rooms {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}
        
        .room-card {{
            background: linear-gradient(145deg, #1a2a4e, #14213d);
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #4a6580;
            position: relative;
            overflow: hidden;
        }}
        
        .room-card::after {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(to right, #ff8c00, #ff2a00);
        }}
        
        .room-name {{
            font-family: 'Exo 2', sans-serif;
            font-size: 1.1rem;
            color: #90e0ef;
            margin-bottom: 8px;
            font-weight: 600;
            text-align: center;
        }}
        
        .room-code {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.3rem;
            color: #ffd166;
            font-weight: bold;
            letter-spacing: 2px;
            text-align: center;
            background: rgba(0, 0, 0, 0.3);
            padding: 6px;
            border-radius: 5px;
            border: 1px solid #ffb74d;
        }}
        
        /* 特勤处和工作台分组 */
        .workstation-section {{
            background: rgba(26, 42, 77, 0.5);
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 12px;
            border: 1px solid #3a506b;
            position: relative;
        }}
        
        .workstation-section::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, #ff8c00, #ff2a00);
            border-radius: 3px 0 0 3px;
        }}
        
        .workstation-group {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}
        
        .workstation-card {{
            background: rgba(22, 38, 66, 0.6);
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #3a506b;
            position: relative;
        }}
        
        .workstation-title {{
            font-family: 'Exo 2', sans-serif;
            font-size: 1.2rem;
            color: #90e0ef;
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 1px solid #3a506b;
            text-align: center;
        }}
        
        .item-row {{
            display: flex;
            padding: 8px 0;
            border-bottom: 1px dashed #3a506b;
            align-items: center;
        }}
        
        .item-row:last-child {{
            border-bottom: none;
        }}
        
        /* 道具图片1:1缩放 */
        .item-image-container {{
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 6px;
            margin-right: 10px;
            border: 2px solid #5d7a9c;
            overflow: hidden;
            background: rgba(26, 42, 77, 0.5);
            position: relative;
        }}
        
        .item-image {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}
        
        .item-info {{
            flex: 1;
            display: flex;
            flex-direction: column;
        }}
        
        .item-name {{
            font-family: 'Exo 2', sans-serif;
            font-size: 0.95rem;
            color: #e0e7ff;
            font-weight: 600;
            margin-bottom: 3px;
        }}
        
        .item-details {{
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }}
        
        .item-value {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            color: #ffd166;
            font-weight: bold;
            letter-spacing: 1px;
        }}
        
        .item-profit {{
            font-family: 'Roboto Condensed', sans-serif;
            font-size: 0.9rem;
            color: #90e0ef;
            font-style: italic;
        }}
        
        /* 子弹变动区域 */
        .bullet-changes {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-top: 12px;
        }}
        
        .change-card {{
            background: linear-gradient(145deg, #1a2a4e, #14213d);
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #4a6580;
            position: relative;
            overflow: hidden;
        }}
        
        .change-card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
        }}
        
        .increase .change-card::before {{
            background: linear-gradient(to right, #06d6a0, #118ab2);
        }}
        
        .decrease .change-card::before {{
            background: linear-gradient(to right, #ef476f, #d90429);
        }}
        
        .change-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 1px solid #3a506b;
        }}
        
        .increase .change-title {{
            color: #06d6a0;
        }}
        
        .decrease .change-title {{
            color: #ef476f;
        }}
        
        .bullet-item {{
            display: flex;
            padding: 8px 0;
            border-bottom: 1px dashed #3a506b;
            align-items: center;
        }}
        
        .bullet-item:last-child {{
            border-bottom: none;
        }}
        
        /* 子弹图片1:1缩放 */
        .bullet-image-container {{
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 5px;
            margin-right: 8px;
            border: 2px solid #5d7a9c;
            overflow: hidden;
            background: rgba(26, 42, 77, 0.5);
        }}
        
        .bullet-image {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}
        
        .bullet-info {{
            flex: 1;
        }}
        
        .bullet-name {{
            font-family: 'Exo 2', sans-serif;
            font-size: 0.9rem;
            color: #e0e7ff;
            font-weight: 500;
            margin-bottom: 2px;
        }}
        
        .bullet-value {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            font-weight: bold;
        }}
        
        .increase .bullet-value {{
            color: #06d6a0;
        }}
        
        .decrease .bullet-value {{
            color: #ef476f;
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
        
        /* 响应式调整 */
        @media (max-width: 380px) {{
            .password-rooms, .workstation-group, .bullet-changes {{
                grid-template-columns: 1fr;
            }}
            
            .title {{
                font-size: 2.0rem;
            }}
            
            .room-name {{
                font-size: 1.1rem;
            }}
            
            .room-code {{
                font-size: 1.2rem;
            }}
            
            .section-title {{
                font-size: 1.3rem;
            }}
            
            .item-image-container {{
                width: 50px;
                height: 50px;
            }}
            
            .bullet-image-container {{
                width: 40px;
                height: 40px;
            }}
        }}
        
        /* 空数据提示 */
        .empty-message {{
            text-align: center;
            padding: 15px;
            color: #ff6b6b;
            font-style: italic;
        }}
        /* 品质边框样式 */
        .item-image-container, .bullet-image-container {{
            position: relative;
            overflow: visible;
        }}
        
        .item-image-container::after, .bullet-image-container::after {{
            content: "";
            position: absolute;
            top: -3px;
            left: -3px;
            right: -3px;
            bottom: -3px;
            z-index: -1;
            border-radius: 8px;
            background: linear-gradient(135deg, #aaa, #777);
        }}
        
        /* 高品质边框效果 */
        .item-image-container.grade-4::after, .bullet-image-container.grade-4::after {{
            background: linear-gradient(135deg, #9b61c8, #6d4699);
        }}
        
        .item-image-container.grade-5::after, .bullet-image-container.grade-5::after {{
            background: linear-gradient(135deg, #e8a64e, #c08535);
        }}
        
        .item-image-container.grade-6::after, .bullet-image-container.grade-6::after {{
            background: linear-gradient(135deg, #cb464a, #a02e31);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">三角洲行动每日一图流</h1>
        </div>
        
        <div class="date">作战日期: {data['operation_date']}</div>
        
        <div class="content">
            <!-- 密码房部分 -->
            <div class="section">
                <h2 class="section-title">今日密码房</h2>
                <div class="password-rooms">
                    {password_rooms_html}
                </div>
            </div>
            
            <!-- 特勤处与工作台分组 -->
            <div class="section">
                <h2 class="section-title">特勤处（总利润Top）</h2>
                <div class="workstation-section">
                    <div class="workstation-group">
                        {workstations_html}
                    </div>
                </div>
            </div>
            
            <!-- 子弹变动部分 -->
            <div class="section">
                <h2 class="section-title">子弹变动</h2>
                <div class="bullet-changes">
                    <div class="increase">
                        <div class="change-card">
                            <h3 class="change-title">7日涨幅</h3>
                            {increase_html if increase_html else '<div class="empty-message">暂无涨幅数据</div>'}
                        </div>
                    </div>
                    
                    <div class="decrease">
                        <div class="change-card">
                            <h3 class="change-title">7日跌幅</h3>
                            {decrease_html if decrease_html else '<div class="empty-message">暂无跌幅数据</div>'}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div>数据来源：三角洲经济学教父 | GTI战术部门</div>
            <div>生成时间: {generate_time}</div>
            <div>主人今天要乌鲁鲁堵桥/红狼炸撤离点/蹲闸蹲丢包蹲飞升吗？</div>
        </div>
    </div>
</body>
</html>
    """