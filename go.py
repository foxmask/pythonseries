# -*- coding: utf-8 -*-
from optparse import OptionParser, OptionGroup

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
    if options.title:
        """
        show_search wrapper
        """
        print "you want to search the title of a movie " + options.title
        data = c.shows_search(options.title)
    elif options.display:
        """
        show_display wrapper
        """
        print "you want to display the content of a serie " + options.display
        data = c.shows_display(options.display)
        print "Genre:"
        for genre in data['show']['genres'].values():
            print "-" + genre
        print "Description: %s" % data['show']['description']
        print "seasons:"
        for season in data['root']['show']['seasons']:
            print season, ' sur ', data['show']['seasons'][season]['episodes']
        # all the data
        # print data
    elif options.name:

        """
        shows_episodes wrapper
        """
        print "you want to search serie %s " % options.name
        params = {}
        if options.name:
            params['url'] = options.name

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
                    number = data['seasons'][season]['episodes'][ep]['number']
                    title = data['seasons'][season]['episodes'][ep]['title']
                    print "Number: {number} Title: {title} ".\
                    format(number=number, title=title)
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
    elif options.chars:
        """
        shows_characters wrapper
        """
        print "you want to search characters of the serie {characters}"\
                .format(characters=options.chars)
        params = {}
        params['url'] = options.chars

        if options.char_summary:
            params['summary'] = options.char_summary

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

    elif options.similar:
        print "you want to find similar series to " + options.similar
        data = c.shows_similar(options.similar)
        print "{title:^40} {url:^20}".format(title='title', url='url')
        for show in data['shows']:
            title = data['shows'][show]['title']
            url = data['shows'][show]['url']
            print u"{title:<30} {url:<20}".format(title=title, url=url)

    elif options.videos:
        print "you want to search videos of serie " + options.videos
        params = {}
        params['url'] = options.videos

        if options.sv:
            params['season'] = options.sv

        if options.ev:
            params['episode'] = options.ev

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

    elif options.last_sub:
        """
        subtitles_last wrapper
        """
        print "you want to see the last subtitles"
        params = {}

        if options.last_sub_lang:
            params['language'] = options.last_sub_lang

        if options.last_sub_nb:
            params['number'] = options.last_sub_nb

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

    elif options.sub:
        """
        subtitles_show wrapper
        """
        print "you want to search subtitles of serie " + options.sub
        params = {}
        params['url'] = options.sub

        if options.sub_lang:
            params['language'] = options.sub_lang
        if options.sub_sv:
            params['season'] = options.sub_sv
        if options.sub_ev:
            params['episode'] = options.sub_ev

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
                print "{season:<10} {ep:<5}  {lang:<5} {file:<50} {url:<50}".\
                      format(season=season,
                             ep=ep,
                             lang=language,
                             file=my_file,
                             url=url)

    elif options.sub_by_file:
        """
        subtitles_show_by_file wrapper
        """
        print "you want to get the subtitle from a given filename" + \
                options.sub_by_file
        # todo fix the name of the options
        data = c.subtitles_show_by_file(options.sub_by_file, options.sub_lang)
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

    elif options.is_active:
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
        print "you want to display the info of " + options.member_infos
        params = {}
        if options.member_infos:
            params['login'] = options.member_infos
        if options.member_token:
            params['token'] = options.member_token
        if options.member_nodata:
            params['nodata'] = options.member_token
        if options.member_since:
            params['since'] = options.member_since
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
                print "TimeOnTV: " + stats['time_on_tv']
                print "TimeToSpend: " + stats['time_to_spend']
                for show in data['member']['shows']:
                    print "url " + data['member']['shows'][show]['url'], \
                          "title " + data['member']['shows'][show]['title']

    elif options.member_ep:
        print "you want to display the 'next' Episodes"
        params = {}
        params['token'] = get_token()
        if options.member_ep_sub:
            params['subtitles'] = options.member_ep_sub
        if options.member_ep_show:
            params['show'] = options.member_ep_show
        if options.member_ep_view:
            params['view'] = options.member_ep_view

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

    elif options.note_serie:
        if options.note and options.note_episode and options.note_season:
            print "You want to give a note %s to \
the episode %s (season %s) of the serie %s" % (options.note,
                                               options.note_episode,
                                               options.note_season,
                                               options.note_serie)
            params = {
                  'token': get_token(),
                  'url': options.note_serie,
                  'episode': options.note_episode,
                  'season': options.note_season,
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

    elif options.members_dl_serie:
        if options.members_dl_serie and options.members_dl_ep and\
        options.members_dl_season:
            print "You want to set the episode %s (season %s) of the serie\
 %s as downloaded" % (options.members_dl_ep, options.members_dl_season, \
                      options.members_dl_serie)
            params = {
                  'token': get_token(),
                  'url': options.members_dl_serie,
                  'episode': options.members_dl_ep,
                  'season': options.members_dl_season,
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

    elif options.members_notif:
        print "you want to display the notifications "
        params = {'token': get_token()}
        if options.members_notif_summary:
            params['summary'] = options.members_notif_summary
        if options.members_notif_number:
            params['number'] = options.members_notif_number
        if options.members_notif_last_id:
            params['last_id'] = options.members_notif_last_id
        if options.members_notif_sort:
            params['sort'] = options.members_notif_sort

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
        if options.members_option and options.members_option_value:
            msg = "You want "
            if options.members_option_value == 'read':
                value = 0
                msg += "to read"
            else:
                value = 1
                msg += "to modify"
            msg += " option to %s" % options.members_option
            params = {
                  'token': get_token(),
                  'value': value,
                  'option': options.members_option
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
        if options.members_signup_pass and options.members_signup_mail:
            params = {'login': options.members_signup,
                      'password': options.members_signup_pass,
                      'mail': options.members_signup_mail}
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
        if options.members_friends_token:
            params['token'] = get_token()
        if options.members_friends_login:
            params['login'] = options.members_friends_login
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
                    print data['friends'][friend]['login']

    elif options.members_badges:
        params = {}
        if options.members_badges_token:
            params['token'] = get_token()
        if options.members_badges_login:
            params['login'] = options.members_badges_login
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
        params['login'] = options.members_add
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
        params['login'] = options.members_delete
        data = c.members_delete(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print "member %s deleted" % options.members_delete

    elif options.members_search:
        params = {}
        params['login'] = options.members_search
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
        params['login'] = options.members_block
        data = c.members_block(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print "member %s deleted" % options.members_block

    elif options.members_unblock:
        params = {}
        params['token'] = get_token()
        params['login'] = options.members_unblock
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
        pass

    elif options.comments_show:
        params = {'url': options.comments_show}
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

    elif options.comments_episode:
        if options.comments_episode_season and options.comments_episode_num:
            params = {'url': options.comments_episode,
                      'episode': options.comments_episode_num,
                      'season': options.comments_episode_season}
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
        data = c.comments_member(options.comments_member)
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
        pass
    elif options.comments_post_episode:
        pass
    elif options.comments_post_member:
        pass
    elif options.comments_subscribe:
        pass
    elif options.comments_unsubscribe:
        pass
    elif options.timeline_home:
        data = c.timeline_home(options.timeline_home)
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
        data = c.timeline_friends(get_token(), options.timeline_friends)
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
        params = {'number': options.timeline_member}
        if options.timeline_member_login:
            params['member'] = options.timeline_member_login
        if options.timeline_member_token:
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

    elif options.message_inbox:
        params = {'token': get_token()}
        if options.message_inbox_page:
            params['page'] = options.message_inbox_page
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
        params = {'token': get_token(),
                  'my_id': options.message_discussion}
        if options.message_discussion_page:
            params['page'] = options.message_discussion_page
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

    elif options.message_send_new:
        params = {'token': get_token(),
                  'title': options.message_send_new,
                  'text': options.message_send_new_text,
                  'recipient': options.message_send_new_recipient}
        data = c.message_send_new(**params)
        if len(data['errors']) > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            print data

    elif options.message_send_response:
        params = {'token': get_token(),
                  'text': options.message_send_response_text,
                  'discussion_id': options.message_send_response}
        data = c.message_send_response(**params)
        print data

    elif options.message_delete:
        params = {'token': get_token(), 'my_id': options.message_delete}
        data = c.message_delete(**params)
        print data


def main():
    parser = OptionParser()

    group0 = OptionGroup(parser, "*** Search series")
    group0.add_option("--title", dest="title", type="string",
                      help="make a search by title")
    parser.add_option_group(group0)

    # group the options for handling Display of series parameters
    group1 = OptionGroup(parser, "*** Details of series")
    group1.add_option("--display", dest="display", action="store",
                     help="the name of the given serie")
    parser.add_option_group(group1)

    # group the options for handling Episodes parameters
    group2 = OptionGroup(parser, "*** Episodes",
                        "use --name <serie> (--season <num>) (--episode <num>)\
 (--summary) to filter episodes you want to search")
    group2.add_option("--name", dest="name", action="store",
                     help="the name of the given serie")

    group2.add_option("--episode", dest="episode", action="store",
                     help="the number of the episode (optional)")

    group2.add_option("--season", dest="season", action="store",
                     help="the number of the season (optional)")

    group2.add_option("--summary", dest="summary", action="store_true",
                     help="boolean set to false by default, \
                     to only get the summary of the episode (optional)")

    parser.add_option_group(group2)

    group3 = OptionGroup(parser, "*** Characters",
                        "use --chars <serie> (--char_summary <num>)\
 (--char_id <num>) to find characters for the series you want to search")
                # print "option value %s set to %s" % (data['option']['name'],
                #                                      data['option']['value'])

    group3.add_option("--chars", action="store",
                     help="give the name of the serie to get\
 the list of characters of this one")

    group3.add_option("--char_summary", action="store_true",
                     help="boolean set to true by default,\
 only get the summary of the characters (optional)")

    group3.add_option("--char_id", action="store",
                     help="display info of THIS character (optional)")

    parser.add_option_group(group3)

    group13 = OptionGroup(parser, "*** Similar Shows",
                        "use --similar <serie> to find similar serie")

    group13.add_option("--similar", action="store",
                     help="give the name of the serie to get similar ones")

    parser.add_option_group(group13)

    group4 = OptionGroup(parser, "*** Videos",
                        "use --videos <serie> (--sv <num>) (--ev <num>) \
to filter episodes you want to search")

    group4.add_option("--videos", action="store",
                     help="give the name of the video you want to search")
    group4.add_option("--sv", action="store",
                     help="display the list of video of the given season\
(optional)")

    group4.add_option("--ev", action="store",
                     help="display the list of video of the given episode\
(optional)")
    parser.add_option_group(group4)

    group5 = OptionGroup(parser, "*** Subtitles",
                        "use --sub <serie> --lang <lang> --sub_sv <num>\
 --sub_ev <num> to find subtitles you want to search")

    group5.add_option("--sub", dest="sub", action="store",
                     help="give the name of the serie \
                     you want to see subtitle")

    group5.add_option("--sub_lang", dest="sub_lang", action="store",
                     help="display the sub for the given language: vo or vf")

    group5.add_option("--sub_sv", dest="sub_sv", action="store",
                     help="display the subtitles of the given season")

    group5.add_option("--sub_ev", dest="sub_ev", action="store",
                     help="display the subtitles of the given episode")

    parser.add_option_group(group5)

    group6 = OptionGroup(parser, "*** Last Subtitles",
                        "use --last_sub --last_lang <lang> --last_nb <num>\
 to search subtitle you want to search")

    group6.add_option("--last_sub", dest="last_sub", action="store_true",
                     help="boolean set to true by defauoptionslt")

    group6.add_option("--last_sub_lang", dest="last_sub_lang", action="store",
                     help="display the last sub \
for a given language: vo or vf")

    group6.add_option("--last_sub_nb", dest="last_sub_nb", action="store",
                     help="display the 'n' last subtitles")

    parser.add_option_group(group6)

    group7 = OptionGroup(parser, "*** Subtitle by Filename")
    group7.add_option("--sub_by_file", action="store",
                      help="display the subtitles from a given filename")

    group7.add_option("--sub_by_file_lang", action="store",
                     help="filter subtitle for a given language: vo or vf")

    parser.add_option_group(group7)

    group8 = OptionGroup(parser, "*** Planning General")
    group8.add_option("--planning_general", action="store_true",
                      help="display the general planning")
    parser.add_option_group(group8)

    group9 = OptionGroup(parser, "*** Planning Member")
    group9.add_option("--planning_member", action="store_true",
                      help="display the planning of the member")
    parser.add_option_group(group9)

    group10 = OptionGroup(parser, "*** Member : is he active ?")
    group10.add_option("--is_active", action="store_true",
                      help="check if the member is active")
    parser.add_option_group(group10)

    group11 = OptionGroup(parser, "*** Member : infos ?")
    group11.add_option("--member_infos", action="store",
                      help="get info from the login of the member")

    group11.add_option("--member_token", action="store",
                      help="member token to get his/our info")

    group11.add_option("--member_nodata", action="store_true",
                      help="will ONLY display login and date")

    group11.add_option("--member_since", action="store",
                      help="give a timestamp date to get info from it")

    parser.add_option_group(group11)

    group12 = OptionGroup(parser, "*** Member : Episodes ?")
    group12.add_option("--member_ep", action="store_true",
                      help="get info from the login of the member")

    group12.add_option("--member_ep_sub", action="store",
                      help="filter serie with subtitles : all / vovf / vf")

    group12.add_option("--member_ep_show", action="store",
                      help="give the name of the serie to ONLY get its \
                      episodes")

    group12.add_option("--member_ep_view", action="store",
                      help="set a number of next episode to view or just \
'next' to get the next one")

    parser.add_option_group(group12)

    group14 = OptionGroup(parser, "*** Member : Note ",
"use --note <note> --note_serie <url> --note_episode <num>\
 --note_episode <num>.\
To give a note to the complet serie put --note_season 0 and --note_episode 0")

    group14.add_option("--note", action="store",
                      help="give a note between 1 and 5", type="int")

    group14.add_option("--note_serie", action="store",
                      help="url of the serie to evluate. eg breakingbad not\
                      'Breaking Bad'")

    group14.add_option("--note_episode", action="store",
                      help="number of the episode of the serie to evluate")

    group14.add_option("--note_season", action="store",
                      help="number of the season of the serie to evluate")
    parser.add_option_group(group14)

    group15 = OptionGroup(parser, "*** Member : Downloaded ",
        "use --members_dl_serie <url> --members_dl_ep <num> \
 --members_dl_season <num>.")

    group15.add_option("--members_dl_serie", action="store",
                      help="the url of the serie to mark as downloaded\
eg breakingbad not 'Breaking Bad'")

    group15.add_option("--members_dl_ep", action="store",
                      help="the number of the episode to mark as downloaded")

    group15.add_option("--members_dl_season", action="store",
                      help="the season of the episode to mark as downloaded")

    parser.add_option_group(group15)

    group16 = OptionGroup(parser, "*** Member : Notifications ", \
                           "use --members_notif \
--members_notif_summary=True/False (optional: default False)\
--members_notif_number <num> (optional)\
--members_notif_last_id <num> (optional)\
dont mix --members_notif_last_id and --members_notif_sort\
all notifications could not be get")

    group16.add_option("--members_notif", action="store_true",
                      help="the see the notifications")

    group16.add_option("--members_notif_summary", action="store_true",
                      help="to get only the number of unread notification")

    group16.add_option("--members_notif_number", action="store",
                      help="to get the notification from this number")

    group16.add_option("--members_notif_last_id", action="store",
                      help="to get the last 'n' notifications")

    group16.add_option("--members_notif_sort", action="store",
                      help="to sort the display, use asc or desc")

    parser.add_option_group(group16)

    group17 = OptionGroup(parser, "*** Members : Option ", \
                          "use --members_option <downloaded|notation|decalage>\
 --members_option_value <read|edit> (mandatory)")

    group17.add_option("--members_option", action="store",
                      help="must be one of them downloaded,notation, decalage")

    group17.add_option("--members_option_value", action="store",
                      help="read : to read options and\
                      edit to modify the option")

    parser.add_option_group(group17)

    group18 = OptionGroup(parser, "*** Members : Signup ", \
                          "use --members_signup <login>\
 --members_signup_pass <password> --members_signup_mail <email>")

    group18.add_option("--members_signup", action="store",
                      help="the login: max 24 chars")

    group18.add_option("--members_signup_pass", action="store")
    group18.add_option("--members_signup_mail", action="store")

    parser.add_option_group(group18)

    group19 = OptionGroup(parser, "*** Members : Friends ", \
                          "use --members_friends\
 --members_friends_token to get the friends of your account (optional)\
 --members_friends_login <login> to get the friends of this member (optional)")

    group19.add_option("--members_friends", action="store_true")

    group19.add_option("--members_friends_token", action="store_true")
    group19.add_option("--members_friends_login", action="store")

    group20 = OptionGroup(parser, "*** Members : Badges", \
                          "use --members_badges\
 --members_badges_token to get the friends of your account (optional)\
 --members_badges_login <login> to get the friends of this member (optional)")

    group20.add_option("--members_badges", action="store_true")

    group20.add_option("--members_badges_token", action="store_true")
    group20.add_option("--members_badges_login", action="store")

    parser.add_option_group(group20)

    group21 = OptionGroup(parser, "*** Members : Add")

    group21.add_option("--members_add",
                       help="give the login of the friend to add",
                       action="store")

    parser.add_option_group(group21)

    group22 = OptionGroup(parser, "*** Members : Delete")

    group22.add_option("--members_delete",
                       help="give the login of the friend to delete",
                       action="store")

    parser.add_option_group(group22)

    group23 = OptionGroup(parser, "*** Members : Search")

    group23.add_option("--members_search",
                       help="get a list of 10 friends starting by this string",
                       action="store")

    parser.add_option_group(group23)

    group24 = OptionGroup(parser, "*** Members : Block")

    group24.add_option("--members_block",
                       help="give the login of the member to block",
                       action="store")

    parser.add_option_group(group24)

    group25 = OptionGroup(parser, "*** Members : Unblock")

    group25.add_option("--members_unblock",
                       help="give the login of the member to unblock",
                       action="store")

    parser.add_option_group(group25)

    group26 = OptionGroup(parser, "*** Members : Options")

    group26.add_option("--members_options",
                       help="will display your options",
                       action="store_true")

    parser.add_option_group(group26)

    group27 = OptionGroup(parser, "*** Members : Options")

    group27.add_option("--members_sync",
                       help="will list your friend from his email\
you can put several emails seperated by a comma", action="store")

    parser.add_option_group(group27)

    group28 = OptionGroup(parser, "*** Comments : Show",
                          "display the list of comments of the serie")

    group28.add_option("--comments_show",
                       help="give the url of the serie eg breakingbad not\
                       'Breaking Bad'", action="store")

    parser.add_option_group(group28)

    group29 = OptionGroup(parser, "*** Comments : Episode",
                          "display the list of comments of the serie")

    group29.add_option("--comments_episode",
                       help="give the url of the serie eg breakingbad not\
                       'Breaking Bad'", action="store")

    group29.add_option("--comments_episode_num", action="store",
                     help="give the number of the episode you want to read\
                     comments")

    group29.add_option("--comments_episode_season", action="store",
                     help="give the number of the season you want to read\
                     the comments of the given episode")

    parser.add_option_group(group29)

    group30 = OptionGroup(parser, "*** Comments : Member", \
                          "display the member's comments")

    group30.add_option("--comments_member",
                       help="give the name of the member", action="store")

    parser.add_option_group(group30)

    group31 = OptionGroup(parser, "*** Comments : Post a comment to a show")
    group31.add_option("--comments_post_show", action="store")
    parser.add_option_group(group31)

    group32 = OptionGroup(parser, "*** Comments : Post a comment\
to an episode")
    group32.add_option("--comments_post_episode", action="store")
    parser.add_option_group(group32)

    group33 = OptionGroup(parser, "*** Comments : Post a comment\
to a member")
    group33.add_option("--comments_post_member", action="store")
    parser.add_option_group(group33)

    group34 = OptionGroup(parser, "*** Comments : Subscribe to a comment")
    group34.add_option("--comments_subscribe", action="store")
    parser.add_option_group(group34)

    group35 = OptionGroup(parser, "*** Comments : Unsubscribe to a comment")
    group35.add_option("--comments_unsubscribe", action="store")
    parser.add_option_group(group35)

    group36 = OptionGroup(parser, "*** Timeline : Home", \
                          "display the last events of the website")

    group36.add_option("--timeline_home",
                       help="give the number between 1 to 100", action="store")

    parser.add_option_group(group36)

    group37 = OptionGroup(parser, "*** Timeline : Friends", \
                          "display the last events of your friends")

    group37.add_option("--timeline_friends",
                       help="give the number between 1 to 100", action="store")

    parser.add_option_group(group37)

    group38 = OptionGroup(parser, "*** Timeline : Member", \
                          "display the last events of a member")
    group38.add_option("--timeline_member",
                       help="give the number between 1 to 100", action="store")
    group38.add_option("--timeline_member_login",
                       help="give login of your friend (mandatory)",
                       action="store")
    group38.add_option("--timeline_member_token",
                       help="to use your token", action="store_true")
    parser.add_option_group(group38)

    group39 = OptionGroup(parser, "*** Message : Inbox", "display your inbox")
    group39.add_option("--message_inbox", action="store_true")
    group39.add_option("--message_inbox_page",
                      help="give the number of the page (optional)",
                      action="store")
    parser.add_option_group(group39)

    group40 = OptionGroup(parser, "*** Message : Discussion", \
"display the given discussion")
    group40.add_option("--message_discussion",
                       help="give the id of the discussion to display",
                       action="store")
    group40.add_option("--message_discussion_page",
                       help="give the number of the page (optional)",
                       action="store")
    parser.add_option_group(group40)

    group41 = OptionGroup(parser, "*** Message : Send a new discussion", \
"send a new discussion")
    group41.add_option("--message_send_new",
                       help="give the title of the discussion",
                       action="store")
    group41.add_option("--message_send_new_text",
                       help="give the text of the discussion",
                       action="store")
    group41.add_option("--message_send_new_recipient",
                       help="give the name of the member who'll received it",
                       action="store")
    parser.add_option_group(group41)

    group42 = OptionGroup(parser, "*** Message : Send a response", \
"send a response")
    group42.add_option("--message_send_response",
                       help="give the id of the discusion you're responding",
                       action="store")
    group42.add_option("--message_send_response_text",
                       help="give the text of the response",
                       action="store")
    parser.add_option_group(group42)

    group43 = OptionGroup(parser, "*** Message : Delete", "delete a message")
    group43.add_option("--message_delete",
                       help="give the id of the discusion to delete",
                       action="store")
    parser.add_option_group(group43)

    (options, args) = parser.parse_args()
    if options.title\
            and options.display\
            and options.name and options.episode and options.season\
            and options.chars\
            and options.similar\
            and options.videos\
            and options.sub\
            and options.last_sub\
            and options.planning_member\
            and options.planning_general\
            and options.sub_by_file\
            and options.is_active\
            and options.member_infos\
            and options.member_ep\
            and options.note\
            and options.members_dl_series\
            and options.members_notif\
            and options.members_option\
            and options.members_signup\
            and options.members_add\
            and options.members_delete\
            and options.members_search\
            and options.members_block\
            and options.members_unblock\
            and options.members_options\
            and options.members_sync\
            and options.comments_show\
            and options.comments_episode\
            and options.comments_member\
            and options.comments_post_show\
            and options.comment_post_episode\
            and options.comment_post_member\
            and options.comments_subscribe\
            and options.comments_unsubscribe\
            and options.timeline_home\
            and options.timeline_friends\
            and options.timeline_member\
            and options.message_inbox\
            and options.message_discussion\
            and options.message_send_new\
            and options.message_send_response\
            and options.message_delete:
        parser.error("use only one option available at a time")
    else:
        if len(sys.argv) > 1:
            do_action(options)
        else:
            parser.error("enter -help to see the options you can use")


if __name__ == '__main__':
    main()
