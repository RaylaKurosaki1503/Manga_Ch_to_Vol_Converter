"""
Author: Rayla Kurosaki

GitHub Account: RaylaKurosaki1503
"""

import math
import os
import shutil
import sys


def get_num_zeros(total_num, current_num):
    """

    :param total_num: Total number of volumes or chapters in the manga.
    :param current_num: Current volume or chapter number.
    """
    num_of_zeros = math.floor(math.log10(total_num))
    if current_num > 0:
        num_of_zeros -= math.floor(math.log10(current_num))
        pass
    return num_of_zeros


def get_path_to_manga():
    lst = sys.argv[1:]
    path_to_manga = lst[0]
    for e in lst[1:]:
        path_to_manga += f" {e}"
        pass
    return path_to_manga


def generate_vol_dir(path_to_manga, num_of_vol):
    """
    This function creates volume directories.

    :param path_to_manga: The path to the manga.
    :param num_of_vol: Number of volumes in the manga.
    """
    # For num_of_vol manga volumes:
    for i in range(num_of_vol):
        # Create the name of the volume directory.
        zeros = "0" * get_num_zeros(num_of_vol, i + 1)
        name_of_dir = f"Volume {zeros}{i + 1}"
        # Create the path to the directory.
        path_to_volume = os.path.join(path_to_manga, name_of_dir)
        # If the path to the directory does not exist:
        if not os.path.exists(path_to_volume):
            # Create the directory.
            os.makedirs(path_to_volume)
            pass
        pass
    pass


def rename_manga_pages_a(path_to_manga, num_of_ch):
    """
    This function renames all the pages in the manga in the format
    "{chapter_num}{file_name}".

    :param path_to_manga: The path to the manga.
    :param num_of_ch: The number of chapters in the manga.
    """
    # For each manga volume:
    for vol_name in os.listdir(path_to_manga):
        # Ignore the Manga Cover directory.
        if "Volume" in vol_name:
            # Get the path to the volume.
            path_to_vol = os.path.join(path_to_manga, vol_name)
            # For each chapter in the volume:
            for ch_name in os.listdir(path_to_vol):
                # Get the chapter info.
                ch_num, ch_ext = get_chapter_info(ch_name, num_of_ch)
                # Get the path to the chapter.
                path_to_ch = os.path.join(path_to_vol, ch_name)
                # For each file in the chapter:
                for file in os.listdir(path_to_ch):
                    # If the file is an image file:
                    if not file.lower().endswith(".nomedia"):
                        # Get the current path of the page.
                        curr_page_path = os.path.join(path_to_ch, file)
                        # Get the new file name for the page.
                        if ch_ext is None:
                            page_name = f"{ch_num}{file}"
                            pass
                        else:
                            page_name = f"{ch_num}{ch_ext}{file[1:]}"
                            pass
                        # Create the path to the renamed page.
                        new_page_path = os.path.join(path_to_ch, page_name)
                        # Rename the page.
                        os.rename(curr_page_path, new_page_path)
                        pass
                    pass
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
        # Ignore the Manga Cover directory.
        if "Volume" in vol_name:
            # Get the path to the volume.
            path_to_vol = os.path.join(path_to_manga, vol_name)
            # For each chapter in the volume:
            for ch_name in os.listdir(path_to_vol):
                # Get the path to the chapter.
                path_to_ch = os.path.join(path_to_vol, ch_name)
                # For each file in the chapter:
                for file in os.listdir(path_to_ch):
                    # If the file is an image file:
                    if not file.lower().endswith(".nomedia"):
                        # Get the current path to the page.
                        curr_path_to_page = os.path.join(path_to_ch, file)
                        # Create the path to move the page in.
                        new_path_to_page = os.path.join(path_to_vol, file)
                        # Move the file to its corresponding volume directory.
                        os.rename(curr_path_to_page, new_path_to_page)
                        pass
                    pass
                # Delete the empty chapter directory.
                shutil.rmtree(path_to_ch)
                pass
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
        # Ignore the Manga Cover directory.
        if "Volume" in vol_name:
            # Get the path to the volume.
            path_to_vol = os.path.join(path_to_manga, vol_name)
            # Get the number of pages in the manga.
            num_of_pages = len(os.listdir(path_to_vol))
            # For each page in the volume:
            for i, page_name in enumerate(os.listdir(path_to_vol), start=1):
                # Get the path to the page.
                path_to_page_curr = os.path.join(path_to_vol, page_name)
                # Get the file extension.
                file_extension = page_name.split(".")[1]
                # Create the name for the page.
                zeros = "0" * get_num_zeros(num_of_pages, i)
                new_page_name = f"{zeros}{i}.{file_extension}"
                # Create the path for the page with the new file name.
                path_to_page_new = os.path.join(path_to_vol, new_page_name)
                # Rename the file.
                os.rename(path_to_page_curr, path_to_page_new)
                pass
            pass
        pass
    pass


def convert_vol_directory_to_cbz(path_to_manga):
    # For each volume in the manga:
    for vol_name in os.listdir(path_to_manga):
        # Ignore the Manga Cover directory.
        if "Volume" in vol_name:
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
    pass


def get_cover_number(filename):
    return int((filename.split(".")[0]).split("_")[-1])


def get_chapter_info(chapter_name, num_of_ch):
    """
    A function to extract the chapter number from the directory title.

    :param chapter_name: The name of the chapter.
    :param num_of_ch: Number of chapters in the manga.
    """
    lst_chapter = chapter_name.split(" ")[1].split(".")
    a = int(lst_chapter[0])
    zeros = "0" * get_num_zeros(num_of_ch, int(a))
    a = f"{zeros}{a}"
    b = None
    if len(lst_chapter) > 1:
        b = f"{lst_chapter[1]}"
        pass
    return a, b


def main():
    num_of_ch = 141
    num_of_vol = 34

    path_to_manga = get_path_to_manga()

    chapters_are_sorted = False
    chapters_are_sorted = True

    if chapters_are_sorted:
        rename_manga_pages_a(path_to_manga, num_of_ch)
        move_manga_pages(path_to_manga)
        rename_manga_pages_b(path_to_manga)
        convert_vol_directory_to_cbz(path_to_manga)
        pass
    else:
        generate_vol_dir(path_to_manga, num_of_vol)
        pass

    path_to_database_sqlite = "C:\\Users\\rayla\\.komga\\database.sqlite"
    new_path = "C:\\Users\\rayla\\Desktop\\Raylas_Manga_Collection\\" \
               "database.sqlite"
    shutil.copy2(path_to_database_sqlite, new_path)
    pass


if __name__ == '__main__':
    main()
    pass
