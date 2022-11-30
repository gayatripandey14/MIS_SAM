import datetime
from mongoengine import *
from mongoengine import signals

# from mongoengine import document
# from mongoengine.document import Document, DynamicDocument, DynamicEmbeddedDocument, EmbeddedDocument
# from mongoengine.fields import BooleanField, DateTimeField, EmailField, EmbeddedDocumentField, FloatField, IntField, ListField, ReferenceField, StringField
# from mongoengine.queryset.base import CASCADE


"""
for testing purpose created these three models
"""
class Comment(EmbeddedDocument):
    comment = StringField(max_length=70)
    
class Comments(Document):
    comment = StringField(max_length=70)

class NewTable(Document):
    name = StringField(max_length=50)
    comments = ListField(EmbeddedDocumentField(Comment))
    # comment_reference = ReferenceField(Comments)




ComposeSMSChoices = (
                ("Scheduled","Scheduled"),
                ("Draft","Draft"),
                ("Submitted","Submitted"),
                ("Stopped","Stopped"),
                ("Completed","Completed"))


userTypeChoices = (('Admin', 'Admin'),
        ('User', 'User'))

idProofChoices = (('Adhar Card',"Adhar Card"),
            ("Pan Card","Pan Card"),
            ("Driving License","Driving License"),
            ("Passport","Passport"))

groupTypeChoices = (("Family","Family"),
            ("Friends","Friends"),
            ("Personal","Personal"),
            ("Official","Official"),
            ("Client","Client"),
            ("Bussiness","Bussiness"),
            ("Promotion","Promotion"),
            ("Other","Other"))

smsTypeChoices = (("TextSMS","TextSMS"),
                ("Unicode","Unicode"))

senderDetailsChoices = (("Pending","Pending"),
                        ("Approved","Approved"),
                        ("Rejected","Rejected"))

composeSMScoding = (("English","English"),
                    ("Unicode","Unicode"))

# class kycDocuments(EmbeddedDocument):
#     file_path = StringField()


# class KYC(EmbeddedDocument):
#     id = SequenceField(primary_key=True)
#     address = StringField(max_length=200)
#     idProof = BooleanField(choices=idProofChoices)
#     date = DateTimeField()
#     Documents = ListField(EmbeddedDocumentField)

# class serviceDetails(DynamicEmbeddedDocument):
#     id = SequenceField(primary_key=True)
#     price = FloatField()
#     planType = BooleanField()


# class Services(Document):
#     id = SequenceField(primary_key=True)
#     name = StringField(max_length=50)
#     details = ListField(EmbeddedDocumentField(serviceDetails))
#     meta = {"allow_inheritance": True}
    

# class userServices(DynamicEmbeddedDocument):
#     id = SequenceField(primary_key=True)
#     name = StringField()
#     price = StringField()
#     expiry_date = DateTimeField()


# class Wallet(DynamicEmbeddedDocument):
#     id = SequenceField(primary_key=True)
#     credits = FloatField()


# class User(Document):
#     id = SequenceField(primary_key=True)
#     name = StringField(max_length=20)
#     email = EmailField()
#     phoneNo = IntField()
#     date = DateTimeField()
#     password = StringField(max_length=50)
#     userType = BooleanField(choices=userTypeChoices)
#     kyc = EmbeddedDocumentField(KYC)
#     company_name = StringField()
#     plan = ListField(EmbeddedDocumentField(userServices))
#     wallet = EmbeddedDocumentField(Wallet)
#     meta = {"allow_inheritance": True}



class User(Document):
    id = SequenceField(primary_key=True)
    user_id = IntField(unique=True)
    entity_id = StringField(default="0")
    smsc_id = StringField(default="celetel")
    dlr_mask = StringField(default="19")
    momt = StringField(default="MT")
    api_key = StringField(default="")
    # created_by = 


# class APIkey(Document):




class headerDetails(Document):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    date = DateTimeField(default=datetime.datetime.now())
    header = StringField(max_length=100)
    headerType = StringField(max_length=50,default="Explicit")
    # name = StringField(max_length=50)
    # tag = StringField(max_length=50)
    default = BooleanField(default=False)
    status = StringField(choices= senderDetailsChoices,default="Pending")
    
    meta = {"allow_inheritance": True}


