from base import board
from base import player
# import board
# import player
import random
import operator
import math

player_04 = player.Player("TheNoob", 0)

def action(board, arr_player):
    return turn(board, player_04)

def turn(board, player_04):
    # list các thẻ
    list_the_lay_ngay = list_the_lay_ngay_func(board)
    # list các sub_list, các sub_list chứa các sub_sub_list (list cấp 3)
    mau_the_quan_trong = mau_the_quan_trong_func(board)
    # list các dictionary, mỗi dictionary chứa 2 keys là thẻ và nguyên liệu thiếu
    list_the_co_the_lay = list_the_co_the_lay_func(board, mau_the_quan_trong)
    # Chia trường hợp
    # Có thể lấy được thẻ
    if len(list_the_lay_ngay) != 0:
        # Kiểm tra xem có thẻ màu quan trọng không
        # Trả về dictionary chứa một biến True/False và một biến chứa thẻ nếu biến ban đầu là True
        check_the_mau_quan_trong = check_the_mau_quan_trong_func(list_the_lay_ngay, mau_the_quan_trong)
        if check_the_mau_quan_trong["TF"] == True:
            return player_04.getCard(check_the_mau_quan_trong["Card"], board)
        # Nếu không có màu thẻ quan trọng thì lấy thẻ có giá trị cao nhất khác 0
        check_the_gia_tri_cao =  check_the_gia_tri_cao_func(list_the_lay_ngay)
        if check_the_gia_tri_cao["TF"] == True:
            return player_04.getCard(check_the_gia_tri_cao["Card"], board)
        # Nếu không có thẻ quan trọng, cũng không có thẻ có điểm thì thực hiện khối lệnh phía dưới
    # Nếu list thẻ có thể lấy không rỗng
    temp = ["red", "blue", "green", "black", "white"]
    if len(list_the_co_the_lay) != 0:
        list_nguyen_lieu_lay = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "white": 0,
            "black": 0                
        }
        list_mau_nguyen_lieu_can_lay = []
        for i in range(len(list_the_co_the_lay)):
            muc_tieu = list_the_co_the_lay[i]
            # Nếu thẻ mục tiêu cần vàng
            if muc_tieu["Need_more"]["auto_color"] == 1 and board.stocks["auto_color"] != 0 and tim_kiem(muc_tieu["Card"], player_04.card_upside_down) == False and len(player_04.card_upside_down) <= 2:
                # Có thể lựa chọn úp thẻ này, tìm dict trả
                dict_tra = {
                    "red": 0,
                    "blue": 0,
                    "green": 0,
                    "white": 0,
                    "black": 0
                }
                if sum(player_04.stocks.values()) == 10: # Cần trả 1
                    nguyen_lieu_du = {
                        "red": 0,
                        "blue": 0,
                        "green": 0,
                        "white": 0,
                        "black": 0
                    }
                    for mau in temp:
                        if player_04.stocks_const[mau] + player_04.stocks[mau] <= muc_tieu["Need_more"]:
                            nguyen_lieu_du[mau] = 0
                        else:
                            if player_04.stocks[mau] == 0:
                                nguyen_lieu_du[mau] = 0
                            else:
                                nguyen_lieu_du[mau] = player_04.stocks_const[mau] + player_04.stocks[mau] - muc_tieu["Need_more"]
                    for mau in nguyen_lieu_du.keys():
                        if nguyen_lieu_du[mau] != 0:
                            dict_tra[mau] == 1
                            break
                return player_04.getUpsideDown(muc_tieu["Card"], board, dict_tra)
            # Nếu không thể lấy thẻ vàng hoặc không thể úp thẻ nữa, hoặc mục tiêu không cần thẻ vàng
            else:
                # Nếu mục tiêu chỉ thiếu duy nhất một thẻ vàng:
                if sum(muc_tieu["Need_more"].values()) == 1 and muc_tieu["Need_more"]["auto_color"] == 1:
                    continue
                # Nếu không thì lấy các nguyên liệu như bình thường, cho đến khi xây dựng được 3 nguyên liệu cần lấy
                for mau in temp:
                    if muc_tieu["Need_more"][mau] != 0:
                        list_mau_nguyen_lieu_can_lay.append(mau)
                        list_nguyen_lieu_lay[mau] = muc_tieu["Need_more"][mau]
                # Nếu đã có 3 màu cần lấy thì lấy luôn
                if len(list_mau_nguyen_lieu_can_lay) >= 3:
                    # Tìm số lượng trả
                    dict_tra = {
                        "red": 0,
                        "blue": 0,
                        "green": 0,
                        "white": 0,
                        "black": 0
                    }
                    so_luong_tra = sum(player_04.stocks.values()) + 3 - 10
                    if so_luong_tra > 0:
                        nguyen_lieu_du = {
                            "red": 0,
                            "blue": 0,
                            "green": 0,
                            "white": 0,
                            "black": 0
                        }
                        for mau in temp:
                            if player_04.stocks_const[mau] + player_04.stocks[mau] <= muc_tieu["Need_more"]:
                                nguyen_lieu_du[mau] = 0
                            else:
                                if player_04.stocks[mau] == 0:
                                    nguyen_lieu_du[mau] = 0
                                else:
                                    nguyen_lieu_du[mau] = player_04.stocks_const[mau] + player_04.stocks[mau] - muc_tieu["Need_more"]
                        #
                        for i in range(so_luong_tra):
                            for mau in temp:
                                if nguyen_lieu_du[mau] != 0:
                                    dict_tra[mau] += 1
                                    nguyen_lieu_du[mau] -= 1
                                    break
                    #
                    return player_04.getThreeStocks(list_mau_nguyen_lieu_can_lay[0], list_mau_nguyen_lieu_can_lay[1], list_mau_nguyen_lieu_can_lay[2], board, dict_tra)
                # Nếu chỉ có 2 màu cần lấy, check xem có lấy được 1 loại 2 màu hay không, nếu không thì lấy thêm 1 màu bất kì nữa hoặc chỉ lấy 2 loại
                if len (list_mau_nguyen_lieu_can_lay) == 2:
                    for mau in list_mau_nguyen_lieu_can_lay:
                        # Có thể lấy được 2 màu 1 loại
                        if list_nguyen_lieu_lay[mau] >= 2 and player_04.checkOneStock(board, mau) == True:
                            # Có thể lấy được 2, tìm dict trả
                            dict_tra = {
                                "red": 0,
                                "blue": 0,
                                "green": 0,
                                "white": 0,
                                "black": 0
                            }
                            so_luong_tra = sum(player_04.stocks.values()) + 2 - 10
                            if so_luong_tra > 0:
                                nguyen_lieu_du = {
                                    "red": 0,
                                    "blue": 0,
                                    "green": 0,
                                    "white": 0,
                                    "black": 0
                                }
                                for mau1 in temp:
                                    if player_04.stocks_const[mau1] + player_04.stocks[mau1] <= muc_tieu["Need_more"]:
                                        nguyen_lieu_du[mau1] = 0
                                    else:
                                        if player_04.stocks[mau1] == 0:
                                            nguyen_lieu_du[mau1] = 0
                                        else:
                                            nguyen_lieu_du[mau1] = player_04.stocks_const[mau1] + player_04.stocks[mau1] - muc_tieu["Need_more"]
                                #
                                for i in range(so_luong_tra):
                                    for mau1 in temp:
                                        if nguyen_lieu_du[mau1] != 0:
                                            dict_tra[mau1] += 1
                                            nguyen_lieu_du[mau1] -= 1
                                            break
                            return player_04.getOneStock(mau, board, dict_tra)
                    # Không thể lấy 2 màu 1 loại thì lấy 2 loại mỗi loại 1 màu
                    # Nếu số nguyên liệu không quá 7
                    if sum(player_04.stocks.values()) <= 7:
                        # Lấy được 3 thẻ mà không cần trả lại
                        color3 = None
                        for mau in temp:
                            if tim_kiem(mau, list_mau_nguyen_lieu_can_lay) == False and board.stocks[mau] != 0:
                                color3 = mau
                        if color3 != None:
                            return player_04.getThreeStocks(list_mau_nguyen_lieu_can_lay[0], list_mau_nguyen_lieu_can_lay[1], color3, board, {})
                        # Nếu trên bàn chỉ còn đúng 2 loại nguyên liệu này:
                        else:
                            return player_04.getOneTwoStock(list_mau_nguyen_lieu_can_lay[0], list_mau_nguyen_lieu_can_lay[1], board, {})
                    else:
                        # Chỉ lấy 2 loại nguyên liệu này
                        dict_tra = {
                            "red": 0,
                            "blue": 0,
                            "green": 0,
                            "white": 0,
                            "black": 0
                        }
                        so_luong_tra = sum(player_04.stocks.values()) + 2 - 10
                        if so_luong_tra > 0:
                            nguyen_lieu_du = {
                                "red": 0,
                                "blue": 0,
                                "green": 0,
                                "white": 0,
                                "black": 0
                            }
                            for mau in temp:
                                if player_04.stocks_const[mau] + player_04.stocks[mau] <= muc_tieu["Need_more"]:
                                    nguyen_lieu_du[mau] = 0
                                else:
                                    if player_04.stocks[mau] == 0:
                                        nguyen_lieu_du[mau] = 0
                                    else:
                                        nguyen_lieu_du[mau] = player_04.stocks_const[mau] + player_04.stocks[mau] - muc_tieu["Need_more"]
                            #
                            for i in range(so_luong_tra):
                                for mau in temp:
                                    if nguyen_lieu_du[mau] != 0:
                                        dict_tra[mau] += 1
                                        nguyen_lieu_du[mau] -= 1
                                        break
                        return player_04.getOneTwoStock(list_mau_nguyen_lieu_can_lay[0], list_mau_nguyen_lieu_can_lay[1], board, dict_tra)
                # Nếu chi có 1 loại màu cần lấy
                if len(list_mau_nguyen_lieu_can_lay) == 1:
                    # if list_nguyen_lieu_lay[list_mau_nguyen_lieu_can_lay[0]] >= 2 and player_04.checkOneStock(board, list_mau_nguyen_lieu_can_lay[0]) == True:
                    #     # Có thể lấy được 2, tìm dict trả
                    #     dict_tra = {
                    #         "red": 0,
                    #         "blue": 0,
                    #         "green": 0,
                    #         "white": 0,
                    #         "black": 0
                    #     }
                    #     so_luong_tra = sum(player_04.stocks.values()) + 2 - 10
                    #     if so_luong_tra > 0:
                    #         nguyen_lieu_du = {
                    #             "red": 0,
                    #             "blue": 0,
                    #             "green": 0,
                    #             "white": 0,
                    #             "black": 0
                    #         }
                    #         for mau in temp:
                    #             if player_04.stocks_const[mau] + player_04.stocks[mau] <= muc_tieu["Need_more"]:
                    #                 nguyen_lieu_du[mau] = 0
                    #             else:
                    #                 if player_04.stocks[mau] == 0:
                    #                     nguyen_lieu_du[mau] = 0
                    #                 else:
                    #                     nguyen_lieu_du[mau] = player_04.stocks_const[mau] + player_04.stocks[mau] - muc_tieu["Need_more"]
                    #         #
                    #         for i in range(so_luong_tra):
                    #             for mau in temp:
                    #                 if nguyen_lieu_du[mau] != 0:
                    #                     dict_tra[mau] += 1
                    #                     nguyen_lieu_du[mau] -= 1
                    #                     break
                    #     print("Return 9")
                    #     return player_04.getOneStock(mau, board, dict_tra)
                    # Không thể lấy được 2 màu 1 loại
                    # Lấy 1 loại rồi lấy thêm ngẫu nhiên 2 loại nữa, không lấy thừa
                    color2 = ""
                    color3 = ""
                    for mau in temp:
                        if mau != list_mau_nguyen_lieu_can_lay[0] and board.stocks[mau] != 0:
                            color2 = mau
                    for mau in temp:
                        if mau != color2 and mau != list_mau_nguyen_lieu_can_lay[0] and board.stocks[mau] != 0:
                            color3 = mau
                    # Nếu số nguyên liệu hiện có không quá 7:
                    if sum(player_04.stocks.values()) <= 7:
                        if color3 != "":
                            return player_04.getThreeStocks(list_mau_nguyen_lieu_can_lay[0], color2, color3, board, {})
                        else:
                            return player_04.getOneTwoStock(list_mau_nguyen_lieu_can_lay[0], color2, board, {})
                    elif sum(player_04.stocks.values()) == 8:
                        return player_04.getOneTwoStock(list_mau_nguyen_lieu_can_lay[0], color2, board, {})
                    elif sum(player_04.stocks.values()) == 9:
                        return player_04.getOneTwoStock(list_mau_nguyen_lieu_can_lay[0], "", board, {})
                    else:
                        dict_tra = {
                            "red": 0,
                            "blue": 0,
                            "green": 0,
                            "white": 0,
                            "black": 0
                        }
                        nguyen_lieu_du = {
                            "red": 0,
                            "blue": 0,
                            "green": 0,
                            "white": 0,
                            "black": 0
                        }
                        for mau in temp:
                            if player_04.stocks_const[mau] + player_04.stocks[mau] <= muc_tieu["Need_more"]:
                                nguyen_lieu_du[mau] = 0
                            else:
                                if player_04.stocks[mau] == 0:
                                    nguyen_lieu_du[mau] = 0
                                else:
                                    nguyen_lieu_du[mau] = player_04.stocks_const[mau] + player_04.stocks[mau] - muc_tieu["Need_more"]
                        for mau in nguyen_lieu_du.keys():
                            if nguyen_lieu_du[mau] != 0:
                                dict_tra[mau] == 1
                                break
                        return player_04.getOneTwoStock(list_mau_nguyen_lieu_can_lay[0], "", board, dict_tra)
    # List thẻ có thể lấy là rỗng
    # Lấy 3 loại thẻ bất kì
    list_random_color = []
    for mau in temp:
        if board.stocks[mau] != 0:
            list_random_color.append(mau)
    a = 0
    if len(list_random_color) >= 3:
        a = 3
    else:
        a = len(list_random_color)
    if sum(player_04.stocks.values()) <= 7:
        if a == 3:
            return player_04.getThreeStocks(list_random_color[0], list_random_color[1], list_random_color[2], board, {})
        elif a == 2:
            return player_04.getOneTwoStock(list_random_color[0], list_random_color[1], board, {})
        else:
            return player_04.getOneTwoStock(list_random_color[0], "", board, {})
    elif sum(player_04.stocks.values()) == 8:
        if a >= 2:
            return player_04.getOneTwoStock(list_random_color[0], list_random_color[1], board, {})
        else:
            return player_04.getOneTwoStock(list_random_color[0], "", board, {})
    elif sum(player_04.stocks.values()) == 9:
        return player_04.getOneTwoStock(list_random_color[0], "", board, {})
    else:
        return board

