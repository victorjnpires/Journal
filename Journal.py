# Victor Jose Novaes Pires
# 2019-01-25

import os, re, subprocess
from datetime import datetime, timedelta

jan_1_2000 = datetime(2000, 1, 1) # Jan 1st of a leap year
leap_year_days = 366

def main():
    print(">>>>> Journal: One paragraph a day memory book <<<<<")
    path = f"{os.path.expanduser('~')}/Documents/Journal"

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
    if not os.path.isdir(path):
        return False
    if not os.path.isfile(f"{path}/Journal.tex"):
        return False
    if not check_all_days(path):
        return False
    return True


def check_all_days(path):
    num_days = []
    for i in range(leap_year_days):
        date = jan_1_2000 + timedelta(i)
        isfile = os.path.isfile(f"{path}/{date.strftime('%m-%b')}/"
                                f"{date.strftime('%b-%d')}.tex")
        num_days.append(isfile)
    if sum(num_days) != leap_year_days:
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
    print("\n>>> Making files and folders...")
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
    title = input(">> Title (Author's Journal)\n> ")
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
        for i in range(leap_year_days):
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
    for i in range(leap_year_days):
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
    date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
    if (date_regex.match(text)):
        return True
    return False


def save_paragraph(path, date, paragraph):
    fpath = f"{path}/{date.strftime('%m-%b')}/{date.strftime('%b-%d')}.tex"
    with open(fpath, 'a') as f:
        section = date.strftime('%Y - %A')
        f.write(''.join([r"\subsection*{", section, "}\n"]))
        f.write(paragraph + '\n\n')


if __name__ == '__main__':
    main()