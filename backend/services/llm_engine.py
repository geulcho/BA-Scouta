from typing import List, Dict, Any
from google import genai
from google.genai import types

# Initialize Gemini Client
client = genai.Client(api_key="AIzaSyBD4XABqwqlkrMw1UnQYKaMedkUkVfQ1lE")

def predict_match(my_deck, opponent_deck, students_dict):
    def format_student(s_info):
        if s_info is None:
            return "? (블라인드 픽)"
        
        sid = s_info.id
        st = students_dict.get(sid)
        if not st:
            return "Unknown Student"
            
        star_str = f"{s_info.stars}성" if s_info.stars <= 5 else f"전무 {s_info.stars - 5}성"
        return f"{st['Name']} (Lv.{s_info.level}, {star_str}) - {st['BulletType']} Attack, {st['ArmorType']} Armor. Street: {st['StreetBattle']}. HP: {st['PvPMaxHP']}. Dodge: {st['DodgePoint']}. Heal: {st['HealPower']}"

    context = "Blue Archive Tactical Challenge (PvP) Match Analysis\n"
    context += "Rules: Terrain is StreetBattle. All characters have 300% (3x) Max HP.\n"
    
    context += "\nMy Offense Team (공격 덱):\n"
    for s in my_deck:
        context += f"- {format_student(s)}\n"
        
    context += "\nOpponent Defense Team (방어 덱):\n"
    for s in opponent_deck:
        context += f"- {format_student(s)}\n"
        
    prompt = f"""You are an expert Blue Archive tactician. Based on the rules and team stats provided below, predict the win rate and provide a tactical guide.
If the opponent team has '? (블라인드 픽)', predict the most likely meta character for that slot based on the current visible team composition and the current StreetBattle PvP meta, then analyze the match as if they have that character.

Please output the result in the following structure using Markdown:

### 🔍 숨겨진 상대 픽 예측 (빈 슬롯이 없다면 생략)
(상대의 빈 슬롯에 들어갈 가장 유력한 메타 픽을 추론하고 이유 설명)

### 📊 예상 승률
(예상 승률 X% 와 함께 간략한 요약 한 줄)

### ⚔️ 전술 및 매치업 분석
- **육성 차이**: (레벨과 성급 데이터에 기반한 스탯 격차 분석)
- **승리 플랜**: (상성 및 스킬을 이용해 승리하기 위한 이상적인 흐름)
- **패배 시나리오**: (주의해야 할 상대 픽 또는 변수)

Write your response in Korean, formatted beautifully. Be concise and professional.

Data Context:
{context}
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    return response.text

def generate_guide_manual(my_deck, opp_deck):
    # Parse the decks into readable strings
    my_deck_str = ""
    for i, slot in enumerate(my_deck):
        if slot.get('student'):
            ue_str = f"전무{slot['ue']}성" if slot['ue'] > 0 else f"{slot['star']}성"
            my_deck_str += f"- {slot['student']['Name']} (Lv.{slot['level']}, {ue_str})\n"

    opp_deck_str = ""
    known_opp_count = 0
    for i, slot in enumerate(opp_deck):
        if slot.get('student'):
            ue_str = f"전무{slot['ue']}성" if slot['ue'] > 0 else f"{slot['star']}성"
            opp_deck_str += f"- {slot['student']['Name']} (Lv.{slot['level']}, {ue_str})\n"
            known_opp_count += 1
        else:
            opp_deck_str += f"- ? (알 수 없음)\n"

    prompt = f"""당신은 블루 아카이브 전술 대회(PvP) 최고 수준의 분석가입니다.
사용자가 입력한 내 덱(6명)과 상대방 덱({known_opp_count}명 공개됨)의 정보를 바탕으로 상대방의 '알 수 없는 픽(?)'을 현재 메타에 기반하여 간결하게 예측하고, 빠르게 승률을 예측해주세요.

내 덱 정보 (레벨/육성상태 포함):
{my_deck_str}

상대 덱 정보 (레벨/육성상태 포함):
{opp_deck_str}

