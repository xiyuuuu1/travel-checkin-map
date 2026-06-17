import streamlit as st
import pandas as pd
from datetime import datetime
import json
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="我的旅行打卡册", layout="wide")
if "list" not in st.session_state:
    if "yuanshuju" in st.session_state and st.session_state.yuanshuju:
        st.session_state.list = json.loads(st.session_state.yuanshuju)
    else:
        st.session_state.list = []
if "sc" not in st.session_state:
    st.session_state.sc = None
if "ss" not in st.session_state:
    st.session_state.ss = None
if "ei" not in st.session_state:
    st.session_state.ei = None


def yonghushuju():
    st.session_state.yonghushuju = json.dumps(st.session_state.list, ensure_ascii=False)


weizhi = {
    "北京": {"lat": 39.9042, "lon": 116.4074},
    "上海": {"lat": 31.2304, "lon": 121.4737},
    "天津": {"lat": 39.0842, "lon": 117.2010},
    "重庆": {"lat": 29.5630, "lon": 106.5516},
    "石家庄": {"lat": 38.0423, "lon": 114.5149},
    "太原": {"lat": 37.8706, "lon": 112.5489},
    "沈阳": {"lat": 41.8070, "lon": 123.4305},
    "长春": {"lat": 43.8800, "lon": 125.3300},
    "哈尔滨": {"lat": 45.8020, "lon": 126.5358},
    "南京": {"lat": 32.0603, "lon": 118.7969},
    "杭州": {"lat": 30.2741, "lon": 120.1551},
    "合肥": {"lat": 31.8611, "lon": 117.2826},
    "福州": {"lat": 26.0745, "lon": 119.2965},
    "南昌": {"lat": 28.6827, "lon": 115.8578},
    "济南": {"lat": 36.6782, "lon": 117.0098},
    "郑州": {"lat": 34.7572, "lon": 113.6537},
    "武汉": {"lat": 30.5928, "lon": 114.3055},
    "长沙": {"lat": 28.2282, "lon": 112.9388},
    "广州": {"lat": 23.1291, "lon": 113.2644},
    "海口": {"lat": 20.0317, "lon": 110.3288},
    "成都": {"lat": 30.5728, "lon": 104.0668},
    "贵阳": {"lat": 26.6543, "lon": 106.6302},
    "昆明": {"lat": 25.6065, "lon": 102.7122},
    "西安": {"lat": 34.2644, "lon": 108.9497},
    "兰州": {"lat": 36.0611, "lon": 103.8343},
    "西宁": {"lat": 36.6171, "lon": 101.7782},
    "呼和浩特": {"lat": 40.8228, "lon": 111.7477},
    "南宁": {"lat": 22.8240, "lon": 108.3275},
    "拉萨": {"lat": 29.6546, "lon": 91.1409},
    "银川": {"lat": 38.4872, "lon": 106.2364},
    "乌鲁木齐": {"lat": 43.8256, "lon": 87.6177},
    "台北": {"lat": 25.0330, "lon": 121.5654},
    "香港": {"lat": 22.2783, "lon": 114.1747},
    "澳门": {"lat": 22.1987, "lon": 113.5439},
    "深圳": {"lat": 22.5431, "lon": 114.0579},
    "日本": {"lat": 35.6762, "lon": 139.6503},
    "韩国": {"lat": 37.5665, "lon": 126.9780},
    "英国": {"lat": 51.5074, "lon": -0.1278},
    "法国": {"lat": 48.8566, "lon": 2.3522},
    "德国": {"lat": 52.5200, "lon": 13.4050},
    "意大利": {"lat": 41.9028, "lon": 12.4964},
    "西班牙": {"lat": 40.4168, "lon": -3.7038},
    "葡萄牙": {"lat": 38.7223, "lon": -9.1393},
    "俄罗斯": {"lat": 55.7558, "lon": 37.6176},
    "瑞士": {"lat": 46.9480, "lon": 7.4474},
    "荷兰": {"lat": 52.3676, "lon": 4.9041},
    "瑞典": {"lat": 59.3293, "lon": 18.0686},
    "挪威": {"lat": 59.9139, "lon": 10.7522},
    "波兰": {"lat": 52.2298, "lon": 21.0118},
    "希腊": {"lat": 37.9838, "lon": 23.7275},
    "美国": {"lat": 38.9072, "lon": -77.0369},
    "加拿大": {"lat": 45.4215, "lon": -75.6972},
    "澳大利亚": {"lat": -35.2809, "lon": 149.1300},
    "新西兰": {"lat": -41.2865, "lon": 174.7762},
}


