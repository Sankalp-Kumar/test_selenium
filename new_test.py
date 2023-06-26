import pandas as pd
import googlemaps
import streamlit as st
import openpyxl
import pandas as pd
import numpy as np
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from python_tsp.exact import solve_tsp_dynamic_programming
from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import re

def to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            format1 = workbook.add_format({'num_format': '0.00'}) 
            worksheet.set_column('A:A', None, format1)  
            writer.save()
            processed_data = output.getvalue()
            return processed_data

st.title('Welcome to Route Optimization')
page_bg_img = '''
<style>
body {
background-image: url("https://mercurygate.com/wp-content/uploads/2022/10/960x540px-Route-Design-Infographic.jpg");
background-size: cover;
}
</style>
'''

#st.markdown(page_bg_img, unsafe_allow_html=True)
# st.markdown(
#       f"""
#       <style>
#       [data-testid="stSidebar"] > div:first-child {{
#           background: url("https://mercurygate.com/wp-content/uploads/2022/10/960x540px-Route-Design-Infographic.jpg");
#           background-size: cover;
#       }}
#       </style>
#       """,
#       unsafe_allow_html=True,
#       )
master_data = st.sidebar.file_uploader("Upload an Excel file",type=['xlsx'])  
number_of_vehicles = st.sidebar.text_input("Please enter the total number of Vehicles")
if master_data :
    #st.selectbox("Select Type of request :",("Simple Route Optimization","Optimization with Priority", "Optimization Vehicle Allocation"))
    source = st.sidebar.selectbox("Please specify number of sources:",("Single Source","Multiple Sources"))
         

    # file_details = {
    #     "Filename":master_data.name,
    #     "FileType":master_data.type,
    #     "FileSize":master_data.size}

    # wb = openpyxl.load_workbook(master_data)
    # #st.header("Sheet view")
    # ## Show Excel file
    # st.sidebar.subheader("File details:")
    # st.sidebar.json(file_details,expanded=False)
    # st.sidebar.markdown("----")
    if source == "Single Source":
        option = st.sidebar.selectbox("Select Type of Request:",("Simple Route Optimization", "Priority Based Solution"))
        if option == "Simple Route Optimization" and number_of_vehicles:
        ## Select sheet
            sheet_selector = st.sidebar.selectbox("Select Type of Data:",("Data Contains latitude and longitude", "Data does not contain latitude and longitude"))     
            if sheet_selector == 'Data Contains latitude and longitude':
                st.markdown("### Raw Data")
                st.markdown("#### Simple Route Optimization with Lat-Long data")
                master_data = pd.read_excel(master_data,sheet_name='10loc')
                #st.markdown(f"### Currently Selected: `{sheet_selector}`")
                st.write(master_data)
                master_data = master_data.head(10)
            
                

                print(sheet_selector)

                API_key = 'AIzaSyB6UXX67IEK-gbZA_1UuMDJeYAySHgAPjo'#enter Google Maps API key
                gmaps = googlemaps.Client(key=API_key)


                #use pairwise function to be used to iterate through two consecutive rows (pairs) in a data frame
                def pairwise(iterable):
                    a, b = tee(iterable)
                    next(b, None)
                    return zip(a, b)



                #empty list - will be used to store calculated distances
                list1 = []


                # Loop through each row in the data frame using pairwise
                for (i1, row1) in master_data.iterrows():
                    #Assign latitude and longitude as origin/departure points
                    LatOrigin = row1['latitude']
                    LongOrigin = row1['longitude']
                    origins = (LatOrigin,LongOrigin)
                    for (i1, row1) in master_data.iterrows():

                        #Assign latitude and longitude from the next row as the destination point
                        LatDest = row1['latitude']   # Save value as lat
                        LongDest = row1['longitude']  # Save value as lat
                        destination = (LatDest,LongDest)

                        #pass origin and destination variables to distance_matrix function# output in meters
                        result = gmaps.distance_matrix(origins, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]/1000
                        #print(result)
                        result_dict = {}
                        result_dict.update({'origin': origins, 'destination': destination, 'Distance':result})
                    #append result to list
                        list1.append(result_dict)

                #Add column 'Distance' to data frame and assign to list values
                # df['Distance'] = list
                updated_df = pd.DataFrame(list1)
                #st.subheader("Distance table")
                #st.write(updated_df)
                updated_df.to_excel('start_end_dist_for_10_with_api_.xlsx')

                import pandas as pd
                import numpy as np
                from python_tsp.exact import solve_tsp_dynamic_programming


                df2=pd.read_excel('start_end_dist_for_10_with_api_.xlsx')
                #print(df2)
                u_loc = df2['origin'].unique()
                #print(len(u_loc))
                matrix = np.zeros((len(u_loc),len(u_loc)))
                #print(matrix)
                dict_u_loc = {v:i for i,v in enumerate(u_loc)}
                for i in df2.iterrows():
                #     print(i)
                #     print(i[1]['origin'])
                    idx_row = dict_u_loc[i[1]['origin']]
                #     print(idx_row)
                    idx_col = dict_u_loc[i[1]['destination']]
                    try:
                        dist = i[1]['Distance']
                #         print(dist)
                    except:
                        dist = i[1]['Distance']
                        print(dist)
                    
                    matrix[idx_row][idx_col] = dist
                print(matrix) 
                #number_of_vehicles = 4

                def create_data_model():
                    """Stores the data for the problem."""
                    data = {}
                    data['distance_matrix'] = matrix
                    data['num_vehicles'] = int(number_of_vehicles)
                    data['depot'] = 0
                    return data

                create_data_model()
                final_plan_output = []
                def print_solution(data, manager, routing, solution):
                    """Prints solution on console."""
                    print(f'Objective: {solution.ObjectiveValue()}')
                    max_route_distance = 0
                    st.subheader("This is the Optimized Route")
                    for vehicle_id in range(data['num_vehicles']):
                        index = routing.Start(vehicle_id)
                        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id+1)
                        route_distance = 0
                        while not routing.IsEnd(index):
                            plan_output += ' {} -> '.format(manager.IndexToNode(index))
                            previous_index = index
                            index = solution.Value(routing.NextVar(index))
                            route_distance += routing.GetArcCostForVehicle(
                                previous_index, index, vehicle_id)
                        plan_output += '{}\n'.format(manager.IndexToNode(index))
                        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
                        print(plan_output)
                        st.write(plan_output)
                        max_route_distance = max(route_distance, max_route_distance)
                        final_plan_output.append(plan_output)
                    print('Maximum of the route distances: {}m'.format(max_route_distance))



                def main():
                    """Entry point of the program."""
                    # Instantiate the data problem.
                    data = create_data_model()

                    # Create the routing index manager.
                    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                                        data['num_vehicles'], data['depot'])

                    # Create Routing Model.
                    routing = pywrapcp.RoutingModel(manager)


                    # Create and register a transit callback.
                    def distance_callback(from_index, to_index):
                        """Returns the distance between the two nodes."""
                        # Convert from routing variable Index to distance matrix NodeIndex.
                        from_node = manager.IndexToNode(from_index)
                        to_node = manager.IndexToNode(to_index)
                        return data['distance_matrix'][from_node][to_node]

                    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

                    # Define cost of each arc.
                    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

                    # Add Distance constraint.
                    dimension_name = 'Distance'
                    routing.AddDimension(
                        transit_callback_index,
                        0,  # no slack
                        3000,  # vehicle maximum travel distance
                        True,  # start cumul to zero
                        dimension_name)
                    distance_dimension = routing.GetDimensionOrDie(dimension_name)
                    distance_dimension.SetGlobalSpanCostCoefficient(100)

                    # Setting first solution heuristic.
                    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
                    search_parameters.first_solution_strategy = (
                        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

                    # Solve the problem.
                    solution = routing.SolveWithParameters(search_parameters)

                    # Print solution on console.
                    if solution:
                        print_solution(data, manager, routing, solution)
                    else:
                        print('No solution found !')


                if __name__ == '__main__':
                    main()


                df = pd.DataFrame({'answer':final_plan_output})

                df = df['answer'].str.split('\n', expand=True)
                df.columns=["F"+str(i) for i in range(0, len(df.columns))]

                import re
                df.iloc[:,1]=[re.sub(' -> ',',', i) for i in df.iloc[:,1]]
                df.iloc[:,1]=[re.sub(' ','', i) for i in df.iloc[:,1]]

                df1 = pd.concat([df[df.columns[[0]]],df.iloc[:,1].str.split(',', expand=True),df.drop(df.columns[[0,1]], axis=1)], axis=1)
                df1.columns = ["F"+str(i) for i in range(0, len(df1.columns))]
                df1.drop(df1.columns[len(df1.columns)-1], axis=1, inplace=True)
                #df1.head(20)


                df2 = df1.melt(id_vars=df1.columns[[0,len(df1.columns)-1]], value_vars=df1.iloc[:,1:(len(df1.columns)-1)], var_name='doesnt_matter', value_name='Location_id')
                df2.dropna(subset=['Location_id'], axis=0, how='any',inplace=True)
                df2.drop('doesnt_matter', axis=1, inplace=True)
                df2['Location_id'] = df2['Location_id'].astype('int32').apply(lambda x: x+1)
                df2.sort_values(by=[df2.columns[0],df2.columns[1]], ascending=True, axis=0, inplace=True)
                #df2.head(20)


                # df2 = pd.DataFrame(df['B'].to_list())
                # df2.columns = df2.columns.map(lambda x: f'category_{x+1}')
                # #df = pd.concat([df.drop('B', axis=1), df2], axis=1)
                # df2


                master_file = pd.merge(df2, master_data, how='left', on='Location_id')


            # master_file.info()

                master_file['latitude'] = master_file['latitude'].astype(str)
                master_file['longitude'] = master_file['longitude'].astype(str)
                master_file.info()

                master_file['lat_long'] = [x+str(',')+y for x,y in zip(master_file['latitude'],master_file['longitude'])]
                #master_file.head()
                
                st.write(master_file)
                column_values = master_file['F0'].values
                routes = np.unique(column_values)
                #st.write(routes)

                #create a data frame dictionary to store your data frames
                DataFrameDict = {elem : pd.DataFrame() for elem in master_file['F0']}

                for key in DataFrameDict.keys():
                    DataFrameDict[key] = master_file[:][master_file.F0 == key]

                #DataFrameDict[routes]

                #import undetected_chromedriver as uc
                from selenium import webdriver
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.common.by import By
                from selenium.webdriver.chrome.service import Service
                import pandas as pd
                from selenium.webdriver.common.action_chains import ActionChains
                from selenium.webdriver.common.keys import Keys
                import time
                import numpy as np
                import random as rdm
                from selenium.webdriver.chrome.options import Options



                def chrome_setup(chromeheadless = True, incognito_window=False,proxy_capabilities=None):
                    '''It set up the Chrome environment to webscraping '''    
                    #ops =webdriver.ChromeOptions()
                    ops = Options()
                    ops.add_argument('--disable-gpu')
                    ops.add_argument('--headless')
                    #ops.headless= chromeheadless
                    #caps = DesiredCapabilities().CHROME
                    #caps["pageLoadStrategy"] = "normal"  #  complete
                    #caps["pageLoadStrategy"] = "eager"  #  interactive
                    #caps["pageLoadStrategy"] = "none"    
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=ops)
                    if incognito_window== True:
                        ops =webdriver.ChromeOptions()
                        ops.add_argument('--incognito')
                        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=ops)
                    return driver


                def page_scroll(driver=None):
                    previous_height = driver.execute_script( 'return document.body.scrollHeight')

                    while True:
                        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        time.sleep(3)

                        new_height = driver.execute_script( 'return document.body.scrollHeight')

                        if new_height == previous_height:
                            break
                        previous_height = new_height

                def load_url(driver= None, url= None, new_tab=False, new_window=False):
                    try:
                    
                        if new_tab == True:
                            driver.switch_to.new_window('tab')
                            driver.get(url)
                            
                        elif new_window == True:
                            driver.switch_to.new_window('window')
                            driver.get(url)
                        else:
                            driver.get(url)

                    except:
                        pass

                driver = chrome_setup()
                url = 'https://www.google.com/maps/dir///@12.9614647,77.5861919,15z/data=!4m2!4m1!3e0'
                #load_url(driver=driver,url=url)
                driver.implicitly_wait(10)

                list_dic=[]
                #opt_dict = map_df1_dict

                for route in range(len(routes)):
                    map_df_1 = DataFrameDict[routes[route]]['lat_long'].to_list()
                    #map_df1_dict = {'Route':map_df_1}
                    map_df1_dict = {f'''Route{route+1}:''':map_df_1}
                    opt_dict = map_df1_dict
                    for k,v in opt_dict.items():
                        print(k,"\t", v)
                        input_names = v
                        load_url(driver=driver,url=url,new_tab=True)
                        driver.implicitly_wait(5)

                        while True:

                            inputs = driver.find_elements(By.CSS_SELECTOR,'div.JuLCid>div>div>.nhb85d >div>div>input')
                            for i in range(len(inputs)):
                                time.sleep(5)
                               # driver.implicitly_wait(5)
                                inputs[i].clear()
                                inputs[i].send_keys(input_names[i])
                                if i+1 == len(inputs):
                                    driver.implicitly_wait(3)
                                    button = driver.find_elements(By.CSS_SELECTOR,'button.mL3xi')[i]
                                    button.click()
                            time.sleep(5)
                            if len(inputs) == len(input_names):
                                break
                            else:
                                driver.implicitly_wait(5)
                                driver.find_element(By.CSS_SELECTOR,'div.AUkJgf>.PLEQOe.d2cEI').click()

                        driver.implicitly_wait(5)

                        route = driver.find_element(By.CSS_SELECTOR,'div.MespJc')
                        route.click()
                        driver.implicitly_wait(5)
                        time1=driver.find_element(By.CSS_SELECTOR,'div.TGDfee > h1 > span:nth-child(1) > span:nth-child(1)').text
                        distance=driver.find_element(By.CSS_SELECTOR,'div.TGDfee > h1 > span:nth-child(1) > span:nth-child(2)').text
                        share_link = driver.find_element(By.CSS_SELECTOR,'.J45yZc.ftEYtf')
                        share_link.click()
                        driver.implicitly_wait(5)
                        #len(inputs)
                        link = driver.find_element(By.CSS_SELECTOR,'div.WVlZT>input').get_attribute('value')
                        #link
                        dict_links={}
                        dict_links.update({k: link,'Total_time':time1,'Total_Distance':distance})
                        list_dic.append(dict_links)

                #print(list_dic)
                st.write(list_dic)
