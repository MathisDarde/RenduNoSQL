from pymongo import MongoClient
from db.configuration import DATABASE_NAME, DATABASE_URL
from uuid import uuid4
from datetime import datetime
from math import ceil

class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db = None
    
    def connect(self):
        try:
            self.client = MongoClient(DATABASE_URL)
            self.db = self.client[DATABASE_NAME]
            print("Connection is OK")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def disconnect(self):
        if self.client:
            self.client.close()
    
    def get_collection(self, collection_name):
        return self.db[collection_name]
    
    def create_item(self, collection_name, item, created_by=None):
        collection = self.get_collection(collection_name)

        now = datetime.now()
        item_to_insert = {
            "pid": str(uuid4()),
            "created_at": now,
            "updated_at": now,
            **item
        }
        if created_by:
            item_to_insert["created_by"] = created_by

        return collection.insert_one(item_to_insert).inserted_id

    def create_items(self, collection_name, items, created_by=None):
        collection = self.get_collection(collection_name)
        now = datetime.now()
        items_to_insert = []

        for item in items:
            item_data = {
                "pid": str(uuid4()),
                "created_at": now,
                "updated_at": now,
                **item
            }
            if created_by:
                item_data["created_by"] = created_by
            items_to_insert.append(item_data)

        return collection.insert_many(items_to_insert).inserted_ids 
    
    def update_item_by_pid(self, collection_name, pid, item_data, updated_by=None):
        collection = self.get_collection(collection_name)
        now = datetime.now()

        set_stage = {**item_data, "updated_at": now}
        if updated_by:
            set_stage["updated_by"] = updated_by

        result = collection.update_one(
            {"pid": pid},
            [{"$set": set_stage}] 
        )
        return result.modified_count

    def update_items_by_pids(self, collection_name, pids, items_data, updated_by=None):
        collection = self.get_collection(collection_name)
        now = datetime.now()

        set_stage = {**items_data, "updated_at": now}
        if updated_by:
            set_stage["updated_by"] = updated_by

        result = collection.update_many(
            {"pid": {"$in": pids}},
            [{"$set": set_stage}]
        )
        return result.modified_count

    def update_item_by_attr(self, collection_name, attributes, item_data, updated_by=None):
        collection = self.get_collection(collection_name)
        now = datetime.now()

        set_stage = {**item_data, "updated_at": now}
        if updated_by:
            set_stage["updated_by"] = updated_by

        result = collection.update_one(
            attributes,
            [{"$set": set_stage}]
        )
        return result.modified_count

    def update_items_by_attr(self, collection_name, attributes, items_data, updated_by=None):
        collection = self.get_collection(collection_name)
        now = datetime.now()

        set_stage = {**items_data, "updated_at": now}
        if updated_by:
            set_stage["updated_by"] = updated_by

        result = collection.update_many(
            attributes,
            [{"$set": set_stage}] 
        )
        return result.modified_count
    
    def get_item_by_pid(self, collection_name, pid, fields=None):
        collection = self.get_collection(collection_name)

        if fields is None:
            projection = {"pid": 1, "_id": 0}
        elif fields == []:
            projection = {"_id": 0}
        else:
            projection = {field: 1 for field in fields}
            projection["pid"] = 1
            projection["_id"] = 0

        return collection.find_one({"pid": pid}, projection)

    def get_item_by_attr(self, collection_name, attributes, fields=None):
        collection = self.get_collection(collection_name)

        if fields is None:
            projection = {"pid": 1, "_id": 0}
        elif fields == []:
            projection = {"_id": 0}
        else:
            projection = {field: 1 for field in fields}
            projection["pid"] = 1
            projection["_id"] = 0

        return collection.find_one(attributes, projection)
    
    def delete_item_by_pid(self, collection_name, pid):
        collection = self.get_collection(collection_name)
        result = collection.delete_one({"pid": pid})
        return result.deleted_count

    def delete_items_by_pids(self, collection_name, pids):
        collection = self.get_collection(collection_name)
        result = collection.delete_many({"pid": {"$in": pids}})
        return result.deleted_count

    def delete_item_by_attr(self, collection_name, attributes):
        collection = self.get_collection(collection_name)
        result = collection.delete_one(attributes)
        return result.deleted_count

    def delete_items_by_attr(self, collection_name, attributes):
        collection = self.get_collection(collection_name)
        result = collection.delete_many(attributes)
        return result.deleted_count
    
    def array_push_item_by_pid(self, collection_name, pid, array_field, new_item, updated_by=None):
        collection = self.get_collection(collection_name)
        update_data = {"$push": {array_field: new_item}, "$set": {"updated_at": datetime.utcnow()}}
        if updated_by:
            update_data["$set"]["updated_by"] = updated_by
        result = collection.update_one({"pid": pid}, update_data)
        return result.modified_count

    def array_push_item_by_attr(self, collection_name, attributes, array_field, new_item, updated_by=None):
        collection = self.get_collection(collection_name)
        update_data = {"$push": {array_field: new_item}, "$set": {"updated_at": datetime.utcnow()}}
        if updated_by:
            update_data["$set"]["updated_by"] = updated_by
        result = collection.update_many(attributes, update_data)
        return result.modified_count

    def array_pull_item_by_pid(self, collection_name, pid, array_field, item_attr, updated_by=None):
        collection = self.get_collection(collection_name)
        update_data = {"$pull": {array_field: item_attr}, "$set": {"updated_at": datetime.utcnow()}}
        if updated_by:
            update_data["$set"]["updated_by"] = updated_by
        result = collection.update_one({"pid": pid}, update_data)
        return result.modified_count

    def array_pull_item_by_attr(self, collection_name, attributes, array_field, item_attr, updated_by=None):
        collection = self.get_collection(collection_name)
        update_data = {"$pull": {array_field: item_attr}, "$set": {"updated_at": datetime.utcnow()}}
        if updated_by:
            update_data["$set"]["updated_by"] = updated_by
        result = collection.update_many(attributes, update_data)
        return result.modified_count
    
    def get_items(
        self,
        collection_name,
        attributes={},
        fields=None,
        sort=None,
        skip=0,
        limit=None,
        return_stats=False,
        pipeline=None
    ):
        collection = self.get_collection(collection_name)
        
        if fields is None:
            projection = {"pid": 1, "_id": 0}
        elif fields == []:
            projection = {"_id": 0}
        else:
            projection = {field: 1 for field in fields}
            projection["pid"] = 1
            projection["_id"] = 0

        if pipeline is not None:
            stages = pipeline.copy()
            if attributes:
                stages.insert(0, {"$match": attributes})
            if fields is not None:
                stages.append({"$project": projection})
            if sort:
                stages.append({"$sort": sort})
            if skip:
                stages.append({"$skip": skip})
            if limit:
                stages.append({"$limit": limit})

            items = list(collection.aggregate(stages))
            total_count = collection.count_documents(attributes) if return_stats else None

        else: 
            cursor = collection.find(attributes, projection)
            if sort:
                cursor = cursor.sort(list(sort.items()))
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)
            items = list(cursor)
            total_count = collection.count_documents(attributes) if return_stats else None

        if return_stats:
            stats = {
                "itemsCount": total_count,
                "pagesCount": ceil(total_count / limit) if limit else 1,
                "firstIndexReturned": skip + 1 if items else 0,
                "lastIndexReturned": skip + len(items)
            }
            return items, stats
        else:
            return items


if __name__ == "__main__":
    mongo = MongoDBConnection()
    if mongo.connect():
        mongo.disconnect()
    else:
        print("Failed to connect to the database")