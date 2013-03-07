# -*- coding: utf-8 -*-
from optparse import OptionParser, OptionGroup

import ConfigParser
import os

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
            # all the data
            # print data['subtitles']
            print "{season:^10} {ep:^10} {lang:^5} {file:^50} {url:^50}".\
                format(season='Season',
                       ep='Episode',
                       lang='Lang',
                       file='File',
                       url='URL')

            # print data['subtitles']

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


def main():
    # meme message d'aide en plus concis
    # usage = "%prog --title my_title\n\
    #        --episodes --episode n --season m"
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
                     help="boolean set to true by default")

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
            and options.note:
        parser.error("use only one option available at a time")
    else:
        do_action(options)

if __name__ == '__main__':
    main()
