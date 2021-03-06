import argparse


def get_args():
    ''' Get all the args'''
    parser = argparse.ArgumentParser(description='Hybrid Provenance Model')
    parser.add_argument(
        "--row",
        type=int,
        # choices=['1591062762131.change', '1591063332588.change', '1591063264316.change', '1591063379500.change', '1591063129144.change', '1591317229023.change', '1591863373048.change', '1591863680781.change','1591864798279.change'],
        default=0,
        help='input the row index: '
    )
    parser.add_argument(
        "--column",
        type = int,
        default=0,
        help='input the column index: '
    )
    parser.add_argument(
        "--log",
        type=str,
        default='log1',
        help='input the log folder: '
    )
    parser.add_argument(
        "--command",
        type = str,
        default= 'merge',
        help = 'return all queries '
    )
    parser.add_argument(
        "--out",
        type=str,
        default='result',
        help='output folder'
    )
    parser.add_argument(
        "--data",
        type=str,
        default='1660451457167_clean.csv',
        help='input current data for reversing'
    )
    return parser.parse_args()