import json
from lunar_python import Solar, Lunar, EightChar
from knowledge_base import KnowledgeBase
import random

# Initialize Knowledge Base
kb = KnowledgeBase()

# 六十甲子纳音表
NA_YIN_MAP = {
    '甲子': '海中金', '乙丑': '海中金', '丙寅': '炉中火', '丁卯': '炉中火', '戊辰': '大林木', '己巳': '大林木',
    '庚午': '路旁土', '辛未': '路旁土', '壬申': '剑锋金', '癸酉': '剑锋金', '甲戌': '山头火', '乙亥': '山头火',
    '丙子': '涧下水', '丁丑': '涧下水', '戊寅': '城头土', '己卯': '城头土', '庚辰': '白蜡金', '辛巳': '白蜡金',
    '壬午': '杨柳木', '癸未': '杨柳木', '甲申': '泉中水', '乙酉': '泉中水', '丙戌': '屋上土', '丁亥': '屋上土',
    '戊子': '霹雳火', '己丑': '霹雳火', '庚寅': '松柏木', '辛卯': '松柏木', '壬辰': '长流水', '癸巳': '长流水',
    '甲午': '沙中金', '乙未': '沙中金', '丙申': '山下火', '丁酉': '山下火', '戊戌': '平地木', '己亥': '平地木',
    '庚子': '壁上土', '辛丑': '壁上土', '壬寅': '金箔金', '癸卯': '金箔金', '甲辰': '覆灯火', '乙巳': '覆灯火',
    '丙午': '天河水', '丁未': '天河水', '戊申': '大驿土', '己酉': '大驿土', '庚戌': '钗钏金', '辛亥': '钗钏金',
    '壬子': '桑柘木', '癸丑': '桑柘木', '甲寅': '大溪水', '乙卯': '大溪水', '丙辰': '沙中土', '丁巳': '沙中土',
    '戊午': '天上火', '己未': '天上火', '庚申': '石榴木', '辛酉': '石榴木', '壬戌': '大海水', '癸亥': '大海水'
}

# 五行与天干地支映射
STEM_ELEMENT = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
BRANCH_ELEMENT = {'子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'}
BRANCH_HIDDEN_STEMS = {
    '子': ['癸'], '丑': ['己', '癸', '辛'], '寅': ['甲', '丙', '戊'], '卯': ['乙'],
    '辰': ['戊', '乙', '癸'], '巳': ['丙', '庚', '戊'], '午': ['丁', '己'], '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'], '酉': ['辛'], '戌': ['戊', '辛', '丁'], '亥': ['壬', '甲']
}

def get_ten_god(me_stem, target_stem):
    """计算十神关系"""
    me_elem = STEM_ELEMENT[me_stem]
    target_elem = STEM_ELEMENT[target_stem]
    me_yin_yang = 1 if me_stem in ['甲', '丙', '戊', '庚', '壬'] else 0
    target_yin_yang = 1 if target_stem in ['甲', '丙', '戊', '庚', '壬'] else 0
    same_polarity = (me_yin_yang == target_yin_yang)

    # 生克关系
    relations = {
        ('木', '木'): '比劫', ('木', '火'): '食伤', ('木', '土'): '财星', ('木', '金'): '官杀', ('木', '水'): '印枭',
        ('火', '火'): '比劫', ('火', '土'): '食伤', ('火', '金'): '财星', ('火', '水'): '官杀', ('火', '木'): '印枭',
        ('土', '土'): '比劫', ('土', '金'): '食伤', ('土', '水'): '财星', ('土', '木'): '官杀', ('土', '火'): '印枭',
        ('金', '金'): '比劫', ('金', '水'): '食伤', ('金', '木'): '财星', ('金', '火'): '官杀', ('金', '土'): '印枭',
        ('水', '水'): '比劫', ('水', '木'): '食伤', ('水', '火'): '财星', ('水', '土'): '官杀', ('水', '金'): '印枭',
    }
    
    base = relations[(me_elem, target_elem)]
    god_map = {
        ('比劫', True): '比肩', ('比劫', False): '劫财',
        ('食伤', True): '食神', ('食伤', False): '伤官',
        ('财星', True): '偏财', ('财星', False): '正财',
        ('官杀', True): '七杀', ('官杀', False): '正官',
        ('印枭', True): '枭神', ('印枭', False): '正印'
    }
    return god_map[(base, same_polarity)]

