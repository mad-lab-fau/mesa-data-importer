"""Import the files of the mesa sleep-wake dataset. The filetypes are PSG, Actigraphy and R-points."""
import re
from typing import Dict
from pathlib import Path
import mne

from xml.etree import ElementTree

import pandas as pd
from mesa_data_importer._types import path_t


def load_all_psg(folder_path) -> Dict[str, pd.DataFrame]:
    """Read in all PSG XML files from the MESA dataset.

    Parameters
    ----------
    folder_path: :class:`~pathlib.Path` or str
        path to the mesa folder with XML files. Important: not the filename itself!

    Returns
    -------
    dict
        dictionary that contains a :class:`~pandas.DataFrame` with PSG data for each subject

    """
    folder_path = Path(folder_path)
    print("start reading psg-data")
    psg = {}
    path_list = list(sorted(folder_path.glob("*.xml")))
    # mesa_list = re.findall("(\d{4})", ''.join(str(p))) -->if mesa_id_list wanted
    for data_name in path_list:
        i = re.findall(r"(\d{4})", data_name.name)[0]
        psg[i] = _xml_reader(folder_path.joinpath(data_name.name))
        print("file {} read in!".format(i))

    print("Reading psg-data finished")
    return psg


def load_single_psg(file_path: path_t, mesa_id: int) -> pd.DataFrame:
    """Read in one single PSG XML files from the MESA dataset.

    Parameters
    ----------
    file_path: :class:`~pathlib.Path` or str
        path to the mesa folder with XML files. Important: not the filename itself!
    mesa_id : int
        MESA subject ID

    Returns
    -------
    :class:`~pandas.DataFrame`
        :class:`~pandas.DataFrame` with PSG data of one subject

    """
    file_path = Path(file_path)
    try:  # look if a dataset exists
        psg = _xml_reader(
            file_path.joinpath(
                "polysomnography/annotations-events-nsrr/mesa-sleep-{:04d}-nsrr.xml".format(
                    mesa_id
                )
            )
        )
    except ImportError as e:
        raise ImportError("Dataset with id {} doesn't exist!".format(mesa_id)) from e

    return psg


def load_all_actigraphy(folder_path: path_t) -> Dict[str, pd.DataFrame]:
    """Read in all actigraphy csv files from the MESA dataset.

    Parameters
    ----------
    folder_path: :class:`~pathlib.Path` or str
        path to the mesa folder with actigraphy csv files. Important: not the filename itself!

    Returns
    -------
    dict:
        dict that contains a :class:`~pandas.DataFrame` with actigraphy data for each subject

    """
    print("Start reading Actigraphy-data!")
    actigraphy = {}
    path_list = list(Path(folder_path).glob("*.csv"))

    for data_name in path_list:
        i = re.findall(r"(\d{4})", data_name.name)[0]
        actigraphy[i] = pd.read_csv(folder_path + data_name.name)
        print("file {} read in!".format(i))

    print("Reading Actigraphy data finished!")
    return actigraphy


def load_single_actigraphy(file_path: path_t, mesa_id: int) -> pd.DataFrame:
    """Read in one single actigraphy csv files from the MESA dataset.

    Parameters
    ----------
    file_path: :class:`~pathlib.Path` or str
        file path to the mesa folder with actigraphy csv-files. Important: not the filename itself!
    mesa_id : int
        MESA subject ID

    Returns
    -------
    :class:`~pandas.DataFrame`
        :class:`~pandas.DataFrame` with actigraphy data of one subject

    """
    file_path = Path(file_path)
    try:
        actigraphy = pd.read_csv(
            file_path.joinpath("actigraphy/mesa-sleep-{:04d}.csv".format(mesa_id))
        )

    except ImportError as e:
        raise ImportError("Dataset with id {} doesn't exist!".format(mesa_id)) from e

    return actigraphy


def load_all_r_point(folder_path: path_t):
    """Read in all the csv-files from the r-point mesa-dataset.

    Parameters
    ----------
    folder_path: :class:`~pathlib.Path` or str
        path to the mesa folder with r-point csv files. Important: not the filename itself!

    Returns
    -------
    dict:
        dict that contains a :class:`~pandas.DataFrame` with r-point data for each subject

    """
    folder_path = Path(folder_path)
    print("Start reading r-point-data!")
    r_point = {}

    path_list = list(sorted(folder_path.glob("*.csv")))
    for data_name in path_list:
        i = re.findall(r"(\d{4})", data_name.name)[0]
        r_point[i] = pd.read_csv(folder_path.joinpath(data_name.name))
        print("file {} read in!".format(i))

    print("Reading r-point-data finished!")
    return r_point


