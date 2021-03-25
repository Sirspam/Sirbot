import logging
from firebase_admin import firestore

prefixes_dict = {}

async def cache_prefixes():
    logging.info("Attempting to cache prefixes")
    dab = firestore.client() # Tried putting this outside the function but it threw a fitty
    prefix_col = dab.collection("prefixes").document("collectionlist").get().get("array")
    for x in prefix_col:
        if x in prefixes_dict:
            continue
        ref = dab.collection("prefixes").document(str(x)).get().get("prefix")
        prefixes_dict.update({int(x): ref})
    logging.info("Finished caching prefixes")

async def get_prefix(bot, ctx):
    if prefixes_dict is {}:
        await cache_prefixes()
    if ctx.guild.id not in prefixes_dict:
        return None
    return str(prefixes_dict[ctx.guild.id])

async def dict_delete(ctx): # Needed to clear a server from the prefixes_dict if they set their prefix back to ">"
    del prefixes_dict[ctx.guild.id] # Had to make this function for a single line because I can't be bothered to figure out how to get the dictionary into other files kekw