def calculate_bazi(year, month, day, hour, gender):
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    eight_char = lunar.getEightChar()
    
    return {
        'year': eight_char.getYear(),
        'month': eight_char.getMonth(),
        'day': eight_char.getDay(),
        'hour': eight_char.getTime(),
        'gender': gender,
        'four_pillars': f"{eight_char.getYear()} {eight_char.getMonth()} {eight_char.getDay()} {eight_char.getTime()}"
    }

def analyze_bazi(bazi_info):
    y, m, d, h = bazi_info['year'], bazi_info['month'], bazi_info['day'], bazi_info['hour']
    me_stem = d[0]
    month_branch = m[1]
    day_branch = d[1]
    gender = bazi_info['gender']
    
    # 1. 十神排布
    ten_gods = {
        '年干': get_ten_god(me_stem, y[0]),
        '月干': get_ten_god(me_stem, m[0]),
        '时干': get_ten_god(me_stem, h[0]),
        '日支': get_ten_god(me_stem, BRANCH_HIDDEN_STEMS[d[1]][0])
    }

    # 2. 月令权重分析 (大白话翻译)
    status_raw = get_strength_status(me_stem, month_branch)
    status_msg = {
        '旺': '能量非常强（生正逢时）',
        '相': '能量比较稳（得令之助）',
        '弱': '自身能量稍显不足（需要借力）'
    }.get(status_raw, status_raw)

    # 3. 五行统计与健康分析
    element_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    for p in [y, m, d, h]:
        element_count[STEM_ELEMENT[p[0]]] += 1
        element_count[BRANCH_ELEMENT[p[1]]] += 1
    
    health_analysis = get_health_analysis(element_count)

    # 4. 家庭与婚姻分析
    family_analysis = get_family_analysis(me_stem, day_branch, ten_gods, gender)

    # 5. 事业分析
    career_analysis = get_career_analysis(ten_gods['月干'], status_raw)

    # 6. 神煞
    gui_ren_map = {'甲': ['丑', '未'], '戊': ['丑', '未'], '庚': ['丑', '未'], '乙': ['子', '申'], '己': ['子', '申']}
    has_gui_ren = any(branch in [p[1] for p in [y, m, d, h]] for branch in gui_ren_map.get(me_stem, []))

    # 8. 四柱时段深度解析 (年月日时对应人生阶段)
    life_stages = get_four_pillar_life_stages(y, m, d, h, me_stem)

    analysis = {
        '日元': me_stem,
        '日主强弱': status_msg,
        '十神': ten_gods,
        '五行分布': element_count,
        '纳音': {
            '年': NA_YIN_MAP.get(y, '未知'),
            '月': NA_YIN_MAP.get(m, '未知'),
            '日': NA_YIN_MAP.get(d, '未知'),
            '时': NA_YIN_MAP.get(h, '未知')
        },
        '神煞提示': "命中带【天乙贵人】：生活中总有‘及时雨’帮忙，遇到困难容易遇到愿意拉你一把的人。" if has_gui_ren else "运势较为平稳，凡事需亲力亲为，一步一个脚印。",
        '性格分析': get_personality_analysis_detailed(me_stem, status_raw, month_branch),
        '事业分析': career_analysis,
        '家庭分析': family_analysis,
        '健康分析': health_analysis,
        '人生命程': life_stages,
        '运势概要': summary,
        '开运建议': lucky_res['建议文案']
    }
    
    return analysis

