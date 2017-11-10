import facebook
import requests
import json

global graph
global access_token
global comment_list
global base
base='https://graph.facebook.com/v2.10'

likes_count="reactions.type(LIKE).limit(0).summary(total_count).as(like),"
love_count="reactions.type(LOVE).limit(0).summary(total_count).as(love),"
wow_count="reactions.type(WOW).limit(0).summary(total_count).as(wow),"
haha_count="reactions.type(HAHA).limit(0).summary(total_count).as(haha),"
sad_count="reactions.type(SAD).limit(0).summary(total_count).as(sad),"
angry_count="reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"

fields="/?fields="+likes_count+love_count+wow_count+haha_count+sad_count+angry_count


base='https://graph.facebook.com/v2.10'
comment_result=[]
access_token='888888888888*********************RMPPGmkJt4TMLpv7XUmz30mjFNkaikwUNvZC4HgrYNKlLfemaWY305OXd0wZDZD'
graph=facebook.GraphAPI(access_token)
parameters='&limit=%s&access_token=%s' % (10,access_token)




#page_id_scraper function to scrape the page ids 
def page_id_scraper(input_string):
	initial_result=graph.request('/search?q='+input_string+'&type=page&limit=5')
	#limig=5 means we are taking the top 5 pages based on the keyword search
	page_id_list=[]
	for j in range(0,len(initial_result['data'])):
		page_id_list.append(initial_result['data'][j]['id'])
	return page_id_list



#comment_scraper funciton 
def comment_scraper(id):
    #we are using the requests library get funciton to retrive the content from the facebook,,,
	response=requests.get(base+"/%s/?fields=comments&limit=%s&access_token=%s" % (id,1000,access_token))
	return response.json()


#facebook_scraper function 
def facebook_scraper(input_string):
	page_id_list=page_id_scraper(input_string)
	for j in range(0,len(page_id_list)):
		node='/%s/posts' % page_id_list[j]
		url=base+node+fields+parameters
		response=requests.get(url)
		result=response.json()
		for k in range(0,10):
			comment_list=comment_scraper(result['data'][k]['id'])
			comment_result.append({'sad_count':result['data'][k]['sad']['summary']['total_count'],
				                 'haha_count':result['data'][k]['haha']['summary']['total_count'],
				                 'angry_count':result['data'][k]['angry']['summary']['total_count'],
				                 'love_count':result['data'][k]['love']['summary']['total_count'],
				                 'wow_count':result['data'][k]['wow']['summary']['total_count'],
				                 'like_count':result['data'][k]['like']['summary']['total_count'],
				                 'comments':comment_list,
				                 })
	with open('result.json','w') as fp:     #to store the result in the result.json file
		json.dump(comment_result,fp,indent=2)




print("\nEnter the keyword to search in facebook:\n")
string=str(input())
facebook_scraper(string)
