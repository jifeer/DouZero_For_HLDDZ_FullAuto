# -*- coding: utf-8 -*-
import logging
import traceback
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fuzhu import douFacade
from fuzhu.douFacade import DouFacade
# 过滤掉警示信息
import warnings

warnings.filterwarnings("ignore")

portal = FastAPI()

douFacadeAry = {}

# encode_html_chars=True to encode < > & as unicode escape sequences.
@portal.get('/')
async def hello_world():
    return JSONResponse({'msg': "", 'result': "Succeed to connect AI server", 'code': 0})


@portal.get('/manual_landlord_requirements/<cards_str>')
async def manual_landlord_requirements(request: Request):
    result = douFacade.manual_landlord_requirements(request.query_params.get('cards_str'))

    return JSONResponse({'cards_str': request.query_params.get('cards_str'), 'result': result, 'code': 0})


@portal.get('/manual_mingpai_requirements/<cards_str>')
async def manual_mingpai_requirements(request: Request):
    result = douFacade.manual_mingpai_requirements(request.query_params.get('cards_str'))
    return JSONResponse({'cards_str': request.query_params.get('cards_str'), 'result': result, 'code': 0})


@portal.get('/poke/init_cards')
async def init_cards(request: Request):
    ld_num = request.query_params.get('ld_num')
    print("################################ 模拟器【", ld_num, "】初始化卡牌 ")
    try:
        user_hand_cards_real = request.query_params.get('user_hand_cards_real')
        three_landlord_cards_real = request.query_params.get('three_landlord_cards_real')
        user_position_code = int(request.query_params.get('user_position_code'))
        model_type = request.query_params.get('model_type')

        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            raise Exception("dou_facde_inst 尚未初始化!", ld_num)

        if user_position_code == "1":
            # 说明玩家本人是地主
            if len(three_landlord_cards_real) < 3:
                three_landlord_cards_real = user_hand_cards_real[:3]

        result = dou_facade_inst.init_cards(user_hand_cards_real, three_landlord_cards_real, user_position_code,
                                            model_type)
        return JSONResponse({'user_position_code': user_position_code, 'result': result, 'code': 0})
    except Exception as e:
        res = "Error {0}".format(traceback.format_exc())
        logging.error(f"######模拟器【{ld_num}], error info: {res}")
    return JSONResponse({'result': res, 'msg': "处理失败"})


@portal.get('/poke/handle_others')
async def handle_others(request: Request):
    ld_num = request.query_params.get('ld_num')
    nick = ""
    try:
        last_cards = request.query_params.get('last_cards')
        # 确定AI工作逻辑的关键参数
        user_position_code = request.query_params.get('user_position_code')
        # 对于“我”来讲，上家和下家的区分
        other_user_pos = request.query_params.get('other_user_pos')
        print("################################ 模拟器【", ld_num, "】出牌人： ", other_user_pos, " : 出牌：", last_cards)
        # 这里的“我”位置始终为0， 1是右侧玩家，2是左侧玩家
        if other_user_pos == "1":
            nick = "上家"
        elif other_user_pos == "3":
            nick = "下家"

        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            raise Exception("dou_facde_inst 尚未初始化!", ld_num)
        server_current_pos = dou_facade_inst.play_order_queue.get()
        if server_current_pos != int(other_user_pos):
            print("!!!!!!!!!!Error: 当前应该执行的玩家是：", server_current_pos)
        dou_facade_inst.handle_others(last_cards, nick, user_position_code, other_user_pos)
        dou_facade_inst.play_order_queue.put(server_current_pos)
        return JSONResponse({'nick': nick, 'msg': "Succeed to deal with workflow", 'code': 0})
    except Exception as e:
        res = "Error {0}".format(traceback.format_exc())
        logging.error(f"######模拟器【{ld_num}], error info: {res}")
    return JSONResponse({'nick': nick, 'result': res, 'msg': "处理失败"})


