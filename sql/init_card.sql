insert into cards_card (id, card_number, card_type, name, score, command)
values (1, 'ACTION_01', 'action', '곡식 활용', 0, 'minus("vegi", prop 1) 또는 minus("grain", prop 2)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (2, 'ACTION_02', 'action', '울타리', 0, 'minus("wood", prop 1), plus("fence", prop 2), 설치(프론트값)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (3, 'ACTION_03', 'action', '주요 설비', 0, '주요/보조 선택, 선택된 주요/보조 조건 확인, 주요/보조 활성화')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (4, 'ACTION_04', 'action', '양시장', 0, 'plus("sheep", accum ), 양 배치')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (5, 'ACTION_05', 'action', '서부 채석장', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (6, 'ACTION_06', 'action', '집 개조', 0,
        'minus("reed",1) , minus(prop1, prop2) , 주요/보조 선택, 선택된 주요/보조 조건 확인, 주요/보조 활성화')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (7, 'ACTION_07', 'action', '기본 가족 늘리기', 0, 'plus("family", 1), 보조 조건 확인, 보조 활성화 ,')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (8, 'ACTION_08', 'action', '돼지 시장', 0, 'plus("pig", accum), 돼지 배치')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (9, 'ACTION_09', 'action', '채소 종자', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (10, 'ACTION_10', 'action', '동부 채석장', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (11, 'ACTION_11', 'action', '소 시장', 0, 'plus("cow", accum), 소 배치')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (12, 'ACTION_12', 'action', '밭 농사', 0, 'plus("field", 1), 밭 배치')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (13, 'ACTION_13', 'action', '급한 가족 늘리기', 0, 'plus("family", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (14, 'ACTION_14', 'action', '농장 개조', 0, 'minus("reed",1) , minus(prop1, prop2) , minus("wood", prop1), 울타리 설치')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (15, 'JOB_01', 'job', '양의 친구', 0,
        '현재 라운드의 2,5,8,10을 더한 라운드가 되면 양을 1마리씩 얻는다. ( cond(round, self.round+2,5,8,10 , add("sheep",1)) ) 양을 공')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (16, 'JOB_02', 'job', '목사', 0, '방이 2개 뿐인 집에 사는 유일한 플레이어? -> 나무3개 흙 2개 갈대 1개 돌 1개 획득')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (17, 'JOB_03', 'job', '벽 건축가', 0, '방을 만들 때, 다음 4개의 라운드 동안 라운드 시작 시 음식 1개 획득')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (18, 'JOB_04', 'job', '마부', 0, 'plus("wood",1) , 돌집에 살고있다면? -> 남은 모든 라운드 시작 시 나무 1개를 외양간 1개로 교환 가능')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (19, 'JOB_05', 'job', '소규모 농부', 0, '방이 2개 뿐인 집에 살면? -> 라운드 시작 시 plus("wood", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (20, 'JOB_06', 'job', '쟁기 몰이꾼', 0, '돌 집에 살면? -> 라운드 시작 시 선택 -> plus("field", 1) , minus("food", 1) 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (21, 'JOB_07', 'job', '학자', 0, '돌 집에 살면? -> 라운드 시작 시 선택 -> 보조 또는 직업 획득 -> 직업은 음식 1개 minus , 보조는 조건')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (22, 'JOB_08', 'job', '하인', 0, '돌 집에 살면? -> 라운드 시작 시 plus("food", 3)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (23, 'JOB_09', 'job', '무자식', 0,
        'room>=3, family == 2 ? -> 라운드 시작 시 plus("food", 1) , 선택 -> plus("vegi", 1) 또는 plus("grain", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (24, 'JOB_10', 'job', '흙집 건축업자', 0, '나무집 아니면? -> 다음 5라운드 동안 plus("soil", 2)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (25, 'JOB_11', 'job', '지붕 다지는 사람', 0, 'minus("food", 1), plus("stone", player.room)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (26, 'JOB_12', 'job', '상담가', 0, 'plus("sheep", 2)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (28, 'JOB_13', 'job', '사제', 0, 'room == 2 , 흙집? -> plus("soil", 3), plus("stone", 2), plus("reed", 2)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (29, 'JOB_14', 'job', '가마 떼는 사람', 0, '나무 누적 행동 칸 이용 시 -> 선택 -> 빵 굽기 행동 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (30, 'JOB_15', 'job', '양부모', 0, '가족 늘리기 행동 칸 이용 시 -> 선택 -> minus("food", 1), is_kid = false 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (31, 'JOB_16', 'job', '재산관리인', 0, '집 고치는 행동 칸 이용시 -> 돌집 코스트 받고 바로 돌집')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (32, 'JOB_17', 'job', '골조 건축업자', 0, '집 고치는 행동 칸 혹은 방 만드는 행동 칸 이용 시 -> 흙 2개 대신 나무 1개 또는 돌 2개 대신 나무 1개')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (33, 'JOB_18', 'job', '채소 장수', 0, '곡식 종자 행동 칸 이용 시 -> plus("vegi", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (34, 'JOB_19', 'job', '류트 연주자', 0,
        '나를 제외한 플레이어가 유랑극단 행동 칸 이용 시 -> plus("food", 1) , plus("wood", 1)  선택 -> minus("food", 2) , plus("veg')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (35, 'JOB_20', 'job', '소 사육사', 0, '곡식 종자 행동 칸 이용 시 -> 선택 -> minus("food", 1) , plus("cow", 1) 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (36, 'JOB_21', 'job', '장작 채집자', 0,
        '농지 또는 곡식 종자 또는 곡식 활용 또는 밭 농사 행동 칸 이용시 -> plus("wood", 1) 근데 이제.. 차례가 끝날 때 줘서 당장은 못쓰는 나무 형태로..')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (37, 'JOB_22', 'job', '농번기 일꾼', 0,
        '날품팔이 행동 칸 이용시 -> plus("grain", 1)  if(round>=6) {선택 -> plus("grain", 1) 또는 plus("vegi", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (38, 'JOB_23', 'job', '오두막집살이', 0, '날품팔이 행동 칸 이용시 -> 선택 -> 집 고치기 액션 또는 방 만들기 (1개만 가능) 액션')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (39, 'JOB_24', 'job', '작살꾼', 0,
        '낚시 행동 칸 이용시 -> 선택 -> minus("wood", 1), plus("food", player.family), plus("reed", 1) 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (40, 'JOB_25', 'job', '창고 관리인', 0, '자원 시장 행동 칸 이용시 -> 선택 -> plus("soil", 1) 또는 plus("grain", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (41, 'JOB_26', 'job', '산울타리지기', 0, '울타리 치기 행동 칸 이용시 -> plus("fence", 3) (울타리 3개 무료 제공)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (42, 'JOB_27', 'job', '숙련 벽돌공', 0, '주요 설비 행동 칸 이용시 -> 주요설비 선택하면? -> cost에서 돌을 room-2만큼 빼줌')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (43, 'JOB_28', 'job', '돌 자르는 사람', 0, '설비 또는 방 만들기 또는 집 고치기 행동 칸 이용시 -> cost에서 돌 1개 빼줌')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (44, 'JOB_29', 'job', '가축 상인', 0,
        '양 시장 또는 돼지 시장 또는 소 시장 행동 칸 이용 시 -> 선택 -> minus("food", 1), plus("해당 시장 가축", 1) 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (45, 'JOB_30', 'job', '지질학자', 0, '숲 또는 갈대밭 또는 흙 채굴장 행동 칸 이용시 -> plus("soil", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (46, 'JOB_31', 'job', '나뭇가지 모으는 사람', 0, '방 만들기 또는 집 고치기 행동 칸 이용시 -> 선택 -> 필요한 cost 중 갈대를 나무 1개로 바꿈 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (47, 'JOB_32', 'job', '목수', 0, '방 만들기 행동 칸 이용시 -> cost에서 갈대를 제외한 필요 cost 2개 빼줌')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (48, 'JOB_33', 'job', '보조 경작자', 0, '날품팔이 행동 칸 이용시 -> 선택 -> plus("field", 1) , 밭 배치 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (49, 'JOB_34', 'job', '나무꾼', 0, '누적 나무 행동 칸 이용시 -> plus("wood", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (50, 'JOB_35', 'job', '버섯 따는 사람', 0, '누적 나무 행동 칸 이용시 -> 선택 -> 나무 한 개 누적 칸에 남겨놓고, plus("food", 2) 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (51, 'JOB_36', 'job', '초벽질공', 0, '방 만들기 또는 집 고치기 행동 칸 이용시 -> 흙집이면? -> plus("food", 3)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (52, 'JOB_37', 'job', '마술사', 0, '유랑극단 행동 칸 이용시 -> plus("wood", 1), plus("grain", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (53, 'JOB_38', 'job', '잡화상인', 0,
        '아무 때나, 선택 -> minus("food", 1) plus(prop1, 1) (나무 - 곡식 - 갈대 - 돌 - 채소 - 흙 - 갈대 - 채소 리스트에서 차례대로 prop1에')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (54, 'JOB_39', 'job', '양 보행자', 0,
        '아무 때나, 선택 -> minus("sheep", 1), plus("pig", 1) 또는 minus("sheep", 1), plus("vegi", 1) 또는 minus("sheep')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (55, 'PRI_FAC_01', 'pri_fac', '우물', 4, '다음 5라운드 간 라운드 시작 시 plus("food", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (56, 'PRI_FAC_02', 'pri_fac', '바구니 제작소', 2,
        '수확 시? -> 선택 -> minus("reed", 1), plus("food", 3) 또는 NONE 계산 시? -> if(reed>=5) score+=3 	elif(reed>=4')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (57, 'PRI_FAC_03', 'pri_fac', '그릇 제작소', 2,
        '수확 시? -> 선택 -> minus("soil", 1), plus("food", 2) 또는 NONE 계산 시? -> if(soil>=7) score+=3 	elif(soil>=5')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (58, 'PRI_FAC_04', 'pri_fac', '가구 제작소', 2,
        '수확 시? -> 선택 -> minus("wood", 1), plus("food", 2) 또는 NONE 계산 시? -> if(wood>=7) score+=3 	elif(wood>=5')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (59, 'PRI_FAC_05', 'pri_fac', '화덕', 1,
        '아무 때나, 선택 -> minus("vegi", prop 1), plus("food", prop 1 * 3) 또는 minus("pig", prop 1), plus("food", p')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (60, 'PRI_FAC_06', 'pri_fac', '화로', 1,
        '아무 때나, 선택 -> minus("vegi", prop 1), plus("food", prop 1 * 2) 또는 minus("pig", prop 1), plus("food", p')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (61, 'PRI_FAC_07', 'pri_fac', '화덕', 1,
        '아무 때나, 선택 -> minus("vegi", prop 1), plus("food", prop 1 * 3) 또는 minus("pig", prop 1), plus("food", p')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (62, 'PRI_FAC_08', 'pri_fac', '화로', 1,
        '아무 때나, 선택 -> minus("vegi", prop 1), plus("food", prop 1 * 2) 또는 minus("pig", prop 1), plus("food", p')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (63, 'PRI_FAC_09', 'pri_fac', '돌가마', 3,
        '설비가 activate될 때 -> 빵 굽기 행동 빵 굽기 행동 시? -> 선택 -> prop 1은 2보다 작거나 같아야 함.. minus("grain", prop 1), plus(')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (64, 'PRI_FAC_10', 'pri_fac', '흙가마', 2,
        '설비가 activate될 때 -> 빵 굽기 행동 빵 굽기 행동 시? -> 선택 -> minus("grain", 1), plus("food", 5) 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (65, 'SUB_FAC_01', 'sub_fac', '부엌방', 0, '라운드 시작 시? -> 나무집이면? -> plus("food", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (66, 'SUB_FAC_02', 'sub_fac', '대형온실', 0, '현재 라운드 +4, 7, 9 라운드 시작 시 -> plus("vegi", 1) 얘도 미리 빼놔야 됨..')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (67, 'SUB_FAC_03', 'sub_fac', '연못 오두막', 1, '다음 3개의 라운드 동안 라운드 시작 시 -> plus("food", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (68, 'SUB_FAC_04', 'sub_fac', '손수레', 0, '5, 8, 11, 14 라운드 시작 시 -> plus("grain", 1) 얘도 미리 빼놔야 됨..')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (69, 'SUB_FAC_05', 'sub_fac', '딸기포', 2, '다음 3개의 라운드 동안 라운드 시작 시 -> plus("food", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (70, 'SUB_FAC_06', 'sub_fac', '손쟁기', 0, '현재 라운드 +5 라운드 시작 시 -> plus("field", 1), 밭 배치')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (71, 'SUB_FAC_07', 'sub_fac', '울창한 숲', 0, '짝수 라운드 시작 시? -> plus("wood", 1) 얘도 미리 빼놔야 됨..')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (72, 'SUB_FAC_08', 'sub_fac', '도토리 바구니', 0, '다음 2개의 라운드 동안 라운드 시작 시 -> plus("pig", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (73, 'SUB_FAC_09', 'sub_fac', '우유 주전자', 0,
        'if(''소 시장'' .is_used==true)-> if(카드 소유자) plus("food", 3) else plus("food", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (74, 'SUB_FAC_10', 'sub_fac', '청어 냄비', 0, '낚시 행동 칸 이용시 -> 다음 3라운드 동안 plus("food", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (75, 'SUB_FAC_11', 'sub_fac', '올가미 밧줄', 0, '양 시장 또는 돼지 시장 또는 소 시장 행동 칸 이용 시 -> 선택 -> 즉시 턴 또는 NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (76, 'SUB_FAC_12', 'sub_fac', '타작판', 1, '농지 또는 밭 농사 행동 칸 이용시 -> 선택 -> 빵굽기 OR NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (77, 'SUB_FAC_13', 'sub_fac', '다진 흙', 0, 'plus("soil", 1) , 울타리 치기 행동 시? -> 나무 대신 흙 선택 가능')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (78, 'SUB_FAC_14', 'sub_fac', '통나무배', 1, '낚시 행동 칸 이용시 -> plus("food", 1), plus("reed", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (79, 'SUB_FAC_15', 'sub_fac', '채굴 망치', 0, 'plus("food", 1) , 집 고치기 행동 시 -> 선택 -> 외양간 짓기 OR NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (80, 'SUB_FAC_16', 'sub_fac', '바구니', 0, '나무 누적 행동 칸 이용 시 -> 선택 -> 나무 2개 남겨놓고 plus("food", 3) OR NONE')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (81, 'SUB_FAC_17', 'sub_fac', '목수의 객실', 0, '방 만들기 행동 시-> if(나무집) 만들기 나무cost-2')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (82, 'SUB_FAC_18', 'sub_fac', '양토 채굴장', 1, '날품팔이 행동 칸 이용시 -> plus("soil", 3)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (83, 'SUB_FAC_19', 'sub_fac', '목재소', 2, '모든 설비 cost에서 나무 -1')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (84, 'SUB_FAC_20', 'sub_fac', '개울', 0, '갈대밭, 흙 채굴장, 숲, 1라운드카드 이용 시 -> plus("food", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (85, 'SUB_FAC_21', 'sub_fac', '곡식용 삽', 0, '곡식 종자 행동 칸 이용 시 -> plus("grain", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (86, 'SUB_FAC_22', 'sub_fac', '폐품 창고', 0, '설비 내려 놓거나, 지을 때 -> plus("food", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (87, 'SUB_FAC_23', 'sub_fac', '빵삽', 0, 'plus("food", 1), 직업 놓을 시 -> 빵굽기 행동')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (88, 'SUB_FAC_24', 'sub_fac', '네덜란드식 풍차', 2, '수확 마친 다음 라운드(5, 8, 10, 12, 14)에 빵굽기 행동 시-> plus("food", 3)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (89, 'SUB_FAC_25', 'sub_fac', '돌 집게', 0, '돌 누적 칸 이용 시 -> plus("stone", 1)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (90, 'SUB_FAC_26', 'sub_fac', '이중날 쟁기', 0, '미친놈인데? 뺴야할 듯')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (91, 'SUB_FAC_27', 'sub_fac', '쇠스랑', 0, '곡식 종자 행동 칸 이용 시 -> if(농지 칸 이용 중일시) ->plus("food", 3)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (92, 'SUB_FAC_28', 'sub_fac', '경질 자기', 0,
        '아무 때나, minus("soil", 2), plus("stone", 1) OR minus("soil", 3), plus("stone", 2) OR ...')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (93, 'SUB_FAC_29', 'sub_fac', '삽', 0, '아무 때나, 작물 2 개 이상인 밭의 작물 빈 밭으로 이동 가능..... 미친놈인듯')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (94, 'SUB_FAC_30', 'sub_fac', '흙판', 0, 'plus("soil", player.resource.soil/2), 카드 넘김')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (95, 'SUB_FAC_31', 'sub_fac', '노점', 0, 'plus("vegi", 1), 카드 넘김')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (96, 'SUB_FAC_32', 'sub_fac', '작은 우리', 0, '1칸 짜리 우리 설치, 카드 넘김')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (97, 'SUB_FAC_33', 'sub_fac', '우시장', 0, 'plus("cow", 1), 카드 넘김')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (98, 'SUB_FAC_34', 'sub_fac', '이동 경작', 0, 'plus("field", 1), 밭 배치, 카드 넘김')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (99, 'SUB_FAC_35', 'sub_fac', '병', 4, 'minus("soil", player.family), minus("food", player.family)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (100, 'SUB_FAC_36', 'sub_fac', '거대 농장', 0, '남은 라운드 당 1점, 음식 2개')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (101, 'SUB_FAC_37', 'sub_fac', '버터 제조기', 1, '수확 시작 시-> plus("food", sheep/3), plus("food", cow/2)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (102, 'SUB_FAC_38', 'sub_fac', '삼포식 농법', 0, '수확 시작 시 -> if(곡식밭>=1&&채소밭>=1 && 빈 밭>=1) -> plus("food", 3)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (103, 'SUB_FAC_39', 'sub_fac', '물통', 0, '우리의 가축 최대 수용 수 +2')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (104, 'BASE_01', 'BASE', '덤불', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (105, 'BASE_02', 'BASE', '수풀', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (106, 'BASE_03', 'BASE', '자원 시장', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (107, 'BASE_04', 'BASE', '점토 채굴장', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (108, 'BASE_05', 'BASE', '교습', 0, 'cls.job_submit_card(player, round_card, info)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (109, 'BASE_06', 'BASE', '유랑극단', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (110, 'BASE_07', 'BASE', '농장 확장', 0, '코스트 내고 방 바꾸기')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (111, 'BASE_08', 'BASE', '회합 장소', 0, '선 바꾸기, 그리고/또는 보조설비')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (112, 'BASE_09', 'BASE', '곡식 종자', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (113, 'BASE_10', 'BASE', '농지', 0, 'plus("field", 1), 밭 배치')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (114, 'BASE_11', 'BASE', '교습', 0, 'cls.job_submit_card(player, round_card, info)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (115, 'BASE_12', 'BASE', '날품팔이', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (116, 'BASE_13', 'BASE', '숲', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (117, 'BASE_14', 'BASE', '흙 채굴장', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (118, 'BASE_15', 'BASE', '갈대밭', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
insert into cards_card (id, card_number, card_type, name, score, command)
values (119, 'BASE_16', 'BASE', '낚시', 0, 'cls.use_round_card_resources(player, round_card)')
ON CONFLICT(card_number) DO NOTHING;