class contactDetails(DynamicDocument):
    id = SequenceField(primary_key=True)
    user = StringField(max_length=100,required=True)
    group = StringField(max_length=100,required=True)
    number = StringField()
    valid = BooleanField()

    meta = {
        'indexes': [
            ('user','-group'),
            ('user','-number'),
            {'fields': ['user']},
        ]
    }


class contact_groups(Document):
    id = SequenceField(primary_key=True)
    name = StringField()
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    date = DateTimeField(default=datetime.datetime.now())
    totalContacts = IntField(default=0)
    invalidNumbers = IntField(default=0)
    validNumbers = IntField(default=0)
    duplicateNumbers = IntField(default=0)
    tag = StringField(default="")
    descirption = StringField(default="")


class Template(Document):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    templateId = StringField(max_length=50)
    templateName = StringField(max_length=100)
    date = DateTimeField(default=datetime.datetime.now())
    headerName = ReferenceField(headerDetails, reverse_delete_rule=CASCADE)
    # templateType = StringField()
    template = StringField()

    meta = {"allow_inheritance": True}


class ErrorCode(Document):
    id = SequenceField(primary_key=True)
    error_code = StringField()
    smsc_id = StringField()
    error_desc = StringField()
    category = StringField()
    display_error = StringField()
    status_flag = StringField()
    ui_grouping = StringField()
    error_description = StringField()



# class PhoneNumbers(DynamicDocument):
#     id = SequenceField(primary_key=True)
#     user = ReferenceField(User, reverse_delete_rule=CASCADE)
#     number = IntField(unique=True)
#     date = DateTimeField()


# class contactGroups(Document):
#     id = SequenceField(primary_key=True)
#     user = ReferenceField(User, reverse_delete_rule=CASCADE)
#     groupName = StringField(max_length=50,unique=True)
#     belongs_to = ListField(ReferenceField(PhoneNumbers, reverse_delete_rule=CASCADE),default=[])
#     groupTag = StringField()
#     groupType = StringField(choices=groupTypeChoices) # remove
#     groupDescription = StringField(max_length=200)
#     date = DateTimeField()
#     meta = {"allow_inheritance": True}


# class PaymentDetails(Document):
#     id = SequenceField(primary_key=True)
#     user = ReferenceField(User,reverse_delete_rule=CASCADE)
#     order_id = StringField()
#     payment_transaction_id = StringField()
#     total_amount = FloatField()
#     gst = StringField()
#     additional_charges = FloatField()
#     date = DateTimeField()
#     meta = {"allow_inheritance": True}

# class WalletLogs(Document):
#     id = SequenceField(primary_key=True)
#     user = ReferenceField(User,reverse_delete_rule=CASCADE)
#     credit = FloatField()
#     date = DateTimeField()
#     type = BooleanField()
#     action = BooleanField()
#     status = BooleanField()
#     comment = StringField(max_length=200)
#     meta = {"allow_inheritance": True}

# wallet in user service
# routes in sms service
# routes that will visible to all for buying 
# routes that a user a bought


###########
# class RouteDetails(Document):
#     id = SequenceField(primary_key=True)
#     name=StringField()
#     deduction = FloatField(default = 0.0)
#     # spend_limit = FloatField(default = 0.0)
#     total_sms = IntField(default=0)
#     date = DateTimeField(default=datetime.datetime.now())
#     description = StringField()
#     blocked = BooleanField(default=False)
#     expiry_date = DateTimeField()
#     expired = BooleanField(default=False)
    

# @route_signal.apply
# class Routing(Document):
#     id = SequenceField(primary_key=True)
#     routeDetails = ReferenceField(RouteDetails, reverse_delete_rule=CASCADE)
#     user = ReferenceField(User, reverse_delete_rule=CASCADE)
#     # spend_limit = FloatField(default = 0.0)
#     total_sms = IntField(default=0)
#     deduction = FloatField(default = 0.0)
#     date = DateTimeField(default=datetime.datetime.now())
#     blocked = BooleanField(default=False)
#     added_by = ReferenceField(User, reverse_delete_rule=CASCADE,default=None)
#     expiry_date = DateTimeField()
#     expired = BooleanField(default=False)
#     profit = FloatField(default = 0.0)
#     loss = FloatField(default = 0.0)
##############

