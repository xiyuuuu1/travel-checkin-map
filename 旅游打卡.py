import streamlit as st
import pandas as pd
from datetime import datetime
import json
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="我的旅行打卡册", page_icon="🌍", layout="wide")
if "my_checkins" not in st.session_state:
    if "checkins_data" in st.session_state and st.session_state.checkins_data:
        st.session_state.my_checkins = json.loads(st.session_state.checkins_data)
    else:
        st.session_state.my_checkins = []

def save_user_data():
    st.session_state.checkins_data = json.dumps(st.session_state.my_checkins, ensure_ascii=False)
CITY_COORDS = {
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
    "朝鲜": {"lat": 39.0392, "lon": 125.7625},
    "越南": {"lat": 21.0278, "lon": 105.8342},
    "泰国": {"lat": 13.7563, "lon": 100.5018},
    "马来西亚": {"lat": 3.1390, "lon": 101.6869},
    "新加坡": {"lat": 1.3521, "lon": 103.8198},
    "印度尼西亚": {"lat": -6.2088, "lon": 106.8456},
    "菲律宾": {"lat": 14.5995, "lon": 120.9842},
    "印度": {"lat": 28.6139, "lon": 77.2090},
    "巴基斯坦": {"lat": 33.6844, "lon": 73.0479},
    "孟加拉国": {"lat": 23.8103, "lon": 90.4125},
    "阿联酋": {"lat": 24.4667, "lon": 54.3667},
    "沙特阿拉伯": {"lat": 24.7136, "lon": 46.6753},
    "土耳其": {"lat": 39.9334, "lon": 32.8597},
    "以色列": {"lat": 31.7683, "lon": 35.2137},
    "伊朗": {"lat": 35.6892, "lon": 51.3890},
    "英国": {"lat": 51.5074, "lon": -0.1278},
    "法国": {"lat": 48.8566, "lon": 2.3522},
    "德国": {"lat": 52.5200, "lon": 13.4050},
    "意大利": {"lat": 41.9028, "lon": 12.4964},
    "西班牙": {"lat": 40.4168, "lon": -3.7038},
    "葡萄牙": {"lat": 38.7223, "lon": -9.1393},
    "俄罗斯": {"lat": 55.7558, "lon": 37.6176},
    "瑞士": {"lat": 46.9480, "lon": 7.4474},
    "奥地利": {"lat": 48.2082, "lon": 16.3738},
    "荷兰": {"lat": 52.3676, "lon": 4.9041},
    "比利时": {"lat": 50.8503, "lon": 4.3517},
    "瑞典": {"lat": 59.3293, "lon": 18.0686},
    "挪威": {"lat": 59.9139, "lon": 10.7522},
    "波兰": {"lat": 52.2298, "lon": 21.0118},
    "乌克兰": {"lat": 50.4501, "lon": 30.5234},
    "希腊": {"lat": 37.9838, "lon": 23.7275},
    "美国": {"lat": 38.9072, "lon": -77.0369},
    "加拿大": {"lat": 45.4215, "lon": -75.6972},
    "巴西": {"lat": -15.7942, "lon": -47.8825},
    "阿根廷": {"lat": -34.6037, "lon": -58.3816},
    "墨西哥": {"lat": 19.4326, "lon": -99.1332},
    "智利": {"lat": -33.4489, "lon": -70.6693},
    "秘鲁": {"lat": -12.0464, "lon": -77.0428},
    "澳大利亚": {"lat": -35.2809, "lon": 149.1300},
    "新西兰": {"lat": -41.2865, "lon": 174.7762},
    "埃及": {"lat": 30.0444, "lon": 31.2357},
    "南非": {"lat": -25.7460, "lon": 28.1871},
    "肯尼亚": {"lat": -1.2864, "lon": 36.8172}
}

LINE_COLOR = "#fb7da8"
df = pd.DataFrame(st.session_state.my_checkins)

if df.empty:
    df_sorted = df.copy()
else:
    if "出发地" not in df.columns:
        df["出发地"] = ""
    df["日期"] = pd.to_datetime(df["日期"])
    df_sorted = df.sort_values(by="日期", ascending=False).reset_index(drop=True)
    df_sorted["日期"] = df_sorted["日期"].dt.strftime("%Y-%m-%d")