def get_four_pillar_life_stages(y, m, d, h, me_stem):
    """年月日时四柱深度解析各阶段命途"""
    # 辅助判断函数
    def get_stage_desc(gan, zhi, me, stage_name):
        god = get_ten_god(me, gan)
        descs = {
            '年': {
                '印': '早年得长辈庇佑，学业顺遂，根基稳固。',
                '财': '出身环境较好，从小对金钱有概念，早年生活富足。',
                '官': '家教甚严，从小表现出远超同龄人的自律。',
                '杀': '早年生活多波折感，性格较同龄人更早成熟。',
                '食': '童年生活无忧无虑，颇受宠爱，口福极佳。',
                '比': '早年多与同辈玩闹，竞争感强，性格开朗。'
            },
            '月': {
                '印': '青年时期贵人多助，适合在稳定机构发展名声。',
                '财': '正值壮年，求财欲强，是事业积累的黄金期。',
                '官': '职场运旺，易得领导提拔，适合在体制内发展。',
                '杀': '青年期压力较大，但极具开创精神，适合自主创业。',
                '才': '思维极其活跃，适合在多变的环境中寻求机遇。'
            },
            '时': {
                '印': '晚年生活安逸，受后辈尊敬，精神世界富足。',
                '财': '晚年财力雄厚，生活优渥，能享儿女之福。',
                '官': '晚年德高望重，在家族或社群中极具威信。',
                '杀': '晚年依然充满活力，闲不下来，喜欢折腾。',
                '食': '晚年有口福，心态年轻，与子孙关系和谐。'
            }
        }
        # 简化匹配逻辑
        for key in descs.get(stage_name, {}):
            if key in god: return descs[stage_name][key]
        return "平稳发展，波澜不惊。"

    res = {
        '早年(1-16岁)': f"【年柱：根基】{get_stage_desc(y[0], y[1], me_stem, '年')}",
        '青年(17-32岁)': f"【月柱：事业】{get_stage_desc(m[0], m[1], me_stem, '月')}",
        '中年(33-48岁)': f"【日柱：核心】日坐‘{get_ten_god(me_stem, BRANCH_HIDDEN_STEMS[d[1]][0])}’。这是你人生最关键的转化期，家庭与自我的平衡是主题。",
        '晚年(49岁后)': f"【时柱：归宿】{get_stage_desc(h[0], h[1], me_stem, '时')}"
    }
    return res

def get_strength_status(stem, month_branch):
    me_elem = STEM_ELEMENT[stem]
    month_elem = BRANCH_ELEMENT[month_branch]
    if me_elem == month_elem: return '旺'
    if (me_elem == '木' and month_elem == '水') or (me_elem == '火' and month_elem == '木') or \
       (me_elem == '土' and month_elem == '火') or (me_elem == '金' and month_elem == '土') or \
       (me_elem == '水' and month_elem == '金'): return '相'
    return '弱'

def get_health_analysis(counts):
    # (保持逻辑，但文案更白话)
    missing = [k for k, v in counts.items() if v == 0]
    over = [k for k, v in counts.items() if v >= 4]
    
    advice = "身体底子不错，各方面气场还算平衡，注意保持锻炼。"
    if '木' in missing or '金' in over: advice = "【要注意肝胆】：最近是不是有点爱熬夜？别太累了。另外金气太旺对木有克制，注意下筋骨酸痛和眼部疲劳。"
    elif '火' in missing or '水' in over: advice = "【要注意循环系统】：可能有点畏寒或者气血运行慢，平时多运动，少吃生冷，保护好心脏和眼睛。"
    elif '土' in missing or '木' in over: advice = "【要注意脾胃】：容易消化不良或者胃口不好。吃饭要定时，别想太多，心思太重也伤脾胃。"
    elif '金' in missing or '火' in over: advice = "【要注意呼吸道】：季节交替容易感冒咳嗽，皮肤也容易过敏。平时多喝温水，保持家里空气流通。"
    elif '水' in missing or '土' in over: advice = "【要注意泌尿系统】：平时别憋尿，多喝淡盐水。冬天要注意保暖，别冻着腰部。"
    return advice

def get_family_analysis(me_stem, day_branch, ten_gods, gender):
    spouse_star = ten_gods['日支']
    spouse_desc = ""
    # 大白话翻译
    if spouse_star in ['正财', '偏财'] and gender == '男': spouse_desc = "你的另一半比较务实能干，是你的‘贤内助’，对你的事业有实质性的支持。"
    elif spouse_star in ['正官', '七杀'] and gender == '女': spouse_desc = "你的另一半比较有威严，有事业心，你们性格上可能需要一定的磨合，但对方很有担当。"
    elif spouse_star in ['食神', '伤官']: spouse_desc = "你的另一半很有才华，挺有生活格调，但也比较感性，你们在一起要注意情绪沟通。"
    else: spouse_desc = "你对感情看得很重，配偶和你比较同心，适合细水长流的生活。"
    
    parents = "家里长辈对你帮助很大，早期能从父母那儿得到不少照应。" if ten_gods['年干'] in ['正印', '偏印'] else "你属于白手起家型，早年比较辛苦，主要是靠自己闯荡。"
    return f"{spouse_desc} {parents}"

