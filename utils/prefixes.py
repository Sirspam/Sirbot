import logging
from firebase_admin import firestore

prefixes_dict = {}
col = None

async def cache_prefixes():
    logging.info("Attempting to cache prefixes")
    dab = firestore.client()
    col = dab.collection("prefixes").document("collectionlist").get().get("array")
    for x in col:
        if x in prefixes_dict:
            continue
        ref = dab.collection("prefixes").document(str(x)).get().get("prefix")
        prefixes_dict.update({x: ref})
        logging.info(prefixes_dict)
    logging.info("Finished caching prefixes")

async def get_prefix(bot, ctx):
    if prefixes_dict is {}:
        await cache_prefixes
    if ctx.guild.id not in col:
        return None
    return str(prefixes_dict[ctx.guild.id])
    
    
