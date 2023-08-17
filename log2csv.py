import csv

from parser import WorldModel


class Log2CSV:
    def __init__(self, wm):
        self.our_name = wm.get_our_team_name()
        self.opp_name = wm.get_their_team_name()
        self.rows = self.get_row_list(wm)

    def get_row_list(self, wm):
        rows = []
        while 1 <= wm.get_cycle() <= 6000:
            chiz = wm.get_cycle()
            """add our player row"""
            for unum in range(1, 12):
                kick = wm.our_player(unum, wm.get_cycle()).get_kick()
                row = {
                    'cycle': wm.get_cycle(),
                    'player_num': unum,
                    'ball_x': wm.get_ball(wm.get_cycle()).get_x(),
                    'ball_y': wm.get_ball(wm.get_cycle()).get_y(),
                    'ball_vx': wm.get_ball(wm.get_cycle()).get_vx(),
                    'ball_vy': wm.get_ball(wm.get_cycle()).get_vy(),
                    'player_x': wm.our_player(unum).get_x(),
                    'player_y': wm.our_player(unum).get_y(),
                    'player_vx': wm.our_player(unum, wm.get_cycle()).get_vx(),
                    'player_vy': wm.our_player(unum, wm.get_cycle()).get_vy(),
                    'kick': ','.join(kick) if kick is not None else None,
                    'dash': wm.our_player(unum, wm.get_cycle()).get_dash(),
                    'catch': wm.our_player(unum, wm.get_cycle()).get_catch(),
                    'turn': wm.our_player(unum, wm.get_cycle()).get_turn(),
                    'turn_neck': wm.our_player(unum, wm.get_cycle()).get_turn_neck(),
                    'tackle': wm.our_player(unum, wm.get_cycle()).get_tackle(),
                    'change_view': wm.our_player(unum, wm.get_cycle()).get_change_view(),
                    'attentionto': wm.our_player(unum, wm.get_cycle()).get_attentionto(),
                    'pointto': wm.our_player(unum, wm.get_cycle()).get_pointto(),
                    'say': wm.our_player(unum, wm.get_cycle()).get_say(),
                    'team_name': self.our_name
                }
                rows.append(row)

            """add their player row"""
            for unum in range(1, 12):
                kick = wm.their_player(unum, wm.get_cycle()).get_kick()
                row = {
                    'cycle': wm.get_cycle(),
                    'player_num': unum,
                    'ball_x': wm.get_ball(wm.get_cycle()).get_x(),
                    'ball_y': wm.get_ball(wm.get_cycle()).get_y(),
                    'ball_vx': wm.get_ball(wm.get_cycle()).get_vx(),
                    'ball_vy': wm.get_ball(wm.get_cycle()).get_vy(),
                    'player_x': wm.their_player(unum).get_x(),
                    'player_y': wm.their_player(unum).get_y(),
                    'player_vx': wm.their_player(unum, wm.get_cycle()).get_vx(),
                    'player_vy': wm.their_player(unum, wm.get_cycle()).get_vy(),
                    'kick': ','.join(kick) if kick is not None else None,
                    'dash': wm.their_player(unum, wm.get_cycle()).get_dash(),
                    'catch': wm.their_player(unum, wm.get_cycle()).get_catch(),
                    'turn': wm.their_player(unum, wm.get_cycle()).get_turn(),
                    'turn_neck': wm.their_player(unum, wm.get_cycle()).get_turn_neck(),
                    'tackle': wm.their_player(unum, wm.get_cycle()).get_tackle(),
                    'change_view': wm.their_player(unum, wm.get_cycle()).get_change_view(),
                    'attentionto': wm.their_player(unum, wm.get_cycle()).get_attentionto(),
                    'pointto': wm.their_player(unum, wm.get_cycle()).get_pointto(),
                    'say': wm.their_player(unum, wm.get_cycle()).get_say(),
                    'team_name': self.opp_name
                }
                rows.append(row)
            wm.game_mode(cycle=wm.get_cycle())
            wm.time().add_time()
        return rows

    def create_csv(self):
        with open('log.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
            writer.writeheader()
            writer.writerows(self.rows)


if __name__ == '__main__':
    wm = WorldModel('./data/20230816101557-HELIOS_1-vs-HELIOS2022_0.rcg')
    l2c = Log2CSV(wm)
    l2c.create_csv()
