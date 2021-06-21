import logging

from firebase_admin import firestore


async def cache_prefixes():
    logging.info("Attempting to cache prefixes")
    global prefixes_dict
    prefixes_dict = dict()
    dab = firestore.client()
    prefix_col = dab.collection("prefixes").document("collectionlist").get().get("array")
    for x in prefix_col:
        if x in prefixes_dict:
            continue
        ref = dab.collection("prefixes").document(str(x)).get().get("prefix")
        prefixes_dict.update({int(x): ref})
    logging.info(f"Finished caching prefixes: {prefixes_dict}")

async def get_prefix(ctx):
    if int(ctx.guild.id) not in prefixes_dict:
        return None
    return str(prefixes_dict[ctx.guild.id])

async def prefix_delete(guild_id):
    try:
        del prefixes_dict[guild_id]
        dab = firestore.client()
        prefix_col = dab.collection("prefixes").document("collectionlist").get().get("array")
        prefix_col.remove(str(guild_id))
        dab.collection("prefixes").document("collectionlist").update({"array": prefix_col})
        dab.collection("prefixes").document(str(guild_id)).delete()
    except Exception as e:
        logging.error(f"Error in prefix_delete: {e}")