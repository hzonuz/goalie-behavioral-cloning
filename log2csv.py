import csv
import os
from threading import Thread

from world_model import WorldModel, get_object_area


class Log2CSV:
    def __init__(self, wm):
        self.our_name = wm.get_our_team_name()
        self.opp_name = wm.get_their_team_name()
        self.rows = self.get_row_list(wm)

    def get_row_list(self, wm):
        rows = []
        while 1 <= wm.get_cycle() < 6000:
            if wm.get_ball(wm.get_cycle()).get_x() > -25:
                wm.time().add_time()
                continue

            wm.game_mode(cycle=wm.get_cycle())
            tm_players, opp_players = wm.get_nearest_players_to_goalie(wm.get_cycle())
            row = {'cycle': wm.get_cycle(), 'mode': wm.mode, 'ball_x': wm.get_ball(wm.get_cycle()).get_x(),
                   'ball_y': wm.get_ball(wm.get_cycle()).get_y(), 'ball_vx': wm.get_ball(wm.get_cycle()).get_vx(),
                   'ball_vy': wm.get_ball(wm.get_cycle()).get_vy(),
                   'ball_area': get_object_area(wm.get_ball(wm.get_cycle())),
                   'my_x': wm.our_player(1, wm.get_cycle()).get_x(),
                   'my_y': wm.our_player(1, wm.get_cycle()).get_y(), 'my_vx': wm.our_player(1, wm.get_cycle()).get_vx(),
                   'my_vy': wm.our_player(1, wm.get_cycle()).get_vy(),
                   'my_dash_power': wm.our_player(1, wm.get_cycle()).get_dash()[0] if wm.our_player(1,
                                                                                                    wm.get_cycle()).get_dash() else 0,
                   'my_dash_dir': wm.our_player(1, wm.get_cycle()).get_dash()[1] if wm.our_player(1,
                                                                                                  wm.get_cycle()).get_dash() and len(
                       wm.our_player(1, wm.get_cycle()).get_dash()) > 1 else 0,
                   'my_turn': wm.our_player(1, wm.get_cycle()).get_turn()}

            for i in range(0, 6):
                row[f'tm_player_{i}_x'] = tm_players[i].get_x()
                row[f'tm_player_{i}_y'] = tm_players[i].get_y()
                row[f'tm_player_{i}_vx'] = tm_players[i].get_vx()
                row[f'tm_player_{i}_vy'] = tm_players[i].get_vy()
                row[f'tm_player_{i}_kick'] = 1 if tm_players[i].get_kick() else 0
                row[f'tm_player_{i}_dist'] = tm_players[i].dist(wm.our_player(1, wm.get_cycle()))
                row[f'tm_player_{i}_area'] = get_object_area(tm_players[i])

            for i in range(0, 6):
                row[f'opp_player_{i}_x'] = opp_players[i].get_x()
                row[f'opp_player_{i}_y'] = opp_players[i].get_y()
                row[f'opp_player_{i}_vx'] = opp_players[i].get_vx()
                row[f'opp_player_{i}_vy'] = opp_players[i].get_vy()
                row[f'opp_player_{i}_kick'] = 1 if opp_players[i].get_kick() else 0
                row[f'opp_player_{i}_dist'] = opp_players[i].dist(wm.our_player(1, wm.get_cycle()))
                row[f'opp_player_{i}_area'] = get_object_area(opp_players[i])

            rows.append(row)
            wm.time().add_time()
        return rows

    def init_csv(self):
        with open('log.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
            writer.writeheader()

    def append_csv(self):
        with open('log.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
            writer.writerows(self.rows)


# def main():
#     for file in os.listdir('./data'):
#         if file.endswith('.rcg'):
#             log_path = os.path.join('./data', file)
#             wm = WorldModel(log_path)
#             l2c = Log2CSV(wm)
#             if not os.path.exists('log.csv'):
#                 l2c.init_csv()
#             l2c.append_csv()
#
#
# if __name__ == '__main__':
#     main()
def read_file(file):
    log_path = os.path.join('./data', file)
    wm = WorldModel(log_path)
    l2c = Log2CSV(wm)
    if not os.path.exists('log.csv'):
        l2c.init_csv()
    l2c.append_csv()


def main():
    threads = []
    for file in os.listdir('./data'):
        if file.endswith('.rcg'):
            # read_file(file)
            # break
            t = Thread(target=read_file, args=(file,))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
