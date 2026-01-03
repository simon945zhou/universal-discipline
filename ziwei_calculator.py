from lunar_python import Solar, Lunar

# 地支索引
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
# 天干索引
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

def get_palace_stems(year_stem):
    """五虎遁起宫干"""
    # 甲己之年丙作首，乙庚之岁戊为头，丙辛之岁寻庚上，丁壬壬寅顺行流，戊癸甲寅定局周。
    start_map = {'甲': 2, '己': 2, '乙': 4, '庚': 4, '丙': 6, '辛': 6, '丁': 8, '壬': 8, '戊': 0, '癸': 0}
    start_stem_idx = start_map.get(year_stem)
    
    palace_stems = []
    for i in range(12):
        # 寅位是索引2，但遁干是从寅位开始算的
        # 我们索引0是子，所以需要调整偏移
        # 寅(2) -> start_stem_idx, 卯(3) -> start_stem_idx+1 ...
        # 子(0) -> start_stem_idx-2, 丑(1) -> start_stem_idx-1
        stem_idx = (start_stem_idx + (i - 2)) % 10
        palace_stems.append(TIAN_GAN[stem_idx])
    return palace_stems

def get_wuxing_ju(palace_stem, palace_branch_idx):
    """定五行局"""
    # 这里的逻辑基于命宫的天干地支
    # 六十甲子纳音定局
    # 简化对应关系
    nai_yin_map = {
        ('甲', '子'): '金', ('乙', '丑'): '金', ('丙', '寅'): '火', ('丁', '卯'): '火', ('戊', '辰'): '木', ('己', '巳'): '木',
        ('庚', '午'): '土', ('辛', '未'): '土', ('壬', '申'): '金', ('癸', '酉'): '金', ('甲', '戌'): '火', ('乙', '亥'): '火',
        ('丙', '子'): '水', ('丁', '丑'): '水', ('戊', '寅'): '土', ('己', '卯'): '土', ('庚', '辰'): '金', ('辛', '巳'): '金',
        ('壬', '午'): '木', ('癸', '未'): '木', ('甲', '申'): '水', ('乙', '酉'): '水', ('丙', '戌'): '土', ('丁', '亥'): '土',
        ('戊', '子'): '火', ('己', '丑'): '火', ('庚', '寅'): '木', ('辛', '卯'): '木', ('壬', '辰'): '水', ('癸', '巳'): '水',
        ('甲', '午'): '金', ('乙', '未'): '金', ('丙', '申'): '火', ('丁', '酉'): '火', ('戊', '戌'): '木', ('己', '亥'): '木',
        ('庚', '子'): '土', ('辛', '丑'): '土', ('壬', '寅'): '金', ('癸', '卯'): '金', ('甲', '辰'): '火', ('乙', '巳'): '火',
        ('丙', '午'): '水', ('丁', '未'): '水', ('戊', '申'): '土', ('己', '酉'): '土', ('庚', '戌'): '金', ('辛', '亥'): '金',
        ('壬', '子'): '木', ('癸', '丑'): '木', ('甲', '寅'): '水', ('乙', '卯'): '水', ('丙', '辰'): '土', ('丁', '巳'): '土',
        ('戊', '午'): '火', ('己', '未'): '火', ('庚', '申'): '木', ('辛', '酉'): '木', ('壬', '戌'): '水', ('癸', '亥'): '水'
    }
    ju_name = nai_yin_map.get((palace_stem, DI_ZHI[palace_branch_idx]), '木')
    ju_num_map = {'水': 2, '木': 3, '火': 4, '土': 5, '金': 6}
    return ju_name, ju_num_map[ju_name]

# 主星五行属性
STAR_ELEMENTS = {
    '紫微': '土', '天机': '木', '太阳': '火', '武曲': '金', '天同': '水', '廉贞': '火',
    '天府': '土', '太阴': '水', '贪狼': '木', '巨门': '水', '天相': '水', '天梁': '土',
    '七杀': '金', '破军': '水'
}

