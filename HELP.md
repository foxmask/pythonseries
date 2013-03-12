HELP
====

python go_new.py -h
usage: go [options]

BetaSeries API Management

Arguments:
----------
```python
positional arguments:
  {shows_search,shows_display,shows_episodes,shows_characters,shows_similar,
  shows_videos,subtitles_show,subtitles_last,subtitles_show_by_file,
  planning_general,planning_member,member_is_active,member_infos,
  members_episodes,members_note,members_downloaded,members_notifications,
  members_option,members_signup,members_friends,members_badges,members_add,
  members_delete,members_search,members_block,members_unblock,members_options,
  members_sync,comments_show,comments_episode,comments_member,
  comments_post_show,comments_post_episode,comments_post_member,
  comments_subscribe,comments_unsubscribe,timeline_home,timeline_friends,
  timeline_member,message_inbox,message_discussion,message_send_new,
  message_send_response,message_delete}
```

Commands:
---------
each command is a name of the function of the API

to read the help of each of them enter -help eg :

```python
python show_search -help
python message_discussion -help
```
and so on  

here is the complet list of the available commands with short help: 

    shows_search        Search series: use --shows_search --title <title>
    shows_display       Details of series: use --shows_display --url <url>
    shows_episodes      Show Episodes: use --shows_episodes --url <serie>
                        (--season <num>) (--episode <num>)(--summary) to
                        filter episodes you want to search
    shows_characters    Show Characters: use shows_characters --url <serie>
                        (--summary)(--char_id <num>) to find characters for
                        the series you want to search
    shows_similar       Similar Shows:use --shows_similar --url <serie> to
                        find similar serie
    shows_videos        Videos: use shows_videos --url <serie> (--season
                        <num>)(--episode <num> to filter episodes you want to
                        search)
    subtitles_show      Subtitles: use subtitles_show --url <serie> --language
                        <lang> --season <num> --episode <num> to find
                        subtitles you want to search
    subtitles_last      Last Subtitles: use subtitles_last --language <lang>
                        --number <num> to search subtitle you want to search
    subtitles_show_by_file
                        Subtitle by Filename: use subtitles_show_by_file
                        --my_file <file> --language <lang>to search subtitle
                        you want to search
    planning_general    Planning General: display the general planning
    planning_member     Planning Member: display the planning of the member
    member_is_active    Member: is he active ? check if the member is active
    member_infos        Member infos: use members_infos --login <login>
                        --token (optional) --nodata (optional) --since
                        timestamp date
    members_episodes    Member Episodes: members_episodes --subtitles
                        <all|vovf|vf> --show <serie> --view <view>
    members_note        Member Note:use members_note --note <note> --url <url>
                        --episode <num> --season <num>.To give a note to the
                        complet serie put --season 0 and --episode 0
    members_downloaded  Member Downloaded: use members_downloaded --url <url>
                        --episode <num> --season <num>.
    members_notifications
                        Member Notifications: use members_notifications
                        --summary=True/False (optional: default False)
                        --number <num> (optional) --last_id <num> (optional)
                        --sort ASC|DESC (optional) dont mix --last_id and
                        --sort or all notifications could not be get
    members_option      Members : Option use members_option --option
                        <downloaded|notation|decalage> --value <read|edit>
                        (mandatory)
    members_signup      Members Signup use members_signup --login <login>
                        --password <password> --mail <email>
    members_friends     Members Friends: use --members_friends --token to get
                        your friends (optional) OR --login <login> to get the
                        friends of this member (optional)
    members_badges      Members Badges: use members_badges --token to get your
                        friends OR --login <login> to get the friends of this
                        member
    members_add         Members Add: give the login of the friend to add
    members_delete      Members Delete: give the login of the friend to delete
    members_search      Members Search get a list of 10 friends starting by
                        this string, use members_search --login <login>
    members_block       Members Block: give the login of the member to block,
                        use members_block --login <login>
    members_unblock     Members Unblock: give the login of the member to
                        unblock
    members_options     Members Options: will display your own options : use
                        members_options
    members_sync        Members Sync: will list your friend from his email you
                        can put several emails seperated by a comma
    comments_show       Comments Show:display the list of comments of the
                        serie : use comments_show --url <url>
    comments_episode    Comments Episode: display the list of comments of the
                        serie : use comments_episode --url <url> --episode
                        <episde> --season <season>
    comments_member     Comments Member display the member's comments : use
                        comments_member --login <login>
    comments_post_show  Comments Post Show : add a comment to a show : use
                        comments_post_episode
    comments_post_episode
                        Comments Post a comment to an episode, use
                        comments_post_episode
    comments_post_member
                        Comments Post a comment to a member : use
                        comments_post_member
    comments_subscribe  Comments Subscribe to a comment : use
                        comments_subscribe
    comments_unsubscribe
                        Comments Unsubscribe to a comment : use
                        comments_unsubscribe
    timeline_home       Timeline Home display the last events of the website :
                        use --timeline_home --number <num> from 1 to 100 to
                        limit the number of event
    timeline_friends    Timeline Friends display the last events of your
                        friends : use timeline_friends --number <num> from 1
                        to 100 to limit the number of event
    timeline_member     Timeline Member display the last events of a member :
                        use timeline_member --number <num> from 1 import to
                        100 --login <login> --token
    message_inbox       Message Inbox display your inbox : message_inbox
                        --page <page> (optional)
    message_discussion  Message Discussion: display the given discussion : use
                        message_discussion --id <id> --page <page> (optional)
    message_send_new    Message Send: send a new discussion : use
                        message_send_new --title <title> --text
                        <text>--recipient <recipient>
    message_send_response
                        Message Send : send a response : use
                        message_send_response --id <id> --text <text>
    message_delete      Message Delete delete a message : use message_delete
                        --id <id>

optional arguments:
  -h, --help            show this help message and exit