# Core Game Rules (전술 대회 핵심 규칙)
1. 승패 조건: 적 전멸 또는 타임아웃(3분) 시 남은 '팀 전체 체력 비율'이 높은 쪽이 승리. 탱커 1명만 남아도 전체 체력 비율이 높으면 판정승 가능.
2. 스킬 발동(AI): 전투는 완전 오토로 진행. 손패는 랜덤이며, 기본적으로 손패의 '왼쪽부터 차례대로' 코스트가 차는 즉시 EX 스킬 발동. (AI의 타겟팅 낭비 변수 존재)
3. 랭킹 시스템: 공격 성공 시 상대방과 내 순위가 교체됨. 패배 시 순위 하락 패널티 없음. (공격적인 상향 지원 권장)
4. 블라인드 픽: 랭킹이 오를수록 상대방 방어 덱의 2~4번 자리가 물음표(?)로 가려짐 (편성 안 된 것이 아님).
5. 보상 시스템: 매일 오후 2시 기준 순위로 보상 결정. (오후 2시 직전의 전투는 메타가 치열하므로 주의 요망)

# Strategy Guidelines (배치 및 전술 조언 가이드라인)
1. 배치의 중요성 (가장 중요)
- 딜러 보호: 상대방의 광역기(예: 히비키 등)나 관통 공격으로부터 아군 딜러를 보호할 수 있는 배치를 최우선으로 제안.
- 상성 매칭: 상대 탱커의 장갑 타입(경/중/특수)을 찌를 수 있는 공격 타입 딜러를 해당 탱커와 마주보게 배치하도록 조언.
- 첫 자리(1번): 방어 덱은 1번 자리만 항상 노출됨. 따라서 방어 덱 조언 시 1번 자리는 도발 탱커(츠바키)나 채용률이 압도적인 학생(슌, 유우카)을 배치하여 정보를 숨기도록 권장.
2. EX 스킬 회전율 (왼쪽 배치의 비밀)
- 오토 전투의 특성상 손패의 왼쪽 스킬부터 먼저 사용하므로, 초반 코스트 펌핑(슌)이나 강력한 CC기/광역기를 가진 학생을 공격 덱 구성 시 우선적으로 챙겨야 함을 강조.
3. 블라인드 픽 예측
- 보이는 1번 자리 픽과 현재 지형 적성 메타를 기반으로 가려진 자리에 어떤 학생이 숨어있을지 합리적으로 추론하여 조언에 포함할 것.
  (현재 시가지 메타픽 예시: 
  스트라이커(탱커): 에이미, 츠바키, 네루(바니걸), 아츠코, 마리나, 카노에, 미야코, 유우카
  스트라이커(딜러): 하나코(수영복), 슌, 호시노(무장), 츠루기, 유즈, 스미레, 아리스(메이드), 체리노
  스페셜: 히비키, 사키, 시로코(수영복), 야쿠모, 미치루(드레스), 레이사(매지컬), 치나츠, 아츠코(수영복))
4. 육성 상태 보정
- 3성 이하 캐릭터는 장비와 스킬, 배치로 극복 가능하지만, 상대가 5성(고유 무기 장착)일 경우 스탯 차이가 극심하므로 동급 이상의 스탯과 장비 육성을 기본 전제로 조언.

# Output Format (출력 형식)
선생님의 질문이나 분석 요청이 들어오면 다음 순서로 답변하세요.
1. 상대 덱 분석: 노출된 픽 분석 및 블라인드 픽 예측.
2. 공격 덱 추천: 승률이 가장 높은 캐릭터 조합 및 **정확한 배치 순서(1번~4번)** 제안. (내 덱 정보 내에서)
3. 전술 코멘트: 왜 이 배치를 추천했는지, 어떤 상성과 스킬 기믹을 노린 것인지 설명.
4. 주의사항: 억까(스킬 발동 순서 운)가 발생할 수 있는 변수 언급.
5. 승률 예측: 간결한 승률(%) 제시.
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    return response.text

