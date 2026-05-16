import streamlit as st
import random
import time
import re


#게임 메인화면
st.set_page_config(page_title="이정인 막아내기", layout="wide")
st.title("경영학원론 에세이 시뮬레이터")
st.markdown(
    "이정인이 당신의 **원론 에세이**를 강탈하러 옵니다.\n\n에세이 작성 완료까지는 24시간...! 과연 이현재는 에세이를 지켜내고 무사히 카페에 제출버튼을 누를 수 있을까요?"
)
st.markdown("호시탐탐 에세이를 노리는 이정인을 막아내기 위해 부원들을 밥약으로 고용할 수 있습니다.\n\n다양한 조합으로 부원간 시너지를 발휘해 보세요.\n\n행운을 빌어요!")

st.write("---")

# [1] 데이터베이스


# 부원 목록 (이름: [가격, 기본 수치, 주사위 최댓값])
guards_db = {
    "이아람": {"cost": 5000, "power": 25, "dice": 10},
    "정진성": {"cost": 5500, "power": 25, "dice": 10},
    "임주성": {"cost": 6000, "power": 25, "dice": 10},
    "류신해": {"cost": 7500, "power": 25, "dice": 10},
    "권준혁": {"cost": 8000, "power": 25, "dice": 10},
    "오유찬": {"cost": 8500, "power": 25, "dice": 10},
    "윤석준": {"cost": 8500, "power": 25, "dice": 10},
    "전재환": {"cost": 9000, "power": 25, "dice": 10},
    "이준혁": {"cost": 9000, "power": 25, "dice": 10},
    "이유빈": {"cost": 9000, "power": 25, "dice": 10},
    "강준서": {"cost": 9500, "power": 25, "dice": 10},
    "김동규": {"cost": 10000, "power": 25, "dice": 10},
    "양서진": {"cost": 10000, "power": 25, "dice": 10},
    "노현경": {"cost": 10500, "power": 25, "dice": 10},
    "송재원": {"cost": 11500, "power": 500, "dice": 10},
    "한성원": {"cost": 12000, "power": 25, "dice": 10},
    "장준혁": {"cost": 13000, "power": 25, "dice": 10},
    "정하윤": {"cost": 14000, "power": 25, "dice": 10},
    "최진영": {"cost": 14500, "power": 25, "dice": 10},
    "류혜정": {"cost": 15000, "power": 25, "dice": 10},
    "한부현": {"cost": 15000, "power": 25, "dice": 10},
    "김유영": {"cost": 20000, "power": 10000, "dice": 0},
}

items_db = {
    "🥤딸기라떼": {"cost": 2000, "desc": "매 시간 종료 시 25% 확률로 시간을 가속하여, 누적 효과(화상, 적응, 회복)를 한 번 더 발동시킵니다."},
    "🍲식어버린김치찜": {"cost": 3500, "desc": "에세이를 빼앗겨도 2번 다시할 수 있습니."},
    "🦪굴": {"cost": 5000, "desc": "치명적인 위기의 순간 사용합니다"},
    "🥓우대갈비": {"cost": 7500, "desc": "이정인의 공격력을 30% 감소시킵니다."},
    "🍖족발": {"cost": 15000, "desc": "이현재를 재미없게해 과제를 더 일찍 끝내도록 만듭니다."},
}

# [2] 사용자 UI 및 고용 시스템
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛡️ 부원 고용")
    g_names = list(guards_db.keys())
    half = (len(g_names) + 1) // 2
    g_col1, g_col2 = st.columns(2)
    
    selected_guards = []
    with g_col1:
        for name in g_names[:half]:
            if st.checkbox(f"{name} ({guards_db[name]['cost']})", key=f"check_{name}"):
                selected_guards.append(name)
    with g_col2:
        for name in g_names[half:]:
            if st.checkbox(f"{name} ({guards_db[name]['cost']})", key=f"check_{name}"):
                selected_guards.append(name)


with col2:
    st.subheader("🍵 간식 구매")
    selected_items = [name for name in items_db if st.checkbox(f"{name} ({items_db[name]['cost']}) - {items_db[name]['desc']}")]

#돈 무한모드
if "김유영" in selected_guards:
    BUDGET = 100000
else:
    BUDGET = 30000

st.write("---")


synergy_messages = []
discount = 0

# 0.돈무한모드
if "김유영" in selected_guards:
    synergy_messages.append("💡 **[🍞🍞🍞김유영 모드🍞🍞🍞]** 재미를 위한 돈 무한 모드입니다. (용돈 10배 증가)")

# 1. 딸기라떼 시너지
if "류혜정" in selected_guards and "🥤딸기라떼" in selected_items:
    discount = 2000
    synergy_messages.append("💡 **[시너지 발견: 백억커피 알바생]** 이정도는 서비스야. (딸기라떼 구매비용 할인)")

# 2. 삼준혁 시너지
if "이준혁" in selected_guards and "권준혁" in selected_guards and "장준혁" in selected_guards:
    synergy_messages.append("💡 **[시너지 발견: 준혁준혁준혁]** 삼준혁이 모였습니다. (아무 효과 없음)")

