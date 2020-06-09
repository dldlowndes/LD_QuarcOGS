import datetime

import LD_MyTLE
import LD_TLEList
import LD_PassFinder

import LD_Planewave
import LD_PWI_Status

def Track_ISS():
    my_TLE_List = LD_TLEList.LD_TLE_List("tle_Files/active.txt", False)
    
    iss_TLE = my_TLE_List.Search_And_Return("zarya")
    
    my_Mount = LD_Planewave.LD_Planewave("http://127.0.0.1", "8220")
    my_Mount.Follow_TLE(iss_TLE)
    
def Get_All_Starlink_TLEs():
    my_TLE_List = LD_TLEList.LD_TLE_List("tle_Files/active.txt", False)
    
    starlink_List = my_TLE_List.Search_And_Return("starlink")
    
    return starlink_List
    
def Get_Tonights_Passes():
    finder = LD_PassFinder.LD_PassFinder()
    finder.Set_Position(51.456671, -2.601768, 71)
    
    t_now = datetime.datetime.now()
    t_start = datetime.datetime(t_now.year, t_now.month, t_now.day, 22, 00)
    t_stop = t_start + datetime.timedelta(hours=8)
    
    finder.Search_Time_Range(str(t_start), str(t_stop), 1)
    finder.Load_TLE_Data("tle_Files/visual.txt") 
    
    finder.Calculate_Passes()
    finder.Filter_Passes(alt_Filter = 30)
    data = finder.Get_Pass_List()
    
    # finder.Print_Pass_List()
    # finder.Save_Pass_List()
    
    return data
    
if __name__ == "__main__":
    pass