def sl(x):
    s = str(x).strip().rstrip("·")
    if "·" in s:
        a, b = s.split("·", 1)
        return a.strip(), b.strip()
    else:
        acl = list(weizhi.keys())
        mc = None
        for city in acl:
            if s.startswith(city):
                mc = city
                break
        if mc:
            return mc, s.replace(mc, "").strip()
        return s[:2], s


COLOR = "#fb7da8"
df = pd.DataFrame(st.session_state.list)
for col in ["出发地", "打卡心得", "星级评价"]:
    if col not in df.columns:
        df[col] = ""

if df.empty:
    paixu = df.copy()
else:
    if "出发地" not in df.columns:
        df["出发地"] = ""
    df["日期"] = pd.to_datetime(df["日期"])
    paixu = df.sort_values(by="日期", ascending=False).reset_index(drop=True)
    paixu["日期"] = paixu["日期"].dt.strftime("%Y-%m-%d")

if "选中城市" not in st.session_state:
    st.session_state.sc = None
if "选中景点" not in st.session_state:
    st.session_state.ss = None

left, right = st.columns([1, 3])

with left:
    st.header("新增打卡记录")
    with st.form("biao"):
        riqi = st.date_input("打卡日期", value=datetime.today())
        chufadi = st.text_input("本次出发地", placeholder="例如：成都（省会城市）")
        mudidi = st.text_input("目的地·景点", placeholder="格式：北京（省会城市）·故宫")
        note = st.text_area("打卡心得", placeholder="写下你的旅行感受吧~")
        pingfen = st.slider("本次旅行体验", 1, 5, 3)
        submitted = st.form_submit_button("保存打卡")
    if submitted and mudidi.strip() and chufadi.strip():
        nr = {
            "日期": riqi.strftime("%Y-%m-%d"),
            "出发地": chufadi.strip(),
            "城市/景点": mudidi.strip(),
            "打卡心得": note,
            "星级评价": "⭐" * pingfen
        }
        st.session_state.list.append(nr)
        yonghushuju()
        st.rerun()
    elif submitted:
        st.warning("出发地和目的地景点不能为空！")
    st.divider()
    st.header("旅行小统计")
    if not paixu.empty:
        temp_paixu = paixu.copy()


        def split_city_only(s):
            city, _ = sl(s)
            return city


        def split_scenic_only(s):
            _, scenic = sl(s)
            return scenic


        temp_paixu["目的地城市"] = temp_paixu["城市/景点"].apply(split_city_only)
        temp_paixu["细分景点"] = temp_paixu["城市/景点"].apply(split_scenic_only)

        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="已打卡目的地城市数", value=temp_paixu["目的地城市"].nunique())
        with c2:
            st.metric(label="总打卡出行次数", value=len(temp_paixu))

        st.divider()
        st.subheader("选择目的地城市查看下属景点")
        cg = temp_paixu.groupby("目的地城市").agg(
            打卡次数=("城市/景点", "count"),
            首次时间=("日期", lambda x: pd.to_datetime(x).min())
        ).reset_index()
        cg = cg.sort_values(by=["打卡次数", "首次时间"], ascending=[False, True])
        sorted_cities = cg["目的地城市"].tolist()

        for cn in sorted_cities:
            count = cg[cg["目的地城市"] == cn]["打卡次数"].values[0]
            if st.button(f"{cn}（{count}次出行）", use_container_width=True):
                st.session_state.sc = cn
                st.session_state.ss = None

        if st.session_state.sc:
            target_city = st.session_state.sc
            st.divider()
            st.subheader(f"{target_city} 下辖景点列表")
            cfd = temp_paixu[temp_paixu["目的地城市"] == target_city]
            scenic_group = cfd.groupby("细分景点").agg(
                景点打卡数=("城市/景点", "count"),
                景点首访=("日期", lambda x: pd.to_datetime(x).min())
            ).reset_index()
            scenic_group = scenic_group.sort_values(by=["景点打卡数", "景点首访"], ascending=[False, True])
            sorted_scenics = scenic_group["细分景点"].tolist()
            for sn in sorted_scenics:
                s = scenic_group[scenic_group["细分景点"] == sn]["景点打卡数"].values[0]
                if st.button(f"{sn}（{s}次）", use_container_width=True):
                    st.session_state.ss = sn

            if st.session_state.ss:
                ts = st.session_state.ss
                st.divider()
                st.markdown(f"### {target_city}·{ts} 全部出行回忆")
                record_data = cfd[cfd["细分景点"] == ts]
                for _, line in record_data.iterrows():
                    disp_start = line["出发地"].strip() if pd.notna(line["出发地"]) else "未填写"
                    st.write(f"出发地：{disp_start}")
                    st.write(f"打卡日期：{line['日期']} ｜ {line['星级评价']}")
                    feel = line["打卡心得"]
                    if pd.isna(feel) or str(feel).strip() == "":
                        dt = "无"
                    else:
                        dt = str(feel)
                    st.write(f"当时感受：{dt}")
                    st.divider()
    else:
        st.info("暂无打卡数据，添加记录后即可查看统计、航线地图与选择功能")