def check_the_gia_tri_cao_func(list_the_lay_ngay):
    check_the_gia_tri_cao = {}
    list_gia_tri_the = []
    temp = ["red", "blue", "green", "black", "white"]
    for the in list_the_lay_ngay:
        list_nguyen_lieu_thieu = the.stocks.copy()
        for mau in temp:
            if player_04.stocks_const[mau] >= list_nguyen_lieu_thieu[mau]:
                list_nguyen_lieu_thieu[mau] = 0
            else:
                list_nguyen_lieu_thieu[mau] -= player_04.stocks_const[mau]
        gia_tri_the = float(the.score)/float(1 + sum(list_nguyen_lieu_thieu.values()))
        list_gia_tri_the.append(gia_tri_the)
    gia_tri_max = max(list_gia_tri_the)
    if gia_tri_max == 0.0:
        check_the_gia_tri_cao["TF"] = False
        return check_the_gia_tri_cao
    for i in range(len(list_gia_tri_the)):
        if list_gia_tri_the[i] == gia_tri_max:
            check_the_gia_tri_cao["TF"] = True
            check_the_gia_tri_cao["Card"] = list_the_lay_ngay[i]
            return check_the_gia_tri_cao

def check_the_mau_quan_trong_func(list_the_lay_ngay, mau_the_quan_trong):
    check_the_mau_quan_trong = {}
    mau_quan_trong = ""
    list_quan_trong = []
    c = True
    for sub_list1 in mau_the_quan_trong:
        for sub_list2 in sub_list1:
            for mau in sub_list2:
                for the in list_the_lay_ngay:
                    if the.type_stock == mau:
                        mau_quan_trong = mau
                        c = False
                        break
                if c == False:
                    break
            if c == False:
                break
        if c == False:
            break
    if c == True:
        check_the_mau_quan_trong["TF"] = False
        return check_the_mau_quan_trong
    for the in list_the_lay_ngay:
        if the.type_stock == mau_quan_trong:
            list_quan_trong.append(the)
    # Sắp xếp theo giá trị thẻ (= số điểm / số nguyên liệu tạm thời bỏ ra)
    list_gia_tri_the = []
    temp = ["red", "blue", "green", "black", "white"]
    for the in list_quan_trong:
        list_nguyen_lieu_thieu = the.stocks.copy()
        for mau in temp:
            if player_04.stocks_const[mau] >= list_nguyen_lieu_thieu[mau]:
                list_nguyen_lieu_thieu[mau] = 0
            else:
                list_nguyen_lieu_thieu[mau] -= player_04.stocks_const[mau]
        gia_tri_the = float(the.score)/float(1 + sum(list_nguyen_lieu_thieu.values()))
        list_gia_tri_the.append(gia_tri_the)
    gia_tri_max = max(list_gia_tri_the)
    for i in range(len(list_gia_tri_the)):
        if list_gia_tri_the[i] == gia_tri_max:
            the_max = list_quan_trong[i]
    check_the_mau_quan_trong["TF"] = True
    check_the_mau_quan_trong["Card"] = the_max

    return check_the_mau_quan_trong