def get_career_analysis(month_god, status):
    career_map = {
        '正官': '【公职管理型】：你做事有章法，适合在体制内、大型企业做管理。',
        '七杀': '【开创英雄型】：你很有魄力，适合做销售、军警或自主创业。',
        '正财': '【稳健商业型】：你对数字敏感，适合财务或固定的技术活儿。',
        '偏财': '【灵活投资型】：你很有商业头脑，适合搞贸易、投资或跨行经营。',
        '正印': '【名声教育型】：你很有学问气质，适合做老师、医生或事业单位。',
        '枭神': '【奇才技术型】：你观察力敏锐，适合钻研偏门技术或玄学研究。',
        '食神': '【福气才艺型】：你挺会享受生活，适合做设计、餐饮或演艺行业。',
        '伤官': '【创意演说型】：你口才极好，适合做广告、咨询、律师。'
    }
    
    # 结合强弱给出深度动态逻辑
    status_advice = {
        '旺': '当前你能量充沛，正是大施拳脚的好时机，建议主动出击，不宜过于保守。',
        '相': '当前气场平衡，适合稳步上升，在现有的平台上深耕细作会有极好收获。',
        '弱': '当前能量稍显内敛，适合‘借势’发展，多寻找有能力的合伙人或依靠大平台，切忌单打独斗。'
    }.get(status, '建议稳健发展。')

    base = career_map.get(month_god, "综合素质全面，适合多元化发展。")
    return f"你的格局属于【{month_god}格】。{base} \n{status_advice}"

def get_personality_analysis_detailed(day_stem, status, month_branch):
    # 季节映射
    SEASON_MAP = {
        '寅': '春', '卯': '春', '辰': '春',
        '巳': '夏', '午': '夏', '未': '夏',
        '申': '秋', '酉': '秋', '戌': '秋',
        '亥': '冬', '子': '冬', '丑': '冬'
    }
    season = SEASON_MAP.get(month_branch, '四季')
    
    # 核心性格库 (日主 + 强弱 + 季节 的深度组合)
    traits = {
        '甲': {
            '春': '生于春季，木气最旺，你像森林中的领头树，极具生命力和进取心。',
            '夏': '生于夏季，火旺泄木，你虽然才华横溢，但容易感到疲惫，需要多沉淀自己。',
            '秋': '生于秋季，金旺克木，你经过磨砺，性格异常坚韧，办事有规有矩。',
            '冬': '生于冬季，水多木漂，你心思细腻但容易焦虑，需要寻找稳固的依靠。'
        },
        '乙': {
            '春': '春天的花草最是娇艳，你人缘极好，性格温柔且极具韧性。',
            '夏': '夏天的草木渴望甘露，你情感丰富且敏感，非常善于察言观色。',
            '秋': '秋天的草木虽然干枯，却更有风骨，你办事利落，从不拖泥带水。',
            '冬': '冬天的草木处于蛰伏，你性格低调，善于保护自己，是个深藏不露的高手。'
        },
        '丙': {
            '春': '春阳和煦，你性格热情且懂得节制，是个极具号召力的伙伴。',
            '夏': '盛夏骄阳，你气场强大，办事风风火火，但要注意控制脾气。',
            '秋': '秋阳爽朗，你为人刚正不阿，喜欢直言不讳，办事讲效率。',
            '冬': '冬日暖阳，你最是重情重义，在困难时刻总能给周围人带来希望。'
        },
        '丁': {
            '春': '春季的灯火，温暖而不夺目，你心思缜密，非常有才气。',
            '夏': '夏季的火焰，能量内敛，你对自己要求极高，注重精神追求。',
            '秋': '秋季的烛光，显得格外珍贵，你观察力极其敏锐，能看透事物的本质。',
            '冬': '冬夜的炉火，你是朋友圈里的主心骨，总能让人感到安心。'
        },
        '戊': {
            '春': '春天的山峦，万物生发，你诚实稳重且富有创新精神。',
            '夏': '夏季的大地，火土燥热，你性格固执但极度忠诚，是值得信赖的基石。',
            '秋': '秋天的山川，宏伟深沉，你办事极有主见，格局非常大。',
            '冬': '冬天的土地，厚重收敛，你喜欢独立思考，不随波逐流。'
        },
        '己': {
            '春': '春季的田园，最适合耕耘，你多才多艺，是那种‘样样精通’的人。',
            '夏': '夏季的干土，性格坚毅，虽然有时会感到委屈，但都能默默承受。',
            '秋': '秋季的田野，正是收获时，你非常有经济头脑，很会理财。',
            '冬': '冬季的泥土，包容性极强，你性格极好，是所有人公认的‘和事佬’。'
        },
        '庚': {
            '春': '春天的铁器，不仅锋利且带有生机，你办事果断且敢于尝试新领域。',
            '夏': '盛夏的熔炉，你经历过磨砺，眼光极高，极具开拓神精。',
            '秋': '秋季的金气最旺，你就是那种典型的‘硬汉’性格，义薄云天。',
            '冬': '冬天的金属，冰冷内含，你冷静睿智，在压力下表现最稳。'
        },
        '辛': {
            '春': '春天的珠玉，光彩夺目，你追求极致的完美，生活极具品位。',
            '夏': '夏季的饰品，清凉宜人，你性格高调但外冷内热，非常有才华。',
            '秋': '秋天的金器，质地最正，你自尊心极强，不屑于与人同流合污。',
            '冬': '冬天的白银，纯净无暇，你心思纯粹，对认定的事非常执着。'
        },
        '壬': {
            '春': '春江水暖，你极具灵活性，脑筋转得比谁都快，总有新点子。',
            '夏': '夏季的水流，能消暑降温，你是个极佳的协调者，擅长解决冲突。',
            '秋': '秋汛之水，格局极其宏大，你志向远大，绝不甘于平凡。',
            '冬': '冬天的寒潭，深不可测，你极具城府，是大规模谋划的天才。'
        },
        '癸': {
            '春': '春雨润物，你好学且博爱，总是能给人带来温润的感受。',
            '夏': '夏天的阵雨，性格直爽，虽然偶尔有脾气，但大家都知道那是为了大家好。',
            '秋': '秋天的露水，灵感极强，你对艺术或玄学有天生的感悟力。',
            '冬': '冬天的冰雪，外表清高内心纯洁，你有自己的独立世界，不被打扰。'
        }
    }
    
    # 动态匹配
    status_msg = "（能量充沛）" if status in ['旺', '相'] else "（需人扶持）"
    res = traits.get(day_stem, {}).get(season, "性格全面，极具可塑性。")
    
    return f"你是【{day_stem}】{STEM_ELEMENT[day_stem]}命人，生于【{season}】季，状态{status_msg}：{res}"