# 3. 정경대 할인
detective_team = [g for g in selected_guards if g in ["한성원", "정하윤", "양서진"]]
if len(detective_team) >= 2:
    discount = 5000
    synergy_messages.append(f"💡 **[시너지 발견: 정경대 학생 할인]** 정하윤의 정경대 학생 할인으로 밥약이 수월해졌습니다! (고용 비용 5,000원 할인)")

# 4. 월간 류앤김
if "류신해" in selected_guards and "김동규" in selected_guards:
    synergy_messages.append("💡 **[시너지 발견: 월간 류앤김]** 웬수같은 둘이 모여 전투력이 올라갑니다. (영구 위력 +10)")

# 5. 요리사
if "권준혁" in selected_guards and "이유빈" in selected_guards:
    synergy_messages.append("💡 **[시너지 발견: 요리사]** 적어도 요리가 망하진 않을겁니다! ")

# 6. 총무즈
money_team = [g for g in selected_guards if g in ["이아람", "권준혁", "김동규"]]
if len(money_team) >= 2:
    discount = 3000
    synergy_messages.append(f"💡 **[시너지 발견: 총무즈]** 총무들이 역시 돈을 알뜰하게 써요. (고용 비용 3,000원 할인)")

# 7. 부회장즈
vice_members = ["류혜정", "류신해", "전재환", "최진영", "이유빈"]
vice_count = sum(1 for g in vice_members if g in selected_guards)
if vice_count >= 2:
    synergy_messages.append(f"💡 **[시너지 발견: 동아리 실세들]** {vice_count}인의 부회장이 모여 계획을 짭니다! (이정인의 위력 -40)")

# 8. 하드게이머
hards = [g for g in selected_guards if g in ["이아람", "정진성", "권준혁", "오유찬", "윤석준", "류혜정", "장준혁", "한성원"]]
if len(hards) >= 3:
    synergy_messages.append("💡 **[시너지 발견: 하드게이머]** 전략가들이 모였습니다! (아군 진형의 영구 방어선 +20)")

# 9. 경평
buisness_team = ["이준혁", "이유빈", "노현경", "류신해", "오유찬", "전재환", "김유영"]
buisness_count = sum(1 for g in buisness_team if g in selected_guards)
if buisness_count >= 3:  # 발동 조건을 3인 이상으로 빡빡하게 올림!
    buisness_penalty = buisness_count * 4
    synergy_messages.append(f"💡 **[시너지 발견: 경평ㅋㅋㅋ]** {buisness_count}인의 경평ㅋㅋ이 모여, 끔찍한 진흙탕 싸움을 유도합니다! (매 6시간마다 이정인의 위력 -{buisness_penalty})")

# 10. 스팸 시너지
    if "이준혁" in selected_guards and "전재환" in selected_guards:
        synergy_messages.append(f"💡 **[시너지 발견: 애착인형]** 이준혁이 계속 도촬을 합니다..ㅠㅠ (디버프 강화)")
    if "이준혁" in selected_guards and "오유찬" in selected_guards:
        synergy_messages.append(f"💡 **[시너지 발견: 애착인형]** 이준혁이 계속 도촬을 합니다..ㅠㅠ (디버프 강화)")

# 11. 04듀오
if "송재원" in selected_guards and "노현경" in selected_guards:
    synergy_messages.append("💡 **[시너지 발견: 쌍둥이]** 송재원이 두시간 더 있다 도망갑니다.")

# 12. 아버지
if "임주성" in selected_guards and "양서진" in selected_guards:
    synergy_messages.append("💡 **[시너지 발견: 양아버지]** 일방적인 부녀관계 입니다.")

# 13. 오따끄
if "임주성" in selected_guards and "한부현" in selected_guards:
    synergy_messages.append("💡 **[시너지 발견: 오따끄]** 오따끄들 잼얘가 늘어납니다.")

# 14. 명예 일본인들
jpops = [g for g in selected_guards if g in ["정진성", "류신해", "류혜정", "오유찬", "윤석준", "최진영"]]
if len(jpops) >= 3:
    synergy_messages.append("💡 **[시너지 발견: 명예 일본인들]** JPOP 료이키 텐카이. (아군 진형의 영구 방어선 +10)")

if synergy_messages:
    for msg in synergy_messages:
        st.success(msg)

# 최종 비용 산출 (할인 적용)
total_cost = sum([guards_db[g]["cost"] for g in selected_guards]) + sum([items_db[i]["cost"] for i in selected_items])
total_cost -= discount 
formatted_budget = f"{BUDGET:,}"
formatted_cost = f"{total_cost:,}"

st.markdown(f"### 💰 현재 소모한 용돈: **{formatted_cost}** / {formatted_budget}원")

# [3] 시뮬레이션 논리 및 실행
if st.button("⏳ 시뮬레이션 시작"):
    if total_cost > BUDGET:
        st.error("경고: 소지한 용돈을 초과했습니다. 조합을 수정하십시오.")
    elif not selected_guards and not selected_items:
        st.error("아무런 대비 없이 에세이를 지켜낼 수 없습니다.")
    else:
        initial_guards = selected_guards.copy()
        initial_items = selected_items.copy()
        st.write("---")
        st.subheader("💻  과제 기록 로그")

