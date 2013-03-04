# -*- coding: utf-8 -*-
from optparse import OptionParser, OptionGroup


def do_action(options):
    #import hashlib
    import ConfigParser
    import os
    
    config = ConfigParser.ConfigParser()
    config.read(os.getcwd()+'/series.config')
    #hash_pass = hashlib.md5(config.get('auth','password')).hexdigest()

    from pythonseries.pythonseries import Client
    c = Client(api_key=config.get('api','key'))
    #c.members_auth(config.get('auth','login'), hash_pass)
    data = {}
    if options.title:
        print "you want to search the title of a movie " + options.title
        data = c.shows_search(options.title)
    elif options.display:
        print "you want to display the content of a serie " + options.display
        data = c.shows_display(options.display)
        print "Genre:"
        for genre in data['show']['genres'].values():
            print "-"+genre
        print "Description: %s"  % data['show']['description']
        print "seasons:"
        for season in data['root']['show']['seasons']:
            print season, ' sur ', data['show']['seasons'][season]['episodes']
        #all the data
        #print data
    elif options.name and options.episode and options.season:
        print "you want to search serie {name} the episode {episode} \
               of the season {season}".\
               format(name=options.name, episode=options.episode,
                         season=options.season)
        if options.summary:
            data = c.shows_episodes(options.name, options.episode,
                                    options.season, options.summary)
        else:
            data = c.shows_episodes(options.name, options.episode,
                                    options.season)

        #all the data
        #print data
        number = data['seasons'][u'0']['episodes'][u'0']['number']
        title = data['seasons'][u'0']['episodes'][u'0']['title']
        print "Number: {number} Title: {title} ".format(number=number,title=title)

    elif options.characters:
        print "you want to search characters of the serie {characters}"\
                .format(characters=options.characters)
        if options.char_summary and options.char_id:
            data = c.shows_characters(options.characters, options.char_summary,\
                                      options.char_id)
        elif options.char_summary:
            data = c.shows_characters(options.characters, options.char_summary)
        elif options.char_id:
            data = c.shows_characters(options.characters, False, options.char_id)
        else:
            data = c.shows_characters(options.characters)
        for character in data['characters']:
            print data['characters'][character]['name']
    elif options.videos:
        print "you want to search videos of serie "+options.videos
        if options.season_video and options.episode_video:
            data = c.shows_videos(options.videos, options.season_video,
                                    options.episode_video)
        elif options.season_video:
            data = c.shows_videos(options.videos, options.season_video)
        elif options.episode_video:
            data = c.shows_videos(options.videos, None, options.episode_video)
        else:
            data = c.shows_videos(options.videos)

        #all the data
        #print data
        print "title %14s - youtube id %10s" % (' ', ' ')
        for video in data['videos']:
            print "%20s - %10s" %\
                  (data['videos'][video]['title'],
                   data['videos'][video]['youtube_id'])
    elif options.sub:
        print "you want to search subtitles of serie "+options.sub
        if options.sub_lang and options.sub_sv and options.sub_ev:
            data = c.shows_subtitles_show(options.sub,
                                  options.sub_lang, 
                                  options.sub_sv, 
                                  options.sub_ev)
        elif options.sub_lang and options.sub_sv:
            data = c.shows_subtitles_show(options.sub,
                                  options.sub_lang, 
                                  options.sub_sv)
        elif options.sub_lang and options.sub_ev:
            data = c.shows_subtitles_show(options.sub,
                                  options.sub_lang,
                                  None, 
                                  options.sub_ev)
        elif options.sub_sv and options.sub_ev:
            data = c.shows_subtitles_show(options.sub,
                                  None, 
                                  options.sub_sv, 
                                  options.sub_ev)
        elif options.sub_sv:
            data = c.shows_subtitles_show(options.sub,
                                  None, 
                                  options.sub_sv)
        elif options.sub_ev:
            data = c.shows_subtitles_show(options.sub,
                                  None, 
                                  None, 
                                  options.sub_ev)
        else:
            data = c.subtitles_show(options.sub)

        #all the data
        #print data['subtitles']
        print "season %s - episode %s - title %14s - Lg%s" %\
              (' ', ' ', ' ', ' ')
        for subtitle in data['subtitles']:
            print "%5s - %5s - %20s - %s" %\
                  (data['subtitles'][subtitle]['season'],
                   data['subtitles'][subtitle]['episode'],
                   data['subtitles'][subtitle]['title'],
                   data['subtitles'][subtitle]['language']
                   )
    elif options.last_sub:
        print "you want to see the last subtitles"
        if options.last_sub_lang and options.last_sub_nb:
            data = c.subtitles_last(options.last_sub_lang, 
                                  options.last_sub_nb)
        elif options.last_sub_lang:
            data = c.subtitles_last(options.last_sub_lang)
        elif options.last_sub_nb:
            data = c.subtitles_last(None, 
                                  options.last_sub_nb)
        else:
            data = c.subtitles_last(None, None)

        #all the data
        #print data
        print "season %s - episode %s - title %7s - Lg%s- file %14s" %\
              (' ', ' ', ' ', ' ', ' ')
        for last_sub in data['subtitles']:
            print "%5s - %5s - %20s - %s - %20s" %\
                  (data['subtitles'][last_sub]['season'],
                   data['subtitles'][last_sub]['episode'],
                   data['subtitles'][last_sub]['title'],
                   data['subtitles'][last_sub]['language'],
                   data['subtitles'][last_sub]['file']
                   )