def list_the_co_the_lay_func(board, mau_the_quan_trong):
    list_the_co_the_lay = []
    list_card_can_check = []
    for the in player_04.card_upside_down:
        list_card_can_check.append(the)
    temp = ["I", "II", "III"]
    for bac_the in temp:
        for the in board.dict_Card_Stocks_Show[bac_the]:
            list_card_can_check.append(the)
    #
    temp = ["red", "blue", "green", "black", "white"]
    for the in list_card_can_check:
        # Kiểm tra nguyên liệu còn thiếu
        stocks_thieu = the.stocks.copy()
        stocks_thieu["auto_color"] = 0
        for mau in temp:
            if player_04.stocks_const[mau] + player_04.stocks[mau] >= stocks_thieu[mau]:
                stocks_thieu[mau] = 0
            else:
                stocks_thieu[mau] -= (player_04.stocks_const[mau] + player_04.stocks[mau])
        # Nếu có nguyên liệu vàng, cần quyết định sẽ dùng nguyên liệu vàng thay thế cho nguyên liệu nào
            # Nếu có 1 nguyên liệu nào đó bàn chơi không thể đáp ứng => chọn
            # Nếu tất cả nguyên liệu được đáp ứng => chọn nguyên liệu ít dư dả nhất
        if player_04.stocks["auto_color"] != 0:
            a = player_04.stocks["auto_color"]
            for i in range(a):
                # Có thể có nhiều thẻ vàng, khi đó cần kiểm tra xem đã bù đủ thẻ vàng hay chưa
                if sum(stocks_thieu.values()) != 0:
                    loai_mau_thieu = []
                    for mau in temp:
                        if stocks_thieu[mau] != 0:
                            loai_mau_thieu.append(mau)
                    dap_ung = True
                    for mau in loai_mau_thieu:
                        if board.stocks[mau] < stocks_thieu[mau]:
                            dap_ung = False
                            stocks_thieu[mau] -= 1
                            break
                    if dap_ung == True:
                        du_da = {}
                        for mau in loai_mau_thieu:
                            du_da[mau] = board.stocks[mau] - stocks_thieu[mau]
                        mini = min(du_da.values())
                        for mau in loai_mau_thieu:
                            if du_da[mau] == mini:
                                stocks_thieu[mau] -= 1
                                break
        # Nếu thẻ chưa đủ nguyên liệu thì mới xét tiếp
        if sum(stocks_thieu.values()) != 0:
            # Cần kiểm tra xem nếu có 10 nguyên liệu thì có lấy được thẻ hay không
            stocks_vinh_cuu_thieu = the.stocks.copy()
            for mau in temp:
                if player_04.stocks_const[mau] >= stocks_vinh_cuu_thieu[mau]:
                    stocks_vinh_cuu_thieu[mau] = 0
                else:
                    stocks_vinh_cuu_thieu[mau] -= player_04.stocks_const[mau]
            kha_nang = True
            # Kiểm tra về số lượng
            if sum(stocks_vinh_cuu_thieu.values()) > (10 - player_04.stocks["auto_color"]):
                kha_nang = False
            # Kiểm tra về khả năng đáp ứng của ngân hàng
            else:
                nguyen_lieu_ngan_hang_thieu = stocks_thieu.copy()
                for mau in temp:
                    if board.stocks[mau] >= nguyen_lieu_ngan_hang_thieu[mau]:
                        nguyen_lieu_ngan_hang_thieu[mau] = 0
                    else:
                        nguyen_lieu_ngan_hang_thieu[mau] -= board.stocks[mau]
                # Nếu nguyên liệu ngân hàng thiếu > 1 thì False
                if sum(nguyen_lieu_ngan_hang_thieu.values()) > 1:
                    kha_nang = False
                else:
                    # Nếu nguyên liệu ngân hàng thiếu = 1 thì chuyển qua nguyên liệu vàng
                    if sum(nguyen_lieu_ngan_hang_thieu.values()) == 1:
                        if board.stocks["auto_color"] != 0:
                            for mau in temp:
                                if nguyen_lieu_ngan_hang_thieu[mau] != 0:
                                    stocks_thieu[mau] -= 1
                                    stocks_thieu["auto_color"] = 1
                                    break
                        else:
                            kha_nang = False
            # Nếu khả năng là True thì thêm dictionary vào list
            if kha_nang == True:
                obj = {
                    "Card": the,
                    "Need_more": stocks_thieu
                }
                list_the_co_the_lay.append(obj)
    #
    if len(list_the_co_the_lay) == 0:
        return list_the_co_the_lay
    # Đã có list thẻ có thể lấy, giờ cần sắp xếp lại theo thứ tự ưu tiên (màu quan trọng, số lượng)
    list_the_co_the_lay_return = []
    list_the_co_the_lay_copy = list_the_co_the_lay.copy()
    # Đầu tiên là sắp xếp theo màu
    if mau_the_quan_trong != [[[]]]:
        for sub_list1 in mau_the_quan_trong:
            for sub_list2 in sub_list1:
                list_temp = []
                for mau in sub_list2:
                    for obj in list_the_co_the_lay:
                        if obj["Card"].type_stock == mau:
                            list_temp.append(obj)
                            list_the_co_the_lay_copy.remove(obj)
                if len(list_temp) != 0:
                    list_the_co_the_lay_return.append(list_temp)
    # Nếu đã sắp xếp theo màu xong mà vẫn còn
    if len(list_the_co_the_lay_copy) != 0:
        list_temp = []
        for obj in list_the_co_the_lay_copy:
            list_temp.append(obj)
        if len(list_temp) != 0:
            list_the_co_the_lay_return.append(list_temp)
    # Sắp xếp theo số lượng nguyên liệu thiếu trong từng sub_list nhỏ
    list_the_co_the_lay = []
    for sub_list in list_the_co_the_lay_return:
        a = len(sub_list)
        for i in range(a):
            mini = 99
            obj_min = sub_list[0]
            for obj in sub_list:
                if sum(obj["Need_more"].values()) < mini:
                    mini = sum(obj["Need_more"].values())
                    obj_min = obj
            list_the_co_the_lay.append(obj_min)
            sub_list.remove(obj_min)
    #
    return list_the_co_the_lay

