import logging
from firebase_admin import firestore

prefixes_dict = {}

async def cache_prefixes():
    logging.info("Attempting to cache prefixes")
    dab = firestore.client()
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
    
    