def load_single_r_point(file_path: path_t, mesa_id: int):
    """Read in all r-point csv files from the MESA dataset.

    Parameters
    ----------
    file_path: :class:`~pathlib.Path` or str
        path to the mesa folder with r-point csv files. Important: not the filename itself!
    mesa_id : int
        MESA subject ID

    Returns
    -------
    :class:`~pandas.DataFrame`
        :class:`~pandas.DataFrame` with r-point data of one subject

    """
    file_path = Path(file_path)
    try:
        r_point = pd.read_csv(
            file_path.joinpath(
                "polysomnography/annotations-rpoints/mesa-sleep-{:04d}-rpoint.csv".format(
                    mesa_id
                )
            )
        )
    except ImportError as e:
        raise ImportError("Dataset with id {} doesn't exist!".format(mesa_id)) from e

    return r_point


def load_single_resp_features(file_path: path_t, mesa_id: int):
    """Read in all respiration features csv files from the MESA dataset.

    Parameters
    ----------
    file_path: :class:`~pathlib.Path` or str
        path to the mesa folder with respiration csv files. Important: not the filename itself!
    mesa_id : int
        MESA subject ID

    Returns
    -------
    :class:`~pandas.DataFrame`
        :class:`~pandas.DataFrame` with respiration features of one subject

    """
    file_path = Path(file_path)
    try:
        resp_features = pd.read_csv(
            file_path.joinpath(
                "respiration_features_raw/respiration{:04d}.csv".format(mesa_id)
            ),
            index_col=0,
        )
    except ImportError as e:
        raise ImportError("Dataset with id {} doesn't exist!".format(mesa_id)) from e

    return resp_features


def load_single_edr_feature(file_path: path_t, mesa_id: int):
    """
    Read in all edr features csv files from the MESA dataset.

    Parameters
    ----------
    file_path: :class:`~pathlib.Path` or str
        path to the mesa folder with edr csv files. Important: not the filename itself!
    mesa_id : int
        MESA subject ID

    Returns
    -------
    :class:`~pandas.DataFrame`
        :class:`~pandas.DataFrame` with edr features of one subject
    """
    file_path = Path(file_path)
    try:
        edr_features = pd.read_csv(
            file_path.joinpath(
                "edr_respiration_features_raw/edr_respiration{:04d}.csv".format(mesa_id)
            ),
            index_col=0,
        )
    except ImportError as e:
        raise ImportError("Dataset with id {} doesn't exist!".format(mesa_id)) from e

    return edr_features


def load_clean_data(folder_path: path_t) -> Dict[str, pd.DataFrame]:
    """Load cleaned MESA dataset from folder.

    Parameters
    ----------
    folder_path : :class:`~pathlib.Path` or str
        path to folder

    Returns
    -------
    dict
        dictionary with

    """
    folder_path = Path(folder_path)
    clean_path = folder_path.joinpath("clean_data")
    data = {}
    path_list = list(sorted(clean_path.glob("*.csv")))
    for data_name in path_list:
        i = re.findall(r"(\d{4})", data_name.name)[0]
        subj_data = pd.read_csv(clean_path.joinpath(data_name.name))
        subj_data["linetime"] = pd.to_datetime(
            subj_data["linetime"], format="%H:%M:%S"
        ).dt.time
        data[i] = subj_data

    return data


def _xml_reader(file_path: path_t):
    psg_data = ElementTree.parse(file_path)  # read xml files in a tree structure
    root = psg_data.getroot()  # root of the tree structure
    data = {}  # tree structure:
    # <PSGAnnotation>
    time = []  # <ScoredEvents>
    sleep = []  # <ScoredEvent>
    j = 0  # <EventType>Stages|Stages<EventType>
    for elem in root:  # <EventConcept>Wake|0<EventConcept>
        for subelem in elem:  # <Start>1500<Start>
            if subelem[0].text == "Stages|Stages":  # <Duration>90<Duration>
                number = float(subelem[3].text)
                i = 0
                for i in range(0, int(number / 30)):
                    time.append(j)
                    sleep.append(subelem[1].text)
                    j += 30  # every 30s we have one label, j is the time counting up without resetting.
                    # i is resetting after each scored event
    data["time"] = time
    data["sleep"] = sleep
    df = pd.DataFrame.from_dict(
        data
    )  # build a dataframe with time and sleep/wake status

    return df


def load_binary_data(folder_path: path_t):
    folder_path = Path(folder_path)
    raw_path = folder_path.joinpath("raw_data")
    data = {}
    path_list = list(sorted(raw_path.glob("*.bin")))
    for data_name in path_list:
        subj_data = pd.read_csv(raw_path)
        data[data_name] = subj_data


def load_edf(file_path: path_t, mesa_id: int):
    file_path = Path(file_path)
    try:
        edf = mne.io.read_raw_edf(
            file_path.joinpath("mesa-sleep-{:04d}.edf".format(mesa_id))
        )
    except ImportError as e:
        raise ImportError("Dataset with id {} doesn't exist!".format(mesa_id)) from e

    return edf