def enrich_analysis(analysis, day_stem, bazi_info):
    """命理语义检索增强"""
    try:
        # 提取当前命理特征
        params = {
            'day_stem': day_stem,
            'ten_gods': analysis.get('十神', {}),
            'pattern': analysis.get('事业分析', '')
        }
        
        # 从知识库获取最相关的断语
        judgments = kb.get_relevant_judgment(params)
        
        if judgments:
            # 格式化展示最匹配的条目
            best = judgments[0]
            snippet = best['content'][:200] + "..." if len(best['content']) > 200 else best['content']
            analysis['古籍引证'] = f"依据《天纪》资料及古籍：\n{snippet}\n(来源: {best['source']})"
        else:
            analysis['古籍引证'] = f"《三命通会》云：{day_stem}日生于{bazi_info['month'][1]}月，其势待发。"
            
    except Exception as e:
        print(f"Enrichment failed: {e}")
        analysis['古籍引证'] = "暂无深度文献匹配"

def calculate_10_year_luck(year, month, day, hour, gender, me_stem):
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    eight_char = lunar.getEightChar()
    gender_num = 1 if gender == '男' else 0
    yun = eight_char.getYun(gender_num)
    
    events = {
        '比肩': '由于‘比肩’入库，这十年你需要多结交朋友，虽然开支不小，但人脉能帮你解决不少棘手问题。',
        '劫财': '进入‘劫财’大运，虽然机会多，但竞争也非常激烈，要注意利益分配，别因为钱的事和亲友闹翻。',
        '食神': '这十年名为‘食神运’，主福气，生活会过得比较舒心，且财源较为平稳，适合发挥才艺或搞点副业。',
        '伤官': '处于‘伤官’大运，你会有很多惊人的创意，适合去搞设计或咨询工作，但要注意收敛锋芒，防范小人。',
        '正财': '进入‘正财’大运，这是勤劳致富的十年，只要脚踏实地工作，财富会稳步增长，适合买房置产。',
        '偏财': '大运见‘偏财’，意味着这十年你有不少赚‘快钱’的机会，适合做生意或搞投资，偏财运极佳。',
        '正官': '处于‘正官’运中，你会被提拔到管理岗位，权力和名声都会有所提升，适合在体制内发展。',
        '七杀': '这十年是‘七杀运’，极具挑战。虽然压力很大，但如果你能扛过去，会有翻天覆地的成就。',
        '正印': '进入‘正印’大运，乃贵人相助之象。你会有长辈或领导的提携，且在名声和学历上会有所进益。',
        '偏印': '这十年正处于‘偏印’运，你会对冷门知识或技能特别敏感。虽然心思较重，但容易在技术领域大放异彩。'
    }

    da_yun_list = []
    dy_list = yun.getDaYun()
    for i in range(1, min(len(dy_list), 9)):
        dy = dy_list[i]
        gz = dy.getGanZhi()
        ln_gan = gz[0]
        shishen = get_ten_god(me_stem, ln_gan)
        
        da_yun_list.append({
            'age': dy.getStartAge(),
            'endAge': dy.getEndAge(),
            'ganZhi': gz,
            'analysis': events.get(shishen, "此阶段大运走势平顺，建议在稳健中寻求突破。")
        })
    return da_yun_list

