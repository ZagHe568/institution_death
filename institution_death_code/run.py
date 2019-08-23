import os

if __name__ == '__main__':
    print('input')
    a = input()
    commands = ['cd 03_author_modeling/',
                'python authorId_first_year.py',
                'cd ..'
                'cd 04_institution_modeling',
                'python 02_affiliation_construction.py',
                'python 03_output_affiliation.py',
                'cd ..'
                # 'tar zcvf institution.tar.gz ../results/{}/dataset_description/'.format(a),
                ]

    for command in commands:
        print(command)
        os.system(command)
