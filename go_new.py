# -*- coding: utf-8 -*-
import argparse

import ConfigParser
import os
import sys

from pythonseries.pythonseries import Client

config = ConfigParser.ConfigParser()
config.read(os.getcwd() + '/series.config')
c = Client(api_key=config.get('api', 'key'))


def get_token():
    """
        get the token of the member
    """
    import hashlib
    hash_pass = hashlib.md5(config.get('auth', 'password')).hexdigest()
    # return the token
    return c.members_auth(config.get('auth', 'login'), hash_pass)


def do_action(options):

    data = {}
    if hasattr(options, 'shows_search'):
        """
        show_search wrapper
        """
        if options.title:
            print "you want to search the title of a movie " + options.title
            data = c.shows_search(options.title)
            print "%15s %40s" % ("URL", "Title")
            for show in data['shows']:
                print "%15s %40s" % (data['shows'][show]['url'],
                                 data['shows'][show]['title'])
        else:
            print "title mandatory"
    elif hasattr(options, 'shows_display'):
        """
        show_display wrapper
        """
        if options.url:
            print "you want to display the content of a serie " + options.url
            data = c.shows_display(options.url)
            print "Genre:"
            for genre in data['show']['genres'].values():
                print "-" + genre
            print "Description: %s" % data['show']['description']
            print "seasons:"
            for season in data['show']['seasons']:
                ep = data['show']['seasons'][season]['episodes']
                print "%s sur %s" % (season, ep)
        else:
            print "url of the serie is mandatory"
    elif hasattr(options, 'shows_episodes'):
        """
        shows_episodes wrapper
        """
        if options.url is None:
            print "url is mandatory"
        else:
            print "you want to search serie %s " % options.url
            params = {}
            params['url'] = options.url
            if options.episode:
                params['episode'] = options.episode

            if options.season:
                params['season'] = options.season

            if options.summary:
                params['summary'] = options.summary

            data = c.shows_episodes(**params)
            # oops we try to find a serie that does not exist
            if 'seasons' not in data.keys() > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:

                # all the data
                # print data
                for season in data['seasons']:
                    for ep in data['seasons'][season]['episodes']:
                        num = data['seasons'][season]['episodes'][ep]['number']
                        ttl = data['seasons'][season]['episodes'][ep]['title']
                        print "Number: {number} Title: {title} ".\
                        format(number=num, title=ttl)
