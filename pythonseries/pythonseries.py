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
        json_data = responses.json()
        return json_data

    def get_api_status(self):
        return self.query('status.json')

    def shows_search(self, title):
        """
            look for a title
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
            and episode 
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
        return self.query('shows/add/' + url + '.json', {'token': token})

    def shows_remove(self, url, token):
        return self.query('shows/remove/' + url + '.json', {'token': token})

    def shows_recommend(self, url, token, friend):
        return self.query(
            'shows/recommend/' + url + '.json',
            {'token': token, 'friend': friend}
        )

    def shows_archive(self, url, token):
        return self.query('shows/archive/' + url + '.json', {'token': token})

    def shows_scrapper(self, my_file):
        return self.query('shows/scraper.json', {'file': my_file})

    def shows_unarchive(self, url, token):
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
        params = {'file': my_file}
        language_list = ('vo', 'vf')
        if language is not None:
            if language not in language_list:
                raise Exception("Language must be 'vo' or 'vf'")
            params['language'] = language

        return self.query('subtitles/show.json', params)

    def members_auth(self, login, password):
        """Retourne le token à utiliser pour les requêtes futures.
        Identifie le membre avec son login et mot de pass sur Beteseries.
        """
        params = {'login': login, 'password': password}
        r = requests.get(self.get_host() + "members/auth.json", params=params)
        re = r.json()
        try:
            token = re['root']['member']['token']
            return token
        except:
            for error in re['root']['errors']:
                logging.error("Betaseries: %s" %
                              re['root']['errors'][error]['content'])
