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
    logging.info(f"Finished caching prefixes: {prefixes_dict}")

async def get_prefix(bot, ctx):
    if prefixes_dict is {}:
        await cache_prefixes()
    if ctx.guild.id not in prefixes_dict:
        return None
    return str(prefixes_dict[ctx.guild.id])

async def prefix_delete(id):
    try:
        del prefixes_dict[id]
        dab = firestore.client()
        prefix_col = dab.collection("prefixes").document("collectionlist").get().get("array")
        prefix_col.remove(str(id))
        dab.collection("prefixes").document("collectionlist").update({"array": prefix_col})
        dab.collection("prefixes").document(str(id)).delete()
    except Exception as e:
        logging.error(f"Error in prefix_delete: {e}")