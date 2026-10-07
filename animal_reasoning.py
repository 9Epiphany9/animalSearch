"""
极简版：经典动物识别专家系统与知识图谱查询
知识表示方法：
1. 产生式规则：IF 条件 THEN 结论（支持多步中间推导）
2. 知识图谱三元组：(动物, 属性关系, 属性值)
"""

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx

# 中文字体设置
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


class AnimalReasoningSystem:
    def __init__(self):
        # 知识表示 1：产生式规则库（分层因果推导）
        self.rules = [
            # 基础分类规则（推导中间结论）
            {"id": "R1", "if": {"有毛发"}, "then": "哺乳动物"},
            {"id": "R2", "if": {"有奶"}, "then": "哺乳动物"},
            {"id": "R3", "if": {"有羽毛"}, "then": "鸟类"},
            {"id": "R4", "if": {"会飞", "会下蛋"}, "then": "鸟类"},
            {"id": "R5", "if": {"哺乳动物", "吃肉"}, "then": "食肉动物"},
            {"id": "R6", "if": {"哺乳动物", "有爪", "有利齿", "眼向前"}, "then": "食肉动物"},
            {"id": "R7", "if": {"哺乳动物", "有蹄"}, "then": "有蹄动物"},

            # 最终识别规则（推导具体动物）
            {"id": "R8", "if": {"食肉动物", "黄褐色", "有暗条纹"}, "then": "老虎"},
            {"id": "R9", "if": {"食肉动物", "黄褐色", "有黑色斑点"}, "then": "金钱豹"},
            {"id": "R10", "if": {"有蹄动物", "脖子长", "腿长", "有暗斑点"}, "then": "长颈鹿"},
            {"id": "R11", "if": {"有蹄动物", "有黑白条纹"}, "then": "斑马"},
            {"id": "R12", "if": {"鸟类", "长脖子", "长腿", "不会飞"}, "then": "鸵鸟"},
            {"id": "R13", "if": {"鸟类", "会游泳", "不会飞", "黑白二色"}, "then": "企鹅"}
        ]

        # 知识表示 2：动物百科知识图谱三元组 (实体, 关系, 属性)
        self.triples = [
            ("老虎", "生活环境", "森林与丛林"),
            ("老虎", "保护级别", "国家一级重点保护野生动物"),
            ("老虎", "食性", "肉食性（捕食鹿、野猪等）"),
            ("金钱豹", "生活环境", "森林和丘陵地带"),
            ("金钱豹", "保护级别", "国家一级重点保护野生动物"),
            ("长颈鹿", "生活环境", "非洲热带草原"),
            ("长颈鹿", "显著特征", "世界上现存最高的陆生动物"),
            ("斑马", "生活环境", "非洲大草原"),
            ("斑马", "天敌", "狮子、鬣狗"),
            ("企鹅", "生活环境", "南极及极寒海域"),
            ("企鹅", "特殊能力", "擅长潜水与耐严寒"),
            ("鸵鸟", "生活环境", "非洲荒漠草地"),
            ("鸵鸟", "特殊能力", "奔跑速度可达70km/h")
        ]

        # 构建 NetworkX 拓扑图
        self.graph = nx.DiGraph()
        for head, rel, tail in self.triples:
            self.graph.add_edge(head, tail, relation=rel)

    def forward_reasoning(self, input_features: set):
        """
        正向产生式推理机：
        从初始特征出发，不断匹配规则推导出新事实，直到推导出具体动物。
        """
        facts = set(input_features)
        trace_logs = []
        final_animal = None
        executed_rules = set()

        # 循环推理直到没有新规则可以触发
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule["id"] in executed_rules:
                    continue
                # 如果规则的所有前提条件都在当前事实库中
                if rule["if"].issubset(facts):
                    executed_rules.add(rule["id"])
                    conclusion = rule["then"]
                    facts.add(conclusion)
                    trace_logs.append({
                        "rule_id": rule["id"],
                        "conditions": list(rule["if"]),
                        "conclusion": conclusion
                    })
                    changed = True
                    # 如果推导出的不是大类分类，而是具体动物目标
                    if rule["id"] in ["R8", "R9", "R10", "R11", "R12", "R13"]:
                        final_animal = conclusion

        return final_animal, trace_logs, facts

    def query_kg(self, animal: str):
        """知识图谱路径检索：查询动物的关联属性"""
        if not self.graph.has_node(animal):
            return []
        results = []
        for neighbor in self.graph.neighbors(animal):
            rel = self.graph[animal][neighbor]["relation"]
            results.append((rel, neighbor))
        return results

    def save_kg_image(self, output_file="knowledge_graph.png", highlight_animal=None):
        """绘制并保存动物知识图谱拓扑图（采用开阔放射状布局，彻底消除挤压重叠）"""
        from kg_layout_util import generate_beautiful_kg
        return generate_beautiful_kg(self.graph, output_path=output_file, highlight_animal=highlight_animal)

    def save_focus_kg_image(self, animal, output_file="focus_graph.png"):
        """绘制并保存单个动物的专属属性子图"""
        from kg_layout_util import generate_focus_kg
        return generate_focus_kg(animal, self.graph, output_path=output_file)


# ==================== 运行测试 ====================
if __name__ == "__main__":
    system = AnimalReasoningSystem()
    system.save_kg_image("knowledge_graph.png")
    print("知识图谱拓扑图已生成: knowledge_graph.png\n")

    # 简单测试输入特征
    test_input = {"有毛发", "吃肉", "黄褐色", "有暗条纹"}
    print(f"【输入特征】: {list(test_input)}")

    # 执行规则正向推理
    animal, logs, all_facts = system.forward_reasoning(test_input)

    print("\n【产生式正向推理过程】:")
    for log in logs:
        print(f" -> 触发规则 {log['rule_id']}: 因为 {log['conditions']}  推导出 ==> [{log['conclusion']}]")

    print(f"\n【最终识别结果】: 【{animal}】")

    # 执行知识图谱扩展查询
    kg_info = system.query_kg(animal)
    print(f"\n【知识图谱关联属性扩展 (实体关系检索)】:")
    for rel, val in kg_info:
        print(f" -> [{animal}] --({rel})--> {val}")
