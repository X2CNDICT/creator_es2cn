def refine_meaning(es2cn):
  ws = es2cn.vocabs.find({})
  for e in ws:
    ex = e["explanation"]
    for item in ex:
      meaning = ", ".join(item["meaning"].split(","))
      item["meaning"] = meaning
    print(e)
    es2cn.vocabs.update_one({"_id": e["_id"]}, {"$set": {"explanation": ex}})

