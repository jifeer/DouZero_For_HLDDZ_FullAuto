#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by: Raf
# Modify by: Vincentzyx
import collections

import traceback
import warnings
from douzero.env.game import GameEnv
from douzero.evaluation.deep_agent import DeepAgent
import BidModel
import LandlordModel
import FarmerModel

warnings.filterwarnings('ignore')

EnvCard2RealCard = {3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: 'T', 11: 'J', 12: 'Q',
                    13: 'K', 14: 'A', 17: '2', 20: 'X', 30: 'D'}

RealCard2EnvCard = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                    '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
                    'K': 13, 'A': 14, '2': 17, 'X': 20, 'D': 30}

AllEnvCard = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7,
              8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12,
              12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 17, 17, 17, 17, 20, 30]

AllCards = ['rD', 'bX', 'b2', 'r2', 'bA', 'rA', 'bK', 'rK', 'bQ', 'rQ', 'bJ', 'rJ', 'bT', 'rT',
            'b9', 'r9', 'b8', 'r8', 'b7', 'r7', 'b6', 'r6', 'b5', 'r5', 'b4', 'r4', 'b3', 'r3']


def manual_landlord_requirements(cards_str):
    counter = collections.Counter(cards_str)
    if (counter['D'] == 1 and counter['2'] >= 1 and counter["A"] >= 1) \
            or (counter['D'] == 1 and counter['2'] >= 2) \
            or (counter['D'] == 1 and len([key for key in counter if counter[key] == 4]) >= 1) \
            or (counter['D'] == 1 and counter['X'] == 1) \
            or (len([key for key in counter if counter[key] == 4]) >= 2) \
            or (counter["X"] == 1 and ((counter["2"] >= 2) or (counter["2"] >= 2 and counter["A"] >= 2) or (
            counter["2"] >= 2 and len([key for key in counter if counter[key] == 4]) >= 1))) \
            or (counter["2"] >= 2 and len([key for key in counter if counter[key] == 4]) >= 1):
        return True
    else:
        return False


def manual_mingpai_requirements(cards_str):
    counter = collections.Counter(cards_str)
    if (counter['D'] == 1 and counter['2'] >= 2) \
            or (counter['D'] == 1 and counter['2'] >= 1 and counter['X'] == 1) \
            or (counter['D'] == 1 and counter['2'] >= 1 and counter['A'] >= 2) \
            or (len([key for key in counter if counter[key] == 4]) >= 2) \
            or (counter["X"] == 1 and ((counter["2"] >= 2) or (counter["2"] >= 2 and counter["A"] >= 2) or (
            counter["2"] >= 2 and len([key for key in counter if counter[key] == 4]) >= 1))) \
            or ("DX" in cards_str and len([key for key in counter if counter[key] == 4]) >= 1):
        return True
    else:
        return False


