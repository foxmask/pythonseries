# -*- coding: utf-8 -*-
import requests
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)


class Client(object):

    host = "http://api.betaseries.com/"
    api_key = ''
    user_agent = ''
    logger = ''

    def __init__(self, api_key, user_agent="BetaSeriesPythonClient"):
        """
            init variable
        """        
        self.api_key = api_key
        self.user_agent = user_agent

    def set_host(self, host):
        self.host = host
        return self

    def set_user_agent(self, user_agent):
        self.user_agent = user_agent
        return self

    def set_logger(self, logger):
        self.logger = logger
        return self

    def get_host(self):
        """
            get the host from which to get series
        """
        return self.host

    def get_user_agent(self):
        """
            get the user agant we set
        """
        return self.user_agent

    def query(self, url, params={}):
        """
            Do a query to the System
        """        
        params = params
        params['key'] = self.api_key
        r = requests.get(self.get_host() + url, params=params)
        return self.handle_json_response(r)

    def handle_json_response(self, responses):
        if responses.status_code != 200:
            raise Exception("Wrong status code", responses.status_code)
        json_data = {'root':''}
        try: 
            json_data = responses.json()
        except:
            for error in json_data['root']['errors']:
                logging.error("Pythonseries: %s" %\
                              json_data['root']['errors'][error]['content'])
        return json_data['root']

    def get_api_status(self):
        """
            To know the last modifications and global status of BetaSeries
        """
        return self.query('status.json')

    def shows_search(self, title):
        """
            look for a serie from the (piece of) title
        """
        return self.query('shows/search.json', {'title': title})

    def shows_display(self, url):
        """
            display the details of a given serie 
        """
        return self.query('shows/display/' + url + '.json')

    def shows_episodes(self, url, season=None, episode=None, summary=False,
                       hide_notes=False, token=None):
        """
            Return all the details of the Episode for a given Season
        """
        params = {'summary': summary, 'hide_notes': hide_notes}

        """handle season parameter"""
        if season is not None:
            if not season.isdigit():
                raise Exception("Invalid season")
            params['season'] = season

        """Handle episode parameter"""
        if episode is not None:
            if not episode.isdigit():
                raise Exception("Invalid episode")
            if season is None:
                raise Exception('season not specified')
            params['episode'] = episode

        """handle token parameter"""
        if token is not None:
            params['token'] = token

        return self.query('shows/episodes/' + url + '.json', params)

    def shows_add(self, url, token):
        """ 
            Add the serie to the authenticated member
        """
        return self.query('shows/add/' + url + '.json', {'token': token})

    def shows_remove(self, url, token):
        """ 
            Remove the serie to the authenticated member
        """
        return self.query('shows/remove/' + url + '.json', {'token': token})

    def shows_recommend(self, url, token, friend):
        """ 
            Recommend the serie to the authenticated member's friend
        """
        
        return self.query(
            'shows/recommend/' + url + '.json',
            {'token': token, 'friend': friend}
        )

    def shows_archive(self, url, token):
        """
            Archive a serie for a given authenticated member
        """
        return self.query('shows/archive/' + url + '.json', {'token': token})

    def shows_scrapper(self, my_file):
        """
            Send the scrapper to find the serie, ID, number of episode
        """
        return self.query('shows/scraper.json', {'file': my_file})

    def shows_unarchive(self, url, token):
        """
            Get the serie out of the archive for a given authenticated member
        """
        return self.query('shows/unarchive/' + url + '.json', {'token': token})

    def shows_characters(self, url, summary=False, id=None):
        """
            list the characters of the series
        """
        params = {'summary': summary}
        '''
            to get only One character
        '''
        if id is not None:
            params['id'] = id
        return self.query('shows/characters/' + url + '.json', params)

    def shows_similar(self, url):
        """
            Get the similar series to the submitted serie
        """
        return self.query('shows/similar/' + url + '.json')

    def shows_videos(self, url, season=None, episode=None):
        params = {}

        if season is not None:
            if not season.isdigit():
                raise Exception("Invalid season")
            params['season'] = season

        if episode is not None:
            if not episode.isdigit():
                raise Exception("Invalid episode")
            if season is None:
                raise Exception('season not specified')
            params['episode'] = episode

        return self.query('shows/videos/' + url + '.json', params)

    def subtitles_last(self, language=None, number=None):
        params = {}
        language_list = ('vo', 'vf')
        if language is not None:
            if language not in language_list:
                raise Exception("Language must be 'vo' or 'vf'")
            params['language'] = language

        if number is not None:
            if not number.isdigit():
                raise Exception("Invalid number")
            params['number'] = number

        return self.query('subtitles/last.json', params)

    def subtitles_show(self, url, language=None, season=None, episode=None):
        params = {}
        language_list = ('vo', 'vf')
        if language is not None:
            if language not in language_list:
                raise Exception("Language must be 'vo' or 'vf'")
            params['language'] = language

        if season is not None:
            if not season.isdigit():
                raise Exception("Invalid season")
            params['season'] = season

        if episode is not None:
            if not episode.isdigit():
                raise Exception("Invalid episode")
            if season is None:
                raise Exception('season not specified')
            params['episode'] = episode

        return self.query('subtitles/show/' + url + '.json', params)

    def subtitles_show_by_file(self, my_file, language=None):
        """
            New : you can now get the subtitle directly from the video filename 
        """
        params = {'file': my_file}
        language_list = ('vo', 'vf')
        if language is not None:
            if language not in language_list:
                raise Exception("Language must be 'vo' or 'vf'")
            params['language'] = language

        return self.query('subtitles/show.json', params)

    def planning_general(self):
        pass
    
    def planning_member(self, token = None, login = None, unseenOnly = False):
        url = 'planning/member.json'
        params = {}

        #Check params
        if token is None and login is None:
            raise Exception("You must specify token or login")

        #handle login parameter
        if login is not None:
            url = 'planning/member/' + login +  '.json'

        #handle token parameter
        if token is not None:
            params['token'] = token

        #handle view parameter
        if unseenOnly == True:
            params['view'] = 'unseen'

        return self.query(url, params)


    def members_auth(self, login, password):
        """
            get the token to use for future requests
            identify the member with his login/pass on Betaserie
        """
        params = {'login': login, 'password': password, 'key': self.api_key}
        url = "members/auth.json"
        r = requests.get(self.get_host() + url, params=params)
        re = r.json()
        try:
            token = re['root']['member']['token']
            return token
        except:
            for error in re['root']['errors']:
                logging.error("Betaseries: %s" %
                              re['root']['errors'][error]['content'])
    
    def member_oauth(self, token):
        """
            Get the key to user in parameter of 
            https://www.betaseries.com/oauth?key=<key> 
            to identify the user without to send a password  
            The user is redirected on the callback URL you've specified 
        """
        return self.query('members/oauth.json', {'token': token})

    def member_is_active(self, token):
        """
            Check if the user is activated
        """
        return self.query('members/is_active.json', {'token': token})

    def member_destroy(self, token):
        """
            destroy immediatly the given token
        """
        return self.query('members/destroy.json', {'token': token})
    
    def member_infos(self,token=None, login=None, nodata=False, since=None):
        """
            Return the main info of the authenticated member
            or from another member (acces vary from the options of the 
            private life of the member)
        """
        url    = 'members/infos.json'
        params = {}

        # Check params
        if token is None and login is None:
            raise Exception("You must specify token or login")

        #handle login parameter
        if login is not None:
            url = 'members/infos/' + login + '.json'

        #handle token parameter
        if token is not None:
            params['token'] = token

        #handle nodata parameter
        if nodata == True:
            params['nodata'] = 1

        #handle since parameter
        if since is not None:
            if not since.isdigit():
                raise Exception("Invalid since parameter")
            params['since'] = since

        return self.query(url, params)

    def members_episodes(self):
        pass

    def members_watched(self):
        pass

    def members_note(self):
        pass

    def members_downloaded(self):
        pass

    def members_notifications(self):
        pass

    def members_option(self):
        pass

    def members_signup(self):
        pass

    def members_friends(self):
        pass

    def members_badges(self):
        pass

    def members_add(self):
        pass

    def members_delete(self):
        pass

    def members_search(self):
        pass

    def members_block(self):
        pass

    def members_unblock(self):
        pass

    def members_options(self):
        pass

    def members_sync(self):
        pass

    def comments_show(self):
        pass

    def comments_episode(self):
        pass

    def comments_member(self):
        pass

    def comment_post_show(self):
        pass

    def comment_post_episode(self):
        pass

    def comment_post_member(self):
        pass

    def comment_subscribe(self):
        pass

    def comment_unsubscribe(self):
        pass

    def timeline_home(self):
        pass

    def timeline_friends(self):
        pass

    def timeline_member(self):
        pass

    def message_inbox(self):
        pass

    def message_discussion(self):
        pass

    def message_send_new(self):
        pass

    def message_send_response(self):
        pass

    def message_delete(self):
        pass