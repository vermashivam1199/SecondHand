from django.db import models
from add.tests import pint




class RecemondationManager(models.Manager):

    def user_recemondations(self, owner):
        print(owner)
        cat = self.get_queryset().raw(f'''WITH x AS
                                                (SELECT
                                                    1 AS id
                                                    ,f.id AS f_id 
                                                    ,c.id AS c_id
                                                    ,c.name AS c_name
                                                    ,a.id AS a_id
                                                    ,a.name AS a_name
                                                    ,o.id AS o_id
                                                    ,a.description AS descp 
                                                    ,COUNT(o.price_offered) OVER(PARTITION BY a.id) as total_count
                                                FROM add_category AS c
                                                JOIN add_favrioute AS f ON f.category_id = c.id
                                                JOIN add_add AS a ON a.category_id = c.id
                                                JOIN add_offeredprice AS o ON a.id = o.add_id
                                                WHERE f.owner_id = {owner}),
                                            y AS
                                                (SELECT
                                                    *
                                                    ,DENSE_RANK() OVER(PARTITION BY c_id ORDER BY total_count DESC) as rank
                                                FROM x)
                                            SELECT * FROM y
                                            WHERE y.rank <= 5''')
        temp_dict = {}
        for c in cat:
            if c.a_id not in temp_dict:
                temp_dict[c.a_id] = c
        return [t for t in temp_dict.values()]


    def anonomous_user_recemondations(self):
        cat = self.get_queryset().raw('''WITH x AS
                                                (SELECT
                                                    1 AS id
                                                    ,c.id AS c_id
                                                    ,c.name AS c_name
                                                    ,a.id AS a_id
                                                    ,a.name AS a_name
                                                    ,o.id AS o_id 
                                                    ,COUNT(o.price_offered) OVER(PARTITION BY a.id) as total_count
                                                FROM add_category AS c
                                                JOIN add_add AS a ON a.category_id = c.id
                                                JOIN add_offeredprice AS o ON a.id = o.add_id),
                                            y AS
                                                (SELECT
                                                    *
                                                    ,DENSE_RANK() OVER(PARTITION BY c_id ORDER BY total_count DESC) as rank
                                                FROM x)
                                            SELECT * FROM y
                                            WHERE y.rank <= 5''')
        temp_dict = {}
        for c in cat:
            if c.a_id not in temp_dict:
                temp_dict[c.a_id] = c
        return [t for t in temp_dict.values()]