# 기본 장비 변수
        target_hours = 18 if "🍖족발" in selected_items else 24
        has_noro = "🦪굴" in selected_items
        revives_left = 2 if "🍲식어버린김치찜" in selected_items else 0
        aggro_multiplier = 0.7 if "🥓우대갈비" in selected_items else 1.0
        has_t_gear = "T사 보조 태엽" in selected_items
        t_gear_triggers = 0  # 터진 횟수 누적

 # 특수 능력 상태 추적 변수
        team_power_base = sum([guards_db[g]["power"] for g in selected_guards])
        persistent_power_bonus = 0 # 누적 스탯 
        ji_perm_debuff = 0
        carried_shield = 0
        battle_logs = ""
        com_secu = 3 if "최진영" in selected_guards else 0
        if "최진영" in selected_guards and "김동규" in selected_guards:
            com_secu += 1
            battle_logs += "> 💻 :blue[**[시너지 발동: 컴퓨터보안]**] 컴과의 힘으로 현재의 컴퓨터보안을 강화합니다. (비밀번호 가능 횟수 +1)\n\n"

        is_ysj_berserk = False
        last_hour_gap = 0  # 직전 시간의 위력 격차 저장
        gjs_shield_used = False
        is_ljs_alive = "임주성" in selected_guards
        log_container = st.empty()
        survival_status = True
        reverse_jungin = False
        jawon_alive = 0
        leg_broke = False
        spam = 0
        blood_gauge = (100 if "류혜정" in selected_guards else 0) + (250 if "한부현" in selected_guards else 0)

        # 이전 빗나감 타겟
        previous_missed_guards = []

        buisness_team = ["이준혁", "이유빈", "노현경", "류신해", "오유찬", "전재환", "김유영"]
        buisness_count_sim = sum(1 for g in buisness_team if g in selected_guards)
        is_buisness = buisness_count_sim >= 3 # 3명 이상일 때만 True

