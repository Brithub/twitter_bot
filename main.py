import generate
import tweet_dumper
import pfp


def downloader_function(thing, thing2):
    try:
        return tweet_dumper.downloader_function(thing, thing2)
    except Exception as e:
        print(f"Something went wrong")
        return e.with_traceback()


def compose_and_send_tweet(thing, thing2):
    return generate.compose_and_send_tweet(thing, thing2)


def generate_and_update_pfp(x, y):
    return pfp.generate_and_update_pfp(x,y)