import streamlit as st
import os
from animal_reasoning import AnimalReasoningSystem

st.set_page_config(
    page_title="动物智能识别与知识推理系统",
    page_icon="🐾",
    layout="wide"
)

# 顶部横幅
st.markdown("""
<div style="background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%); padding: 18px 24px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h2 style="margin: 0; color: white;">🐾 经典动物智能识别与知识推理系统</h2>
    <p style="margin: 6px 0 0 0; opacity: 0.9; font-size: 14px;">
        人工智能基础实践：基于「产生式规则 (IF-THEN)」与「知识图谱 (三元组)」的双驱动推理演示平台
    </p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def get_system():
    return AnimalReasoningSystem()

system = get_system()

# 侧边栏：点选
st.sidebar.header("🎯 特征输入面板")

preset = st.sidebar.selectbox(
    "快速载入经典案例：",
    ["自主勾选", "测试案例1：老虎（食肉/有条纹）", "测试案例2：企鹅（鸟类/会游泳）", "测试案例3：斑马（有蹄/黑白斑纹）", "测试案例4：长颈鹿（长脖长腿）"]
)

candidate_features = [
    "有毛发", "有奶", "有羽毛", "会飞", "会下蛋", "吃肉", "有爪", "有利齿", "眼向前",
    "有蹄", "黄褐色", "有暗条纹", "有黑色斑点", "脖子长", "腿长", "有暗斑点", "有黑白条纹",
    "长脖子", "长腿", "不会飞", "会游泳", "黑白二色"
]

default_selected = []
if preset == "测试案例1：老虎（食肉/有条纹）":
    default_selected = ["有毛发", "吃肉", "黄褐色", "有暗条纹"]
elif preset == "测试案例2：企鹅（鸟类/会游泳）":
    default_selected = ["有羽毛", "会游泳", "不会飞", "黑白二色"]
elif preset == "测试案例3：斑马（有蹄/黑白斑纹）":
    default_selected = ["有毛发", "有蹄", "有黑白条纹"]
elif preset == "测试案例4：长颈鹿（长脖长腿）":
    default_selected = ["有毛发", "有蹄", "脖子长", "腿长", "有暗斑点"]

selected = st.sidebar.multiselect(
    "请勾选已知特征（可多选）：",
    options=candidate_features,
    default=default_selected
)

btn = st.sidebar.button("🚀 启动双驱动推理识别", type="primary", use_container_width=True)

# 主显示区
col_res, col_kg = st.columns([1.05, 0.95])

animal_result = None

with col_res:
    st.subheader("🔍 推理演化全过程")
    
    if btn or selected:
        if not selected:
            st.warning("请在左侧侧边栏至少勾选一项特征！")
        else:
            animal, logs, all_facts = system.forward_reasoning(selected)
            animal_result = animal
            
            # 第一阶段：产生式多步推理
            st.markdown("### 步骤一：产生式规则正向推导演绎 (IF-THEN)")
            if logs:
                for idx, log in enumerate(logs, 1):
                    st.success(f"""
                    **推导步骤 {idx}** | 触发规则 `{log['rule_id']}`：  
                    - 前提条件：`{' + '.join(log['conditions'])}`  
                    - 导出新事实：➜ **【{log['conclusion']}】**
                    """)
            else:
                st.info("当前输入特征未能触发任何规则。")

            # 最终识别结论
            if animal:
                st.markdown(f"""
                <div style="background-color: #ECFDF5; border-left: 5px solid #10B981; padding: 12px 18px; border-radius: 6px; margin: 15px 0;">
                    <h3 style="margin: 0; color: #065F46;">🎉 最终识别动物：{animal}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # 第二阶段：知识图谱属性关联
                st.markdown(f"### 步骤二：知识图谱多跳语义扩展 (查询【{animal}】关联属性)")
                kg_info = system.query_kg(animal)
                if kg_info:
                    for rel, val in kg_info:
                        st.markdown(f"- 🏷️ **{rel}**：`{val}`")
                else:
                    st.write("图谱中暂无该动物的拓展信息。")
            else:
                st.warning("⚠️ 推理结束，但现有特征尚未满足任何特定动物的最终识别条件（需要补充更多特征）。")
    else:
        st.info("👈 请在左侧勾选特征或点击预设案例，即可查看两阶段推理过程。")

with col_kg:
    st.subheader("🌐 动物百科知识图谱网络")
    
    # 使用 Tabs 标签页切换展示
    tab_focus, tab_global = st.tabs(["🎯 目标物种专属子图", "🗺️ 全局放射拓扑图"])
    
    with tab_focus:
        if animal_result:
            focus_img = f"focus_{animal_result}.png"
            system.save_focus_kg_image(animal_result, output_file=focus_img)
            st.image(focus_img, caption=f"【{animal_result}】专属知识图谱属性关联子图", use_container_width=True)
        else:
            # 默认展示老虎
            default_animal = "老虎"
            focus_img = f"focus_{default_animal}.png"
            system.save_focus_kg_image(default_animal, output_file=focus_img)
            st.image(focus_img, caption=f"【{default_animal}】属性示例（启动推理后动态刷新为对应物种）", use_container_width=True)

    with tab_global:
        global_img = "knowledge_graph.png"
        if not os.path.exists(global_img):
            system.save_kg_image(global_img)
        st.image(global_img, caption="开阔星型放射拓扑图（各物种环形均匀分布，绝不拥挤）", use_container_width=True)
