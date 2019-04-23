# Victor Jose Novaes Pires
# Version 2.2 -- 2019-04-23
# Version 2.1 -- 2019-04-22
# Version 2.0 -- 2019-04-20
# Version 1.0 -- 2019-01-25

import re, subprocess
from datetime import datetime, timedelta
from os.path import expanduser, isdir, isfile

jan_1_2000 = datetime(2000, 1, 1) # Jan 1st of a leap year
days_in_leap_year = 366

def main():
    print(">>>>> Journal: One paragraph a day memory book <<<<<")
    path = f"{expanduser('~')}/Documents/Journal"

    journal = check_files_and_folders(path)
    if not journal:
        journal = make_journal(path)
    if not journal:
        print("\n>>> ERROR: Journal files and folders not found!")
        return

    date = datetime.now()
    paragraph = input(f"\n>>> {date.strftime('%A, %B %d, %Y')}\n>> ")

    if is_date(paragraph):
        date = datetime.strptime(paragraph, '%Y-%m-%d')
        paragraph = input(f"\n>>> {date.strftime('%A, %B %d, %Y')}\n>> ")

    confirm_save = input('\n>> Save? [Y/n]: ')
    if (len(confirm_save) == 0) or confirm_save.lower().startswith('y'):
        save_paragraph(path, date, paragraph)
    else:
        print("\n>>> No changes were saved!")
        return

    print("\n>>> Building journal...")
    for _ in range(2): # Compiling twice for the table of contents
        run(f"pdflatex -synctex=1 -interaction=nonstopmode {path}/Journal.tex",
            path=path)

    print("\n>>> Program finished successfully!")


def check_files_and_folders(path):
    if not isdir(path):
        return False
    if not isfile(f"{path}/Journal.tex"):
        return False
    if not check_all_days(path):
        return False
    return True


def check_all_days(path):
    for i in range(days_in_leap_year):
        date = jan_1_2000 + timedelta(i)
        exists = isfile(f"{path}/{date.strftime('%m-%b')}/"
                        f"{date.strftime('%b-%d')}.tex")
        if exists == False:
            return False
    return True


def make_journal(path):
    print("\n>>> WARNING!")
    print(">> This script will make the files and folders for the Journal.")
    print(f">> It will delete all files from the folder '{path}'")
    proceed = input(">> Type 'YES' to continue\n> ")
    if proceed != 'YES':
        print('\n>>> ERROR: No changes were made!')
        return False
    print("\n>>> New journal")
    run(f"rm -rf {path}")
    run(f"mkdir -p {path}")
    make_main_file(path)
    make_folders(path)
    make_daily_files(path)
    return True


def run(command, path=None):
    return subprocess.run(command, cwd=path, shell=True, check=True)


def make_main_file(path):
    author = input(">> Author\n> ")
    title = input(f">> Title ({author.split()[0]}'s Journal)\n> ")
    print("\n>>> Making files and folders...")
    run(f"touch {path}/Journal.tex")
    with open(f"{path}/Journal.tex", 'w') as journal:
        journal.write(r"\documentclass[10pt,oneside,english]{book}" + '\n')
        journal.write(r"\usepackage[english]{babel}" + '\n')
        journal.write(r"\usepackage[hidelinks]{hyperref}" + '\n')
        journal.write(''.join([r"\author{", author, "}\n"]))
        journal.write(''.join([r"\title{", title, "}\n"]))
        journal.write(r"\makeindex" + '\n')
        journal.write(r"\begin{document}" + '\n')
        journal.write(r"\maketitle" + '\n')
        journal.write(r"\pagestyle{plain}" + '\n')
        journal.write(r"\tableofcontents" + '\n')
        # Links to the daily files
        for i in range(days_in_leap_year):
            date = jan_1_2000 + timedelta(i)
            fpath = (f"{path}/{date.strftime('%m-%b')}/"
                     f"{date.strftime('%b-%d')}.tex")
            journal.write(''.join([r"\input{", fpath, "}\n"]))
            journal.write(r"\newpage" + '\n')
        journal.write(r"\end{document})")


def make_folders(path):
    for i in range(1, 13): # The 12 months
        date = datetime(2019, i, 1)
        run(f"mkdir -p {path}/{date.strftime('%m-%b')}")


def make_daily_files(path):
    for i in range(days_in_leap_year):
        date = jan_1_2000 + timedelta(i)
        fpath = f"{path}/{date.strftime('%m-%b')}/{date.strftime('%b-%d')}.tex"
        run(f"touch {fpath}")

        with open(fpath, 'w') as f:
            # Add chapter on first day of the month
            if date.strftime('%d') == '01':
                month = f"{date.strftime('%B')}"
                f.write(''.join([r"\chapter*{", month, "}\n"]))
                f.write(''.join([r"\addcontentsline{toc}{chapter}{", month,
                        "}\n"]))
                f.write(r"\newpage" + '\n\n')
            # Daily file header
            day = date.strftime('%B %d')
            f.write(''.join([r"\section*{", day, "}\n\n"]))
            f.write(''.join([r"\addcontentsline{toc}{section}{", day[-2:],
                    "}\n"]))


def is_date(text):
    date_regex = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')
    if (date_regex.match(text)):
        return True
    return False


def save_paragraph(path, date, paragraph):
    fpath = f"{path}/{date.strftime('%m-%b')}/{date.strftime('%b-%d')}.tex"
    content = file_to_list(fpath)
    previous_entries = check_previous_entries(content)
    line_number = get_line_number(content,
                                  previous_entries,
                                  this_year=int(date.strftime('%Y')))
    new_content = make_new_content(content, date, paragraph, line_number)
    save_to_file(fpath, new_content)


def file_to_list(fpath):
    with open(fpath, 'r') as f:
        return f.readlines()


def check_previous_entries(content):
    year_regex = re.compile(r'\d{4}')
    previous_entries = []
    for line_number, line in enumerate(content):
        if year_regex.search(line) is not None:
            year = int(year_regex.search(line).group(0))
            previous_entries.append([line_number, year])
    return previous_entries


def get_line_number(content, previous_entries, this_year):
    # No previous entries
    if len(previous_entries) == 0:
        return len(content)
    # Bigger than or equal to the last year
    if this_year >= previous_entries[-1][1]:
        return len(content)
    # Smaller than the first year
    if this_year < previous_entries[0][1]:
        return previous_entries[0][0]
    # Entry between previous years
    return get_line_in_between(previous_entries, this_year)


def get_line_in_between(previous_entries, this_year):
    line_numbers, years = [], []
    for pair in previous_entries:
        line_numbers.append(pair[0])
        years.append(pair[1])
    if this_year in years:
        print('\n>>> WARNING: There is an entry on this date already!')
    for line_number, previous_year in zip(line_numbers, years):
        if this_year < previous_year:
            return line_number


def make_new_content(content, date, paragraph, line_number):
    new_content = content.copy()
    section = date.strftime('%Y - %A')
    new_content.insert(line_number, ''.join([r"\subsection*{", section, "}\n"]))
    new_content.insert((line_number + 1), (paragraph + '\n\n'))
    return new_content


def save_to_file(fpath, content):
    with open(fpath, 'w') as f:
        f.writelines(content)


if __name__ == '__main__':
    main()