with right:
    st.title("我的旅行打卡册")
    st.subheader("记录每一次心动的旅行瞬间")
    st.header("我的旅行足迹")
    if paixu.empty:
        st.info("待添加新的足迹")
    else:
        show_df = paixu.reset_index(drop=True)
        for idx, row in show_df.iterrows():
            sr = str(row["出发地"])
            sd = sr.strip() if sr.strip() else "未填写"
            expander_title = f"> {row['日期']} | {sd} → {row['城市/景点']} {row['星级评价']}"
            with st.expander(expander_title, expanded=(st.session_state.ei== idx)):
                if st.session_state.ei == idx:
                    st.markdown("### 编辑记录")
                    original_data = st.session_state.list[idx]
                    star_str = original_data.get("星级评价", "")
                    star_count = len(star_str) if star_str else 3
                    with st.form(key=f"edit_form_{idx}"):
                        eda = st.date_input(
                            "打卡日期",
                            value=datetime.strptime(original_data["日期"], "%Y-%m-%d").date()
                        )
                        ef = st.text_input("本次出发地", value=original_data.get("出发地", ""))
                        ede = st.text_input("目的地·景点", value=original_data.get("城市/景点", ""))
                        en = st.text_area("打卡心得", value=original_data.get("打卡心得", ""))
                        er = st.slider("本次旅行体验", 1, 5, star_count)
                        c1, c2 = st.columns(2)
                        with c1:
                            save_edit = st.form_submit_button("保存修改", use_container_width=True)
                        with c2:
                            cancel_edit = st.form_submit_button("取消编辑", use_container_width=True)
                        if save_edit:
                            if ef.strip() and ede.strip():
                                st.session_state.list[idx] = {
                                    "日期": eda.strftime("%Y-%m-%d"),
                                    "出发地": ef.strip(),
                                    "城市/景点": ede.strip(),
                                    "打卡心得": en,
                                    "星级评价": "⭐" * er
                                }
                                yonghushuju()
                                st.session_state.ei = None
                                st.rerun()
                            else:
                                st.warning("出发地和目的地景点不能为空！")
                        if cancel_edit:
                            st.session_state.ei = None
                            st.rerun()
                else:
                    feeling = row["打卡心得"]
                    stt = str(feeling).strip() if pd.notna(feeling) and str(feeling).strip() else "无"
                    st.write(f"出发地：{sd}")
                    st.write(f"目的地：{row['城市/景点']}")
                    st.write(f"**打卡心得：** {stt}")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button(f"编辑", key=f"edit_{idx}"):
                            st.session_state.ei = idx
                            st.rerun()
                    with c2:
                        if st.button(f"删除", key=f"del_{idx}"):
                            del st.session_state.list[idx]
                            yonghushuju()
                            if st.session_state.ei == idx:
                                st.session_state.ei = None
                            st.rerun()
    st.divider()
    st.subheader("全国旅行航线地图")
    ditu = folium.Map(
        location=[35, 105],
        zoom_start=4,
        tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
        attr='&copy; 高德地图'
    )
    rd = st.session_state.list
    if len(rd) > 0:
        for item in rd:
            fc = str(item["出发地"]).strip()
            dest_str = str(item["城市/景点"]).strip()
            dci, _ = sl(dest_str)
            if fc in weizhi and dci in weizhi:
                lat1 = weizhi[fc]["lat"]
                lon1 = weizhi[fc]["lon"]
                lat2 = weizhi[dci]["lat"]
                lon2 = weizhi[dci]["lon"]
                folium.PolyLine(
                    locations=[[lat1, lon1], [lat2, lon2]],
                    color="#fb7da8",
                    weight=3,
                    opacity=0.9
                ).add_to(ditu)
    st_folium(ditu, width="100%", height=450)
    st.caption("粉色实线代表行程路线：出发地→目的地")
