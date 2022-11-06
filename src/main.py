"""
Author: Rayla Kurosaki

GitHub Account: RaylaKurosaki1503
"""

import math
import os
import shutil
import sys


def get_num_zeroes(total, current):
    """

    :param total: Total number of volumes or chapters in the manga.
    :param current: Current volume or chapter number.
    """
    return math.floor(math.log10(total)) - math.floor(math.log10(current))


def get_path_to_manga():
    lst = sys.argv[1:]
    path_to_manga = lst[0]
    for e in lst[1:]:
        path_to_manga += f" {e}"
        pass
    return path_to_manga


def generate_volumes(path_to_manga, n):
    """
    This function creates folders named "Volume X" for n volumes.

    :param path_to_manga: The path to the manga.
    :param n: Number of volumes in the manga.
    """
    # For n manga volumes:
    for i in range(n):
        # Create the name of the volume directory.
        zeros = "0" * get_num_zeroes(n, i + 1)
        name_of_dir = f"Volume {zeros}{i + 1}"
        # Create the path to the directory.
        path_to_volume = os.path.join(path_to_manga, name_of_dir)
        # Create the directory if it does not already exist.
        if not os.path.exists(path_to_volume):
            os.makedirs(path_to_volume)
            pass
        pass
    pass


def rename_manga_pages_a(path_to_manga, num_ch):
    """
    This function renames all the pages in the manga in the format
    "{chapter_num}{file_name}".

    :param path_to_manga: The path to the manga.
    :param num_ch: The number of chapters in the manga.
    """
    # For each manga volume:
    for vol_name in os.listdir(path_to_manga):
        # Get the path to the volume.
        path_to_vol = os.path.join(path_to_manga, vol_name)
        # For each chapter in the volume:
        for ch_name in os.listdir(path_to_vol):
            # Get the chapter info.
            ch_num, ch_ext = get_chapter_info(ch_name, num_ch)
            # Get the path to the chapter.
            path_to_ch = os.path.join(path_to_vol, ch_name)
            # For each page in the chapter:
            for page in os.listdir(path_to_ch):
                # Get the current path of the page.
                curr_page_path = os.path.join(path_to_ch, page)
                # Get the new file name for the page.
                if ch_ext is None:
                    page_name = f"{ch_num}{page}"
                    pass
                else:
                    page_name = f"{ch_num}{ch_ext}{page[1:]}"
                    pass
                # Create the path to the renamed page.
                new_page_path = os.path.join(path_to_ch, page_name)
                # Rename the page.
                os.rename(curr_page_path, new_page_path)
                pass
            pass
        pass
    pass


def move_manga_pages(path_to_manga):
    """
    Thus function moves all the pages out of their chapters into their
    respective volumes.

    :param path_to_manga: The path to the manga.
    """
    # For each manga volume:
    for vol_name in os.listdir(path_to_manga):
        # Get the path to the volume.
        path_to_vol = os.path.join(path_to_manga, vol_name)
        # For each chapter in the volume:
        for ch_name in os.listdir(path_to_vol):
            # Get the path to the chapter.
            path_to_ch = os.path.join(path_to_vol, ch_name)
            # For each page in the chapter:
            for page_name in os.listdir(path_to_ch):
                # Get the current path to the page.
                curr_path_to_page = os.path.join(path_to_ch, page_name)
                # Create the path to move the page in.
                new_path_to_page = os.path.join(path_to_vol, page_name)
                # Move the file to its corresponding volume directory.
                os.rename(curr_path_to_page, new_path_to_page)
                pass
            # Delete the empty chapter directory.
            shutil.rmtree(path_to_ch)
            pass
        pass
    pass


def rename_manga_pages_b(path_to_manga):
    """
    This function renames the pages of the manga in the format "{i}.{ext}"
    where "i" is the page number.

    :param path_to_manga: The path to the manga.
    """
    # For each manga volume:
    for vol_name in os.listdir(path_to_manga):
        # Get the path to the volume.
        path_to_vol = os.path.join(path_to_manga, vol_name)
        # Get the number of pages in the manga.
        n = len(os.listdir(path_to_vol))
        # For each page in the volume:
        for i, page_name in enumerate(os.listdir(path_to_vol), start=1):
            # Get the path to the page.
            path_to_page_curr = os.path.join(path_to_vol, page_name)
            # Get the file extension.
            file_extension = page_name.split(".")[1]
            # Create the name for the page.
            zeros = "0" * get_num_zeroes(n, i)
            new_page_name = f"{zeros}{i}.{file_extension}"
            # Create the path for the page with the new file name.
            path_to_page_new = os.path.join(path_to_vol, new_page_name)
            # Rename the file.
            os.rename(path_to_page_curr, path_to_page_new)
            pass
        pass
    pass


def convert_vol_directory_to_cbz(path_to_manga):
    # For each volume in the manga:
    for vol_name in os.listdir(path_to_manga):
        # Get the path to the volume.
        path_to_vol = os.path.join(path_to_manga, vol_name)
        # Zip the volume directory.
        shutil.make_archive(path_to_vol, "zip", root_dir=path_to_vol)
        # Convert the zip file to a cbz file.
        os.rename(f"{path_to_vol}.zip", f"{path_to_vol}.cbz")
        # Delete the original directory.
        shutil.rmtree(path_to_vol)
        pass
    pass


def get_chapter_info(chapter_name, num_ch):
    """
    A function to extract the chapter number from the directory title.

    :param chapter_name: The name of the chapter.
    :param num_ch: Number of chapters in the manga.
    """
    lst_chapter = chapter_name.split(" ")
    chapter_number = lst_chapter[1].split(".")
    a = int(chapter_number[0])
    zeroes = "0" * get_num_zeroes(num_ch, int(a))
    a = f"{zeroes}{a}"
    b = None
    if len(chapter_number) == 2:
        b = f"{chapter_number[1]}"
        pass
    return a, b


def main():
    num_of_vol = 11
    num_of_ch = 107
    path_to_manga = get_path_to_manga()

    # generate_volumes(path_to_manga, num_of_vol)

    # rename_manga_pages_a(path_to_manga, num_of_ch)
    # move_manga_pages(path_to_manga)
    # rename_manga_pages_b(path_to_manga)
    # convert_vol_directory_to_cbz(path_to_manga)

    path_to_database_sqlite = "C:\\Users\\rayla\\.komga\\database.sqlite"
    new_path = "C:\\Users\\rayla\\Desktop\\Raylas_Manga_Collection\\" \
               "database.sqlite"
    shutil.copy2(path_to_database_sqlite, new_path)
    pass


if __name__ == '__main__':
    main()
    pass