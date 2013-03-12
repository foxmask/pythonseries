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
    if options.shows_search:
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
    elif options.shows_display:
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
        # all the data
        # print data
    elif options.shows_episodes:
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
#    elif options.add:
#        """
#        shows_add wrapper
#        """
#        print "you want to add a file to your account"
#        data = c.shows_add(get_token())
#    elif options.remove:
#        """
#        shows_remove wrapper
#        """
#        print "you want to remove a file to your account"
#        data = c.shows_remove(get_token())
#    elif options.recommend:
#        """
#        shows_recommend wrapper
#        """
#        print "you want to recommend a file to a friend"
#        data = c.shows_recommend(get_token())
#        print data
#    elif options.archive:
#        """
#        shows_archive wrapper
#        """
#        print "you want to archive a serie"
#        data = c.shows_archive(get_token())
#        print data
#    elif options.scrapper:
#        """
#        shows_scrapper wrapper
#        """
#        data = c.shows_scrapper()
#        print data
#    elif options.unarchive:
#        """
#        shows_unarchive wrapper
#        """
#        print "you want to get out the serie from your archives"
#        data = c.shows_unarchive(get_token())
#        print data
    elif options.shows_characters:
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

    elif options.shows_similar:
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
    elif options.shows_videos:
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

    elif options.subtitles_last:
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

    elif options.subtitles_show:
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
    elif options.subtitles_show_by_file:
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

    elif options.planning_general:
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

    elif options.planning_member:
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

    elif options.member_is_active:
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

    elif options.member_infos:
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

    elif options.members_episodes:
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

    elif options.members_note:
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

    elif options.members_downloaded:
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

    elif options.members_notifications:
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

    elif options.members_option:
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

    elif options.members_signup:
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

    elif options.members_friends:
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

    elif options.members_badges:
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

    elif options.members_add:
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

    elif options.members_delete:
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

    elif options.members_search:
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

    elif options.members_block:
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

    elif options.members_unblock:
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

    elif options.members_options:
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

    elif options.members_sync:
        print "API implemented but no example ready yet"

    elif options.comments_show:
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
    elif options.comments_episode:
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
    elif options.comments_member:
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
    elif options.comments_post_show:
        print "API implemented but no example ready yet"
    elif options.comments_post_episode:
        print "API implemented but no example ready yet"
    elif options.comments_post_member:
        print "API implemented but no example ready yet"
    elif options.comments_subscribe:
        print "API implemented but no example ready yet"
    elif options.comments_unsubscribe:
        print "API implemented but no example ready yet"
    elif options.timeline_home:
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
    elif options.timeline_friends:
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
    elif options.timeline_member:
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
    elif options.message_inbox:
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

    elif options.message_discussion:
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
    elif options.message_send_new:
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

    elif options.message_send_response:
        if options.text and options.id:
            params = {'token': get_token(),
                      'text': options.text,
                      'discussion_id': options.id}
            data = c.message_send_response(**params)
            print data
        else:
            print "All parameters are mandatory"
    elif options.message_delete:
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
    parser = argparse.ArgumentParser(description='Process some integers.',
                                     conflict_handler='resolve',
                                     add_help=True)

    group0 = parser.add_argument_group("*** Search series",
                "use --shows_search --title <title>")
    group0.add_argument("--shows_search", action="store_true")
    group0.add_argument("--title", action="store",
                        help="make a search by title")

    # group the options for handling Display of series parameters
    group1 = parser.add_argument_group("*** Details of series",
                "use --shows_display --url <url>")
    group1.add_argument("--shows_display", action="store_true")
    group1.add_argument("--url", action="store", nargs="+",
                     help="the url/name of the given serie")

    # group the options for handling Episodes parameters
    group2 = parser.add_argument_group("*** Episodes",
"use --shows_episodes --url <serie> (--season <num>) (--episode <num>)\
(--summary) to filter episodes you want to search")
    group2.add_argument("--shows_episodes", action="store_true")
    group2.add_argument("--url", action="store", nargs="+",
                     help="the url of the given serie")
    group2.add_argument("--episode", action="store", nargs="+",
                     help="the number of the episode (optional)")
    group2.add_argument("--season", action="store", nargs="+",
                     help="the number of the season (optional)")
    group2.add_argument("--summary", action="store_true",
                     help="boolean set to false by default, \
                     to only get the summary of the episode (optional)")

    group3 = parser.add_argument_group("*** Characters",
"use --shows_characters --url <serie> (--summary)\
(--char_id <num>) to find characters for the series you want to search")
    group3.add_argument('--shows_characters', action="store_true")
    group3.add_argument("--url", action="store",
                     help="give the name of the serie to get\
 the list of characters of this one")
    group3.add_argument("--summary", action="store_true",
                     help="boolean set to true by default,\
 only get the summary of the characters (optional)")
    group3.add_argument("--char_id", action="store",
                     help="display info of THIS character (optional)")

    group13 = parser.add_argument_group("*** Similar Shows",
"use --shows_similar --url <serie> to find similar serie")
    group13.add_argument('--shows_similar', action="store_true")
    group13.add_argument("--url", action="store",
                     help="give the name of the serie to get similar ones")

    group4 = parser.add_argument_group("*** Videos",
                        "use --shows_videos --url <serie> (--season <num>)\
(--episode <num> to filter episodes you want to search)")
    group4.add_argument("--shows_videos", action="store_true")
    group4.add_argument("--url", action="store",
                     help="give the name of the video you want to search")
    group4.add_argument("--season", action="store",
                     help="display the list of video of the given season\
(optional)")
    group4.add_argument("--episode", action="store",
                     help="display the list of video of the given episode\
(optional)")

    group5 = parser.add_argument_group("*** Subtitles",
"use --subtitles_show --url <serie> --language <lang> --season <num>\
 --episode <num> to find subtitles you want to search")
    group5.add_argument("--subtitles_show", action="store_true")
    group5.add_argument("--url", action="store",
                    help="give the name of the serie you want to see subtitle")
    group5.add_argument("--language", action="store",
                     help="display the sub for the given language: vo or vf",
                     choices=('vo', 'vf'))
    group5.add_argument("--season", action="store",
                     help="display the subtitles of the given season")
    group5.add_argument("--episode", action="store",
                     help="display the subtitles of the given episode")

    group6 = parser.add_argument_group("*** Last Subtitles",
                        "use --subtitles_last --language <lang> --number <num>\
 to search subtitle you want to search")
    group6.add_argument("--subtitles_last", action="store_true")
    group6.add_argument("--language", action="store",
                     help="display the last sub \
for a given language: vo or vf")
    group6.add_argument("--number", action="store",
                     help="display the 'n' last subtitles")

    group7 = parser.add_argument_group("*** Subtitle by Filename",
"use --subtitles_show_by_file --my_file <file> --language <lang>\
to search subtitle you want to search")
    group7.add_argument('--subtitles_show_by_file', action="store_true")
    group7.add_argument("--my_file", action="store",
                      help="display the subtitles from a given filename")
    group7.add_argument("--language", action="store",
                     help="filter subtitle for a given language: vo or vf",
                     choices=('vo', 'vf'))

    group8 = parser.add_argument_group("*** Planning General")
    group8.add_argument("--planning_general", action="store_true",
                      help="display the general planning")

    group9 = parser.add_argument_group("*** Planning Member")
    group9.add_argument("--planning_member", action="store_true",
                      help="display the planning of the member")

    group10 = parser.add_argument_group("*** Member : is he active ?")
    group10.add_argument("--member_is_active", action="store_true",
                      help="check if the member is active")

    group11 = parser.add_argument_group("*** Member : infos ?")
    group11.add_argument("--member_infos", action="store_true")
    group11.add_argument("--login", action="store",
                      help="get info from the login of the member")
    group11.add_argument("--token", action="store_true",
                      help="to use the token or not, to get his/our info")
    group11.add_argument("--nodata", action="store_true",
                      help="will ONLY display login and date")
    group11.add_argument("--since", action="store",
                      help="give a timestamp date to get info from it")

    group12 = parser.add_argument_group("*** Member : Episodes ?")
    group12.add_argument('--members_episodes', action="store_true")
    group12.add_argument("--subtitles", action="store",
                      help="filter serie with subtitles : all / vovf / vf",
                     choices=('all', 'vovf', 'vf'))
    group12.add_argument("--show", action="store",
                      help="give the name of the serie to ONLY get its \
                      episodes")
    group12.add_argument("--view", action="store",
                      help="set a number of next episode to view or just \
'next' to get the next one")

    group14 = parser.add_argument_group("*** Member : Note ",
"use --note <note> --url <url> --episode <num> --season <num>.\
To give a note to the complet serie put --season 0 and --episode 0")
    group14.add_argument('--members_note', action="store_true")
    group14.add_argument("--url", action="store",
                      help="url of the serie to evluate. eg breakingbad not\
                      'Breaking Bad'")
    group14.add_argument("--episode", action="store",
                      help="number of the episode of the serie to evaluate")
    group14.add_argument("--season", action="store",
                      help="number of the season of the serie to evaluate")
    group14.add_argument("--note", action="store",
                      help="give a note between 1 and 5", choices=range(1, 6),
                      type=int)

    group15 = parser.add_argument_group("*** Member : Downloaded",
        "use --members_downloaded --url <url> --episode <num> --season <num>.")
    group15.add_argument('--members_downloaded', action="store_true")
    group15.add_argument("--url", action="store",
                      help="the url of the serie to mark as downloaded\
eg breakingbad not 'Breaking Bad'")
    group15.add_argument("--episode", action="store",
                      help="the number of the episode to mark as downloaded")
    group15.add_argument("--season", action="store",
                      help="the season of the episode to mark as downloaded")

    group16 = parser.add_argument_group("*** Member : Notifications ", \
                           "use --members_notifications \
--summary=True/False (optional: default False)\
--number <num> (optional)\
--last_id <num> (optional)\
--sort ASC|DESC (optional)\
dont mix --last_id and --sort\
or all notifications could not be get")

    group16.add_argument("--members_notifications", action="store_true",
                      help="the see the notifications")
    group16.add_argument("--summary", action="store_true",
                      help="to get only the number of unread notification")
    group16.add_argument("--number", action="store",
                      help="to get the notification from this number")
    group16.add_argument("--last_id", action="store",
                      help="to get the last 'n' notifications")
    group16.add_argument("--sort", action="store",
                      help="to sort the display, use asc or desc")

    group17 = parser.add_argument_group("*** Members : Option ", \
"use --members_option --options <downloaded|notation|decalage>\
 --value <read|edit> (mandatory)")
    group17.add_argument("--members_option", action="store_true")
    group17.add_argument("--option", action="store",
                      help="can be one of <downloaded|notation|decalage>",
                      choices=('downloaded', 'notation', 'decalage'))
    group17.add_argument("--value", action="store",
                      help="read : to read options and\
                      edit to modify the option",
                      choices=('edit', 'read'))

    group18 = parser.add_argument_group("*** Members : Signup ", \
                          "use --members_signup --login <login>\
 --password <password> --mail <email>")

    group18.add_argument("--members_signup", action="store_true")
    group18.add_argument("--login", action="store",
                      help="the login: max 24 chars")
    group18.add_argument("--password", action="store")
    group18.add_argument("--mail", action="store")

    group19 = parser.add_argument_group("*** Members : Friends ", \
                          "use --members_friends\
 --token to get the friends of your account (optional) OR\
 --login <login> to get the friends of this member (optional)")

    group19.add_argument("--members_friends", action="store_true")
    group19.add_argument("--token", action="store_true")
    group19.add_argument("--login", action="store")

    group20 = parser.add_argument_group("*** Members : Badges", \
                          "use --members_badges\
 --token to get the friends of your account (optional) OR\
 --login <login> to get the friends of this member (optional)")

    group20.add_argument("--members_badges", action="store_true")
    group20.add_argument("--token", action="store_true")
    group20.add_argument("--login", action="store")

    group21 = parser.add_argument_group("*** Members : Add",
                    "give the login of the friend to add")
    group21.add_argument("--members_add", action="store_true")
    group21.add_argument("--login", action="store")

    group22 = parser.add_argument_group("*** Members : Delete",
                    "give the login of the friend to delete")
    group22.add_argument("--members_delete",
                       action="store_true")
    group22.add_argument("--login", action="store")

    group23 = parser.add_argument_group("*** Members : Search",
                        "get a list of 10 friends starting by this string")
    group23.add_argument("--members_search", action="store_true")
    group23.add_argument("--login", action="store")

    group24 = parser.add_argument_group("*** Members : Block",
                    "give the login of the member to block")
    group24.add_argument("--members_block", action="store_true")
    group24.add_argument("--login", action="store")

    group25 = parser.add_argument_group("*** Members : Unblock",
                                "give the login of the member to unblock")
    group25.add_argument("--members_unblock", action="store_true")
    group25.add_argument("--login", action="store")

    group26 = parser.add_argument_group("*** Members : Options",
                                        "will display your options")
    group26.add_argument("--members_options", action="store_true")
    group26.add_argument("--login", action="store")

    group27 = parser.add_argument_group("*** Members : Sync")
    group27.add_argument("--members_sync",
                       help="will list your friend from his email\
you can put several emails seperated by a comma", action="store")

    group28 = parser.add_argument_group("*** Comments : Show",
                          "display the list of comments of the serie")

    group28.add_argument("--comments_show", action="store_true")
    group28.add_argument("--url",
                       help="give the url of the serie eg breakingbad not\
                       'Breaking Bad'", action="store")

    group29 = parser.add_argument_group("*** Comments : Episode",
                          "display the list of comments of the serie")

    group29.add_argument("--comments_episode", action="store_true")
    group29.add_argument("--url",
                       help="give the url of the serie eg breakingbad not\
                       'Breaking Bad'", action="store")

    group29.add_argument("--episode", action="store",
                     help="give the number of the episode you want to read\
                     comments")

    group29.add_argument("--season", action="store",
                     help="give the number of the season you want to read\
                     the comments of the given episode")

    group30 = parser.add_argument_group("*** Comments : Member", \
                          "display the member's comments")

    group30.add_argument("--comments_member", action="store_true")
    group30.add_argument("--login",
                       help="give the name of the member", action="store")

    group31 = parser.add_argument_group("*** Comments : \
Post a comment to a show")
    group31.add_argument("--comments_post_show", action="store")

    group32 = parser.add_argument_group("*** Comments : Post a comment\
to an episode")
    group32.add_argument("--comments_post_episode", action="store")

    group33 = parser.add_argument_group("*** Comments : Post a comment\
to a member")
    group33.add_argument("--comments_post_member", action="store")

    group34 = parser.add_argument_group("*** Comments : \
    Subscribe to a comment")
    group34.add_argument("--comments_subscribe", action="store")

    group35 = parser.add_argument_group("*** Comments : \
    Unsubscribe to a comment")
    group35.add_argument("--comments_unsubscribe", action="store")

    group36 = parser.add_argument_group("*** Timeline : Home", \
                          "display the last events of the website")

    group36.add_argument("--timeline_home", action="store_true")
    group36.add_argument("--number",
                       choices=range(1, 101),
                       help="give the number between 1 to 100", action="store")

    group37 = parser.add_argument_group("*** Timeline : Friends", \
                          "display the last events of your friends")

    group37.add_argument("--timeline_friends", action="store_true")
    group37.add_argument("--number",
                       choices=range(1, 101), type=int,
                       help="give the number between 1 to 100", action="store")

    group38 = parser.add_argument_group("*** Timeline : Member", \
                          "display the last events of a member")
    group38.add_argument("--timeline_member", action="store_true")
    group38.add_argument("--number",
                       choices=range(1, 101), type=int,
                       help="give the number between 1 to 100", action="store")
    group38.add_argument("--login",
                       help="give login of your friend (mandatory)",
                       action="store")
    group38.add_argument("--token",
                       help="to use your token", action="store_true")

    group39 = parser.add_argument_group("*** Message : Inbox",
                                        "display your inbox")
    group39.add_argument("--message_inbox", action="store_true")
    group39.add_argument("--page",
                      help="give the number of the page (optional)",
                      action="store")

    group40 = parser.add_argument_group("*** Message : Discussion", \
"display the given discussion")
    group40.add_argument("--message_discussion", action="store_true")
    group40.add_argument("--id",
                       help="give the id of the discussion to display",
                       action="store")
    group40.add_argument("--page",
                       help="give the number of the page (optional)",
                       action="store")

    group41 = parser.add_argument_group("*** Message: Send a new discussion", \
"send a new discussion")
    group41.add_argument("--message_send_new", action="store_true")
    group41.add_argument("--title",
                       help="give the title of the discussion",
                       action="store")
    group41.add_argument("--text",
                       help="give the text of the discussion",
                       action="store")
    group41.add_argument("--recipient",
                       help="give the name of the member who'll received it",
                       action="store")

    group42 = parser.add_argument_group("*** Message: Send a response",
"send a response")
    group42.add_argument("--message_send_response", action="store_true")
    group42.add_argument("--id",
                       help="give the id of the discusion you're responding",
                       action="store")
    group42.add_argument("--text",
                       help="give the text of the response",
                       action="store")

    group43 = parser.add_argument_group("*** Message : Delete",
"delete a message")
    group43.add_argument("--message_delete", action="store_true")
    group43.add_argument("--id",
                       help="give the id of the discusion to delete",
                       action="store")

    args = parser.parse_args()
    print args
    if len(sys.argv) > 1:
        do_action(args)
    else:
        parser.error("enter -help to see the options you can use")


if __name__ == '__main__':
    main()