def analyze_ziwei(year, month, day, hour, gender, bazi_context=None):
    """进行精准紫微斗数分析，并融入八字五行因子"""
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    
    lunar_month = lunar.getMonth()
    lunar_day = lunar.getDay()
    # 时辰索引：子1, 丑2... 转换为 0-11
    # lunar_python 的 getTimeZhiIndex 返回 0(子), 1(丑)...
    hour_idx = lunar.getTimeZhiIndex()
    
    # 1. 定命身宫
    # 命宫：寅宫起正月，顺数月，逆数时
    life_palace_idx = (2 + (lunar_month - 1) - hour_idx) % 12
    # 身宫：寅宫起正月，顺数月，顺数时
    body_palace_idx = (2 + (lunar_month - 1) + hour_idx) % 12
    
    # 2. 起宫干
    year_stem = lunar.getYearGan()
    palace_stems = get_palace_stems(year_stem)
    
    # 3. 定命身宫干
    life_palace_stem = palace_stems[life_palace_idx]
    
    # 4. 定五行局
    ju_name, ju_num = get_wuxing_ju(life_palace_stem, life_palace_idx)
    
    # 5. 定紫微星位置 (查表法的数学逼近)
    quotient = lunar_day // ju_num
    remainder = lunar_day % ju_num
    
    if remainder != 0:
        m = ju_num - remainder
        if m % 2 != 0:
            ziwei_idx = (2 + quotient + 1 + m) % 12
        else:
            ziwei_idx = (2 + quotient + 1 - m) % 12
    else:
        ziwei_idx = (2 + quotient) % 12

    # 6. 布十四主星
    # 紫微星系：紫微、天机(逆1)、太阳(逆3)、武曲(逆4)、天同(逆5)、廉贞(逆8)
    star_pos = {}
    ziwei_stars = ['紫微', '天机', None, '太阳', '武曲', '天同', None, None, '廉贞']
    for i, star in enumerate(ziwei_stars):
        if star:
            pos = (ziwei_idx - i) % 12
            if pos not in star_pos: star_pos[pos] = []
            star_pos[pos].append(star)
            
    # 天府星系：天府(找紫微对称)、太阴、贪狼、巨门、天相、天梁、七杀、破军
    # 对称轴：寅申 (索引2和8)
    # 天府与紫微在 寅申 轴上对称计算： (2 + 8) - ziwei_idx = 10 - ziwei_idx
    tianfu_idx = (10 - ziwei_idx) % 12
    tianfu_stars = ['天府', '太阴', '贪狼', '巨门', '天相', '天梁', '七杀', None, None, None, '破军']
    for i, star in enumerate(tianfu_stars):
        if star:
            pos = (tianfu_idx + i) % 12
            if pos not in star_pos: star_pos[pos] = []
            star_pos[pos].append(star)

    # 7. 整理十二宫
    names = ['命宫', '兄弟宫', '夫妻宫', '子女宫', '财帛宫', '疾厄宫', 
             '迁移宫', '奴仆宫', '官禄宫', '田宅宫', '福德宫', '父母宫']
    palace_analysis = {}
    for i in range(12):
        p_idx = (life_palace_idx - i) % 12
        stars = star_pos.get(p_idx, [])
        palace_analysis[names[i]] = {
            'position': DI_ZHI[p_idx],
            'stars': stars,
            'is_body': p_idx == body_palace_idx
        }

    life_stars = star_pos.get(life_palace_idx, [])
    
    return {
        '命宫位置': DI_ZHI[life_palace_idx],
        '身宫位置': DI_ZHI[body_palace_idx],
        '五行局': f'{ju_name}局({ju_num})',
        '命宫主星': life_stars,
        '十二宫分析': palace_analysis,
        '总体评断': generate_overall_judgment(life_stars, gender, bazi_context)
    }

def generate_overall_judgment(life_stars, gender, bazi_context):
    if not bazi_context:
        # 回退逻辑
        if not life_stars: return "命无正曜，借对宫推之。性格灵活多变。"
        return f"【{'-'.join(life_stars)}】坐命，具备典型的星曜特质，建议顺势而为。"

    # 结合八字的深度判断
    day_master = bazi_context.get('日元', '')
    lucky_elem = bazi_context.get('喜用五行', '土')
    
    if not life_stars:
        return f"你八字日元为【{day_master}】，但紫微命宫无主星。这说明你这辈子‘变数’很多，不容易被某种刻板印象框住。结合你八字喜【{lucky_elem}】，建议多往相关行业发展，以稳住阵脚。"

    # 分析主星与日主的契合度
    major_star = life_stars[0]
    star_elem = STAR_ELEMENTS.get(major_star, '土')
    
    judgment = f"【命理深析】：你的八字日元是‘{day_master}’，紫微命盘主星是‘{major_star}’。"
    
    if star_elem == lucky_elem:
        judgment += f"\n【天助之象】：非常妙！你命宫主星属{star_elem}，正好是你八字最需要的五行。这意味着你天生具备解决困难的天赋，往往能‘不求自得’。"
    elif (lucky_elem == '木' and star_elem == '火') or (lucky_elem == '火' and star_elem == '土'):
         judgment += f"\n【顺势而发】：你的星曜气场能很好地辅助八字能量，属于‘细水长流’型，只要坚持一个方向，必有大成。"
    else:
         judgment += f"\n【磨炼成才】：你的紫微能量与八字能量存在‘跨界’情况。这说明你早年可能比较奔波，但通过这种碰撞，你能练就一身本事，属于大器晚成的格局。"

    if '紫微' in life_stars:
        judgment += f"\n【帝王特质】：紫微星入命，自尊心极强。配合你{bazi_context.get('日主强弱')}的能量，适合在管理或领导岗位大展宏图。"
    elif any(s in ['七杀', '破军', '贪狼'] for s in life_stars):
        judgment += f"\n【杀破狼格】：你是个坐不住的人，行动力极强。八字与紫微同步显示你适合开拓新市场或不稳定的职业方向。"
        
    return judgment

def generate_ziwei_report(year, month, day, hour, gender, bazi_context=None):
    return analyze_ziwei(year, month, day, hour, gender, bazi_context)