# class campaignSchedules(EmbeddedDocument):
#     id = SequenceField(primary_key=True)
#     user = ReferenceField(User, reverse_delete_rule=CASCADE)
#     # composeSMS = ReferenceField(ComposeSMS,reverse_delete_rule=CASCADE)
#     date = DateTimeField()
#     status = BooleanField()
#     meta = {"allow_inheritance": True}


class Compose_headerDetails(EmbeddedDocument):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User)
    date = DateTimeField(default=datetime.datetime.now())
    header = StringField(max_length=10)
    headerType = StringField(max_length=50)
    header_id = IntField()
    # name = StringField(max_length=50)
    # tag = StringField(max_length=50)
    default = BooleanField()
    status = StringField(choices= senderDetailsChoices)




class Compose_Template(EmbeddedDocument):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User)
    templateId = StringField(max_length=100)
    templateName = StringField(max_length=100)
    date = DateTimeField(default=datetime.datetime.now())
    headerName = ReferenceField(headerDetails)
    # templateType = StringField()
    template = StringField()
    template_id = IntField()

class Compose_Routing(EmbeddedDocument):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User)
    total_sms = IntField(default=0)
    route_id = IntField()
    deduction = FloatField(default = 0.0)
    priority = IntField(default=1)
    date = DateTimeField(default=datetime.datetime.utcnow)
    name = StringField()

class Compose_contact_groups(EmbeddedDocument):
    id = SequenceField(primary_key=True)
    name = StringField()
    user = ReferenceField(User)
    date = DateTimeField(default=datetime.datetime.now())
    totalContacts = IntField(default=0)
    invalidNumbers = IntField(default=0)
    validNumbers = IntField(default=0)
    duplicateNumbers = IntField(default=0)
    group_id = IntField()
    tag = StringField(default="")
    descirption = StringField(default="")

class APIS(Document):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    header = EmbeddedDocumentField(Compose_headerDetails)
    template = EmbeddedDocumentField(Compose_Template)
    routing = EmbeddedDocumentField(Compose_Routing)
    date = DateTimeField(default=datetime.datetime.now())
    apikey = StringField(default="")


class ComposeSMS(Document):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    header = EmbeddedDocumentField(Compose_headerDetails)
    template = EmbeddedDocumentField(Compose_Template)
    routing = EmbeddedDocumentField(Compose_Routing)
    message=StringField()
    transaction_id = StringField(default="")
    date = DateTimeField()
    start_index = IntField(default=0)
    end_index = IntField(default=0)
    message_type = IntField()
    link_shortner = BooleanField(default=False)
    link = StringField()
    api = BooleanField()
    api_key = StringField(default="")
    campaing_name = StringField()
    contacts = ListField(default=[])
    all_contacts = ListField(default=[])
    numbers_to_send = IntField(default=0)
    total_amount = FloatField()
    duplicates = BooleanField(default=False)
    draft = BooleanField(default=False)
    tag = StringField(default="")
    group = EmbeddedDocumentListField(Compose_contact_groups,default=[])
    total_sms = IntField()
    characterSize = IntField(default=0)
    sent = IntField(default=0)
    started = DateTimeField(default=datetime.datetime.now())
    finished = DateTimeField(default=datetime.datetime.now())
    rejected = IntField(default=0)
    valid_numbers = IntField(default=0)
    invalid_numbers = IntField(default=0)
    duplicate_numbers = IntField(default=0)
    dnd_numbers = IntField(default=0)
    failed = IntField(default=0)
    total_pending = IntField()
    dnd = IntField(default=0)
    running = BooleanField(default=True)
    status = StringField(choices=ComposeSMSChoices)
    suspension_reason = StringField(default="")
    dlr_saved = BooleanField(default=False)
    deleted = BooleanField(default=False)
    meta = {
        "allow_inheritance": True,
        'indexes': [
            ("user","-transaction_id"),
        ]

        }