def generate_liu_nians(start_year, me_stem):
    # 根据流年干支和日元的关系，生成不再敷衍的动态运势
    liunians = []
    events = {
        '比肩': '今年会有很多朋友联系你，社交活动增多，虽然花销大，但能得到不少有用的消息。',
        '劫财': '今年容易有计划外的开销，感觉钱不太够花。建议和人合作时要把利益分清楚。',
        '食神': '今年心情不错，口福也特别好。如果你打算学个新技能或者搞创作，今年是非常好的机会。',
        '伤官': '今年你才华横溢，点子特别多，但要注意别在职场上得罪领导，说话稍微收敛点。',
        '正财': '今年财运不错，主要是靠你的本职工作或者稳定投入带来的收入，属于稳扎稳打的一年。',
        '偏财': '今年有‘意外惊喜’的可能，如果有投资或者中奖机会别放过，但也别太贪心。',
        '正官': '今年很有事业运，容易得到长辈或领导的提拔。虽然压力大点，但职位有望提升。',
        '七杀': '今年很有干劲，事情特别多，虽然感觉很忙很累，但你的决心能帮你打开新局面。',
        '正印': '今年贵人运特别强，很多麻烦事儿都有人帮你化解。适合买房、考试或者办各种证件。',
        '偏印': '今年你的第六感特别灵，适合静静提升自己。不过别想得太复杂，简单生活更快乐。'
    }
    
    for i in range(5):
        y = start_year + i
        solar = Solar.fromYmdHms(y, 6, 1, 12, 0, 0)
        lunar = solar.getLunar()
        year_pillar = lunar.getYearInGanZhi()
        ln_gan = year_pillar[0]
        shishen = get_ten_god(me_stem, ln_gan)
        
        liunians.append({
            'year': y,
            'ganZhi': year_pillar,
            'event': events.get(shishen, "今年运势平顺，按部就班生活即可。")
        })
    return liunians

def analyze_geographic_luck(birth_place, residence, yong_shen_elem):
    """地理方位分析：判定地域五行契合度"""
    region_map = {
        '北': '水', '黑': '水', '吉': '水', '辽': '水', '京': '水', '津': '水',
        '南': '火', '粤': '火', '桂': '火', '湘': '火', '琼': '火',
        '东': '木', '沪': '木', '苏': '木', '浙': '木', '闽': '木',
        '西': '金', '川': '金', '渝': '金', '秦': '金', '新': '金', '藏': '金',
        '中': '土', '豫': '土', '鄂': '土', '皖': '土', '鲁': '土'
    }

    def get_elem(place):
        if not place: return None
        for k, v in region_map.items():
            if k in place: return v
        return None

    birth_elem = get_elem(birth_place)
    res_elem = get_elem(residence)
    
    analysis = ""
    if res_elem:
        if res_elem == yong_shen_elem:
            analysis += f"【地域契合】：你目前居住在{residence}，此地五行属{res_elem}，正好是你的喜用方位，这叫‘得地之利’，非常利于事业稳定和身心健康。"
        else:
            analysis += f"【地域提醒】：现居地{residence}的五行气场与你并不十分契合。如果你感觉近期发展受限，可以考虑通过居家风水或多往喜用方向活动来化解。"
    
    if birth_place and residence and birth_place != residence:
        analysis += f"\n【迁移运势】：你从{birth_place}迁往{residence}，这是一次空间的跨越。{'这种变动带动了你的财运，属于越动越旺的类型' if res_elem == yong_shen_elem else '变动虽然辛苦，但能磨炼意志。'}。"
    
    return analysis if analysis else "目前在出生地或未知区域平稳发展。"

