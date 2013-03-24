# -*- coding: utf-8 -*-
import requests
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)


class Client(object):
    """
        Python Class 'Client' to deal with BetaSeries API
    """

    host = "http://api.betaseries.com/"
    api_key = ''
    user_agent = ''
    logger = ''

    def __init__(self, api_key, user_agent="BetaSeriesPythonClient"):
        """
            init variable
            :param api_key: string of the key provided by BetaSeries
            :param user_agent
        """
        self.api_key = api_key
        self.user_agent = user_agent

    def set_host(self, host):
        """
            set the host from where the API is avaible
        """
        self.host = host
        return self

    def set_user_agent(self, user_agent):
        """
            define the user_agent
            :param user_agent
        """
        self.user_agent = user_agent
        return self

    def set_logger(self, logger):
        self.logger = logger
        return self

    def get_host(self):
        """
            get the host from which to get series
            :return host
        """
        return self.host

    def get_user_agent(self):
        """
            get the user agant we set
            :return user_agent
        """
        return self.user_agent

    def query(self, url, params={}, method='get'):
        """
            Do a query to the System API
            :param url: mainly the name of the serie
            :param params: a dict with all the necessary thins to query the API
            :return json data
        """
        params = params
        params['key'] = self.api_key
        if method == 'get':
            r = requests.get(self.get_host() + url, params=params)
        elif method == 'post':
            r = requests.post(self.get_host() + url, params=params)
        return self.handle_json_response(r)

    def handle_json_response(self, responses):
        """
            get the json data reponse
            :param responses: the json reponse
            :return the json data without 'root' node
        """
        if responses.status_code != 200:
            raise Exception("Wrong status code", responses.status_code)
        json_data = {'root': ''}
        try:
            json_data = responses.json()
        except:
            for error in json_data['root']['errors']:
                logging.error("Pythonseries: %s" % \
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
            :param title: the title to search
            :return json data
        """
        return self.query('shows/search.json', {'title': title})

    def shows_display(self, url):
        """
            display the details of a given serie
            :param url: the url of the serie to display
            :return json data
        """
        return self.query('shows/display/' + url + '.json')

    def shows_episodes(self, url, season=None, episode=None, summary=False,
                       hide_notes=False, token=None):
        """
            Return all the details of the Episode for a given Season
            :param url: the url of the serie to show
            :param season: the season to filter (optional)
            :type season: int
            :param episode: the episode to filter (optional)
            :type episode: int
            :param summary: to summarize the display of the episode (optional)
            :type summary: boolean
            :param hide_note (optional)
            :type hide_note: boolean
            :param token: token of the user (optional)
            :return json data
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
            :param url: url to add a serie
            :param token: the token that identifed the user to access the API
            :return json data
        """
        return self.query('shows/add/' + url + '.json', {'token': token})

    def shows_remove(self, url, token):
        """
            Remove the serie to the authenticated member
            :param url: url to remove a serie
            :param token: the token that identifed the user to access the API
            :return json data
        """
        return self.query('shows/remove/' + url + '.json', {'token': token})

    def shows_recommend(self, url, token, friend):
        """
            Recommend the serie to the authenticated member's friend
            :param url: url to remove a serie
            :param token: the token that identifed the user to access the API
            :param friend: the name of a friend
            :return json data
        """
        return self.query(
            'shows/recommend/' + url + '.json',
            {'token': token, 'friend': friend}
        )

    def shows_archive(self, url, token):
        """
            Archive a serie for a given authenticated member
            :param url: url to show the series we archive
            :param token: the token that identifed the user to access the API
            :return json data
        """
        return self.query('shows/archive/' + url + '.json', {'token': token})

    def shows_scraper(self, my_file):
        """
            Send the scrapper to find the serie, ID, number of episode
            :param my_file: try to find a serie from the given file
            :return json data
        """
        return self.query('shows/scraper.json', {'file': my_file})

    def shows_unarchive(self, url, token):
        """
            Get the serie out of the archive for a given authenticated member
            :param url: url to show the series we 'unarchive'
            :param token: the token that identifed the user to access the API
            :return json data
        """
        return self.query('shows/unarchive/' + url + '.json', {'token': token})

    def shows_characters(self, url, summary=False, the_id=None):
        """
            list the characters of the series
            :param url: name of the serie from which we want to display chars
            :param summary: when set to true will display id and chars name
            :type summary: boolean
            :param the_id: display only one character details
            :type the_id: int
            :return json data
        """
        params = {'summary': summary}
        '''
            to get only One character
        '''
        if the_id is not None:
            params['id'] = the_id
        return self.query('shows/characters/' + url + '.json', params)

    def shows_similar(self, url):
        """
            Get the similar series to the submitted serie
            :param url: name of the serie (mandatory)
            :return json data
        """
        return self.query('shows/similar/' + url + '.json')

    def shows_videos(self, url, season=None, episode=None):
        """
            Show the videos of the given series
            :param url: the given serie - mandatory
            :param season: the season to show (optional)
            :type season: int
            :param episode: the episode to show (optional)
            :type episode: int
            :return: json data
        """
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
        """
            show the last subtitles
            :param language: can be vo or vf (optional)
            :param number: the number of subtitle to show max : 100 (optional)
            :type number: int
            :return: json data
        """
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
        """
            show the subtitle of a given serie
            :param url: the given serie (mandatory)
            :param language: can be vo or vf (optional)
            :param season: the season to show (optional)
            :type season: int
            :param episode: the episode to show (optional)
            :type episode: int
            :return: json data
        """
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
            :param my_file: the file to search
            :param language: vo or vf (optional)
            :return: json data
        """
        if not my_file:
            raise Exception("You have to set a filename to search")

        params = {'file': my_file}

        language_list = ('vo', 'vf')
        if language is not None:
            if language not in language_list:
                raise Exception("Language must be 'vo' or 'vf'")
            params['language'] = language

        return self.query('subtitles/show.json', params)

    def planning_general(self):
        """
            show the general planning
            :return: json data
        """
        return self.query('planning/general.json')

    def planning_member(self, token=None, login=None, unseen_only=False):
        """
            show the member's planning
            :param token: the string to identify the member (optional)
            :type token: string
            :param login: the connection id (optional)
            :type login: string
            :param unseen_only: display just the unseen planning (optional)
            :type unseen: boolean
            :return: json data
        """
        url = 'planning/member.json'
        params = {}

        # Check params
        if token is None and login is None:
            raise Exception("You must specify token or login")

        # handle login parameter
        if login is not None:
            url = 'planning/member/' + login + '.json'

        # handle token parameter
        if token is not None:
            params['token'] = token

        # handle view parameter
        if unseen_only == True:
            params['view'] = 'unseen'

        return self.query(url, params)

    def members_auth(self, login, password):
        """
            get the token to use for future requests
            identify the member with his login/pass on Betaserie
            :param login: the string to identify the member (mandatory)
            :type login: string
            :param password: the pass in md5
            :type password: string
            :return: json data (in fact : the precious token ! )
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
            :param token: the string to identify the member (mandatory)
            :type token: string
            :return: json data
        """
        return self.query('members/oauth.json', {'token': token})

    def member_is_active(self, token):
        """
            Check if the user is activated
            :param token: the string to identify the member (mandatory)
            :type token: string
            :return: json data
        """
        return self.query('members/is_active.json', {'token': token})

    def member_destroy(self, token):
        """
            destroy immediatly the given token
            :param token: the string to identify the member (mandatory)
            :type token: string
            :return: json data
        """
        return self.query('members/destroy.json', {'token': token})

    def member_infos(self, token=None, login=None, nodata=False, since=None):
        """
            Return the main info of the authenticated member
            or from another member (acces vary from the options of the
            private life of the member)
            :param token: the string to identify the member (optional)
            :type token: string
            :param login: the string to identify the member (optional)
            :type login: string
            :param nodata: is True only login and date are returned
            :type nodata: boolean
            :param since: filter the infos from this date
            :type since: int  (timestamp)
            :return: json data
        """
        url = 'members/infos.json'
        params = {}
        # Check params
        if token is None and login is None:
            raise Exception("You must specify token or login")

        # handle login parameter
        if login is not None:
            url = 'members/infos/' + login + '.json'

        # handle token parameter
        if token is not None:
            params['token'] = token

        # handle nodata parameter
        if nodata == True:
            params['nodata'] = 1

        # handle since parameter
        if since is not None:
            if not since.isdigit():
                raise Exception("Invalid since parameter")
            params['since'] = since

        return self.query(url, params)

    def members_episodes(self, token, subtitles='all',
                         show=None, view=None):
        """
            the remaining episode to be seen by the member
            :param token: the token of the authenticated user (mandatory)
            :param subtitles: string : all vf vovf to filter episode (optional)
            :param show: string : the name of the serie (optional)
            :param view: mixed: 'next' or nn where nn is the number of episode
to return
            :return json data
        """
        # handle sousTitres params
        if subtitles not in ('all', 'vovf', 'vf'):
            raise Exception("Invalid subtitles parameter")

        url = 'members/episodes/' + subtitles + '.json'

        params = {'token': token}

        # handle show parameter
        if show is not None:
            params['show'] = show

        if view is not None:
            if 'next' == view or view.isdigit():  # bug ?
                params['view'] = view
        return self.query(url, params)

    def members_watched(self):
        pass

    def members_note(self, token, url, season, episode, note):
        """
            Give a note to an episode for the given season of the serie
            to give a note to the complet serie put season=0 and episode=0
            :param token: the string to identify the member (optional)
            :type token: string
            :param url: the name of the serie to note
            :type url: string
            :param season
            :type season: int
            :param episode
            :type episode: int
            :param note: from 1 to 5
            :type note: int
            :return: json data
        """
        # handle season parameter
        if not season.isdigit():
            raise Exception("Invalid season parameter")

        # Handle episode parameter
        if not episode.isdigit():
            raise Exception("Invalid episode parameter")

        # handle note parameter
        if note not in range(1, 6):
            raise Exception("Invalid note parameter")

        params = {
            'token': token,
            'season': season,
            'episode': episode,
            'note': note
        }

        return self.query('members/note/' + url + '.json', params)

    def members_downloaded(self, token, url, season, episode):
        """
            set the episode of the season from the serie as downloaded
            :param token: the string to identify the member (optional)
            :type token: string
            :param url: the name of the serie to set as downloaded
            :type url: string
            :param season
            :type season: int
            :param episode
            :type episode: int
            :return json data
        """
        # handle season parameter
        if not season.isdigit():
            raise Exception("Invalid season parameter")

        # Handle episode parameter
        if not episode.isdigit():
            raise Exception("Invalid episode parameter")

        params = {'token': token, 'season': season, 'episode': episode}

        return self.query('members/downloaded/' + url + '.json', params)

    def members_notifications(self, token, summary=False, number=None,
                              last_id=None, sort=None):
        """
            Get the Notification of a member
            if summary is set, return the number of unread notification
            :param token: the string to identify the member (optional)
            :type token: string
            :param summary
            :type summary: boolean
            :param number
            :type number: int
            :param last_id
            :type last_id: int
            :param sort
            :type last_id: string
            :return json data
        """
        params = {'token': token}

        # handle sumary parameter
        if summary == True:
            params['summary'] = 'yes'

        # handle number parameter
        if number is not None:
            if not number.isdigit():
                raise Exception("Invalid number parameter")
            params['number'] = number

        # handle last_id parameter
        if last_id is not None:
            if not last_id.isdigit():
                raise Exception("Invalid last_id parameter")
            params['last_id'] = last_id

        # handle sort parameter
        if sort is not None:
            if sort not in ('asc', 'desc'):
                raise Exception("Invalid sort parameter")
            params['sort'] = sort

        print params
        return self.query('members/notifications.json', params)

    def members_option(self, token, option, value=None):
        """
            Get the Notification of a member
            if summary is set, return the number of unread notification
            :param token: the string to identify the member (optional)
            :type token: string
            :param option has to be 'downloaded', 'notation', 'decalage'
            :type option: string
            :param value has to be 0 (to read) or 1 (to modify)
            :type value: int
            :return json data
        """
        params = {'token': token}

        # handle option parameter
        if option not in ('downloaded', 'notation', 'decalage'):
            raise Exception("Invalid option parameter")

        # handle value parameter
        if value is not None:
            if value not in (0, 1):
                raise Exception("Invalid value parameter")
            params['value'] = value

        return self.query('members/option/' + option + '.json', params)

    def members_signup(self, login, password, mail):
        """
            create a new account
            :param login
            :param password
            :param email
            :return json data
        """
        # handle login parameter
        if len(login) > 24:
            raise Exception("login too long")

        params = {'login': login, 'password': password, 'mail': mail}
        print params
        return self.query('members/signup.json', params)

    def members_friends(self, token=None, login=None):
        """
            get the list of friends of the user identified by is login or token
            :param token
            :param login
            :return json data
        """
        params = {}

        # handle token parameter
        if token is not None:
            params['token'] = token

        url = 'members/friends.json'

        # handle login parameter
        if login is not None:
            url = 'members/friends/' + login + '.json'

        return self.query(url, params)

    def members_badges(self, token=None, login=None):
        """
            get the list of badges of the user identified by is login or token
            :param token
            :param login
            :return json data
        """
        params = {}

        # handle token parameter
        if token is not None:
            params['token'] = token

        url = 'members/badges.json'

        # handle login parameter
        if login is not None:
            url = 'members/badges/' + login + '.json'

        return self.query(url, params)

    def members_add(self, token, login):
        """
            add the user as friend
            :param token
            :param login
            :return json data
        """
        params = {'token': token}

        return self.query('members/add/' + login + '.json', params)

    def members_delete(self, token, login):
        """
            delete the user as friend
            :param token
            :param login
            :return json data
        """
        params = {'token': token}

        return self.query('members/delete/' + login + '.json', params)

    def members_search(self, login):
        """
            list the 10 user that start by the login
            :param login
            :return json data
        """
        params = {'login': login}

        return self.query('members/search.json', params)

    def members_block(self, token, login):
        """
            block the user
            :param token
            :param login
            :return json data
        """
        params = {'token': token}

        return self.query('members/block/' + login + '.json', params)

    def members_unblock(self, token, login):
        """
            unblock the user
            :param token
            :param login
            :return json data
        """
        params = {'token': token}

        return self.query('members/unblock/' + login + '.json', params)

    def members_options(self, token):
        """
            get the options of the member
            :param token
            :return json data
        """
        params = {'token': token}

        return self.query('members/options.json', params)

    def members_sync(self, token, mail):
        """
            get the friends list that match the email address
            several email addresses accepted seperated by comma
            :param token
            :param mail
            :return json data
        """
        params = {'token': token, 'mail': mail}

        return self.query('members/sync.json', params)

    def comments_show(self, url):
        """
            display the comment of the given serie
            :param url : url of the serie
            :type url: string
            :return json data
        """
        return self.query('comments/show/' + url + '.json')

    def comments_episode(self, url, season, episode):
        """
            display the comment of the given episode
            :param url: url of the serie
            :type url: string
            :param season: number of the season of the episode
            :type season: int
            :param episode: number of the episode
            :type episode: int
            :return json data
        """
        params = {'season': season, 'episode': episode}
        if not season.isdigit():
            raise Exception("Invalid season parameter")

        if not episode.isdigit():
            raise Exception("Invalid season parameter")

        return self.query('comments/episode/' + url + '.json', params)

    def comments_member(self, login):
        """
            display the comment of the given member
            :param login : login's member
            :type login: string
            :return json data
        """
        return self.query('comments/member/' + login + '.json')

    def comments_post_show(self, token, show, text, in_reply_to=None):
        """
            post a comment on the show
            :param token : token of the authenticated member
            :type token: string
            :param show : the name of the show
            :type show: string
            :param in_reply_to : to specify the comment you reply
            :type in_reply_to: int
            :return json data
        """

        params = {'token': token, 'show': show, 'text': text}

        # handle in_reply_to parameter
        if in_reply_to is not None:
            if not in_reply_to.isdigit():
                raise Exception('Invalid in_reply_to parameter')
            params['in_reply_to'] = in_reply_to

        return self.query('comments/post/show.json', params)

    def comments_post_episode(self, token, show, season, episode,
                             text, in_reply_to=None):
        """
            post a comment on the episode
            :param token : token of the authenticated member
            :type token: string
            :param show : the name of the show
            :type show: string
            :param season : the season
            :type season: int
            :param episode : the episode
            :type episode: int
            :param in_reply_to : to specify the comment you reply
            :type in_reply_to: int
            :return json data
        """
        params = {'token': token,
                  'show': show,
                  'season': season,
                  'episode': episode,
                  'text': text}

        # handle in_reply_to parameter
        if in_reply_to is not None:
            if not in_reply_to.isdigit():
                raise Exception('Invalid in_reply_to parameter')
            params['in_reply_to'] = in_reply_to

        return self.query('comments/post/episode.json', params)

    def comments_post_member(self, token, member, text, in_reply_to=None):
        params = {'token': token,
                  'member': member,
                  'text': text}

        # handle in_reply_to parameter
        if in_reply_to is not None:
            if not in_reply_to.isdigit():
                raise Exception('Invalid in_reply_to parameter')
            params['in_reply_to'] = in_reply_to

        return self.query('comments/post/episode.json', params)

    def comments_subscribe(self, token, ref_id):
        """
            subscribe to the comment of the given ref by mail
            :param token : token of the authenticated member
            :type token: string
            :param ref_id : the ref_id of the comment to subscribe
            :type ref_id: int
            :return json data
        """

        params = {'token': token, 'ref_id': ref_id}

        return self.query('comments/subscribe.json', params)

    def comments_unsubscribe(self, token, ref_id):
        """
            unsubscribe to the comment of the given ref
            :param token : token of the authenticated member
            :type token: string
            :param ref_id : the ref_id
            :type ref_id: int
            :return json data
        """
        params = {'token': token, 'ref_id': ref_id}

        return self.query('comments/subscribe.json', params)

    def timeline_home(self, number=None):
        """
            display the last 'n' event from the website
            :param number: a number between 1 and 100
            :type number: int
            :return json data
        """

        params = {}

        # handle number parameter
        if number is not None:
            if 0 == number or 101 < number:
                raise Exception('Invalid number parameter')
            params['number'] = number

        return self.query('timeline/home.json', params)

    def timeline_friends(self, token, number):
        """
            display the timeline of the 'n' last event of the auth'ed member
            :param token: string the member name
            :type token: string
            :param number: number between 1 and 100
            :type number: int
            :return json data
        """

        params = {'token': token}

        # handle number parameter
        if number is not None:
            if 0 == number or 101 < number:
                raise Exception('Invalid number parameter')
            params['number'] = number

        return self.query('timeline/friends.json', params)

    def timeline_member(self, member, token=None, number=None):
        """
            display the timeline of the 'n' last event of the member
            :param member: the member name
            :type member: string
            :param token: string the member name
            :type token: string
            :param number: number between 1 and 100
            :type number: int
            :return json data
        """

        params = {}

        # handle token parameter
        if token is not None:
            params['token'] = token

        # handle number parameter
        if number is not None:
            if 0 == number or not 101 < number:
                raise Exception('Invalid number parameter')
            params['number'] = number

        return self.query('timeline/member/' + member + '.json', params)

    def message_inbox(self, token, page=None):
        """
            display the inbox by page of 15 messages
            :param token: string the member name
            :type token: string
            :param page: the page number to display
            :type number: int
            :return json data
        """
        params = {'token': token}

        if page is not None:
            if not page.isdigit():
                raise Exception('Invalid page parameter')
            params['page'] = page

        return self.query('messages/inbox.json', params)

    def message_discussion(self, token, my_id, page=None):
        """
            display the discussion from the given id by page of 15 messages
            :param token: string the member name
            :type token: string
            :param id: the id of the discussion
            :type id: int
            :param page: number between 1 and 100
            :type page: int
            :return json data
        """
        params = {'token': token}

        if page is not None:
            if not page.isdigit():
                raise Exception('Invalid page parameter')
            params['page'] = page

        return self.query('messages/discussion/' + my_id + '.json', params)

    def message_send_new(self, token, title, text, recipient):
        """
            send a response to the discussion
            :param token: string the member name
            :type token: string
            :param title: string the title of discussion
            :type title: string
            :param text: string the discussion
            :type text: string
            :param recipient: string recipient
            :type recipient: string
            :return json data
        """
        params = {
            'token': token,
            'title': title,
            'text': text,
            'recipient': recipient}

        return self.query('messages/send.json', params, 'post')

    def message_send_response(self, token, text, discussion_id):
        """
            send a response to the discussion
            :param token: string the member name
            :type token: string
            :param text: string the discussion
            :type text: string
            :param discussion_id: the id of the discussion
            :type discussion_id: int
            :return json data
        """
        params = {
            'token': token,
            'text': text,
            'discussion_id': discussion_id}

        return self.query('messages/send.json', params, 'post')

    def message_delete(self, token, my_id):
        """
            delete the given message by its ID
            :param token: string the member name
            :type token: string
            :param id: the id of the discussion
            :type id: int
            :return json data
        """
        params = {'token': token}

        return self.query('messages/delete/' + my_id + '.json', params)