@portal.get('/poke/replay')
async def prepare_start(request: Request):
    ld_num = request.query_params.get('ld_num')
    try:
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            raise Exception("dou_facde_inst 尚未初始化!", ld_num)
        result = dou_facade_inst.prepare_start()
        return JSONResponse({'code': 0, 'result': result, 'request_id': "prepare_start"})
    except Exception as e:
        msg = "Error {0}".format(traceback.format_exc())
        logging.error(f"######模拟器【{ld_num}], error info: {msg}")
    return JSONResponse({'code': 1, 'result': msg, 'request_id': "prepare_start"})


@portal.get('/poke/play')
async def play_one_poke(request: Request):
    ld_num = request.query_params.get('ld_num')
    try:
        user_position_code = request.query_params.get('user_position_code')
        desk_user_pos = request.query_params.get('other_user_pos')
        # TODO：确定是否及如何更新牌
        cards_str = request.query_params.get('cards_str')
        print("################################ 模拟器【", ld_num, "】出牌人： 本人-", desk_user_pos)
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            raise Exception("dou_facde_inst 尚未初始化!", ld_num)

        server_current_pos = dou_facade_inst.play_order_queue.get()
        if server_current_pos != int(desk_user_pos):
            print("!!!!!!!!!!Error: 当前应该执行的玩家是：", server_current_pos)
        result = dou_facade_inst.play_one_poke(user_position_code)
        action = result.get("action")
        if action == "Pass":
            action = ""
        print("#########################################")
        dou_facade_inst.play_order_queue.put(server_current_pos)
        return JSONResponse(
            {'winRate': result.get("win_rate"), 'action': action, 'code': 0, 'hands_pokes': result.get("hands_pokes")})
    except Exception as e:
        msg = "Error {0}".format(traceback.format_exc())
        logging.error(f"######模拟器【{ld_num}], error info: {msg}")
    return JSONResponse({'code': 1, 'result': msg, 'request_id': "play_one_poke"}, escape_forward_slashes=False)


@portal.get('/poke/judge_if_mingpai')
async def judge_if_mingpai(request: Request):
    ld_num = request.query_params.get('ld_num')
    try:
        user_position_code = request.query_params.get('user_position_code')
        cards_str = request.query_params.get('user_hand_cards_real')
        three_cards = request.query_params.get('three_landlord_cards_real')
        is_farmer = request.query_params.get('is_farmer')
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            raise Exception("dou_facde_inst 尚未初始化!", ld_num)

        result = dou_facade_inst.judge_if_mingpai(cards_str, three_cards, user_position_code, is_farmer)
        return JSONResponse({'is_farmer': is_farmer, 'result': result, 'code': 0})
    except Exception as e:
        msg = "Error {0}".format(traceback.format_exc())
        logging.error(f"######模拟器【{ld_num}], error info: {msg}")
    return JSONResponse({'code': 1, 'result': msg, 'request_id': "judge_if_mingpai"})


@portal.get('/poke/judge_if_jiaodizhu')
async def judge_if_jiaodizhu(request: Request):
    ld_num = request.query_params.get('ld_num')
    try:
        user_position_code = request.query_params.get('user_position_code')
        cards_str = request.query_params.get('user_hand_cards_real')
        jiao_dizhu_type = request.query_params.get('jiao_dizhu_type')
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            raise Exception("dou_facde_inst 尚未初始化!", ld_num)

        result = dou_facade_inst.judge_if_jiaodizhu(cards_str, jiao_dizhu_type)
        return JSONResponse({'user_position_code': user_position_code, 'result': result.get("result"), 'landlord_score': result.get("landlord_score"), 'farmer_score': result.get("farmer_score"), 'code': 0})
    except Exception as e:
        msg = "Error {0}".format(traceback.format_exc())
        logging.error(f"######模拟器【{ld_num}], error info: {msg}")
    return JSONResponse({'code': 1, 'result': msg, 'msg': "judge_if_jiaodizhu"})


