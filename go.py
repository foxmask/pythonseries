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
        for genre in data['root']['show']['genres'].values():
            print "-"+genre
        print "Description: %s"  % data['root']['show']['description']
        print "seasons:"
        for season in data['root']['show']['seasons']:
            print season, ' sur ', data['root']['show']['seasons'][season]['episodes']
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
        number = data['root']['seasons'][u'0']['episodes'][u'0']['number']
        title = data['root']['seasons'][u'0']['episodes'][u'0']['title']
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
        for character in data['root']['characters']:
            print data['root']['characters'][character]['name']

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

    (options, args) = parser.parse_args()
    if options.title and options.display\
            and options.episode and options.season\
            and options.characters:
        parser.error("only one option available at a time")
    else:
        do_action(options)

if __name__ == '__main__':
    main()
