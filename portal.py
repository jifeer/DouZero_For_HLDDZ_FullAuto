# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import jsonify
import douFacade
from douFacade import DouFacade

portal = Flask(__name__)

douFacadeAry = {}


@portal.route('/')
def hello_world():
    return jsonify({'msg': "", 'result': "Succeed to connect AI server", 'code': 0})


@portal.route('/manual_landlord_requirements/<cards_str>')
def manual_landlord_requirements(cards_str):

    result = douFacade.manual_landlord_requirements(cards_str)

    return jsonify({'cards_str': cards_str, 'result': result, 'code': 0})


@portal.route('/manual_mingpai_requirements/<cards_str>')
def manual_mingpai_requirements(cards_str):
    result = douFacade.manual_mingpai_requirements(cards_str)
    return jsonify({'cards_str': cards_str, 'result': result, 'code': 0})


@portal.route('/poke/init_cards')
def init_cards():
    user_hand_cards_real = request.values.get("user_hand_cards_real")
    three_landlord_cards_real = request.values.get("three_landlord_cards_real")
    user_position_code = int(request.values.get("user_position_code"))
    model_type = request.values.get("model_type")
    ld_num = request.values.get("ld_num")
    if ld_num in douFacadeAry:
        dou_facade_inst = douFacadeAry[ld_num]
    else:
        dou_facade_inst = DouFacade()
        douFacadeAry[ld_num] = dou_facade_inst
    if user_position_code == "1":
        # 说明玩家本人是地主
        if three_landlord_cards_real == "":
            three_landlord_cards_real = user_hand_cards_real[:3]

    result = dou_facade_inst.init_cards(user_hand_cards_real, three_landlord_cards_real, user_position_code, model_type)
    return jsonify({'user_position_code': user_position_code, 'result': result, 'code': 0})


@portal.route('/poke/handle_others')
def handle_others():
    result = ""
    nick = ""
    try:
        last_cards = request.values.get("last_cards")
        ld_num = request.values.get("ld_num")
        # 确定AI工作逻辑的关键参数
        # user_position_code = request.values.get("user_position_code")
        # 对于“我”来讲，上家和下家的区分
        other_user_pos = request.values.get("other_user_pos")
        print("################################ 模拟器【", ld_num, "】出牌人： ", other_user_pos)
        # 这里的“我”位置始终为0， 1是右侧玩家，2是左侧玩家
        if other_user_pos == "1":
            nick = "上家"
        elif other_user_pos == "3":
            nick = "下家"

        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            dou_facade_inst = DouFacade()
            douFacadeAry[ld_num] = dou_facade_inst
        dou_facade_inst.handle_others(last_cards, nick)

    except Exception as e:
        res = "Error {0}".format(str(e))
        return jsonify({'nick': nick, 'result': res, 'msg': "处理失败"})
    return jsonify({'nick': nick, 'msg': "Succeed to deal with workflow", 'code': 0})


@portal.route('/poke/replay')
def prepare_start():
    try:
        ld_num = request.values.get("ld_num")
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            dou_facade_inst = DouFacade()
            douFacadeAry[ld_num] = dou_facade_inst
        result = dou_facade_inst.prepare_start()
        return jsonify({'code': 0, 'result': result, 'request_id': "prepare_start"})
    except Exception as e:
        msg = "Error {0}".format(str(e))
        return jsonify({'code': 1, 'result': msg, 'request_id': "prepare_start"})


@portal.route('/poke/play')
def play_one_poke():
    user_position_code = request.values.get("user_position_code")
    # TODO：确定是否及如何更新牌
    cards_str = request.values.get("cards_str")
    ld_num = request.values.get("ld_num")
    print("################################ 模拟器【", ld_num, "】出牌人： ",  "2")
    if ld_num in douFacadeAry:
        dou_facade_inst = douFacadeAry[ld_num]
    else:
        dou_facade_inst = DouFacade()
        douFacadeAry[ld_num] = dou_facade_inst
    result = dou_facade_inst.play_one_poke(user_position_code)
    action = result.get("action")
    if action == "Pass":
        action = ""
    return jsonify({'winRate': result.get("win_rate"), 'action': action, 'code': 0})


@portal.route('/poke/judge_if_mingpai')
def judge_if_mingpai():
    try:
        user_position_code = request.values.get("user_position_code")
        cards_str = request.values.get("user_hand_cards_real")
        three_cards = request.values.get("three_landlord_cards_real")
        is_farmer = request.values.get("is_farmer")
        ld_num = request.values.get("ld_num")
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            dou_facade_inst = DouFacade()
            douFacadeAry[ld_num] = dou_facade_inst
        result = dou_facade_inst.judge_if_mingpai(cards_str, three_cards, user_position_code, is_farmer)
        return jsonify({'is_farmer': is_farmer, 'result': result, 'code': 0})
    except Exception as e:
        msg = "Error {0}".format(str(e))
    return jsonify({'code': 1, 'result': msg, 'request_id': "judge_if_mingpai"})


@portal.route('/poke/judge_if_jiaodizhu')
def judge_if_jiaodizhu():
    user_position_code = request.values.get("user_position_code")
    cards_str = request.values.get("user_hand_cards_real")
    jiao_dizhu_type = request.values.get("jiao_dizhu_type")
    ld_num = request.values.get("ld_num")
    if ld_num in douFacadeAry:
        dou_facade_inst = douFacadeAry[ld_num]
    else:
        dou_facade_inst = DouFacade()
        douFacadeAry[ld_num] = dou_facade_inst
    result = dou_facade_inst.judge_if_jiaodizhu(cards_str, jiao_dizhu_type)
    return jsonify({'user_position_code': user_position_code, 'result': result, 'code': 0})


@portal.route('/poke/eval_poke_score')
def eval_poke_score():
    try:
        user_position_code = request.values.get("user_position_code")
        cards_str = request.values.get("user_hand_cards_real")
        three_cards = request.values.get("three_landlord_cards_real")
        is_farmer = request.values.get("is_farmer")
        jiao_dizhu_type = request.values.get("jiao_dizhu_type")
        ld_num = request.values.get("ld_num")
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            dou_facade_inst = DouFacade()
            douFacadeAry[ld_num] = dou_facade_inst
        result = dou_facade_inst.eval_poke_score(cards_str, three_cards, user_position_code, is_farmer, jiao_dizhu_type)
        return jsonify({'user_position_code': user_position_code, 'win_rate': result, 'code': 0})
    except Exception as e:
        msg = "Error {0}".format(str(e))
    return jsonify({'code': 1, 'result': msg, 'msg': "eval_poke_score"})


@portal.route('/poke/judge_if_jiabei')
def judge_if_jiabei():
    try:
        user_position_code = request.values.get("user_position_code")
        cards_str = request.values.get("user_hand_cards_real")
        three_cards = request.values.get("three_landlord_cards_real")
        is_farmer = request.values.get("is_farmer")
        jiao_dizhu_type = request.values.get("jiao_dizhu_type")
        ld_num = request.values.get("ld_num")
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            dou_facade_inst = DouFacade()
            douFacadeAry[ld_num] = dou_facade_inst

        result = dou_facade_inst.judge_if_jiabei(cards_str, three_cards, user_position_code, is_farmer, jiao_dizhu_type)
        return jsonify(result)
    except Exception as e:
        msg = "Error {0}".format(str(e))
    return jsonify({'code': 1, 'result': msg, 'msg': "judge_if_jiabei"})


if __name__ == '__main__':
    portal.run()