def mau_the_quan_trong_func(board):
    mau_the_quan_trong = []
    # Nếu không còn thẻ quý tộc thì cũng chẳng có màu nào là quan trọng
    if len(board.dict_Card_Stocks_Show["Noble"]) == 0:
        return mau_the_quan_trong
    # Nếu còn thẻ quý tộc, tính số lượng biên mỗi màu
    so_luong_bien = {
        "red": 0,
        "blue": 0,
        "green": 0,
        "black": 0,
        "white": 0
    }
    temp = ["red", "blue", "green", "black", "white"]
    for mau in temp:
        maxi = -1
        for the in board.dict_Card_Stocks_Show["Noble"]:
            if the.stocks[mau] > maxi:
                maxi = the.stocks[mau]
        # Nếu số lượng biên là 0 thì bỏ màu đấy
        if maxi == 0:
            del so_luong_bien[mau]
        else:
            so_luong_bien[mau] = maxi
    # Xem có màu nào đạt số lượng biên hay không
    mau_dat_so_luong_bien = []
    for mau in so_luong_bien.keys():
        if player_04.stocks_const[mau] >= so_luong_bien[mau]:
            mau_dat_so_luong_bien.append(mau)
    
    # Chia case theo số lượng màu đạt số lượng biên, xây dựng list các thẻ cần xét và list các màu cần lấy
    mau_can_lay = []
    list_the_can_xet = []
    # Case thứ nhất: không có màu nào đạt số lượng biên
    if len(mau_dat_so_luong_bien) == 0:
        mau_can_lay_1 = []
        list_the_can_xet_1 = []
        for mau in so_luong_bien.keys():
            mau_can_lay_1.append(mau)
        for the in board.dict_Card_Stocks_Show["Noble"]:
            list_the_can_xet_1.append(the)
        mau_can_lay.append(mau_can_lay_1)
        list_the_can_xet.append(list_the_can_xet_1)
    # Case thứ hai: chỉ có một màu đạt số lượng biên
    elif len(mau_dat_so_luong_bien) == 1:
        mau_can_lay_1 = []
        list_the_can_xet_1 = []
        temp_mau = mau_dat_so_luong_bien[0]
        # Xem thẻ nào có chứa màu này
        for the in board.dict_Card_Stocks_Show["Noble"]:
            if the.stocks[temp_mau] != 0:
                list_the_can_xet_1.append(the)
                for mau in the.stocks.keys():
                    if mau != temp_mau and the.stocks[mau] != 0:
                        if tim_kiem(mau, mau_can_lay_1) == False:
                            mau_can_lay_1.append(mau)
        mau_can_lay.append(mau_can_lay_1)
        list_the_can_xet.append(list_the_can_xet_1)
        # Xét các thẻ và các màu còn lại
        # mau_can_lay_2 = []
        # list_the_can_xet_2 = []
        # for mau in so_luong_bien.keys():
        #     if mau != temp_mau and tim_kiem(mau, mau_can_lay_1) == False:
        #         mau_can_lay_2.append(mau)
        # for the in board.dict_Card_Stocks_Show["Noble"]:
        #     if tim_kiem(the, list_the_can_xet_1) == False:
        #         list_the_can_xet_2.append(the)
        # mau_can_lay.append(mau_can_lay_2)
        # list_the_can_xet.append(list_the_can_xet_2)
    # Case thứ ba: có nhiều hơn 1 màu đạt số lượng biên
    else:
        mau_can_lay_1 = []
        list_the_can_xet_1 = []
        # Xem thẻ nào chứa ít nhất 2 màu đạt số lượng biên
        a = len(mau_dat_so_luong_bien)
        for i in range(a):
            mau1 = mau_dat_so_luong_bien[i]
            mau2 = mau_dat_so_luong_bien[(i+1)%a]
            for the in board.dict_Card_Stocks_Show["Noble"]:
                if the.stocks[mau1] != 0 and the.stocks[mau2] != 0:
                    list_the_can_xet_1.append(the)
                    for mau in the.stocks.keys():
                        if mau != mau1 and mau != mau2 and the.stocks[mau] != 0:
                            if tim_kiem(mau, mau_can_lay_1) == False:
                                mau_can_lay_1.append(mau)
        mau_can_lay.append(mau_can_lay_1)
        list_the_can_xet.append(list_the_can_xet_1)
        # Xem trong các thẻ còn lại, có thẻ nào chứa ít nhất 1 màu đạt số lượng biên
        # mau_can_lay_2 = []
        # list_the_can_xet_2 = []
        # for mau in mau_dat_so_luong_bien:
        #     for the in board.dict_Card_Stocks_Show["Noble"]:
        #         if the.stocks[mau] != 0 and tim_kiem(the, list_the_can_xet_1) == False:
        #             if tim_kiem(the, list_the_can_xet_2) == False:
        #                 list_the_can_xet_2.append(the)
        #                 for mau1 in the.stocks.keys():
        #                     if tim_kiem(mau1, mau_dat_so_luong_bien) == False and tim_kiem(mau1, mau_can_lay_1) == False:
        #                         mau_can_lay_2.append(mau)
        # Xét các thẻ và các màu còn lại
        # mau_can_lay_3 = []
        # list_the_can_xet_3 = []
        # for mau in so_luong_bien.keys():
        #     if tim_kiem(mau, mau_dat_so_luong_bien) == False and tim_kiem(mau, mau_can_lay_1) == False and tim_kiem(mau, mau_can_lay_2) == False:
        #         mau_can_lay_3.append(mau)
        # for the in board.dict_Card_Stocks_Show["Noble"]:
        #     if tim_kiem(the, list_the_can_xet_1) == False and tim_kiem(the, list_the_can_xet_2) == False:
        #         list_the_can_xet_3.append(the)
        # mau_can_lay.append(mau_can_lay_3)
        # list_the_can_xet.append(list_the_can_xet_3)
    #
    if len(mau_can_lay) == 0:
        return mau_the_quan_trong
    for i in range(len(mau_can_lay)):
        if len(mau_can_lay[i]) != 0 and len(list_the_can_xet[i]) != 0:
            mau_the_quan_trong.append(mau_the_quan_trong_sub_func(mau_can_lay[i], list_the_can_xet[i]))
    # Sắp xếp một lần nữa theo thứ tự các thẻ còn thiếu để đạt số lượng biên
    for sub_list1 in mau_the_quan_trong:
        for sub_list2 in sub_list1:
            if len(sub_list2) == 1:
                continue
            else:
                for i in range(len(sub_list2)-1):
                    for j in range(len(sub_list2)-i-1):
                        num1 = so_luong_bien[sub_list2[j]] - player_04.stocks_const[sub_list2[j]]
                        num2 = so_luong_bien[sub_list2[j+1]] - player_04.stocks_const[sub_list2[j+1]]
                        if num1 > num2:
                            temp_color = sub_list2[j]
                            sub_list2[j] = sub_list2[j+1]
                            sub_list2[j+1] = temp_color
    #
    return mau_the_quan_trong

