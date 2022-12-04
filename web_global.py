
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
# ------ 阈值 ------
BidThresholds = [0,  # 叫地主阈值
                      0.3,  # 抢地主阈值 (自己第一个叫地主)
                      0]  # 抢地主阈值 (自己非第一个叫地主)
JiabeiThreshold = (
    (0.3, 0.15),  # 叫地主 超级加倍 加倍 阈值
    (0.5, 0.15)  # 叫地主 超级加倍 加倍 阈值  (在地主是抢来的情况下)
)
FarmerJiabeiThreshold = (6, 1.2)
MingpaiThreshold = 0.93

card_play_resnet_path_dict = {
    'landlord': resnet_path + "resnet_landlord.ckpt",
    'landlord_up': resnet_path + "resnet_landlord_up.ckpt",
    'landlord_down': resnet_path + "resnet_landlord_down.ckpt"
}
card_play_wp_model_path = {
    'landlord': wp_path + "landlord.ckpt",
    'landlord_up': wp_path + "landlord_up.ckpt",
    'landlord_down': wp_path + "landlord_down.ckpt"
}
card_play_adp_model_path = {
    'landlord': adp_path + "landlord.ckpt",
    'landlord_up': adp_path + "landlord_up.ckpt",
    'landlord_down': adp_path + "landlord_down.ckpt"
}