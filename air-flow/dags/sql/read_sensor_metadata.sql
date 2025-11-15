select s.id as sensor_id, s.type as sensor_type, prod.id as product_id, prod.type as product_type,
       pers.last_name as last_name, pers.first_name as first_name, pers.patronymic as patronymic, pers.birthday as birthday
from sensor s
inner join product prod on prod.id = s.product_id
inner join person pers on pers.id = prod.person_id
where s.id in (?);