#    elif hasattr(options, 'add:
#        """
#        shows_add wrapper
#        """
#        print "you want to add a file to your account"
#        data = c.shows_add(get_token())
#    elif hasattr(options, 'remove:
#        """
#        shows_remove wrapper
#        """
#        print "you want to remove a file to your account"
#        data = c.shows_remove(get_token())
#    elif hasattr(options, 'recommend:
#        """
#        shows_recommend wrapper
#        """
#        print "you want to recommend a file to a friend"
#        data = c.shows_recommend(get_token())
#        print data
#    elif hasattr(options, 'archive:
#        """
#        shows_archive wrapper
#        """
#        print "you want to archive a serie"
#        data = c.shows_archive(get_token())
#        print data
#    elif hasattr(options, 'scrapper:
#        """
#        shows_scrapper wrapper
#        """
#        data = c.shows_scrapper()
#        print data
#    elif hasattr(options, 'unarchive:
#        """
#        shows_unarchive wrapper
#        """
#        print "you want to get out the serie from your archives"
#        data = c.shows_unarchive(get_token())
#        print data
    elif hasattr(options, 'shows_characters'):
        """
        shows_characters wrapper
        """
        if options.url is None:
            print "url is mandatory"
        else:
            print "you want to search characters of the serie {characters}"\
                    .format(characters=options.url)
            params = {}
            params['url'] = options.url

            if options.summary:
                params['summary'] = options.summary

            if options.char_id:
                params['the_id'] = options.char_id

            data = c.shows_characters(**params)

            # oops we try to find a serie that does not exist
            if 'characters' not in data.keys() > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                for character in data['characters']:
                    name = data['characters'][character]['name']
                    the_id = data['characters'][character]['id']
                    print "%8s %s " % (the_id, name)

    elif hasattr(options, 'shows_similar'):
        if options.url:
            print "you want to find similar series to " + options.url
            data = c.shows_similar(options.url)
            print "{title:^40} {url:^20}".format(title='title', url='url')
            for show in data['shows']:
                title = data['shows'][show]['title']
                url = data['shows'][show]['url']
                print u"{title:<30} {url:<20}".format(title=title, url=url)
        else:
            print "url of the serie is mandatory"
    elif hasattr(options, 'shows_videos'):
        if options.url:
            print "you want to search videos of serie " + options.url
            params = {}
            params['url'] = options.url

            if options.season:
                params['season'] = options.season

            if options.episode:
                params['episode'] = options.episode

            data = c.shows_videos(**params)

            # oops we try to find a serie that does not exist
            if 'videos' not in data.keys() > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                # all the data
                # print data
                print "title %14s - youtube id %10s" % (' ', ' ')
                for video in data['videos']:
                    print "%20s - %10s" % \
                          (data['videos'][video]['title'],
                           data['videos'][video]['youtube_id'])
        else:
            print "url of the serie is mandatory"

    elif hasattr(options, 'subtitles_last'):
        """
        subtitles_last wrapper
        """
        print "you want to see the last subtitles"
        params = {}

        if options.language:
            params['language'] = options.language

        if options.number:
            params['number'] = options.number

        data = c.subtitles_last(**params)

        # oops we try to find a serie that does not exist
        if 'subtitles' not in data.keys() > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            # all the data
            # print data
            print "{season:^10} {ep:^10} {title:^20} {lang} {file:^50}".\
                format(season='Season',
                       ep='Episode',
                       title='Title',
                       lang='Lang',
                       file='File')
            for last_sub in data['subtitles']:
                season = data['subtitles'][last_sub]['season']
                ep = data['subtitles'][last_sub]['episode']
                title = data['subtitles'][last_sub]['title'],
                lang = data['subtitles'][last_sub]['language']
                my_file = data['subtitles'][last_sub]['file']
                print "{season:<10} {ep:<5} {title:<20} {lang:<5} {file:<50}"\
                      .format(season=season,
                             ep=ep,
                             title=title,
                             lang=lang,
                             file=my_file)

    elif hasattr(options, 'subtitles_show'):
        """
        subtitles_show wrapper
        """
        if options.url:
            print "you want to search subtitles of serie " + options.url
            params = {}
            params['url'] = options.url

            if options.language:
                params['language'] = options.language
            if options.season:
                params['season'] = options.season
            if options.episode:
                params['episode'] = options.episode

            data = c.subtitles_show(**params)

            # oops we try to find a serie that does not exist
            if 'subtitles' not in data.keys() > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                print "{season:^10} {ep:^10} {lang:^5} {file:^50} {url:^50}".\
                    format(season='Season',
                           ep='Episode',
                           lang='Lang',
                           file='File',
                           url='URL')

                for subtitle in data['subtitles']:
                    season = data['subtitles'][subtitle]['season']
                    ep = data['subtitles'][subtitle]['episode']
                    language = data['subtitles'][subtitle]['language']
                    my_file = data['subtitles'][subtitle]['file']
                    url = data['subtitles'][subtitle]['url']
                    print "{season:<10} {ep:<5}  {lang:<5} \
{file:<50} {url:<50}".\
                          format(season=season,
                                 ep=ep,
                                 lang=language,
                                 file=my_file,
                                 url=url)
        else:
            print "url of the serie is mandatory"
    elif hasattr(options, 'subtitles_show_by_file'):
        """
        subtitles_show_by_file wrapper
        """
        print "you want to get the subtitle from a given filename" + \
                options.my_file
        # todo fix the name of the options
        data = c.subtitles_show_by_file(options.my_file, options.language)
        if 'subtitles' not in data.keys() > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']

    elif hasattr(options, 'planning_general'):
        """
        planning_general wrapper
        """
        data = c.planning_general()
        # print the Heading
        print u"{show:^40} {number:^10} {title:^30}".\
            format(show='Show', number='Number', title='Title')
        # print the lines
        for planning in data['planning']:
            show = data['planning'][planning]['show']
            number = data['planning'][planning]['number']
            title = data['planning'][planning]['title']
            print u"{show:<40} {number:<10} {title:<30}".\
                format(show=show, number=number, title=title)

    elif hasattr(options, 'planning_member'):
        """
        planning_member wrapper
        """
        data = c.planning_member(get_token())
        # print the Heading
        print u"{show:^40} {number:^10} {title:^30}".\
            format(show='Show', number='Number', title='Title')
        # print the lines
        for planning in data['planning']:
            show = data['planning'][planning]['show']
            number = data['planning'][planning]['number']
            title = data['planning'][planning]['title']
            print u"{show:<40} {number:<10} {title:<30}".\
                format(show=show, number=number, title=title)

    elif hasattr(options, 'member_is_active'):
        """
        member_is_active wrapper
        """
        print "you want to check if the user is autenticated"
        # todo : fix the options.token
        data = c.member_is_active(get_token())
        if 'token' not in data.keys() > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print "Member is active"

    elif hasattr(options, 'member_infos'):
        """
        member_infos wrapper
        """
        print "you want to display the info of member"
        params = {}
        if options.login:
            params['login'] = options.login
        if options.token:
            params['token'] = get_token()
        if options.nodata:
            params['nodata'] = options.nodata
        if options.since:
            params['since'] = options.since
        data = c.member_infos(**params)

        if 'member' not in data.keys() > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            if data['member']['login'] is None:
                print "unknow member"
            else:
                stats = data['member']['stats']
                print "Login:" + data['member']['login']
                print "Avatar:" + data['member']['avatar']
                print "Stats >>"
                print "Friends:" + stats['friends']
                print "Shows: %i" % stats['shows']
                print "Seasons: %i" % stats['seasons']
                print "Episodes: %i" % stats['episodes']
                print "Progress:" + stats['progress']
                print "ToWatch: %i" % stats['episodes_to_watch']
                print "TimeOnTV: %s" % stats['time_on_tv']
                print "TimeToSpend: %s " % stats['time_to_spend']
                for show in data['member']['shows']:
                    print "url " + data['member']['shows'][show]['url'], \
                          "title " + data['member']['shows'][show]['title']

    elif hasattr(options, 'members_episodes'):
        print "you want to display the 'next' Episodes"
        params = {}
        params['token'] = get_token()
        if options.subtitles:
            params['subtitles'] = options.subtitles
        if options.show:
            params['show'] = options.show
        if options.view:
            params['view'] = options.view

        data = c.members_episodes(**params)

        for ep in data['episodes']:
            season = data['episodes'][ep]['season']
            episode = data['episodes'][ep]['episode']
            show = data['episodes'][ep]['show']
            for sub in  data['episodes'][ep]['subs']:
                lang = data['episodes'][ep]['subs'][sub]['language']
                my_file = data['episodes'][ep]['subs'][sub]['file']
                url = data['episodes'][ep]['subs'][sub]['url']
                source = data['episodes'][ep]['subs'][sub]['source']
                qty = data['episodes'][ep]['subs'][sub]['quality']
                print "%s %s %s %s %50s %40s %20s %10s" % \
                (season, episode, show, lang, my_file, url, source, qty)

    elif hasattr(options, 'members_note'):
        if options.note and options.episode and options.season and options.url:
            print "You want to give a note %s to \
the episode %s (season %s) of the serie %s" % (options.note,
                                               options.episode,
                                               options.season,
                                               options.url)
            params = {
                  'token': get_token(),
                  'url': options.url,
                  'episode': options.episode,
                  'season': options.season,
                  'note': options.note
                  }
            data = c.members_note(**params)
            if len(data['errors']) > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                print "note submitted"
        else:
            print "All parameters are mandatory"

    elif hasattr(options, 'members_downloaded'):
        if options.url and options.episode and options.season:
            print "You want to set the episode %s (season %s) of the serie\
 %s as downloaded" % (options.episode, options.season, options.url)
            params = {
                  'token': get_token(),
                  'url': options.url,
                  'episode': options.episode,
                  'season': options.season,
                  }
            data = c.members_downloaded(**params)
            if len(data['errors']) > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                print "episode marked as downloaded"
        else:
            print "All parameters are mandatory"

    elif hasattr(options, 'members_notifications'):
        print "you want to display the notifications "
        params = {'token': get_token()}
        if options.summary:
            params['summary'] = options.summary
        if options.number:
            params['number'] = options.number
        if options.last_id:
            params['last_id'] = options.last_id
        if options.sort:
            params['sort'] = options.sort

        data = c.members_notifications(**params)
        if 'text' not in data.keys() > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            if len(data['notifications']) == 0:
                print "no notification"
            else:
                print "%10s %2s %40s" % ('Date', 'Seen?', 'Text')
                for notif in data['notifications']:
                    text = data['notifications'][notif]['text']
                    my_date = data['notifications'][notif]['timestamp']
                    seen = data['notifications'][notif]['seen']

                    print "{date:<10} {seen:<2} {text:<40}".\
                        format(date=my_date, seen=seen, text=text)

    elif hasattr(options, 'members_option'):
        if options.option and options.value:
            msg = "You want "
            if options.value == 'read':
                value = 0
                msg += "to read"
            else:
                value = 1
                msg += "to modify"
            msg += " option to %s" % options.option
            print msg
            params = {
                  'token': get_token(),
                  'value': value,
                  'option': options.option
                  }
            data = c.members_option(**params)
            if len(data['errors']) > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                print "option value %s set to %s" % (data['option']['name'],
                                                      data['option']['value'])
        else:
            print "All parameters are mandatory"

    elif hasattr(options, 'members_signup'):
        if options.login and options.password and options.mail:
            params = {'login': options.login,
                      'password': options.password,
                      'mail': options.mail}
            data = c.members_signup(**params)
            if len(data['errors']) > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                print "Account created"
        else:
            print "All parameters are mandatory"

    elif hasattr(options, 'members_friends'):
        params = {}
        if options.token:
            params['token'] = get_token()
        if options.login:
            params['login'] = options.login
        data = c.members_friends(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            if len(data['friends']) == 0:
                print "No friends found"
            else:
                for friend in data['friends']:
                    print data['friends'][friend]

    elif hasattr(options, 'members_badges'):
        params = {}
        if options.token:
            params['token'] = get_token()
        if options.login:
            params['login'] = options.login
        data = c.members_badges(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            if len(data['badges']) == 0:
                print "No badge found"
            else:
                for badge in data['badges']:
                    name = data['badges'][badge]['name']
                    description = data['badges'][badge]['description']
                    print "%s -*- %s" % (name, description)

    elif hasattr(options, 'members_add'):
        params = {}
        params['token'] = get_token()
        params['login'] = options.login
        data = c.members_add(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print "member %s added" % options.members_add

    elif hasattr(options, 'members_delete'):
        params = {}
        params['token'] = get_token()
        params['login'] = options.login
        data = c.members_delete(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print "member %s deleted" % options.members_delete

    elif hasattr(options, 'members_search'):
        params = {}
        params['login'] = options.login
        data = c.members_search(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            if len(data['members']) == 0:
                print "no member found"
            else:
                for member in data['members']:
                    print data['members'][member]['login']

    elif hasattr(options, 'members_block'):
        params = {}
        params['token'] = get_token()
        params['login'] = options.login
        data = c.members_block(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print "member %s blocked" % options.members_block

    elif hasattr(options, 'members_unblock'):
        params = {}
        params['token'] = get_token()
        params['login'] = options.login
        data = c.members_unblock(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print "member %s unblocked" % options.members_unblock

    elif hasattr(options, 'members_options'):
        params = {}
        params['token'] = get_token()
        data = c.members_options(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            for option in data['options']:
                for source in data['options'][option]:
                    enabled = data['options'][option][source]['enabled']
                    name = data['options'][option][source]['name']
                    print "%s ? %s" % (name, enabled)

    elif hasattr(options, 'members_sync'):
        print "API implemented but no example ready yet"

    elif hasattr(options, 'comments_show'):
        if options.url:
            params = {'url': options.url}
            data = c.comments_show(**params)
            if len(data['errors']) > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                if len(data['comments']) == 0:
                    print "no comment"
                else:
                    print "%20s - %14s - %40s" % ('Login', 'Date', 'Text')
                    for comment in data['comments']:
                        text = data['comments'][comment]['text']
                        my_date = data['comments'][comment]['date']
                        login = data['comments'][comment]['login']
                        print "%20s - %14s - %40s" % (login, my_date, text)
        else:
            print "the url of the serie is mandatory"
    elif hasattr(options, 'comments_episode'):
        if options.season and options.episode and options.url:
            params = {'url': options.url,
                      'episode': options.episode,
                      'season': options.season}
            data = c.comments_episode(**params)
            if len(data['errors']) > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                if len(data['comments']) == 0:
                    print "no comment"
                else:
                    print "%20s - %14s - %40s" % ('Login', 'Date', 'Text')
                    for comment in data['comments']:
                        text = data['comments'][comment]['text']
                        my_date = data['comments'][comment]['date']
                        login = data['comments'][comment]['login']
                        print "%20s - %14s - %40s" % (login, my_date, text)
        else:
            print "All parameters are mandatory"
    elif hasattr(options, 'comments_member'):
        data = c.comments_member(options.login)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            if len(data['comments']) == 0:
                print "no comment"
            else:
                print "%14s - %40s" % ('Date', 'Text')
                for comment in data['comments']:
                    text = data['comments'][comment]['text']
                    my_date = data['comments'][comment]['date']
                    print "%14s - %40s" % (my_date, text)
    elif hasattr(options, 'comments_post_show'):
        print "API implemented but no example ready yet"
    elif hasattr(options, 'comments_post_episode'):
        print "API implemented but no example ready yet"
    elif hasattr(options, 'comments_post_member'):
        print "API implemented but no example ready yet"
    elif hasattr(options, 'comments_subscribe'):
        print "API implemented but no example ready yet"
    elif hasattr(options, 'comments_unsubscribe'):
        print "API implemented but no example ready yet"
    elif hasattr(options, 'timeline_home'):
        data = c.timeline_home(options.number)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print "%12s - %20s - %5s - %20s - %40s - %40s" % \
            ('Date', 'Login', 'Types', 'URL', 'Event', 'Title')
            for timeline in data['timeline']:
                types = data['timeline'][timeline]['type']
                if 'data' in data['timeline'][timeline].keys():
                    url = data['timeline'][timeline]['data']['url']
                    title = data['timeline'][timeline]['data']['title']
                else:
                    url = ""
                    title = ""
                my_date = data['timeline'][timeline]['date']
                login = url = data['timeline'][timeline]['login']
                html = data['timeline'][timeline]['html']
                print "%12s - %20s - %5s - %20s - %40s - %40s" % \
                (my_date, login, types, url, html, title)
    elif hasattr(options, 'timeline_friends'):
        data = c.timeline_friends(get_token(), options.number)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print "%12s - %20s - %5s - %20s - %40s - %40s" % \
            ('Date', 'Friends', 'Types', 'URL', 'Event', 'Title')
            for timeline in data['timeline']:
                types = data['timeline'][timeline]['type']
                if 'data' in data['timeline'][timeline].keys():
                    url = data['timeline'][timeline]['data']['url']
                else:
                    url = ""
                if 'title' in data['timeline'][timeline].keys():
                    title = data['timeline'][timeline]['data']['title']
                else:
                    title = ""
                my_date = data['timeline'][timeline]['date']
                login = url = data['timeline'][timeline]['login']
                html = data['timeline'][timeline]['html']
                print "%12s - %20s - %5s - %20s - %40s - %40s" % \
                (my_date, login, types, url, html, title)
    elif hasattr(options, 'timeline_member'):
        if options.login:
            params = {'member': options.login}
            if options.login:
                params['number'] = options.number
            if options.token:
                params['token'] = get_token()
            data = c.timeline_member(**params)
            if len(data['errors']) > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                print "%12s - %20s - %5s - %20s - %40s - %40s" % \
                ('Date', 'Friends', 'Types', 'URL', 'Event', 'Title')
                for timeline in data['timeline']:
                    types = data['timeline'][timeline]['type']
                    if 'data' in data['timeline'][timeline].keys():
                        url = data['timeline'][timeline]['data']['url']
                    else:
                        url = ""
                    if 'title' in data['timeline'][timeline].keys():
                        title = data['timeline'][timeline]['data']['title']
                    else:
                        title = ""
                    my_date = data['timeline'][timeline]['date']
                    login = url = data['timeline'][timeline]['login']
                    html = data['timeline'][timeline]['html']
                    print "%12s - %20s - %5s - %20s - %40s - %40s" % \
                    (my_date, login, types, url, html, title)
        else:
            print "login of the member mandatory"
    elif hasattr(options, 'message_inbox'):
        params = {'token': get_token()}
        if options.page:
            params['page'] = options.page
        data = c.message_inbox(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            if len(data['discussions']) == 0:
                print "no message found"
            else:
                for msg in data['discussions']:
                    print data['discussions'][msg]

    elif hasattr(options, 'message_discussion'):
        if options.id:
            params = {'token': get_token(),
                      'my_id': options.id}
            if options.page:
                params['page'] = options.page
            data = c.message_discussion(**params)
            if len(data['errors']) > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                if len(data['discussions']) == 0:
                    print "no message found"
                else:
                    for msg in data['discussions']:
                        print data['discussions'][msg]
        else:
            print "ID is mandatory"
    elif hasattr(options, 'message_send_new'):
        params = {'token': get_token(),
                  'title': options.title,
                  'text': options.text,
                  'recipient': options.recipient}
        data = c.message_send_new(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print data

    elif hasattr(options, 'message_send_response'):
        if options.text and options.id:
            params = {'token': get_token(),
                      'text': options.text,
                      'discussion_id': options.id}
            data = c.message_send_response(**params)
            print data
        else:
            print "All parameters are mandatory"
    elif hasattr(options, 'message_delete'):
        if options.id:
            params = {'token': get_token(), 'my_id': options.id}
            data = c.message_delete(**params)
            if len(data['errors']) > 0:
                for error in data['errors']:
                    print "Error:"
                    print data['errors'][error]['content']
            else:
                print data
        else:
            print "All parameters are mandatory"


def main():
    parser = argparse.ArgumentParser(prog="go",
                                     usage='%(prog)s [options]',
                                     description='BetaSeries API Management',
                                     conflict_handler='resolve',
                                     add_help=True)

    subparsers = parser.add_subparsers(help='sub-command help')
    group0 = subparsers.add_parser('shows_search', help='Search series: \
use --shows_search --title <title>')
    # group0 = subparsers.add_parser(help="Search series",
# "use --shows_search --title <title>")
    group0.add_argument("shows_search", action="store_true",
                    help='Search series: use --shows_search --title <title>')
    group0.add_argument("--title", action="store", required=True,
                        help="make a search by title")

    # group the options for handling Display of series parameters
    group1 = subparsers.add_parser("shows_display",
            help="Details of series: use --shows_display --url <url>")
    group1.add_argument("shows_display", action="store_true",
                    help="Details of series : use --shows_display --url <url>")
    group1.add_argument("--url", action="store", required=True,
                     help="the url/name of the given serie")

    group2 = subparsers.add_parser("shows_episodes", help="Show Episodes: use \
--shows_episodes --url <serie> (--season <num>) (--episode <num>)\
(--summary) to filter episodes you want to search")
    group2.add_argument("shows_episodes", action="store_true", help="Episodes:\
--shows_episodes --url <serie> (--season <num>) (--episode <num>)\
(--summary) to filter episodes you want to search")
    group2.add_argument("--url", action="store", required=True,
                     help="the url of the given serie")
    group2.add_argument("--episode", action="store",
                     help="the number of the episode (optional)")
    group2.add_argument("--season", action="store",
                     help="the number of the season (optional)")
    group2.add_argument("--summary", action="store_true",
                     help="boolean set to false by default, \
                     to only get the summary of the episode (optional)")

    # group the options for handling Characters parameters
    group3 = subparsers.add_parser("shows_characters", help="Show Characters:\
 use shows_characters --url <serie> (--summary)\
(--char_id <num>) to find characters for the series you want to search")
    group3.add_argument('shows_characters', action="store_true",
                        help="use shows_characters --url <serie> (--summary)\
(--char_id <num>) to find characters for the series you want to search")
    group3.add_argument("--url", action="store", required=True,
                     help="give the name of the serie to get\
 the list of characters of this one")
    group3.add_argument("--summary", action="store_true",
                     help="boolean set to true by default,\
 only get the summary of the characters (optional)")
    group3.add_argument("--char_id", action="store",
                     help="display info of THIS character (optional)")

    # group the options for handling Similar shows
    group13 = subparsers.add_parser("shows_similar", help="Similar Shows:\
use --shows_similar --url <serie> to find similar serie")
    group13.add_argument('shows_similar', action="store_true",
help="Similar Shows: use --shows_similar --url <serie> to find similar serie")
    group13.add_argument("--url", action="store", required=True,
                     help="give the name of the serie to get similar ones")

    # group the options for handling Videos parameters
    group4 = subparsers.add_parser("shows_videos", help="Videos: use \
shows_videos --url <serie> (--season <num>)\
(--episode <num> to filter episodes you want to search)")
    group4.add_argument("shows_videos", action="store_true", help="Videos: use\
 shows_videos --url <serie> (--season <num>)\
(--episode <num> to filter episodes you want to search)")
    group4.add_argument("--url", action="store", required=True,
                     help="give the name of the serie you want to search")
    group4.add_argument("--season", action="store",
                     help="display the list of video of the given season\
(optional)")
    group4.add_argument("--episode", action="store",
                     help="display the list of video of the given episode\
(optional)")

    group5 = subparsers.add_parser("subtitles_show", help="Subtitles: use \
 subtitles_show --url <serie> --language <lang> --season <num>\
 --episode <num> to find subtitles you want to search")
    group5.add_argument("subtitles_show", action="store_true",
        help="Subtitles:use subtitles_show --url <serie> \
        --language <lang> --season <num>\
 --episode <num> to find subtitles you want to search")
    group5.add_argument("--url", action="store", required=True,
                    help="give the name of the serie you want to see subtitle")
    group5.add_argument("--language", action="store",
                     help="display the sub for the given language: vo or vf",
                     choices=('vo', 'vf'))
    group5.add_argument("--season", action="store",
                     help="display the subtitles of the given season")
    group5.add_argument("--episode", action="store",
                     help="display the subtitles of the given episode")

    group6 = subparsers.add_parser("subtitles_last", help="Last Subtitles: \
use subtitles_last --language <lang> --number <num>\
 to search subtitle you want to search")
    group6.add_argument("subtitles_last", action="store_true")
    group6.add_argument("--language", action="store",
                     help="display the last sub \
for a given language: vo or vf")
    group6.add_argument("--number", action="store",
                     help="display the 'n' last subtitles")

    group7 = subparsers.add_parser("subtitles_show_by_file", help="Subtitle \
by Filename: use subtitles_show_by_file --my_file <file> --language <lang>\
to search subtitle you want to search")
    group7.add_argument('subtitles_show_by_file', action="store_true")
    group7.add_argument("--my_file", action="store", required=True,
                      help="display the subtitles from a given filename")
    group7.add_argument("--language", action="store",
                     help="filter subtitle for a given language: vo or vf",
                     choices=('vo', 'vf'))

    group8 = subparsers.add_parser("planning_general", help="Planning General:\
 display the general planning")
    group8.add_argument("planning_general", action="store_true",
                      help="display the general planning")

    group9 = subparsers.add_parser("planning_member", help="Planning Member:\
 display the planning of the member")
    group9.add_argument("planning_member", action="store_true",
                      help="display the planning of the member")

    group10 = subparsers.add_parser("member_is_active", help="Member: \
is he active ? check if the member is active")
    group10.add_argument("member_is_active", action="store_true",
                      help="check if the member is active")

    group11 = subparsers.add_parser("member_infos", help="Member infos:\
 use members_infos --login <login> \
--token (optional) --nodata (optional) --since timestamp date")
    group11.add_argument("member_infos", action="store_true",
help="Member: infos ?  use members_infos --login <login> \
--token (optional) --nodata (optional) --since timestamp date")
    group11.add_argument("--login", action="store",
                      help="get info from the login of the member")
    group11.add_argument("--token", action="store_true",
                      help="to use the token or not, to get his/our info")
    group11.add_argument("--nodata", action="store_true",
                      help="will ONLY display login and date")
    group11.add_argument("--since", action="store",
                      help="give a timestamp date to get info from it")

    group12 = subparsers.add_parser("members_episodes",
help="Member Episodes: members_episodes --subtitles <all|vovf|vf>\
 --show <serie> --view <view>")
    group12.add_argument('members_episodes', action="store_true",
help="Member : Episodes ? members_episodes --subtitles <all|vovf|vf>\
 --show <serie> --view <view>")
    group12.add_argument("--subtitles", action="store",
                      help="filter serie with subtitles : all / vovf / vf",
                     choices=('all', 'vovf', 'vf'))
    group12.add_argument("--show", action="store",
                      help="give the name of the serie to ONLY get its \
                      episodes")
    group12.add_argument("--view", action="store",
                      help="set a number of next episode to view or just \
'next' to get the next one")

    group14 = subparsers.add_parser("members_note", help="Member Note:\
use members_note --note <note> --url <url> --episode <num> --season <num>.\
To give a note to the complet serie put --season 0 and --episode 0")
    group14.add_argument('members_note', action="store_true",
help="Member : Note use members_note --note <note> --url <url> --episode <num>\
 --season <num>.\ To give a note to the complet serie put --season 0 and\
 --episode 0")
    group14.add_argument("--url", action="store", required=True,
                      help="url of the serie to evluate. eg breakingbad not\
                      'Breaking Bad'")
    group14.add_argument("--episode", action="store", required=True,
                      help="number of the episode of the serie to evaluate")
    group14.add_argument("--season", action="store", required=True,
                      help="number of the season of the serie to evaluate")
    group14.add_argument("--note", action="store", required=True,
                      help="give a note between 1 and 5", choices=range(1, 6),
                      type=int)

    group15 = subparsers.add_parser("members_downloaded", help="Member \
Downloaded: use members_downloaded --url <url> --episode <num> --season <num>")
    group15.add_argument('members_downloaded', action="store_true",
help="Member : Downloaded use members_downloaded --url <url> --episode <num>\
 --season <num>.")
    group15.add_argument("--url", action="store", required=True,
                      help="the url of the serie to mark as downloaded\
eg breakingbad not 'Breaking Bad'")
    group15.add_argument("--episode", action="store", required=True,
                      help="the number of the episode to mark as downloaded")
    group15.add_argument("--season", action="store", required=True,
                      help="the season of the episode to mark as downloaded")

    group16 = subparsers.add_parser("members_notifications", help="Member \
Notifications: use members_notifications \
 --summary=True/False (optional: default False) --number <num> (optional)\
 --last_id <num> (optional) --sort ASC|DESC (optional)\
 dont mix --last_id and --sort or all notifications could not be get")
    group16.add_argument("members_notifications", action="store_true",
                    help="Member :Notifications: use members_notifications \
 --summary=True/False (optional: default False) --number <num> (optional)\
 --last_id <num> (optional) --sort ASC|DESC (optional)\
 dont mix --last_id and --sort or all notifications could not be get")
    group16.add_argument("--summary", action="store_true",
                      help="to get only the number of unread notification")
    group16.add_argument("--number", action="store",
                      help="to get the notification from this number")
    group16.add_argument("--last_id", action="store",
                      help="to get the last 'n' notifications")
    group16.add_argument("--sort", action="store",
                      help="to sort the display, use asc or desc")

    group17 = subparsers.add_parser("members_option", help="Members :\
    Option use members_option --option <downloaded|notation|decalage>\
 --value <read|edit> (mandatory)")
    group17.add_argument("members_option", action="store_true",
    help="Members :Option use members_option\
     --option <downloaded|notation|decalage>\
 --value <read|edit> (mandatory)")
    group17.add_argument("--option", action="store", required=True,
                      help="can be one of <downloaded|notation|decalage>",
                      choices=('downloaded', 'notation', 'decalage'))
    group17.add_argument("--value", action="store", required=True,
                      help="read : to read options and\
                      edit to modify the option",
                      choices=('edit', 'read'))

    group18 = subparsers.add_parser("members_signup", help="Members Signup\
 use members_signup --login <login> --password <password> --mail <email>")
    group18.add_argument("--members_signup", action="store_true",
        help="Members Signup: use members_signup --login <login>\
 --password <password> --mail <email>")
    group18.add_argument("--login", action="store", required=True,
                      help="the login: max 24 chars")
    group18.add_argument("--password", action="store", required=True,)
    group18.add_argument("--mail", action="store", required=True,)

    group19 = subparsers.add_parser("members_friends",
        help="Members Friends: use --members_friends --token \
to get your friends (optional) OR --login <login> \
to get the friends of this member (optional)")
    group19.add_argument("members_friends", action="store_true",
help="Members Friends: use --members_friends --token \
to get your friends (optional) OR --login <login> \
to get the friends of this member (optional)")
    group19.add_argument("--token", action="store_true")
    group19.add_argument("--login", action="store")

    group20 = subparsers.add_parser("members_badges",
help="Members Badges: use members_badges --token to get your friends OR\
 --login <login> to get the friends of this member")
    group20.add_argument("members_badges", action="store_true",
help="Members Badges: use members_badges --token to get your friends OR\
 --login <login> to get the friends of this member")
    group20.add_argument("--token", action="store_true")
    group20.add_argument("--login", action="store")

    group21 = subparsers.add_parser("members_add",
        help="Members Add: give the login of the friend to add")
    group21.add_argument("members_add", action="store_true",
        help="Members Add: give the login of the friend to add")
    group21.add_argument("--login", action="store", required=True)

    group22 = subparsers.add_parser("members_delete",
            help="Members Delete: give the login of the friend to delete")
    group22.add_argument("members_delete",
            help="Members Delete: give the login of the friend to delete",
                       action="store_true")
    group22.add_argument("--login", action="store", required=True)

    group23 = subparsers.add_parser("members_search", help="Members Search \
get a list of 10 friends starting by this string, use members_search\
 --login <login>")
    group23.add_argument("members_search",
        help="Members Search get a list of 10 friends starting by this string",
                         action="store_true")
    group23.add_argument("--login", action="store", required=True)

    group24 = subparsers.add_parser("members_block", help="Members Block:\
 give the login of the member to block, use members_block --login <login>")
    group24.add_argument("members_block", action="store_true")
    group24.add_argument("--login", action="store", required=True)

    group25 = subparsers.add_parser("members_unblock", help="Members Unblock:\
 give the login of the member to unblock")
    group25.add_argument("members_unblock", action="store_true")
    group25.add_argument("--login", action="store", required=True)

    group26 = subparsers.add_parser("members_options", help="Members Options:\
 will display your own options : use members_options")
    group26.add_argument("members_options", action="store_true",
    help="Members Options: will display your own options")

    group27 = subparsers.add_parser("members_sync", help="Members Sync:\
 will list your friend from his email you can put several\
 emails seperated by a comma")
    group27.add_argument("members_sync",
                       help="will list your friend from his email\
you can put several emails seperated by a comma", action="store", nargs="+")

    group28 = subparsers.add_parser("comments_show", help="Comments Show:\
display the list of comments of the serie : use comments_show --url <url>")
    group28.add_argument("comments_show", action="store_true")
    group28.add_argument("--url",
                       help="give the url of the serie eg breakingbad not\
                       'Breaking Bad'", action="store")

    group29 = subparsers.add_parser("comments_episode",
    help="Comments Episode: display the list of comments of the serie : \
    use comments_episode  --url <url> --episode <episde> --season <season>")
    group29.add_argument("comments_episode", action="store_true")
    group29.add_argument("--url", required=True,
                       help="give the url of the serie eg breakingbad not\
                       'Breaking Bad'", action="store")
    group29.add_argument("--episode", action="store", required=True,
                     help="give the number of the episode you want to read\
                     comments")
    group29.add_argument("--season", action="store", required=True,
                     help="give the number of the season you want to read\
                     the comments of the given episode")

    group30 = subparsers.add_parser("comments_member", help="Comments Member\
 display the member's comments : use comments_member  --login <login>")
    group30.add_argument("--comments_member", action="store_true")
    group30.add_argument("--login",
                       help="give the name of the member", action="store")

    group31 = subparsers.add_parser("comments_post_show", help="Comments \
    Post Show : add a comment to a show : use comments_post_episode ")
    group31.add_argument("comments_post_show", action="store",
     help="Comments Post Show : add a comment to a show")

    group32 = subparsers.add_parser("comments_post_episode", help="Comments \
Post a comment to an episode, use comments_post_episode")
    group32.add_argument("comments_post_episode", action="store",
    help="Post a comment to an episode")

    group33 = subparsers.add_parser("comments_post_member", help="Comments \
Post a comment to a member : use comments_post_member")
    group33.add_argument("comments_post_member", action="store",
                         help="Post a comment to a member")

    group34 = subparsers.add_parser("comments_subscribe", help="Comments \
Subscribe to a comment : use comments_subscribe")
    group34.add_argument("comments_subscribe", action="store",
                         help="Subscribe to a comment")

    group35 = subparsers.add_parser("comments_unsubscribe", help="Comments \
Unsubscribe to a comment : use comments_unsubscribe")
    group35.add_argument("comments_unsubscribe", action="store",
                         help="Unsubscribe to a comment")

    group36 = subparsers.add_parser("timeline_home", help="Timeline Home\
 display the last events of the website : use --timeline_home --number <num>\
 from 1 to 100 to limit the number of event")
    group36.add_argument("timeline_home", action="store_true",
    help="Timeline Home display the last events of the website")
    group36.add_argument("--number",
                       choices=range(1, 101),
                       help="give the number between 1 to 100", action="store")

    group37 = subparsers.add_parser("timeline_friends", help="Timeline Friends\
 display the last events of your friends : use timeline_friends --number <num>\
 from 1 to 100 to limit the number of event")

    group37.add_argument("--timeline_friends", action="store_true",
        help="Timeline Friends display the last events of your friends")
    group37.add_argument("--number",
                       choices=range(1, 101), type=int,
                       help="give the number between 1 to 100", action="store")

    group38 = subparsers.add_parser("timeline_member", help="Timeline Member \
display the last events of a member : use timeline_member --number <num>\
 from 1 to 100 --login <login> --token")
    group38.add_argument("timeline_member", action="store_true",
        help="Timeline Member display the last events of a member")
    group38.add_argument("--number",
                       choices=range(1, 101), type=int,
                       help="give the number between 1 to 100", action="store")
    group38.add_argument("--login",
                       help="give login of your friend (mandatory)",
                       action="store")
    group38.add_argument("--token",
                    help="to use your token and display your own timeline",
                    action="store_true")

    group39 = subparsers.add_parser("message_inbox", help="Message Inbox\
 display your inbox : message_inbox --page <page> (optional)")
    group39.add_argument("message_inbox", action="store_true",
                         help="Message Inbox display your inbox")
    group39.add_argument("--page",
                      help="give the number of the page (optional)",
                      action="store")

    group40 = subparsers.add_parser("message_discussion",
        help="Message Discussion: display the given discussion : \
        use message_discussion --id <id> --page <page> (optional)")
    group40.add_argument("--message_discussion", action="store_true",
                help="Message Discussion: display the given discussion")
    group40.add_argument("--id", required=True,
                       help="give the id of the discussion to display",
                       action="store")
    group40.add_argument("--page",
                       help="give the number of the page (optional)",
                       action="store")

    group41 = subparsers.add_parser("message_send_new", help="Message Send: \
send a new discussion : use message_send_new --title <title> --text <text>\
--recipient <recipient>")
    group41.add_argument("message_send_new", action="store_true",
                         help="Send a new discussion")
    group41.add_argument("--title", required=True,
                       help="give the title of the discussion",
                       action="store")
    group41.add_argument("--text", required=True,
                       help="give the text of the discussion",
                       action="store")
    group41.add_argument("--recipient", required=True,
                       help="give the name of the member who'll received it",
                       action="store")

    group42 = subparsers.add_parser("message_send_response",
        help="Message Send : send a response : use message_send_response\
         --id <id> --text <text>")
    group42.add_argument("message_send_response", action="store_true",
                help="Message Send : send a response to a given id message ")
    group42.add_argument("--id", required=True,
                       help="give the id of the discusion you're responding",
                       action="store")
    group42.add_argument("--text", required=True,
                       help="give the text of the response",
                       action="store")

    group43 = subparsers.add_parser("message_delete", help="Message Delete\
 delete a message : use message_delete --id <id>")
    group43.add_argument("message_delete", action="store_true")
    group43.add_argument("--id", required=True,
                       help="give the id of the discusion to delete",
                       action="store")

    args = parser.parse_args()

    if len(sys.argv) > 1:
        do_action(args)
    else:
        parser.error("enter -help to see the options you can use")


if __name__ == '__main__':
    main()