# --- [시너지 전투 수치 적용 구역] ---
        spam = 0 # 엄지 시너지 화상 보너스 초기화
        song_noh = 0
        
        # 1. 검은침묵 부부 시너지
        if "롤랑" in selected_guards and "검은침묵 안젤리카" in selected_guards:
            revives_left += 1  # K사 앰플 1회 분량 추가 (또는 3회로 하려면 += 3)
            has_t_badge = True # T사 배지 강제 활성화

        # 3. 류앤김 시너지
        if "류신해" in selected_guards and "김동규" in selected_guards:
            persistent_power_bonus += 10

        # 4. 스팸 시너지
        if "이준혁" in selected_guards and "전재환" in selected_guards:
            spam += 3
        if "이준혁" in selected_guards and "오유찬" in selected_guards:
            spam += 3

        # 5. 부회장 시너지 (초기 영구 디버프)
        vice_count = sum(1 for g in ["류혜정", "류신해", "전재환", "최진영", "이유빈"] if g in selected_guards)
        if vice_count >= 2:
            ji_perm_debuff += 40

        # 6. 하드 (영구 방어선 증가)
        hards = [g for g in selected_guards if g in ["이아람", "정진성", "권준혁", "오유찬", "윤석준", "류혜정", "장준혁", "한성원"]]
        if len(hards) >= 2:
            persistent_power_bonus += 20

        # 7. 제이팝 (영구 방어선 증가)
        jpops = [g for g in selected_guards if g in ["정진성", "류신해", "류혜정", "오유찬", "윤석준", "최진영"]]
        if len(jpops) >= 3:
            persistent_power_bonus += 10


        # 7. 소지 시너지 (영구 방어선 증가)
        if "송재원" in selected_guards and "노현경" in selected_guards:
            song_noh = 2

        log_container = st.empty()
        survival_status = True


  # 시간 흐름 루프 시작
        for hour in range(1, target_hours + 1):
            hour_log = f"#### **🕒 {hour}시간 경과**\n"
            missed_guards_this_turn = []
            if hour == 1:
                hour_log += "> 🗡️ **[전투 개시]** 이정인이 에세이를 빼앗기 위해 천천히 접근합니다.\n\n"
            elif hour == 13:
                hour_log += "> 📱 :red[**[단톡방 피드백]**] 이정인이 톡방에 지적질을 하며 엄청난 살의를 내뿜습니다!\n\n"
            elif hour == 18 and target_hours == 18:
                hour_log += "> 게임 재미없다 빨리 끝내라.\n\n"
            elif hour == 21:
                hour_log += "> ⚠️ :red[**[해킹]**] 이정인이 네이버 아이디 해킹공격을 시도합니다!\n\n"
                if "최진영" in selected_guards:
                    hour_log += "> 💉 :red[**[무력화]**] 최진영이 보안프로그램을 작동시켜, 사악한 해킹공격을 저지합니다!\n\n"
            elif hour == 24:
                hour_log += "> 과제 끝! 제출 버튼만 누르면...!\n\n"

            # 패스 기믹 처리
            if "정하윤" in selected_guards and hour % 4 == 0:
                hour_log += "> ♠️  **[마이티하자]** 하윤이가 마이티를 하기 위해 당신을 숨겼습니다. (전투 패스)\n\n"
                battle_logs += hour_log
                log_container.markdown(battle_logs)
                time.sleep(0.3)
                continue
            if reverse_jungin == True:
                reverse_jungin = False
                hour_log += "> 😡 **[역정인정인]** 이정인이 빼앗긴 노트북을 겨우 다시 찾아옵니다. (전투 패스)\n\n"
                battle_logs += hour_log
                log_container.markdown(battle_logs)
                time.sleep(0.3)
                continue

            # 🪖 경평
            if is_buisness and hour % 6 == 0:
                buisness_penalty = buisness_count_sim * 4
                ji_perm_debuff += buisness_penalty
                hour_log += f"> 💰 :blue[**[시너지 발동: 경영평균]**] {buisness_count_sim}인의 원론을 겪은 경영인들이 모여 사오정을 방지합니다! (칼리 영구 위력 -{buisness_penalty})\n\n"


            #송재원 복귀 기믹
            if jawon_alive == 1 and random.random() < 0.1:
                selected_guards.append("송재원")
                jawon_alive = 2
                hour_log += ">  👋 **[나 다시 왔어]** 송재원 복귀\n\n"

            # 호위 전력 및 주사위 난수 계산
            current_team_power = persistent_power_bonus + carried_shield # 영구 버프(바퀴 황제 등)부터 시작
            if carried_shield > 0:
                hour_log += f"> 💪 **[기세 유지]** 이전 시간의 압도적인 우위로 기세를 이어갑니다. (이월된 방어선 +{carried_shield})\n\n"
                carried_shield = 0 # 적용했으니 다음 턴을 위해 다시 0으로 초기화합니다.
            if len(selected_guards) == 0:
                current_team_power = 0
                hour_log += "> 😨 **[동사0]** 곁을 지켜주던 모든 동아리원이 탈주했습니다. 운명이 다가오고 있습니다...\n\n"
                
            for guard in selected_guards:
                base_power = guards_db[guard]["power"]
                max_dice = guards_db[guard]["dice"]
                if max_dice > 0:
                    roll = random.randint(1, max_dice)
                    current_team_power += (base_power + roll)

            for guard in selected_guards:
                base_power = guards_db[guard]["power"]
                max_dice = guards_db[guard]["dice"]
                if guard == "이유빈" and "권준혁" in selected_guards:
                    max_dice = max(5, max_dice // 2)

                if max_dice > 0:
                    roll = random.randint(1, max_dice)
                    current_team_power += (base_power + roll)
                    
                    # 🎯 필살기 발동 로직 - 주사위가 최댓값이 떴을 때!
                    if roll == max_dice:
                        if guard == "리카르도":
                            current_team_power += 15
                            hour_log += "> 🕶️ :red[**[전원, 처형이다!]**] 리카르도가 원한 문신의 힘을 끌어내 지면을 강타합니다!\n\n"
                            
                        elif guard == "에즈라":
                            current_team_power += 15
                            hour_log += "> 🦮 :red[**[유리아 공방 - 총공 모드, 마크 17!]**] 에즈라가 온갖 무기를 한꺼번에 전개하여 화력을 쏟아붓습니다!\n\n"
                        
                        elif guard == "모제스":
                            ji_perm_debuff += 10 
                            hour_log += "> 👁️ :red[**[붉은 점]**] 모제스가 연기 너머로 E.G.O의 가장 취약한 틈새를 꿰뚫어 봅니다! (칼리 영구 위력 -10)\n\n"
                        
                        elif guard == "뇌횡":
                            current_team_power += 20
                            hour_log += "> 🐯 :red[**[초절맹호살격난참]**] 뇌횡이 맹호의 기세로 적의 숨통을 끊을 난격을 꽂아 넣습니다!\n\n"
                        
                        elif guard == "어느 싱클레어":
                            current_team_power += 25
                            hour_log += "> 🐣 :red[**[취수낭랑 - 성]**] 어느 싱클레어의 할버드와 대검이 붉은안개의 참격을 깔끔하게 흘려냅니다!\n\n"
                        
                        elif guard == "산초":
                            current_team_power += 30
                            blood_gauge += 50
                            hour_log += "> 🩸 :red[**[아류 산초 경혈식 - 라 샹그레]**] 산초가 끓어오르는 피를 창끝에 모아 폭발시킵니다!\n\n"
                        
                        elif guard == "니콜라이":
                            current_team_power += 35
                            hour_log += "> 🎯 :red[**[처분]**] 니콜라이가 붉은안개에게 처분 표식을 새겨넣고, 검으로 주홍빛 궤적을 그려냅니다!\n\n"
                        
                        elif guard == "샤오":
                            current_team_power += 35
                            hour_log += "> 🐉 :red[**[도철]**] 샤오가 불타오르는 언월도를 휘두르며 거대한 화염의 용을 뿜어냅니다!\n\n"
                        
                        elif guard == "엄지 아비 발렌치나":
                            current_team_power += 35
                            hour_log += "> 🤺 :red[**[처분]**] 발렌치나가 원망을 실은 칼날 두 자루를 무자비하게 휘두릅니다!\n\n"
                        
                        elif guard == "중지 아비 마티아스":
                            current_team_power += 35
                            hour_log += "> ⛓️ :red[**[즉결처형 - 레바테인]**] 마티아스가 장부의 기록에 따라 피할 수 없는 징벌을 내립니다!\n\n"
                        
                        elif guard == "노란작살 베스파":
                            current_team_power += 40
                            hour_log += "> 🐝 :red[**[섬봉광검술 - 환도]**] 베스파가 시야에서 사라진 순간, 사각을 파고드는 치명적인 참격이 작렬합니다!\n\n"
                        
                        elif guard == "검지 아비 뤼엔":
                            if "롤랑" in selected_guards:
                                current_team_power += 60
                                hour_log += "> 📜 :red[**[Furioso - Resonance]**] 뤼엔이 원본의 움직임에 완벽히 동기화하여 파괴적인 모방 난무를 펼칩니다!\n\n"
                            else:
                                current_team_power += 40
                                hour_log += "> 📜 :red[**[Furioso - Replica]**] 뤼엔이 헤르메스의 의지로 검은침묵의 난무를 기괴하게 모방해냅니다!\n\n"
                        
                        elif guard == "붉은시선 베르길리우스":
                            current_team_power += 45
                            hour_log += "> 🩸 :red[**[죽은 혈귀를 위한 장례]**] 베르길리우스의 글라디우스가 피의 궤적을 그리며 주변을 압도합니다!\n\n"
                        
                        elif guard == "가치우":
                            current_team_power += 45
                            hour_log += "> 🍂 :red[**[천강성 - 격]**] 가치우의 봉에 다섯 개의 망이 감기고, 파괴적인 힘을 뿜어냅니다!\n\n"
                        
                        elif guard == "푸른잔향 아르갈리아":
                            current_team_power += 50
                            hour_log += "> 🎼 :red[**[최후의 선율]**] 아르갈리아가 광소하며 치명적인 진동의 낫을 휘두릅니다!\n\n"
                        
                        elif guard == "롤랑":
                            if "검지 아비 뤼엔" in selected_guards:
                                current_team_power += 75
                                hour_log += "> ⬛ :red[**[Furioso - Original]**] 롤랑이 모조품 앞에서 원본의 품격을 보여줍니다!\n\n"
                            else:
                                current_team_power += 50
                                hour_log += "> ⬛ :red[**[Furioso]**] 롤랑이 9개의 무기를 꺼내어 숨 쉴 틈 없는 난무를 펼칩니다!\n\n"
                        
                        elif guard == "검은침묵 안젤리카":
                            current_team_power += 50
                            hour_log += "> 🧤 :red[**[백색 왈츠]**] 안젤리카가 무도회를 거닐듯 우아하고도 파괴적인 공방 무기 연계를 선보입니다!\n\n"
                        
                        elif guard == "보라눈물 이오리":
                            current_team_power += 50
                            hour_log += "> 🐍 :red[**[환영난무]**] 보라눈물이 여러 차원의 자세를 동시에 전개하여 회피불능의 참격을 날립니다!\n\n"
                        
                        elif guard == "처형자 바랄":
                            current_team_power += 55
                            hour_log += "> 💉 :red[**[혈청 R]**] 바랄이 혈청 R을 투여하여 폭발적인 기세로 칼리에게 돌진합니다!\n\n"
                        
                        elif guard == "바퀴 황제":
                            current_team_power += 60
                            hour_log += "> 🪳 :red[**[황제의 적출]**] 진화를 거듭한 황제가 거대한 껍데기를 휘둘러 대지를 짓뭉갭니다!\n\n"
                        
                        elif guard == "핏빛 밤 엘레나":
                            current_team_power += 70
                            hour_log += "> 🧛‍♀️ :red[**[핏빛 밤의 진노]**] 엘레나가 굶주림을 개방하여 시야에 보이는 모든 것을 찢어발깁니다!\n\n"
                        
                        elif guard == "장로 돈키호테":
                            current_team_power += 85
                            blood_gauge += 50
                            hour_log += "> 🎠 :red[**[돈키호테류 경혈 오의 - 구]**] 장로 돈키호테가 만든 피의 구가 폭발하며 전장을 뒤덮습니다!\n\n"

                    # 💥 대실패 발동 로직 - 주사위가 1이 떴을 때
                    elif roll == 1:
                        # 1. 오유찬 (기본 패시브)
                        if guard == "오유찬":
                            half_power = base_power // 2
                            penalty = (base_power + 1) - half_power
                            current_team_power -= penalty
                            hour_log += f"> ⏲️  **[네무리]** 오유찬은 이현재를 슬프게하지 않기 위해 잠에서 깼다! 억지로 졸음을 쫓아 방어선의 절반({half_power})은 사수해냅니다!\n\n"
                        
                        # 2. 요리 시너지 시 발동
                        elif guard == "이유빈" and "권준혁" in selected_guards:
                            hour_log += "> 👨‍🍳 👩‍🍳 :blue[**[시너지 발동: 요리사]**] 권준혁의 개입이 이유빈의 망한 요리를 살려냅니다! (대실패 면역)\n\n"
                        # 3. 다리부러짐
                        elif guard == "이아람" and leg_broke == False:
                            current_team_power -= 50
                            leg_broke == True
                            hour_log += "> 🦵 :red[**[다리부상]**] 아람이가 다리를 헛디뎌 부원들이 정신이 팔린 사이 이정인이 기회를 노립니다! (방어선 감소)\n\n"
                        elif guard == "송재원":
                            jawon_alive = 0
                            selected_guards.remove("송재원")
                            hour_log += "> :red[**[다시 도망치기]**] 바빠서 다음에 다시 올게~\n\n"
                        else:
                            current_team_power -= (base_power + 1) # 방금 더했던 위력을 다시 빼서 0으로 무효화
                            hour_log += f"> 💤  **[잠듦]** {guard}은(는) 깜빡 졸아버렸습니다... ({guard} 공격 모두 취소)\n\n"
                            missed_guards_this_turn.append(guard)

                        
                        
                    if guard == "류신해":
                        actual_victims = [g for g in previous_missed_guards if g != "류신해"]
                        if actual_victims:
                            retaliation_bonus = 30 * len(actual_victims)
                            current_team_power += retaliation_bonus   
                            victims_str = ", ".join(actual_victims)
                            hour_log += f"> 🪓 **[분노]** {victims_str}의 트롤링에 빡친 류신해가 야구방망이를 휘두릅니다. (+{retaliation_bonus})\n\n"      

            if "김유영" in selected_guards: 
                #current_team_power *= 1.2
                if hour == 1:
                    hour_log += "> 🍞🍞🍞 **:green[동두천의 가호가 함께합니다.]** \n\n"            

            if "임주성" in selected_guards: 
                current_team_power *= 1.2
                if hour == 1:
                    hour_log += "> 🧐 **[어설픈 리더]** 임주성의 지도를 통해, 아군 전체의 방어 점수가 1.2배 증폭됩니다.\n\n"

            if "정진성" in selected_guards: 
                if hour == 1:
                    hour_log += "> 🥱 **[차분함]** 정진성이 차분하게 부원들을 진정시켜 기세 유지에 도움을 줍니다. (이월 방어 보너스)\n\n"

            if "송재원" in selected_guards and hour == (1 + song_noh):
                jawon_alive = 1
                selected_guards.remove("송재원")
                hour_log += "> 🤾 :red**[얘들아 먼저 갈게~~~]** 송재원이 도망갔습니다.\n\n"

            if "이준혁" in selected_guards and "이준혁" not in missed_guards_this_turn and random.random() < 0.30:
                ezra_buff = random.randint(5, 25)
                current_team_power += ezra_buff
                hour_log += f"> 🛎️ **[할리갈리 승부]** 이준혁이 책장에서 할리갈리를 뽑아옵니다. (+{ezra_buff})\n\n"
                if "최진영" in selected_guards and "최진영" not in missed_guards_this_turn:
                    extra_buff = random.randint(5, 25)
                    current_team_power += extra_buff
                    hour_log += f"> ⚔️ :blue[**[시너지 발동: 할리갈리 진심녀]**] 이준혁의 자극을 받은 최진영이 종을 마구 난타합니다! (+{extra_buff})\n\n"

            # 기믹 처리
            if "장준혁" in selected_guards and hour % 3 == 0 and "장준혁" not in missed_guards_this_turn:
                current_team_power += 30
                hour_log += "> 🔫 **[불침번]** 군인정신이 남아있는 장준혁이 방어에 집중합니다. (이번 시간 방어선 +30)\n\n"
                
            if "이유빈" in selected_guards and "이유빈" not in missed_guards_this_turn: 
                angelica_buff = random.randint(5, 45)
                current_team_power += angelica_buff
                hour_log += f"> 🍮 **[제빵]** 이유빈이 직접 만든 에그타르트를 꺼냅니다. (추가 방어 점수 +{angelica_buff})\n\n"


            # 적 기본 공격력 결정
            if hour <= 12:
                ji_max_roll = 10 if "이아람" in selected_guards else 20
                ji_max_roll = 20
                ji_base = 50 + (hour * 5) 
                ji_roll = random.randint(ji_base - 10, ji_base + ji_max_roll)

            else:
                ji_max_roll = 15 if "이아람" in selected_guards else 40
                ji_max_roll = 40
                ji_base = 100 + ((hour - 12) * 20) 
                ji_roll = random.randint(ji_base - 15, ji_base + ji_max_roll)
                if hour == 21:
                    if "최진영" in selected_guards:
                        ji_roll = 0
                    else:
                        ji_roll = 300

            # 다수의 적을 상대할 때 칼리의 투지 상승
            crowd_bonus = len(selected_guards) * 15
            ji_roll += crowd_bonus
            
            if hour == 1 and len(selected_guards) >= 3:
                hour_log += f"> 🔴 :red**[조별과제]** 우리의 부원 수반큼 이정인이 경영학부 조원들을 대동합니다... (매 턴 위력 +{crowd_bonus})\n\n"

            # 디버프 적용 계산 (화상, 베스파, 롤랑 등)
            burn_debuff = (3 if "이준혁" in selected_guards else 0) + (spam)
            current_burn_penalty = burn_debuff * ((hour + t_gear_triggers) // 2)
            temp_debuff = current_burn_penalty + ji_perm_debuff
            

            if current_burn_penalty > 0:
                hour_log += f"> 🖼️ :orange**[사진 마구 보내기]** 이준혁의 스팸문자가 이정인의 정신을 흐트려 갉아먹어 위력을 {current_burn_penalty}만큼 깎아냅니다.\n\n"
            
            if "노현경" in selected_guards and hour % 3 == 0 and "노현경" not in missed_guards_this_turn: 
                # 기본 30 + 지난 격차의 20% 보너스
                tactical_bonus = int(last_hour_gap * 0.2)
                temp_debuff += (30 + tactical_bonus)
                hour_log += f"> 🍰  **[긴급간식보급]** 여유로워진 노현경이 동방에 디저트를 잔뜩 싸들고옵니다. (이정인의 위력 -30 / 간식 보너스 +{tactical_bonus})\n\n"
            
            # 기믹 처리
            if "양서진" in selected_guards:
                if is_ysj_berserk:
                    current_team_power += 9999 
                    ji_perm_debuff += 25 
                    
                    hour_log += "> ⬛ **[아빠어디가!!!]** 아버지가 탈주하자 양서진이 온갖 호들갑을 떱니다! (플레이어 무적 / 이정인 위력 지속적으로 -25)\n\n"
                    if random.random() < 0.30:
                        selected_guards.remove("양서진")
                        hour_log += "> 🥀 **[아버지 찾으러 가요]** 양서진도 아버지의 뒤를 따라 사라져버렸습니다...\n\n"
                    else:
                        hour_log += "\n"
                        

            if "이아람" in selected_guards and "이아람" not in missed_guards_this_turn:
                hour_log += "> 😀 **[위력 억제]** 이아람의 무해한 웃음으로 이정인의 위력 최댓값이 억제되고 있습니다.\n\n"

            # 최종 공격력 산출
            effective_ji_attack = int((ji_roll) * aggro_multiplier)
            if effective_ji_attack < 0: effective_ji_attack = 0


            # 모제스의 연기 디버프 (최종 위력 10% 감소)
            if "윤석준" in selected_guards and hour % 2 == 0 and "윤석준" not in missed_guards_this_turn:
                reduction = int(effective_ji_attack * 0.1)
                effective_ji_attack -= reduction
                hour_log += f"> 👀  **[위력감소]** 윤석준이 예민한 감각으로 순찰을 돌아 이정인의 집중을 흐트러뜨립니다. (감소된 위력: {reduction})\n\n"

            # 뤼엔의 지령 회피 (15% 확률로 위력 0)
            if "전재환" in selected_guards and random.random() < 0.15 and "전재환" not in missed_guards_this_turn:
                effective_ji_attack = 0
                hour_log += "> 📜 **[선배의 도움]** 전재환이 먼저 에세이의 오타를 지적해 이정인의 개입을 완벽히 방어합니다. (공격 무효화)\n\n"

            if effective_ji_attack < 0: effective_ji_attack = 0

            #최종 방어 판정
            if "류혜정" in selected_guards and abs(effective_ji_attack - current_team_power) <= 20 and "류혜정" not in missed_guards_this_turn:
                persistent_power_bonus += 25
                hour_log += "> 🔩 **[금속스튜디오 과제물로 만들어주지]** 위기의 순간 류혜정이 전기톱을 꺼내 영구적인 흐름을 가져옵니다. (영구 방어선 +25)\n\n"
                
                # 만약 방어선이 뚫릴 뻔했다면, 강제로 방어 점수를 끌어올려 세이브
                if current_team_power < effective_ji_attack:
                    current_team_power = effective_ji_attack


            time.sleep(0.3)
            if current_team_power >= effective_ji_attack:
                if "한성원" in selected_guards: 
                    # 13시간 이전에는 +4, E.G.O 발현 이후에는 +8로 성장폭 대폭 증가
                    emp_bonus = 6 if hour >= 13 else 4
                    persistent_power_bonus += emp_bonus
                    hour_log += f"> 🤣 **[웃음테러]** 동방을 웃음바다로 만들어 사기를 크게 끌어올립니다. (영구 방어선 +{emp_bonus})\n\n"
                hour_log += f"> 🛡️ **[방어 성공]** (정인's 공격력: {effective_ji_attack} / 동아리 방어선: {int(current_team_power)})\n\n"
            else:
                # 0순위 생존기
                if "양서진" in selected_guards and "임주성" in selected_guards:
                    selected_guards.remove("임주성")
                    is_ljs_alive = False
                    is_ysj_berserk = True
                    hour_log += "> 🤸‍♂️ :red**[아버지의 도망]** 어느순간 임주성이 갑자기 사라져있었습니다.\n\n"
                    hour_log += "> 🤬 :red**[딸의 절규]** 아버지에게 배신당한 양서진의 눈빛에 섬뜩한 광기가 차오릅니다...\n\n"
                # 1순위 생존기: 마티아스의 강제 희생
                elif "김동규" in selected_guards and len(selected_guards) > 1:
                    # 조건이 만족되었을 때(elif 안쪽) 비로소 명단을 작성합니다.
                    available_sacrifices = [g for g in selected_guards if g != "김동규"]
                    sacrifice = random.choice(available_sacrifices)
                    selected_guards.remove(sacrifice)
                    if sacrifice == "임주성":
                        is_ljs_alive = False
                    sacrifice_power = guards_db[sacrifice]["power"]
                    debuff_amount = int(sacrifice_power * 0.5)
                    ji_perm_debuff += debuff_amount
                    
                    hour_log += f"> 😛  :red**[맛보기]** 방어선이 무너지자, 김동규가 충동적으로 곁에 있던 **{sacrifice}**를 이정인에게 맛보기로 던져버립니다.\n\n"
                    hour_log += f"> 😵 **[부원 희생됨ㅠㅠ / 이정인의 영구 위력 {debuff_amount} 감소 / 이번 턴 강제 생존]**\n\n"
                elif blood_gauge >= 50:
                    blood_gauge -= 50
                    hour_log += f"> 😎 :orange**[잼얘로 시간끌기]** 잼얘를 소모하여 버텼습니다. (남은 잼얘: {blood_gauge})\n\n"
                elif com_secu > 0:
                    com_secu -= 1
                    hour_log += f"> 💉 :orange**[컴과의 기지]** 네이버 계정이 털리려는 순간 비밀번호를 변경해 계정을 지켜냅니다. (남은 회피: {com_secu})\n\n"
                elif "강준서" in selected_guards and not gjs_shield_used:
                    gjs_shield_used = True
                    reverse_jungin = True
                    hour_log += f"> 🦹 :orange**[리버스 정인]** 위기의 순간, 강준서가 이정인을 밀쳐내고 이정인의 노트북을 정인해갔습니다!\n\n"
                elif has_noro:
                    has_noro = False
                    ji_perm_debuff += 30  # 시간 역행으로 칼리의 위력 스노우볼을 깎아버림
                    hour_log += f"> 🧻 :orange[**[노로바이러스]**] 방어선이 붕괴된 순간, 이정인에게 굴을 먹여 노로바이러스에 감염시킵니다! 녀석 후퇴하는 꼴이 좋군요.\n\n"
                    hour_log += f"> ⚠️ **(강제 생존 / 이정인의 위력이 영구적으로 30 감소)**\n\n"
                elif revives_left > 0:
                    revives_left -= 1
                    if is_ljs_alive and random.random() < 0.5: is_ljs_alive = False
                    hour_log += f"> 🍲 :orange[**[두번은 해야지]**] 아 나 네이버 계정 안주면 조별과제 안함;;; (남은 김치찜: {revives_left})\n\n"


                else:
                    hour_log += f"> 💀 :red**[방어선 붕괴]** 이정인에게 에세이를 빼앗겼습니다. (정인's 위력: {effective_ji_attack} / 동아리 방어선: {int(current_team_power)})\n\n"
                    battle_logs += hour_log
                    log_container.markdown(battle_logs)
                    survival_status = False
                    break

            # 시간 경과 후처리 기믹
            raw_gap = abs(effective_ji_attack - current_team_power)
            last_hour_gap = min(300, raw_gap) 
            if current_team_power > effective_ji_attack and raw_gap >= 50:
                if current_team_power >= 9000:
                    carried_shield = 0
                elif "정진성" in selected_guards and "정진성" not in missed_guards_this_turn:
                    carried_shield = int(raw_gap * 0.5)
                else:
                    carried_shield = int(raw_gap * 0.3) # 초과분의 30%를 다음 턴으로 이월
            else:
                carried_shield = 0
            
            battle_logs += hour_log
            log_container.markdown(battle_logs)
            previous_missed_guards = missed_guards_this_turn.copy()


        # 결과 출력
        st.write("---")
        if survival_status:
            st.success(f"🎉 **미션 성공!** {target_hours}시간 안에 과제를 제출하는데 성공했습니다. 현재가 기쁨의 눈물을 흘립니다.")
        else:
            st.error("❌ **미션 실패!** 에세이는 강탈당했고, 결과는 사오정입니다!")

        st.write("---")
        
        final_report = f"#### 🛡️ 밥약 건 부원 및 간식\n> 부원: {', '.join(initial_guards)}\n> 간식: {', '.join(initial_items)}\n\n"
        final_report += battle_logs

        clean_report = re.sub(r':[a-zA-Z]+\[(.*?)\]', r'\1', final_report)
        clean_report = clean_report.replace('**', '')
        clean_report = clean_report.replace('\n\n>', '\n>')

        # 2. 클릭 한 번으로 복사할 수 있도록 원문 코드를 숨겨두는 구역 (보관용)
        with st.expander("📋 기록 원문 복사하기"):
            st.code(clean_report, language="text")
