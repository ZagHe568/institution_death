"""
This script records the publication year and references of each paper.
"""

import sys
sys.path.append('..')
from utils.directories import *
from utils.pkl_io import save_pkl_file, open_pkl_file
import time
import argparse
import pandas as pd


def is_valid_paper(paper_entity):
    # the maximum teamsize of each paper is 25
    # each paper should contain the complete information of the authors and their affiliations
    if 'AA' not in paper_entity:
        return False
    authors = paper_entity['AA']
    if len(authors) > 25:
        return False
    for author in authors:
        if 'DAuN' not in author:
            return False
        if 'AuId' not in author:
            return False
        if 'DAfN' not in author:
            return False
        if 'AfId' not in author:
            return False
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fos', default='physics', type=str, choices=('physics', 'cs', 'sociology', 'math'),
                      help='field of study')
    args = parser.parse_args()
    print(args.fos)
    directories = Directory(args.fos)
    directories.refresh()

    paperId_year = {}
    paperId_references = {}
    affId_affnames = set()


    num = 0
    for filename in os.listdir(directories.directory_mag_data):
        paper_entities = open_pkl_file(directories.directory_mag_data, filename[0:-4])
        for paper_entity in paper_entities:
            if not is_valid_paper(paper_entity):
                continue
            num += 1
            if num % 1000 == 0:
                print(num, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            paperId = paper_entity['Id']
            year = paper_entity['Y']
            references = paper_entity['RId'] if 'RId' in paper_entity else []
            paperId_year[paperId] = year
            paperId_references[paperId] = references

            for author in paper_entity['AA']:
                affId = author['AfId']
                aff_name = author['DAfN']
                affId_affnames.add((affId, aff_name))

    pd.DataFrame(list(affId_affnames)).to_csv(
        os.path.join(directories.directory_dataset_description, 'paperId_year.csv'), index=False)

    save_pkl_file(directories.directory_dataset_description, 'paperId_year', paperId_year)
    save_pkl_file(directories.directory_dataset_description, 'paperId_references', paperId_references)
    save_pkl_file(directories.directory_dataset_description, 'affId_affnames', affId_affnames)
