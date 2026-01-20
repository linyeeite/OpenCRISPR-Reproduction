import torch
import seaborn as sns
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM

# 1. 设置路径和设备 (和 inference.py 一样)
repo_path = "../progen/progen2"
device = "cuda" if torch.cuda.is_available() else "cpu"

# 2. 加载模型 (注意：这次我们要把 output_attentions 打开！)
print("正在加载模型以提取注意力...")
tokenizer = AutoTokenizer.from_pretrained(repo_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    repo_path,
    trust_remote_code=True,
    output_attentions=True  # <--- 关键！告诉模型把注意力矩阵吐出来
)

# 补丁：修复 num_hidden_layers 问题
if not hasattr(model.config, "num_hidden_layers"):
    model.config.num_hidden_layers = model.config.n_layer

model = model.to(device)

# 3. 输入你刚才生成的这段序列 (取最后20个氨基酸来观察，太长了图看不清)
# 这是你刚才生成的结尾部分
text = "QRQITELISDRVSGETRRIQK"
inputs = tokenizer(text, return_tensors="pt").to(device)

# 4. 前向传播 (不生成，只是看一眼)
with torch.no_grad():
    outputs = model(**inputs)

# 5. 提取注意力 (Attention)
# 形状: [Batch, Num_Heads, Seq_Len, Seq_Len]
# ProGen2-small 通常有 12 个头或者 8 个头
attention_all_heads = outputs.attentions[-1].squeeze(0).cpu()
num_heads = attention_all_heads.shape[0]

print(f"当前层一共有 {num_heads} 个注意力头")

# 6. 画出前 4 个头的热力图，看看它们有什么不同
tokens = [tokenizer.decode([i]) for i in inputs['input_ids'][0]]

fig, axes = plt.subplots(2, 2, figsize=(16, 14)) # 创建 2x2 的画布
axes = axes.flatten()

for i in range(4): # 只看前4个头
    ax = axes[i]
    sns.heatmap(
        attention_all_heads[i], # 取出第 i 个头
        xticklabels=tokens,
        yticklabels=tokens,
        cmap="viridis",
        annot=False,
        cbar=False,
        ax=ax
    )
    ax.set_title(f"Head {i+1} (Focus Area)")

plt.tight_layout()
plt.show()