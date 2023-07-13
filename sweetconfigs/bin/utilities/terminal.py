#!/usr/bin/env python3

import os
import pathlib
import sys

from argparse import ArgumentParser
from subprocess import run

sys.path.insert(1, f'{pathlib.Path(__file__).resolve().parent}/../system')
import utils


def launch(action: str, force: bool = False) -> None:
    session: str = os.environ['XDG_SESSION_TYPE']

    foot_conf, alac_conf: str = (
        utils.path_expander(utils.config.terminal.foot_config_file),
        utils.path_expander(utils.config.terminal.alacritty_config_file)
    )

    if action == 'float':
        if session == 'wayland' and force is False:
            run(
                [
                    'foot', 
                    '--app-id=foot_floating', 
                    f'--config={conf_foot}'
                ]
            )

        elif session == 'x11' or force is True:
            run(
                [
                    'alacritty',
                    '--class',
                    'alacritty_floating',
                    '--config-file',
                    conf_alac
                ]
            )
    
    elif action == 'full':
        if session == 'wayland' and force is False:
            run(
                [
                    'foot',
                    '--fullscreen',
                    '--app-id=foot_fullscreen',
                    f'--config={conf_foot}',
                ]
            )

        elif session == 'x11' or force is True:
            run(
                [
                    'alacritty',
                    '--class',
                    'alacritty_fullscreen',
                    '--config-file',
                    conf_alac,
                ]
            )

    elif action == 'area':
        if session == 'wayland' and force is False:
            area = run(
                [
                    'slurp',
                    '-b',
                    '1B1F23AA',
                    '-c',
                    'FFDEDEFF',
                    '-s',
                    '00000000',
                    '-w',
                    '2',
                    '-f',
                    '%wx%h',
                ],

                check=True,
                text=True,
                capture_output=True,
            ).stdout

            run(
                [
                    'foot',
                    '--app-id=foot_floating',
                    f'--config={conf_foot}',
                    f'--window-size-pixels={area.rstrip()}',
                ]
            )

        elif session == 'x11' or force is True:
            run(
                [
                    'alacritty',
                    '--class',
                    '--config-file', conf_alac
                ]
            )

    else:
        if session == 'wayland' and force is False:
            run(
                [
                    'foot', 
                    f'--config={conf_foot}'
                ]
            )
        
        elif session == 'x11' or force is True:
            run(
                [
                    'alacritty', 
                    '--config-file', conf_alac
                ]
            )


def arguments():
    parser = ArgumentParser(description='a simple terminal script')

    parser.add_argument(
        '-f',
        '--float',
        action='store_true',
        help='launch the terminal in floating mode',
    )

    parser.add_argument(
        '-F',
        '--full',
        action='store_true',
        help='launch the terminal in fullscreen mode',
    )

    parser.add_argument(
        '-a',
        '--area',
        action='store_true',
        help='launch the terminal in a specified area',
    )

    parser.add_argument(
        '-x',
        '--alacritty',
        action='store_true',
        help='will force to use alacritty in wayland'
    )

    return parser.parse_args()


def main():
    args = arguments()
    forced: bool = utils.config.terminal.force_use_alacritty

    if args.float:
        action: str = 'float'
    
    elif args.full:
        action: str = 'full'
    
    elif args.area:
        action: str = 'area'
    
    else:
        action: str = 'normal'

    
    if args.alacritty is True and forced is False:
        forced = True

    launch(action, forced)


if __name__ == '__main__':
    main()
