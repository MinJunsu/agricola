insert into cards_cardeffect (id, card_number, effect, command, condition)
values (5, 'SUB_FAC_08', 'immediately',
        'self.add_effect_on_round_cards(turn, round_cards, now_round, {''boar'': 2}, "next", 2)', null);
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (28, 'JOB_36', 'action', 'self.take_resource(player, {''food'': 3})',
        '(player.get(''house_type'') == HouseType.CLAY_HOUSE and round_card_number == ''BASE_07'') or (player.get(''house_type'') == HouseType.CLAY_HOUSE and (round_card_number == ''ACTION_14'' or round_card_number == ''ACTION_06''))');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (25, 'JOB_37', 'action', 'self.take_resource(player, {''wood'': 1, ''grain'': 1})',
        'round_card_number == "BASE_06"');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (11, 'SUB_FAC_05', 'immediately',
        'self.add_effect_on_round_cards(turn, round_cards, now_round, {''food'': 1}, "next", 3)', null);
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (12, 'SUB_FAC_03', 'immediately',
        'self.add_effect_on_round_cards(turn, round_cards, now_round, {''food'': 1}, "next", 3)', null);
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (13, 'JOB_01', 'immediately',
        'self.add_effect_on_round_cards(turn, round_cards, now_round, {''sheep'': 1}, "additional", 0, [2, 5, 8, 10])',
        null);
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (14, 'SUB_FAC_04', 'immediately',
        'self.add_effect_on_round_cards(turn, round_cards, now_round, {''grain'': 1}, "farming")', null);
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (15, 'SUB_FAC_02', 'immediately',
        'self.add_effect_on_round_cards(turn, round_cards, now_round, {''vegetable'': 1}, "additional", 0, [4, 7, 9])',
        null);
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (16, 'SUB_FAC_07', 'immediately',
        'self.add_effect_on_round_cards(turn, round_cards, now_round, {''wood'': 1}, "even")', null);
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (17, 'JOB_08', 'immediately',
        'self.add_effect_on_round_cards(turn, round_cards, now_round, {''food'': 3}, "remain")',
        'player.get(''house_type'') == HouseType.STONE_HOUSE');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (20, 'JOB_13', 'immediately', 'self.take_resource(player, {''clay'': 3, ''reed'': 2, ''stone'': 2})',
        'player.get(''house_type'') == HouseType.CLAY_HOUSE and len(list(filter(lambda f: f.get(''field_type'') == FieldType.ROOM, player.get(''fields'')))) == 2');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (21, 'JOB_25', 'action', 'self.take_resource(player, {''clay'': 1})', 'round_card_number == "BASE_03"');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (27, 'SUB_FAC_22', 'immediately', 'self.take_resource(player, {''food'': 1})', null);
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (3, 'JOB_03', 'action', 'self.add_effect_on_round_cards(turn, round_cards, now_round, {''food'': 1}, "next", 4)',
        'round_card_number == "BASE_07"');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (4, 'SUB_FAC_10', 'action',
        'self.add_effect_on_round_cards(turn, round_cards, now_round, {''food'': 1}, "next", 3)',
        'round_card_number == "BASE_16"');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (6, 'SUB_FAC_14', 'action', 'self.take_resource(player, {''food'': 1, ''reed'': 1})',
        'round_card_number == "BASE_16"');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (8, 'SUB_FAC_21', 'action', 'self.take_resource(player, {''grain'': 1})', 'round_card_number == "BASE_09"');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (7, 'SUB_FAC_18', 'action', 'self.take_resource(player, {''clay'': 3})', 'round_card_number == "BASE_12"');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (24, 'JOB_18', 'action', 'self.take_resource(player, {''vegetable'': 1})', 'round_card_number == "BASE_09"');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (19, 'JOB_21', 'action', 'self.take_resource(player, {''wood'': 1})',
        'round_card_number in ["ACTION_01",  "BASE_09", "BASE_10", "ACTION_12"]');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (22, 'JOB_34', 'action', 'self.take_resource(player, {''wood'': 1})',
        'round_card_number in ["BASE_13", "BASE_01", "BASE_02"]');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (23, 'JOB_30', 'action', 'self.take_resource(player, {''clay'': 1})',
        'round_card_number in ["BASE_13", "BASE_14", "BASE_15"]');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (26, 'SUB_FAC_22', 'action', 'self.take_resource(player, {''food'': 1})',
        'round_card_number in ["ACTION_07", "ACTION_06", "ACTION_03", "BASE_08"]');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (10, 'SUB_FAC_20', 'action', 'self.take_resource(player, {''food'': 3})',
        'round_card_number in ["BASE_13", "BASE_14", "BASE_15"]');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (9, 'SUB_FAC_25', 'action', 'self.take_resource(player, {''stone'': 1})',
        'round_card_number in ["ACTION_05", "ACTION_10"]');
insert into cards_cardeffect (id, card_number, effect, command, condition)
values (18, 'JOB_12', 'immediately', 'self.take_resource(player, {''sheep'': 2})', null);
