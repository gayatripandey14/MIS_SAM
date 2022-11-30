
# Create your models here.


"""

service(id) ---> smpps({id},{id},{id})

step 1
payload = {
    id:1
    k:0
    n:1
}

smpp --> [{id,service_id:1,name:"test",stop:false},{id:2,service_id:2,name:"test",stop:false},
                {id:3,service_id:1,name:"test",stop:false}]

fetch  from service_id eg. [1,2,3]


campaigns -- [{smpp_id:1},{smpp_id:1},{smpp_id:2},{smpp_id:3}]
fetch campaigns consisting that route id

fetch dlr and send it to kannel



"""