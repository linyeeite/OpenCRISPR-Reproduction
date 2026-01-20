OpenCRISPR-Reproduction 🧬
📖 项目简介
本项目是对 ProGen2 蛋白质语言模型在 CRISPR-Cas9 系统中应用的工程复现与机理研究。 基于 Salesforce 的 ProGen2-Small 架构，本项目实现了从序列生成到注意力机制可视化的完整流程，重点验证了 Transformer 架构在生物序列中的长距离依赖捕捉能力。

🛠️ 核心工作 (Key Contributions)
工程复现：解决了 ProGen2 旧版架构与 Hugging Face 新版 transformers 库的 DynamicCache 兼容性问题，通过运行时补丁（Runtime Patching）修复了 KV Cache 接口冲突。

推理优化：针对模型上下文窗口（1024 tokens）限制，实现了基于 max_new_tokens 的生成策略，成功生成了具有生物学意义的 Cas9 片段。

深度解释性分析：

Mask 机制验证：通过注意力热力图验证了 Causal Masking（因果掩码）的有效性（对角线特征）。

多头注意力分工：可视化证明了不同 Attention Head 分别负责捕捉局部序列连续性（对角线）和全局锚点依赖（垂直条纹）。

📊 结果展示
Self-Attention 机制可视化： (注：左图展示了 Head 2 捕捉局部依赖，右图展示了 Head 3 捕捉起始位点的全局依赖)

🚀 快速开始 (Quick Start)
1. 环境配置

Bash
pip install torch transformers seaborn matplotlib
2. 模型权重下载 由于版权和文件大小限制，请自行从 Hugging Face 下载 ProGen2-small 权重：

Hugging Face Link

将 pytorch_model.bin, config.json 等文件放入 progen/progen2/ 目录。

3. 运行推理

Bash
python src/inference.py
4. 运行可视化

Bash
python src/visualize.py
