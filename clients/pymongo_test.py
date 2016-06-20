#coding=utf-8
import mongodb_client

if __name__ == "__main__" :
    coll = mongodb_client.get_coll("UserAddress")
    #
    #insert one
    # res = coll.insert_one({
    #         "kid":"4",
    #         "name":"niyoufa",
    #         "a":"c",
    #         "b":"b",
    #     })
    # print res #<pymongo.results.InsertOneResult object at 0x7f79e31cd960>
    # print res.inserted_id #574fe43887b244648545fbc2
    #
    # # insert
    # res = coll.insert([
    #     {
    #         "kid":"1",
    #         "name":"niyoufa",
    #     },
    #     {
    #         "kid": "2",
    #         "name":"liuxiaoyan",
    #     },
    #     {
    #         "kid": "3",
    #         "name":"xiaming",
    #     }
    # ])
    # print res # [ObjectId('574fe37a87b244636a6762e2'), ObjectId('574fe37a87b244636a6762e3'), ObjectId('574fe37a87b244636a6762e4')]
    #
    #
    # # insert many
    # res = coll.insert_many([
    #     {
    #         "kid": "5",
    #         "name": "niyoufa",
    #     },
    #     {
    #         "kid": "6",
    #         "name": "liuxiaoyan",
    #     },
    #     {
    #         "kid": "7",
    #         "name": "xiaming",
    #     }
    # ])
    # print res # <pymongo.results.InsertManyResult object at 0x7f79e31cd960>
    # print res.inserted_ids # [ObjectId('574fe43887b244648545fbc6'), ObjectId('574fe43887b244648545fbc7'), ObjectId('574fe43887b244648545fbc8')]
    #
    # # find_one
    # res = coll.find_one()
    # print res # {u'_id': ObjectId('574fe2c787b2446254bd99e4'), u'name': u'niyoufa'}
    #
    # # find
    # res = coll.find()
    # print res #<pymongo.cursor.Cursor object at 0x7f79e5ed8ed0>
    #
    # # count
    # print coll.count()
    # print coll.find().count()
    #
    # #sort
    # res = coll.find().sort("name",-1)
    # for obj in res :
    #     print obj["name"]

    # index
    # coll.create_index([('kid', pymongo.ASCENDING),('a',pymongo.ASCENDING)],name="kid_a" , unique=True)
    # coll.drop_index("kid_a")


    # coll.insert({
    #     "kid": "4",
    #     "name":"niyoufa",
    #     "a":"c",
    #     "b":"b",
    # })
    # coll.insert({
    #     "kid": "4",
    #     "name": "niyoufa",
    #     "a": "a",
    #     "b": "b",
    # })

    # update_one
    # res = coll.update_one({"name":"niyoufa"},{"$set":{"name":"ni"}}) # <pymongo.results.UpdateResult object at 0x7f21bfd9ab40>
    # print res

    # update_many
    # res = coll.update_many({"name":"niyoufa"},{"$set":{"name":"ni"}})
    # print res # <pymongo.results.UpdateResult object at 0x7f32da128b90>


    # find_one_and_update
    # res = coll.find_one_and_update({"name":"niyoufa"},{"$set":{"name":"ni"}})

    # group
    # group(key, condition, initial, reduce, finalize=None)
    # coll.insert_many([
    #     {
    #         "poiName":"a",
    #         "editStatus":"accept",
    #     },
    #     {
    #         "poiName":"a",
    #         "editStatus":"accept",
    #     },
    #     {
    #         "poiName":"b",
    #         "editStatus":"accept",
    #     },
    #     {
    #         "poiName":"a",
    #         "editStatus":"pending",
    #     },
    # ])
    #
    # func = """
    #     function(obj, prev){
    #         if(obj.editStatus == 'pending')
    #             prev.pendingNum++;
    #         else if (obj.editStatus == 'discard')
    #             prev.discardNum++;
    #         else if (obj.editStatus == 'accept')
    #             prev.acceptNum++;
    #         prev.shareNum++;
    #     }
    # """
    # res = coll.group(["poiName"], None,{
    #     "pendingNum": 0, "discardNum": 0, "acceptNum": 0
    # },func)
    # print res
    # [{u'pendingNum': 1.0, u'poiName': u'a', u'shareNum': nan, u'discardNum': 0.0, u'acceptNum': 2.0},
    #  {u'pendingNum': 0.0, u'poiName': u'b', u'shareNum': nan, u'discardNum': 0.0, u'acceptNum': 1.0}]


    # map_reduce
    from bson.code import Code

    # coll.insert({"x": 1, "tags": ["dog", "cat"]})
    # coll.insert({"x": 2, "tags": ["cat"]})
    # coll.insert({"x": 2, "tags": ["mouse", "cat", "dog"]})
    # coll.insert({"x": 3, "tags": []})

    # mapper = Code(
    #     """
    #         function () {
    #             this.tags.forEach(function(z) {
    #             emit(z, 1);
    #             });
    #         }
    #     """
    # )
    #
    # reducer = Code(
    #     """
    #         function (key, values) {
    #             var total = 0;
    #             for (var i = 0; i < values.length; i++) {
    #                 total += values[i];
    #             }
    #             return total;
    #         }
    #     """
    # )
    #
    # result = coll.map_reduce(mapper, reducer, out="result_collection", full_response=True,
    #                               query={"tags": {"$exists": "true"}})
    #

    # aggreate
    from bson.son import SON

    # pipeline = [
    #     {"$unwind": "$tags"},
    #     {"$group": {"_id": "$tags", "count": {"$avg": "$x"}}},
    #     {"$sort": SON([("count", -1), ("_id", -1)])}
    # ]
    # result = coll.aggregate(pipeline)
    # for doc in result:
    #     print doc
    #
    # print "\n"
    #
    # pipeline = [
    #     {"$unwind": "$tags"},
    #     {"$group": {"_id": "$tags", "count": {"$sum": "$x"}}},
    #     {"$sort": SON([("count", -1), ("_id", -1)])}
    # ]
    # result = coll.aggregate(pipeline)
    # for doc in result :
    #     print doc
    #
    # print "\n"