def generate_fortune_report(year, month, day, hour, gender):
    bazi_info = calculate_bazi(year, month, day, hour, gender)
    analysis = analyze_bazi(bazi_info)
    da_yuns = calculate_10_year_luck(year, month, day, hour, gender, analysis['日元'])
    liu_nians = generate_liu_nians(2025, analysis['日元'])
    
    return {
        '基本信息': {
            '出生日期': f"{year}年{month}月{day}日 {hour}时",
            '性别': gender,
            '八字': bazi_info['four_pillars']
        },
        '命理分析': analysis,
        '大运': da_yuns,
        '流年': liu_nians,
        '建议': f"【大师寄语】：凡事顺其自然。{analysis['开运建议']}"
    }

def match_bazi(male_info, female_info):
    """
    专业的八字合婚评估系统 (大白话版)
    """
    m_y, m_m, m_d, m_h = male_info['year'], male_info['month'], male_info['day'], male_info['hour']
    f_y, f_m, f_d, f_h = female_info['year'], female_info['month'], female_info['day'], female_info['hour']
    
    # 获取基础排盘
    m_bazi = calculate_bazi(m_y, m_m, m_d, m_h, '男')
    f_bazi = calculate_bazi(f_y, f_m, f_d, f_h, '女')
    m_ana = analyze_bazi(m_bazi)
    f_ana = analyze_bazi(f_bazi)
    
    score = 60 # 基础分
    analysis_points = []
    
    # 1. 天干五合 (缘分深度)
    he_map = {'甲': '己', '己': '甲', '乙': '庚', '庚': '乙', '丙': '辛', '辛': '丙', '丁': '壬', '壬': '丁', '戊': '癸', '癸': '戊'}
    m_me = m_bazi['day'][0]
    f_me = f_bazi['day'][0]
    if he_map.get(m_me) == f_me:
        score += 20
        analysis_points.append(f"【缘分极深】：你们俩的日元正好是‘天干五合’，这就是民间说的‘天作之合’，第一次见面就容易觉得特别亲切，缘分非常深。")
    elif STEM_ELEMENT[m_me] == STEM_ELEMENT[f_me]:
         score += 8
         analysis_points.append(f"【志趣相投】：你们俩五行属性相同，脾气性格很像，像朋友也像知己，相处起来没那么多弯弯绕。")

    # 2. 地支冲合 (感情稳固度)
    m_home = m_bazi['day'][1]
    f_home = f_bazi['day'][1]
    chong_map = {'子': '午', '午': '子', '丑': '未', '未': '丑', '寅': '申', '申': '寅', '卯': '酉', '酉': '卯', '辰': '戌', '戌': '辰', '巳': '亥', '亥': '巳'}
    if m_home == f_home:
        score += 5 
        analysis_points.append("【默契十足】：你们对生活的追求、对家庭的看法非常一致，属于那种不用说话也能懂对方想什么的一对。")
    elif chong_map.get(m_home) == f_home:
        score -= 15
        analysis_points.append("【性格火爆】：你们的夫妻宫有冲突，平时可能为了点鸡毛蒜皮的小事拌嘴。建议多给对方留点空间，各退一步海阔天空。")

    # 3. 五行互补 (互助加分项)
    m_counts = m_ana['五行分布']
    f_counts = f_ana['五行分布']
    m_weak = min(m_counts, key=m_counts.get)
    f_strong = max(f_counts, key=f_counts.get)
    if m_weak == f_strong:
        score += 15
        analysis_points.append(f"【天生互补】：男方最缺的‘{m_weak}’正好女方身上非常旺。这种搭配就是相互旺对方，在一起后各方面运气都容易变好。")

    # 4. 年支匹配 (根基分析)
    m_year_zhi = m_bazi['year'][1]
    f_year_zhi = f_bazi['year'][1]
    if chong_map.get(m_year_zhi) == f_year_zhi:
        score -= 5
        analysis_points.append("【初期磨合】：你们的生肖稍微有点犯冲，刚开始在一起的时候可能觉得想法不太一样，多沟通、多听听长辈的意见就好了。")

    # 判定等级 (大白话)
    level_map = {
        '上等婚': '【上等婚】：这就是缘分到了，天造地设的一对，好好珍惜，必能幸福美满。',
        '中等婚': '【中等婚】：生活平平淡淡才是真，你们虽然偶有吵架，但感情基础很稳，是合适的一对。',
        '磨合婚': '【磨合婚】：你们更像是一对‘欢喜冤家’，需要性格上的长期磨合，只要真心相待，也能修成正果。'
    }
    raw_level = "上等婚" if score >= 85 else "中等婚" if score >= 70 else "磨合婚"
    level = level_map[raw_level]
    
    return {
        'score': max(0, min(100, score)),
        'level': level,
        'analysis': analysis_points if analysis_points else ["【平平淡淡】：你们的婚配虽然没有轰轰烈烈，但细水长流才是真，好好经营生活一样幸福。"],
        'male': {'dayMaster': m_me, 'pillars': m_bazi['four_pillars']},
        'female': {'dayMaster': f_me, 'pillars': f_bazi['four_pillars']}
    }

