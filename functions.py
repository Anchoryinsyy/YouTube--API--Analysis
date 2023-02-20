import math

def make_first_call(youtube,keyword,publishstart,publishend):
        """
        Make the first call and return crucial values

        Params:
        ------
        youtube: build object of Youtube API

        keyword: the word you want to search in the YouTube

        publishstart: the earlest publish date of the video you want to see

        publishend: the newest publish date of the video you want to see
        
        """

        response = youtube.search().list(
        part = 'snippet',
        maxResults=50,
        q=keyword,
        publishedAfter = publishstart,
        publishedBefore = publishend,
                order='date').execute()
        
        totalpages = math.ceil(500/response["pageInfo"]['resultsPerPage'])

        # next_page_token = response["nextPageToken"]
        
        repeat_window = math.floor(response["pageInfo"]['totalResults']/500)

    
        return  response,totalpages,repeat_window   



def make_next_call(youtube,next_page_token,keyword,publishstart,publishend):
            
            response = youtube.search().list(
            part = 'snippet',
            maxResults=50,
            q=keyword,
            publishedAfter = publishstart,
            publishedBefore = publishend,
            pageToken = next_page_token,
            order='date').execute()

            

            return  response




def get_data(youtube,response):

  
        # gather the results from the page
        temp_list = []
        # key_names1 = 'videoId'
        for item in response['items']:
            dic ={}
            # temp_dict_keys =list(item['id'].keys())
            
            try:
                dic['videoId'] = item['id']['videoId']
            except: 
                dic['videoId'] = None
            
            dic['title'] = item['snippet']['title']
            dic['publishTime'] = item['snippet']['publishTime']
            temp_list.append(dic)
            
        video_ids = []
        for ele in temp_list:
                video_ids.append(ele['videoId'])
            

        request = youtube.videos().list(
                part = 'statistics',
                id = ','.join([ele for ele in video_ids if ele is not None]))
        stats = request.execute()

        # all_data =[]     
        key_names2 = ['viewCount','likeCount','commentCount']
        n = 0
        for _,v in enumerate(temp_list):
             if v['videoId'] is None:
                for ele in key_names2:  
                        v[ele] = '0'
             else:
                    
                    item = stats['items'][n]
                    # temp_dict_keys = list(item['statistics'].keys())
                    for ele in key_names2:
                        try:  
                            v[ele] = item['statistics'][ele]
                        except:
                            v[ele] = '0'
                    n += 1
            
            
        
    


        return temp_list