def tim_kiem(phan_tu_can_tim, list_tim_kiem):
    for phan_tu in list_tim_kiem:
        if phan_tu == phan_tu_can_tim:
            return True
    #
    return False

def mau_the_quan_trong_sub_func(mau_can_lay, list_the_can_xet):
    mau_the_quan_trong = []
    so_lan_xuat_hien = {}
    # Tính số thẻ có sự hiện diện của màu xét
    for mau in mau_can_lay:
        dem = 0
        for the in list_the_can_xet:
            if the.stocks[mau] != 0:
                dem += 1
        so_lan_xuat_hien[mau] = dem
    # Lập các sub_list và thêm vào list mau_the_quan_trong
    for i in range(len(mau_can_lay)):
        if len(so_lan_xuat_hien) == 0:
            continue
        else:
            maxi = -1
            temp = []
            for mau in so_lan_xuat_hien.keys():
                if so_lan_xuat_hien[mau] > maxi:
                    maxi = so_lan_xuat_hien[mau]
            for mau in so_lan_xuat_hien.keys():
                if so_lan_xuat_hien[mau] == maxi:
                    temp.append(mau)
            for mau in temp:
                del so_lan_xuat_hien[mau]
            mau_the_quan_trong.append(temp)
    #
    return mau_the_quan_trong

def list_the_lay_ngay_func(board):
    list_the_lay_ngay = []
    # Kiểm tra chồng thẻ úp
    if len(player_04.card_upside_down) > 0:
        for the in player_04.card_upside_down:
            if player_04.checkGetCard(the) == True:
                list_the_lay_ngay.append(the)
    temp = ["I", "II", "III"]
    # Kiểm tra chồng thẻ trên bàn
    for bac_the in temp:
        for the in board.dict_Card_Stocks_Show[bac_the]:
            if player_04.checkGetCard(the) == True:
                list_the_lay_ngay.append(the)
    #
    return list_the_lay_ngay