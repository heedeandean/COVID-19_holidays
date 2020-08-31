import pandas as pd
from def_module import *
import pymysql  

if __name__ == "__main__":

    # 부산시
    url = "http://www.busan.go.kr/covid19/Corona19/travelhist.do"
    busan = busan()
    busan.parser(url)
    busan.change_dataFrame()
    bs_df = busan.bs_df_regex()

    # 인천시
    url = 'https://www.incheon.go.kr/health/HE020409'
    inchon = inchon()
    inchon.parser(url)
    inchon.list_data_regex()
    inchon.change_dataFrame()
    ic_df = inchon.ic_df_regex()

    # 광주시
    url = "https://www.gwangju.go.kr/confiremListHome.do"
    html = "https://www.gwangju.go.kr/c19/c19/contentsView.do?pageId=coronagj2"
    gwangju = gwangju()
    gwangju.parser(url,html)
    gju_df= gwangju.change_dataFrame()


    # SAVE POINT
    # frames = [bs_df, ic_df, gju_df]
    # all_df = pd.concat(frames)
    # all_df.to_csv('new_df_data_all_20200829.csv', encoding='UTF-8')

    # 중간에 뻑났을 때 확인하는 용도
    # np.savetxt('busan_arr/arr_data_bs_20200829_test.csv', busan.arr_data_bs, fmt='%s', delimiter=",", encoding='UTF-8')
    # np.savetxt('inchon_arr/arr_data_ic_20200829_test.csv', inchon.arr_data_ic, fmt='%s', delimiter=",", encoding='UTF-8')
    
    list_all = bs_df.values.tolist() + ic_df.values.tolist() + gju_df.values.tolist()

    sql_coronic = "insert into Coronic(area, cfm_date, route, contact_cnt, gender, age) values(%s,%s,%s,%s,%s,%s)"

    conn = pymysql.connect(
        user='root', 
        passwd='1234', 
        host='127.0.0.1', 
        db='covid19', 
        charset='utf8'
    )

    with conn:
        cur = conn.cursor()

        cur.executemany(sql_coronic, list_all)
        print("반영된 수", cur.rowcount)


    print(len(list_all))