class DouFacade(object):
    def __init__(self):
        self.model_type = ""
        self.env = None
        # ------ 阈值 ------
        self.BidThresholds = [0,  # 叫地主阈值
                              0.3,  # 抢地主阈值 (自己第一个叫地主)
                              0]  # 抢地主阈值 (自己非第一个叫地主)
        self.JiabeiThreshold = (
            (0.3, 0.15),  # 叫地主 超级加倍 加倍 阈值
            (0.5, 0.15)  # 叫地主 超级加倍 加倍 阈值  (在地主是抢来的情况下)
        )
        self.FarmerJiabeiThreshold = (6, 1.2)
        self.MingpaiThreshold = 0.93

        self.use_manual_landlord_requirements = False  # 手动规则
        self.use_manual_mingpai_requirements = True  # Manual Mingpai
        # ------------------
        # 坐标
        self.landlord_position_code = 0
        self.play_order = 0
        self.l_user_pos = 1  # 左边玩家位置
        self.my_pos = 2  # 我的位置
        self.r_user_pos = 3  # 右边玩家位置
        self.LastValidPlayCardEnv = []
        self.LastValidPlayPos = 0
        # Game Log Variables
        self.GameRecord = []
        self.game_type = ""
        self.initial_cards = ""
        self.initial_bid_rate = ""
        self.initial_model_rate = ""
        self.initial_farmer_rate = ""
        self.initial_mingpai = ""
        self.initial_multiply = ""
        # -------------------
        self.shouldExit = 0  # 通知上一轮记牌结束
        self.card_play_model_path_dict = {
            'landlord': "baselines/resnet/resnet_landlord.ckpt",
            'landlord_up': "baselines/resnet/resnet_landlord_up.ckpt",
            'landlord_down': "baselines/resnet/resnet_landlord_down.ckpt"
        }
        self.card_play_wp_model_path = {
            'landlord': "baselines/douzero_WP/landlord.ckpt",
            'landlord_up': "baselines/douzero_WP/landlord_up.ckpt",
            'landlord_down': "baselines/douzero_WP/landlord_down.ckpt"
        }
        self.card_play_adp_model_path = {
            'landlord': "baselines/douzero_ADP/landlord.ckpt",
            'landlord_up': "baselines/douzero_ADP/landlord_up.ckpt",
            'landlord_down': "baselines/douzero_ADP/landlord_down.ckpt"
        }
        # others
        self.other_played_cards_real = ""
        self.other_played_cards_env = []
        # 上家打出的牌
        self.upper_played_cards_real = ""
        # 下家打出的牌
        self.lower_played_cards_real = ""
        self.card_play_data_list = {}
        self.other_hand_cards = []
        self.user_hand_cards_real = ""
        self.user_hand_cards_env = []

        self.three_landlord_cards_real = ""
        self.three_landlord_cards_env = []

        self.user_position_code = 0
        self.user_position = ['landlord_up', 'landlord', 'landlord_down'][self.user_position_code]

    def init_cards(self, _user_hand_cards_real, _three_landlord_cards_real, _user_position_code, _model_type):
        self.model_type = _model_type

        self.initial_model_rate = 0

        self.user_hand_cards_env = []
        self.other_played_cards_real = ""
        self.other_played_cards_env = []
        # 上家打出的牌
        self.upper_played_cards_real = ""
        # 下家打出的牌
        self.lower_played_cards_real = ""

        self.other_hand_cards = []

        self.three_landlord_cards_real = ""
        self.three_landlord_cards_env = []
        # 玩家角色代码：0-地主上家, 1-地主, 2-地主下家
        self.user_position_code = None
        self.user_position = ""

        self.card_play_data_list = {}
        self.play_order = 0
        self.env = None

        self.user_hand_cards_real = _user_hand_cards_real
        self.user_hand_cards_env = [RealCard2EnvCard[c] for c in list(self.user_hand_cards_real)]

        self.three_landlord_cards_real = _three_landlord_cards_real
        self.three_landlord_cards_env = [RealCard2EnvCard[c] for c in list(self.three_landlord_cards_real)]

        self.user_position_code = _user_position_code

        self.user_position = ['landlord_up', 'landlord', 'landlord_down'][self.user_position_code]

        # 整副牌减去玩家手上的牌，就是其他人的手牌,再分配给另外两个角色（如何分配对AI判断没有影响）
        for i in set(AllEnvCard):
            self.other_hand_cards.extend([i] * (AllEnvCard.count(i) - self.user_hand_cards_env.count(i)))
        self.card_play_data_list.update({
            'three_landlord_cards': self.three_landlord_cards_env,
            ['landlord_up', 'landlord', 'landlord_down'][(self.user_position_code + 0) % 3]:
                self.user_hand_cards_env,
            ['landlord_up', 'landlord', 'landlord_down'][(self.user_position_code + 1) % 3]:
                self.other_hand_cards[0:17] if (self.user_position_code + 1) % 3 != 1 else self.other_hand_cards[17:],
            ['landlord_up', 'landlord', 'landlord_down'][(self.user_position_code + 2) % 3]:
                self.other_hand_cards[0:17] if (self.user_position_code + 1) % 3 == 1 else self.other_hand_cards[17:]
        })
        try:
            # 地主model初始化
            if _model_type == "resnet":
                LandlordModel.init_model("baselines/resnet/landlord.ckpt")
            elif _model_type == "wp":
                LandlordModel.init_model("baselines/douzero_WP/landlord.ckpt")
            elif _model_type == "adp":
                LandlordModel.init_model("baselines/douzero_ADP/landlord.ckpt")
            else:
                LandlordModel.init_model("baselines/sl/landlord.ckpt")
            # AI 初始化
            self.play_order = 0 if self.user_position == "landlord" else 1 if self.user_position == "landlord_up" else 2
            self.LastValidPlayPos = self.play_order
            if self.model_type == "resnet":
                ai_players = [self.user_position,
                              DeepAgent(self.user_position, self.card_play_model_path_dict[self.user_position])]
            elif self.model_type == "wp":
                ai_players = [self.user_position,
                              DeepAgent(self.user_position, self.card_play_wp_model_path[self.user_position])]
            elif self.model_type == "adp":
                ai_players = [self.user_position,
                              DeepAgent(self.user_position, self.card_play_adp_model_path[self.user_position])]
            else:
                ai_players = [self.user_position,
                              DeepAgent(self.user_position, self.card_play_model_path_dict[self.user_position])]

            self.env = GameEnv(ai_players, None)

        except Exception as e:
            return "Error {0}".format(str(e))
        self.GameRecord.clear()
        self.env.card_play_init(self.card_play_data_list)
        print("info: " + self.card_play_data_tostr(self.card_play_data_list))
        return 1

    @staticmethod
    def real_to_env(self, cards):
        env_card = [RealCard2EnvCard[c] for c in cards]
        env_card.sort()
        return env_card

    @staticmethod
    def move_type_tostr(move_type):
        mtype = move_type["type"]
        mtype_map = ["", "单张", "对子", "三张", "炸弹", "王炸", "三带一", "三带一对", "顺子", "连对", "飞机", "飞机带单根", "飞机带一对", "四带二", "四带两对",
                     "不是合法牌型"]
        t_str = mtype_map[mtype]
        if "len" in move_type:
            t_str += " 长度: " + str(move_type["len"])
        return t_str

    # 处理其他用户
    def handle_others(self, last_cards, nick):

        self.other_played_cards_real = last_cards
        self.other_played_cards_env = [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
        self.other_played_cards_env.sort()
        cards = self.other_played_cards_real
        # 更新上下家手牌
        if nick == "上家":
            self.upper_played_cards_real = cards
        else:
            self.lower_played_cards_real = cards
        # 元引擎中为三方游戏，所以需要把三方流程走完
        self.env.step(self.user_position, self.other_played_cards_env)
        self.GameRecord.append(self.other_played_cards_real if self.other_played_cards_real != "" else "Pass")
        # 清理对手牌，更新记牌器
        self.record_cards()

    @staticmethod
    def action_to_str(action):
        if len(action) == 0:
            return "Pass"
        else:
            return "".join([EnvCard2RealCard[card] for card in action])

    def card_play_data_tostr(self, card_play_data):
        s = "---------- 对局信息 ----------\n"
        s += "      地主牌: " + self.action_to_str(card_play_data["three_landlord_cards"]) + "\n" + \
             "    地主手牌: " + self.action_to_str(card_play_data["landlord"]) + "\n" + \
             "地主上家手牌:" + self.action_to_str(card_play_data["landlord_up"]) + "\n" + \
             "地主下家手牌:" + self.action_to_str(card_play_data["landlord_down"])
        s += "\n------------------------------"
        return s

    def record_cards(self):
        try:
            for card in self.other_played_cards_env:
                if card in self.other_hand_cards:
                    self.other_hand_cards.remove(card)
        except ValueError as e:
            traceback.print_exc()

    # 第一次启动
    def prepare_start(self):
        first_run = True
        action_message, action_list = self.env.step(self.user_position)
        if first_run:
            self.initial_model_rate = round(float(action_message["win_rate"]), 3)  # win_rate at start
            first_run = False

        hand_cards_str = ''.join(
            [EnvCard2RealCard[c] for c in self.env.info_sets[self.user_position].player_hand_cards])
        print("出牌:", action_message["action"] if action_message["action"] else "Pass", "| 得分:",
              round(action_message["win_rate"], 3), "| 剩余手牌:", hand_cards_str)
        play = action_message["action"] if action_message["action"] else "Pass"
        win_rate = action_message["win_rate"] if action_message["win_rate"] else 0
        self.GameRecord.append(action_message["action"] if action_message["action"] != "" else "Pass")
        res = {"action": play, "win_rate": win_rate}
        return res

    def play_one_poke(self, user_position_code):
        index = int(user_position_code)
        self.user_position = ['landlord_up', 'landlord', 'landlord_down'][index]
        action_message, action_list = self.env.step(self.user_position)
        play = action_message["action"] if action_message["action"] else "Pass"
        win_rate = action_message["win_rate"] if action_message["win_rate"] else 0
        res = {"action": play, "win_rate": round(win_rate,3)}
        self.GameRecord.append(action_message["action"] if action_message["action"] != "" else "Pass")
        return res

    # 判断是否明牌， is_farmer = false , 表示地主
    def judge_if_mingpai(self, cards_str, three_cards, user_position_code, is_farmer):
        landlord_requirement = manual_mingpai_requirements(cards_str)
        if landlord_requirement:
            if is_farmer == "0":
                index = int(user_position_code)
                user_position = ['up', 'landlord', 'down'][index]
                initial_bid_rate = FarmerModel.predict(cards_str, user_position)
                # (6, 1.2)
                jia_bei_threshold = self.FarmerJiabeiThreshold
                if initial_bid_rate > jia_bei_threshold[0]:
                    result = {'is_farmer': is_farmer, 'result': 1, 'code': 0, 'win_rate': round(initial_bid_rate, 3)}
                else:
                    result = {'is_farmer': is_farmer, 'result': 0, 'code': 0, 'win_rate': round(initial_bid_rate, 3)}
            else:
                initial_bid_rate = LandlordModel.predict_by_model(cards_str, three_cards)
                #  (0.5, 0.15)
                jia_bei_threshold = self.JiabeiThreshold[1]
                if initial_bid_rate > jia_bei_threshold[1]:
                    result = {'is_farmer': is_farmer, 'result': 1, 'code': 0, 'win_rate': round(initial_bid_rate, 3)}
                else:
                    result = {'is_farmer': is_farmer, 'result': 0, 'code': 0, 'win_rate': round(initial_bid_rate, 3)}
        else:
            result = {'is_farmer': is_farmer, 'result': 0, 'code': 0, 'win_rate': 0.001}

        return result

    # # 叫地主类型：1， 首叫；2，抢地主
    def judge_if_jiaodizhu(self, cards_str, jiao_dizhu_type):
        have_bid = False
        if jiao_dizhu_type == 1:
            have_bid = True
        if have_bid:
            threshold_index = 1
        else:
            threshold_index = 2

        landlord_requirement = manual_landlord_requirements(cards_str)
        if landlord_requirement:
            if self.initial_bid_rate == 0:
                win_rate = BidModel.predict_score(cards_str)
            else:
                win_rate = self.initial_bid_rate
            if self.initial_farmer_rate == 0:
                farmer_score = FarmerModel.predict(cards_str, "farmer")
            else:
                farmer_score = self.initial_farmer_rate

            compare_win_rate = win_rate
            if compare_win_rate > 0:
                compare_win_rate *= 2.5
            if win_rate > self.BidThresholds[threshold_index] and compare_win_rate > farmer_score:
                return {'result': 1, 'farmer_score': round(farmer_score, 3), 'landlord_score': round(win_rate, 3)}
        return {'result': 0, 'farmer_score': round(farmer_score, 3), 'landlord_score': round(win_rate, 3)}

    def eval_poke_score(self, cards_str, three_cards, user_position_code, is_farmer):
        if is_farmer == "0":
            index = int(user_position_code)
            user_position = ['up', 'landlord', 'down'][index]
            result = FarmerModel.predict(cards_str, user_position)
        else:
            result = LandlordModel.predict_by_model(cards_str, three_cards)

        return round(result, 3)

    # 叫地主类型：1， 首叫；2，抢地主
    def judge_if_jiabei(self, cards_str, three_cards, user_position_code, is_farmer, jiao_dizhu_type):
        is_stolen = 0
        if jiao_dizhu_type == 2:
            is_stolen = 1

        if is_farmer == "0":
            index = int(user_position_code)
            user_position = ['up', 'landlord', 'down'][index]
            initial_bid_rate = FarmerModel.predict(cards_str, user_position)
            # (6, 1.2)
            jia_bei_threshold = self.FarmerJiabeiThreshold
            if initial_bid_rate > jia_bei_threshold[is_stolen]:
                result = {'is_farmer': is_farmer, 'result': 1, 'code': 0, 'win_rate': round(initial_bid_rate, 3)}
            else:
                result = {'is_farmer': is_farmer, 'result': 0, 'code': 0, 'win_rate': round(initial_bid_rate, 3)}
        else:
            initial_bid_rate = LandlordModel.predict_by_model(cards_str, three_cards)
            #  (0.5, 0.15)
            jia_bei_threshold = self.JiabeiThreshold[1]
            if initial_bid_rate > jia_bei_threshold[1]:
                result = {'is_farmer': is_farmer, 'result': 1, 'code': 0, 'win_rate': round(initial_bid_rate, 3)}
            else:
                result = {'is_farmer': is_farmer, 'result': 0, 'code': 0, 'win_rate': round(initial_bid_rate, 3)}
        return result

    def reset_my_hand_card(self, user_position_code, my_hand_cards_real):
        # reset user_hand_cards
        user_hand_cards_env = [RealCard2EnvCard[c] for c in list(my_hand_cards_real)]
        index = int(user_position_code)
        user_position = ['up', 'landlord', 'down'][index]
        self.env.info_sets[user_position].player_hand_cards = user_hand_cards_env
        # reset played cards
        my_played_cards = list(self.env.played_cards[user_position])
        for exist_card in user_hand_cards_env:
            if exist_card in my_played_cards:
                my_played_cards.remove(exist_card)
        return self.env.info_sets[user_position].player_hand_cards
