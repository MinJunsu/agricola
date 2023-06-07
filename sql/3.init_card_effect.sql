insert into cards_cardeffect (id, card_number, effect, command)
values (8, 'JOB_12', 'action', 'self.take_resource(player, {''sheep'': 2})');
insert into cards_cardeffect (id, card_number, effect, command)
values (2, 'JOB_37', 'action',
        'self.take_resource_in_condition(player, card_number, "card_number == ''BASE_06''", {''wood'': 1, ''grain'': 1})');
insert into cards_cardeffect (id, card_number, effect, command)
values (9, 'JOB_36', 'immediately',
        'self.take_resource_in_condition(player, card_number, "player.get(''house_type'') == HouseType.CLAY_HOUSE and card_number == ''BASE_07'' or card_number == ''ACTION_14'' or card_number == ''ACTION_06''",{''food'': 3})');
insert into cards_cardeffect (id, card_number, effect, command)
values (5, 'JOB_30', 'action',
        'self.take_resource_in_condition(player, card_number, "card_number == ''BASE_13'' or card_number == ''BASE_15'' or card_number == ''BASE_14''", {''clay'': 1})');
insert into cards_cardeffect (id, card_number, effect, command)
values (6, 'JOB_13', 'immediately',
        'self.take_resource_in_condition(player, card_number, "player.get(''house_type'') == HouseType.CLAY_HOUSE and len(list(filter(lambda p: p.get(''field_type'') == FieldType.ROOM, player.get(''fields'')))) == 2", {''clay'': 3, ''reed'': 2, ''stone'': 2})');
insert into cards_cardeffect (id, card_number, effect, command)
values (7, 'JOB_21', 'action',
        'self.take_resource_in_condition(player, card_number, "card_number == ''BASE_10'' or card_number == ''BASE_09'' or card_number == ''ACTION_01''", {''wood'': 1})');
insert into cards_cardeffect (id, card_number, effect, command)
values (3, 'JOB_18', 'action',
        'self.take_resource_in_condition(player, card_number, "card_number == ''BASE_09''", {''vegetable'', 1})');
insert into cards_cardeffect (id, card_number, effect, command)
values (4, 'JOB_25', 'action',
        'self.take_resource_in_condition(player, card_number, "card_number == ''BASE_03''", {''grain'': 1})');
insert into cards_cardeffect (id, card_number, effect, command)
values (1, 'JOB_34', 'action',
        'self.take_resource_in_condition(player, card_number, "card_number == ''BASE_01'' or card_number == ''BASE_02'' or card_number == ''BASE_13''", {''wood'': 1})');
