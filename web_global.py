
import os
# 获取当前文件的目录
base_dir = os.path.abspath(os.path.dirname(__file__))
print(base_dir)
model_base_path = base_dir
adp_path = base_dir + "/baselines/douzero_ADP/"
wp_path = base_dir + "/baselines/douzero_WP/"
resnet_path = base_dir + "/baselines/resnet/"
sl_path = base_dir + "/baselines/sl/"
pkl_path = base_dir + "/baselines/pkl/"

