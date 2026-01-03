import os
import json
import pandas as pd
import pdfplumber
import docx
from datetime import datetime

class KnowledgeBase:
    def __init__(self, storage_dir='knowledge_data'):
        self.storage_dir = storage_dir
        self.knowledge_file = os.path.join(storage_dir, 'knowledge.json')
        self.ensure_directories()
        self.load_knowledge()
    
    def ensure_directories(self):
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
    
    def load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge = json.load(f)
        else:
            self.knowledge = {}
    
    def save_knowledge(self):
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
    
    def add_knowledge(self, category, title, content, source=None):
        if category not in self.knowledge:
            self.knowledge[category] = []
        
        knowledge_item = {
            'id': f"{category}_{len(self.knowledge[category])}_{int(datetime.now().timestamp())}",
            'title': title,
            'content': content,
            'source': source,
            'added_at': datetime.now().isoformat()
        }
        
        self.knowledge[category].append(knowledge_item)
        self.save_knowledge()
        return knowledge_item['id']
    
    def delete_knowledge(self, category, item_id):
        if category in self.knowledge:
            self.knowledge[category] = [item for item in self.knowledge[category] if item['id'] != item_id]
            self.save_knowledge()
            return True
        return False
    
    def get_knowledge_by_category(self, category):
        return self.knowledge.get(category, [])
    
    def get_all_categories(self):
        return list(self.knowledge.keys())
    
    def parse_docx(self, file_path, category, title):
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            content = '\n'.join(full_text)
            
            return self.add_knowledge(category, title, content, source=file_path)
        except Exception as e:
            print(f"解析DOCX文件错误: {e}")
            return None
    
    def parse_pdf(self, file_path, category, title):
        try:
            content = ''
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        content += page_text + '\n'
            
            return self.add_knowledge(category, title, content, source=file_path)
        except Exception as e:
            print(f"解析PDF文件错误: {e}")
            return None
    
    def initialize_with_basic_content(self):
        # 添加一些基础的八字命理知识
        self.add_knowledge(
            '八字基础', 
            '什么是八字', 
            '八字，也叫四柱，是从历法查出的天干地支八个字，用天地天干地支表示人出生的年、月、日、时，合起来是八个字。八字（八字命理，八字命理学）是一种根据八字推命的方法。',
            '基础理论'
        )
        
        self.add_knowledge(
            '八字基础', 
            '天干地支', 
            '天干有十个：甲、乙、丙、丁、戊、己、庚、辛、壬、癸。\n地支有十二个：子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥。\n天干地支组合形成六十甲子，用于纪年、月、日、时。',
            '基础理论'
        )
        
        self.add_knowledge(
            '八字排盘', 
            '排盘方法', 
            '八字排盘需要知道出生的年、月、日、时和性别。排盘时需要考虑节气、真太阳时等因素。排盘结果会显示四柱天干地支，以及大运、流年等信息。',
            '排盘方法'
        )
        
        self.add_knowledge(
            '命理分析', 
            '五行生克', 
            '五行包括金、木、水、火、土。五行相生：金生水、水生木、木生火、火生土、土生金。五行相克：金克木、木克土、土克水、水克火、火克金。五行平衡是八字命理的核心思想。',
            '命理分析'
        )

    def extract_keywords(self, text):
        """从文本中提取关键词"""
        # 这里可以实现更复杂的关键词提取算法
        # 目前使用简单的基于词频的方法
        import jieba
        import jieba.analyse
        
        # 设置停用词
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        
        # 使用jieba分词
        words = jieba.lcut(text)
        
        # 过滤停用词和单个字符
        filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
        
        # 提取关键词（TF-IDF方法）
        keywords = jieba.analyse.extract_tags(text, topK=20)
        
        return keywords
    
    def learn_from_text(self, text, category, title):
        """从文本中学习知识"""
        try:
            # 提取关键词
            keywords = self.extract_keywords(text)
            print(f"从 {title} 中提取的关键词: {keywords}")
            
            # 这里可以实现更复杂的学习逻辑，比如：
            # 1. 建立知识图谱
            # 2. 学习命理规则
            # 3. 提取概念之间的关系
            
            # 保存学习结果
            self.save_learning_result(category, title, keywords)
            
            return keywords
        except Exception as e:
            print(f"学习过程中出错: {e}")
            return []
    
    def get_relevant_judgment(self, parameters):
        """
        命理语义搜索：根据算命参数获取最相关的天纪断语
        parameters: dict, 包含 'ten_gods', 'stars', 'pattern', 'day_stem' 等
        """
        results = []
        # 构建搜索关键词库
        search_terms = []
        if 'ten_gods' in parameters:
            search_terms.extend(list(parameters['ten_gods'].values()))
        if 'stars' in parameters:
            search_terms.extend(parameters['stars'])
        if 'pattern' in parameters:
            search_terms.append(parameters['pattern'])
        if 'day_stem' in parameters:
            search_terms.append(f"{parameters['day_stem']}日")
            
        # 遍历所有分类寻找匹配
        for category in self.get_all_categories():
            items = self.get_knowledge_by_category(category)
            for item in items:
                content = item['content']
                title = item['title']

                # 增加深度过滤逻辑：跳过目录类非实质内容
                # 如果内容中含有大量的虚线和页码（如 ............. 23），判定为目录
                if content.count('...') > 10 or content.count('···') > 10:
                    continue
                if len(content) < 50: # 太短的内容往往也缺乏参考价值
                    continue
                
                score = 0
                # 语义加权评分
                for term in search_terms:
                    if term in title: score += 20 # 标题匹配权重极高
                    if term in content: score += content.count(term)
                
                if score > 0:
                    results.append({
                        'content': content,
                        'score': score,
                        'source': item.get('source', '天纪资料库')
                    })
        
        # 按相关度排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:3] # 返回前3条最相关的内容

# 自动安装jieba库（如果需要）
try:
    import jieba
    import jieba.analyse
except ImportError:
    print("正在安装jieba库用于中文分词...")
    import subprocess
    import sys
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'jieba'])
    import jieba
    import jieba.analyse

if __name__ == '__main__':
    kb = KnowledgeBase()
    kb.initialize_with_basic_content()
    print("知识库已初始化，添加了基础八字命理知识。")
    print(f"可用分类: {kb.get_all_categories()}")