def main():
    #meme message d'aide en plus concis
    usage = "%prog --title my_title\n\
            --episodes --episode n --season m"
    parser = OptionParser(usage)

    parser.add_option("--title",  dest="title", type="string",
                      help="make a search by title")

    #group the options for handling Display of series parameters
    group1 = OptionGroup(parser, "Display details of series",
                        "use --display <serie>")
    group1.add_option("--display", dest="display", action="store",
                     help="the name of the given serie")
    parser.add_option_group(group1)

    #group the options for handling Episodes parameters
    group2 = OptionGroup(parser, "Episodes handling",
                        "use --name <serie> --season <num> --episode <num>\
                        to filter episodes you want to search")
    group2.add_option("--name", dest="name", action="store",
                     help="the name of the given serie")

    group2.add_option("--episode", dest="episode", action="store",
                     help="the number of the episode")

    group2.add_option("--season", dest="season", action="store",
                     help="the number of the season")

    group2.add_option("--summary", dest="summary", action="store_true",
                     help="only get the summary of the episode (optional)")

    parser.add_option_group(group2)

    group3 = OptionGroup(parser, "Characters handling",
                        "use --name <serie> --season <num> --episode <num>\
                        to filter episodes you want to search")

    group3.add_option("--characters", dest="characters", action="store",
                     help="display the list of character")

    group3.add_option("--char_summary", dest="char_summary", action="store_true",
                     help="only get the summary of the characters (optional)")

    group3.add_option("--char_id", dest="char_id", action="store",
                     help="display info of THIS character (optional)")

    parser.add_option_group(group3)

    group4 = OptionGroup(parser, "Videos handling",
                        "use --videos <serie> --sv <num> --ev <num>\
                        to filter episodes you want to search")

    group4.add_option("--videos", dest="videos", action="store",
                     help="get the video of the given serie")

    group4.add_option("--sv", dest="season_video", action="store",
                     help="display the list of video of the given season")

    group4.add_option("--ev", dest="episode_video", action="store",
                     help="display the list of video of the given episode")

    parser.add_option_group(group4)


    group5 = OptionGroup(parser, "Subtitles handling",
                        "use --sub <serie> --lang <lang> --sub_sv <num>\
                        --sub_ev to search subtitle you want to search")

    group5.add_option("--sub", dest="sub", action="store",
                     help="get the subtitles of the given serie")

    group5.add_option("--sub_lang", dest="sub_lang", action="store",
                     help="display the list of subtitles for the gieven language")

    group5.add_option("--sub_sv", dest="sub_sv", action="store",
                     help="display the list of subtitles of the given season")

    group5.add_option("--sub_ev", dest="sub_ev", action="store",
                     help="display the list of subtitle of the given episode")

    parser.add_option_group(group5)

    group6 = OptionGroup(parser, "Last Subtitles handling",
                        "use --last_sub --last_lang <lang> --last_nb <num>\
                        to search subtitle you want to search")

    group6.add_option("--last_sub", dest="last_sub", action="store_true",
                     help="get the last subtitles")

    group6.add_option("--last_sub_lang", dest="last_sub_lang", action="store",
                     help="display the last subtitles for a given langugage")

    group6.add_option("--last_sub_nb", dest="last_sub_nb", action="store",
                     help="display the 'n' last subtitles")

    parser.add_option_group(group6)

    
    (options, args) = parser.parse_args()
    if options.title and options.display\
            and options.episode and options.season\
            and options.characters and options.videos\
            and options.sub and options.last_sub:
        parser.error("only one option available at a time")
    else:
        do_action(options)

if __name__ == '__main__':
    main()
