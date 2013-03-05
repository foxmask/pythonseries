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
            print "-"+genre
        print "Description: %s"  % data['show']['description']
        print "seasons:"
        for season in data['root']['show']['seasons']:
            print season, ' sur ', data['show']['seasons'][season]['episodes']
        #all the data
        #print data
    elif options.name:
         
        """
        shows_episodes wrapper
        """
        print "you want to search serie %s " % options.name
        if options.episode and options.season and options.summary:
            data = c.shows_episodes(options.name, 
                                    options.episode,
                                    options.season, 
                                    options.summary)
        elif options.episode and options.season:
            data = c.shows_episodes(options.name, 
                                    options.season,
                                    options.episode)
        elif options.episode and options.summary:
            data = c.shows_episodes(options.name, 
                                    None,
                                    options.episode,
                                    options.summary)
        elif options.season and options.summary:
            data = c.shows_episodes(options.name, 
                                    options.season,
                                    None, 
                                    options.summary)
        elif options.season:
            data = c.shows_episodes(options.name, 
                                    options.season)
        elif options.episode:
            data = c.shows_episodes(options.name, 
                                    None,
                                    options.episode)
        elif options.summary:
            data = c.shows_episodes(options.name, 
                                    None,
                                    None, 
                                    options.summary)
        else:
            data = c.shows_episodes(options.name, options.episode,
                                    options.season)
        #oops we try to find a serie that does not exist
        if 'seasons' not in data.keys() > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:

        #all the data
        #print data
            for season in data['seasons']:
                for ep in data['seasons'][season]['episodes']:
                    number = data['seasons'][season]['episodes'][ep]['number']
                    title = data['seasons'][season]['episodes'][ep]['title']
                    print "Number: {number} Title: {title} ".\
                    format(number=number,title=title) 
#    elif options.add:
#        """
#        shows_add wrapper
#        """
#        print "you want to add a file to your account"
#        data = c.shows_add()
#    elif options.remove:
#        """
#        shows_remove wrapper
#        """
#        print "you want to remove a file to your account"
#        data = c.shows_remove()
#    elif options.recommend:
#        """
#        shows_recommend wrapper
#        """        
#        print "you want to recommend a file to a friend"
#        data = c.shows_recommend()
#        print data
#    elif options.archive:
#        """
#        shows_archive wrapper
#        """
#        print "you want to archive a serie"
#        data = c.shows_archive()
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
#        data = c.shows_unarchive()
#        print data
    elif options.chars:
        """
        shows_characters wrapper
        """
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
        #oops we try to find a serie that does not exist
        if 'characters' not in data.keys() > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            for character in data['characters']:
                print data['characters'][character]['name']
#    elif options.similar:
#        print "you want to find similar serie to " + options.similar
#        data = c.shows_similar(options.similar)
#        print data
    elif options.videos:
        print "you want to search videos of serie " + options.videos
        if options.sv and options.ev:
            data = c.shows_videos(options.videos, options.sv, options.ev)
        elif options.sv:
            data = c.shows_videos(options.videos, options.sv)
        elif options.ev:
            data = c.shows_videos(options.videos, None, options.ev)
        else:
            data = c.shows_videos(options.videos)

        #oops we try to find a serie that does not exist
        if 'videos' not in data.keys() > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
            #all the data
            #print data
            print "title %14s - youtube id %10s" % (' ', ' ')
            for video in data['videos']:
                print "%20s - %10s" %\
                      (data['videos'][video]['title'],
                       data['videos'][video]['youtube_id'])
    elif options.last_sub:
        """
        subtitles_last wrapper
        """
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

        #oops we try to find a serie that does not exist
        if 'subtitles' not in data.keys() > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
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
    elif options.sub:
        """
        subtitles_show wrapper
        """
        print "you want to search subtitles of serie "+options.sub
        if options.sub_lang and options.sub_sv and options.sub_ev:
            data = c.subtitles_show(options.sub,
                                  options.sub_lang, 
                                  options.sub_sv, 
                                  options.sub_ev)
        elif options.sub_lang and options.sub_sv:
            data = c.subtitles_show(options.sub,
                                  options.sub_lang, 
                                  options.sub_sv)
        elif options.sub_lang and options.sub_ev:
            data = c.subtitles_show(options.sub,
                                  options.sub_lang,
                                  None, 
                                  options.sub_ev)
        elif options.sub_sv and options.sub_ev:
            data = c.subtitles_show(options.sub,
                                  None, 
                                  options.sub_sv, 
                                  options.sub_ev)
        elif options.sub_sv:
            data = c.subtitles_show(options.sub,
                                  None, 
                                  options.sub_sv)
        elif options.sub_ev:
            data = c.subtitles_show(options.sub,
                                  None, 
                                  None, 
                                  options.sub_ev)
        else:
            data = c.subtitles_show(options.sub)

        #oops we try to find a serie that does not exist
        if 'subtitles' not in data.keys() > 0:
            for error in data['errors']:
                print "Error:"
                print data['errors'][error]['content']
        else:
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
#    elif options.sub_by_file:
#        print "you want to get the subtitle from a given filename"
#        #todo fix the name of the options
#        data = c.subtitles_show_by_file(options.sub_filename,options.sub_lang)
#        print data
#    elif options.is_activated:
#        """
#        member_is_activated wrapper
#        """
#        print "you want to check if the user is autenticated"
#        #todo : fix the options.token
#        data = c.member_is_activated(options.token)
#        print data
#    elif options.member_destroy:
#        """
#        member_destroy wrapper
#        """
#        print "you want to destroy immediatly the token " + options.token
#        data = c.member_destroy(options.token)


def main():
    #meme message d'aide en plus concis
    #usage = "%prog --title my_title\n\
    #        --episodes --episode n --season m"
    parser = OptionParser()

    group0 = OptionGroup(parser, "*** Search series")
    group0.add_option("--title",  dest="title", type="string",
                      help="make a search by title")
    parser.add_option_group(group0)
    
    #group the options for handling Display of series parameters
    group1 = OptionGroup(parser, "*** Details of series")
    group1.add_option("--display", dest="display", action="store",
                     help="the name of the given serie")
    parser.add_option_group(group1)

    #group the options for handling Episodes parameters
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
                     help="give the name of the serie you want to see subtitle")

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
                     help="display the last sub for a given language: vo or vf")

    group6.add_option("--last_sub_nb", dest="last_sub_nb", action="store",
                     help="display the 'n' last subtitles")

    parser.add_option_group(group6)

    
    (options, args) = parser.parse_args()
    if options.title\
            and options.display\
            and options.name and options.episode and options.season\
            and options.chars\
            and options.videos\
            and options.sub\
            and options.last_sub:
        parser.error("only one option available at a time")
    else:
        do_action(options)

if __name__ == '__main__':
    main()