@portal.get('/poke/eval_poke_score')
async def eval_poke_score(request: Request):
    ld_num = request.query_params.get('ld_num')
    try:
        user_position_code = request.query_params.get('user_position_code')
        cards_str = request.query_params.get('user_hand_cards_real')
        three_cards = request.query_params.get('three_landlord_cards_real')
        is_farmer = request.query_params.get('is_farmer')
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            raise Exception("dou_facde_inst 尚未初始化!", ld_num)

        result = dou_facade_inst.eval_poke_score(cards_str, three_cards, user_position_code, is_farmer)
        return JSONResponse({'user_position_code': user_position_code, 'win_rate': result, 'code': 0})
    except Exception as e:
        msg = "Error {0}".format(traceback.format_exc())
        logging.error(f"######模拟器【{ld_num}], error info: {msg}")
    return JSONResponse({'code': 1, 'result': msg, 'msg': "eval_poke_score"})


@portal.get('/poke/judge_if_jiabei')
async def judge_if_jiabei(request: Request):
    ld_num = request.query_params.get('ld_num')
    try:
        user_position_code = request.query_params.get('user_position_code')
        cards_str = request.query_params.get('user_hand_cards_real')
        three_cards = request.query_params.get('three_landlord_cards_real')
        is_farmer = request.query_params.get('is_farmer')
        jiao_dizhu_type = request.query_params.get('jiao_dizhu_type')
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            raise Exception("dou_facde_inst 尚未初始化!", ld_num)

        print("cards_str=" + cards_str)
        result = dou_facade_inst.judge_if_jiabei(cards_str, three_cards, user_position_code, is_farmer, jiao_dizhu_type)
        return JSONResponse(result)
    except Exception as e:
        msg = "Error {0}".format(traceback.format_exc())
        logging.error(f"######模拟器【{ld_num}], error info: {msg}")
    return JSONResponse({'code': 1, 'result': msg, 'msg': "judge_if_jiabei"})


@portal.get('/poke/reset_hands_cards')
async def reset_hands_cards(request: Request):
    ld_num = request.query_params.get('ld_num')
    print("ld_num", ld_num)
    try:
        user_position_code = request.query_params.get("user_position_code")
        cards_str = request.query_params.get("user_hand_cards_real")
        three_cards = request.query_params.get("three_landlord_cards_real")
        if ld_num in douFacadeAry:
            dou_facade_inst = douFacadeAry[ld_num]
        else:
            raise Exception("dou_facde_inst 尚未初始化!", ld_num)

        # result = dou_facade_inst.reset_my_hand_card(user_position_code, cards_str)
        return JSONResponse({'code': 0, 'result': 1, 'msg': "reset_hands_cards", "ld_num": ld_num})
    except Exception as e:
        msg = "Error {0}".format(traceback.format_exc())
        logging.error(f"######模拟器【{ld_num}], error info: {msg}")
        return JSONResponse({'code': 1, 'result': 0, 'msg': msg})


@portal.get('/poke/init_ai_model')
async def init_ai_model(request: Request):
    ld_num = request.query_params.get('ld_num')
    try:
        model_type = request.query_params.get('model_type')
        dou_facade_inst = DouFacade()
        douFacadeAry[ld_num] = dou_facade_inst
        result = dou_facade_inst.init_ai_model(model_type)
        return JSONResponse({'result': result, 'code': 0})
    except Exception as e:
        msg = "Error {0}".format(traceback.format_exc())
        logging.error(f"######模拟器【{ld_num}], error info: {msg}")
    return JSONResponse({'code': 1, 'result': msg, 'request_id': "judge_if_mingpai"})


if __name__ == '__main__':
    import sys
    import io
    import colorama
    import multiprocessing
    # 下面这句必须在if下面添加
    multiprocessing.freeze_support()

    args = sys.argv
    print(args)
    # ['test.py', 'my.txt', '/home/charles', '/home/charles/target']
    monitorId = 0
    try:
        if len(args) > 1:
            monitorId = int(args[1].strip())
            print("monite id is not null: ", monitorId)
        if monitorId:
            print("18000 + monitorId ")
            port = int(18000) + monitorId
        else:
            port = 18003
        print(" port is %d", port)
        # 改变标准输出的默认编码
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
        colorama.init(autoreset=True)

        uvicorn.run(app='portal:portal', host="127.0.0.1", port=port, reload=True, limit_concurrency=500)

    except Exception as e:
        msg = "Error {0}".format(traceback.format_exc())
        logging.error(f" error info: {msg}")
