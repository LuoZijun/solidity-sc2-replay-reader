#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, time
import sc2reader

base_path = "/Users/luozijun/Library/Application Support/Blizzard/StarCraft II/Accounts"
path = os.path.join(base_path, "") # 自定义 目录

def number_to_binary(n, b):
    s = []
    while n != 0:
        m = n % b
        n = n / b
        s.append(str(m))
    s.append("0b")
    s.reverse()
    return "".join(s)

# replay = sc2reader.load_replay('MyReplay', load_map=true)
replays = sc2reader.load_replays(path)

for replay in replays:
    """
    ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__getstate__', '__hash__', 
    '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
    '__str__', '__subclasshook__', '__weakref__', '_get_datapack', '_get_reader', '_read_data', 
    'active_units', 'amm', 'archive', 'attributes', 'base_build', 'battle_net', 'build', 'category', 
    'client', 'clients', 'competitive', 'computer', 'computers', 'cooperative', 'datapack', 'date', 
    'end_time', 'entities', 'entity', 'events', 'expansion', 'expasion', 'factory', 'filehash', 
    'filename', 'frames', 'game_events', 'game_fps', 'game_length', 'game_type', 'hero_duplicates_allowed', 
    'human', 'humans', 'is_ladder', 'is_private', 'length', 'load_details', 'load_game_events', 'load_level', 
    'load_map', 'load_message_events', 'load_players', 'load_tracker_events', 'logger', 'map', 'map_file', 
    'map_hash', 'map_name', 'marked_error', 'message_events', 'messages', 'objects', 'observer', 'observers', 
    'opt', 'packets', 'people', 'people_hash', 'person', 'pings', 'player', 'players', 'plugin_failures', 
    'plugin_result', 'plugins', 'practice', 'ranked', 'raw_data', 'real_length', 'real_type', 'recorder', 
    'region', 'register_datapack', 'register_default_datapacks', 'register_default_readers', 'register_reader', 
    'registered_datapacks', 'registered_readers', 'release_string', 'resume_from_replay', 'resume_method', 
    'resume_user_info', 'speed', 'start_time', 'team', 'teams', 'time_zone', 'tracker_events', 'type', 'unit', 
    'units', 'unix_timestamp', 'versions', 'windows_timestamp', 'winner']

    """
    print("Replay: ", replay.filename)
    print("\t 地图: ", replay.map_name)
    print("\t 开始: ", replay.start_time.strftime("%Y/%m/%d %H:%M:%S") )
    print("\t 结束: ", replay.end_time.strftime("%Y/%m/%d %H:%M:%S") )

    for team in replay.teams:
        print("\t 队伍 %d: "%team.number)
        for player in team.players:
            state = "UNKNOW"
            if player.detail_data['result'] == 1:
                state = "WIN"
            elif player.detail_data['result'] == 2:
                state = "LOSS"
            else:
                state = "UNKNOW"
            print("\t\t %s - %s - %d (%s) " %(player.detail_data['name'], player.detail_data['race'], player.detail_data['bnet']['uid'], state)  )


    print("\tWinner: ", replay.winner)





