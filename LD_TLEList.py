import itertools
import logging
import requests
import sys

import LD_MyTLE

log = logging.getLogger(__name__)

class LD_TLEList:
    """
    Get TLE database from a file (local or internet).
    """

    def __init__(self, path=None, internet=False):
        """
        Get the TLE data and sort it into a nice structure.
        """

        self.tle_Dict = {}

        if (path == "") or isinstance(path, type(None)):
            log.debug(""""
                  No TLE list loaded initially; use Load_TLEs_From_URL to get
                  list from a website or use Load_TLEs_From_File to load a
                  local file.
                  """)
            pass
        else:
            if internet:
                self.Load_TLEs_From_URL(path)
            else:
                self.Load_TLEs_From_File(path)

    def Load_TLEs_From_File(self, path, append=False):
        log.info(f"Load TLEs from file: {path}")
        data = open(path).read()
        flatlist = data.split("\n")

        self._Parse_File(flatlist, append)

    def Load_TLEs_From_URL(self, url, append=False):
        log.info(f"Load TLEs from URL: {url}")
        req = requests.get(url)
        flatlist = req.text.split("\r\n")

        self._Parse_File(flatlist, append)

    def _Parse_File(self, flatlist, append):
        """
        Pass in plan text of TLE list. Each line is a TLE element so every 3
        class uses to hold the TLEs.
        If append is true, it keeps any old values that were in the dict before
        this function was called. Any duplicates are overwritten (updated?)
        """

        # Every 3rd line is a satellite name. Extract them and trim the whitespace off.
        tle_Names = map(lambda x: x.rstrip(), flatlist[0::3])
        # Reshape the data from the file grouped into threes
        tle_List = zip(flatlist[0::3], flatlist[1::3], flatlist[2::3])

        # If not appending, clear any previously held values.
        if not append:
            self.tle_Dict = {}

        # Put the data into a dict - old way before appending.
        #self.tle_Dict = {key:LD_MyTLE.LD_MyTLE(data) for (key, data) in zip(tle_Names, tle_List)}
        # Put the data into a dict - new way, allows appending.
        for i, (key, data) in enumerate(zip(tle_Names, tle_List)):
            self.tle_Dict[key] = LD_MyTLE.LD_MyTLE(data)

        if append:
            log.info(f"Added {i} additional TLEs")
        log.info(f"List contains {self.__len__()} TLEs")

        # Hilarious one liner to do the above:
        # {x.rstrip():(x,y,z) for x,y,z in itertools.zip_longest(*[iter(flatlist)] * 3)}

    def Search_Keys(self, search_String):
        """
        Return all satellite names that contain a substring (case insensitive)
        """

        search_Keys = list(filter(lambda x: search_String.lower() in x.lower(), self.tle_Dict.keys()))
        log.info(f"Searched TLE list for {search_String}, found {len(search_Keys)} matching TLE names")
        log.debug(f"Keys are: {search_Keys}")
        return search_Keys

    def Search_And_Return(self, search):
        """
        Search the satellites names for a substring, return a
        list of all the matching satellites (eg searching "starlink" returns
        a list of about 400 My_TLE objects)
        If a list is passed, each string is searched separately and anything
        matching any string is returned.
        """

        if isinstance(search, str):
            search_Keys = self.Search_Keys(search)
        elif isinstance(search, (list, tuple, set)):
            # Search for each keyword individually.
            searches_List = [self.Search_Keys(this_Search.strip()) for this_Search in search]
            # Flatten the list and remove duplicates (by making into a set)
            search_Keys = set(itertools.chain.from_iterable(searches_List))

        return [self.Get_TLE(key) for key in search_Keys]

    def Get_TLE_String(self, key):
        """
        Get the TLE elements of the requested satellite name as a string.
        """
        return str(self.Get_TLE(key))

    def Get_TLE(self, key):
        """
        Get the TLE of the requested satellite as a My_TLE object.
        """
        return self.tle_Dict[key]

    def __getitem__(self, index):
        """
        Mostly this is implemented as an easy way to be able to make this
        object iterable.
        """
        return list(self.tle_Dict.values())[index]

    def __len__(self):
        return len(self.tle_Dict)

    @property
    def Keys(self):
        return self.tle_Dict.keys()

    @property
    def TLEs(self):
        return self.tle_Dict.values()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    my_tle_list = LD_TLEList("tle_Files/active.txt")

    sat_key = my_tle_list.Search_Keys("resurs-dk")
    tle = my_tle_list.tle_Dict[sat_key[0]]

    print(tle)