def get_lucky_suggestions(element_count):
    # 模拟寻找平衡点：寻找最弱的五行作为喜用（简单逻辑）
    weakest = min(element_count, key=element_count.get)
    
    suggestions = {
        '木': {
            '颜色': '绿色、青色、翠色、藏青色',
            '饰品': '木质手串（如小叶紫檀、沉香、黄花梨）、绿幽灵水晶、绿松石、翡翠、孔雀石',
            '家装': '室内多摆放阔叶长青植物，装修风格宜偏向原木风，多用棉麻质地的窗帘或地毯。',
            '建议': '多前往公园、森林等植被茂密处散步。心态上要保持生发之气，多学习新知识，像树木一样向上生长。服饰宜选择舒适透气的天然材质。'
        },
        '火': {
            '颜色': '红色、粉色、紫色、暖橘色',
            '饰品': '红玛瑙、南红、红宝石、朱砂、紫水晶、石榴石',
            '家装': '室内灯光宜选择暖色调，可以点缀一些红色系的靠枕或挂画，营造温馨、热烈的氛围。',
            '建议': '性格要积极阳光，多参加聚会、演讲等社交活动。工作上适合站在前台展示自己。服饰宜选择鲜艳、亮丽的色调，材质可以多用丝绸。'
        },
        '土': {
            '颜色': '黄色、咖啡色、棕色、卡其色、米灰色',
            '饰品': '玉石（和氏璧、黄龙玉）、蜜蜡、黄水晶、陶瓷质地饰品、琥珀',
            '家装': '家具宜稳重厚实，多用陶瓷、石材作为装饰品。色调应保持沉稳，给人以安全感。',
            '建议': '为人处世要脚踏实地，诚信为本。适合进行冥想、登山等活动，多亲近土地和自然。服饰宜选择厚实耐穿的布料，剪裁大方得体。'
        },
        '金': {
            '颜色': '白色、金色、银色、杏色、金属色',
            '饰品': '金银首饰、白水晶、钛晶、金属材质的手表、砗磲、珍珠',
            '家装': '可以多使用一些金属材质的线条进行点缀，整体风格宜简约明亮，保持环境的整洁干净。',
            '建议': '处事要果断利落，坚持正义和原则。适合进行器械健身等有质感的运动。服饰宜选择挺括的空间感版型，展现利落的气质。'
        },
        '水': {
            '颜色': '黑色、蓝色、暗蓝色、灰黑色',
            '饰品': '黑曜石、海蓝宝、深色珍珠、黑发晶、蓝宝石、深色墨玉',
            '家装': '可以考虑在室内放置流水摆件或鱼缸，家具色调宜沉静。空间动线宜圆润，避免过多尖锐棱角。',
            '建议': '处事要圆润灵活，顺势而为，像水一样具有包容力。适合游泳、垂钓等水边的休闲活动。服饰宜选择轻盈、飘逸的材质。'
        }
    }
    
    res = suggestions.get(weakest, suggestions['土'])
    return {
        '喜用五行': weakest,
        '建议文案': f"【色彩开运】：建议日常多穿着【{res['颜色']}】系的服饰。 \n【饰品改运】：佩戴【{res['饰品']}】能有效增强你的气场，平衡五行，驱邪避灾。 \n【居家开运】：{res['家装']} \n【生活智慧】：{res['建议']}"
    }