class campaignDrafts(Document):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    route = IntField(default=0)
    route_name = StringField(default="")
    route_deduction = FloatField(default=0)
    headerId = IntField(default=0)
    template = IntField(default=0)
    url_start_index = IntField(default=0)
    url_end_index = IntField(default=0)
    tag = StringField(default="")
    sms_content = StringField(default="")
    content_type = StringField(default="")
    campaignName = StringField(default="")
    link_shortner = BooleanField(default=False)
    link = StringField(default="")
    schedule = ListField(default=[])
    duplicate=BooleanField(default=False)
    group = ListField(default=[])
    contacts = ListField(default=[])



class DLR(Document):
    id = SequenceField(primary_key=True)
    msg_id = StringField(default="")
    # user = ReferenceField(User,reverse_delete_rule=CASCADE)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    composeSMS = ReferenceField(ComposeSMS,reverse_delete_rule=CASCADE)
    date = DateTimeField(default=datetime.datetime.now())
    reciever = StringField()
    err = StringField(default="")
    dlrvd = StringField(default="")
    sub = StringField(default="")
    message = StringField()
    response = StringField(default="")
    kannel_error_code = IntField(default=0)
    kannel_error = StringField(default="")
    unknown_elements = StringField(default="")
    error_code = StringField(default="")
    error_desc = StringField(default="")
    smsc_id = StringField(default="")
    momt = StringField(default="")
    dlr_mask = StringField(default="")
    done_date = StringField(default="")
    submit_date = StringField(default="")
    recieved = BooleanField(default=False)
    sent = BooleanField(default=False)
    status = StringField()
    meta = {
        "allow_inheritance": True,
        'indexes': [
            ("composeSMS"),
            ("composeSMS","-sent"),
            ("composeSMS","-user"),
            ("sent","-recieved"),
            ("composeSMS","-reciever")
        ]

        }


class campaignSchedules(Document):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    composeSMS = ReferenceField(ComposeSMS,reverse_delete_rule=CASCADE)
    date = DateTimeField()
    status = BooleanField(default=False)
    draft = BooleanField(default=False)
    meta = {"allow_inheritance": True}


class recentlyUsedGroups(Document):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    date = DateTimeField(default=datetime.datetime.now())
    composeSMS = ReferenceField(ComposeSMS,reverse_delete_rule=CASCADE)
    group = ListField(ReferenceField(contact_groups,reverse_delete_rule=CASCADE))
    total_sms = IntField(default=0)
    meta = {"allow_inheritance": True}



# rabbitMQ Producer broker consumer (kannel)
# kafka
# pyspark 

"""
INSERT INTO send_sms(momt,sender,receiver,msgdata,
smsc_id,dlr_mask,dlr_url,coding,meta_data) VALUES
"""




###########
class contactUs(Document):
    firstName = StringField()
    lastName = StringField()
    message = StringField()
    phoneNo = IntField()
    email = StringField()

class Career(Document):
    firstName = StringField()
    lastName = StringField()
    file = StringField()
    phoneNo = IntField()
    email = StringField()
    coverLatter = StringField()



###TEST####


class testtask(Document):
    id = SequenceField(primary_key=True)
    process_id = IntField()
    name = StringField()

class Roi(Document):
    id = SequenceField(primary_key=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    composeSMS =  ReferenceField(ComposeSMS, reverse_delete_rule=CASCADE)
    start_date = StringField()
    end_date = StringField()
    sale_input = FloatField()
    roi_result = FloatField()
    matched_roi = FloatField()
    unmatch_roi = FloatField()
    match_sales = FloatField()
    unmatch_sale = FloatField()
   
    meta = {
        "allow_inheritance": True,
        

        }

class roi_matched_number(Document):
    id = SequenceField(primary_key=True)
    user = StringField(max_length=100,required=True)
    composeSMS = ReferenceField(ComposeSMS,reverse_delete_rule=CASCADE)
    number = StringField()
    price = FloatField()
    name = StringField()
    valid = BooleanField()   
   


class roi_unmatched_number(Document):
    id = SequenceField(primary_key=True)
    user = StringField(max_length=100,required=True)
    composeSMS = ReferenceField(ComposeSMS,reverse_delete_rule=CASCADE)
    number = StringField()
    price = FloatField()
    name = StringField()
    valid = BooleanField()      