def split_city_scenic(full_name):
    name_str = str(full_name).strip()
    if "·" in name_str:
        city_part, scenic_part = name_str.split("·", 1)
        return city_part.strip(), scenic_part.strip()
    else:
        city_part = name_str[:2]
        scenic_part = name_str
        return city_part, scenic_part

if not df_sorted.empty:
    df_sorted[["目的地城市", "细分景点"]] = df_sorted["城市/景点"].apply(lambda x: pd.Series(split_city_scenic(x)))
if "sel_city" not in st.session_state:
    st.session_state.sel_city = None
if "sel_scenic" not in st.session_state:
    st.session_state.sel_scenic = None

col_form, col_content = st.columns([1, 3])

with col_form:
    st.header("✨ 新增打卡记录")
    with st.form("checkin_form"):
        date = st.date_input("打卡日期", value=datetime.today())
        start_city = st.text_input("本次出发地", placeholder="例如：成都（省会城市）")
        location = st.text_input("目的地·景点", placeholder="格式：北京（省会城市）·故宫")
        note = st.text_area("打卡心得", placeholder="写下你的旅行感受吧~")
        rating = st.slider("本次旅行体验", 1, 5, 3)
        submitted = st.form_submit_button("✅ 保存打卡")

# 保存打卡逻辑
if submitted and location.strip() and start_city.strip():
    new_row = {
        "日期": date.strftime("%Y-%m-%d"),
        "出发地": start_city.strip(),
        "城市/景点": location.strip(),
        "打卡心得": note,
        "星级评价": "⭐" * rating
    }
    st.session_state.my_checkins.append(new_row)
    save_user_data()
    st.rerun()
elif submitted:
    st.warning("出发地和目的地景点不能为空！")

