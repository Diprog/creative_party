from vk.api import VKAPI
import asyncio
import db.posts
import utils
import time
class GroupParser:
    def __init__(self, vk, group_id):
        self.vk = vk
        self.group_id = group_id

    async def get_all_posts(self):
        posts = await self.vk.get('wall.get', group_id=self.group_id, count=100)
        items = posts['items']
        count = posts['count']
        offset = 1
        while count >= 100:
            posts = await self.vk.get('wall.get', group_id=self.group_id, count=100, offset=offset*100)
            items += posts['items']
            count -= posts['count']
            offset += 1
        return items

    async def get_all_comments(self, posts):
        posts_chunks = utils.chunks(posts, 25)
        threads = []
        for chunk in posts_chunks:
            post_ids = [post['id'] for post in chunk]
            owner_ids = [post['owner_id'] for post in chunk]
            threads.append(self.vk.execute(f'''
                var a = {str(post_ids)};
                var b = {str(owner_ids)};
                var c = {len(post_ids)};
                var d = 0;
                var comments = [];
                while (c - d > 0) {{
                    comments.push({{"owner_id": b[d], 
                                    "post_id": a[d],
                                    "comments": API.wall.getComments({{
                                        "owner_id":b[d], 
                                        "post_id":a[d], 
                                        "extended": 1,
                                        "fields": "city",
                                        "count":100
                                    }})
                    }});
                    d = d + 1;
                }};
                return comments;
            '''))
        result = await asyncio.wait_for(asyncio.gather(*threads), timeout=None)
        # Результат возвращается также по чанкам, так что чанки надо объединить.
        comments = []
        for chunk in result:
            comments += chunk
        return comments

    async def get_all_likes(self, posts):
        posts_chunks = utils.chunks(posts, 25)
        threads = []
        for chunk in posts_chunks:
            post_ids = [post['id'] for post in chunk]
            owner_ids = [post['owner_id'] for post in chunk]
            threads.append(self.vk.execute(f'''
                        var a = {str(post_ids)};
                        var b = {str(owner_ids)};
                        var c = {len(post_ids)};
                        var d = 0;
                        var likes = [];
                        while (c - d > 0) {{
                            likes.push({{"owner_id": b[d], 
                                            "post_id": a[d],
                                            "likes": API.likes.getList({{
                                                "type":"post",
                                                "owner_id":b[d], 
                                                "item_id":a[d], 
                                                "extended": 1,
                                                "count":1000
                                            }})
                            }});
                            d = d + 1;
                        }};
                        return likes;
                    '''))
        result = await asyncio.wait_for(asyncio.gather(*threads), timeout=None)
        # Результат возвращается также по чанкам, так что чанки надо объединить.
        likes = []
        for chunk in result:
            likes += chunk
        return likes


async def main():
    group_id = 177920803
    async with VKAPI(['483dc040cfe9b5877db315ef57607277e4ca902c2273cf43e383ccd1497020273df5abca3c852024ac5c4']) as vk:
        now = time.time()
        parser = GroupParser(vk, group_id)
        posts = db.posts.get()
        if not posts:
            posts = await parser.get_all_posts()
            db.posts.save(posts)
        comments = await parser.get_all_comments(posts)
        likes = await parser.get_all_likes(posts)
        for like in likes:
            print(len(like['likes']['items']))
        print(len(likes))
        print(time.time() - now)


if __name__ == '__main__':
    asyncio.run(main())