with col_content:
    st.title("🌍 我的旅行打卡册")
    st.subheader("记录每一次心动的旅行瞬间")
    st.header("📋 我的旅行足迹")
    if "edit_index" not in st.session_state:
        st.session_state.edit_index = None
    if df_sorted.empty:
        st.info("待添加新的足迹")
    else:
        display_df = df_sorted.reset_index(drop=True)
        for idx, row in display_df.iterrows():
            start_raw = str(row["出发地"])
            start_display = start_raw.strip() if start_raw.strip() else "未填写"
            expander_title = f"> {row['日期']} | {start_display} → {row['城市/景点']} {row['星级评价']}"
            with st.expander(expander_title):
                feeling = row["打卡心得"]
                show_text = str(feeling).strip() if pd.notna(feeling) and str(feeling).strip() else "无"
                st.write(f"🚀 出发地：{start_display}")
                st.write(f"📍 目的地：{row['城市/景点']}")
                st.write(f"**打卡心得：** {show_text}")
                btn_edit, btn_del = st.columns([1, 1])
                with btn_edit:
                    if st.button(f"✏️ 编辑", key=f"edit_{idx}"):
                        st.session_state.edit_index = idx
                with btn_del:
                    if st.button(f"🗑️ 删除", key=f"del_{idx}"):
                        st.session_state.my_checkins.append(new_row)
                        save_user_data()
                        st.rerun()

    if st.session_state.edit_index is not None and not df_sorted.empty:
        edit_idx = st.session_state.edit_index
        edit_row = display_df.iloc[edit_idx]
        st.divider()
        st.subheader("✏️ 修改行程记录")
        with st.form("edit_form"):
            new_date = st.date_input("打卡日期", value=pd.to_datetime(edit_row["日期"]))
            new_start = st.text_input("本次出发地", value=str(edit_row["出发地"]).strip())
            new_loc = st.text_input("目的地·景点", value=edit_row["城市/景点"])
            new_note = st.text_area("打卡心得",
                                    value=str(edit_row["打卡心得"]) if pd.notna(edit_row["打卡心得"]) else "")
            old_star = len(edit_row["星级评价"]) if edit_row["星级评价"] else 3
            new_rating = st.slider("本次旅行体验", 1, 5, old_star)

            save_edit, cancel_edit = st.columns([1, 1])
            with save_edit:
                sub_save = st.form_submit_button("✅ 保存修改")
            with cancel_edit:
                sub_cancel = st.form_submit_button("❌ 取消")

            if sub_save:
                st.session_state.my_checkins[edit_idx] = {
                    "日期": new_date.strftime("%Y-%m-%d"),
                    "出发地": new_start.strip(),
                    "城市/景点": new_loc.strip(),
                    "打卡心得": new_note,
                    "星级评价": "⭐" * new_rating
                }
                save_user_data()
                st.session_state.edit_index = None
                st.rerun()
            if sub_cancel:
                st.session_state.edit_index = None
                st.rerun()

    st.divider()
    st.subheader("🗺️ 全国旅行航线地图")
    map_china = folium.Map(
        location=[35, 105],
        zoom_start=3.8,
        tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
        attr='&copy; 高德地图'
    )

    if not df_sorted.empty:
        for _, row in df_sorted.iterrows():
            s_name = str(row["出发地"]).strip()
            d_name = str(row["目的地城市"]).strip()
            print(f"【行程】出发:{s_name} 目的地城市:{d_name}")
            if s_name in CITY_COORDS and d_name in CITY_COORDS:
                s_pos = [CITY_COORDS[s_name]["lat"], CITY_COORDS[s_name]["lon"]]
                d_pos = [CITY_COORDS[d_name]["lat"], CITY_COORDS[d_name]["lon"]]
                folium.PolyLine(
                    locations=[s_pos, d_pos],
                    color="#fb7da8",
                    weight=5,
                    opacity=0.9
                ).add_to(map_china)

    st_folium(map_china, width="100%", height=450)
    st.caption("粉色实线代表行程路线：出发地→目的地")
    st.divider()
    st.header("📊 旅行小统计")
    if not df_sorted.empty:
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.metric(label="已打卡目的地城市数", value=df_sorted["目的地城市"].nunique())
        with stat_col2:
            st.metric(label="总打卡出行次数", value=len(df_sorted))

        st.divider()
        st.subheader("📍 选择目的地城市查看下属景点")
        city_group = df_sorted.groupby("目的地城市").agg(
            打卡次数=("城市/景点", "count"),
            首次时间=("日期", lambda x: pd.to_datetime(x).min())
        ).reset_index()
        city_group = city_group.sort_values(by=["打卡次数", "首次时间"], ascending=[False, True])
        sorted_cities = city_group["目的地城市"].tolist()
        for city_name in sorted_cities:
            count = city_group[city_group["目的地城市"] == city_name]["打卡次数"].values[0]
            if st.button(f"{city_name}（{count}次出行）", use_container_width=True):
                st.session_state.sel_city = city_name
                st.session_state.sel_scenic = None
        if st.session_state.sel_city:
            target_city = st.session_state.sel_city
            st.divider()
            st.subheader(f"📍 {target_city} 下辖景点列表")
            city_filter_data = df_sorted[df_sorted["目的地城市"] == target_city]
            scenic_group = city_filter_data.groupby("细分景点").agg(
                景点打卡数=("城市/景点", "count"),
                景点首访=("日期", lambda x: pd.to_datetime(x).min())
            ).reset_index()
            scenic_group = scenic_group.sort_values(by=["景点打卡数", "景点首访"], ascending=[False, True])
            sorted_scenics = scenic_group["细分景点"].tolist()
            for scenic_name in sorted_scenics:
                s_count = scenic_group[scenic_group["细分景点"] == scenic_name]["景点打卡数"].values[0]
                if st.button(f"{scenic_name}（{s_count}次）", use_container_width=True):
                    st.session_state.sel_scenic = scenic_name
            if st.session_state.sel_scenic:
                target_scenic = st.session_state.sel_scenic
                st.divider()
                st.markdown(f"### 📌 {target_city}·{target_scenic} 全部出行回忆")
                record_data = city_filter_data[city_filter_data["细分景点"] == target_scenic]
                for _, line in record_data.iterrows():
                    disp_start = line["出发地"].strip() if pd.notna(line["出发地"]) else "未填写"
                    st.write(f"🚀 出发地：{disp_start}")
                    st.write(f"🗓️ 打卡日期：{line['日期']} ｜ {line['星级评价']}")
                    feel_text = line["打卡心得"]
                    if pd.isna(feel_text) or str(feel_text).strip() == "":
                        disp_text = "无"
                    else:
                        disp_text = str(feel_text)
                    st.write(f"💭 当时感受：{disp_text}")
                    st.divider()
    else:
        st.info("暂无打卡数据，添加记录后即可查看统计、航线地图与选择功能")
